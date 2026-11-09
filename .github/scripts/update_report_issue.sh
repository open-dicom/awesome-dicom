#!/usr/bin/env bash
# Keep one open issue per scheduled check in step with that check's latest result.
#
# Usage: update_report_issue.sh ISSUE_TITLE REPORT_FILE CHECK_EXIT_CODE
#
# - If the check found problems (exit code 1) it opens an issue titled ISSUE_TITLE with the
#   report as its body, or replaces the body of the open issue with that title.
# - If the check passed (exit code 0) it closes any open issue with that title, with a comment.
# - Any other exit code means the check itself failed, so the workflow run fails and no issue
#   is touched.
#
# Needs GH_TOKEN with issues: write, and GITHUB_REPOSITORY, both of which Actions provides.
set -euo pipefail

readonly CHECK_PASSED=0
readonly CHECK_FOUND_PROBLEMS=1

issue_title="$1"
report_file="$2"
check_exit_code="$3"

# Exact-title match: the search is fuzzy, so filter its results by title.
open_issue_number=$(
  gh issue list --repo "$GITHUB_REPOSITORY" --state open --search "\"$issue_title\" in:title" \
    --json number,title --jq "map(select(.title == \"$issue_title\")) | first | .number // empty"
)

case "$check_exit_code" in
  "$CHECK_FOUND_PROBLEMS")
    if [[ -n "$open_issue_number" ]]; then
      gh issue edit "$open_issue_number" --repo "$GITHUB_REPOSITORY" --body-file "$report_file"
      echo "Updated issue #$open_issue_number."
    else
      gh issue create --repo "$GITHUB_REPOSITORY" --title "$issue_title" --body-file "$report_file"
    fi
    ;;
  "$CHECK_PASSED")
    if [[ -n "$open_issue_number" ]]; then
      run_url="$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID"
      gh issue close "$open_issue_number" --repo "$GITHUB_REPOSITORY" \
        --comment "The latest run passed: $run_url"
      echo "Closed issue #$open_issue_number."
    else
      echo "The check passed and no issue is open."
    fi
    ;;
  *)
    echo "::error::The check itself failed (exit code $check_exit_code), so the issue was left alone."
    exit 1
    ;;
esac
