# Autonomous Defense Magazine Generator (`mag-gen`)

[![CI Pipeline](https://github.com/yashagarwal-lab/automated-defense-magazine-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/yashagarwal-lab/automated-defense-magazine-generator/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Page Budget](https://img.shields.io/badge/page%20budget-50%20pages%20A4-success.svg)](#page-budget-model)
[![DOM Overflow](https://img.shields.io/badge/DOM%20overflow-0mm%20clipping-brightgreen.svg)](#automated-layout-fitting)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An autonomous multi-stage intelligence curation, typesetting, and publishing system that synthesizes verified defense open-source intelligence (OSINT) into a publication-grade, **50-page print-ready A4 magazine** and an **interactive dual-spread digital web reader**.

---

## ⚡ Overview & Key Capabilities

- **Strict Mathematical Page Budgeting & Variable Lengths:** Rigidly constrains publication geometry to arbitrary page counts (e.g., 24, 32, 50, 64 pages) using an exact constraint solver that balances Front Matter, Section Openers, Content Pages, Dynamic Appendices, and Back Matter with zero page drift.
- **Zero-Clipping Autonomous Typesetting:** Dynamically fits article summaries using a headless Chromium DOM feedback loop, guaranteeing **0mm text clipping** and zero whitespace starvation across all physical pages.
- **Extensible Layout Registry:** 5 modular layout archetypes (`lead`, `pair`, `trio`, `quad`, `photo_essay`) registered dynamically and matched to article density, visual hierarchy, and photo availability.
- **Pluggable Multi-Source Ingestion:** Decoupled ingestion architecture supporting raw JSON archives, Markdown documents with YAML frontmatter, and RSS 2.0 / Atom XML syndicated feeds.
- **Modular Theme System:** Switchable CSS3 design token palettes (`army_gold`, `navy_blue`, `airforce_slate`, `editorial_mono`) supporting distinct service branches and publication contexts.
- **Declarative YAML/JSON Configuration:** Clean specifications for publication metadata, section definitions, thematic preferences, and target page counts (`configs/securing_the_northeast_50p.yaml`, `configs/briefing_24p.yaml`).
- **Dual-Target Output:**
  - **Vector Print PDF:** High-resolution 300-DPI-equivalent A4 document with microtypography, drop-caps, two-column editorial flow, and clickable source citations.
  - **Interactive Digital Reader:** Responsive dark-mode flipbook viewer featuring dual-page spread navigation, keyboard shortcuts, off-canvas Table of Contents drawer, and 1-click PDF download.
- **Unified Click CLI:** Single entrypoint (`mag-gen`) orchestrating ingestion, planning, curation, layout fitting, overflow auditing, PDF compilation, and local preview serving.

---

## 🏗️ Architecture & Pipeline Lifecycle

The compilation pipeline operates across modular, decoupled stages:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  1. Ingestion    │ ──> │  2. Curation     │ ──> │  3. Synthesis    │
│  JSON / MD / RSS │     │  Temporal Window │     │  Text Hygiene &  │
│  Auto-Detection  │     │  & 4-Taxonomy    │     │  Overrides Dict  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                            │
                                                            ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  6. Dual Output  │ <── │  5. DOM Fitting  │ <── │  4. Layout Plan  │
│  - Vector PDF    │     │  Playwright Loop │     │  Auto-Budgeter   │
│  - Web Flipbook  │     │  0mm Overflow    │     │  Layout Registry │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

1. **Ingestion (`ingestion/`):** Pluggable ingestors parse heterogeneous OSINT sources (JSON, Markdown + YAML frontmatter, RSS/Atom feeds) into normalized article models.
2. **Curatorial Filtering (`curation/`):** Enforces hard temporal boundaries (`2026-09-01` to `2026-10-03`) and allocates articles across strategic defense domains.
3. **Editorial Synthesis (`synthesis/`):** Removes news artifacts and boilerplate, normalizes sentence boundaries, and applies editorial overrides.
4. **Layout Planning & Budgeting (`layout/`):** Dynamic auto-budgeter calculates exact page quotas for any target page count (24, 32, 50, 64 pp), selects layout archetypes via the registry, and dynamically chunks multi-page appendices.
5. **DOM Auto-Fitting Feedback Loop (`layout/`):** Uses headless Chromium to iteratively expand article sentences until pages reach optimal density without triggering overflow.
6. **Publication Compilation (`rendering/`):** Injects selected themes, compiles print-ready vector PDF via Chromium Skia, and renders the interactive web flipbook.

Detailed specifications are documented in:
- [System Design & C4 Architecture](docs/SYSTEM_DESIGN.md)
- [Mathematical Page Budgeting Model](docs/PAGE_BUDGETING.md)
- [Editorial Taxonomy & Curation Rules](docs/EDITORIAL_TAXONOMY.md)

---

## 🎨 Modular Theme System

The design system supports switchable service themes via CSS3 custom properties:

| Theme | Identifier | Primary Accent | Secondary | Best Suited For |
|---|---|---|---|---|
| **Army Gold** (Default) | `army_gold` | Deep Olive (`#1c281a`) | Gold / Amber (`#c5a059`) | Ground forces, army theater reviews, general defense |
| **Navy Blue** | `navy_blue` | Maritime Blue (`#0f233a`) | Signal Blue (`#3b82f6`) | Naval doctrine, maritime domain awareness, carrier ops |
| **Air Force Slate** | `airforce_slate` | Slate Charcoal (`#1a202c`)| Aero Cyan (`#0ea5e9`) | Air dominance, aerospace technology, radar networks |
| **Editorial Mono** | `editorial_mono` | True Black (`#0a0a0a`) | Crimson Line (`#991b1b`) | Formal strategic whitepapers, unclassified debriefs |

Specify themes using the `--theme` flag or inside declarative publication YAML configs.

---

## 📐 Layout Archetypes Registry

The layout registry (`src/magazine_generator/layout/registry.py`) provides 5 distinct archetypes:

- **`lead` (2 articles):** 1 hero feature article with prominent photography and deep text analysis + 1 secondary supporting dispatch.
- **`pair` (2 articles):** Balanced dual-column split for two articles of equal strategic weight.
- **`trio` (3 articles):** 1 horizontal top-half banner feature + 2 side-by-side bottom-half analytical cards.
- **`quad` (4 articles):** High-density 2×2 grid of concise intelligence bulletins.
- **`photo_essay` (1 hero article):** Full-bleed photography accompanied by comprehensive, long-form narrative commentary.

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.12 or newer
- Git & Git LFS (for high-resolution asset tracking)

### Setup

```bash
# Clone the repository
git clone https://github.com/yashagarwal-lab/automated-defense-magazine-generator.git
cd automated-defense-magazine-generator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package and dependencies
pip install -e .

# Install Playwright Chromium headless engine
playwright install --with-deps chromium
```

---

## 💻 CLI Usage (`mag-gen`)

The `mag-gen` CLI orchestrates every stage of the publishing pipeline:

```bash
# Preview page budgeting matrix for any arbitrary page count
mag-gen plan --pages 32
mag-gen plan --pages 50 --config configs/securing_the_northeast_50p.yaml

# Ingest articles from external sources (JSON, Markdown, or RSS feeds)
mag-gen ingest --source data/raw_feed.json --type json
mag-gen ingest --source "content/briefs/*.md" --type markdown
mag-gen ingest --source https://example.com/defense-feed.xml --type rss

# Render print A4 HTML magazine (supports custom configs, themes, and page targets)
mag-gen render --config configs/briefing_24p.yaml --theme navy_blue --pages 24
mag-gen render --theme airforce_slate

# Run sentence-by-sentence DOM auto-fitting loop
mag-gen fit

# Audit all pages for DOM overflow or text clipping
mag-gen check

# Compile publication-grade print PDF
mag-gen pdf --config configs/securing_the_northeast_50p.yaml --theme army_gold

# Render interactive digital flipbook reader
mag-gen reader --theme navy_blue

# Run complete end-to-end pipeline (fit -> render -> check -> pdf -> reader)
mag-gen all --config configs/securing_the_northeast_50p.yaml --theme army_gold

# Launch interactive web reader preview server (default http://127.0.0.1:8000)
mag-gen serve
```

---

## 📊 Variable Page Budget Models

The auto-budgeter mathematically balances any publication length:

| Target | Front Matter | Sections ($N_S=4$) | Appendices | Back | Total Articles Accommodated |
|---|---|---|---|---|---|
| **24 Pages** | 4 pp | 16 pp (4 openers + 12 content) | 3 pp (1 src + 2 rationale) | 1 p | 24–28 articles |
| **32 Pages** | 4 pp | 24 pp (4 openers + 20 content) | 3 pp (1 src + 2 rationale) | 1 p | 40–46 articles |
| **50 Pages** | 4 pp | 41 pp (4 openers + 37 content) | 4 pp (1 src + 3 rationale) | 1 p | 74 articles (Standard Edition) |
| **64 Pages** | 4 pp | 54 pp (4 openers + 50 content) | 5 pp (1 src + 4 rationale) | 1 p | 100–108 articles |

---

## 🧪 Testing & Verification

Run the automated test suite with pytest:

```bash
pytest tests/ -v
```

The test suite validates:
- **Dynamic Auto-Budgeter:** Exact mathematical page conservation across 24, 32, 50, and 64 page configurations; appendix chunking.
- **Layout Registry:** Layout archetype registration, selection heuristics, and capacity calculations.
- **Pluggable Ingestion:** Parsing for JSON, Markdown (frontmatter), and RSS/Atom feeds with factory auto-detection.
- **Text Cleaner:** Sentence tokenization, boilerplate removal, quote handling, and control character elimination.
- **Curation & Taxonomy:** Four-domain categorization, keyword filtering, and temporal window enforcement.
- **Layout Planner:** Invariant verification of physical page sequences, TOC target resolutions, and article budgeting.

---

## 📂 Repository Layout

```
├── .github/workflows/ci.yml       # GitHub Actions CI workflow
├── configs/                       # Declarative publication specifications
│   ├── briefing_24p.yaml          # 24-page tactical briefing config
│   └── securing_the_northeast_50p.yaml # 50-page flagship publication config
├── data/                          # Magazine configuration and curated article datasets
│   ├── articles.json              # 74 curated articles with summaries and metadata
│   ├── images.json                # Curated image registry
│   ├── magazine.json              # Section outlines, masthead, and colophon data
│   └── pool.json                  # Full raw OSINT article body pool
├── docs/                          # Formal technical documentation
│   ├── EDITORIAL_TAXONOMY.md      # Taxonomy, keywords, and curation policy
│   ├── PAGE_BUDGETING.md          # Variable length math and column geometry
│   └── SYSTEM_DESIGN.md           # System design, C4 diagrams, and modular subsystems
├── output/                        # Compiled artifacts
│   ├── index.html                 # Print layout HTML
│   ├── reader.html                # Interactive digital web reader
│   └── Securing_the_Northeast...  # Vector print PDF
├── src/magazine_generator/        # Core modular Python package
│   ├── cli.py                     # Unified Click CLI (plan, ingest, render, pdf, reader, all)
│   ├── config.py                  # Publication parameters and path configs
│   ├── curation/                  # Filtering, taxonomy, and allocation
│   ├── ingestion/                 # Pluggable ingestion (JSON, Markdown, RSS/Atom)
│   ├── layout/                    # Auto-budgeter, layout registry, planner, DOM fitter
│   ├── models/                    # Typed data structures
│   ├── reader/                    # Web reader server and request handler
│   ├── rendering/                 # Jinja2 rendering engine and PDF exporter
│   └── synthesis/                 # Cleaner, summarizer, and editorial overrides
├── static/                        # CSS stylesheets, themes, JavaScript, and 201 photographs
│   ├── css/
│   │   ├── layouts.css            # Grid layouts for all 5 archetypes
│   │   ├── styles.css             # Print CSS with @page rules
│   │   └── themes/                # Army Gold, Navy Blue, Airforce Slate, Editorial Mono
│   ├── js/reader.js               # Interactive digital reader script
│   └── images/                    # High-resolution defense OSINT imagery
├── templates/                     # Modular Jinja2 template components
│   ├── components/macros.html.j2  # Lead, Pair, Trio, Quad, Photo-Essay macros
│   ├── print/magazine.html.j2     # Print publication master template
│   └── reader/web_reader.html.j2  # Interactive web reader master template
├── tests/                         # Comprehensive unit test suite (21 tests)
├── pyproject.toml                 # Package definition & console script entrypoint
└── requirements.txt               # Dependencies
```

---

## 📜 License

Licensed under the [MIT License](LICENSE).
