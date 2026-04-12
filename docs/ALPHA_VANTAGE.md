# Alpha Vantage integration (build and operations)

Official reference: **[Alpha Vantage API documentation](https://www.alphavantage.co/documentation/)** — use this for current parameters, limits, and premium vs free behavior.

## What this project calls

We use the **NEWS_SENTIMENT** function (Alpha Intelligence™ → News & Sentiment) with:

| Parameter | In code | Notes |
|-----------|---------|--------|
| `function` | `NEWS_SENTIMENT` | Required |
| `tickers` | Single ticker per request | Comma-separated list supported upstream; we pass one symbol per run |
| `limit` | `ALPHAVANTAGE_NEWS_LIMIT` or default `20` | Bounded 1–1000 |
| `sort` | Optional `ALPHAVANTAGE_NEWS_SORT` | When set, one of `LATEST`, `EARLIEST`, `RELEVANCE` (see AV docs for semantics) |
| `apikey` | Resolved by `_alpha_vantage_api_key()` | Never commit real keys |

**Where the key is read (in order):** (1) environment variable `ALPHAVANTAGE_API_KEY` (e.g. from repo-root `.env` via `load_dotenv` in `main.py`); (2) first line of the file pointed to by `ALPHAVANTAGE_KEY_FILE` (repo-relative or absolute); (3) default gitignored file **`secrets/alphavantage_api_key.txt`** (first line only). See [`secrets/README.md`](../secrets/README.md).

Implementation: [`src/market_data.py`](../src/market_data.py) (`fetch_alpha_vantage_news`, `_alpha_vantage_api_key`).

### Rate limits and errors

Free and paid tiers publish limits in the [documentation](https://www.alphavantage.co/documentation/) and on [premium](https://www.alphavantage.co/premium/) pages. Typical patterns:

- Responses may include **`Note`** or **`Information`** when throttled or when no data is returned.
- **`Error Message`** is handled explicitly and surfaced in `news_features.note` without crashing the pipeline.

Optional env **`ALPHAVANTAGE_MIN_INTERVAL_SEC`**: minimum seconds between Alpha Vantage HTTP calls from this process (helps avoid burst traffic when analyzing many tickers).

## Related tools (citing / inspiration)

- **[Trading Agents](https://trading-agents.ai/)** — institutional-style equity research tooling; cited by Alpha Vantage as an example direction (not a dependency of this repo).
- **[Alpha Vantage MCP](https://mcp.alphavantage.co/)** — Model Context Protocol server so assistants can query Alpha Vantage through a standard MCP interface; this homework uses direct `httpx` calls instead, but MCP is a reasonable capstone or report citation for “how else to integrate market data with agents.”

## Key confirmation screenshot (local only)

If you keep a welcome / key-issued screen capture for your report, save it as **`docs/assets/alphavantage-welcome.png`** on your machine. That filename is **gitignored** so a screenshot that might expose your API key is never pushed. Do not commit key images; rotate the key at [Alpha Vantage support](https://www.alphavantage.co/support/#api-key) if it was ever exposed in a public repo.
