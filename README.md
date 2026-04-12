# AGAI_HW2 — StockTrader (Individual Assignment 2 + bonus + capstone runway)

Multi-agent stock signal system: **News Sentiment Follower**, **Volatility Averse**, and extension **Moral Trader**. Uses **[Microsoft AutoGen](https://microsoft.github.io/autogen/)** (`AssistantAgent` + structured outputs), **Ollama** locally, and an optional **LiteLLM** OpenAI-compatible endpoint for future multi-provider capstone work.

**Why AutoGen here:** strong multi-agent orchestration, clear roles, and message-based patterns that scale to manager–worker flows, tool loops, and reflection—useful for a larger FININT/OSINT capstone. This homework keeps strategies **strictly parallel** (no debate round) to match the rubric. You can still layer **LangChain** or **LangGraph** later for retrieval subgraphs without replacing AutoGen agents. See also the AutoGen cookbook for [local LLMs with Ollama and LiteLLM](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/cookbook/local-llms-ollama-litellm.html).

**Target remote:** [https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git](https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git)

**Continuing on another machine?** See [`docs/HANDOFF_NEXT_AGENT.md`](docs/HANDOFF_NEXT_AGENT.md) (Ollama setup on a new PC, Alpha Vantage `.env`, and what the next agent should do).

**Alpha Vantage (news API):** Implementation notes, rate-limit tips, and citations — [`docs/ALPHA_VANTAGE.md`](docs/ALPHA_VANTAGE.md). Official docs: [alphavantage.co/documentation](https://www.alphavantage.co/documentation/). Related: [Trading Agents](https://trading-agents.ai/) (example ecosystem), [Alpha Vantage MCP](https://mcp.alphavantage.co/) (MCP server for assistants).

## Repository layout (course spec)

This repo matches the assignment tree: `README.md`, `requirements.txt`, `src/`, `prompts/`, `outputs/`, `report/`. (The brief used a `stocktrader/` wrapper; here the **clone root is the project root**.)

---

## Before you begin (requirements)

Complete these **before** cloning or running the analysis loop:

1. **Python** — 3.10+ (3.12 recommended). Install from [python.org](https://www.python.org/downloads/).
2. **Virtual environment** — Create and activate a venv in the repo root:
   - Windows (PowerShell): `python -m venv .venv` then `.\.venv\Scripts\Activate.ps1`
3. **Install dependencies** — From the repo root: `pip install -r requirements.txt`
4. **Ollama** — Install from [ollama.com](https://ollama.com), then pull a JSON-capable model, e.g. `ollama pull llama3.2` (or `mistral`, `qwen2.5`, etc.).
5. **Run Ollama** — Ensure the daemon is up (default `http://localhost:11434`). Override with env `OLLAMA_HOST` if needed.
6. **Alpha Vantage (recommended for News Sentiment)** — Free key at [alphavantage.co](https://www.alphavantage.co/support/#api-key). Set `ALPHAVANTAGE_API_KEY` in `.env`. Without it, news blocks are empty and the News agent must still behave (per assignment).
7. **LiteLLM (optional capstone layer)** — To route all traffic through LiteLLM’s OpenAI-compatible proxy, set `LITELLM_BASE_URL` (e.g. `http://localhost:4000/v1`) and `LITELLM_API_KEY` if your proxy requires it, plus `LITELLM_MODEL` (e.g. `ollama/llama3.2`). When unset, the app uses `OllamaChatCompletionClient` directly.
8. **Smoke tests** — Confirm `python -c "import yfinance as yf; print(yf.Ticker('AAPL').info.get('symbol'))"` and that Ollama answers: `ollama run llama3.2 "ping"`.

Copy `.env.example` to `.env` in the repo root and fill keys.

News Sentiment warning handling (required): if Alpha Vantage returns no feed data (missing key, rate limit, or no ticker news), the app records zero-news metadata and the strategy falls back to conservative reasoning instead of failing.

---

## Project productivity checkpoints

Check off as you go (update dates in your fork):

- [ ] **C0 — Environment** — Python venv, `pip install -r requirements.txt`, Ollama model pulled.
- [ ] **C1 — Market data** — `market_data.py` returns 90d+ history + volatility + optional AV news; handles empty news.
- [ ] **C2 — AutoGen strategies** — Three `AssistantAgent` instances, parallel `asyncio.gather`, structured JSON output; no cross-talk between strategies.
- [ ] **C3 — Evaluator** — Consensus vs split narrative for three decisions; saved in JSON.
- [ ] **C4 — Four tickers + JSON** — `outputs/*.json` + `summary.json`; diverse stock rationale for report.
- [ ] **C5 — Backtest bonus** — `outputs/backtest.json` generated; limitations noted in report.
- [ ] **C6 — Report + AI appendix** — PDF sections per rubric; honesty on failures.
- [ ] **C7 — GitHub** — Push to `AGAI_HW2-IndividualAssignment-Coding`; README + pinned `requirements.txt`.

---

## Quality upgrades from HW1 feedback

To directly address prior feedback, this project should emphasize:

- **Specific quantitative comparison** (not just narrative): report agreement/disagreement counts, confidence deltas, and a small per-stock comparison table.
- **Low-noise metrics**: avoid arbitrary random noise in scoring; keep formulas deterministic and explain thresholds.
- **Granular AI attribution**: log exactly which files/sections used AI assistance, plus what you accepted vs revised vs rejected.

Recommended minimum quantitative section in the report:

- `total_agreements`, `total_disagreements` from `outputs/summary.json`
- Per-stock: `a_decision`, `b_decision`, `c_decision`, and confidence spread
- Backtest: per-ticker hit-rate comparison and overall winner from `outputs/backtest.json`

---

## Environment variables

| Variable | Purpose |
|----------|---------|
| `OLLAMA_HOST` | Default `http://localhost:11434` |
| `OLLAMA_MODEL` | e.g. `llama3.2` |
| `OLLAMA_NUM_PREDICT` | Max generated tokens per call (default `220`, faster) |
| `OLLAMA_NUM_CTX` | Context window size (default `4096`) |
| `OLLAMA_TEMPERATURE` | Sampling temperature (default `0.2`) |
| `ALPHAVANTAGE_API_KEY` | News sentiment ([NEWS_SENTIMENT](https://www.alphavantage.co/documentation/)) |
| `ALPHAVANTAGE_NEWS_LIMIT` | Optional; max articles (1–1000), default 20 |
| `ALPHAVANTAGE_NEWS_SORT` | Optional; `LATEST`, `EARLIEST`, or `RELEVANCE` |
| `ALPHAVANTAGE_MIN_INTERVAL_SEC` | Optional; minimum seconds between AV HTTP calls (rate-limit hygiene) |
| `LITELLM_BASE_URL` | If set, use OpenAI-compatible client (LiteLLM proxy) |
| `LITELLM_MODEL` | Model id for proxy |
| `LITELLM_API_KEY` | Proxy API key if required |
| `STOCKTRADER_SKIP_LLM` | `1` to stub LLM outputs (CI / no GPU) |

---

## Run

From the repository root (this folder):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:PYTHONPATH = (Get-Location).Path
python -m src.main --tickers NVDA,TSLA,JNJ,KO --backtest
```

Artifacts: `outputs/<TICKER>.json`, `summary.json`, optional `backtest.json`.

Performance tip: increase throughput with `--ticker-workers 2` (default). For lower-memory systems, set `--ticker-workers 1`.

Run with stubs disabled (required for final submission-quality outputs):

```powershell
Remove-Item Env:STOCKTRADER_SKIP_LLM -ErrorAction SilentlyContinue
$env:PYTHONPATH = (Get-Location).Path
python -m src.main --tickers NVDA,TSLA,JNJ,KO --backtest
```

### Full run with transcript log

From repo root (writes `logs/full_run_<timestamp>.txt` and `logs/full_run_latest.txt`). **Commit** transcripts only if they contain **no secrets** — see [`logs/README.md`](logs/README.md).

```powershell
.\scripts\run_full_with_log.ps1
```

---

## Architecture (brief)

- `src/market_data.py` — yfinance + derived features + Alpha Vantage news.
- `src/llm_factory.py` — Ollama vs LiteLLM-backed `ChatCompletionClient`.
- `src/orchestration.py` — Builds three fresh `AssistantAgent`s per ticker; `asyncio.gather` for parallel strategies; evaluator pass.
- `src/evaluator.py`, `src/strategies.py` — Prompts + parsing helpers.
- `src/backtest.py` — Point-in-time heuristic scorecard for bonus (deterministic, documented).
- `prompts/*.txt` — Saved prompts for grading.

LangGraph / LangChain can be added later as subgraphs or RAG without replacing AutoGen agents.

---

## Honest scope notes

- **Graded “two strategies”** are News Sentiment Follower (`strategy_a`) and Volatility Averse (`strategy_b`). **Moral Trader** is `strategy_c` (third-agent bonus + capstone hook).
- **Backtest** uses transparent **heuristic** signals aligned with each philosophy so graders get `backtest.json` without hundreds of local LLM calls. Compare to live LLM behavior in the report.

---

## AI appendix template (granular attribution)

Use this structure in `report/ai_use_appendix.pdf`:

1. **Prompt / interaction log excerpt**
   - Task goal
   - Prompt used
   - Output excerpt
2. **File-level attribution**
   - File path
   - AI-assisted change summary
   - Status: accepted / revised / rejected
3. **Verification steps**
   - What you checked manually (logic, numbers, API behavior)
   - Any mismatch found and fix applied
4. **Failure case**
   - One weak/incorrect AI output
   - Why it failed
   - How you corrected or constrained it
