# System Design & Architecture Specification: Autonomous Defense Magazine Generator

## 1. Executive Summary

The **Autonomous Defense Magazine Generator** (`mag-gen`) is an automated digital and print publishing engine engineered to ingest, curate, synthesize, and typeset defense intelligence articles into a publication-grade, 50-page print-ready A4 document and an interactive web reader.

The system addresses the challenge of automated layout typesetting: dynamically balancing arbitrary lengths of prose across rigid physical paper constraints (210mm × 297mm) without human intervention, whitespace starvation, or text clipping.

```mermaid
graph TD
    A[Raw Intelligence Ingestion] --> B[Domain Curation & Filtering]
    B --> C[Synthesis & Editorial Attribution]
    C --> D[50-Page Layout Planning]
    D --> E[Headless DOM Feedback Fitting]
    E --> F[Dual Output Compilation]
    F --> G[Print A4 PDF Skia/Chromium Engine]
    F --> H[Interactive Dual-Spread Web Reader]
```

---

## 2. C4 Architecture Specification

### 2.1 C4 Level 1: System Context Diagram

```mermaid
C4Context
    title System Context Diagram - Automated Defense Publication Compiler

    Person(editor, "Defense Analyst / Editor", "Oversees intelligence curation, taxonomy rules, and triggers automated publication pipelines.")
    System(maggen, "Automated Magazine Generator (mag-gen)", "Compiles normalized OSINT feeds into publication-grade print PDFs and interactive digital readers.")
    System_Ext(osint, "OSINT News Crawlers / Wire Feeds", "Feeds raw military and regional intelligence articles.")
    System_Ext(chromium, "Headless Chromium Runtime", "Renders DOM layout trees, validates overflow metrics, and prints vector A4 PDFs.")
    Person(reader, "Command Staff / Policy Analyst", "Reads the 50-page briefing in high-resolution print or interactive digital reader.")

    Rel(editor, maggen, "Executes CLI commands (render, fit, check, pdf, reader, all)")
    Rel(osint, maggen, "Supplies pool of raw articles and metadata")
    Rel(maggen, chromium, "Executes DOM metrics evaluation and PDF printing")
    Rel(maggen, reader, "Delivers print PDF and interactive web reader")
```

---

### 2.2 C4 Level 2: Container Diagram

```mermaid
C4Container
    title Container Diagram - mag-gen Subsystems

    Container(cli, "CLI Interface", "Click Python 3.12+", "Provides unified command dispatcher (mag-gen).")
    Container(curation, "Curation Engine", "Python", "Enforces temporal windows (2026-09-01 to 2026-10-03) and 4-domain taxonomy classification.")
    Container(synthesis, "Synthesis Engine", "Python / Regex", "Applies text hygiene, editorial overrides, and length-bounded summarization.")
    Container(layout, "Layout Planner & DOM Fitter", "Python / Playwright", "Plans 50-page layout budgets and iteratively fits text using browser feedback.")
    Container(renderer, "Rendering Engine", "Jinja2 / CSS3", "Compiles component macros into print-ready and web-ready HTML documents.")
    Container(pdf, "PDF Compiler", "Playwright / Chromium Skia", "Generates vector print-accurate A4 PDF.")
    Container(web, "Digital Reader Engine", "Vanilla JS / CSS3 / HTTP Server", "Renders responsive dual-page flipbook with TOC drawer and keyboard navigation.")

    Rel(cli, curation, "Invokes filtering & selection")
    Rel(curation, synthesis, "Passes curated articles")
    Rel(synthesis, layout, "Provides candidate sentences")
    Rel(layout, renderer, "Supplies 50-page layout plan")
    Rel(renderer, pdf, "Feeds rendered print DOM")
    Rel(renderer, web, "Feeds rendered reader DOM")
```

---

### 2.3 C4 Level 3: Component Diagram (Layout & Fitting Engine)

```mermaid
C4Component
    title Component Diagram - Layout Planning & DOM Auto-Fitting Loop

    Component(planner, "Planner (planner.py)", "Assembles 50-page sequence, computes TOC page refs, chunks appendix tables.")
    Component(cleaner, "Cleaner (cleaner.py)", "Performs artifact stripping and unambiguous sentence tokenization.")
    Component(fitter, "DOM Fitter (fitter.py)", "Spawns headless Chromium, loads page DOM, and applies sentence-by-sentence expansion.")
    Component(check_js, "CHECK_JS Evaluator", "JavaScript inside Chromium", "Measures bounding rects and scrollHeight overflow down to 0.1mm.")
    Component(fit_js, "FIT_JS Evaluator", "JavaScript inside Chromium", "Iteratively increments sentence budget k until overflow condition trips, then backs off.")

    Rel(planner, fitter, "Passes initial page article mapping")
    Rel(cleaner, fitter, "Extracts clean candidate sentences")
    Rel(fitter, fit_js, "Dispatches candidate sentence plan")
    Rel(fit_js, check_js, "Verifies margin limits")
    Rel(fitter, planner, "Stores optimal sentence counts in articles.json")
```

---

## 3. Data Pipeline & Algorithmic State Machine

```mermaid
stateDiagram-v2
    [*] --> Ingested: Load pool.json & articles.json
    Ingested --> Curated: Filter dates (2026-09-01..2026-10-03) & taxonomy classification
    Curated --> Synthesized: Clean artifacts & inject explicit editorial overrides
    Synthesized --> Planned: Allocate 50 physical page budgets (1 Cover + 1 TOC + 2 Editorial + 4 Openers + 37 Content + 4 Appendix + 1 Back)
    Planned --> Fitted: Playwright evaluates DOM bounding boxes per page
    Fitted --> Verified: Zero-clipping audit (CHECK_JS worst delta <= 0mm)
    Verified --> PrintCompiled: Skia headless vector PDF export (595.92 x 842.88 pt)
    Verified --> ReaderCompiled: Interactive dual-spread reader HTML/JS compiled
    PrintCompiled --> [*]
    ReaderCompiled --> [*]
```

### 3.1 Sentence-by-Sentence DOM Fitting Algorithm

In traditional desktop publishing, text is either manually massaged or clipped by rigid frames. `mag-gen` uses a **browser-in-the-loop greedy expansion algorithm**:

1. **Candidate Sentence Extraction:**
   For every article slot on a page $P$, extract $S = [s_1, s_2, \dots, s_m]$ up to `MAX_WORDS = 220`.
2. **Initial Minimum Assignment:**
   Initialize each article $i$ with $k_i = 1$ sentence. Render page DOM.
3. **Iterative Greedy Growth:**
   Loop while progress can be made:
   - For each article $i$ in page $P$:
     * Increment $k_i \leftarrow k_i + 1$.
     * Replace DOM `<p>` element with joined sentences $s_1 \dots s_{k_i}$.
     * Audit DOM bounding boxes:
       $$\text{overflow}(P) = \exists e \in P : \text{bottom}(e) > \text{bottom}(\text{inner}) - \text{buffer} \quad \lor \quad \text{scrollHeight}(e) > \text{clientHeight}(e)$$
     * If $\text{overflow}(P) = \text{True}$:
       $$k_i \leftarrow k_i - 1; \quad \text{mark article } i \text{ as saturated}$$
     * Else:
       $$\text{progress} \leftarrow \text{True}$$
4. **Convergence:**
   The algorithm terminates when all articles on the page are saturated. This mathematically guarantees the maximum possible informative text density on each page with zero overflow.

---

## 4. Dual-Target Output Architecture

### 4.1 Print Publication Architecture (`index.html` → PDF)
- **Target Standard:** ISO 216 A4 Portrait ($210\text{mm} \times 297\text{mm}$).
- **Typography:**
  * Primary Display / Masthead: Cinzel serif (`font-weight: 800`).
  * Body Prose: Lora serif with proportional optical sizing and drop-caps (`cols-2`).
  * Captions, Folios & Metadata: Inter sans-serif.
- **Color Model:** Print-ready CSS tokens (`--ink: #111`, `--paper: #fdfdfc`, `--saffron: #c99738`, `--muted: #555`).
- **Rendering Pipeline:** Headless Playwright Chromium (`print_to_pdf`) with `print_background=True` and `@page { size: A4 portrait; margin: 0; }`.

### 4.2 Interactive Digital Reader (`reader.html`)
- **Viewport Layout:** Dark mode military operations center aesthetic (`--reader-bg: #0d1117`).
- **Modes:**
  * Dual-Page Spread View (`📖 Spread`): Side-by-side even/odd pages simulating physical magazine reading.
  * Single Page Focus View: Adaptive for smaller viewports and mobile devices.
- **Controls & Navigation:**
  * Off-canvas Table of Contents drawer with direct section jumps.
  * Folio counter (`Page X of 50`).
  * Keyboard navigation (`ArrowRight`, `ArrowLeft`, `PageUp`, `PageDown`, `Home`, `End`).
  * Fullscreen toggle (`⛶ Fullscreen`).
  * Direct 1-click download of the compiled print PDF.

---

## 5. Non-Functional Requirements & Verification Metrics

| Metric | Target | Verified Value | Validation Tool |
|---|---|---|---|
| **Total Page Budget** | Configurable (24, 32, 50, 64 pp) | 50 pages (default) | `pdfinfo`, Chromium DOM |
| **DOM Text Clipping** | 0 mm overflow | 0 mm (Pass) | `mag-gen check` (Playwright) |
| **Date Window Compliance** | 2026-09-01 to 2026-10-03 | 100% compliant | `mag-gen render` assertions |
| **PDF File Size** | < 15 MB | 9.31 MB | High-res image compression |
| **CLI Cold Execution Time** | < 15s end-to-end | ~9.2s | Linux 6.12 x86_64 |

---

## 6. Modular Subsystems Architecture

### 6.1 Pluggable Ingestion Engine (`src/magazine_generator/ingestion/`)
The ingestion pipeline decouples intelligence data sources from typesetting:
- `BaseIngestor`: Abstract protocol establishing the normalized article contract.
- `JSONIngestor`: Ingests from wire dumps and structured JSON datasets (`pool.json`, `articles.json`).
- `MarkdownIngestor`: Parses field dispatches written in Markdown with YAML frontmatter.
- `RSSIngestor`: Parses live or archived RSS 2.0 and Atom XML feeds.
- `create_ingestor(type)`: Factory dispatcher for seamless CLI ingestion (`mag-gen ingest`).

### 6.2 Layout Archetypes Registry (`src/magazine_generator/layout/registry.py`)
Layout archetypes are registered with geometric and editorial constraints:
- `lead`: 1 hero story with 108mm photo, 2-column dropcap body, 1 sidebar brief (2 articles).
- `pair`: 2 balanced vertical stories with 72mm photos (2 articles).
- `trio`: 1 top headline story + 2 compact briefing notes (3 articles).
- `quad`: 4 compact intelligence briefs in a symmetrical 2x2 grid (4 articles).
- `photo_essay`: Full-width 130mm panoramic hero photo with expansive analysis (1 article).

### 6.3 Dynamic Auto-Budgeter (`src/magazine_generator/layout/budgeter.py`)
Computes the exact layout matrix for arbitrary target page counts $T$:
- Computes front matter ($P_{\text{front}} \in \{3, 4\}$), section openers ($N_S$), and back matter ($P_{\text{back}} = 2$).
- Pro-rates content pages across sections based on available articles.
- Selects optimal layout archetypes (`lead`, `pair`, `trio`, `quad`, `photo_essay`).
- Dynamically chunks Appendix 2 rationale rows across $K$ pages without generating unwanted trailing sheets.

### 6.4 Modular Theme Subsystem (`static/css/themes/`)
CSS custom properties decouple design tokens into hot-swappable theme stylesheets:
- `army_gold.css`: Classic Army Saffron (`#d9822b`), Olive (`#4b5320`), Paper (`#fbfaf6`).
- `navy_blue.css`: Navy Deep Blue (`#0a192f`), Ocean Accent (`#0077b6`), Crisp Slate Paper (`#f8fafc`).
- `airforce_slate.css`: Air Force Steel Slate (`#1e293b`), Sky Cyan (`#0ea5e9`), Cool Paper (`#f8fafc`).
- `editorial_mono.css`: Minimalist high-contrast monochrome (`#111111`), stark rules, timeless serif.

### 6.5 Declarative YAML Configurations (`configs/`)
Replaces hardcoded parameters with version-controlled YAML specifications:
- `configs/securing_the_northeast_50p.yaml`: Full 50-page compendium specification.
- `configs/briefing_24p.yaml`: 24-page executive tactical briefing specification.
