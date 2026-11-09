"""Find entries in readme.md whose GitHub repositories are archived, moved, missing or inactive.

The archive policy in contributing.md moves a project to archive.md when its repository is
archived or deprecated, or its default branch has had no commits for about two years. This
script checks every GitHub repository linked from an entry, but doesn't report inactivity for
those listed in .github/staleness-exceptions.txt. It writes a Markdown report. Run from the
repository root:

    GITHUB_TOKEN=... python3 .github/scripts/find_stale_entries.py readme.md report.md

Exit codes: 0 when nothing needs attention, 3 when the report lists problems, and 2 when the
check couldn't finish. Python itself exits with 1 on an uncaught error, so 1 also means the
check failed, never that it found problems.

Only GitHub links are checked. Projects hosted elsewhere (GitLab, Bitbucket, Mercurial or a
project's own site) need a manual check.
"""

from __future__ import annotations

import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

EXIT_ALL_CLEAR = 0
EXIT_CHECK_FAILED = 2
EXIT_FOUND_PROBLEMS = 3

GITHUB_API_URL = "https://api.github.com"
GITHUB_URL = "https://github.com"
ARCHIVE_POLICY_URL = "https://github.com/open-dicom/awesome-dicom/blob/main/contributing.md#archive"
EXCEPTIONS_PATH = Path(__file__).resolve().parent.parent / "staleness-exceptions.txt"

REQUEST_TIMEOUT_SECONDS = 30
REQUEST_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 10
RETRYABLE_STATUS_CODES = frozenset({500, 502, 503, 504})
NOT_FOUND_STATUS_CODES = frozenset({404, 451})
EMPTY_REPOSITORY_STATUS_CODE = 409  # GitHub answers 409 for the commits of an empty repository.

INACTIVE_AFTER_DAYS = 730  # About two years, as in contributing.md's archive policy.
# Inactivity only matters for software. Datasets, learning resources and related lists have
# other bars, so only archived, moved or missing repositories are reported for them.
SECTIONS_CHECKED_FOR_INACTIVITY = frozenset({"Libraries", "Tools"})

TOP_LEVEL_HEADING_PATTERN = re.compile(r"^## (.+?)\s*$")
# An entry: "- [Name](url)", with an optional <...> around the URL and an optional quoted title.
ENTRY_PATTERN = re.compile(
    r"^- \[(?P<name>[^\]]+)\]\(<?(?P<url>[^)\s>]+)>?(?:\s+(?:\"[^\"]*\"|'[^']*'))?\)"
)
GITHUB_REPOSITORY_PATTERN = re.compile(
    r"^https?://(?:www\.)?github\.com/(?P<owner>[^/]+)/(?P<repository>[^/#?]+)", re.IGNORECASE
)
# github.com paths that look like owner/repository but aren't repositories.
RESERVED_GITHUB_OWNERS = frozenset(
    {
        "apps", "collections", "explore", "features", "marketplace", "orgs",
        "search", "sponsors", "topics", "trending", "users",
    }
)


@dataclass(frozen=True)
class LinkedRepository:
    """A GitHub repository linked from one entry of the list."""

    entry_name: str
    section: str
    slug: str


class GitHubApiError(Exception):
    """Raised when the GitHub API can't answer, even after retries."""


def find_linked_repositories(readme_path: Path) -> list[LinkedRepository]:
    """List the GitHub repository that each entry links to, with the entry's top-level section.

    Parameters
    ----------
    readme_path : Path
        Path to readme.md.

    Returns
    -------
    list[LinkedRepository]
        One item per entry whose link points into a GitHub repository.
    """
    linked_repositories: list[LinkedRepository] = []
    section = ""
    for line in readme_path.read_text(encoding="utf-8").splitlines():
        heading = TOP_LEVEL_HEADING_PATTERN.match(line)
        if heading:
            section = heading.group(1)
            continue
        entry = ENTRY_PATTERN.match(line)
        if not entry:
            continue
        repository_link = GITHUB_REPOSITORY_PATTERN.match(entry.group("url"))
        if not repository_link or repository_link.group("owner").lower() in RESERVED_GITHUB_OWNERS:
            continue
        repository_name = repository_link.group("repository").removesuffix(".git")
        slug = f"{repository_link.group('owner')}/{repository_name}"
        linked_repositories.append(LinkedRepository(entry.group("name"), section, slug))
    return linked_repositories


def load_inactivity_exceptions(exceptions_path: Path) -> frozenset[str]:
    """Read the slugs of repositories that are kept on purpose despite inactivity.

    Parameters
    ----------
    exceptions_path : Path
        A text file with one ``owner/name`` slug per line, followed by a reason. Blank lines
        and lines starting with ``#`` are ignored. A missing file means no exceptions.

    Returns
    -------
    frozenset[str]
        The slugs, lower-cased.
    """
    if not exceptions_path.exists():
        return frozenset()
    slugs: set[str] = set()
    for line in exceptions_path.read_text(encoding="utf-8").splitlines():
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith("#"):
            slugs.add(stripped_line.split()[0].lower())
    return frozenset(slugs)


def fetch_github_json(api_path: str, token: str) -> tuple[int, Any]:
    """Fetch one GitHub REST API path, retrying server and connection errors.

    Parameters
    ----------
    api_path : str
        Path under the API root, such as ``/repos/pydicom/pydicom``.
    token : str
        A GitHub token, or an empty string for unauthenticated requests.

    Returns
    -------
    tuple[int, Any]
        The HTTP status and the decoded JSON. For 404, 409 and 451 the JSON is None, and the
        caller decides what the status means.

    Raises
    ------
    GitHubApiError
        If GitHub keeps failing, or answers with any other error status.
    """
    request = urllib.request.Request(f"{GITHUB_API_URL}{api_path}")
    request.add_header("Accept", "application/vnd.github+json")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    last_error = ""
    for attempt in range(1, REQUEST_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            if error.code in NOT_FOUND_STATUS_CODES or error.code == EMPTY_REPOSITORY_STATUS_CODE:
                return error.code, None
            if error.code not in RETRYABLE_STATUS_CODES:
                raise GitHubApiError(f"{api_path}: HTTP {error.code}") from error
            last_error = f"HTTP {error.code}"
        except (http.client.HTTPException, OSError) as error:  # OSError covers URLError and timeouts.
            last_error = str(error)
        if attempt < REQUEST_ATTEMPTS:
            time.sleep(RETRY_DELAY_SECONDS)
    raise GitHubApiError(f"{api_path}: {last_error} after {REQUEST_ATTEMPTS} attempts")


def find_last_commit_date(slug: str, token: str) -> datetime | None:
    """Return the date of the latest commit on a repository's default branch.

    Parameters
    ----------
    slug : str
        The repository, as ``owner/name``.
    token : str
        A GitHub token, or an empty string.

    Returns
    -------
    datetime | None
        The committer date, or None if the repository has no commits.

    Raises
    ------
    GitHubApiError
        If GitHub can't answer, or answers the commits request with an unexpected status.
    """
    status, latest_commits = fetch_github_json(f"/repos/{slug}/commits?per_page=1", token)
    if status == EMPTY_REPOSITORY_STATUS_CODE or latest_commits == []:
        return None
    if latest_commits is None:
        raise GitHubApiError(f"/repos/{slug}/commits: HTTP {status}")
    last_commit_date_text = latest_commits[0]["commit"]["committer"]["date"]
    return datetime.fromisoformat(last_commit_date_text.replace("Z", "+00:00"))


def describe_repository_problem(slug: str, token: str) -> str | None:
    """Return why a repository's link needs attention whatever its activity, or None.

    Parameters
    ----------
    slug : str
        The repository, as ``owner/name``.
    token : str
        A GitHub token, or an empty string.

    Returns
    -------
    str | None
        "repository not found", "repository is archived", a note that it moved, or None.

    Raises
    ------
    GitHubApiError
        If GitHub can't answer, or answers the repository request with an unexpected status.
    """
    status, repository = fetch_github_json(f"/repos/{slug}", token)
    if status in NOT_FOUND_STATUS_CODES:
        return "repository not found"
    if repository is None:
        raise GitHubApiError(f"/repos/{slug}: HTTP {status}")
    if repository["archived"]:
        return "repository is archived"
    if repository["full_name"].lower() != slug.lower():
        return f"repository moved to {repository['full_name']}; update the link"
    return None


def describe_inactivity(slug: str, token: str, now: datetime) -> str | None:
    """Return a note if a repository's default branch has been inactive too long, or None.

    Parameters
    ----------
    slug : str
        The repository, as ``owner/name``.
    token : str
        A GitHub token, or an empty string.
    now : datetime
        The current time, in UTC.

    Returns
    -------
    str | None
        A note naming the date of the last commit, or None if the branch is active.
    """
    last_commit_date = find_last_commit_date(slug, token)
    if last_commit_date is None:
        return "default branch has no commits"
    if now - last_commit_date > timedelta(days=INACTIVE_AFTER_DAYS):
        return f"no commits on the default branch since {last_commit_date:%Y-%m-%d}"
    return None


def build_report(problems: list[tuple[LinkedRepository, str]], entry_count: int, repository_count: int) -> str:
    """Write the Markdown report for the issue that tracks these problems.

    Parameters
    ----------
    problems : list[tuple[LinkedRepository, str]]
        Each entry that needs attention, with its problem.
    entry_count : int
        How many entries link to a GitHub repository.
    repository_count : int
        How many distinct repositories those entries link to.

    Returns
    -------
    str
        The report, in Markdown.
    """
    entry_noun = "entry" if entry_count == 1 else "entries"
    repository_noun = "repository" if repository_count == 1 else "repositories"
    checked_summary = f"{entry_count} {entry_noun} linking {repository_count} GitHub {repository_noun}"
    if not problems:
        return f"Checked {checked_summary}. Nothing needs attention.\n"
    attention_verb = "needs" if len(problems) == 1 else "need"
    introduction = (
        f"Checked {checked_summary}. {len(problems)} {attention_verb} attention. "
        f"Under the [archive policy]({ARCHIVE_POLICY_URL}), an archived or inactive project moves "
        "to `archive.md`, unless it is widely used and stable rather than abandoned; list such a "
        "project in `.github/staleness-exceptions.txt`. A moved repository just needs its link updated."
    )
    problem_lines = [
        f"- [ ] **{linked_repository.entry_name}** ({linked_repository.section}): "
        f"[{linked_repository.slug}]({GITHUB_URL}/{linked_repository.slug}), {problem}."
        for linked_repository, problem in problems
    ]
    return introduction + "\n\n" + "\n".join(problem_lines) + "\n"


def find_problems(
    linked_repositories: list[LinkedRepository], inactivity_exceptions: frozenset[str], token: str
) -> list[tuple[LinkedRepository, str]]:
    """Check each linked repository once, and list the entries that need attention.

    Parameters
    ----------
    linked_repositories : list[LinkedRepository]
        Every entry that links to a GitHub repository.
    inactivity_exceptions : frozenset[str]
        Lower-cased slugs kept on purpose, so their inactivity isn't reported.
    token : str
        A GitHub token, or an empty string.

    Returns
    -------
    list[tuple[LinkedRepository, str]]
        Each entry that needs attention, with its problem.
    """
    now = datetime.now(timezone.utc)
    problem_by_slug: dict[str, str | None] = {}
    problems: list[tuple[LinkedRepository, str]] = []
    for linked_repository in linked_repositories:
        slug_key = linked_repository.slug.lower()
        if slug_key not in problem_by_slug:
            problem_by_slug[slug_key] = describe_repository_problem(linked_repository.slug, token)
        problem = problem_by_slug[slug_key]
        is_checked_for_inactivity = (
            linked_repository.section in SECTIONS_CHECKED_FOR_INACTIVITY and slug_key not in inactivity_exceptions
        )
        if problem is None and is_checked_for_inactivity:
            problem = describe_inactivity(linked_repository.slug, token, now)
        if problem:
            problems.append((linked_repository, problem))
            print(f"{linked_repository.entry_name}: {problem}")
    return problems


def main(readme_path: Path, report_path: Path) -> int:
    """Check every linked GitHub repository and write the report.

    Parameters
    ----------
    readme_path : Path
        Path to readme.md.
    report_path : Path
        Where to write the Markdown report.

    Returns
    -------
    int
        EXIT_ALL_CLEAR, EXIT_FOUND_PROBLEMS or EXIT_CHECK_FAILED.
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    # Anything not caught here, such as an unexpected API response, crashes with a traceback
    # and exit code 1, which the workflow also treats as a failed check.
    try:
        linked_repositories = find_linked_repositories(readme_path)
        inactivity_exceptions = load_inactivity_exceptions(EXCEPTIONS_PATH)
    except OSError as error:
        print(f"::error::Can't read the list or the exceptions file: {error}")
        return EXIT_CHECK_FAILED
    if not linked_repositories:
        print(f"::error::Found no entries linking GitHub repositories in {readme_path}.")
        return EXIT_CHECK_FAILED

    try:
        problems = find_problems(linked_repositories, inactivity_exceptions, token)
    except GitHubApiError as error:
        print(f"::error::The staleness check couldn't finish: {error}")
        return EXIT_CHECK_FAILED
    repository_count = len({linked_repository.slug.lower() for linked_repository in linked_repositories})
    report = build_report(problems, len(linked_repositories), repository_count)
    try:
        report_path.write_text(report, encoding="utf-8")
    except OSError as error:
        print(f"::error::Can't write the report to {report_path}: {error}")
        return EXIT_CHECK_FAILED
    print(report)
    return EXIT_FOUND_PROBLEMS if problems else EXIT_ALL_CLEAR


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: find_stale_entries.py README_PATH REPORT_PATH")
        sys.exit(EXIT_CHECK_FAILED)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
