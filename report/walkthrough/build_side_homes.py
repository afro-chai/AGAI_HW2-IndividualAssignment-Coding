# -*- coding: utf-8 -*-
"""One-off: build LowSide_Home.html and GreenSide_Home.html from Project_Home.html panels."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> None:
    ph = (ROOT / "Project_Home.html").read_text(encoding="utf-8")
    s_low = ph.index("<!-- Low-side panel -->")
    e_low = ph.index("<!-- Green panel -->")
    low_panel = ph[s_low:e_low].strip()
    s_green = ph.index("<!-- Green panel -->")
    e_green = ph.index('   </div>\n   <section aria-labelledby="tree-heading"')
    green_panel = ph[s_green:e_green].strip()

    future_nipr = """
   <section aria-labelledby=\"future-int-heading\" class=\"future-int-section\">
    <h2 id=\"future-int-heading\">
     Future intelligence disciplines (OPEN / low-side)
    </h2>
    <p class=\"future-int-lede\">
     Placeholder nodes for additional INT types and tooling on the low-side path. Not in scope for
     Phase 1; reserved for later development on the low-side tier and related paths.
    </p>
    <div class=\"future-int-grid\">
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>HUMINT</strong> &mdash; human-source interfaces (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>MASINT</strong> &mdash; measurement and signature collection (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>SIGINT / ELINT</strong> &mdash; communications and electronic intelligence feeds (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>CYBER INT</strong> &mdash; network and technical indicators (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>FININT / ACINT</strong> &mdash; financial and activity feeds (not built).
     </div>
    </div>
   </section>"""

    future_green = """
   <section aria-labelledby=\"future-int-heading-green\" class=\"future-int-section\">
    <h2 id=\"future-int-heading-green\">
     Future intelligence disciplines (NIPR / green-side)
    </h2>
    <p class=\"future-int-lede\">
     Placeholder nodes for additional INT types and tooling on the green-side path. Not in scope for
     Phase 1; reserved for later development on NIPR and higher paths.
    </p>
    <div class=\"future-int-grid\">
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>HUMINT</strong> &mdash; human-source interfaces (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>MASINT</strong> &mdash; measurement and signature collection (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>SIGINT / ELINT</strong> &mdash; communications and electronic intelligence feeds (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>CYBER INT</strong> &mdash; network and technical indicators (not built).
     </div>
     <div class=\"future-int-card\">
      <div class=\"ph\">Reserved</div>
      <strong>FININT / ACINT</strong> &mdash; financial and activity feeds (not built).
     </div>
    </div>
   </section>"""

    # LowSide_Home.html = OPEN hub (left / low-side pipeline). GreenSide_Home.html = NIPR hub.
    nav_on_open_hub = """   <nav aria-label="Site navigation" class="site-nav-top">
    <a href="Project_Home.html#conceptual-architecture">Map</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="Scope.html">Scope</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="MultiAgentSystemCanvas_AFRICOM.html">System Canvas</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <span class="site-nav-now">OPEN</span>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="GreenSide_Home.html">NIPR</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="Project_Home.html#repo-map">Repository Outline</a>
   </nav>"""

    nav_on_nipr_hub = """   <nav aria-label="Site navigation" class="site-nav-top">
    <a href="Project_Home.html#conceptual-architecture">Map</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="Scope.html">Scope</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="MultiAgentSystemCanvas_AFRICOM.html">System Canvas</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="LowSide_Home.html">OPEN</a>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <span class="site-nav-now">NIPR</span>
    <span aria-hidden="true" class="site-nav-sep">&middot;</span>
    <a href="Project_Home.html#repo-map">Repository Outline</a>
   </nav>"""

    foot = """   <footer aria-label="Site navigation footer" class="repo-map-footer">
    <p class="repo-map-title">
     <a href="Project_Home.html#conceptual-architecture">Map</a>
     &middot;
     <a href="Scope.html">Scope</a>
     &middot;
     <a href="MultiAgentSystemCanvas_AFRICOM.html">System Canvas</a>
     &middot;
     <a href="LowSide_Home.html">OPEN</a>
     &middot;
     <a href="GreenSide_Home.html">NIPR</a>
     &middot;
     <a href="Project_Home.html#repo-map">Repository Outline</a>
    </p>
    <p class="footer-note" style="margin-top:10px;">
     <a href="Project_Home.html">Full project map (both tiers)</a>
    </p>
   </footer>"""

    head = """<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>{title}</title>
  <link href="site_nav.css" rel="stylesheet"/>
  <link href="project_hub.css" rel="stylesheet"/>
 </head>
 <body>
  <div class="wrap">
"""

    low_doc = (
        head.format(title="OPEN &mdash; Low-side home")
        + nav_on_open_hub
        + """
   <header class="header-bar">
    <h1>OPEN (low-side home)</h1>
    <span class="course">94815 &middot; Agentic Technologies &middot; Track A</span>
   </header>
   <p class="lede">
    Expandable home for the OPEN / PAI pipeline: same agent nodes as the project map, with room for
    notes, SOPs, and future low-side INT additions. Pair with
    <a href="GreenSide_Home.html">NIPR home</a> (green-side hub) for the sister tier.
   </p>
   <div class="masc-banner">
    <p><strong>Two-tier context</strong> &mdash; open the full conceptual architecture on the
    project map when you need both pipelines.</p>
    <a class="btn" href="Project_Home.html#conceptual-architecture">View conceptual architecture
    (both tiers)</a>
   </div>
   <p class="diagram-title">OPEN pipeline &mdash; clickable agent specs</p>
   <div class="panels panels-single" role="region">
"""
        + low_panel
        + """
   </div>
"""
        + future_nipr
        + foot
        + """
  </div>
 </body>
</html>
"""
    )

    green_doc = (
        head.format(title="NIPR &mdash; Green-side home")
        + nav_on_nipr_hub
        + """
   <header class="header-bar">
    <h1>NIPR (green-side home)</h1>
    <span class="course">94815 &middot; Agentic Technologies &middot; Track A</span>
   </header>
   <p class="lede">
    Expandable home for the NIPR / green-side pipeline: marked fixtures, releasability path, and future
    higher-side INT work. Pair with <a href="LowSide_Home.html">OPEN home</a> (low-side hub).
   </p>
   <div class="masc-banner">
    <p><strong>Two-tier context</strong> &mdash; open the full conceptual architecture on the
    project map when you need both pipelines.</p>
    <a class="btn" href="Project_Home.html#conceptual-architecture">View conceptual architecture
    (both tiers)</a>
   </div>
   <p class="diagram-title">NIPR pipeline &mdash; clickable agent specs</p>
   <div class="panels panels-single" role="region">
"""
        + green_panel
        + """
   </div>
"""
        + future_green
        + foot
        + """
  </div>
 </body>
</html>
"""
    )

    (ROOT / "LowSide_Home.html").write_text(low_doc, encoding="utf-8", newline="\n")
    (ROOT / "GreenSide_Home.html").write_text(green_doc, encoding="utf-8", newline="\n")
    print("Wrote LowSide_Home.html and GreenSide_Home.html")


if __name__ == "__main__":
    main()
