# Venue plan — getting PakLegalQA peer-reviewed

Written 2026-08-21, after the Zenodo publish (DOI 10.5281/zenodo.22037183).
This is the working plan; tick items as they happen and date every change.

## Where things stand

- Preprint is PUBLISHED: irshados.com/ebooks/grounded-or-silent-paklegalqa/ +
  Zenodo DOI + public GitHub repo. Preprints do not block any venue below.
- NLLP 2026 (the natural first-choice workshop, EMNLP Budapest, 28 Oct 2026)
  was MISSED: direct-submission deadline was extended to 18 Aug 2026 and we
  published on 21 Aug. The 27 Aug route requires existing ARR reviews or an
  EMNLP rejection — not available. Verified 2026-08-21 from
  https://nllpw.org/workshop/call/.

## Target 1 — JURIX 2026 (ACTIVE, deadlines imminent)

39th International Conference on Legal Knowledge and Information Systems,
8–10 December 2026, Toulouse, France. Proceedings: IOS Press FAIA, gold open
access. Review is SINGLE-BLIND — the public DOI/site/repo are evidence, not a
problem. "Datasets and other resources with high potential to support future
AI & Law research" are explicitly in scope — PakLegalQA's exact category.
CFP: https://www.irit.fr/jurix2026/call-for-papers/
Submission: https://easychair.org/conferences?conf=jurix2026

Deadlines (AoE):
- [ ] **28 Aug 2026** — abstract submission (recommended, non-binding).
      USER: create EasyChair account, enter title + abstract. ~15 minutes.
- [ ] **before 5 Sep** — email organizers asking whether remote presentation
      is allowed (Toulouse in December = Schengen visa weeks + travel cost;
      decide long/short/poster partly on this answer). USER.
- [ ] **now → 5 Sep** — advocate outreach: 1–2 Bar contacts to spot-check
      30–40 gold labels (offer acknowledgment or co-authorship). Even a
      partial expert-checked sample is the single biggest strengthener.
      If it doesn't land in time, submit anyway with verification disclosed
      as in-progress. USER recruits; Claude prepares the verification sheet.
- [ ] **by 3 Sep** — reshape paper into IOS Press format as a LONG paper
      (max 10 pages excl. acknowledgements/references; short = 5, poster = 2).
      Template: https://www.iospress.com/book-article-instructions
      If time allows: expand manual audit beyond n=24; add BM25 baseline.
      CLAUDE, on user's go.
- [ ] **5 Sep 2026** — full paper submission on EasyChair. USER presses submit.
- Decision expected in the autumn; at least one author must register and
  present if accepted.

Fallback ladder if long-paper scope or travel doesn't work:
long paper → short paper (5pp) → poster (2pp) → withdraw and hold for NLLP 2027.

## Target 2 — NLLP 2027 (the v2 paper)

Workshop co-located with EMNLP; deadline expected ~August 2027 (2026's was
11→18 Aug; ARR commitment 27 Aug). Double-blind, ACL two-column template,
OpenReview. Watch https://nllpw.org/ from ~May 2027.

The v2 paper must differ enough from JURIX v1 to be its own contribution:
- [ ] full advocate verification (30% per category per design protocol)
- [ ] BM25 + HYB baselines (deferred from v1)
- [ ] expanded manual audit (~60–100 items)
- [ ] F6 (RU per-question variance) and F7 (rewrite-refusal) studied properly
- [ ] more High Courts if corpus growth allows

## Target 3 — journal (later, not now)

*Artificial Intelligence and Law* (Springer) after workshop/conference
feedback is incorporated. 6–18 month process; do not go there with v1 as-is.

## Standing warnings

- Predatory journals WILL email inviting submission for a fee once the DOI
  circulates. The venues worth having (NLLP, JURIX, ICAIL, AI & Law) never
  charge submission fees. Delete those emails.
- Any venue submission must disclose the preprint and the self-evaluation
  (author evaluates his own deployed system) — both already disclosed in the
  paper; keep them disclosed in every reshaped version.

## Later — derivative works (after JURIX submission, 2026-08-21 idea)

- Course (YouTube free + Udemy paid, one build): "Build and Evaluate a
  Citation-Grounded AI Assistant — RAG for Legal/Regulated Domains", paper as
  spine, F1–F7 as lessons, public repo as materials, stats screenshots as
  evidence slides, credit-exhaustion incident as a lesson. ElevenLabs for
  lesson narration (Udemy requires AI-voice disclosure; check current policy),
  user's own voice for course/section intros. Stronger after peer review.
- LinkedIn long-form article "how the benchmark was built" — after the
  announcement post has run.
