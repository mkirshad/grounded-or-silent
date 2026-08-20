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

## 2026-08-20 (night — batch 06: AUTHORING COMPLETE)

- Harvest round 2 (`harvest_dispositions_2.py`, ascending ids, used-titles
  excluded): 26 dispositions → 22 C-HOLD golds (criminal appeals with
  convictions set aside, a merger petition, service transfers, civil
  revisions both ways).
- Verification wave 5: 24/24 FOUND (labour trio — Payment of Wages 1936,
  Workmen's Compensation 1923, IRA 2012 — plus CNSA 1997, Zakat & Ushr 1980,
  bailment/agency/guarantee/lease/exchange, habeas 491, s.145, holder in due
  course, probate, ITO 122, PECA 13-14, TM/copyright infringement).
- batch-06 (89 items): C-HOLD 22, S-REC 18, TIME 3, S-INT 19, UNANS 14, RU 13.
- **MILESTONE: PakLegalQA v1 authoring complete — 360 items: main 300/300
  (S-REC 80, S-INT 60, C-HOLD 50, C-FACT 20, TIME 20, FALSE 20, UNANS 50) +
  RU overlay 60/60. All ids unique, all twin references valid, every statute
  gold corpus-checked (5 waves, ~115 checks), every C-HOLD from a read or
  harvested disposition.**
- All golds remain `verified: false` until the advocate round (30% per
  category per the design's annotation protocol).

Next: (1) advocate verification round — user recruits 1–2 Bar contacts,
offer co-authorship; (2) ablation flags in run_paklegalqa (CB/BM25/DENSE/
HYB/ABL-x); (3) full 360-item runs on a corpus snapshot; (4) scoring
scripts; (5) paper drafting (ask user for sample preprints first).

## 2026-08-21 (incident + correction: credit exhaustion contaminated prod-sol's tail)

- OpenAI credits ran out DURING prod-sol (~row 225 of 360), not after it:
  embedding calls failed silently, the engine refused everything with empty
  sources, and the run "completed" looking plausible. Positional analysis
  exposed it: refusal rate by 60-row window = 10,10,13,19,60,60.
- **The earlier "32% over-refusal / too silent" reading is RETRACTED as an
  artifact.** Clean head (225 rows): 84% answered, 25 correct refusals,
  **over-refusal only 5%** — the system is far better calibrated than the
  contaminated table suggested.
- Methods lesson worth a paragraph in the paper: a silent dependency failure
  produced a plausible-looking calibration collapse; per-position (or
  per-timestamp) sanity checks belong in any LLM evaluation harness.
- Surgery: clean head preserved (prod-sol-clean-head.jsonl), 135 suspect ids
  listed, rerun + merge scripts added (rerun_prodsol_tail.sh, merge_prodsol.py)
  — tail reruns after the main driver finishes (model must be back on Sol).
- Live-product side effect of the same outage acknowledged: /ask refused all
  questions during the window; verified recovered after top-up.

## 2026-08-20 (late night — ablation harness built and proven)

- Backend commit 578b975: `AIE_EVAL_RETRIEVAL` contextvar (default "prod",
  production never changes) gates three component groups: candidate pools
  (dense/abl-pools), title affinity (dense/abl-title), keyword+citation
  rescues incl. deep-read (dense/abl-rescue). Closed-book ("cb") lives in the
  management command only — no production path can run ungrounded. Regression
  test asserts dense bypasses rescues and prod uses them. Suite green.
- BM25/HYB deferred to the scoring phase (offline rank_bm25 over the corpus
  snapshot; noted in design §4.1 as build-needed).
- **Mini comparative run (4 diagnostic questions × prod/dense/cb),
  `results/ablation-mini-*.jsonl` — the paper's story in miniature:**
  - PROD 4/4: three grounded answers + correct refusal on the SC question.
  - DENSE loses the citation lookup: "which judge decided 2025 LHC 846"
    REFUSED (rescue components carry it in prod).
  - CB: honest "I do not know" on the judge; statute answers plausible from
    parametric knowledge; but ANSWERS the Panama-case question from memory —
    exactly the behaviour a corpus-grounded system must not exhibit. UNANS
    items thus measure grounding DISCIPLINE, not model ignorance — worth a
    paragraph in the paper.
