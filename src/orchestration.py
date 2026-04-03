from __future__ import annotations

import json
import os
from datetime import date
from typing import Any

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import StructuredMessage

from src.evaluator import run_evaluator
from src.llm_factory import build_chat_client
from src.market_data import build_market_payload
from src.schemas import StrategyStructured
from src.strategies import load_prompt, user_message_from_payload


async def _run_one_strategy(
    name: str,
    system_message: str,
    task: str,
    client_factory,
) -> StrategyStructured:
    if os.environ.get("STOCKTRADER_SKIP_LLM") == "1":
        return StrategyStructured(
            decision="HOLD",
            confidence=5,
            justification=f"Stub strategy {name} (set STOCKTRADER_SKIP_LLM=0 and run Ollama for real output).",
        )
    client = client_factory()
    try:
        agent = AssistantAgent(
            name=name,
            model_client=client,
            system_message=system_message,
            output_content_type=StrategyStructured,
        )
        res = await agent.run(task=task)
        for m in reversed(res.messages):
            if isinstance(m, StructuredMessage):
                return m.content  # type: ignore[return-value]
        raise RuntimeError(f"{name}: no structured output")
    finally:
        await client.close()


async def run_parallel_analysis(ticker: str) -> dict[str, Any]:
    payload = build_market_payload(ticker)
    task = user_message_from_payload(payload)

    news_sys = load_prompt("strategy_news_sentiment.txt")
    vol_sys = load_prompt("strategy_volatility_averse.txt")
    moral_sys = load_prompt("strategy_moral_trader.txt")

    # Parallel: each strategy gets its own model client to keep AutoGen agent state isolated.
    import asyncio

    cf = build_chat_client
    a, b, c = await asyncio.gather(
        _run_one_strategy("news_sentiment", news_sys, task, cf),
        _run_one_strategy("volatility_averse", vol_sys, task, cf),
        _run_one_strategy("moral_trader", moral_sys, task, cf),
    )

    strat_payloads = [
        {"name": "News Sentiment Follower", **a.model_dump()},
        {"name": "Volatility Averse", **b.model_dump()},
        {"name": "Moral Trader", **c.model_dump()},
    ]
    ev = await run_evaluator(strat_payloads)

    run_date = payload.get("market_data_summary", {}).get("run_date") or date.today().isoformat()
    return {
        "ticker": ticker,
        "run_date": run_date,
        "market_data_summary": payload["market_data_summary"],
        "news_features": payload.get("news_features"),
        "strategy_a": {
            "name": "News Sentiment Follower",
            "decision": a.decision,
            "confidence": a.confidence,
            "justification": a.justification,
        },
        "strategy_b": {
            "name": "Volatility Averse",
            "decision": b.decision,
            "confidence": b.confidence,
            "justification": b.justification,
        },
        "strategy_c": {
            "name": "Moral Trader",
            "decision": c.decision,
            "confidence": c.confidence,
            "justification": c.justification,
        },
        "evaluator": {
            "agents_agree": ev.agents_agree,
            "analysis": ev.analysis,
            "pattern_note": ev.pattern_note,
        },
    }
