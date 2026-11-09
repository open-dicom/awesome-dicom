"""Find entries in readme.md whose GitHub repositories are archived, moved, missing or inactive.

The archive policy in contributing.md moves a project to archive.md when its repository is
archived or deprecated, or its default branch has had no commits for about two years. This
script checks every GitHub repository linked from an entry. It writes a Markdown report and
exits with 1 if anything needs a maintainer's attention. Run from the repository root:

    GITHUB_TOKEN=... python3 .github/scripts/find_stale_entries.py readme.md report.md

Only GitHub links are checked. Projects hosted elsewhere (GitLab, Bitbucket, Mercurial or a
project's own site) need a manual check.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

GITHUB_API_URL = "https://api.github.com"
REQUEST_TIMEOUT_SECONDS = 30
INACTIVE_AFTER_DAYS = 730  # About two years, as in contributing.md's archive policy.
# Inactivity only matters for software. Datasets, learning resources and related lists have
# other bars, so only archived, moved or missing repositories are reported for them.
SECTIONS_CHECKED_FOR_INACTIVITY = frozenset({"Libraries", "Tools"})
TOP_LEVEL_HEADING_PATTERN = re.compile(r"^## (.+?)\s*$")
ENTRY_PATTERN = re.compile(r"^- \[(?P<name>[^\]]+)\]\(<?(?P<url>[^)\s>]+)>?\)")
GITHUB_REPOSITORY_PATTERN = re.compile(r"^https://github\.com/(?P<owner>[^/]+)/(?P<repository>[^/#?]+)")


@dataclass(frozen=True)
class LinkedRepository:
    """A GitHub repository linked from one entry of the list."""

    entry_name: str
    section: str
    slug: str


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
        if repository_link:
            slug = f"{repository_link.group('owner')}/{repository_link.group('repository')}"
            linked_repositories.append(LinkedRepository(entry.group("name"), section, slug))
    return linked_repositories


def fetch_github_json(api_path: str, token: str) -> dict | list | None:
    """Fetch one GitHub REST API path and decode its JSON.

    Parameters
    ----------
    api_path : str
        Path under the API root, such as ``/repos/pydicom/pydicom``.
    token : str
        A GitHub token, or an empty string for unauthenticated requests.

    Returns
    -------
    dict | list | None
        The decoded JSON, or None if GitHub answers 404 or 451.

    Raises
    ------
    urllib.error.HTTPError
        For any other HTTP error, such as an exhausted rate limit.
    """
    request = urllib.request.Request(f"{GITHUB_API_URL}{api_path}")
    request.add_header("Accept", "application/vnd.github+json")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if error.code in (404, 451):
            return None
        raise


def describe_problem(linked_repository: LinkedRepository, token: str, now: datetime) -> str | None:
    """Return what's wrong with one linked repository, or None if nothing is.

    Parameters
    ----------
    linked_repository : LinkedRepository
        The entry and the repository it links to.
    token : str
        A GitHub token, or an empty string.
    now : datetime
        The current time, in UTC.

    Returns
    -------
    str | None
        A short description of the problem, or None.
    """
    repository = fetch_github_json(f"/repos/{linked_repository.slug}", token)
    if repository is None:
        return "repository not found"
    if repository["archived"]:
        return "repository is archived"
    if repository["full_name"].lower() != linked_repository.slug.lower():
        return f"repository moved to {repository['full_name']}; update the link"
    if linked_repository.section not in SECTIONS_CHECKED_FOR_INACTIVITY:
        return None

    latest_commits = fetch_github_json(f"/repos/{linked_repository.slug}/commits?per_page=1", token)
    if not latest_commits:
        return "default branch has no commits"
    last_commit_date_text = latest_commits[0]["commit"]["committer"]["date"]
    last_commit_date = datetime.fromisoformat(last_commit_date_text.replace("Z", "+00:00"))
    if now - last_commit_date > timedelta(days=INACTIVE_AFTER_DAYS):
        return f"no commits on the default branch since {last_commit_date:%Y-%m-%d}"
    return None


def build_report(problems: list[tuple[LinkedRepository, str]], checked_count: int) -> str:
    """Write the Markdown report for the issue that tracks these problems.

    Parameters
    ----------
    problems : list[tuple[LinkedRepository, str]]
        Each entry that needs attention, with its problem.
    checked_count : int
        How many repositories were checked.

    Returns
    -------
    str
        The report, in Markdown.
    """
    archive_policy_link = "[archive policy](https://github.com/open-dicom/awesome-dicom/blob/main/contributing.md#archive)"
    if not problems:
        return f"All {checked_count} linked GitHub repositories are active and in place.\n"
    problem_lines = [
        f"- [ ] **{linked_repository.entry_name}** ({linked_repository.section}): "
        f"[{linked_repository.slug}](https://github.com/{linked_repository.slug}), {problem}."
        for linked_repository, problem in problems
    ]
    introduction = (
        f"The monthly check of {checked_count} linked GitHub repositories found {len(problems)} "
        f"that need attention. Under the {archive_policy_link}, an archived or inactive project moves "
        "to `archive.md`, unless it is widely used and stable rather than abandoned. A moved "
        "repository just needs its link updated."
    )
    return introduction + "\n\n" + "\n".join(problem_lines) + "\n"


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
        0 if nothing needs attention, 1 if something does, 2 if the check couldn't run.
    """
    token = os.environ.get("GITHUB_TOKEN", "")
    now = datetime.now(timezone.utc)
    try:
        linked_repositories = find_linked_repositories(readme_path)
    except OSError as error:
        print(f"::error::Can't read {readme_path}: {error}")
        return 2

    problems: list[tuple[LinkedRepository, str]] = []
    for linked_repository in linked_repositories:
        try:
            problem = describe_problem(linked_repository, token, now)
        except (urllib.error.URLError, TimeoutError) as error:
            print(f"::error::Couldn't check {linked_repository.slug}: {error}")
            return 2
        if problem:
            problems.append((linked_repository, problem))
            print(f"{linked_repository.entry_name}: {problem}")

    report = build_report(problems, len(linked_repositories))
    report_path.write_text(report, encoding="utf-8")
    print(report)
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: find_stale_entries.py README_PATH REPORT_PATH")
        sys.exit(2)
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
