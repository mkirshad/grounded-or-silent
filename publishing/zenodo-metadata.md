# Zenodo record — draft metadata (DOI 10.5281/zenodo.22037183)

Paste-ready values for https://zenodo.org/uploads/22037183. Items marked
[UPDATE-AT-PUBLISH] get final values when the paper is done.

## Required fields (clears the 3 errors)

**Resource type:** Publication → Preprint

**Title:**
Grounded or Silent: Citation-Faithful Legal Question Answering for Pakistani Law

**Publication date:** 2026-08-21  [UPDATE-AT-PUBLISH to the actual publish date]

**Authors/Creators:**
- Family name: Irshad · Given names: Muhammad Kashif
  Affiliation: IrshadOS, Lahore, Pakistan
  (add ORCID if available — free at orcid.org, strongly recommended before publish)

## Description (abstract — numbers in [brackets] finalize after the runs)

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
The production system correctly refuses [X] of 84 unanswerable questions while
over-refusing on only [Y]% of answerable ones; retrieval rescues (citation
lookup, title matching, deep reading of named judgments) account for [Z]
recovered answers versus vanilla dense retrieval; and the closed-book baseline
answers [W] of the unanswerable questions from parametric memory — the
grounding-discipline gap the benchmark is designed to expose. We additionally
document a query-rewrite-stage hallucination (the rewrite model injecting a
wrong-jurisdiction statute), a failure stage named but unmeasured in prior
work, and an infrastructure-failure episode that masqueraded as a calibration
collapse — motivating positional sanity checks in LLM evaluation harnesses.
The benchmark, evaluation harness, and corpus manifest are released.

LIMITATION: gold labels were authored and corpus-verified by a single
annotator; independent legal review is planned for a future version.

AI ASSISTANCE DISCLOSURE: this research was conducted and drafted with
substantial AI assistance (Anthropic's Claude, used for experiment tooling,
analysis, and prose drafting). All experiments, data, and claims were
reviewed and are the responsibility of the human author.

## License / Copyright
- License: Creative Commons Attribution 4.0 International (already selected)
- Copyright: © 2026 Muhammad Kashif Irshad

## Recommended information

**Keywords:** legal question answering; retrieval-augmented generation;
benchmark; Pakistani law; refusal calibration; hallucination; citation
grounding; low-resource jurisdictions; Roman Urdu; legal NLP

**Languages:** English

**Version:** 0.1.0-draft  [UPDATE-AT-PUBLISH → 1.0.0]

**Publisher:** Zenodo (default)

## Related works  [UPDATE-AT-PUBLISH]
- "Is supplemented by" → https://github.com/mkirshad/grounded-or-silent
  (URL type; repo is PRIVATE today — make it public at publish time, or drop
  this entry)
- "Is identical to" → https://irshados.com/ebooks/<final-slug>/ (URL type;
  add once the ebook page slug exists)

## Software section
- Repository URL: https://github.com/mkirshad/grounded-or-silent
- Programming language: Python
- Development status: Active

## Files
Zenodo requires at least one file to save past validation. Until the paper
PDF exists, upload the current PakLegalQA-design.md (or a placeholder PDF of
it) — files CAN be replaced freely before first publish, never after.
IMPORTANT: do NOT press Publish until the final paper.pdf is uploaded; the
DOI registers on publish and files freeze.

## Publication pipeline (agreed 2026-08-21)
1. Paper drafted to match the Sabbath Pond Test paper's format
   (irshados.com/ebooks/islamic-banking-sabbath-pond-test-reevaluation/).
2. Published as an ebook entry on irshados.com/ebooks/ + paper.pdf in the
   IrshadOS-Main-Site repo, with the DOI 10.5281/zenodo.22037183 printed on
   the paper and page, and an AI-assistance indicator on both.
3. Zenodo record completed and published with the same PDF.
