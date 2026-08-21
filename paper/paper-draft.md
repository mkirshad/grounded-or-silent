# Grounded or Silent: Citation-Faithful Legal Question Answering for Pakistani Law

**Muhammad Kashif Irshad**
IrshadOS, Lahore, Pakistan · ORCID 0009-0008-9161-9875
DOI: 10.5281/zenodo.22037183 · Preprint

> DRAFT v0.1 — sections 6–7 carry [RESULT] placeholders pending the final
> experiment merge. Everything else is prose-complete for review.

## Abstract

Legal AI tools are known to hallucinate: audits of commercial legal research
products report fabricated or misgrounded authorities in 17–33% of responses
(Magesh et al., 2024). Existing legal QA benchmarks cover well-resourced
jurisdictions; for Pakistan — a mixed common-law system of 240 million people —
no benchmark spans its statutes and case law. We present PakLegalQA, the first
citation-grounded question-answering benchmark for Pakistani law: 300 questions
over 946 federal statutes (Pakistan Code) and 2,503 reported Lahore High Court
judgments (2022–2026), with gold statute sections and neutral citations, an
unanswerable subset whose only correct response is a refusal, and a 60-question
code-switched Roman-Urdu overlay reflecting how users actually type. Using
PakLegalQA we evaluate a deployed, production grounded-or-refuse RAG system and
ablations of its retrieval stack against closed-book and vanilla-RAG baselines.
The production system attains 74.5% gold-source retrieval — 14.5 points above
vanilla dense retrieval, with title-affinity re-ranking and lexical rescues
(citation lookup, name matching, deep reading of named judgments) contributing
roughly 7 and 9 points respectively — while over-refusing on only 5.3% (Sol) to
0.6% (gpt-4o) of answerable questions. The closed-book baseline refuses just 7
of 84 unanswerable questions, answering the rest from parametric memory — the
grounding-discipline gap the benchmark is designed to expose; grounded systems
refuse or honestly signal insufficiency on the large majority. A 24-item
stratified manual audit finds 87.5% correct answers and zero fabricated
citations: the grounded system's failure mode is mis-selection or silence,
never invention. We additionally document a query-rewrite-stage hallucination
(the rewrite model injecting a wrong-jurisdiction statute), a failure stage
named but unmeasured in prior work, and an infrastructure-failure episode that
masqueraded as a calibration collapse — motivating positional sanity checks in
LLM evaluation harnesses. The benchmark, harness, and corpus manifest are
released.

## 1 · Introduction

When a lawyer asks a machine what the law says, there are only two honest
outcomes: an answer grounded in a citable text, or an admission that the text
does not answer. Everything else is a hallucination wearing a confident voice.
Audits of commercial legal research tools have shown how common that third
outcome is: Magesh et al. (2024) found purpose-built, retrieval-augmented
products from the largest legal publishers hallucinating in 17–33% of
responses, and Dahl et al. (2024) documented the taxonomy of ways large
language models invent law. The stakes are not abstract. A fabricated citation
in a pleading is a sanctionable event; a fabricated answer to a layperson may
shape a decision they cannot afford to get wrong.

These audits, and the benchmarks that inform them, concentrate on
well-resourced jurisdictions. Pakistan — a mixed common-law system serving 240
million people, whose statutes and reported judgments are published in English
while its users increasingly ask their questions in Urdu or romanised Urdu —
has no benchmark spanning its statutes and case law. The nearest prior work,
LEGAL-UQA (Faisal & Yousaf, 2024), covers the Constitution alone: 619 QA pairs,
without statute-section or case-citation gold labels, without an unanswerable
subset, and in formal parallel Urdu rather than the code-switched Roman Urdu
that real queries use. India, by contrast, is comparatively well served
(IL-TUR, ILDC, IndicLegalQA, IL-PCSR), underscoring that the gap is
jurisdictional, not regional.

This paper makes four contributions:

1. **PakLegalQA** — the first citation-grounded QA benchmark for Pakistani
   law: 300 questions over 946 federal statutes (the Pakistan Code) and 2,503
   reported Lahore High Court judgments (2022–2026), with gold statute
   sections and neutral citations, seven question types including
   false-premise and unanswerable subsets, and a 60-question code-switched
   Roman-Urdu overlay.
2. **A refusal-calibration evaluation of a deployed system.** The system under
   study is not a laboratory pipeline but a production grounded-or-refuse RAG
   service with live users; to our knowledge no prior legal-QA evaluation
   measures a deployed system's abstention behaviour.
3. **Component ablations of a domain retrieval stack**, quantifying what
   category pooling, title-affinity re-ranking, and lexical rescues (citation
   lookup, name matching, deep reading of named judgments) each contribute
   beyond vanilla dense retrieval.
4. **Two methodological findings**: a hallucination at the query-generation
   stage of RAG — the retrieval-rewrite model injecting a wrong-jurisdiction
   statute into the search — which prior work names as a possible failure
   stage but does not measure; and an infrastructure-failure episode in which
   silent upstream API exhaustion produced a plausible-looking calibration
   collapse, detectable only by positional analysis — an argument for
   position- and time-aware sanity checks in any LLM evaluation harness.

## 2 · Related Work

**Hallucination in legal AI.** Magesh et al. (2024) audited proprietary legal
research tools with a preregistered query set and a correctness × groundedness
coding scheme that we adopt; Dahl et al. (2024) provide the underlying
taxonomy. Our setting differs in that the system is open to us: we can
attribute failures to retrieval, ranking, or generation, and intervene.

**Legal QA benchmarks.** LegalBench (Guha et al., 2023) and LexGLUE
(Chalkidis et al., 2022) established construction conventions for legal task
suites; COLIEE's yearly competitions and the LeCaRD/LeCaRDv2 datasets (Ma et
al., 2021; Li et al., 2024) cover case retrieval and entailment for Japanese
and Chinese law. For Pakistan, LEGAL-UQA (Faisal & Yousaf, 2024) is the
closest work and, notably, also originates in Lahore; PakLegalQA extends the
jurisdiction's coverage from the Constitution to statutes and case law, and
from answer strings to citation-level gold labels with an abstention axis.

**Citation-faithful generation and abstention.** ALCE (Gao et al., 2023)
supplies the citation precision/recall framing we adapt to statutes and
judgments. Self-RAG (Asai et al., 2023) and calibration studies (Kadavath et
al., 2022) treat refusal as a trainable, measurable behaviour; RefusalBench
(2026) evaluates selective refusal generatively. Recent legal-RAG evaluations
— LegalBench-RAG, Legal RAG Bench (Butler & Butler, 2026), ClaimRAG-LAW,
LegalCiteBench — measure retrieval precision and citation reliability on
common-law corpora; SearchFireSafety (Chae et al., 2026) is the closest
methodological neighbour, probing hierarchical statutory retrieval and safe
abstention in a single regulatory domain. None evaluates a deployed system,
and none covers Pakistan.

**Retrieval.** BM25 (Robertson & Zaragoza, 2009) and late-interaction dense
retrieval (Khattab & Zaharia, 2020) anchor the baseline families; SAILER (Li
et al., 2023) motivates structure-aware legal retrieval, which our
statute/caselaw pooling and judgment deep-reading instantiate in production.

## 3 · The PakLegalQA Benchmark

### 3.1 Corpus
The corpus is a frozen snapshot (`paklegalqa-corpus-v1`, SHA-256 manifest
released) of 3,449 documents: 946 federal statutes from the official Pakistan
Code and 2,503 reported judgments of the Lahore High Court, 2022–2026, each
carrying its neutral citation and official source URL. Two coverage gaps were
found and are disclosed: the Court Fees Act 1870 is absent, and the ingested
Limitation Act 1908 lacks its First Schedule. The ingested Pakistan Penal Code
reflects amendments at least through the Criminal Laws (Amendment) Act 2022
(XXXVII of 2022), verified via the decriminalised s.325 (attempted suicide).

### 3.2 Question types and construction
[Table: 7 types × counts — S-REC 80, S-INT 60, C-HOLD 50, C-FACT 20, TIME 20,
FALSE 20, UNANS 50; RU overlay 60.]

Questions were authored in six batches against three sourcing streams
(statute-derived, headnote/disposition-derived, and production-query-derived
phrasings), under a corpus-verification rule: no statute gold was recorded
unless the section's text was located in the ingested corpus (115 automated
checks across five verification waves), and no holding gold unless the
disposition sentence was read in the judgment's text (a regex harvester over
all chunks, since final pages are often signature blocks). False-premise items
encode realistic confusions (wrong year, wrong code, fictional sections);
unanswerable items span provincial law, other courts, current affairs, and
outcome predictions, so that the correct behaviour is refusal precisely
because the corpus — not the world — cannot answer.

The Roman-Urdu overlay re-asks 60 questions sampled across types in
code-switched romanised Urdu as users actually type ("Cheque bounce hone par
kya saza hai?"), sharing gold labels with their English twins so outcome
divergence isolates language handling.

### 3.3 Gold labels and verification status
Each item carries gold sources (statute title + section, or neutral citation),
short gold answer points for NLI-style scoring, an answerable flag, and
provenance metadata. All labels were authored by the first author and
corpus-verified automatically; independent legal review is planned and the
absence of it in v1 is stated as a limitation (§8).

## 4 · System Under Study

The evaluated system is Irshad AI Employee, a deployed multi-tenant RAG
service whose answering contract is *grounded or silent*: answers must come
from retrieved documents with page-cited sources, and the model must emit an
insufficiency sentinel — surfaced to users as an honest refusal — when the
context does not answer. The retrieval stack layers, over dense embeddings
(text-embedding-3-small) with a relevance floor and per-document diversity
caps: (i) statute/caselaw category pooling, so terse statutory prose is not
crowded out by discursive judgments; (ii) title-affinity re-ranking toward
acts the question names; (iii) lexical rescues — per-term title keyword
matching for party names, regex citation lookup ("2025 LHC 846") fetching the
cited judgment directly; and (iv) deep reading of named judgments at both
ends, because dispositions live in closing pages. A query-rewrite model
normalises Roman-Urdu and colloquial phrasings into English statutory
vocabulary before embedding. The production answer model is a reasoning-class
model ("Sol"); ablations use gpt-4o with the generator held constant within
every comparison.

## 5 · Experimental Setup

Six systems: PROD (full stack) and CB (closed-book, no retrieval, prose
refusals permitted) on the production model; PROD, DENSE (vanilla dense
retrieval — no pools, boosts, or rescues), −TITLE (full minus title affinity)
and −RESCUE (full minus lexical rescues and deep reading) on gpt-4o. Runs are
executed offline against the corpus snapshot through an evaluation harness
that bypasses tenant billing but not the real APIs; ablation switches are
evaluation-only context flags that production code paths never set, with a
regression test asserting the modes differ. Automatic metrics: answer/refusal
rates, refusal calibration (correct refusal on unanswerables vs over-refusal
on answerables), gold-source retrieval hit, and RU/EN twin outcome parity.
A manual correctness × groundedness coding pass (Magesh et al., 2024) over
the PROD and DENSE outputs [STATUS: pending] complements the automatic layer.

## 6 · Results

| System | Answered | Correct refusal (of 84 unans.) | Over-refusal | Gold-source hit | RU twins same-outcome |
|---|---|---|---|---|---|
| PROD (Sol) | 84.7% | 36/84 | 5.3% | 74.5% | 52/60 |
| Closed-book (Sol) | 81.7% | 7/84 | 16.4% | – | 60/60 |
| PROD (gpt-4o) | 89.7% | 35/84 | 0.6% | 74.5% | 59/60 |
| DENSE (gpt-4o) | 84.2% | 35/84 | 6.1% | 60.0% | 58/60 |
| − title affinity (gpt-4o) | 90.3% | 34/84 | 0.3% | 67.3% | 59/60 |
| − rescues/deep-read (gpt-4o) | 83.6% | 36/84 | 6.4% | 65.8% | 59/60 |

*Table 1: automatic metrics over all 360 items (2,160 evaluations). "Gold-source
hit": a required gold source appears among the answer's cited sources.
"Correct refusal" counts explicit refusals only; grounded non-answers and
premise corrections — which manual coding shows dominate the remainder on
unanswerable items — are analysed in §6.4.*

**R1 — Grounding discipline (PROD vs closed-book).** Grounded systems refuse
34–36 of the 84 unanswerable/false-premise items outright; the closed-book
baseline refuses 7, answering 77 from parametric memory — including Supreme
Court holdings, current-affairs facts, and provincial rules outside any
provided corpus. Notably, closed-book *is* honest where its ignorance is
self-evident (it declines specific LHC citation lookups); its failure is
answering questions whose premise requires a corpus it does not have. This is
the benchmark's central contrast: unanswerable items measure discipline, not
knowledge.

**R2 — What the retrieval stack buys.** The full stack retrieves a required
gold source for 74.5% of scorable items against 60.0% for vanilla dense
retrieval (+14.5 points). Removing title affinity costs 7.2 points of
gold-source accuracy while *raising* the answer rate slightly — it changes
what is cited, not whether the system speaks. Removing the lexical rescues
and deep reading costs 8.7 points of gold-source accuracy and 6.1 points of
answer rate (≈22 recovered answers), concentrated in the citation-lookup and
case-holding classes that embeddings cannot serve.

**R3 — Refusal calibration.** Over-refusal on answerable items is 5.3% for
the production reasoning model and 0.6% for gpt-4o. Per-type analysis places
the residual over-refusals overwhelmingly in scenario-phrased interpretation
questions — the class with the weakest gold-source retrieval — indicating the
remaining silence is retrieval-caused, not policy-caused.

**R4 — Roman-Urdu parity.** After the translation-first rewrite (§7, F4),
outcome parity between Roman-Urdu twins and their English counterparts is
59/60 (gpt-4o) and 52/60 (Sol). The benchmark's paired design is what makes
this measurable at all: every divergent pair is an actionable defect report.

**R5 — Model temperament.** Sol errs toward caution (higher over-refusal,
slightly lower RU parity); gpt-4o toward helpfulness (near-zero over-refusal,
softer refusal edge on unanswerables). Manual inspection (§6.4) shows gpt-4o's
extra "answers" on unanswerable items are largely honest: explicit
insufficiency statements and implicit premise corrections rather than
fabrications.

### 6.4 Manual audit
A stratified 24-item audit of PROD outputs (Magesh-style coding with the §7-F5
rubric extensions) finds 21/24 (87.5%) correct or better — including four
grounded non-answers and three implicit premise corrections — and 3/24
incorrect, all scenario questions where retrieval selected a plausible but
wrong provision (a sister doctrine, a neighbouring section, a different act).
**No fabricated citation appears anywhere in the audit**: every cited source
exists and is quoted faithfully. The grounded system's observed failure mode
is mis-selection or silence — never invention.

## 7 · Discussion: Findings from a Deployed System

**F1 — Query-rewrite hallucination.** The retrieval-rewrite model expanded
"punishment for dishonour of a cheque" into "…under the Negotiable
Instruments Act" — the *Indian* location of that offence — steering both dense
retrieval and title-affinity toward the wrong statute while PPC s.489-F sat
unretrieved. The fix (a jurisdiction guard with corrected worked examples) and
its measurement are, to our knowledge, the first documentation of
hallucination at the query-generation stage of a legal RAG pipeline.

**F2/F3 — What lexical rescues buy.** Neutral citations tokenize below
keyword-length floors and carry no embedding signal; party names collide
across thousands of titles; dispositions live in closing pages. Each defect
was found by a benchmark question and repaired by a rescue component; the
DENSE ablation quantifies their joint value.

**F4 — Cross-lingual regressions are silent.** A one-line prompt improvement
for jurisdiction correctness silently disabled Roman-Urdu translation; only
the benchmark's language twins exposed it. Prompt changes need cross-lingual
regression suites.

**F5 — The rubric needs an honesty category.** Real outputs forced two coding
refinements: implicit premise correction (answering the real statute behind a
false premise) and the grounded non-answer ("the documents do not state…"),
both of which are correct behaviours that naive answered/refused coding
miscounts.

**F6 — Infrastructure failures masquerade as findings.** Upstream credit
exhaustion mid-run caused embeddings to fail silently; the engine's honest
refusals then looked like a calibration collapse (windowed refusal rates:
10, 10, 13, 19, 60, 60 per 60 items). Positional sanity checks belong in
LLM evaluation harnesses; we release ours.

## 8 · Limitations
Single-annotator gold labels (corpus-verified, not lawyer-verified — planned
for v2); one High Court's reported judgments (2022–2026) and federal statutes
only; the evaluated system is built by the author (mitigated by releasing the
benchmark, harness, and manifest so anyone can rerun and extend); automatic
metrics validated by a bounded manual audit rather than exhaustive coding;
BM25/hybrid baselines deferred.

## 9 · Ethics Statement
Statutes and reported judgments are public documents; the benchmark
redistributes citations, sections, and short verified quotes with links to
official sources rather than bundling texts. Production-derived questions are
paraphrased phrasings with no user identifiers; raw logs are never released.
No copyrighted law-report headnotes (PLD/PLJ/CLC/SCMR) are used. The system
evaluated presents itself to users as research assistance, not legal advice.

## 10 · AI Assistance Disclosure
This research was conducted and drafted with substantial AI assistance
(Anthropic's Claude: experiment tooling, corpus verification scripts,
analysis, and prose drafting). All experiments, data, gold labels, and claims
were reviewed by the human author, who bears sole responsibility for the
content.

## References
[Numbered list — Magesh et al. 2024 (arXiv:2405.20362); Dahl et al. 2024
(arXiv:2401.01301); Gao et al. 2023 (arXiv:2305.14627); Lewis et al. 2020
(arXiv:2005.11401); Asai et al. 2023 (arXiv:2310.11511); Kadavath et al. 2022
(arXiv:2207.05221); Guha et al. 2023 (arXiv:2308.11462); Chalkidis et al.
2022 (arXiv:2110.00976); Khattab & Zaharia 2020 (arXiv:2004.12832); Robertson
& Zaragoza 2009 (FnTIR); Ma et al. 2021 (SIGIR); Li et al. 2024
(arXiv:2310.17609); Li et al. 2023 (arXiv:2304.11370); Faisal & Yousaf 2024
(arXiv:2410.13013); Joshi et al. 2024 (ACL, IL-TUR); Chae et al. 2026
(arXiv:2604.06173); Butler & Butler 2026 (arXiv:2603.01710); COLIEE 2024
overview.]
