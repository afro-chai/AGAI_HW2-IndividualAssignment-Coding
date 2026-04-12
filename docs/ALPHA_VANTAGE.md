# Alpha Vantage (minimal reference)

## API budget (this repo)

- **One** `NEWS_SENTIMENT` HTTP request **per ticker** in `build_market_payload()` → default run = **5 calls** (five tickers). Historical `backtest.json` uses **0** AV calls.
- Free tier is often **~25 requests/day**; five-ticker runs leave headroom for retries. Optional `ALPHAVANTAGE_MIN_INTERVAL_SEC` spaces bursts.

## Endpoint

`NEWS_SENTIMENT` — parameters in code: `tickers`, `limit`, optional `sort`, `apikey`. Details: [Alpha Vantage documentation](https://www.alphavantage.co/documentation/).

## Key

Resolved in `src/market_data.py`: `ALPHAVANTAGE_API_KEY` → `ALPHAVANTAGE_KEY_FILE` → `secrets/alphavantage_api_key.txt` (see [`secrets/README.md`](../secrets/README.md)). Never commit keys.

## Errors

`Note`, `Information`, `Error Message` → surfaced in `news_features` without crashing.

Optional links for reports: [Trading Agents](https://trading-agents.ai/), [Alpha Vantage MCP](https://mcp.alphavantage.co/).
