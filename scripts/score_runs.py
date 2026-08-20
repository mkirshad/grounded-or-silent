#!/usr/bin/env python3
"""Score PakLegalQA run outputs against the benchmark's gold labels.

Pure Python (no Django): reads benchmark/all-360.jsonl + results/full/*.jsonl
and emits per-system, per-type tables. Automatic metrics only — answer-content
correctness (Magesh-style coding / NLI) is a separate, later pass. What this
scores:

  answer rate / refusal rate      per question type
  refusal calibration             correct-refusal on answerable:false items,
                                  over-refusal on answerable:true items
  gold-source retrieval hit       does any returned source match a gold source
                                  (statute title fuzzy-match, or the neutral
                                  citation prefix for judgments)?

Usage:
  python scripts/score_runs.py [results_dir] [benchmark_file]
Defaults: results/full and benchmark/all-360.jsonl relative to the repo root.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Words too generic to prove a statute-title match on their own.
_STOP = {
    "act", "ordinance", "order", "code", "the", "of", "and", "pakistan", "west",
    "1860", "1872", "1881", "1882", "1890", "1898", "1908", "1923", "1925",
    "1936", "1951", "1961", "1962", "1964", "1969", "1974", "1976", "1977",
    "1979", "1980", "1984", "1990", "1997", "1999", "2001", "2002", "2010",
    "2012", "2016", "2017",
}


def _title_tokens(title):
    return {t for t in re.findall(r"[a-z0-9]+", (title or "").lower()) if t not in _STOP}


def _gold_matches_source(gold, source_title):
    st = (source_title or "").lower()
    citation = gold.get("citation")
    if citation:
        # "2025 LHC 846" must match as a prefix of the judgment title.
        return st.startswith(citation.lower() + " ")
    want = _title_tokens(gold.get("title", ""))
    if not want:
        return False
    have = _title_tokens(source_title)
    # All distinctive words of the gold title must appear (subset match): the
    # corpus titles carry suffixes like "(PPC),1860 (Under Review)".
    return want <= have


# Closed-book rows carry refused=None; their refusals are prose. Conservative
# patterns — only unambiguous decline phrasings count, and only when they appear
# in the answer's opening (a caveat buried mid-answer is not a refusal).
_CB_REFUSAL = re.compile(
    r"(i do not know|i don't know|cannot verify|can't verify|unable to confirm|"
    r"not confident|do not have (reliable|verified|that) information|"
    r"نہیں معلوم|معلوم نہیں)",
    re.I,
)


def _cb_refused(answer):
    head = (answer or "")[:300]
    return bool(_CB_REFUSAL.search(head))


def load_benchmark(path):
    gold = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                row = json.loads(line)
                gold[row["id"]] = row
    return gold


def score_file(path, gold):
    per_type = defaultdict(lambda: defaultdict(int))
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            g = gold.get(r["question_id"])
            if g is None:
                continue
            t = g["type"]
            per_type[t]["n"] += 1
            refused = r.get("refused")
            if refused is None and r.get("mode") == "cb":
                refused = _cb_refused(r.get("answer"))
            answerable = g.get("answerable", True)
            if refused is True:
                per_type[t]["refused"] += 1
                if answerable:
                    per_type[t]["over_refusal"] += 1
                else:
                    per_type[t]["correct_refusal"] += 1
            elif refused is False:
                per_type[t]["answered"] += 1
                if not answerable:
                    per_type[t]["answered_unanswerable"] += 1
            # Retrieval hit: any gold source matched by any returned source.
            required = [s for s in g.get("gold_sources", []) if not s.get("optional")]
            if required and refused is not None:
                hit = any(
                    _gold_matches_source(gs, src.get("title", ""))
                    for gs in required
                    for src in (r.get("sources") or [])
                )
                per_type[t]["gold_retrieval_n"] += 1
                if hit:
                    per_type[t]["gold_retrieval_hit"] += 1
            rows.append((r, g))
    return per_type, rows


def pct(a, b):
    return f"{100.0 * a / b:5.1f}%" if b else "    –"


def main():
    results_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "results", "full")
    bench = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "benchmark", "all-360.jsonl")
    gold = load_benchmark(bench)

    for path in sorted(glob.glob(os.path.join(results_dir, "*.jsonl"))):
        system = os.path.splitext(os.path.basename(path))[0]
        per_type, rows = score_file(path, gold)
        total = sum(v["n"] for v in per_type.values())
        print(f"\n=== {system}  ({total} items)")
        print(f"{'type':8} {'n':>4} {'answered':>9} {'refused':>8} "
              f"{'corr-ref':>9} {'over-ref':>9} {'ans-unans':>10} {'gold-hit':>9}")
        agg = defaultdict(int)
        for t in ["S-REC", "S-INT", "C-HOLD", "C-FACT", "TIME", "FALSE", "UNANS", "RU"]:
            v = per_type.get(t)
            if not v:
                continue
            for k, val in v.items():
                agg[k] += val
            print(f"{t:8} {v['n']:>4} {pct(v['answered'], v['n']):>9} "
                  f"{pct(v['refused'], v['n']):>8} "
                  f"{pct(v['correct_refusal'], v['n']):>9} "
                  f"{pct(v['over_refusal'], v['n']):>9} "
                  f"{pct(v['answered_unanswerable'], v['n']):>10} "
                  f"{pct(v['gold_retrieval_hit'], v['gold_retrieval_n']):>9}")
        print(f"{'ALL':8} {agg['n']:>4} {pct(agg['answered'], agg['n']):>9} "
              f"{pct(agg['refused'], agg['n']):>8} "
              f"{pct(agg['correct_refusal'], agg['n']):>9} "
              f"{pct(agg['over_refusal'], agg['n']):>9} "
              f"{pct(agg['answered_unanswerable'], agg['n']):>10} "
              f"{pct(agg['gold_retrieval_hit'], agg['gold_retrieval_n']):>9}")

        # The paper's RU table: EN-vs-RU outcome pairs via twin_of.
        by_id = {r["question_id"]: r for r, _ in rows}
        pairs = same = ru_worse = ru_better = 0
        for r, g in rows:
            twin = g.get("twin_of")
            if not twin or twin not in by_id:
                continue
            ru_ref, en_ref = r.get("refused"), by_id[twin].get("refused")
            if ru_ref is None or en_ref is None:
                continue
            pairs += 1
            if ru_ref == en_ref:
                same += 1
            elif ru_ref and not en_ref:
                ru_worse += 1
            else:
                ru_better += 1
        if pairs:
            print(f"RU twins: {pairs} pairs | same outcome {same} | "
                  f"RU refused where EN answered {ru_worse} | reverse {ru_better}")


if __name__ == "__main__":
    main()
