# Grounded or Silent: Citation-Faithful Legal Question Answering for Pakistani Law

**PakLegalQA** — the first citation-grounded question-answering benchmark for
Pakistani law — and a refusal-calibration evaluation of a deployed
grounded-or-refuse legal AI system.

- 📄 **Paper (preprint v1, August 2026):**
  [irshados.com/ebooks/grounded-or-silent-paklegalqa](https://irshados.com/ebooks/grounded-or-silent-paklegalqa/)
  · [PDF](https://irshados.com/ebooks/grounded-or-silent-paklegalqa/paper.pdf)
- 🔗 **DOI:** [10.5281/zenodo.22037183](https://doi.org/10.5281/zenodo.22037183)
- ✍️ **Author:** Muhammad Kashif Irshad (IrshadOS, Lahore, Pakistan) ·
  ORCID [0009-0008-9161-9875](https://orcid.org/0009-0008-9161-9875)
- ⚖️ **System under study:** [Irshad AI Employee](https://irshados.com/apps/irshad-ai-employee/) —
  a deployed grounded-or-refuse RAG service (ask it a legal question at
  [irshados.com/ask](https://irshados.com/ask))

## The benchmark

360 items over a frozen corpus of **946 federal statutes** (Pakistan Code) and
**2,503 reported Lahore High Court judgments** (2022–2026):

| Type | Count | Description |
|---|---|---|
| S-REC | 80 | Statute recall — punishments, definitions, procedures |
| S-INT | 60 | Interpretation — real-life scenarios mapped to provisions |
| C-HOLD | 50 | Case holdings — what a named judgment decided |
| C-FACT | 20 | Judgment facts — judge, bench, dates |
| TIME | 20 | Amendment- and currency-sensitive probes |
| FALSE | 20 | False premises — wrong years, wrong codes, fictional sections |
| UNANS | 50 | Unanswerable from the corpus — refusal is the only correct output |
| RU | 60 | Code-switched Roman-Urdu overlay, twinned with English items |

Every statute gold label was verified against the corpus text before being
recorded; every case-holding label comes from a disposition sentence read in
the judgment itself. Labels are single-annotator in v1 (stated limitation);
independent legal review is planned for v2.

## Headline results (automatic metrics, 2,160 evaluations)

| System | Answered | Correct refusal (of 84 unans.) | Over-refusal | Gold-source hit |
|---|---|---|---|---|
| PROD (full stack, Sol) | 84.7% | 36/84 | 5.3% | 74.5% |
| Closed-book (Sol) | 81.7% | 7/84 | 16.4% | – |
| PROD (gpt-4o) | 89.7% | 35/84 | 0.6% | 74.5% |
| DENSE / vanilla RAG (gpt-4o) | 84.2% | 35/84 | 6.1% | 60.0% |
| − title affinity | 90.3% | 34/84 | 0.3% | 67.3% |
| − rescues/deep-read | 83.6% | 36/84 | 6.4% | 65.8% |

A 24-item stratified manual audit found **87.5% correct answers and zero
fabricated citations** — the grounded system's failure mode is mis-selection
or silence, never invention.

## Repository layout

| Path | Contents |
|---|---|
| `benchmark/` | The 360 PakLegalQA items as JSONL (`all-360.jsonl` = combined) |
| `corpus/manifest-v1.jsonl` | Frozen corpus manifest: 3,449 documents with SHA-256 checksums, titles, official source URLs |
| `corpus/*.py` | Gold-label verification and disposition-harvesting scripts (run inside the system's Django shell) |
| `results/` | Run summaries, the manual-coding sample, and the incident record; per-question outputs regenerate via the harness |
| `scripts/` | Experiment driver, scoring (`score_runs.py`), tables (`make_tables.py`) |
| `paper/` | Paper source (markdown) |
| `publishing/` | PDF/docx build pipeline and Zenodo metadata |
| `PakLegalQA-design.md` | The benchmark's design document |
| `PROGRESS.md` | Dated research log (including the findings' discovery order) |

The evaluation harness itself is a management command
(`run_paklegalqa`) in the evaluated system's backend; ablation switches are
evaluation-only context flags that production code never sets.

## Citing

> Irshad, Muhammad Kashif. "Grounded or Silent: Citation-Faithful Legal
> Question Answering for Pakistani Law." IrshadOS Research, 2026.
> DOI: 10.5281/zenodo.22037183.

## License and AI assistance

Paper and benchmark released under **CC BY 4.0**. Statute and judgment texts
are not bundled — the manifest carries citations, checksums, and official
source URLs. This research was conducted and drafted with substantial AI
assistance (Anthropic's Claude), reviewed throughout by the human author, who
bears sole responsibility for the content.
