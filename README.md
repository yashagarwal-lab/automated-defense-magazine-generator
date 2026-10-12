# Autonomous Defense Magazine Generator (`mag-gen`)

[![CI Pipeline](https://github.com/yashagarwal-lab/automated-defense-magazine-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/yashagarwal-lab/automated-defense-magazine-generator/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Page Budget](https://img.shields.io/badge/page%20budget-50%20pages%20A4-success.svg)](#page-budget-model)
[![DOM Overflow](https://img.shields.io/badge/DOM%20overflow-0mm%20clipping-brightgreen.svg)](#automated-layout-fitting)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An autonomous multi-stage intelligence curation, typesetting, and publishing system that synthesizes verified defense open-source intelligence (OSINT) into a publication-grade, **50-page print-ready A4 magazine** and an **interactive dual-spread digital web reader**.

---

## ⚡ Overview & Key Capabilities

- **Zero-Clipping Autonomous Typesetting:** Dynamically fits article summaries using a headless Chromium DOM feedback loop, guaranteeing **0mm text clipping** and zero whitespace starvation across all 50 physical pages.
- **Strict Mathematical Page Budgeting:** Rigidly constrains publication geometry to exactly 50 A4 portrait pages (1 Cover + 1 TOC + 2 Editorial/Primer + 4 Openers + 37 Content Pages + 4 Appendices + 1 Back Cover).
- **Dual-Target Output:**
  - **Vector Print PDF:** High-resolution 300-DPI-equivalent A4 document with microtypography, drop-caps, two-column editorial flow, and clickable source citations.
  - **Interactive Digital Reader:** Responsive dark-mode flipbook viewer featuring dual-page spread navigation, keyboard shortcuts, off-canvas Table of Contents drawer, and 1-click PDF download.
- **Unified Click CLI:** Single entrypoint (`mag-gen`) orchestrating curation, layout fitting, overflow auditing, PDF compilation, and local preview serving.
- **Pure Python & Vanilla Web Stack:** Decoupled architecture with zero framework bloat, leveraging Jinja2, Playwright Chromium, CSS3 custom properties, and vanilla ES6.

---

## 🏗️ Architecture & Pipeline Lifecycle

The compilation pipeline operates across six decoupled stages:

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  1. Ingestion    │ ──> │  2. Curation     │ ──> │  3. Synthesis    │
│  OSINT Pool &    │     │  Temporal Window │     │  Text Hygiene &  │
│  Articles Normal.│     │  & 4-Taxonomy    │     │  Overrides Dict  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                            │
                                                            ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  6. Dual Output  │ <── │  5. DOM Fitting  │ <── │  4. Layout Plan  │
│  - Vector PDF    │     │  Playwright Loop │     │  50-Page Budget  │
│  - Web Flipbook  │     │  0mm Overflow    │     │  Grid Geometry   │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

1. **Ingestion & Normalization:** Ingests raw news wires, extracts high-resolution photographs, and normalizes publication metadata.
2. **Curatorial Filtering:** Enforces hard temporal boundaries (`2026-09-01` to `2026-10-03`) and filters articles across four strategic domains.
3. **Editorial Synthesis:** Removes news artifacts and boilerplate, normalizes sentence boundaries, and injects explicit curated editorial overrides.
4. **Layout Planning:** Assembles the 50-page sequence, computes dynamic TOC folio references, and chunks appendix tables.
5. **DOM Auto-Fitting Feedback Loop:** Uses headless Chromium to iteratively expand article sentences until pages reach optimal density without triggering overflow.
6. **Publication Compilation:** Generates print-ready vector PDF via Chromium Skia and renders the interactive web flipbook.

Detailed specifications are documented in:
- [System Design & C4 Architecture](docs/SYSTEM_DESIGN.md)
- [Editorial Taxonomy & Curation Rules](docs/EDITORIAL_TAXONOMY.md)
- [Mathematical Page Budgeting Model](docs/PAGE_BUDGETING.md)

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

The `mag-gen` CLI provides dedicated commands for each stage of the publishing pipeline:

```bash
# Run the complete end-to-end pipeline (fit -> render -> check -> pdf -> reader)
mag-gen all

# Run sentence-by-sentence DOM auto-fitting loop
mag-gen fit

# Audit all 50 pages for DOM overflow or text clipping
mag-gen check

# Render print A4 HTML magazine
mag-gen render

# Compile publication-grade 50-page print PDF
mag-gen pdf

# Render interactive digital flipbook reader
mag-gen reader

# Launch interactive web reader preview server (default http://127.0.0.1:8000)
mag-gen serve
```

---

## 📊 Page Budget Model

| Section / Spread | Page Range | Type / Format | Content |
|---|---|---|---|
| **Front Matter** | pp. 1–4 | `cover`, `contents`, `editor`, `overview` | Masthead, TOC, Editor's Note, Theater Primer |
| **Section 01** | pp. 5–16 | 1 Opener + 11 Content Pages | Security & Strategic Affairs (22 articles) |
| **Section 02** | pp. 17–27 | 1 Opener + 10 Content Pages | Border Infrastructure & Readiness (20 articles) |
| **Section 03** | pp. 28–36 | 1 Opener + 8 Content Pages | Regional Geopolitics & External Dynamics (16 articles) |
| **Section 04** | pp. 37–45 | 1 Opener + 8 Content Pages | Civil-Military Relations & Community Outreach (16 articles) |
| **Appendix 1** | p. 46 | `appendix-src` | Source Publications & Volume Breakdown |
| **Appendix 2** | pp. 47–49 | `appendix-rat` (3 sheets: 23, 25, 26 rows) | Editorial Rationale for all 74 selected stories |
| **Back Cover** | p. 50 | `back` | Closing quote, citation, and official insignia |
| **Total** | **50 Pages** | **ISO 216 A4 Portrait** | **100% Zero DOM Overflow** |

---

## 🧪 Testing & Verification

Run the automated test suite with pytest:

```bash
pytest tests/ -v
```

The test suite validates:
- **Text Cleaner:** Sentence tokenization, boilerplate removal, quote handling, and control character elimination.
- **Curation & Taxonomy:** Four-domain categorization, keyword filtering, and temporal window enforcement.
- **Layout Planner:** Invariant verification of exactly 50 physical pages, TOC target resolutions, and article budgeting.

---

## 📂 Repository Layout

```
├── .github/workflows/ci.yml       # GitHub Actions CI workflow
├── data/                          # Magazine configuration and curated article datasets
│   ├── articles.json              # 74 curated articles with summaries and metadata
│   ├── images.json                # Curated image registry
│   ├── magazine.json              # Section outlines, masthead, and colophon data
│   └── pool.json                  # Full raw OSINT article body pool
├── docs/                          # Formal technical documentation
│   ├── EDITORIAL_TAXONOMY.md      # Taxonomy, keywords, and curation policy
│   ├── PAGE_BUDGETING.md          # 50-page layout math and column geometry
│   └── SYSTEM_DESIGN.md           # System design, C4 diagrams, and state machine
├── output/                        # Compiled artifacts
│   ├── index.html                 # 50-page print layout HTML
│   ├── reader.html                # Interactive digital web reader
│   └── Securing_the_Northeast...  # 50-page vector print PDF
├── src/magazine_generator/        # Core modular Python package
│   ├── cli.py                     # Unified Click command-line interface
│   ├── config.py                  # Publication parameters and path configs
│   ├── curation/                  # Filtering and taxonomy categorization
│   ├── layout/                    # Page planner and Playwright DOM fitter
│   ├── models/                    # Typed data structures
│   ├── reader/                    # Web reader server and request handler
│   ├── rendering/                 # Jinja2 rendering engine and PDF exporter
│   └── synthesis/                 # Cleaner, summarizer, and editorial overrides
├── static/                        # CSS stylesheets, JavaScript, and 201 photographs
├── templates/                     # Modular Jinja2 template components
│   ├── components/macros.html.j2  # Shared page-rendering macros
│   ├── print/magazine.html.j2     # Print publication master template
│   └── reader/web_reader.html.j2  # Interactive web reader master template
├── tests/                         # Comprehensive unit test suite
├── pyproject.toml                 # Modern package definition & console script
└── requirements.txt               # Dependencies
```

---

## 📜 License

Licensed under the [MIT License](LICENSE).
