# StockTrader — project plan and status

**Where you are now:** working on the **laptop** after pulling the latest from `origin/master`. Use this file as the single checklist for what to do **on this machine** next.

---

## On this laptop — do these next (in order)

1. **Pull** (already done when you asked; run again before long sessions):  
   `git pull origin master`

2. **Secrets file** — Ensure **repo-root `.env`** exists on the laptop (gitignored, never committed):
   - Copy from `.env.example` if needed, or securely copy your **private** `.env` from the desktop.
   - Must include at least: `ALPHAVANTAGE_API_KEY=...` (same key as desktop is fine) and Ollama-related vars if you override defaults.
   - See [`docs/ALPHA_VANTAGE.md`](docs/ALPHA_VANTAGE.md) for behavior and optional throttles.

3. **Ollama** — Confirm the laptop has Ollama running and a model pulled (e.g. `llama3.2`):  
   `ollama list` / `ollama run llama3.2 "ping"`

4. **Python env** — From repo root:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

5. **Full live run** (real LLM outputs — not stubs). Prefer the logging wrapper (same command, plus `logs/full_run_latest.txt`):
   ```powershell
   .\scripts\run_full_with_log.ps1
   ```
   Or manually:
   ```powershell
   $env:PYTHONPATH = (Get-Location).Path
   Remove-Item Env:STOCKTRADER_SKIP_LLM -ErrorAction SilentlyContinue
   python -m src.main --tickers NVDA,TSLA,JNJ,KO --backtest --ticker-workers 2
   ```
   - Expect `outputs/<TICKER>.json`, `outputs/summary.json`, `outputs/backtest.json` with **non-stub** justifications and, ideally, **news_features** populated when `ALPHAVANTAGE_API_KEY` is in **repo-root `.env`** (not only a one-off terminal variable).

6. **Quality check** — Open `outputs/summary.json`: note agreements vs disagreements. If everything is still HOLD everywhere, consider rerunning after AV data loads or adjusting tickers; document honestly in the report.

7. **Reports (PDF)** — Edit names/content in `report/comparative_analysis.tex` and `report/ai_use_appendix.tex`, then build per [`report/LATEX_BUILD.md`](report/LATEX_BUILD.md). Align numbers/excerpts with the JSON you keep for submission.

8. **Git** — After outputs (and optional PDFs) are final:
   ```powershell
   git add -A
   git status
   git commit -m "Refresh outputs and report artifacts from laptop"
   git push origin master
   ```

9. **Other machine** — On the desktop, `git pull` so both clones match `master`.

**Handoff / continuity:** [`docs/HANDOFF_NEXT_AGENT.md`](docs/HANDOFF_NEXT_AGENT.md)

---

## Status at a glance

### Done (project-wide)

- **Implementation:** AutoGen `AssistantAgent`, parallel strategies, evaluator; see `src/`.
- **Alpha Vantage:** Integrated in `src/market_data.py`; key lives only in **local** `.env`.
- **Docs:** `README.md`, `docs/ALPHA_VANTAGE.md`, handoff doc, LaTeX drafts under `report/`.

### Left to do (until submission)

- [ ] Laptop: `.env` present with `ALPHAVANTAGE_API_KEY` + successful live run → refreshed `outputs/`.
- [ ] Compile PDFs from `report/*.tex`; submit per course naming (`report.pdf`, AI appendix).
- [ ] Final commit/push; optional pull on desktop for parity.

---

## Execution stack (reference)

- **Agents:** AutoGen `AssistantAgent` + structured Pydantic outputs; no strategy cross-talk before evaluation.
- **Models:** Ollama (`src/llm_factory.py`); optional LiteLLM proxy via `LITELLM_*`.
- **Strategies:** News Sentiment Follower (`strategy_a`), Volatility Averse (`strategy_b`), Moral Trader (`strategy_c`).
- **Bonuses:** `outputs/backtest.json`; third agent in outputs + evaluator.

## Remote

[https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git](https://github.com/afro-chai/AGAI_HW2-IndividualAssignment-Coding.git)
