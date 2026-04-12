"""Strip echoed Alpha Vantage API keys from committed outputs/*.json (one-off / CI helper)."""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs"
# AV sometimes returns "API key as ABCDE12345" in Note/Information strings.
_KEY_ECHO = re.compile(r"(?i)\bAPI key as\s+[A-Za-z0-9]{8,48}\b")


def main() -> None:
    for path in sorted(OUT.glob("*.json")):
        if path.name in {"summary.json", "backtest.json"}:
            continue
        text = path.read_text(encoding="utf-8")
        new = _KEY_ECHO.sub("API key as [REDACTED]", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("redacted", path.name)


if __name__ == "__main__":
    main()
