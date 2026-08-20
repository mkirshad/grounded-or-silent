# Grounded or Silent: Citation-Faithful Legal QA for Pakistani Law

Working folder for the research paper. Product under study: **Irshad AI Employee**
(production system — 946 Pakistan Code statutes + 2,503 LHC judgments 2022–2026,
grounded-or-refuse answering with page-cited sources).

## Planned contributions
1. **PakLegalQA** — first Pakistani legal QA benchmark (questions + gold statute
   sections / case citations, English + Roman Urdu subset).
2. Evaluation of retrieval strategies on it (dense vs hybrid vs title-affinity /
   category-pool / structure-aware ranking).
3. Refusal calibration study: when does the system correctly say "the documents
   don't answer this" vs guess.
4. Analysis of anonymised production queries from a deployed system.

Target venue: arXiv preprint → NLLP workshop (EMNLP). Step-up: JURIX / ICAIL.

## papers/ — reading list (all fetched 2026-08-20, open access)

| File | Cite as | Take from it |
|---|---|---|
| 2024-Magesh-Hallucination-Free-legal-tools.pdf | Magesh et al. 2024 (arXiv:2405.20362) | Audit methodology for legal AI tools; headline framing to replicate for Pakistan |
| 2024-Dahl-Large-Legal-Fictions.pdf | Dahl et al. 2024 (arXiv:2401.01301) | Taxonomy of legal hallucination types — use to classify failures |
| 2023-Gao-ALCE-citations.pdf | Gao et al. 2023 (arXiv:2305.14627) | Citation precision/recall metrics — scoring "cites the right page" |
| 2020-Lewis-RAG.pdf | Lewis et al. 2020 (arXiv:2005.11401) | Canonical RAG citation, baseline architecture |
| 2023-Asai-Self-RAG.pdf | Asai et al. 2023 (arXiv:2310.11511) | Self-reflective retrieval/abstention framing |
| 2022-Kadavath-Know-What-They-Know.pdf | Kadavath et al. 2022 (arXiv:2207.05221) | Model self-knowledge / calibration for the refusal study |
| 2023-Guha-LegalBench.pdf | Guha et al. 2023 (arXiv:2308.11462) | Benchmark construction: question sourcing, gold labels, annotation |
| 2021-Chalkidis-LexGLUE.pdf | Chalkidis et al. 2022 (arXiv:2110.00976) | How legal NLP papers structure task suites |
| 2020-Khattab-ColBERT.pdf | Khattab & Zaharia 2020 (arXiv:2004.12832) | Dense/late-interaction retrieval baseline |
| 2023-Li-SAILER-legal-retrieval.pdf | Li et al. 2023 (arXiv:2304.11370) | Structure-aware legal case retrieval — closest prior to our statute-structure problem |
| 2023-Li-LeCaRDv2.pdf | Li et al. 2024 (arXiv:2310.17609) | Chinese legal case retrieval dataset design (v2; v1 = Ma et al. SIGIR'21, ACM-only) |
| 2024-COLIEE2024-task1-summary.pdf | COLIEE 2024 task 1 summary | Competition task design + evaluation conventions |

Added by the 2026-08-20 novelty sweep (see design doc §2 for positioning):

| File | Cite as | Why it matters |
|---|---|---|
| 2024-Mahmood-LEGAL-UQA-pakistan-constitution.pdf | LEGAL-UQA (arXiv:2410.13013) | CLOSEST prior work: 619 Urdu-English QA pairs from Pakistan's constitution only — must be cited and differentiated prominently |
| 2026-Chae-SearchFireSafety-statute-QA.pdf | Chae et al. 2026 (arXiv:2604.06173) | Statutory retrieval gap + refusal stress-testing (fire-safety regs) — methodological neighbour |
| 2026-Butler-Legal-RAG-Bench.pdf | Butler & Butler 2026 (arXiv:2603.01710) | End-to-end legal RAG eval, Victorian Criminal Charge Book |
| 2024-Joshi-IL-TUR-indian-legal.pdf | IL-TUR (ACL 2024) | Indian legal NLP benchmark family — South Asia is served; our claim is Pakistan-specific |

Not fetched (paywalled — cite without PDF):
- Robertson & Zaragoza 2009, "The Probabilistic Relevance Framework: BM25 and
  Beyond" (Foundations and Trends in IR) — BM25 baseline citation.
- Ma et al. 2021, LeCaRD v1 (SIGIR '21, ACM) — cite alongside LeCaRDv2.

## Progress (2026-08-20)
- Design doc, harness (`run_paklegalqa`), and corpus manifest v1 done.
- Pilot (20 q) run; findings F1–F4 fixed in production, F5 = rubric additions.
- **Benchmark: 137/300 questions authored** (pilot-20 + batch-02 + batch-03),
  every statute gold checked against corpus text (`corpus/verify_checks*.py`,
  60 checks across two waves). Confirmed corpus gaps: Court Fees Act 1870
  (absent) and Limitation Act 1908 First Schedule (missing from ingest).
  Lesson: title patterns must be fuzzy — "Anti Terrorism Act (ATA),1997" has no
  hyphen and two questions were misfiled as UNANS before the engine itself
  corrected the record.
- Quota progress after batch-04 (202/300 total): S-REC 47/80 · S-INT 33/60 ·
  C-HOLD 14/50 · C-FACT 16/20 · TIME 13/20 · FALSE 16/20 · UNANS 28/50 ·
  RU 35/60. Remaining ~98 lean on S-REC (33), C-HOLD (36 — needs more judgment
  sampling; read chunks[-2] where the last chunk is signature-only), S-INT (27),
  RU (25), UNANS (22).
- Batch-04 smoke: TIME-174 (suicide) revealed the ingested PPC REFLECTS the
  2022 amendment — answer cited Act XXXVII of 2022 with the exact date. The
  corpus is more current than assumed; amendment-currency probes work.
- Batch-03 smoke: C-HOLD-102 (maintenance holding) answered exactly per gold;
  **new RU/EN divergence pair found** — custody question answers in English
  (S-INT-094) but refuses in Roman Urdu (RU-128), showing per-question RU
  variance persists after the translation fix. Candidate finding F6.
- Novelty sweep done (design doc §2): LEGAL-UQA is the closest prior; four
  defensible novelty claims stand.

## Next steps
1. Author remaining ~226 questions (statute long tail, more C-HOLD from judgment
   sampling, production-log-derived items, RU overlay to 60).
2. Advocate verification round (30% sample per category).
3. Ablation flags in the harness (CB / BM25 / DENSE / HYB / ABL-x) + full runs.
4. ChatGPT Research novelty sweep on the design doc (user-side).
5. Anonymisation protocol for production question logs before any use.
