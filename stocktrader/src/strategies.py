from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_prompt(name: str) -> str:
    path = ROOT / "prompts" / name
    return path.read_text(encoding="utf-8")


def user_message_from_payload(payload: dict) -> str:
    """Single user turn: JSON market context only (no peer strategy outputs)."""
    slim = {
        "ticker": payload.get("ticker"),
        "market_data_summary": payload.get("market_data_summary"),
        "news_features": payload.get("news_features"),
        "ohlc_note": payload.get("ohlc_note"),
    }
    return (
        "You are given fresh market context as JSON. Respond ONLY using the structured output schema.\n\n"
        + json.dumps(slim, indent=2)
    )
