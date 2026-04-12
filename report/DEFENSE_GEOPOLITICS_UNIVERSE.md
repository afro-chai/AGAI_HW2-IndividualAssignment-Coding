# Defense, geopolitics, and energy-security equity universe

**Purpose:** Posterity and selection pool for StockTrader (HW2). Names below are **investable or tradeable equities** where noted; some entities in your original notes are **private or state-linked** and are listed only under *Non-investable reference* for analytic context (AFRICOM / hybrid warfare lens).

**Disclaimer:** Educational framing for a course assignment—not investment advice, not an endorsement of any security.

---

## How this document is organized

| Section | Contents |
|--------|-----------|
| **1. Global — by field** | AI / platforms, chips, defense primes, gov-tech, big tech cloud, cyber, shipping, LNG, uranium, copper & miners, oil supermajors |
| **2. Regional — AFRICOM & related** | Africa / MENA footprint: oil majors, mining in conflict-adjacent jurisdictions, cyber |
| **3. Default five tickers (this repo)** | The symbols wired into `src/main.py` as `DEFAULT_TICKERS` (minimizes Alpha Vantage calls) |
| **4. Non-investable / reference-only** | Private cos., state actors, ADR caveats |

Duplicates (e.g. NVDA, Shell, TotalEnergies appearing in multiple lists) appear **once** in the field tables, with cross-tags.

---

## 1. Global — by field

### 1.1 AI / data / platforms (defense & intel adjacency)

| Name | Ticker (when public) | Notes | Typical vol (1–5) |
|------|----------------------|--------|-------------------|
| Palantir Technologies | **PLTR** | DoD / NATO / intel analytics; Golden Dome / defense contract headlines | 5 |
| Anthropic | *(private)* | Claude family used in gov / enterprise; policy controversy risk | ~5 equiv. |

### 1.2 Chips & compute (AI + autonomy backbone)

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| NVIDIA | **NVDA** | GPUs for AI, autonomy, surveillance stacks | 5 |
| AMD | **AMD** | MI-series AI accelerators vs. NVDA | 5 |
| Intel | **INTC** | US fabs, CHIPS Act, defense supply chain | 4 |
| Taiwan Semiconductor | **TSM** | Leading-edge fab concentration; Taiwan strait geopolitics | 4 |

### 1.3 Defense primes (kinetic + aerospace)

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Lockheed Martin | **LMT** | F-35, missiles, hypersonics | 2 |
| RTX Corporation | **RTX** | Patriot, radar, missile demand | 2 |
| Northrop Grumman | **NOC** | Bombers, nuclear, space | 2 |
| General Dynamics | **GD** | Subs, land systems, IT | 2 |
| Boeing | **BA** | Defense aircraft + space; integration narratives | 4 |

### 1.4 Gov-tech / systems integrators

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| CACI International | **CACI** | Classified / cyber / C4ISR | 3 |
| Science Applications Intl. | **SAIC** | Gov IT integration | 2 |

### 1.5 Big tech — cloud & defense infrastructure

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Oracle | **ORCL** | Gov cloud / data estates | 3 |
| Amazon | **AMZN** | AWS GovCloud; defense AI plumbing | 3 |
| Microsoft | **MSFT** | Azure JWCC / DoD ecosystem | 3 |
| Alphabet | **GOOGL** | AI, analytics, Maven-era history | 3 |

### 1.6 Cybersecurity (state + criminal + hybrid)

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| CrowdStrike | **CRWD** | Endpoint + threat intel | 4 |
| Palo Alto Networks | **PANW** | Network / cloud security | 3 |
| Fortinet | **FTNT** | Gov + critical infrastructure | 4 |
| Check Point | **CHKP** | Strong Middle East threat context | 2 |
| Darktrace | **DARK** (listing varies) | AI anomaly detection | 4 |

### 1.7 Shipping & chokepoints (Hormuz, Red Sea, Suez)

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Frontline | **FRO** | Crude tankers; rate spikes on disruption | 5 |
| Euronav | **EURN** | Large crude carriers | 4 |
| Teekay Tankers | **TNK** | Mid-size tanker exposure | 5 |
| ZIM Integrated | **ZIM** | Containers; Israel / MENA headline beta | 5 |
| Maersk | **AMKBY** / listings vary | Global liner / logistics | 3 |

### 1.8 LNG & gas exporters

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Cheniere | **LNG** | US LNG export scale | 4 |
| Shell | **SHEL** | LNG + trading | 2 |
| TotalEnergies | **TTE** | LNG + MENA / Africa footprint | 2 |
| Equinor | **EQNR** | European gas / security-of-supply | 3 |
| QatarEnergy | *(state)* | Global LNG supply power | ~2 equiv. |

### 1.9 Uranium / naval nuclear (energy security)

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Cameco | **CCJ** | Western uranium producer | 4 |
| Kazatomprom | **KAP** (venue varies) | Kazakhstan supply chain | 4 |
| NexGen Energy | **NXE** | Canadian developer | 5 |
| Denison Mines | **DNN** | ISR / development | 5 |
| BWX Technologies | **BWXT** | Naval reactors | 3 |

### 1.10 Copper & critical minerals

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Freeport-McMoRan | **FCX** | Copper levered to electrification + defense supply chain | 4 |
| Rio Tinto | **RIO** | Diversified; copper / lithium exposure | 3 |
| BHP | **BHP** | Global mining; copper | 3 |
| Glencore | **GLEN** (UK) / **GLNCY** (ADR) | DRC cobalt / copper; resource competition | 4 |
| Ivanhoe Mines | **IVN** (venue varies) | DRC copper development | 5 |
| China Molybdenum | **CMCLF** / venue varies | DRC cobalt (EV + defense metals) | 4 |

### 1.11 Oil supermajors & upstream (global supply shock)

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Exxon Mobil | **XOM** | US supermajor; global / MENA exposure | 2 |
| Chevron | **CVX** | US supermajor | 2 |
| Shell | **SHEL** | Integrated; Nigeria / LNG | 2 |
| BP | **BP** | UK major; geopolitical whiplash beta | 3 |
| TotalEnergies | **TTE** | Africa + MENA + LNG | 2 |
| ConocoPhillips | **COP** | Upstream levered to crude | 3 |
| Occidental | **OXY** | Permian; headline crude beta | 4 |
| EOG Resources | **EOG** | Quality shale / pure oil beta | 4 |
| Equinor | **EQNR** | Norway / Europe supply story | 3 |
| Saudi Aramco | **2222.SR** (Tadawul) | Spare capacity / OPEC+; **broker access required** | 2 |

---

## 2. Regional — AFRICOM & related (oil, mining, cyber)

*Analytic lens: resources finance conflict; non-state actors attach to extractive corridors; state competition plays out via commercial proxies where investable.*

### 2.1 Oil (Africa + MENA overlap)

| Name | Ticker | AFRICOM / regional relevance | Vol |
|------|--------|-------------------------------|-----|
| TotalEnergies | **TTE** | Mozambique LNG, Sahel / MENA footprint | 2 — **VERY HIGH** |
| Eni | **E** | Libya, Egypt, West Africa | 2 — **VERY HIGH** |
| Shell | **SHEL** | Nigeria / Niger Delta instability | 2 — HIGH |
| Exxon Mobil | **XOM** | West Africa + Iraq exposure | 2 — HIGH |
| Chevron | **CVX** | Nigeria + offshore Africa | 2 — HIGH |

### 2.2 Mining (DRC / Sahel / conflict-adjacent gold & copper)

| Name | Ticker | Notes | Vol |
|------|--------|--------|-----|
| Glencore | **GLEN** / **GLNCY** | DRC cobalt + copper | 4 |
| Barrick Gold | **GOLD** | Mali, DRC, gold in conflict-adjacent states | 3 |
| Anglo American | **NGLOY** / venue varies | Platinum, diamonds, Africa footprint | 3 |
| China Molybdenum | **CMCLF** | DRC cobalt concentration | 4 |
| Ivanhoe Mines | **IVN** | DRC copper development | 5 |

**AFRICOM insight (summary):** DRC as cobalt choke point; gold linked to conflict financing narratives; PRC vs. West competition in critical minerals.

### 2.3 Cybersecurity (terror + hybrid overlap)

| Name | Ticker | AFRICOM / hybrid angle | Vol |
|------|--------|-------------------------|-----|
| CrowdStrike | **CRWD** | Nation-state + criminal tooling | 4 |
| Palo Alto Networks | **PANW** | Gov / cloud | 3 |
| Fortinet | **FTNT** | Gov + infrastructure | 4 |
| Check Point | **CHKP** | Middle East threat expertise | 2 |
| Darktrace | **DARK** | AI-driven anomaly detection | 4 |

### 2.4 Strategic / non-investable networks (environment only)

| Entity | Type | Why it matters (no ticker) |
|--------|------|----------------------------|
| Huawei | Private / state-linked | Telecom + data influence across Africa |
| Wagner-style networks | Proxy / irregular | Security-for-resources deals (historical framing) |
| IRGC / proxy ecosystem | State / irregular | Logistics + financing channels |
| CNPC | NOC | Africa + MENA oil |
| Baykar | Private | TB2 drone exports |
| QatarEnergy | NOC | LNG market power |

**Key point:** these shape the **operating environment** for oil, mining, cyber, and defense names above—they are **not** presented here as investable “terror stocks.”

---

## 3. Default five tickers (this repository)

These are **`DEFAULT_TICKERS`** in [`src/main.py`](../src/main.py) — **five** liquid U.S. listings for **sector diversity**, **mixed volatility**, and **at least one AFRICOM hook** (here: **TTE** integrated oil Africa–MENA, **GOLD** conflict-adjacent mining). The small basket keeps **Alpha Vantage usage to five `NEWS_SENTIMENT` calls per full run** (see [`docs/ALPHA_VANTAGE.md`](../docs/ALPHA_VANTAGE.md)).

| # | Ticker | Company | Sector bucket | Vol (guide) | Defense / geo hook |
|---|--------|---------|-----------------|------------|----------------------|
| 1 | **PLTR** | Palantir | AI / gov analytics | High | DoD / NATO software; defense contract headlines |
| 2 | **TTE** | TotalEnergies | Integrated oil / LNG | Low | **AFRICOM / MENA** footprint (Africa LNG, Sahel exposure) |
| 3 | **GOLD** | Barrick Gold | Mining | Medium | **AFRICOM:** Mali / DRC gold narratives |
| 4 | **LMT** | Lockheed Martin | Defense prime | Low | F-35, missiles, budget cycles |
| 5 | **FRO** | Frontline | Crude tankers | High | Hormuz / supply disruption → freight rates |

**Run command (reference):**

```powershell
python -m src.main --backtest --ticker-workers 2
```

---

## 4. Ticker hygiene (yfinance / venue)

- Default list (**PLTR**, **TTE**, **GOLD**, **LMT**, **FRO**) is chosen for straightforward `yfinance` use.
- **Saudi Aramco (2222)**, **Kazatomprom**, some **ADR/pink** names may need broker-specific symbols—keep them in this universe doc for research, not necessarily in `DEFAULT_TICKERS` without verification.

---

## 5. Changelog

- **2026-04 (latest):** Default basket reduced to **five** tickers (`PLTR`, `TTE`, `GOLD`, `LMT`, `FRO`) to **minimize Alpha Vantage daily usage** while keeping **AFRICOM** exposure (TTE, GOLD) and cross-sector spread.
- **2026-04:** Earlier revision used ten defense–geopolitics names; universe tables above remain the wider pick list.
