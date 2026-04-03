from __future__ import annotations

import json

from autogen_agentchat.agents import AssistantAgent

from stocktrader.src.llm_factory import build_chat_client
from stocktrader.src.schemas import EvaluatorStructured
from stocktrader.src.strategies import load_prompt


def evaluator_task(strategy_outputs: list[dict]) -> str:
    lines = [json.dumps(o, indent=2) for o in strategy_outputs]
    body = "\n---\n".join(lines)
    return (
        "Compare the following independent strategy results for the SAME stock. "
        "Explain agreement or disagreement in terms of philosophy and data emphasis. "
        "Respond using the structured output schema only.\n\n"
        + body
    )


async def run_evaluator(outputs: list[dict]) -> EvaluatorStructured:
    import os
    if os.environ.get("STOCKTRADER_SKIP_LLM") == "1":
        agree = len({o["decision"] for o in outputs}) == 1
        return EvaluatorStructured(
            agents_agree=agree,
            analysis="Stub evaluator (STOCKTRADER_SKIP_LLM=1). Replace with live Ollama run.",
            pattern_note="stub",
        )
    client = build_chat_client()
    try:
        agent = AssistantAgent(
            name="evaluator",
            model_client=client,
            system_message=load_prompt("evaluator.txt"),
            output_content_type=EvaluatorStructured,
        )
        res = await agent.run(task=evaluator_task(outputs))
        from autogen_agentchat.messages import StructuredMessage

        for m in reversed(res.messages):
            if isinstance(m, StructuredMessage):
                out = m.content  # type: ignore[assignment]
                break
        else:
            raise RuntimeError("evaluator: no StructuredMessage")
        unanimous = len({o["decision"] for o in outputs}) == 1
        return out.model_copy(update={"agents_agree": unanimous})
    finally:
        await client.close()
