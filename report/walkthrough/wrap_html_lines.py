# -*- coding: utf-8 -*-
"""Wrap long physical lines in HTML source (~100 cols) for editor readability.
Newlines in text/CSS lines do not change browser rendering for normal flow."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MAX = 100


def wrap_plain_line(line: str, max_len: int) -> list[str]:
    if len(line) <= max_len:
        return [line]
    m = re.match(r"^(\s*)(.*)$", line.rstrip("\n"))
    if not m:
        return [line]
    indent, rest = m.group(1), m.group(2)
    if "<" in rest or ">" in rest:
        return [line]
    if not rest.strip():
        return [line]
    words = rest.split()
    if not words:
        return [line]
    lines_out: list[str] = []
    cur = indent + words[0]
    for w in words[1:]:
        candidate = cur + " " + w
        if len(candidate) <= max_len:
            cur = candidate
        else:
            lines_out.append(cur)
            if len(indent + w) > max_len:
                lines_out.append(indent + w)
                cur = indent
            else:
                cur = indent + w
    if cur.strip() != "" or cur == indent:
        lines_out.append(cur)
    return lines_out if lines_out else [line]


def wrap_html_source(text: str, max_len: int = DEFAULT_MAX) -> str:
    lines = text.splitlines()
    ends_nl = text.endswith("\n")
    out: list[str] = []
    for line in lines:
        if len(line) > max_len:
            out.extend(wrap_plain_line(line, max_len))
        else:
            out.append(line)
    result = "\n".join(out)
    if ends_nl and not result.endswith("\n"):
        result += "\n"
    elif not ends_nl and out and result.endswith("\n"):
        result = result.rstrip("\n")
    return result


def process_file(path: Path, max_len: int = DEFAULT_MAX) -> bool:
    raw = path.read_text(encoding="utf-8")
    wrapped = wrap_html_source(raw, max_len)
    if wrapped != raw:
        path.write_text(wrapped, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    max_len = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MAX
    paths = sorted(ROOT.glob("**/*.html"))
    changed = 0
    for p in paths:
        if process_file(p, max_len):
            print("wrapped", p.relative_to(ROOT))
            changed += 1
    print(f"Done. {changed} file(s) updated.")


if __name__ == "__main__":
    main()
