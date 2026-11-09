"""Check readme.md for duplicated entries and headings, and for entries out of alphabetical order.

awesome-lint doesn't catch these. Duplicates can appear silently after a merge, because
.gitattributes merges readme.md with the union driver. Run from the repository root:

    python3 .github/scripts/check_list_structure.py readme.md
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

# Top-level sections whose groups must be in case-insensitive alphabetical order.
# Datasets and Learning Resources are deliberately unsorted.
SORTED_SECTIONS = frozenset({"Libraries", "Tools", "Hosted Tools", "Related Lists"})
HEADING_PATTERN = re.compile(r"^(#{2,4}) (.+?)\s*$")
ENTRY_PATTERN = re.compile(r"^- \[([^\]]+)\]")
TOP_LEVEL_HEADING_MARKS = "##"


def find_duplicate_lines(lines: list[str]) -> list[str]:
    """Return entry and heading lines that appear more than once.

    Parameters
    ----------
    lines : list[str]
        The lines of readme.md, without trailing newlines.

    Returns
    -------
    list[str]
        Each duplicated entry or heading line, once.
    """
    checked_lines = [line for line in lines if ENTRY_PATTERN.match(line) or HEADING_PATTERN.match(line)]
    line_counts = Counter(checked_lines)
    return [line for line, count in line_counts.items() if count > 1]


def find_unsorted_groups(lines: list[str]) -> list[str]:
    """Return a message for each group of a sorted section whose entries are out of order.

    A group is the run of entries under one heading. Order is case-insensitive.

    Parameters
    ----------
    lines : list[str]
        The lines of readme.md, without trailing newlines.

    Returns
    -------
    list[str]
        One message per unsorted group, naming the heading and the expected order.
    """
    problems: list[str] = []
    top_level_section = ""
    group_heading = ""
    entry_names: list[str] = []

    def check_group() -> None:
        expected_order = sorted(entry_names, key=str.lower)
        if top_level_section in SORTED_SECTIONS and entry_names != expected_order:
            problems.append(f"'{group_heading}' should be ordered: {', '.join(expected_order)}")

    for line in lines:
        heading = HEADING_PATTERN.match(line)
        if heading:
            check_group()
            heading_marks, heading_text = heading.groups()
            if heading_marks == TOP_LEVEL_HEADING_MARKS:
                top_level_section = heading_text
            group_heading = heading_text
            entry_names = []
            continue
        entry = ENTRY_PATTERN.match(line)
        if entry:
            entry_names.append(entry.group(1))
    check_group()
    return problems


def main(readme_path: Path) -> int:
    """Run both checks on a readme and print what they find.

    Parameters
    ----------
    readme_path : Path
        Path to readme.md.

    Returns
    -------
    int
        0 if both checks pass, 1 if either finds a problem, 2 if the file can't be read.
    """
    try:
        lines = readme_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        print(f"::error::Can't read {readme_path}: {error}")
        return 2

    duplicates = find_duplicate_lines(lines)
    unsorted_groups = find_unsorted_groups(lines)
    for duplicate in duplicates:
        print(f"::error file={readme_path}::Duplicated line: {duplicate}")
    for problem in unsorted_groups:
        print(f"::error file={readme_path}::Out of alphabetical order: {problem}")
    if duplicates or unsorted_groups:
        return 1
    print("No duplicated entries or headings, and every sorted group is in order.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_list_structure.py README_PATH")
        sys.exit(2)
    sys.exit(main(Path(sys.argv[1])))
