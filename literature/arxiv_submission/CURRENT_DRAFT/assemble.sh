#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

ORDER_FILE="SECTION_ORDER"
OUT="CURRENT_WORKING_DRAFT_ASSEMBLED.md"

if [[ ! -f "$ORDER_FILE" ]]; then
  echo "Error: $ORDER_FILE not found" >&2
  exit 1
fi

> "$OUT"
first=1
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  if [[ ! -f "$f" ]]; then
    echo "Error: section file missing: $f" >&2
    exit 2
  fi
  if [[ $first -eq 1 ]]; then
    cat "$f" >> "$OUT"
    first=0
  else
    # Avoid injecting an extra blank line; rely on section file's own trailing newline
    cat "$f" >> "$OUT"
  fi
done < "$ORDER_FILE"

echo "Assembled into $OUT"
