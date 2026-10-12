# Mathematical Page Budgeting & Physical Typesetting Model

## 1. Physical Constraints & Target Budget

The publication must adhere to a strict **50-Page Target Budget** under the **ISO 216 A4 Portrait** standard ($210\text{mm} \times 297\text{mm}$).

### Comprehensive 50-Page Sequence Inventory

$$\sum_{i=1}^{8} \text{Pages}_i = 1 + 1 + 1 + 1 + 12 + 11 + 9 + 9 + 1 + 3 + 1 = 50$$

```
┌───────┬───────────────────────────────────┬──────────────┬───────────────┐
│ Page  │ Functional Role                   │ Layout Type  │ Article Count │
├───────┼───────────────────────────────────┼──────────────┼───────────────┤
│ 01    │ Front Cover (Masthead & Artwork)  │ cover        │ 0             │
│ 02    │ Table of Contents & Colophon      │ contents     │ 0             │
│ 03    │ Editor's Letter & Statistics      │ editor       │ 0             │
│ 04    │ Theater Primer & Order of Battle  │ overview     │ 0             │
│ 05–16 │ Section 01: Security & Strategy   │ 1 Opener +11 │ 22 articles   │
│ 17–27 │ Section 02: Infrastructure        │ 1 Opener +10 │ 20 articles   │
│ 28–36 │ Section 03: Geopolitics & LAC     │ 1 Opener + 8 │ 16 articles   │
│ 37–45 │ Section 04: Civil-Military WHAM   │ 1 Opener + 8 │ 16 articles   │
│ 46    │ Appendix 1: Sources & Counts      │ appendix-src │ (Chart/Table) │
│ 47–49 │ Appendix 2: Editorial Rationale   │ appendix-rat │ 74 articles   │
│ 50    │ Back Cover (Citation & Seal)      │ back         │ 0             │
├───────┴───────────────────────────────────┴──────────────┼───────────────┤
│ TOTAL PUBLICATION BUDGET                                  │ 50 Pages      │
└───────────────────────────────────────────────────────────┴───────────────┘
```

---

## 2. Geometry & Grid Allocation Formulas

### 2.1 Page Margin Geometry
- **Page Dimensions:** $W = 210\text{mm}$, $H = 297\text{mm}$.
- **Print Safety Margins:**
  * Top: $14\text{mm}$
  * Bottom: $15\text{mm}$
  * Inner (Gutter side): $18\text{mm}$ (accommodates binding shift)
  * Outer: $14\text{mm}$
- **Effective Printable Area:**
  $$W_{\text{eff}} = 210 - (18 + 14) = 178\text{mm}$$
  $$H_{\text{eff}} = 297 - (14 + 15) = 268\text{mm}$$

### 2.2 Layout Archetypes

#### A. Lead Layout (`layout-lead`)
- **Structure:** 1 primary feature story + 1 secondary sidebar story.
- **Top Image:** Fixed height $108\text{mm} \times 178\text{mm}$.
- **Grid Ratio:**
  $$W_{\text{main}} = 116\text{mm} \quad (\text{2-column dropcap prose}) \quad \mid \quad W_{\text{side}} = 56\text{mm} \quad (\text{sidebar brief + pullquote})$$
  $$\text{Column Gutter} = 6\text{mm}$$

#### B. Pair Layout (`layout-pair`)
- **Structure:** 2 balanced parallel intelligence reports.
- **Top Images:** Fixed height $72\text{mm}$ each.
- **Grid Ratio:** Symmetrical split:
  $$W_1 = W_2 = \frac{178 - 7}{2} = 85.5\text{mm}$$

#### C. Trio Layout (`layout-trio`)
- **Structure:** 1 horizontal headline story + 2 compact briefing notes.
- **Top Area:** Horizontal split ($88\text{mm}$ image + $84\text{mm}$ text block).
- **Bottom Area:** 2 columns with optional thumbnail briefs.

---

## 3. Appendix Row Chunking Math

Appendix 2 contains an exhaustive, transparent defense rationale explaining why each of the 74 curated articles was selected.

Because table row heights vary based on article title and rationale length, rows are mathematically chunked across three consecutive appendix pages:

$$\text{Rows Per Page} = [23, 25, 26]$$

- **Page 47 (Appendix 2, Sheet 1):**
  * Title block & dek: $38\text{mm}$
  * Table header: $8\text{mm}$
  * Capacity: 23 rows $\times \sim 9.5\text{mm} = 218.5\text{mm}$
- **Page 48 (Appendix 2, Sheet 2):**
  * Continuation running head: $12\text{mm}$
  * Table header: $8\text{mm}$
  * Capacity: 25 rows $\times \sim 9.5\text{mm} = 237.5\text{mm}$
- **Page 49 (Appendix 2, Sheet 3):**
  * Continuation running head: $12\text{mm}$
  * Table header: $8\text{mm}$
  * Capacity: 26 rows $\times \sim 9.5\text{mm} = 247.0\text{mm}$

$$\sum \text{Rows} = 23 + 25 + 26 = 74 = \text{Total Curated Articles}$$

This deterministic partition guarantees that all 74 editorial records fit without generating an unexpected 51st page.
