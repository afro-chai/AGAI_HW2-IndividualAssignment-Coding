from __future__ import annotations

import json
import re

from autogen_agentchat.agents import AssistantAgent

from src.llm_factory import build_chat_client
from src.schemas import EvaluatorStructured
from src.strategies import load_prompt


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
        analysis = out.analysis.strip()
        if unanimous and re.search(r"\bdisagree|do not align|diverge\b", analysis, flags=re.IGNORECASE):
            analysis = (
                "All strategy agents converge on the same decision for this ticker. "
                "They differ slightly in rationale emphasis, but the final recommendation is aligned."
            )
        if (not unanimous) and re.search(r"\ball\b.*\bagree|unanimous\b", analysis, flags=re.IGNORECASE):
            analysis = (
                "The strategy agents diverge on this ticker; disagreement reflects different philosophy-specific "
                "weighting of sentiment, volatility, and narrative-risk signals."
            )
        return out.model_copy(update={"agents_agree": unanimous, "analysis": analysis})
    finally:
        await client.close()
