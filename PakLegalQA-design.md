# Grounded or Silent: Citation-Faithful Legal QA for Pakistani Law
## Research design draft v0.1 — 2026-08-20
### Author: Muhammad Kashif Irshad · System under study: Irshad AI Employee (production)

> Status: design draft for external review (ChatGPT Research pass planned).
> Everything marked ⚠ is a decision still open or a known reviewer risk.

---

## 1 · Abstract (draft)

Legal AI tools hallucinate. Magesh et al. (2024) found that even purpose-built,
RAG-based legal research products from LexisNexis and Thomson Reuters answer with
hallucinations 17–33% of the time. Every existing legal QA benchmark, however,
targets a handful of well-resourced jurisdictions (US, EU, Japan, China); no
benchmark exists for Pakistan — a mixed common-law jurisdiction of 240 million
people whose statutes and judgments are published in English but whose users
increasingly query in Roman Urdu. We present **PakLegalQA**, the first legal QA
benchmark for Pakistani law: N questions over 946 federal statutes (Pakistan Code)
and 2,503 reported Lahore High Court judgments (2022–2026), each labelled with gold
statute sections or case citations, including an *unanswerable* subset whose only
correct response is a refusal and a Roman-Urdu paraphrase subset. Using PakLegalQA
we evaluate a deployed, grounded-or-refuse RAG system and ablations of its
retrieval stack (dense-only, lexical, category-pooled, title-affinity ranking),
measuring correctness, citation faithfulness (ALCE-style citation precision/
recall), and *refusal calibration* — how often the system correctly stays silent
versus guessing. We find [RESULTS]. We release the benchmark, evaluation harness,
and an analysis of anonymised production queries from the deployed system.

**Contributions:**
1. PakLegalQA — first Pakistani legal QA benchmark (statutes + case law + refusal
   set + Roman-Urdu subset), with gold citations at section/page granularity.
2. First evaluation of grounded legal QA on a low-resource-jurisdiction corpus,
   including retrieval ablations that show where general-purpose dense retrieval
   fails on statutory text (e.g., semantically-near but legally-wrong acts
   outranking the governing statute).
3. A refusal-calibration methodology and results for a production
   grounded-or-refuse system, extending Magesh et al.'s correctness/groundedness
   coding with an explicit abstention axis.
4. A taxonomy-coded analysis of real user queries from deployment (anonymised),
   showing what lawyers and laypeople actually ask.

---

## 2 · Positioning against prior work (the "combination")

| Prior work | What we take | What we add |
|---|---|---|
| Magesh et al. 2024 (Hallucination-Free?) | Correctness (correct/incorrect/refusal) × groundedness (grounded/misgrounded/ungrounded) manual coding; query category design (general research / jurisdiction-time / false premise / factual recall) | New jurisdiction; open system (they audited closed products); refusal treated as a *designed behaviour* to calibrate, not only a failure mode |
| Dahl et al. 2024 (Large Legal Fictions) | Hallucination taxonomy (unfaithful to training data / prompt / world) | Applied to a RAG system where "prompt" = retrieved statutes; failure classification of our errors |
| Gao et al. 2023 (ALCE) | Automatic citation recall/precision via NLI over cited passages | Legal-domain adaptation: passages = statute sections / judgment pages, not 100-word Wikipedia chunks ⚠ (chunking choice must be justified) |
| Lewis et al. 2020 (RAG) | Canonical architecture citation | — |
| Asai et al. 2023 (Self-RAG); Kadavath et al. 2022 | Abstention/self-knowledge framing | Production grounded-or-refuse policy with confidence threshold + retry, measured as calibration |
| Guha et al. 2023 (LegalBench); Chalkidis et al. 2022 (LexGLUE) | Benchmark/task-suite construction conventions, annotation reporting | New jurisdiction + citation-level gold labels |
| LeCaRDv2 (Li et al. 2024); COLIEE 2024 | Case-retrieval task design, pooled relevance judgments | Statute+case mixed corpus; QA (not just retrieval) with citations |
| SAILER (Li et al. 2023) | Structure-aware legal retrieval motivation | Statute structure (sections/schedules) rather than case structure |
| Khattab & Zaharia 2020 (ColBERT); Robertson & Zaragoza 2009 (BM25) | Retrieval baselines | — |

### Novelty sweep (2026-08-20, web search — supersedes the first claim draft)

Closest prior work found, all to be cited and differentiated:

- **LEGAL-UQA** (arXiv:2410.13013) — THE closest: 619 English↔Urdu QA pairs from
  Pakistan's **constitution only**. No statutes beyond it, no case law, no
  page-level citation golds, no refusal set, formal parallel Urdu (not
  code-switched Roman Urdu). We must cite it prominently and position against it.
- **Indian legal NLP family** — IL-TUR (ACL 2024), ILDC, IndicLegalQA, IL-PCSR
  (statute+case retrieval): South Asia is NOT unserved; the earlier "any
  South-Asian jurisdiction" wording was wrong and is withdrawn.
- **SearchFireSafety / "Beyond Case Law"** (arXiv:2604.06173, Jan 2026) —
  statute-centric QA with hierarchical-retrieval gap + refusal stress-testing,
  on fire-safety regulations. Methodological neighbour for our statutory
  retrieval failure analysis; different jurisdiction, single regulatory domain,
  no case law, lab-only.
- **Legal RAG Bench** (arXiv:2603.01710, Isaacus) — end-to-end legal RAG eval,
  100 questions over the Victorian Criminal Charge Book (Australia).
- **LegalBench-RAG**, **LegalCiteBench** (arXiv:2605.10186), **ClaimRAG-LAW**
  (arXiv:2605.21071), **RefusalBench** (EACL 2026), **LRAGE**, and the Stanford
  legal-RAG hallucination study (JELS 2025) — the citation-faithfulness and
  abstention evaluation toolbox we draw metrics from.

**Revised novelty claim (defensible after the sweep):**
1. First citation-grounded QA benchmark for **Pakistani law spanning statutes
   and case law** (LEGAL-UQA covers the constitution only, without citation-level
   golds or an unanswerable set).
2. First refusal-calibration study of a **deployed, production**
   grounded-or-refuse legal system, including analysis of real user queries —
   every benchmark above is a lab evaluation.
3. First **code-switched Roman-Urdu** legal QA subset (as users actually type,
   vs. LEGAL-UQA's formal parallel translations).
4. First measurement of **query-generation-stage hallucination** in legal RAG
   (the rewrite model injecting a wrong-jurisdiction statute), a failure stage
   named but unmeasured in prior work.

---

## 3 · PakLegalQA benchmark design

### 3.1 Corpus (fixed, versioned)
- **Statutes:** 946 federal acts/ordinances from the Pakistan Code (official PDFs,
  page-anchored). Known gap: some acts lack schedules (e.g., Limitation Act 1908
  First Schedule) — audit and either repair or document as a corpus limitation. ⚠
- **Case law:** 2,503 reported LHC judgments 2022–2026 with neutral citations
  (e.g., 2025 LHC 846), judge, year, official PDF link.
- Freeze a corpus snapshot (document list + checksums) and version it
  (`paklegalqa-corpus-v1`) so results are reproducible.

### 3.2 Question taxonomy (adapting Magesh et al. to a statutory jurisdiction)

| Code | Type | Example | Gold label |
|---|---|---|---|
| S-REC | Statute recall | "What is the punishment for dishonour of a cheque?" | Act + section (+ page) |
| S-INT | Statute interpretation / doctrine | "What are the conditions for bail in a non-bailable offence?" | Act + section; multiple sources allowed |
| C-HOLD | Case-law holding | "What did the LHC hold on PECA bailability in 2025?" | Neutral citation(s) |
| C-FACT | Judgment factual recall | "Which judge decided 2025 LHC 846?" | Neutral citation |
| TIME | Time/amendment-sensitive | "Is the punishment under s.489-F still seven years?" | Act + section, amendment note |
| FALSE | False premise | "Which section of the Cyber Crimes Act 1995 covers SIM fraud?" (no such act) | correct = correction or refusal |
| UNANS | Unanswerable from corpus | Provincial statutes, Supreme Court-only doctrine, medical questions | correct = refusal |
| RU | Roman-Urdu paraphrases of a sample of the above | "Cheque bounce hone par kya saza hai?" | same gold as source question |

Size targets (v1, solo-feasible): **300 questions** — 80 S-REC, 60 S-INT,
50 C-HOLD, 20 C-FACT, 20 TIME, 20 FALSE, 50 UNANS; plus RU paraphrases of 60
questions sampled across types (RU is an overlay, not new gold labels).
⚠ Reviewer risk: 300 is small — defend with per-category confidence intervals and
compare to Magesh et al.'s n=202.

### 3.3 Question sourcing (three independent streams)
1. **Headnote-derived:** from LHC judgment tag lines and holdings (author-written,
   lawyer-checked).
2. **Statute-derived:** systematic templates over high-traffic acts (PPC, CrPC,
   CPC, Qanun-e-Shahadat, NI Act, PECA, Companies Act, tax ordinances).
3. **Production-derived:** anonymised real queries from the deployed system's
   question logs (see §6 ethics). These keep the benchmark honest about what
   people actually ask — including vague and code-switched phrasings.

### 3.4 Gold-label schema (JSONL, one question per line)
```json
{
  "id": "S-REC-014",
  "type": "S-REC",
  "language": "en",
  "question": "What is the punishment for dishonour of a cheque in Pakistan?",
  "answerable": true,
  "gold_sources": [
    {"doc_type": "statute", "title": "Pakistan Penal Code 1860",
     "section": "489-F", "pages": [214]},
    {"doc_type": "judgment", "citation": "2024 LHC 6629", "optional": true}
  ],
  "gold_answer_points": [
    "imprisonment up to three years, or fine, or both",
    "offence relates to dishonest issuance of a cheque"
  ],
  "source_stream": "statute-derived",
  "annotator": "MKI", "verified_by": "advocate-1"
}
```
- `gold_answer_points` = short claims for ALCE-style NLI scoring.
- `optional: true` marks sources that support but are not required.

### 3.5 Annotation protocol
- Author drafts all gold labels; **at least one licensed advocate independently
  verifies a random 30% sample per category**; report agreement (percent + Cohen's
  κ on answerable/refusal and on primary gold source). Disagreements adjudicated
  and documented. ⚠ Need 1–2 advocate collaborators (Bar demo contacts) — offer
  co-authorship; this also materially strengthens the paper's credibility.
- Every gold source must be verifiable by opening the official PDF at the cited
  page — the same standard the product promises users.

---

## 4 · Systems and experiments

### 4.1 Systems compared
| ID | System | Purpose |
|---|---|---|
| CB | Closed-book LLM (same answer model, no retrieval) | Floor; replicates Dahl-style hallucination rates for Pakistani law |
| BM25 | Lexical retrieval → same generator | Classic baseline |
| DENSE | text-embedding-3-small cosine, top-k, no domain logic | "Vanilla RAG" |
| HYB | BM25 + dense reciprocal-rank fusion | Standard strong baseline ⚠ build needed |
| PROD | Full production stack: category pools (statute/caselaw), title-affinity boost, vector floor, per-document diversity cap, grounded-or-refuse policy with confidence threshold + retry | The studied system |
| ABL-x | PROD minus one component at a time (pools / title affinity / floor / refusal-retry) | Which component buys what |

All systems share the same generator and prompt so retrieval is the only variable
(except CB). Fixed decoding settings; N=1 run per question per system, plus a
stability probe (3 repeats on a 50-question sample) to report variance.

### 4.2 Metrics
- **Retrieval:** gold-source recall@k (k=5), MRR of the primary gold source.
- **Answer correctness:** manual coding per Magesh et al.: correct / incorrect /
  refusal; plus automatic claim recall via NLI over `gold_answer_points`
  (ALCE-style) to scale.
- **Citation faithfulness:** citation precision and recall (does each cited
  source support the answer; is every key claim cited) — automatic NLI +
  manual audit of a 20% sample to validate the automatic metric. ⚠ Choose NLI
  model; TRUE (T5-11B) is heavy — a modern LLM-as-judge with the manual audit as
  validation is acceptable if disclosed.
- **Refusal calibration:**
  - correct-refusal rate on UNANS + FALSE (higher = better)
  - over-refusal rate on answerable questions (lower = better)
  - calibration curve: refusal frequency vs. the system's internal confidence;
    ECE-style summary using the production confidence score.
- **Language robustness:** all of the above on the RU subset vs. English twins.

### 4.3 Headline analyses planned
1. Hallucination rate of vanilla RAG vs PROD on Pakistani law (the Magesh
   replication, on an open system).
2. The statutory-retrieval failure mode: quantify how often DENSE ranks a
   semantically-near but legally-wrong act above the governing statute
   (e.g., military-law ordinances outranking PPC on "theft"), and how much the
   title-affinity + category-pool ablations recover.
3. Refuse-vs-guess: what fraction of would-be hallucinations the refusal policy
   converts into silence, and at what over-refusal cost.
4. Production-query analysis: taxonomy-coded distribution of real questions;
   share answerable from the corpus; language mix.

---

## 5 · Evaluation harness (build plan)

- Django management command `run_paklegalqa` in the backend repo:
  reads the JSONL, calls `answer_question()` **directly (offline)** per system
  variant (flags select retrieval mode), writes one result JSONL per run:
  question id, retrieved docs + scores, answer text, cited sources, confidence,
  refusal flag, latency, token/cost counters.
- Never through the public web endpoint (no allowance burn, no rate limits).
- Run against a **local corpus snapshot** (Neon branch or pg_dump restore), not
  live prod. ⚠ Cost estimate needed: ~300 q × 6 systems × Sol weight — consider
  running ablations on gpt-4o and only PROD + DENSE on Sol; disclose.
- Scoring scripts in `research/grounded-or-silent/eval/` (Python, no Django):
  retrieval metrics, NLI scoring, calibration plots, LaTeX tables.

---

## 6 · Ethics, licensing, anonymisation

- Statutes and reported judgments are public documents; the benchmark
  redistributes only citations, sections, page numbers and short quotes — link to
  official PDFs rather than bundling them. ⚠ Confirm Pakistan Code / LHC site
  terms permit citation-level redistribution (they do for citation; do not bundle
  full PDF text in the release).
- Production queries: strip all identifiers (names, phone numbers, CNIC, case
  numbers when tied to private matters); only aggregate statistics and paraphrased
  exemplars appear in the paper; raw logs never released. State this in the paper.
- No PLD/PLJ/CLC/SCMR headnote text anywhere (copyrighted); neutral citations only.
- Disclose author's dual role (system builder + evaluator) prominently; the
  benchmark and harness release is the mitigation — anyone can rerun and extend.

---

## 7 · Paper outline (target: NLLP @ EMNLP, 8pp + appendix; arXiv first)

> **At writing time:** ask the author for his previously published preprints and
> follow their format (or better). Known exemplar: the Sabbath Pond Test paper —
> irshados.com/ebooks/islamic-banking-sabbath-pond-test-reevaluation/ (+ its
> paper.pdf), source in the IrshadOS-Main-Site repo. Publication mirrors that
> route: paper page + PDF on irshados.com alongside the arXiv upload.

1. Introduction — the Magesh 17–33% finding; the jurisdictional gap; contributions.
2. Background & related work (§2 table in prose).
3. PakLegalQA (§3): corpus, taxonomy, sourcing, annotation, statistics table.
4. Systems (§4.1) and the grounded-or-refuse policy as a first-class design.
5. Results: retrieval table; correctness/groundedness table; refusal calibration
   figure; RU-vs-EN table; the statutory-retrieval failure analysis.
6. Production query study.
7. Limitations (single jurisdiction slice: federal + LHC only; benchmark size;
   author-built system; automatic-metric validity bounded by the manual audit).
8. Ethics statement (§6).
9. Release: benchmark JSONL, harness, corpus manifest (checksums + fetch scripts).

## 8 · Timeline (weekends, realistic)

| Wk | Milestone |
|---|---|
| 1–2 | Corpus snapshot + manifest; schedule audit; harness skeleton + CB/DENSE/PROD runs on 20 pilot questions |
| 3–5 | Author 300 questions + gold labels (taxonomy quotas) |
| 6 | Advocate verification round; fix labels; agreement stats |
| 7 | Build BM25/HYB + ablation flags; full runs |
| 8 | Scoring, tables, calibration plots; manual coding of PROD + DENSE outputs |
| 9–10 | Write paper; internal review (ChatGPT Research pass on draft); arXiv |
| 11+ | NLLP submission at next deadline |

## 9 · Product payoff checklist (why IrshadOS is "first user")
- Ablation results directly tune the live retrieval stack (keep what buys
  citation-recall, drop what doesn't).
- Site claim after publication: "evaluated on PakLegalQA — [X]% citation
  precision, [Y]% correct-refusal, 0 fabricated citations" with a link to the
  paper. (Only claims the numbers support.)
- Benchmark page on irshados.com → inbound citations and Bar credibility.
- The RU results decide whether to invest in Urdu-aware retrieval next.
