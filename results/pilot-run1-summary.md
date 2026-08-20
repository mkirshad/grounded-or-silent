# Pilot run 1 — 20 questions, system=prod (Sol), 2026-08-20

Raw: `pilot-run1.jsonl`. 13 answered / 7 refused / 0 errors. Median latency ~14.4s.
Coding below is provisional (Magesh-style correct/incorrect/refusal × grounded),
pending advocate verification of gold labels.

## Per-question outcomes

| id | outcome | provisional coding | note |
|---|---|---|---|
| S-REC-001 cheque | answered | correct, grounded | ONLY after today's rewrite fix (see finding F1) |
| S-REC-002 theft | answered | to verify | |
| S-REC-003 breach of trust | answered | to verify | |
| S-REC-004 defamation | answered | to verify | |
| S-REC-005 qatl-e-amd | answered | to verify | |
| S-INT-006 bail | answered | correct, grounded | matches live /ask behaviour |
| S-INT-007 pre-arrest bail | answered | to verify | |
| S-INT-008 FIR | answered | to verify | |
| C-HOLD-009 Rizwan holding | answered | honest partial | right case retrieved; retrieved chunks lack the holding → said so, gave case no./judge/bench/date (finding F3) |
| C-FACT-010 judge of 2025 LHC 846 | refused | over-refusal | citation-number lookup fails retrieval entirely (finding F2) |
| C-FACT-011 year of 2026 LHC 4593 | answered | correct | |
| TIME-012 limitation promissory note | refused | expected corpus gap | Limitation Act First Schedule missing — probe behaved as designed |
| FALSE-013 Cyber Crimes Act 1995 | answered | implicit correction | answered from the REAL act (PECA 2016 s.17, SIM issuance); did not name the fictional act. Rubric decision needed: implicit vs explicit premise correction (finding F5) |
| FALSE-014 PPC s.999 | refused | correct refusal | |
| UNANS-015 SC Panama | refused | correct refusal | |
| UNANS-016 paracetamol | refused | correct refusal | |
| UNANS-017 NEPRA tariffs | answered | grounded non-answer | said explicitly "documents do not state current tariffs; they only establish NEPRA determines rates". Honest insufficiency — rubric needs a category between answer and refusal (finding F5) |
| RU-018 cheque (Roman Urdu) | answered | correct, grounded | matches English twin after F1 fix |
| RU-019 bail (Roman Urdu) | refused | over-refusal | English twin S-INT-006 ANSWERED (finding F4) |
| RU-020 theft (Roman Urdu) | refused | over-refusal | English twin S-REC-002 ANSWERED; PPC was retrieved — generation refused (finding F4) |

Provisional score: refusal set (FALSE+UNANS, n=5): 4/5 handled correctly, 1
grounded non-answer (arguably correct). Answerable set (n=15): 12 answered,
3 over-refusals (2 of them Roman Urdu, 1 citation lookup).

## Findings (each = paper material + product work item)

**F1 — Query-rewrite hallucination (FIXED today).** The gpt-4o retrieval rewrite
expanded "punishment for dishonour of a cheque" to "...under Negotiable
Instruments Act", injecting the *Indian* location of the offence from parametric
knowledge. The injected act name then (a) steered dense retrieval to banking
statutes and (b) fed the title-affinity boost, actively rewarding the wrong act.
PPC 489-F sat 4th in the candidate pool and never reached the context. Fix:
jurisdiction guard + corrected worked example in the rewrite prompt; verified
end-to-end (answer now cites 489-F, 3 years/fine/both). Paper framing:
hallucination at the *query-generation* stage of RAG — a stage Magesh et al.'s
Figure 3 names but does not measure.

**F2 — Neutral citations are unretrievable.** "2025 LHC 846" tokenises to terms
of ≤3 chars ("lhc", "846"), which the title-keyword rescue deliberately excludes,
and embeddings carry no signal for citation numbers — so a lookup any lawyer
would type fails. Product fix (todo): regex-detect `\d{4}\s+LHC\s+\d+` and do a
direct title lookup, injecting that document's chunks. Cheap, high-value.

**F3 — Holding questions read the wrong pages.** The right judgment was
retrieved (top source), but seq-0/header chunks don't contain the holding; the
unscoped per-doc cap (3) stops before the operative paragraphs. The system was
honest about it. Product idea: when a single judgment dominates relevance,
deepen its per-doc allowance (mirror of the scoped-folder rule).

**F4 — Roman-Urdu generation gap (headline finding).** 2 of 3 RU twins refused
where English answered — and for RU-020 the PPC was successfully retrieved, so
the failure is at GENERATION: the answer model refuses on code-switched input
despite adequate English context. Retrieval translation works; generation does
not. Product fix candidate: give the answer model the English-normalised
question alongside the original, with an instruction to answer in the user's
language. Measure before/after — this is exactly the paper's RU-vs-EN table.

**F5 — Rubric gaps found by real outputs.** Need coding rules for
(a) implicit premise correction (FALSE-013), (b) "grounded non-answer" — an
answer that explicitly states the corpus cannot answer (UNANS-017). Proposed:
both count as non-hallucinating; (b) scores as correct abstention.

## Cost/ops
Run consumed ~40+ Sol-weighted credits on workspace 3 and ~20 QuestionLog rows
(channel portal) — purge as usual. Latencies 10–19s per question.

## Post-pilot fixes (2026-08-20, same day — see `pilot-fix2.jsonl`)

- **F2 FIXED**: `_citation_hits` regex-detects neutral citations and fetches the
  cited judgment's leading chunks directly (prefix-bounded, 846 ≠ 8460).
  C-FACT-010 now answers: Justice Muhammad Jawad Zafar, official PDF link.
  3 regression tests added (`apps/library/tests/test_citation_lookup.py`).
- **F4 FIXED — and the root cause is itself a finding**: the F1 prompt fix had
  REGRESSED Urdu translation (the model obeyed the newest instruction and
  stopped translating: "chori ki saza" searched as-is). Rewrite prompt
  restructured into numbered rules, translation first and unconditional.
  RU-019/RU-020 now answer IN Roman Urdu with grounded content. Paper note:
  prompt-patch regressions in the query-generation stage are silent and
  cross-lingual — a benchmark with language twins is what catches them.
- **F3 FIXED (2026-08-20 evening, commit 26a2e3b; see `pilot-fix4.jsonl`)** —
  three connected changes: (a) citation lookup fetches BOTH ends of the judgment
  and named documents get a relaxed per-doc cap; (b) the title-keyword rescue
  queries per term (the old single OR-query sliced 60 rows that common words
  flooded before "rizwan" surfaced); (c) institutional words (court, lahore,
  state, justice) no longer count as title matches. The deep-read triggers on
  the top-RANKED judgment sharing the question's distinctive title words —
  party names alone are ambiguous (several real Muhammad Rizwans in the corpus;
  judge names put "Muhammad" in thousands of titles), a finding in itself for
  the paper's case-identification discussion. C-HOLD-009 now answers with the
  actual disposition: bail granted, PKR 1,000,000 bonds, outside the
  prohibitory clause, detention since 7 Nov 2024.
- RU-020 half-win recorded: answers in Urdu but from s.411 (receiving stolen
  property) because s.378/379's chunk still doesn't rank — retrieval
  granularity finding stays live for the full benchmark.
- Both commits pushed: 3911423 (F1 + harness), c4e3a4d (F2 + F4). Full backend
  suite green.
