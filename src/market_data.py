"""Market data: yfinance OHLC + derived metrics + optional Alpha Vantage news."""

from __future__ import annotations

import os
import re
import threading
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import numpy as np
import pandas as pd
import yfinance as yf

# Alpha Vantage NEWS_SENTIMENT: https://www.alphavantage.co/documentation/
# Free tier: respect per-minute / daily limits (see docs/ALPHA_VANTAGE.md).
_AV_THROTTLE_LOCK = threading.Lock()
_AV_LAST_CALL_MONO = 0.0
# Alpha Vantage sometimes echoes the API key inside Note/Information text; never persist that.
_AV_KEY_ECHO = re.compile(r"(?i)\bAPI key as\s+[A-Za-z0-9]{8,48}\b")


def _scrub_alpha_vantage_public_text(msg: str) -> str:
    if not msg:
        return msg
    return _AV_KEY_ECHO.sub("API key as [REDACTED]", msg)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _alpha_vantage_api_key() -> str:
    """Resolve API key: env ALPHAVANTAGE_API_KEY, then ALPHAVANTAGE_KEY_FILE, then secrets/alphavantage_api_key.txt."""
    k = os.environ.get("ALPHAVANTAGE_API_KEY", "").strip()
    if k:
        return k
    path_raw = (os.environ.get("ALPHAVANTAGE_KEY_FILE") or "").strip()
    candidates: list[Path] = []
    if path_raw:
        p = Path(path_raw)
        if not p.is_absolute():
            p = _repo_root() / p
        candidates.append(p)
    candidates.append(_repo_root() / "secrets" / "alphavantage_api_key.txt")
    for path in candidates:
        try:
            if path.is_file():
                line = path.read_text(encoding="utf-8").strip().splitlines()
                if line:
                    return line[0].strip()
        except OSError:
            continue
    return ""


def _throttle_alpha_vantage() -> None:
    """Optional spacing between AV calls to reduce rate-limit errors (set ALPHAVANTAGE_MIN_INTERVAL_SEC)."""
    try:
        sec = float(os.environ.get("ALPHAVANTAGE_MIN_INTERVAL_SEC") or "0")
    except ValueError:
        sec = 0.0
    if sec <= 0:
        return
    global _AV_LAST_CALL_MONO
    with _AV_THROTTLE_LOCK:
        now = time.monotonic()
        wait = _AV_LAST_CALL_MONO + sec - now
        if wait > 0:
            time.sleep(wait)
        _AV_LAST_CALL_MONO = time.monotonic()


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
    """NEWS_SENTIMENT endpoint; see https://www.alphavantage.co/documentation/ (Alpha Intelligence)."""
    key = _alpha_vantage_api_key()
    if not key:
        return {"articles_count": 0, "avg_sentiment_score": None, "articles": [], "note": "no API key"}
    try:
        lim_env = int(os.environ.get("ALPHAVANTAGE_NEWS_LIMIT") or str(limit))
    except ValueError:
        lim_env = limit
    # Docs: limit is optional; use a bounded value (typical max 1000 for feed size).
    limit_use = min(max(1, lim_env), 1000)
    sort_raw = (os.environ.get("ALPHAVANTAGE_NEWS_SORT") or "").strip().upper()
    allowed_sort = {"LATEST", "EARLIEST", "RELEVANCE"}
    url = "https://www.alphavantage.co/query"
    params: dict[str, str] = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "limit": str(limit_use),
        "apikey": key,
    }
    if sort_raw in allowed_sort:
        params["sort"] = sort_raw
    _throttle_alpha_vantage()
    try:
        r = httpx.get(url, params=params, timeout=30.0)
        r.raise_for_status()
        data = r.json()
    except Exception as e:  # noqa: BLE001
        return {"articles_count": 0, "avg_sentiment_score": None, "articles": [], "error": _scrub_alpha_vantage_public_text(str(e))}
    err = data.get("Error Message")
    if err:
        return {
            "articles_count": 0,
            "avg_sentiment_score": None,
            "articles": [],
            "note": _scrub_alpha_vantage_public_text(str(err)[:500]),
        }
    if "feed" not in data:
        raw_note = str(data.get("Note") or data.get("Information") or "empty_or_rate_limit")
        return {
            "articles_count": 0,
            "avg_sentiment_score": None,
            "articles": [],
            "note": _scrub_alpha_vantage_public_text(raw_note),
        }
    feed = data["feed"][:limit_use]
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
    vol_30 = float(daily_ret.tail(30).std()) if len(daily_ret) >= 10 else None
    atr_14 = _atr(tail_90, 14)
    last_px = float(close.iloc[-1])
    ma20 = float(close.tail(20).mean()) if len(close) >= 20 else None
    ma50 = float(close.tail(50).mean()) if len(close) >= 50 else None
    ret_5d = float(close.iloc[-1] / close.iloc[-6] - 1) if len(close) >= 6 else 0.0
    px_30_ago = float(close.iloc[-22]) if len(close) >= 22 else float("nan")
    pct_30 = float((last_px / px_30_ago - 1) * 100) if px_30_ago == px_30_ago and px_30_ago else None

    summary = {
        "ticker": ticker,
        "asof": str(asof.date()),
        "current_price": round(last_px, 4),
        "moving_avg_20d": round(ma20, 4) if ma20 else None,
        "moving_avg_50d": round(ma50, 4) if ma50 else None,
        "std_daily_return_90d": round(std_90, 6),
        "volatility_30d": round(vol_30, 6) if vol_30 is not None and vol_30 == vol_30 else None,
        "atr_14": round(atr_14, 4) if atr_14 == atr_14 else None,
        "max_single_day_drop_90d": round(max_drop_90, 6),
        "return_5d": round(ret_5d, 6),
        "pct_change_30d": round(pct_30, 2) if pct_30 is not None and pct_30 == pct_30 else None,
    }
    return {
        "ticker": ticker,
        "as_of_utc": asof.isoformat(),
        "market_data_summary": summary,
        "news_features": {"articles_count": 0, "avg_sentiment_score": None, "note": "historical_backtest_proxy"},
    }
