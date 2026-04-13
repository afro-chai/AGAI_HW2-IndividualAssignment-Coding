from __future__ import annotations

import json
import re

from autogen_agentchat.agents import AssistantAgent

from src.llm_factory import build_chat_client
from src.schemas import EvaluatorStructured
from src.strategies import load_prompt


def _decisions(outputs: list[dict]) -> tuple[str, str, str]:
    return (
        outputs[0]["decision"],
        outputs[1]["decision"],
        outputs[2]["decision"],
    )


def _pattern_note_from_decisions(outputs: list[dict]) -> str:
    """Deterministic summary so JSON always matches actual News / Vol / Moral votes."""
    n, v, m = _decisions(outputs)
    if n == v == m:
        return f"Unanimous {n} (News, Vol, Moral)"
    if n == v:
        return f"News & Vol {n}; Moral {m}"
    if n == m:
        return f"News & Moral {n}; Vol {v}"
    if v == m:
        return f"Vol & Moral {v}; News {n}"
    return f"News {n} · Vol {v} · Moral {m}"


def _graded_agree(outputs: list[dict]) -> bool:
    return outputs[0]["decision"] == outputs[1]["decision"]


def _unanimous_three(outputs: list[dict]) -> bool:
    return len({o["decision"] for o in outputs}) == 1


def evaluator_task(outputs: list[dict]) -> str:
    lines = [json.dumps(o, indent=2) for o in outputs]
    body = "\n---\n".join(lines)
    agree3 = _unanimous_three(outputs)
    agree_ab = _graded_agree(outputs)
    n, v, m = _decisions(outputs)

    if agree3:
        branch = (
            "BRANCH: FULL AGREEMENT — all three decisions are identical.\n"
            f"Shared action: {n}.\n"
            "Explain why three different philosophies (headlines, tail risk, narrative/governance) still landed on the same action. "
            "Contrast what each strategy *emphasized* in its justification, not merely that they match.\n"
        )
    elif agree_ab:
        branch = (
            "BRANCH: GRADED PAIR AGREES — News and Volatility share the same decision but Moral may differ.\n"
            f"News={n}, Vol={v}, Moral={m}.\n"
            "Explain why the two graded strategies converged on the same side, and what Moral adds or disputes.\n"
        )
    else:
        branch = (
            "BRANCH: GRADED DISAGREEMENT — News and Volatility differ.\n"
            f"News={n}, Vol={v}, Moral={m}.\n"
            "Explain the *substantive* reason the headline-oriented agent and the tail-risk-oriented agent diverge on this tape. "
            "Tie the split to concrete themes in their justifications (e.g. missing news vs turbulence thresholds), "
            "not to a play-by-play of BUY/HOLD/SELL labels alone.\n"
        )

    return (
        "Compare the following independent strategy results for the SAME stock.\n"
        + branch
        + "Respond using the structured output schema only. Leave pattern_note empty or very short; routing text above is for you only.\n\n"
        + body
    )


async def run_evaluator(outputs: list[dict]) -> EvaluatorStructured:
    import os

    if os.environ.get("STOCKTRADER_SKIP_LLM") == "1":
        agree = _unanimous_three(outputs)
        return EvaluatorStructured(
            agents_agree=agree,
            analysis="Stub evaluator (STOCKTRADER_SKIP_LLM=1). Replace with live Ollama run.",
            pattern_note=_pattern_note_from_decisions(outputs),
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
        unanimous = _unanimous_three(outputs)
        analysis = out.analysis.strip()
        if unanimous and re.search(r"\bdisagree|do not align|diverge\b", analysis, flags=re.IGNORECASE):
            analysis = (
                "All three strategies reached the same action; the split to highlight is in *how* they reasoned—"
                "news availability vs realized risk metrics vs governance framing—not disagreement on the label."
            )
        if (not unanimous) and re.search(
            r"\ball\b.*\bagree|unanimous|converge on the same\b", analysis, flags=re.IGNORECASE
        ):
            analysis = (
                "The strategies do not fully align on this ticker. The meaningful comparison is which inputs each philosophy "
                "treated as decisive (sentiment and momentum language vs turbulence and drawdown gates vs narrative risk), "
                "which explains why recommendations diverge despite one shared market JSON."
            )
        note = _pattern_note_from_decisions(outputs)
        return EvaluatorStructured(
            agents_agree=unanimous,
            analysis=analysis,
            pattern_note=note,
        )
    finally:
        await client.close()
