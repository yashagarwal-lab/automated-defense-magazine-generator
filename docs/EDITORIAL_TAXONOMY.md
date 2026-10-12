# Editorial Taxonomy & Curation Specification

## 1. Editorial Charter

The **Securing the Northeast** publication serves as a comprehensive defense intelligence compendium documenting the Indian Armed Forces' operational posture, strategic infrastructure developments, border diplomacy, and civic initiatives across the Northeast frontier (Arunachal Pradesh, Assam, Manipur, Nagaland, Mizoram, Tripura, Meghalaya, and Sikkim).

All ingested material adheres to strict open-source intelligence (OSINT) standards, cross-verified against verified wire services and regional defense correspondents.

---

## 2. Four-Domain Section Taxonomy

The intelligence pool is partitioned into four balanced, thematic sections:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   SECURING THE NORTHEAST TAXONOMY                      │
├──────────────────────────┬─────────────────────────────────────────────┤
│ 01. Security & Strategic │ Counter-insurgency operations, joint army-   │
│     Affairs              │ police raids, weapons caches, tactical ops  │
├──────────────────────────┼─────────────────────────────────────────────┤
│ 02. Border Infrastructure│ Strategic roads, tunnels, forward bridges,  │
│     & Readiness          │ logistics corridors, high-altitude readiness│
├──────────────────────────┼─────────────────────────────────────────────┤
│ 03. Regional Geopolitics │ LAC border talks, Special Representative     │
│     & External Dynamics  │ meetings, cross-border dynamics (China/Myan)│
├──────────────────────────┼─────────────────────────────────────────────┤
│ 04. Civil-Military       │ Operation Sadbhavana, civic action drives,  │
│     Relations & Outreach │ sports tournaments, youth empowerment, NCC  │
└──────────────────────────┴─────────────────────────────────────────────┘
```

### Section 01: Security & Strategic Affairs
- **Focus:** Operational readiness, counter-insurgency (CI) operations, tactical maneuvers, and counter-terror interdictions.
- **Key Entities:** Eastern Command (Kolkata), Spear Corps (III Corps, Dimapur), Gajraj Corps (IV Corps, Tezpur), Brahmastra Corps (XVII Corps, Panagarh), Assam Rifles, Manipur Police joint task forces.
- **Keywords:** `insurgents`, `militants`, `Assam Rifles`, `Spear Corps`, `IED`, `arms cache`, `patrol`, `joint operation`, `neutralised`.

### Section 02: Border Infrastructure & Readiness
- **Focus:** Physical border security architecture, dual-use infrastructure, logistics mobility, and environmental hazard mitigation.
- **Key Entities:** Border Roads Organisation (BRO), Project Vartak, Project Arunank, Project Dantak, Indian Army Corps of Engineers.
- **Keywords:** `border road`, `Sela tunnel`, `Nechiphu`, `bridge`, `high-altitude`, `logistics`, `glacial lake`, `GLOF`, `LAC forward post`.

### Section 03: Regional Geopolitics & External Dynamics
- **Focus:** Bilateral border negotiations, Corps Commander meetings, buffer zone enforcement, trans-Himalayan infrastructure monitoring.
- **Key Entities:** Line of Actual Control (LAC), McMahon Line, Border Personnel Meeting (BPM) huts (Wacha-Damai, Kibithoo, Bum La, Nathu La), Ministry of External Affairs (MEA), Chinese PLA frontier forces.
- **Keywords:** `LAC`, `talks`, `corps commander`, `Doval`, `Wang Yi`, `Wacha`, `Kibithoo`, `satellite imagery`, `border meeting`, `diplomatic`.

### Section 04: Civil-Military Relations & Community Outreach
- **Focus:** Winning Hearts and Minds (WHAM), civic action programs, educational sponsorship, sports tournaments, disaster relief.
- **Key Entities:** Assam Rifles Civic Action Programme (CAP), Operation Sadbhavana, Durand Cup, Army Public Schools, National Cadet Corps (NCC).
- **Keywords:** `civic action`, `Sadbhavana`, `football`, `sports`, `school`, `medical camp`, `sewing machine`, `youth`, `veterans`, `ESM`.

---

## 3. Strict Temporal & Verification Criteria

1. **Temporal Publication Window:**
   - **Hard Cutoff:** Only articles with verified publication dates in the range:
     $$\text{Date} \in [\text{2026-09-01}, \text{2026-10-03}]$$
   - Any record outside this window triggers immediate pipeline assertion failure.
2. **Exclusion Criteria (Zero-Tolerance Noise Filter):**
   - Purely partisan political party polemics.
   - Unverified local crime blotters unrelated to defense, national security, or border governance.
   - Commercial advertising advertorials and clickbait news spam.
3. **Source Provenance & Attribution:**
   - Every single article retains its canonical publication title, source name, original date, and verified external hyperlink.
   - Hyperlinks are fully interactive across both the digital reader and print PDF.

---

## 4. Curated Editorial Overrides Architecture

In legacy prototypes, editorial interventions were injected by mutating script strings or splicing Python files on disk. `mag-gen` replaces this anti-pattern with an explicit, declarative overrides dictionary in `src/magazine_generator/synthesis/overrides.py`.

```python
EDITORIAL_OVERRIDES = {
    "doval_wang": {
        "match": lambda t, d, text: "doval" in t.lower() and "wang" in t.lower(),
        "summary": "Following recent tension in the Taksing area..."
    },
    "corps_commander": {
        "match": lambda t, d, text: "corps commander" in t.lower() and "wacha" in text.lower(),
        "summary": "India and China recently conducted Corps Commander-level talks at the Wacha-Damai border meeting point..."
    },
    ...
}
```

This decoupled design guarantees:
- **Traceability:** Editorial decisions are version-controlled alongside code.
- **Determinism:** The synthesis pipeline produces identical, verified paragraphs across environments.
- **Extensibility:** Editors can register new strategic summaries without altering the layout engine.
