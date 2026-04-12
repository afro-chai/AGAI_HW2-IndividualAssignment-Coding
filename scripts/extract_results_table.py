"""One-off: print LaTeX table rows from outputs/*.json (not imported by app)."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs"
TICKERS = ["PLTR", "NVDA", "LMT", "RTX", "TTE", "E", "GOLD", "CRWD", "FRO", "NOC"]


def main() -> None:
    for t in TICKERS:
        d = json.loads((OUT / f"{t}.json").read_text(encoding="utf-8"))
        a, b, c = d["strategy_a"], d["strategy_b"], d.get("strategy_c") or {}
        ca, cb, cc = a["confidence"], b["confidence"], c.get("confidence", 0)
        sp = max(ca, cb, cc) - min(ca, cb, cc)
        print(
            f"    {t} & {a['decision']} & {ca} & {b['decision']} & {cb} & "
            f"{c.get('decision', '')} & {cc} & {sp} \\\\"
        )


if __name__ == "__main__":
    main()
