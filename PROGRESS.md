# Grounded or Silent — dated progress log

One entry per working session. The README holds current state; this file holds
the story (what happened, in order), so the paper's methods section can be
reconstructed without any chat history.

## 2026-08-20 (day 1 — design, pilot, fixes, 202 questions)

**Morning — setup and design**
- Downloaded 12 open-access papers (reading list in README); design doc
  `PakLegalQA-design.md` v0.1 written: taxonomy (8 types), gold-label JSONL
  schema, annotation protocol (advocate verifies 30%/category), 6 systems
  (CB/BM25/DENSE/HYB/PROD/ABL-x), metrics (Magesh coding, ALCE citation P/R,
  refusal calibration), ethics, timeline.

**Pilot (20 questions) and findings F1–F5**
- Harness `run_paklegalqa` added to the backend (offline, library-only:
  folder_ids=[] + folders_chosen=False). 20/20 ran clean.
- F1 query-rewrite hallucination: rewrite injected "Negotiable Instruments
  Act" (Indian location of cheque dishonour); PPC 489-F unreachable. FIXED
  (Pakistan-only guard, commit 3911423).
- F2 neutral citations unretrievable ("2025 LHC 846"): FIXED via _citation_hits
  regex lookup + tests (commit c4e3a4d).
- F4 Roman-Urdu regression: the F1 prompt patch made the rewrite stop
  translating; RU twins refused while EN twins answered. FIXED (numbered-rules
  prompt, translation first; same commit). Meta-lesson recorded: rerun RU twins
  after ANY rewrite-prompt change.
- F3 holding questions read header pages: FIXED (deep-read of named/cited
  judgments at both ends + per-term title rescue + institutional stop-words;
  commit 26a2e3b). All fixes deployed to Cloud Run and verified live.
- F5: rubric needs "implicit premise correction" and "grounded non-answer"
  categories. Full details: `results/pilot-run1-summary.md`.

**Novelty sweep (done in-house, web search)**
- Closest prior: LEGAL-UQA (arXiv:2410.13013, Pakistan constitution-only).
  Indian family (IL-TUR, ILDC, IndicLegalQA, IL-PCSR); SearchFireSafety
  (2604.06173); Legal RAG Bench (2603.01710); citation/abstention toolbox
  (LegalCiteBench, ClaimRAG-LAW, RefusalBench, LRAGE). "First for South Asia"
  claim WITHDRAWN; four narrowed claims recorded in design doc §2. Four new
  PDFs added to papers/.

**Corpus**
- Manifest v1 frozen: 3,449 documents (946 statutes + 2,503 LHC judgments),
  SHA-256 checksums → `corpus/manifest-v1.jsonl`.
- Confirmed gaps: Court Fees Act 1870 absent; Limitation Act 1908 First
  Schedule missing. False-alarm lesson: statute titles have odd spellings
  ("Anti Terrorism Act (ATA),1997" — no hyphen) — verify absences with iregex.
- Good news: ingested PPC carries the 2022 amendments (s.325 suicide omission,
  cited by the engine as Act XXXVII of 2022, effective 28.12.2022).

**Question authoring — 202/300**
- pilot-20 (20) → batch-02 (54) → batch-03 (63) → batch-04 (65).
- Every statute gold checked against corpus text before writing
  (`corpus/verify_checks*.py`, 3 waves, ~70 checks). Case-law golds taken from
  dispositions read in judgment tails (`corpus/sample_judgments*.py`, 3 waves).
- Candidate finding F6: RU/EN divergence persists per-question after the
  translation fix (custody: EN answered, RU refused — batch03-smoke).
- Quotas: S-REC 47/80 · S-INT 33/60 · C-HOLD 14/50 · C-FACT 16/20 ·
  TIME 13/20 · FALSE 16/20 · UNANS 28/50 · RU 35/60.

**Repo**: this folder became a git repository on 2026-08-20, pushed to the
private GitHub repo mkirshad/grounded-or-silent (see git log for everything
after this line).

## 2026-08-20 (evening — batch 05, disposition harvester, accounting fix)

- `corpus/harvest_dispositions.py`: regex-harvests explicit disposition
  sentences from ANY chunk (the last chunk is often just signatures) — 22
  dispositions in one pass; 14 became C-HOLD golds.
- Verification wave 4 (18 checks, 16 FOUND): PPC 448/468/511/34, QSO Art 133,
  Contract 73/124, TPA 52/58, Succession 372, Companies AGM/memorandum,
  ITO 114, Sales Tax registration, PECA 16/10.
- batch-05 (69 items): C-HOLD 14, C-FACT 4 (quota complete), S-REC 15,
  S-INT 8, UNANS 8, TIME 4, FALSE 4 (quota complete), RU 12.
- **Accounting correction**: the 300 target is the MAIN set; the 60 RU twins
  are an overlay (360 items total). True position: main 224/300
  (S-REC 62/80 · S-INT 41/60 · C-HOLD 28/50 · C-FACT 20/20 · TIME 17/20 ·
  FALSE 20/20 · UNANS 36/50) + RU overlay 47/60.
- Remaining: 76 main (S-REC 18, S-INT 19, C-HOLD 22, TIME 3, UNANS 14) +
  13 RU — two more authoring passes.
