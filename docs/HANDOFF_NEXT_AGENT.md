# Handoff — AGAI HW2 StockTrader (for the next agent / new machine)

**Purpose:** Continuity between machines. The student worked on a **laptop**; work may continue on a **new desktop** where **Ollama is not installed yet**. This file tells you exactly where the project stands and what you should walk the user through.

**Repo (pull from here):** [https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding](https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding)

---

## 1. Situation (read first)

| Item | Status |
|------|--------|
| **Machine context** | Prior development on **laptop**; **new desktop** may have a clean OS — assume **no Ollama**, possibly fresh Python/venv. |
| **Git** | Latest work should be on `master`; student pulls before continuing. |
| **Local LLM** | App expects **Ollama** at `http://localhost:11434` by default (`OLLAMA_HOST`). Model env: `OLLAMA_MODEL` (e.g. `llama3.2`). |
| **News API (assignment requirement)** | **Alpha Vantage** key obtained (student account). Set **`ALPHAVANTAGE_API_KEY` only in repo-root `.env`** (gitignored — **never commit** the key or paste it into tracked docs). Copy `.env` to each machine (laptop/desktop) that runs the pipeline. Without a key in `.env`, code still runs with empty news (implemented). |
| **Your role as the next agent** | **Guide the user** through: (1) clone/pull, (2) venv + `pip install -r requirements.txt`, (3) **install Ollama + pull a model**, (4) create `.env` from `.env.example` and add **Alpha Vantage key**, (5) run the pipeline without `STOCKTRADER_SKIP_LLM`, (6) finish report PDFs in `report/`. |

---

## 2. What this project is (one paragraph)

**CO2 StockTrader:** Two graded strategies (**News Sentiment Follower**, **Volatility Averse**) + extension **Moral Trader**, same market JSON per ticker, **AutoGen** `AssistantAgent` with structured outputs, **evaluator**, JSON under `outputs/`. **Bonus:** `outputs/backtest.json` (heuristic scorecard). Not a production trading system — focus is agent behavior and comparison.

---

## 3. Repository layout (clone root = project root)

```
README.md
requirements.txt
src/           # main.py, market_data.py, orchestration.py, evaluator.py, backtest.py, llm_factory.py, schemas.py, strategies.py
prompts/       # strategy_a.txt, strategy_b.txt, evaluator.txt, + named strategy files
outputs/       # per-ticker JSON, summary.json, backtest.json (regenerate for submission)
report/        # report.pdf, ai appendix, DEFENSE_GEOPOLITICS_UNIVERSE.md — student deliverables
docs/          # this handoff, ALPHA_VANTAGE.md, assets/ (optional local screenshots; key image gitignored)
```

**Instructions folder:** If present locally, it may be gitignored; assignment text lives in course materials, not required in repo for code to run.

---

## 4. What was already implemented (don’t redo unless broken)

- **Market data:** `src/market_data.py` — yfinance + volatility features; Alpha Vantage **NEWS_SENTIMENT** with empty/rate-limit/`Error Message` handling; optional sort/limit/throttle via env (see [`ALPHA_VANTAGE.md`](ALPHA_VANTAGE.md)).
- **Orchestration:** `src/orchestration.py` — three parallel strategy agents per ticker + evaluator.
- **LLM:** `src/llm_factory.py` — Ollama default; optional LiteLLM OpenAI-compatible proxy via env.
- **Speed:** `OLLAMA_NUM_PREDICT`, `OLLAMA_NUM_CTX`, `OLLAMA_TEMPERATURE`; `src/main.py` has `--ticker-workers` (default 2).
- **Evaluator guard:** `src/evaluator.py` normalizes contradictory “disagree” text when decisions are actually unanimous.
- **README:** Setup, env table, Alpha Vantage no-news note, HW1-style quantitative + AI appendix guidance.
- **Report helper:** `report/report_checklist.md`.

---

## 5. Due outs for the user (prioritize in this order)

1. **On the new desktop — install Ollama**
   - Download from [ollama.com](https://ollama.com), install, confirm `ollama --version` (or use full path: `%LocalAppData%\Programs\Ollama\ollama.exe` if PATH not updated yet).
   - Pull a model: e.g. `ollama pull llama3.2`
   - Ensure the Ollama app/service is running before Python runs.

2. **Alpha Vantage API key (News Sentiment fidelity)**
   - Key is issued; **store the value only in local `.env`** at repo root (`ALPHAVANTAGE_API_KEY=...`). Do not commit `.env` or embed the key in README/handoff/issues.
   - On a **new clone or machine:** copy `.env.example` → `.env` and paste the key again (or copy your private `.env` over securely).
   - API reference: [alphavantage.co/documentation](https://www.alphavantage.co/documentation/) (NEWS_SENTIMENT). Key signup: [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key). Build notes for *this* repo: [`ALPHA_VANTAGE.md`](ALPHA_VANTAGE.md). Optional citations for reports: [Trading Agents](https://trading-agents.ai/), [Alpha Vantage MCP](https://mcp.alphavantage.co/).
   - Optional welcome/key screenshot: save locally as `docs/assets/alphavantage-welcome.png` (**gitignored**, not in remote — hygiene).
   - Free tier has **request limits**; empty/no news handling is already in code. Use `ALPHAVANTAGE_MIN_INTERVAL_SEC` if you burst too many tickers.

3. **Re-run full pipeline for submission-quality JSON**
   - Do **not** set `STOCKTRADER_SKIP_LLM=1` for final outputs.
   - From repo root:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     $env:PYTHONPATH = (Get-Location).Path
     Remove-Item Env:STOCKTRADER_SKIP_LLM -ErrorAction SilentlyContinue
     python -m src.main --backtest --ticker-workers 2
     ```

4. **Report**
   - `report/report.pdf` + AI use appendix per course rubric.
   - Use quantitative bits from `outputs/summary.json` and `outputs/backtest.json`.
   - Document one failure/surprise; granular AI attribution (see root `README.md`).

5. **Git**
   - Commit refreshed `outputs/*.json` after real runs; push `master`.

---

## 6. Assignment constraints to remember

- **News Sentiment Follower:** Must handle **no news** / API limits — see `market_data.py` + prompts.
- **Parallelism:** Strategies must not see each other’s outputs before evaluation (current design: parallel per ticker, then evaluator).
- **Bonus third agent:** Moral Trader is custom extension; official “third from menu” wording may differ — student can note in report if needed.

---

## 7. If something fails on the new machine

| Symptom | Likely fix |
|---------|------------|
| `ollama` not recognized | Use full path to `ollama.exe` or restart shell after install; add to PATH. |
| Connection errors to localhost:11434 | Start Ollama application / service. |
| All HOLD / no disagreement | Common without news + similar regimes; consider different tickers or add Alpha Vantage key for news signal. |
| Slow runs | Lower `--ticker-workers 1`; reduce `OLLAMA_NUM_PREDICT` slightly in `.env`. |

---

## 8. First files to open after pull

1. [`README.md`](../README.md) — full setup
2. [`ALPHA_VANTAGE.md`](ALPHA_VANTAGE.md) — AV endpoint, limits, related links
3. [`src/main.py`](../src/main.py) — CLI entry
4. [`src/orchestration.py`](../src/orchestration.py) — agent wiring
5. [`report/report_checklist.md`](../report/report_checklist.md) — report structure

---

**End handoff.** On a **new desktop**, prioritize **Ollama install** and a **local `.env`** with `ALPHAVANTAGE_API_KEY` (same key as the student’s Alpha Vantage account — never put secrets in git).
