from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Decision = Literal["BUY", "HOLD", "SELL"]


class StrategyStructured(BaseModel):
    decision: Decision
    confidence: int = Field(ge=1, le=10)
    justification: str = Field(
        description="3-5 sentences referencing specific numbers from the market payload."
    )


class EvaluatorStructured(BaseModel):
    agents_agree: bool
    analysis: str = Field(
        description="If strategies disagree, explain philosophical/data emphasis divergence; if agree, short consensus."
    )
    pattern_note: str | None = Field(
        default=None,
        description="Optional: three-way pattern (e.g. two buy, one hold).",
    )
