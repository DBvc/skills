#!/usr/bin/env bash
set -euo pipefail
# Usage: issue-workflow.sh [--expected-bundle-scheme SCHEME --expected-bundle-fingerprint HASH] <init|bundle-fingerprint|status|next|seal|review-ready|complete> <issue-id>
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
exec python3 "$SCRIPT_DIR/issue_workflow.py" "$@"
