# -*- coding: utf-8 -*-
"""Generate Phase 1 Agent Canvas HTML files (suffix _L = lowside, _G = green).

Run from phase1/: python gen_agent_canvases.py
"""
from __future__ import annotations

import html
from pathlib import Path

from bs4 import BeautifulSoup

from wrap_html_lines import wrap_html_source

ROOT = Path(__file__).resolve().parent

LOW_AGENT_LINKS: list[tuple[str, str]] = [
    ("AgentCanvas_OSINT_L.html", "OSINT"),
    ("AgentCanvas_GEOINT_L.html", "GEOINT"),
    ("AgentCanvas_Fusion_L.html", "Fusion"),
    ("AgentCanvas_SECMAN_L.html", "SECMAN"),
    ("AgentCanvas_Products_L.html", "Products"),
    ("AgentCanvas_Translation_L.html", "Translation (low)"),
]
GREEN_AGENT_LINKS: list[tuple[str, str]] = [
    ("AgentCanvas_GEOINT_G.html", "GEOINT"),
    ("AgentCanvas_GreenInt_G.html", "GreenInt"),
    ("AgentCanvas_Fusion_G.html", "Fusion"),
    ("AgentCanvas_SECMAN_G.html", "SECMAN"),
    ("AgentCanvas_Products_G.html", "Products"),
    ("AgentCanvas_Translation_G.html", "Translation (green)"),
]


def _nav_here(text: str) -> str:
    return f'<span class="site-nav-now">{html.escape(text)}</span>'


def _nav_a(href: str, text: str) -> str:
    return f'<a href="{html.escape(href)}">{html.escape(text)}</a>'


def _footer_link(href: str, text: str, is_here: bool) -> str:
    if is_here:
        return f'<span class="repo-map-here">{html.escape(text)}</span>'
    return f'<a href="{html.escape(href)}">{html.escape(text)}</a>'


def site_nav_top_html(*, path_prefix: str, active: str) -> str:
    """Six global crumbs. active: phase1_map | project_scope | system_canvas | open | nipr | repository_outline | ""."""
    pm = f"{path_prefix}Project_Home.html#conceptual-architecture"
    scope_h = f"{path_prefix}Scope.html"
    open_h = f"{path_prefix}LowSide_Home.html"
    nipr_h = f"{path_prefix}GreenSide_Home.html"
    sc_h = f"{path_prefix}MultiAgentSystemCanvas_AFRICOM.html"
    ro_h = f"{path_prefix}Project_Home.html#repo-map"

    def item(key: str, href: str, label: str) -> str:
        if active == key:
            return _nav_here(label)
        return _nav_a(href, label)

    parts = [
        item("phase1_map", pm, "Map"),
        '<span class="site-nav-sep" aria-hidden="true">&middot;</span>',
        item("project_scope", scope_h, "Scope"),
        '<span class="site-nav-sep" aria-hidden="true">&middot;</span>',
        item("system_canvas", sc_h, "System Canvas"),
        '<span class="site-nav-sep" aria-hidden="true">&middot;</span>',
        item("open", open_h, "OPEN"),
        '<span class="site-nav-sep" aria-hidden="true">&middot;</span>',
        item("nipr", nipr_h, "NIPR"),
        '<span class="site-nav-sep" aria-hidden="true">&middot;</span>',
        item("repository_outline", ro_h, "Repository Outline"),
    ]
    inner = "\n    ".join(parts)
    return f"""<nav class="site-nav-top" aria-label="Site navigation">
    {inner}
  </nav>"""


def repo_map_footer_html(*, nav_mode: str, current_file: str) -> str:
    if nav_mode == "root":
        pfx, low_p, green_p = "", "lowside/", "green/"
    elif nav_mode == "lowside":
        pfx, low_p, green_p = "../", "", "../green/"
    else:
        pfx, low_p, green_p = "../", "../lowside/", ""

    ca_h = f"{pfx}Project_Home.html#conceptual-architecture"
    scope_h = f"{pfx}Scope.html"
    open_h = f"{pfx}LowSide_Home.html"
    nipr_h = f"{pfx}GreenSide_Home.html"
    masc_h = f"{pfx}MultiAgentSystemCanvas_AFRICOM.html"
    ro_h = f"{pfx}Project_Home.html#repo-map"
    nav_line = " &middot; ".join(
        [
            _nav_a(ca_h, "Map"),
            _nav_a(scope_h, "Scope"),
            _nav_a(masc_h, "System Canvas"),
            _nav_a(open_h, "OPEN"),
            _nav_a(nipr_h, "NIPR"),
            _nav_a(ro_h, "Repository Outline"),
        ]
    )
    low_links = " &middot; ".join(
        _footer_link(f"{low_p}{fn}", lab, current_file == fn)
        for fn, lab in LOW_AGENT_LINKS
    )
    green_links = " &middot; ".join(
        _footer_link(f"{green_p}{fn}", lab, current_file == fn)
        for fn, lab in GREEN_AGENT_LINKS
    )
    return f"""<footer class="repo-map-footer" aria-label="Repository map">
    <p class="repo-map-title">{nav_line}</p>
    <div class="repo-map-cols">
      <div>
        <span class="repo-map-label">Low-side specs</span>
        <div class="repo-map-links">{low_links}</div>
      </div>
      <div>
        <span class="repo-map-label">Green-side specs</span>
        <div class="repo-map-links">{green_links}</div>
      </div>
    </div>
  </footer>"""


def agent_short_label(filename: str) -> str:
    for fn, lab in LOW_AGENT_LINKS + GREEN_AGENT_LINKS:
        if fn == filename:
            return lab
    return filename


def rows(cls: str, labels_texts: list[tuple[str, str]]) -> str:
    bits = []
    for lab, txt in labels_texts:
        bits.append(
            f"""            <div class="field-row">
              <span class="field-row-label {cls}">{html.escape(lab)}</span>
              <span class="field-row-text">{html.escape(txt)}</span>
            </div>"""
        )
    return "\n".join(bits)


def build_page(
    *,
    title: str,
    subtitle: str,
    footer_right: str,
    use_case: str,
    task: str,
    stakeholders: list[tuple[str, str]],
    ins: list[str],
    outs: list[str],
    allow: list[str],
    may_do: list[str],
    deny: list[str],
    autonomous: list[str],
    gated: list[str],
    policies: list[tuple[str, str]],
    memory_lines: list[tuple[str, str]],
    failures: list[str],
    escalations: list[str],
    success: list[tuple[str, str]],
    nav_mode: str,
    nav_current_file: str,
    nav_path_prefix: str,
    nav_active: str,
) -> str:
    st_rows = rows("field-row-label-1", stakeholders)
    in_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-2">IN</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in ins
    )
    out_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-2">OUT</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in outs
    )
    allow_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-2">ALLOW</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in allow
    )
    may_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-2">MAY DO</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in may_do
    )
    deny_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-2">DENY</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in deny
    )
    auto_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-2">Autonomous</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in autonomous
    )
    gated_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-2">Gated</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in gated
    )
    pol_rows = rows("field-row-label-2", policies)
    mem_rows = rows("field-row-label-3", memory_lines)
    fail_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-3">Fail</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in failures
    )
    esc_rows = "\n".join(
        f"""            <div class="field-row">
              <span class="field-row-label field-row-label-3">Escalate</span>
              <span class="field-row-text">{html.escape(s)}</span>
            </div>"""
        for s in escalations
    )
    succ_rows = rows("field-row-label-3", success)

    nav_top = site_nav_top_html(path_prefix=nav_path_prefix, active=nav_active)
    nav_foot = repo_map_footer_html(
        nav_mode=nav_mode,
        current_file=nav_current_file,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="../agent_canvas.css">
<link rel="stylesheet" href="../site_nav.css">
</head>
<body>

<div class="container">
  {nav_top}
  <div class="header">
    <div class="header-bar">
      <h1>Agent System Specification Canvas</h1>
      <span class="course">94815 · Agentic Technologies · Track A</span>
    </div>
    <div class="subtitle">{html.escape(subtitle)}</div>
  </div>

  <div class="container canvas">
    <div class="flow-indicator"></div>
    <div class="zone zone-1">
      <div class="zone-badge zone-badge-1">
      <span class="zone-num zone-num-1">1</span>
      <span class="zone-label zone-label-1">System Intent</span>
    </div>
      <div class="row row-full"><div class="field field-z1 bookend-1">
      <div class="field-num field-num-1">1</div>
      <div class="field-header">
        <span class="field-icon">🎯</span>
        <span class="field-title prominent field-title-1">Use Case / Purpose</span>
      </div>
      <div class="field-text">{html.escape(use_case)}</div>
    </div></div>
<div class="row row-half"><div class="field field-z1">
      <div class="field-num field-num-1">2</div>
      <div class="field-header">
        <span class="field-icon">✂️</span>
        <span class="field-title field-title-1">Task Slice / Goal</span>
      </div>
      <div class="field-text">{html.escape(task)}</div>
    </div><div class="field field-z1">
      <div class="field-num field-num-1">3</div>
      <div class="field-header">
        <span class="field-icon">👥</span>
        <span class="field-title field-title-1">Users / Stakeholders</span>
      </div>
      <div class="field-rows">
{st_rows}
</div>
    </div></div>
    </div><div class="zone zone-2">
      <div class="zone-badge zone-badge-2">
      <span class="zone-num zone-num-2">2</span>
      <span class="zone-label zone-label-2">Bounded Behavior</span>
    </div>
      <div class="row row-half"><div class="field field-z2">
      <div class="field-num field-num-2">4</div>
      <div class="field-header">
        <span class="field-icon">⇄</span>
        <span class="field-title field-title-2">Inputs / Outputs</span>
      </div>
      <div class="field-rows">
{in_rows}
{out_rows}
</div>
    </div><div class="field field-z2">
      <div class="field-num field-num-2">5</div>
      <div class="field-header">
        <span class="field-icon">🔧</span>
        <span class="field-title field-title-2">Tools / Permissions</span>
      </div>
      <div class="field-rows">
{allow_rows}
{may_rows}
{deny_rows}
</div>
    </div></div>
<div class="row row-half"><div class="field field-z2">
      <div class="field-num field-num-2">6</div>
      <div class="field-header">
        <span class="field-icon">🛡️</span>
        <span class="field-title field-title-2">Autonomy / Human Checkpoints</span>
      </div>
      <div class="field-rows">
{auto_rows}
{gated_rows}
</div>
    </div><div class="field field-z2">
      <div class="field-num field-num-2">7</div>
      <div class="field-header">
        <span class="field-icon">📜</span>
        <span class="field-title field-title-2">Operating Rules / Policies</span>
      </div>
      <div class="field-rows">
{pol_rows}
</div>
    </div></div>
      <div class="watermark">Bounded Agentic System</div>
    </div><div class="zone zone-3">
      <div class="zone-badge zone-badge-3">
      <span class="zone-num zone-num-3">3</span>
      <span class="zone-label zone-label-3">Context & Evaluation</span>
    </div>
      <div class="row row-half"><div class="field field-z3">
      <div class="field-num field-num-3">8</div>
      <div class="field-header">
        <span class="field-icon">💾</span>
        <span class="field-title field-title-3">Memory / Context</span>
      </div>
      <div class="field-rows">
{mem_rows}
</div>
    </div><div class="field field-z3">
      <div class="field-num field-num-3">9</div>
      <div class="field-header">
        <span class="field-icon">⚠️</span>
        <span class="field-title field-title-3">Failure Conditions / Escalations</span>
      </div>
      <div class="field-rows">
{fail_rows}
{esc_rows}
</div>
    </div></div>
<div class="row row-full"><div class="field field-z3 bookend-3">
      <div class="field-num field-num-3">10</div>
      <div class="field-header">
        <span class="field-icon">✅</span>
        <span class="field-title prominent field-title-3">Success Criteria</span>
      </div>
      <div class="field-rows">
{succ_rows}
</div>
    </div></div>
    </div>
  </div>

  <div class="container footer">
    <span class="footer-left">Define intent, bounded behavior, and evaluation before choosing architecture</span>
    <span class="footer-right">{html.escape(footer_right)}</span>
  </div>
  {nav_foot}
</div>

</body>
</html>
"""


def write(subdir: str, name: str, **kwargs) -> None:
    p = ROOT / subdir / name
    p.parent.mkdir(parents=True, exist_ok=True)
    nav_mode = "lowside" if subdir == "lowside" else "green"
    raw = build_page(
        **kwargs,
        nav_mode=nav_mode,
        nav_current_file=name,
        nav_path_prefix="../",
        nav_active="",
    )
    pretty = BeautifulSoup(raw, "html.parser").prettify(formatter="html")
    pretty = wrap_html_source(pretty)
    p.write_text(pretty, encoding="utf-8", newline="\n")
    print("Wrote", p.relative_to(ROOT.parent))


HITL_GATE = "Final dissemination and partner release remain human-gated after Products (see Multi-Agent System Canvas)."
HITL_PARTNER_INTERPRETER_LOW = (
    "Partner interpreter / liaison (not required to be uniformed) confirms translated PAI text "
    "before partner handoff; English bundle still passes staff HITL first."
)


def main() -> None:
    foot_low = "AFRICOM OSINT · low-side · Phase 1"
    foot_green = "AFRICOM OSINT · green-side (open-internet path) · Phase 1"

    write(
        "lowside",
        "AgentCanvas_OSINT_L.html",
        title="Agent Canvas — OSINT Collection (low-side)",
        subtitle=(
            "OSINT Collection Agent — passive open-web collection from explicit seed allowlists, "
            "up to three link hops from seeds, per-source legitimacy scoring, and corroboration "
            "rules for fast-breaking social sources."
        ),
        footer_right=foot_low,
        use_case=(
            "Deliver timely OSINT Summaries while biasing Fusion toward legitimate outlets: "
            "support fast reporting but treat first reports from Twitter and similar as unverified "
            "until at least one independent corroborating source is collected."
        ),
        task=(
            "Start from an explicit seed allowlist (domains, RSS/API feeds). Passively fetch and "
            "parse articles; extract outbound references and follow them up to three hops deep "
            "from each seed URL (each hop is one rabbit hole). Score every domain and article for "
            "source legitimacy (tier tables, heuristics, optional fact-check or reputation lookup). "
            "Tag items for Fusion weighting; down-rank or flag uncorroborated social-first claims. "
            "Dedupe, attach metadata (source, time, language, URL, hop depth, legitimacy score), "
            "emit OSINT Summary."
        ),
        stakeholders=[
            ("Downstream", "Fusion Agent (primary consumer)"),
            ("Beneficiary", "Staff officers and analysts consuming finished products"),
            ("Human", "HITL reviews only after Products; not part of this agent"),
        ],
        ins=[
            "Scheduler / trigger (e.g., daily run or event-driven refresh)",
            "Seed allowlist: domains, RSS/API endpoints, and optional starter URLs (PAI only)",
            "Optional fact-check / domain-viability API or lookup table version id",
        ],
        outs=[
            "OSINT Summary — structured findings with provenance, hop depth from seed, legitimacy score",
            "Ingestion log: fetch status, corroboration flags, errors, skipped items",
        ],
        allow=[
            "Passive HTTP/HTTPS GET and RSS read only (no posting, no credential use)",
            "Fetch any public URL reachable within three hops from a seed page via extracted links",
            "HTML/article parsing, language detection, link extraction, basic dedupe",
            "Legitimacy scoring: rules, learned tiers, and/or external fact-check or viability checks",
            "Write to run-scoped artifact store for this collection batch",
        ],
        may_do=[
            "Respect robots.txt and per-domain rate limits when configured",
            "Treat wire / major outlet tiers as higher legitimacy priors in the scorer",
        ],
        deny=[
            "Access to classified systems or stolen credentials",
            "Following beyond the third hop from a seed URL without a new seed path",
            "Non-passive actions: logins, form submission, comments, votes, purchases, partner email",
            "Automated public posting or claiming verification without corroboration metadata",
        ],
        autonomous=[
            "Expand from seeds, score sources, apply corroboration rules, package OSINT Summary",
        ],
        gated=[
            HITL_GATE,
        ],
        policies=[
            ("PAI ONLY", "No simulated classified content in collection outputs"),
            ("3-HOP", "Link expansion depth from any seed URL ≤ 3; log full chain for audit"),
            ("LEGITIMACY", "Every emitted item carries legitimacy score and category; emphasis on established news"),
            ("SOCIAL FIRST", "Twitter/X and similar first reports stay low-confidence until corroborated elsewhere"),
            ("TRACE", "Every observation retains URL, hop depth from seed, retrieval time"),
            ("UNCERT.", "If parse or scoring fails, emit partial with explicit gap flag"),
        ],
        memory_lines=[
            ("Session", "Current batch, per-seed crawl frontier, hop depth map, fetch cursors"),
            ("Context", "Rolling dedupe hashes; cached domain legitimacy scores for this run"),
        ],
        failures=[
            "Source timeout, rate limit, paywall or unexpected HTML structure",
            "Fact-check or reputation service unavailable",
            "Conflicting timestamps or contradictory claims across sources",
        ],
        escalations=[
            "Repeated failures from a tier-1 seed → mark degraded and continue other seeds",
            "Viral single-source social burst → emit breaking flag with corroboration-required tag",
        ],
        success=[
            ("Seeds", "All configured seed entry points attempted each run with logged outcomes"),
            ("Depth", "No fetch attributed to more than three hops from its seed URL"),
            ("Legitimacy", "100% of OSINT Summary items include score and legitimacy category"),
            ("Schema", "100% of OSINT Summary payloads validate against Observation schema"),
            ("Corroboration", "Social-first claims carry corroboration state per policy"),
        ],
    )

    write(
        "lowside",
        "AgentCanvas_GEOINT_L.html",
        title="Agent Canvas — GEOINT Collection (low-side)",
        subtitle="GEOINT Collection Agent — public geospatial context (ArcGIS / map APIs / OSM-style layers) for AFRICOM AOI.",
        footer_right=foot_low,
        use_case="Provide geospatial context for OSINT narratives: locations, distances, key infrastructure references derived from public map data.",
        task="Resolve placenames to coordinates where possible, fetch public basemap or feature layers, compute simple proximity context (e.g., distance to airports, ports), produce GEOINT Summary for Fusion.",
        stakeholders=[
            ("Downstream", "Fusion Agent"),
            ("Beneficiary", "Analysts validating location claims"),
            ("Human", HITL_GATE),
        ],
        ins=[
            "Placenames, regions, or lat/lon hints from OSINT or user AOI config",
            "Public map/GIS endpoints and layer definitions (PAI)",
        ],
        outs=[
            "GEOINT Summary — structured report of geospatial findings with provenance for Fusion",
            "Geocoding confidence and source layer attribution log",
        ],
        allow=[
            "Geocode API, public feature queries, distance/bearing calculations",
        ],
        may_do=[
            "Emit uncertainty bands when geocode is approximate",
        ],
        deny=[
            "Classified imagery or restricted military map servers",
            "Storing precise coordinates of protected individuals (minimize PII)",
        ],
        autonomous=[
            "Geocode, query layers, package geometry summaries for Fusion",
        ],
        gated=[
            HITL_GATE,
        ],
        policies=[
            ("PUBLIC", "Only public or demo-safe layers"),
            ("LABEL", "Tag coordinate system and layer version on every feature"),
        ],
        memory_lines=[
            ("Session", "Pending geocode queue and last-good AOI bounds"),
            ("Context", "Cached tile/layer responses for single run only"),
        ],
        failures=[
            "Ambiguous placename (multiple matches)",
            "Layer outage or quota exceeded",
        ],
        escalations=[
            "Ambiguity → emit multiple candidates with scores for Fusion to reconcile",
        ],
        success=[
            ("Linkage", "Geo outputs reference parent observation or event ids"),
            ("Attribution", "Layer/source named for every geometry output"),
            ("Honesty", "Low-confidence geocodes explicitly flagged"),
        ],
    )

    write(
        "lowside",
        "AgentCanvas_Fusion_L.html",
        title="Agent Canvas — Fusion (low-side)",
        subtitle="Fusion Agent — merges OSINT and GEOINT streams; iterates with SECMAN and Products per pipeline loop.",
        footer_right=foot_low,
        use_case="Reduce fragmentation between textual reporting and geospatial context by producing a single, time-bounded operational picture for the low-side cell.",
        task="Align events across OSINT observations and GEOINT features, deduplicate, detect conflicts, produce an Intelligence Summary (timeline + map-linked bullets) for SECMAN review.",
        stakeholders=[
            ("Upstream", "OSINT and GEOINT collection agents"),
            ("Peer", "SECMAN and Products agents (bidirectional loop)"),
            ("Human", HITL_GATE),
        ],
        ins=[
            "Observation stream from OSINT agent",
            "GeoFeature / GeoContext from GEOINT agent",
            "Feedback requests from SECMAN (marking gaps) or Products (format gaps)",
        ],
        outs=[
            "Intelligence Summary — versioned structured fusion report for SECMAN",
            "Conflict and uncertainty register for SECMAN/Products",
        ],
        allow=[
            "Read/write run-scoped fusion workspace",
            "LLM-assisted clustering and summarization with schema constraints",
        ],
        may_do=[
            "Request re-fetch or clarification via orchestrator (not direct human)",
        ],
        deny=[
            "Changing source URLs or fabricating coordinates",
            "Bypassing SECMAN marking requirements before Products",
        ],
        autonomous=[
            "Merge, correlate, and version fusion outputs until stop condition",
        ],
        gated=[
            "Release to external networks only after downstream HITL (system-level)",
        ],
        policies=[
            ("CONFLICT", "Never silently resolve; surface competing claims"),
            ("TIME", "Respect collection timestamps; flag stale items"),
        ],
        memory_lines=[
            ("Session", "Current fusion graph, prior package versions in this run"),
            ("Context", "Active AOI and topic filters from mission profile"),
        ],
        failures=[
            "Empty or one-sided inputs (only OSINT or only GEOINT)",
            "Irreconcilable location vs. narrative",
        ],
        escalations=[
            "High-impact conflict → elevate severity flag in package for SECMAN",
        ],
        success=[
            ("Integration", "Every narrative bullet ties to zero or more geo refs"),
            ("Versioning", "Each loop increments package version with changelog"),
            ("Trace", "Sources preserved end-to-end from observations"),
        ],
    )

    write(
        "lowside",
        "AgentCanvas_SECMAN_L.html",
        title="Agent Canvas — SECMAN (low-side)",
        subtitle="Security Management Agent — simulated classification-style markings, formatting gates, and release-prep rules on low-side artifacts.",
        footer_right=foot_low,
        use_case="Enforce consistent handling labels and structural checks so Products can render RAW + PRETTY packages suitable for human review.",
        task="Apply marking templates (e.g., UNCLASSIFIED / simulated caveats), validate required fields, request Fusion/Products revisions when schema or policy checks fail.",
        stakeholders=[
            ("Upstream", "Fusion Agent"),
            ("Peer", "Products Agent"),
            ("Human", "HITL is final release authority"),
        ],
        ins=[
            "Intelligence Summary and conflict register",
            "Organization policy stub (marking dictionary, course-safe)",
        ],
        outs=[
            "Tagged INTSUM — SECMAN-approved draft with markings block",
            "List of blocking issues OR clearance token for Products",
        ],
        allow=[
            "Rule engine + LLM assist for labeling suggestions (human-readable rationale)",
            "Write annotations back to shared artifact",
        ],
        may_do=[
            "Downgrade content to reference-only if source quality insufficient (flag)",
        ],
        deny=[
            "Authorizing actual public release (HITL only)",
            "Inventing classification beyond simulated labels",
        ],
        autonomous=[
            "Run checks, attach markings, gate forward when checks pass",
        ],
        gated=[
            HITL_GATE,
        ],
        policies=[
            ("NO FABRICATION", "Markings must map to explicit rules or stubs"),
            ("SCHEMA", "Block Products if required sections missing"),
        ],
        memory_lines=[
            ("Session", "Checklist state per package version"),
            ("Context", "Applicable policy version id for audit trail"),
        ],
        failures=[
            "Missing provenance for a highlighted claim",
            "Conflicting marking suggestions from rules vs. model",
        ],
        escalations=[
            "Unresolved policy ambiguity → block and annotate for human reviewer",
        ],
        success=[
            ("Consistency", "Markings applied uniformly across sections"),
            ("Block rate", "Zero false 'pass' when required fields absent"),
            ("Audit", "Each decision logged with rule id or rationale stub"),
        ],
    )

    write(
        "lowside",
        "AgentCanvas_Products_L.html",
        title="Agent Canvas — Products (low-side)",
        subtitle="Product Producer Agent — formats SECMAN-cleared fusion into RAW + PRETTY staff-ready outputs for HITL.",
        footer_right=foot_low,
        use_case="Deliver standardized intelligence-style summaries that staff can scan quickly while preserving pointers to evidence for reviewers.",
        task="Render dual outputs: RAW (dense, citation-heavy) and PRETTY (executive skim); align to template; hand off to HITL queue (not automated send).",
        stakeholders=[
            ("Upstream", "SECMAN, Fusion (for rework)"),
            ("Downstream", "Translation (low) (optional, post–staff HITL)"),
            ("Consumer", "Staff officers, decision makers (after HITL)"),
            ("Human", "Staff HITL reviewer; partner interpreter separate for Translation (low)"),
        ],
        ins=[
            "SECMAN-approved draft with markings",
            "Template id (daily summary, spot report, etc.)",
        ],
        outs=[
            "INTSUM, SIGACTs, and targeting packet artifacts plus RAW + PRETTY review bundle",
            "Export bundle metadata for review UI / GitLab-attached run",
            (
                "Releasable + translated GEOINT Summary, OSINT Summary, Intelligence Summary, "
                "INTSUMs, SIGACTs, and targeting packets via Translation (low) when routed post–staff HITL"
            ),
        ],
        allow=[
            "Template rendering, section reordering within schema",
            "LLM polish constrained to provided facts only",
        ],
        may_do=[
            "Request Fusion/SECMAN loop if facts insufficient for template section",
        ],
        deny=[
            "Adding uncited facts or external web search at this stage",
            "Emailing or posting products automatically",
            "Invoking Translation (low) before staff HITL approval",
        ],
        autonomous=[
            "Format, validate template completeness, package for review",
        ],
        gated=[
            "Staff HITL before external routing; Translation (low) only after HITL + interpreter path",
        ],
        policies=[
            ("CITE", "Every PRETTY bullet maps to RAW evidence list"),
            ("TONE", "Neutral analytic voice; no policy prescription"),
        ],
        memory_lines=[
            ("Session", "Draft render versions and template variables"),
            ("Context", "Active product type and audience hint (internal only)"),
        ],
        failures=[
            "Template section cannot be filled from approved facts",
            "Markings text overflows layout constraints",
        ],
        escalations=[
            "Emit partial PRETTY with explicit 'data gap' section",
        ],
        success=[
            ("Dual output", "RAW and PRETTY generated and cross-linked"),
            ("Schema", "Passes automated template validator"),
            ("HITL-ready", "Queue payload contains reviewer checklist fields"),
        ],
    )

    write(
        "lowside",
        "AgentCanvas_Translation_L.html",
        title="Agent Canvas — Translation (low-side)",
        subtitle="Translation Agent — PAI-only products; partner interpreter / liaison HITL (not required to be uniformed).",
        footer_right=foot_low,
        use_case=(
            "Produce partner-language versions of staff-approved English products derived entirely "
            "from PAI, for coalition sharing with interpreter oversight."
        ),
        task="After staff HITL approves the English RAW/PRETTY bundle, translate approved spans to target languages using API or LLM; preserve citations and structure; queue for partner interpreter confirmation.",
        stakeholders=[
            ("Upstream", "Products Agent (low-side) + staff HITL approval record"),
            ("Human", "Partner interpreter or liaison — confirms nuance and suitability (may be civilian)"),
            ("Consumer", "Partner-facing channels after interpreter gate"),
        ],
        ins=[
            "Staff-HITL-approved English text scope + target language list (PAI-derived only)",
            "Optional glossary stub for regional / military terms",
        ],
        outs=[
            (
                "Releasable + translated GEOINT Summary, OSINT Summary, Intelligence Summary, "
                "INTSUMs, SIGACTs, and targeting packets (partner interpreter–gated)"
            ),
            "Translation log (model/API version)",
        ],
        allow=[
            "Translation API or LLM on approved PAI text only",
        ],
        may_do=[
            "Flag low-confidence spans for interpreter review",
        ],
        deny=[
            "Translating pre–staff-HITL drafts",
            "Adding facts beyond approved English source",
            "Claiming classified sourcing (PAI only)",
        ],
        autonomous=[
            "Translate within orchestrator-approved span after staff HITL token present",
        ],
        gated=[
            HITL_PARTNER_INTERPRETER_LOW,
            "No partner handoff until interpreter confirmation recorded",
        ],
        policies=[
            ("PAI ONLY", "Source material must trace to PAI observations in this run"),
            ("FIDELITY", "No expansion of meaning; [AMBIG] on uncertain lines"),
        ],
        memory_lines=[
            ("Session", "Source hash, staff HITL id, target locale, glossary version"),
        ],
        failures=[
            "Entity or acronym untranslatable without context",
        ],
        escalations=[
            "Return partial translation + confidence map for interpreter",
        ],
        success=[
            ("Gated", "No run without staff HITL token; no release without interpreter ack"),
            ("Structure", "Sections map 1:1 to approved English bundle"),
        ],
    )

    # --- Green side ---
    write(
        "green",
        "AgentCanvas_GEOINT_G.html",
        title="Agent Canvas — GEOINT Collection (green-side)",
        subtitle="GEOINT Collection Agent — green-side instance: public or simulated enclave-safe layers with classification markings on derived artifacts.",
        footer_right=foot_green,
        use_case="Support green-side fusion with geospatial context consistent with marking rules applied throughout the VANTAGE-style pipeline.",
        task="Same core geospatial functions as low-side, but tag outputs with green marking placeholders and respect green allowlists (simulated).",
        stakeholders=[
            ("Downstream", "Green Fusion Agent"),
            ("Human", HITL_GATE),
        ],
        ins=[
            "Green-side AOI profile and cleared layer list (simulated)",
            "Optional handoff package from low-side (structured, sanitized stub)",
        ],
        outs=[
            "GEOINT Summary — structured geospatial findings with marking fields populated",
            "Audit log of layer access for this run",
        ],
        allow=[
            "Public or stubbed GIS calls approved for green prototype",
        ],
        may_do=[
            "Attach 'with classification markings' metadata per system policy stub",
        ],
        deny=[
            "Real SECRET network access in course prototype",
        ],
        autonomous=[
            "Produce marked geo context for Fusion",
        ],
        gated=[
            "Tearline and release decisions after Products + HITL",
        ],
        policies=[
            ("MARK", "All outputs carry marking block per green profile"),
        ],
        memory_lines=[
            ("Session", "Run-scoped geo batch and marking profile id"),
            ("Context", "SCG stub version reference if applicable"),
        ],
        failures=[
            "Marking profile mismatch vs. layer sensitivity (simulated)",
        ],
        escalations=[
            "Stop and flag for SECMAN if marking cannot be assigned",
        ],
        success=[
            ("Marked outputs", "100% geo rows include marking metadata"),
            ("Trace", "Layer ids and times recorded"),
        ],
    )

    write(
        "green",
        "AgentCanvas_GreenInt_G.html",
        title="Agent Canvas — Green INT Collection (green-side)",
        subtitle="Green INT Collection Agent — simulated higher-side structured intelligence feed entering the green fusion path (not real classified data).",
        footer_right=foot_green,
        use_case="Represent additional organic inputs available on the green path so Fusion can exercise richer correlation than PAI-only low-side.",
        task="Ingest stubbed or sanitized 'green' reports (JSON fixtures), normalize to Observation schema with green marking fields, hand to Fusion.",
        stakeholders=[
            ("Downstream", "Green Fusion Agent"),
            ("Human", HITL_GATE),
        ],
        ins=[
            "Fixture files or approved internal stub API (course-safe)",
            "Marking profile for incoming records",
        ],
        outs=[
            "Green INT Summary — structured findings with classification placeholders",
            "Ingestion audit trail",
        ],
        allow=[
            "Read from local fixture store or mock API only",
        ],
        may_do=[
            "Annotate reliability and handling caveats per stub policy",
        ],
        deny=[
            "Live classified databases",
        ],
        autonomous=[
            "Normalize and release to Fusion when schema valid",
        ],
        gated=[
            HITL_GATE,
        ],
        policies=[
            ("SIMULATED", "Clearly label synthetic or scrubbed content in metadata"),
        ],
        memory_lines=[
            ("Session", "Batch cursor and last-ingested fixture ids"),
        ],
        failures=[
            "Schema drift in fixtures",
        ],
        escalations=[
            "Halt batch on unexpected fields; log for developer",
        ],
        success=[
            ("Validity", "All outputs validate against green Observation schema"),
            ("Labeling", "Handling labels present on every record"),
        ],
    )

    write(
        "green",
        "AgentCanvas_Fusion_G.html",
        title="Agent Canvas — Fusion (green-side)",
        subtitle="Green Fusion Agent — correlates GEOINT + Green INT; participates in Fusion ↔ SECMAN ↔ Products with marking-aware artifacts.",
        footer_right=foot_green,
        use_case="Produce a fused operational picture on the green path with markings carried forward for SECMAN and tearline review.",
        task="Merge streams, preserve classification fields, escalate conflicts to SECMAN annotations; iterate until Products can render review-ready marked draft.",
        stakeholders=[
            ("Upstream", "Green GEOINT and Green INT collectors"),
            ("Peer", "Green SECMAN and Products"),
        ],
        ins=[
            "Marked observations from Green INT",
            "Marked GeoFeatures from green GEOINT",
            "Revision notes from SECMAN/Products",
        ],
        outs=[
            "Intelligence Summary — versioned structured fusion report with marking section",
            "Conflict register with handling suggestions (non-binding)",
        ],
        allow=[
            "Read/write green fusion workspace; LLM assist under schema lock",
        ],
        may_do=[
            "Propose tearline candidates (must be validated by SECMAN/HITL)",
        ],
        deny=[
            "Stripping classification placeholders",
        ],
        autonomous=[
            "Fuse, version, and loop with peers per orchestrator",
        ],
        gated=[
            "External release only via HITL after tearline review",
        ],
        policies=[
            ("MARKINGS", "Downstream packages must remain marking-consistent"),
        ],
        memory_lines=[
            ("Session", "Fusion graph versions and marking profile"),
        ],
        failures=[
            "Marking conflict between sources",
        ],
        escalations=[
            "SECMAN must adjudicate before Products proceeds",
        ],
        success=[
            ("Consistency", "Markings consistent across fused narrative"),
            ("Trace", "Sources and fixture ids preserved"),
        ],
    )

    write(
        "green",
        "AgentCanvas_SECMAN_G.html",
        title="Agent Canvas — SECMAN (green-side)",
        subtitle="Security Management Agent — green-side: SCG-informed rules, classification markings on all stages, blocks forward if tearline/policy checks fail.",
        footer_right=foot_green,
        use_case="Operationalize SCG-style guidance in prototype: ensure Products receive only marking-valid, release-ready structure for HITL tearline review.",
        task="Consume SCG stub + Intelligence Summary; apply marking rules; inject required caveats; coordinate with Fusion/Products for fixes.",
        stakeholders=[
            ("Upstream", "Green Fusion"),
            ("Peer", "Green Products"),
            ("Human", "HITL tearline and release authority"),
        ],
        ins=[
            "Intelligence Summary + conflict register",
            "SCG stub (ruleset id, handling phrases)",
        ],
        outs=[
            "Tagged INTSUM — SECMAN-approved draft with full marking block",
            "Explicit blockers OR proceed token for Products",
        ],
        allow=[
            "Rule engine, SCG lookup table, LLM explanation of rule hits",
        ],
        may_do=[
            "Suggest tearline placement (human approves)",
        ],
        deny=[
            "Final release authorization",
        ],
        autonomous=[
            "Enforce checks and annotate failures",
        ],
        gated=[
            "Tearline and language path decided by HITL after Products",
        ],
        policies=[
            ("SCG", "No forward progress on SCG violations (simulated)"),
        ],
        memory_lines=[
            ("Session", "Per-version checklist; SCG version used"),
        ],
        failures=[
            "Ambiguous SCG clause vs. content",
        ],
        escalations=[
            "Block with human-readable question list for reviewer",
        ],
        success=[
            ("SCG trace", "Each marking tied to rule or explicit exception flag"),
            ("Zero bypass", "Products cannot start without token when rules require"),
        ],
    )

    write(
        "green",
        "AgentCanvas_Products_G.html",
        title="Agent Canvas — Products (green-side)",
        subtitle="Product Producer Agent — green-side: formats cleared fusion for higher dissemination paths and tearline review; English vs. translation branch after HITL.",
        footer_right=foot_green,
        use_case="Produce staff-ready green products that preserve markings and prepare optional partner language outputs only after human tearline approval.",
        task=(
            "Render marked summary suitable for higher routing; prepare structured handoff for HITL "
            "tearline; if approved non-English, invoke Translation (green)."
        ),
        stakeholders=[
            ("Upstream", "Green SECMAN"),
            ("Downstream", "Translation (green) (conditional), HITL reviewer"),
        ],
        ins=[
            "SECMAN-approved marked draft",
            "Product template for green audience",
        ],
        outs=[
            "INTSUM, SIGACTs, targeting packets; review-ready product with tearline metadata",
            (
                "Releasable + translated GEOINT Summary, Green INT Summary, Intelligence Summary, "
                "INTSUMs, SIGACTs, and targeting packets via Translation (green) when HITL-routed"
            ),
        ],
        allow=[
            "Template rendering with marking banners",
            "LLM formatting constrained to provided facts",
        ],
        may_do=[
            "Package bilingual metadata for Translation input",
        ],
        deny=[
            "Calling Translation (green) before HITL approval for non-English",
            "Auto-posting to partner channels",
        ],
        autonomous=[
            "Assemble product package for HITL",
        ],
        gated=[
            "HITL tearline review mandatory before external or partner release",
        ],
        policies=[
            ("TEARLINE", "Clearly separate releasable body vs. higher portions (simulated)"),
        ],
        memory_lines=[
            ("Session", "Render versions and HITL decision placeholders"),
        ],
        failures=[
            "Template cannot represent marking layout",
        ],
        escalations=[
            "Request SECMAN clarification on marking placement",
        ],
        success=[
            ("HITL-ready", "Tearline checklist fields populated"),
            ("Branching", "English-only vs. Translation path correctly flagged"),
        ],
    )

    write(
        "green",
        "AgentCanvas_Translation_G.html",
        title="Agent Canvas — Translation (green-side)",
        subtitle="Translation Agent — converts HITL-approved product text to partner languages; runs only after tearline gate.",
        footer_right=foot_green,
        use_case="Support coalition and partner engagement with accurate, governed translations of releasable content.",
        task="Take approved English (or source language) tearline-safe text; produce target-language product using translation API or LLM; preserve structure and marking banners where applicable.",
        stakeholders=[
            ("Upstream", "Green Products + HITL approval record"),
            ("Consumer", "Partner-facing staff after human release"),
        ],
        ins=[
            "HITL-approved text scope + target language list",
            "Glossary stub for military/geo terms (optional)",
        ],
        outs=[
            (
                "Releasable + translated GEOINT Summary, Green INT Summary, Intelligence Summary, "
                "INTSUMs, SIGACTs, and targeting packets (tearline-gated)"
            ),
            "Translation log (model/api version)",
        ],
        allow=[
            "Translation API or LLM translate action on approved text only",
        ],
        may_do=[
            "Flag low-confidence segments for human linguist",
        ],
        deny=[
            "Translating pre-HITL drafts",
            "Expanding content beyond source meaning",
        ],
        autonomous=[
            "Translate within approved span",
        ],
        gated=[
            "Invocation only after HITL tearline approval captured in orchestrator",
        ],
        policies=[
            ("FIDELITY", "No added facts; ambiguous lines carry [AMBIG] tag"),
        ],
        memory_lines=[
            ("Session", "Source hash, target locale, glossary version"),
        ],
        failures=[
            "Untranslatable named entities or acronym collisions",
        ],
        escalations=[
            "Stop and return partial with confidence scores",
        ],
        success=[
            ("Gated", "No run without HITL approval token in payload"),
            ("Quality", "Structural parity with source sections"),
        ],
    )

    print("Done.")


if __name__ == "__main__":
    main()
