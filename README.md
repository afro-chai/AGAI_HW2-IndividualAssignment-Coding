# AGAI_HW2 — StockTrader (Individual Assignment 2 + bonus + capstone runway)

Multi-agent stock signal system: **News Sentiment Follower**, **Volatility Averse**, and extension **Moral Trader**. Uses **[Microsoft AutoGen](https://microsoft.github.io/autogen/)** (`AssistantAgent` + structured outputs), **Ollama** locally, and an optional **LiteLLM** OpenAI-compatible endpoint for future multi-provider capstone work.

**Why AutoGen here:** strong multi-agent orchestration, clear roles, and message-based patterns that scale to manager–worker flows, tool loops, and reflection—useful for a larger FININT/OSINT capstone. This homework keeps strategies **strictly parallel** (no debate round) to match the rubric. You can still layer **LangChain** or **LangGraph** later for retrieval subgraphs without replacing AutoGen agents. See also the AutoGen cookbook for [local LLMs with Ollama and LiteLLM](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/cookbook/local-llms-ollama-litellm.html).

**Target remote:** [https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git](https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git)

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

## Environment variables

| Variable | Purpose |
|----------|---------|
| `OLLAMA_HOST` | Default `http://localhost:11434` |
| `OLLAMA_MODEL` | e.g. `llama3.2` |
| `ALPHAVANTAGE_API_KEY` | News sentiment |
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

