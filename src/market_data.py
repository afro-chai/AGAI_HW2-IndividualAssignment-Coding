"""Market data: yfinance OHLC + derived metrics + optional Alpha Vantage news."""

from __future__ import annotations

import os
from datetime import date, datetime, timezone
from typing import Any

import httpx
import numpy as np
import pandas as pd
import yfinance as yf


def _true_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    prev_close = close.shift(1)
    tr = pd.concat(
        [
            high - low,
            (high - prev_close).abs(),
            (low - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return tr


def _atr(df: pd.DataFrame, period: int = 14) -> float:
    if len(df) < period + 1:
        return float("nan")
    tr = _true_range(df["High"], df["Low"], df["Close"])
    return float(tr.tail(period).mean())


def fetch_alpha_vantage_news(ticker: str, limit: int = 20) -> dict[str, Any]:
    key = os.environ.get("ALPHAVANTAGE_API_KEY", "").strip()
    if not key:
        return {"articles_count": 0, "avg_sentiment_score": None, "articles": [], "note": "no API key"}
    url = "https://www.alphavantage.co/query"
    params = {"function": "NEWS_SENTIMENT", "tickers": ticker, "limit": limit, "apikey": key}
    try:
        r = httpx.get(url, params=params, timeout=30.0)
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        return {"articles_count": 0, "avg_sentiment_score": None, "articles": [], "error": str(e)}
    if "feed" not in data:
        return {
            "articles_count": 0,
            "avg_sentiment_score": None,
            "articles": [],
            "note": str(data.get("Note") or data.get("Information") or "empty_or_rate_limit"),
        }
    feed = data["feed"][:limit]
    scores: list[float] = []
    articles: list[dict[str, Any]] = []
    for item in feed:
        ticker_sent = item.get("ticker_sentiment") or []
        sc = None
        for ts in ticker_sent:
            if ts.get("ticker") == ticker:
                sc = ts.get("ticker_sentiment_score")
                break
        if sc is not None:
            try:
                scores.append(float(sc))
            except (TypeError, ValueError):
                pass
        articles.append(
            {
                "title": (item.get("title") or "")[:200],
                "summary": (item.get("summary") or "")[:400],
                "source": item.get("source"),
                "overall_sentiment_score": item.get("overall_sentiment_score"),
            }
        )
    avg = float(np.mean(scores)) if scores else None
    return {"articles_count": len(feed), "avg_sentiment_score": avg, "articles": articles}


def build_market_payload(ticker: str, lookback_days: int = 120) -> dict[str, Any]:
    """Fetch live market data as of today. No LLM calls."""
    t = yf.Ticker(ticker)
    hist = t.history(period=f"{lookback_days}d", auto_adjust=True)
    if hist.empty or len(hist) < 30:
        raise ValueError(f"Insufficient history for {ticker}")

    hist = hist.rename(columns=str.strip)
    tail_90 = hist.tail(90)
    close = tail_90["Close"]
    daily_ret = close.pct_change().dropna()
    std_90 = float(daily_ret.std()) if len(daily_ret) else float("nan")
    max_drop_90 = float(daily_ret.min()) if len(daily_ret) else float("nan")
    atr_14 = _atr(tail_90, 14)

    bench = yf.Ticker("SPY").history(period=f"{lookback_days}d", auto_adjust=True)
    common = tail_90.index.intersection(bench.index)
    beta_proxy = None
    if len(common) >= 60:
        a = tail_90.loc[common, "Close"].pct_change().dropna()
        b = bench.loc[common, "Close"].pct_change().dropna()
        joined = pd.concat([a, b], axis=1, join="inner").dropna()
        if len(joined) >= 40:
            cov = np.cov(joined.iloc[:, 0], joined.iloc[:, 1])[0, 1]
            var_b = np.var(joined.iloc[:, 1])
            beta_proxy = float(cov / var_b) if var_b else None

    last_px = float(close.iloc[-1])
    px_30_ago = float(close.iloc[-22]) if len(close) >= 22 else float("nan")
    pct_30 = float((last_px / px_30_ago - 1) * 100) if px_30_ago and not np.isnan(px_30_ago) else None

    ma20 = float(close.tail(20).mean()) if len(close) >= 20 else None
    ma50 = float(close.tail(50).mean()) if len(close) >= 50 else None

    news = fetch_alpha_vantage_news(ticker)

    run_date = date.today().isoformat()
    summary = {
        "ticker": ticker,
        "run_date": run_date,
        "current_price": round(last_px, 4),
        "price_30d_ago": round(px_30_ago, 4) if px_30_ago and not np.isnan(px_30_ago) else None,
        "pct_change_30d": round(pct_30, 2) if pct_30 is not None else None,
        "avg_daily_volume": int(tail_90["Volume"].tail(30).mean()) if "Volume" in tail_90 else None,
        "volatility_30d": round(float(daily_ret.tail(30).std()), 6) if len(daily_ret) >= 10 else None,
        "moving_avg_20d": round(ma20, 4) if ma20 else None,
        "moving_avg_50d": round(ma50, 4) if ma50 else None,
        "std_daily_return_90d": round(std_90, 6),
        "atr_14": round(atr_14, 4) if atr_14 == atr_14 else None,
        "max_single_day_drop_90d": round(max_drop_90, 6),
        "beta_proxy_spy": round(beta_proxy, 3) if beta_proxy is not None else None,
    }

    payload = {
        "ticker": ticker,
        "as_of_utc": datetime.now(timezone.utc).isoformat(),
        "market_data_summary": summary,
        "news_features": news,
        "ohlc_note": "Agents receive summarized fields only; no future data leaks.",
    }
    return payload


def market_payload_asof(ticker: str, asof: pd.Timestamp, hist_window: pd.DataFrame) -> dict[str, Any]:
    """Point-in-time slice for backtest: hist_window ends on asof (inclusive)."""
    sub = hist_window.loc[:asof]
    if len(sub) < 60:
        return {}
    tail_90 = sub.tail(90)
    close = tail_90["Close"]
    daily_ret = close.pct_change().dropna()
    std_90 = float(daily_ret.std()) if len(daily_ret) else float("nan")
    max_drop_90 = float(daily_ret.min()) if len(daily_ret) else float("nan")
    atr_14 = _atr(tail_90, 14)
    last_px = float(close.iloc[-1])
    ma20 = float(close.tail(20).mean()) if len(close) >= 20 else None
    ma50 = float(close.tail(50).mean()) if len(close) >= 50 else None
    ret_5d = float(close.iloc[-1] / close.iloc[-6] - 1) if len(close) >= 6 else 0.0

    summary = {
        "ticker": ticker,
        "asof": str(asof.date()),
        "current_price": round(last_px, 4),
        "moving_avg_20d": round(ma20, 4) if ma20 else None,
        "moving_avg_50d": round(ma50, 4) if ma50 else None,
        "std_daily_return_90d": round(std_90, 6),
        "atr_14": round(atr_14, 4) if atr_14 == atr_14 else None,
        "max_single_day_drop_90d": round(max_drop_90, 6),
        "return_5d": round(ret_5d, 6),
    }
    return {
        "ticker": ticker,
        "as_of_utc": asof.isoformat(),
        "market_data_summary": summary,
        "news_features": {"articles_count": 0, "avg_sentiment_score": None, "note": "historical_backtest_proxy"},
    }
