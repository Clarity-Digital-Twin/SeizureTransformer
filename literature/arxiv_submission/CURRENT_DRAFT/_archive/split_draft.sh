#!/usr/bin/env bash
set -euo pipefail

SRC="CURRENT_WORKING_DRAFT.md"
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

if [[ ! -f "$SRC" ]]; then
  echo "Error: $SRC not found in $DIR" >&2
  exit 1
fi

get_line() {
  local pattern="$1"
  local ln
  ln=$(grep -n -m1 -E "^${pattern}$" "$SRC" | cut -d: -f1 || true)
  if [[ -z "$ln" ]]; then
    echo "Error: heading pattern not found: $pattern" >&2
    exit 2
  fi
  echo "$ln"
}

# Anchor headings (exact text as in the draft)
L_ABS=$(get_line "## Abstract")
L_INTRO=$(get_line "# Introduction")
L_BG=$(get_line "# Background and Related Work")
L_METHODS=$(get_line "# Methods")
L_RESULTS=$(get_line "# Results")
L_DISCUSS=$(get_line "# Discussion")
L_CONCL=$(get_line "# Conclusion")
L_REPRO=$(get_line "# Reproducibility and Resources")
L_ACK=$(get_line "# Acknowledgments")
L_REFS=$(get_line "# References")
L_APPX=$(get_line "# Appendix")

# Compute ranges (inclusive)
START=1
END_FRONT=$((L_ABS-1))
END_ABS=$((L_INTRO-1))
END_INTRO=$((L_BG-1))
END_BG=$((L_METHODS-1))
END_METHODS=$((L_RESULTS-1))
END_RESULTS=$((L_DISCUSS-1))
END_DISCUSS=$((L_CONCL-1))
END_CONCL=$((L_REPRO-1))
END_REPRO=$((L_ACK-1))
END_ACK=$((L_REFS-1))
END_REFS=$((L_APPX-1))
END_APPX=

# Extract helper
extract() {
  local from=$1 to=$2 out=$3
  if [[ -z "$to" ]]; then
    sed -n "${from},\$p" "$SRC" > "$out"
  else
    sed -n "${from},${to}p" "$SRC" > "$out"
  fi
}

extract "$START"     "$END_FRONT"   00_front_matter.md
extract "$L_ABS"     "$END_ABS"     01_abstract.md
extract "$L_INTRO"   "$END_INTRO"   02_introduction.md
extract "$L_BG"      "$END_BG"      03_background.md
extract "$L_METHODS" "$END_METHODS" 04_methods.md
extract "$L_RESULTS" "$END_RESULTS" 05_results.md
extract "$L_DISCUSS" "$END_DISCUSS" 06_discussion.md
extract "$L_CONCL"   "$END_CONCL"   07_conclusion.md
extract "$L_REPRO"   "$END_REPRO"   08_reproducibility.md
extract "$L_ACK"     "$END_ACK"     09_acknowledgments.md
extract "$L_REFS"    "$END_REFS"    10_references_from_draft.md
extract "$L_APPX"    "$END_APPX"    11_appendix.md

echo "Split complete: created 12 section files."

