from __future__ import annotations

from typing import Any, Literal

import pandas as pd
import yfinance as yf

from stocktrader.src.market_data import market_payload_asof

Decision = Literal["BUY", "HOLD", "SELL"]


def _signal_news_proxy(payload: dict) -> Decision:
    nf = payload.get("news_features") or {}
    score = nf.get("avg_sentiment_score")
    if score is not None:
        if score >= 0.15:
            return "BUY"
        if score <= -0.15:
            return "SELL"
        return "HOLD"
    r5 = payload.get("market_data_summary", {}).get("return_5d", 0) or 0
    if r5 > 0.03:
        return "BUY"
    if r5 < -0.03:
        return "SELL"
    return "HOLD"


def _signal_vol_averse(payload: dict) -> Decision:
    s = payload.get("market_data_summary", {})
    std = float(s.get("std_daily_return_90d") or 0)
    max_drop = float(s.get("max_single_day_drop_90d") or 0)
    atr = s.get("atr_14")
    vol_score = std + abs(min(0, max_drop)) * 0.5
    if vol_score < 0.012 and (atr is None or atr < s.get("current_price", 1) * 0.02):
        return "BUY"
    if vol_score > 0.028 or max_drop < -0.06:
        return "SELL"
    return "HOLD"


def _forward_return(hist: pd.DataFrame, asof: pd.Timestamp, days: int = 20) -> float | None:
    future = hist.loc[asof:]
    if len(future) <= days:
        return None
    p0 = float(future.iloc[0]["Close"])
    p1 = float(future.iloc[days]["Close"])
    return (p1 / p0) - 1


def _accuracy(signal: Decision, fwd: float) -> bool:
    if fwd > 0.02:
        ideal: Decision = "BUY"
    elif fwd < -0.02:
        ideal = "SELL"
    else:
        ideal = "HOLD"
    return signal == ideal


def run_backtest(tickers: list[str], weeks: int = 26, fwd_days: int = 20) -> dict[str, Any]:
    """Deterministic scorecard for bonus: mirrors News vs Volatility philosophies on history."""
    rows: list[dict] = []
    agg_news_hits = agg_news_n = 0
    agg_vol_hits = agg_vol_n = 0
    per_ticker: list[dict] = []

    for t in tickers:
        hist = yf.Ticker(t).history(period="730d", auto_adjust=True).rename(columns=str.strip)
        if hist.empty:
            continue
        idx = hist.index.sort_values()
        samples = [idx[-1 - 7 * w] for w in range(weeks) if -1 - 7 * w >= -len(idx)]
        hits_news = hits_vol = 0
        total_news = total_vol = 0
        for ts in samples:
            pay = market_payload_asof(t, ts, hist)
            if not pay:
                continue
            sig_n = _signal_news_proxy(pay)
            sig_v = _signal_vol_averse(pay)
            fr = _forward_return(hist, ts, fwd_days)
            if fr is None:
                continue
            if _accuracy(sig_n, fr):
                hits_news += 1
            if _accuracy(sig_v, fr):
                hits_vol += 1
            total_news += 1
            total_vol += 1
            rows.append(
                {
                    "ticker": t,
                    "asof": str(ts.date()),
                    "signal_news_follower": sig_n,
                    "signal_volatility_averse": sig_v,
                    f"forward_return_{fwd_days}d": round(fr, 6),
                }
            )

        r_news = hits_news / total_news if total_news else None
        r_vol = hits_vol / total_vol if total_vol else None
        win = "insufficient_samples"
        if r_news is not None and r_vol is not None:
            win = "tie"
            if r_news > r_vol + 0.05:
                win = "news_sentiment_heuristic"
            elif r_vol > r_news + 0.05:
                win = "volatility_averse_heuristic"
        agg_news_hits += hits_news
        agg_news_n += total_news
        agg_vol_hits += hits_vol
        agg_vol_n += total_vol
        per_ticker.append(
            {
                "ticker": t,
                "hit_rate_news": round(r_news, 4) if r_news is not None else None,
                "hit_rate_volatility": round(r_vol, 4) if r_vol is not None else None,
                "winner_heuristic": win,
            }
        )

    overall = "tie"
    if agg_news_n and agg_vol_n:
        gn = agg_news_hits / agg_news_n
        gv = agg_vol_hits / agg_vol_n
        if gn > gv + 0.02:
            overall = "news_sentiment_heuristic"
        elif gv > gn + 0.02:
            overall = "volatility_averse_heuristic"

    return {
        "method": "deterministic_heuristic_vs_forward_return",
        "disclaimer": "Not identical to live LLM agents; transparent proxy signals for grading artifact.",
        "weeks": weeks,
        "forward_days": fwd_days,
        "overall_winner": overall,
        "per_ticker": per_ticker,
        "rows": rows,
    }
