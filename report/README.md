# report/

Written deliverables: LaTeX sources for the comparative analysis and AI-use appendix, plus the defense/geopolitics ticker universe note. Build PDFs per your LaTeX toolchain; submit `report.pdf` (and appendix) per course instructions.

## Walkthrough (`walkthrough/`)

Static **HTML** pages (open locally in a browser) that mirror the **three strategy agents + one evaluator** architecture from `comparative_analysis.tex` / `src/`—useful for graders who prefer a clickable diagram over LaTeX alone.

| File | Description |
|------|-------------|
| [`walkthrough/StockTrader_Walkthrough_Home.html`](walkthrough/StockTrader_Walkthrough_Home.html) | Home: SVG diagram (market data → three agents → evaluator) + links. |
| [`walkthrough/StockTrader_MultiAgent_System_Canvas.html`](walkthrough/StockTrader_MultiAgent_System_Canvas.html) | System canvas: control flow, parallelism, JSON persistence. |
| [`walkthrough/AgentCanvas_StrategyA_NewsSentiment.html`](walkthrough/AgentCanvas_StrategyA_NewsSentiment.html) | Strategy A — News Sentiment Follower. |
| [`walkthrough/AgentCanvas_StrategyB_VolatilityAverse.html`](walkthrough/AgentCanvas_StrategyB_VolatilityAverse.html) | Strategy B — Volatility Averse. |
| [`walkthrough/AgentCanvas_StrategyC_MoralTrader.html`](walkthrough/AgentCanvas_StrategyC_MoralTrader.html) | Strategy C — Moral Trader. |
| [`walkthrough/AgentCanvas_Evaluator.html`](walkthrough/AgentCanvas_Evaluator.html) | Evaluator agent + branching logic. |
