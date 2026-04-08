from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from src.backtest import run_backtest
from src.orchestration import run_parallel_analysis

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env")

DEFAULT_TICKERS = ["NVDA", "TSLA", "JNJ", "KO"]


def _out_dir() -> Path:
    return REPO_ROOT / "outputs"


def _build_summary(results: list[dict]) -> dict:
    agreements = disagreements = 0
    rows = []
    names_a = names_b = names_c = None
    for r in results:
        names_a = r["strategy_a"]["name"]
        names_b = r["strategy_b"]["name"]
        names_c = r.get("strategy_c", {}).get("name")
        a, b = r["strategy_a"]["decision"], r["strategy_b"]["decision"]
        sc = r.get("strategy_c") or {}
        c = sc.get("decision")
        if c:
            unanimous = len({a, b, c}) == 1
        else:
            unanimous = a == b
        if unanimous:
            agreements += 1
        else:
            disagreements += 1
        rows.append(
            {
                "ticker": r["ticker"],
                "a_decision": a,
                "b_decision": b,
                "c_decision": c or "",
                "agree_core_ab": a == b,
                "unanimous": unanimous,
                "agree": unanimous,
            }
        )
    strategies = [names_a, names_b]
    if names_c:
        strategies.append(names_c)
    return {
        "strategies": strategies,
        "stocks_analyzed": [r["ticker"] for r in results],
        "total_agreements": agreements,
        "total_disagreements": disagreements,
        "results": rows,
        "note": "agree/unanimous reflects three agents when strategy_c present.",
    }


def main() -> None:
    p = argparse.ArgumentParser(description="StockTrader AutoGen + Ollama / LiteLLM")
    p.add_argument("--tickers", default=",".join(DEFAULT_TICKERS))
    p.add_argument("--backtest", action="store_true")
    p.add_argument("--skip-llm", action="store_true")
    p.add_argument(
        "--ticker-workers",
        type=int,
        default=2,
        help="Number of tickers to process concurrently (default: 2).",
    )
    args = p.parse_args()
    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    if args.skip_llm:
        os.environ["STOCKTRADER_SKIP_LLM"] = "1"

    async def _run() -> None:
        out = _out_dir()
        out.mkdir(parents=True, exist_ok=True)
        workers = max(1, args.ticker_workers)
        sem = asyncio.Semaphore(workers)

        async def _one(ticker: str) -> dict:
            async with sem:
                payload = await run_parallel_analysis(ticker)
                (out / f"{ticker}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
                return payload

        results = await asyncio.gather(*[_one(t) for t in tickers])
        (out / "summary.json").write_text(json.dumps(_build_summary(results), indent=2), encoding="utf-8")
        if args.backtest:
            bt = run_backtest(tickers)
            (out / "backtest.json").write_text(json.dumps(bt, indent=2), encoding="utf-8")

    asyncio.run(_run())


if __name__ == "__main__":
    main()


