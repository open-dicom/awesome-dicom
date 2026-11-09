"""Check readme.md for duplicated entries and headings, and for entries out of alphabetical order.

awesome-lint doesn't catch these. Duplicates can appear silently after a merge, because
.gitattributes merges readme.md with the union driver. Run from the repository root:

    python3 .github/scripts/check_list_structure.py readme.md

Exit codes: 0 when both checks pass, 1 when either finds a problem, 2 when the file can't be read.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

EXIT_PASSED = 0
EXIT_FOUND_PROBLEMS = 1
EXIT_CHECK_FAILED = 2

# Top-level sections whose groups must be in case-insensitive alphabetical order.
# Datasets and Learning Resources are deliberately unsorted.
SORTED_SECTIONS = frozenset({"Libraries", "Tools", "Hosted Tools", "Related Lists"})
HEADING_PATTERN = re.compile(r"^(#{2,4}) (.+?)\s*$")
ENTRY_PATTERN = re.compile(r"^- \[([^\]]+)\]")
TOP_LEVEL_HEADING_MARKS = "##"


def find_duplicate_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Return each repeated entry or heading line, with the line number of its second occurrence.

    Parameters
    ----------
    lines : list[str]
        The lines of readme.md, without trailing newlines.

    Returns
    -------
    list[tuple[int, str]]
        The 1-based line number of each repeat after the first, and the repeated line.
    """
    line_numbers_by_text: dict[str, list[int]] = defaultdict(list)
    for line_number, line in enumerate(lines, start=1):
        if ENTRY_PATTERN.match(line) or HEADING_PATTERN.match(line):
            line_numbers_by_text[line].append(line_number)
    return [
        (repeat_line_number, line)
        for line, line_numbers in line_numbers_by_text.items()
        for repeat_line_number in line_numbers[1:]
    ]


def find_unsorted_groups(lines: list[str]) -> list[tuple[int, str]]:
    """Return a message for each group of a sorted section whose entries are out of order.

    A group is the run of entries under one heading. Order is case-insensitive.

    Parameters
    ----------
    lines : list[str]
        The lines of readme.md, without trailing newlines.

    Returns
    -------
    list[tuple[int, str]]
        The 1-based line number of each unsorted group's heading, and a message naming the
        expected order.
    """
    problems: list[tuple[int, str]] = []
    top_level_section = ""
    group_heading = ""
    group_heading_line_number = 0
    entry_names: list[str] = []

    def check_group() -> None:
        """Record a problem if the group just finished is in a sorted section and out of order."""
        expected_order = sorted(entry_names, key=str.lower)
        if top_level_section in SORTED_SECTIONS and entry_names != expected_order:
            message = f"'{group_heading}' should be ordered: {', '.join(expected_order)}"
            problems.append((group_heading_line_number, message))

    for line_number, line in enumerate(lines, start=1):
        heading = HEADING_PATTERN.match(line)
        if heading:
            check_group()
            heading_marks, heading_text = heading.groups()
            if heading_marks == TOP_LEVEL_HEADING_MARKS:
                top_level_section = heading_text
            group_heading = heading_text
            group_heading_line_number = line_number
            entry_names = []
            continue
        entry = ENTRY_PATTERN.match(line)
        if entry:
            entry_names.append(entry.group(1))
    check_group()
    return problems


def main(readme_path: Path) -> int:
    """Run both checks on a readme and print what they find as GitHub annotations.

    Parameters
    ----------
    readme_path : Path
        Path to readme.md.

    Returns
    -------
    int
        EXIT_PASSED, EXIT_FOUND_PROBLEMS or EXIT_CHECK_FAILED.
    """
    try:
        lines = readme_path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        print(f"::error::Can't read {readme_path}: {error}")
        return EXIT_CHECK_FAILED

    duplicates = find_duplicate_lines(lines)
    unsorted_groups = find_unsorted_groups(lines)
    for line_number, duplicate in duplicates:
        print(f"::error file={readme_path},line={line_number}::Duplicated line: {duplicate}")
    for line_number, message in unsorted_groups:
        print(f"::error file={readme_path},line={line_number}::Out of alphabetical order: {message}")
    if duplicates or unsorted_groups:
        return EXIT_FOUND_PROBLEMS
    print("No duplicated entries or headings, and every sorted group is in order.")
    return EXIT_PASSED


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_list_structure.py README_PATH")
        sys.exit(EXIT_CHECK_FAILED)
    sys.exit(main(Path(sys.argv[1])))
