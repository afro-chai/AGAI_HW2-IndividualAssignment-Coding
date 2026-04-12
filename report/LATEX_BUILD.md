# Building PDFs from LaTeX

Ticker research catalog (defense / geopolitics / AFRICOM): [`DEFENSE_GEOPOLITICS_UNIVERSE.md`](DEFENSE_GEOPOLITICS_UNIVERSE.md).

From this `report/` directory (with a LaTeX distribution installed, e.g. MiKTeX or TeX Live):

```powershell
pdflatex comparative_analysis.tex
pdflatex ai_use_appendix.tex
```

Course submission names the main report as `report.pdf`. After building, rename as needed:

```powershell
Copy-Item comparative_analysis.pdf report.pdf
Copy-Item ai_use_appendix.pdf ai_use_appendix.pdf
```

Run `pdflatex` twice if references require a second pass.
