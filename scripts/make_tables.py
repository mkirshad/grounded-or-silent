#!/usr/bin/env python3
"""Emit the paper's comparison tables from results/full/*.jsonl.

Writes results/summary.md (markdown tables ready for the paper draft) and
results/coding-sheet.csv (one row per prod-system item for the manual
Magesh-style correctness/groundedness pass).

Only canonical run files are read (SYSTEMS below) — head/tail/contaminated
artifacts from the credit-exhaustion incident are ignored.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score_runs import _cb_refused, _gold_matches_source, load_benchmark  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, "results", "full")

SYSTEMS = [
    ("prod-sol", "PROD (Sol)"),
    ("cb-sol", "Closed-book (Sol)"),
    ("prod-4o", "PROD (gpt-4o)"),
    ("dense-4o", "DENSE (gpt-4o)"),
    ("abl-title-4o", "– title affinity"),
    ("abl-rescue-4o", "– rescues/deep-read"),
]

MAIN_TYPES = ["S-REC", "S-INT", "C-HOLD", "C-FACT", "TIME", "FALSE", "UNANS"]


def load_run(tag):
    path = os.path.join(FULL, tag + ".jsonl")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def effective_refused(r):
    refused = r.get("refused")
    if refused is None and r.get("mode") == "cb":
        refused = _cb_refused(r.get("answer"))
    return refused


def stats(rows, gold):
    s = {"n": 0, "answered": 0, "refused": 0, "corr_ref": 0, "over_ref": 0,
         "ans_unans": 0, "gr_n": 0, "gr_hit": 0, "ru_pairs": 0, "ru_same": 0}
    by_id = {r["question_id"]: r for r in rows}
    for r in rows:
        g = gold.get(r["question_id"])
        if not g:
            continue
        s["n"] += 1
        refused = effective_refused(r)
        answerable = g.get("answerable", True)
        if refused:
            s["refused"] += 1
            s["corr_ref" if not answerable else "over_ref"] += 1
        elif refused is False:
            s["answered"] += 1
            if not answerable:
                s["ans_unans"] += 1
        required = [x for x in g.get("gold_sources", []) if not x.get("optional")]
        if required and r.get("mode") != "cb":
            s["gr_n"] += 1
            if any(_gold_matches_source(gs, src.get("title", ""))
                   for gs in required for src in (r.get("sources") or [])):
                s["gr_hit"] += 1
        twin = g.get("twin_of")
        if twin and twin in by_id:
            s["ru_pairs"] += 1
            if effective_refused(r) == effective_refused(by_id[twin]):
                s["ru_same"] += 1
    return s


def pct(a, b):
    return f"{100.0 * a / b:.1f}%" if b else "–"


def main():
    gold = load_benchmark(os.path.join(ROOT, "benchmark", "all-360.jsonl"))
    lines = ["# PakLegalQA — automatic-metric summary", "",
             "| System | n | Answered | Correct refusal (of 84 unans.) | Over-refusal | Gold-source hit | RU twins same-outcome |",
             "|---|---|---|---|---|---|---|"]
    coding_rows = []
    for tag, label in SYSTEMS:
        rows = load_run(tag)
        if rows is None:
            lines.append(f"| {label} | – | (run missing) | | | | |")
            continue
        s = stats(rows, gold)
        unans_total = sum(1 for g in gold.values() if not g.get("answerable", True))
        lines.append(
            f"| {label} | {s['n']} | {pct(s['answered'], s['n'])} | "
            f"{s['corr_ref']}/{unans_total} | {pct(s['over_ref'], s['n'])} | "
            f"{pct(s['gr_hit'], s['gr_n'])} | {s['ru_same']}/{s['ru_pairs']} |"
        )
        if tag in ("prod-sol", "prod-4o", "dense-4o", "cb-sol"):
            for r in rows:
                g = gold[r["question_id"]]
                coding_rows.append({
                    "system": tag,
                    "id": r["question_id"],
                    "type": g["type"],
                    "answerable": g.get("answerable", True),
                    "question": r["question"],
                    "refused": effective_refused(r),
                    "answer": (r.get("answer") or "")[:1500],
                    "sources": "; ".join(s0.get("title", "")[:60] for s0 in (r.get("sources") or [])[:4]),
                    "gold": json.dumps(g.get("gold_sources", []), ensure_ascii=False),
                    "gold_points": " | ".join(g.get("gold_answer_points", [])),
                    "coding_correctness": "",   # correct / incorrect / refusal (manual)
                    "coding_groundedness": "",  # grounded / misgrounded / ungrounded (manual)
                })
    out_md = os.path.join(ROOT, "results", "summary.md")
    with open(out_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    out_csv = os.path.join(ROOT, "results", "coding-sheet.csv")
    with open(out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(coding_rows[0].keys()))
        w.writeheader()
        w.writerows(coding_rows)
    print("wrote", out_md, "and", out_csv, f"({len(coding_rows)} coding rows)")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
