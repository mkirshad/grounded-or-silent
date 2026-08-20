#!/usr/bin/env bash
# Rerun the credit-exhaustion-contaminated tail of prod-sol (135 ids from
# S-REC-226 onward; see PROGRESS.md 2026-08-21). Run AFTER the main driver's
# DONE marker, so the workspace model is back on the platform default (Sol):
#   wsl bash -lc 'bash /mnt/f/IrshadOS/research/grounded-or-silent/scripts/rerun_prodsol_tail.sh'
set -u
PY=/home/mkirshad/aievenv/bin/python
BACKEND=/mnt/f/Android-Projects/AutoCareAI/backend
BASE=/mnt/f/IrshadOS/research/grounded-or-silent
IDS=$(cat "$BASE/results/full/prod-sol-suspect-ids.txt")
cd "$BACKEND"
echo "==== $(date -u +%H:%M:%S) rerunning prod-sol tail (135 ids)"
"$PY" manage.py run_paklegalqa --file "$BASE/benchmark/all-360.jsonl" \
  --out "$BASE/results/full/prod-sol-tail.jsonl" \
  --company-id 3 --system prod --ids "$IDS" 2>&1 | grep -vE 'severity|FutureWarning|warnings.warn' | tail -1
echo "==== tail rerun done; merge with: python scripts/merge_prodsol.py"
