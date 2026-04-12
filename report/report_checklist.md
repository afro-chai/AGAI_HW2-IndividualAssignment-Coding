# Report Checklist (next session)

- [ ] Strategy Selection and Rationale
- [ ] System Architecture + diagram
- [ ] Stock Selection and Rationale (default **10** defense/geopolitics tickers; see `report/DEFENSE_GEOPOLITICS_UNIVERSE.md`)
- [ ] Results by Stock (include JSON excerpts)
- [ ] Patterns of Agreement and Disagreement (quantitative)
- [ ] Failure or Surprise Case
- [ ] Reflection
- [ ] AI Use Appendix with file-level attribution

## Quantitative minimums

- Pull `total_agreements` and `total_disagreements` from `outputs/summary.json`.
- For each stock, include decisions and confidence values for Strategy A/B (+ C if used).
- Include confidence spread (max - min) per stock.
- Include backtest per-ticker hit rates from `outputs/backtest.json`.

## Attribution minimums

- Track AI-assisted edits by file path.
- Mark each AI suggestion as accepted/revised/rejected.
- List at least one independently verified numeric check.
