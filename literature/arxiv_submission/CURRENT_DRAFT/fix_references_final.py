#!/usr/bin/env python3
"""
Final reference fix:
- Extract in-text citation order of first appearance across section files
- Renumber citations sequentially [1..N]
- Rewrite references list to match new order; drop uncited refs (best practice)
- Verify assembled draft has sequential first-appearance order

Safe for current folder structure.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

BASE = Path(__file__).resolve().parent

# Respect SECTION_ORDER; exclude references entry when enumerating in-text citations
ORDER_FILE = BASE / "SECTION_ORDER"
REFS_FILE = BASE / "10_references_from_draft.md"
ASSEMBLED = BASE / "CURRENT_WORKING_DRAFT_ASSEMBLED.md"


def load_section_list() -> List[Path]:
    files: List[Path] = []
    for line in ORDER_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        files.append(BASE / line)
    return files


def parse_in_text_order(section_paths: List[Path]) -> List[int]:
    # Citation pattern: [digits, digits ...] or ranges like [12-14]
    pat = re.compile(r"\[(?P<inner>[^\]]+)\]")
    digits_ok = re.compile(r"^[0-9,\-\s]+$")
    order: List[int] = []
    seen = set()
    for p in section_paths:
        if p.name == REFS_FILE.name:
            continue
        text = p.read_text(encoding="utf-8")
        for m in pat.finditer(text):
            inner = m.group("inner").strip()
            if not digits_ok.match(inner):
                continue
            parts = [x.strip() for x in inner.split(",") if x.strip()]
            for part in parts:
                if "-" in part:
                    a, b = part.split("-", 1)
                    if a.strip().isdigit() and b.strip().isdigit():
                        a_i, b_i = int(a), int(b)
                        rng = range(a_i, b_i + 1) if a_i <= b_i else range(b_i, a_i + 1)
                        for k in rng:
                            if k not in seen:
                                seen.add(k)
                                order.append(k)
                elif part.isdigit():
                    k = int(part)
                    if k not in seen:
                        seen.add(k)
                        order.append(k)
    return order


def parse_references() -> Dict[int, str]:
    refs: Dict[int, str] = {}
    for line in REFS_FILE.read_text(encoding="utf-8").splitlines():
        if not line.startswith("["):
            continue
        # [num] rest
        try:
            num_str, rest = line.split("]", 1)
        except ValueError:
            continue
        num = int(num_str[1:])
        refs[num] = f"[{num}]{rest}"
    return refs


def rewrite_sections(section_paths: List[Path], mapping: Dict[int, int]) -> None:
    pat = re.compile(r"\[(?P<inner>[^\]]+)\]")
    digits_ok = re.compile(r"^[0-9,\-\s]+$")

    def remap_inner(inner: str) -> str:
        parts = [x.strip() for x in inner.split(",") if x.strip()]
        out_parts: List[str] = []
        for part in parts:
            if "-" in part:
                a, b = part.split("-", 1)
                if a.strip().isdigit() and b.strip().isdigit():
                    a_i, b_i = int(a), int(b)
                    # expand, map, and then compress back to min-max sequential range only if contiguous
                    seq = [mapping.get(k, k) for k in (range(a_i, b_i + 1) if a_i <= b_i else range(b_i, a_i + 1))]
                    # Keep explicit list to avoid accidental resorting; do not re-compress
                    out_parts.extend([str(n) for n in seq])
                else:
                    out_parts.append(part)
            elif part.isdigit():
                out_parts.append(str(mapping.get(int(part), int(part))))
            else:
                out_parts.append(part)
        return ", ".join(out_parts)

    for p in section_paths:
        if p.name == REFS_FILE.name:
            continue
        text = p.read_text(encoding="utf-8")
        def repl(m: re.Match) -> str:
            inner = m.group("inner")
            if not digits_ok.match(inner.strip()):
                return m.group(0)
            return f"[{remap_inner(inner)}]"
        new_text = pat.sub(repl, text)
        if new_text != text:
            p.write_text(new_text, encoding="utf-8")


def rewrite_references(order: List[int], refs: Dict[int, str]) -> None:
    # Only keep cited references in order; renumber to [1..N]
    new_lines: List[str] = ["# References", ""]
    for new_idx, old in enumerate(order, start=1):
        src = refs.get(old)
        if not src:
            continue
        # replace leading [old] with [new_idx]
        _, rest = src.split("]", 1)
        new_lines.append(f"[{new_idx}]{rest}")
    REFS_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def verify_sequential(section_paths: List[Path]) -> Tuple[List[int], List[int]]:
    # Return (order_in_sections, refs_declared)
    order = parse_in_text_order(section_paths)
    declared: List[int] = []
    for line in REFS_FILE.read_text(encoding="utf-8").splitlines():
        if line.startswith("[") and "]" in line:
            n = int(line.split("]", 1)[0][1:])
            declared.append(n)
    return order, declared


def main() -> None:
    section_paths = load_section_list()
    # exclude references file to compute in-text order
    in_text_order = parse_in_text_order([p for p in section_paths if p.name != REFS_FILE.name])
    if not in_text_order:
        print("No in-text citations found; nothing to do.")
        return
    refs = parse_references()
    missing = [n for n in in_text_order if n not in refs]
    if missing:
        raise SystemExit(f"Citations missing in references list: {missing}")
    mapping = {old: new for new, old in enumerate(in_text_order, start=1)}
    # rewrite sections
    rewrite_sections(section_paths, mapping)
    # rewrite references
    rewrite_references(in_text_order, refs)
    # re-verify
    new_order, declared = verify_sequential(section_paths)
    print("Old first-appearance order:", in_text_order)
    print("New first-appearance order:", new_order)
    print("Declared refs:", declared)
    if new_order != list(range(1, len(new_order) + 1)):
        raise SystemExit("First-appearance order not sequential after rewrite.")
    print("OK: citations sequential and references aligned.")


if __name__ == "__main__":
    main()

