# Manual coding sample — PROD (gpt-4o), n=24, stratified, seed 42

Coded 2026-08-21 by the author with AI assistance (disclosed in §10 of the
paper): Magesh-style correctness, with the F5 rubric extensions (implicit
premise correction and grounded non-answer count as correct behaviours).

## Verdicts

| id | verdict | note |
|---|---|---|
| S-REC-030 arrest w/o warrant | correct, grounded | CrPC top source |
| S-REC-004 defamation | correct, grounded | s.499 definition + Defamation Ord. |
| S-REC-080 customs smuggling | correct (partial), grounded | answers via an offences-table provision; responsive |
| S-REC-076 succession certificate | correct, grounded | |
| S-REC-063 ATA financing | grounded non-answer | honest: found 11-H–11-K, says penalties not in extract |
| S-REC-034 confession to police | correct+, grounded | adds the ATA exception — better than gold |
| S-INT-322 acid survivor | **incorrect** | answered from Protection of Pakistan Act 2014, not PPC 336-B — scenario-retrieval miss |
| S-INT-091 249-A acquittal | correct, grounded | |
| S-INT-318 ending a lease | **incorrect (off-section)** | cites s.109 transfer, not s.111 determination modes |
| S-INT-332 exchange of plots | correct, grounded | s.118 exact |
| S-INT-238 joint liability | **incorrect (doctrine swap)** | answered s.149 unlawful assembly (needs 5 members) for a 3-person s.34 scenario |
| C-HOLD-102 maintenance | correct, grounded | exact holding |
| C-HOLD-281 MAG vs LDA | correct, grounded | disposition + dates |
| C-HOLD-216 Gillani | correct, grounded | + policy direction detail |
| C-HOLD-050 Abdus Salam ICA | correct, grounded | all three gold points |
| C-HOLD-049 Meher Ali | correct, grounded | all three gold points, dates exact |
| C-FACT-052 / 107 / 108 | correct ×3, grounded | judges/bench exact (108 names both judges) |
| FALSE-259 FCA 1984 | correct (implicit correction) | answers as "Family Courts Act, 1964" + khula s.10(5) |
| FALSE-013 Cyber Crimes Act 1995 | correct (implicit correction) | answers from PECA 2016 s.14, flags the SIM gap |
| FALSE-182 CrPC-302 mix-up | correct (correction) | states murder is PPC 302; honest about punishment text |
| UNANS-165 nikah fee | correct (grounded non-answer) | "fees shall be prescribed" — amount honestly absent |
| UNANS-341 Hajj policy | correct (grounded non-answer) | uses Hajj & Umrah Act 2024 framework, refuses the quota |

## Summary
- **21/24 correct or better (87.5%)**, including 4 honest grounded non-answers
  and 3 implicit premise corrections — validating the F5 rubric categories.
- **3/24 incorrect — all S-INT scenario questions**, and all three are
  retrieval misses to a *plausible but wrong* provision (wrong act, wrong
  section, sister doctrine). Consistent with S-INT's lowest gold-source hit
  rate in the automatic metrics: scenario phrasing is where retrieval loses
  the governing text.
- **0 fabricated citations in the sample** — every cited source exists; errors
  are selection errors, never inventions. This is the central claim's shape:
  the failure mode of a grounded system is mis-selection or silence, not
  fabrication.
