#!/usr/bin/env python3
"""Merge the clean head of prod-sol with the rerun tail into prod-sol.jsonl.

The original prod-sol run was contaminated from index 225 (S-REC-226) onward by
OpenAI credit exhaustion: embedding calls failed silently and every question
refused with empty sources. The head (225 rows) is kept; the tail comes from
the post-top-up rerun. The contaminated original is preserved as
prod-sol-contaminated.jsonl for the incident record.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FULL = os.path.join(ROOT, "results", "full")


def load(name):
    path = os.path.join(FULL, name)
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


head = load("prod-sol-clean-head.jsonl")
tail = load("prod-sol-tail.jsonl")
suspect = set(
    open(os.path.join(FULL, "prod-sol-suspect-ids.txt")).read().strip().split(",")
)

tail_ids = {r["question_id"] for r in tail}
missing = suspect - tail_ids
assert not missing, f"tail rerun is missing {len(missing)} ids: {sorted(missing)[:5]}"

# Keep benchmark order: head ids first, then tail in suspect-list order.
order = open(os.path.join(FULL, "prod-sol-suspect-ids.txt")).read().strip().split(",")
by_id = {r["question_id"]: r for r in tail}
merged = head + [by_id[i] for i in order]
assert len(merged) == 360 and len({r["question_id"] for r in merged}) == 360

os.replace(
    os.path.join(FULL, "prod-sol.jsonl"),
    os.path.join(FULL, "prod-sol-contaminated.jsonl"),
)
with open(os.path.join(FULL, "prod-sol.jsonl"), "w", encoding="utf-8") as fh:
    for r in merged:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print("merged 360 rows -> prod-sol.jsonl (original kept as prod-sol-contaminated.jsonl)")
