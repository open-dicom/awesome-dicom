#!/usr/bin/env bash
# Keep one open issue per scheduled check in step with that check's latest result.
#
# Usage: update_report_issue.sh ISSUE_TITLE REPORT_FILE CHECK_STATUS
#
# CHECK_STATUS is one of:
# - found-problems: open an issue titled ISSUE_TITLE with REPORT_FILE as its body, or replace
#   the body of the open issue with that title. If several are open, the oldest is updated.
# - passed: close every open issue with that title, with a comment linking the run.
# - anything else: the check itself failed, so fail this step and leave issues alone.
#
# Needs GH_TOKEN with issues: write, which the workflow sets, plus GITHUB_REPOSITORY,
# GITHUB_SERVER_URL and GITHUB_RUN_ID, which Actions provides. Uses gh and jq.
set -euo pipefail

readonly STATUS_PASSED="passed"
readonly STATUS_FOUND_PROBLEMS="found-problems"
readonly OPEN_ISSUE_LIMIT=500

issue_title="$1"
report_file="$2"
check_status="$3"

# List open issues directly rather than through search, which can lag, and match the exact title.
matching_issue_numbers=$(
  gh issue list --repo "$GITHUB_REPOSITORY" --state open --limit "$OPEN_ISSUE_LIMIT" --json number,title |
    jq -r --arg title "$issue_title" 'map(select(.title == $title)) | sort_by(.number) | .[].number'
)

case "$check_status" in
  "$STATUS_FOUND_PROBLEMS")
    if ! grep -q '[^[:space:]]' "$report_file" 2>/dev/null; then
      echo "::error::The check reported problems but wrote no report to $report_file."
      exit 1
    fi
    oldest_issue_number=$(head -n 1 <<<"$matching_issue_numbers")
    if [[ -n "$oldest_issue_number" ]]; then
      gh issue edit "$oldest_issue_number" --repo "$GITHUB_REPOSITORY" --body-file "$report_file"
      echo "Updated issue #$oldest_issue_number."
    else
      gh issue create --repo "$GITHUB_REPOSITORY" --title "$issue_title" --body-file "$report_file"
    fi
    ;;
  "$STATUS_PASSED")
    run_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
    if [[ -z "$matching_issue_numbers" ]]; then
      echo "The check passed and no issue is open."
    fi
    for issue_number in $matching_issue_numbers; do
      gh issue close "$issue_number" --repo "$GITHUB_REPOSITORY" --comment "The latest run passed: $run_url"
      echo "Closed issue #$issue_number."
    done
    ;;
  *)
    echo "::error::The check itself failed (status '$check_status'), so issues were left alone."
    exit 1
    ;;
esac
