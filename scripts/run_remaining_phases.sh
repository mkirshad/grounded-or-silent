#!/usr/bin/env bash
# Resume the PakLegalQA experiment AFTER OpenAI credits are topped up.
# prod-sol completed before the credit exhaustion; this runs the other 5 phases.
#   wsl bash -lc 'bash /mnt/f/IrshadOS/research/grounded-or-silent/scripts/run_remaining_phases.sh'
set -u
PY=/home/mkirshad/aievenv/bin/python
BACKEND=/mnt/f/Android-Projects/AutoCareAI/backend
BENCH=/mnt/f/IrshadOS/research/grounded-or-silent/benchmark/all-360.jsonl
OUT=/mnt/f/IrshadOS/research/grounded-or-silent/results/full
mkdir -p "$OUT"
cd "$BACKEND"

run() {
  sys="$1"; tag="$2"
  echo "==== $(date -u +%H:%M:%S) starting $sys ($tag)"
  "$PY" manage.py run_paklegalqa --file "$BENCH" --out "$OUT/$tag.jsonl" \
    --company-id 3 --system "$sys" 2>&1 | grep -vE 'severity|FutureWarning|warnings.warn' | tail -1
}

set_model() {
  "$PY" manage.py shell -c "
from apps.assistant.services import get_or_create_employee
from apps.tenants.models import Company
e = get_or_create_employee(Company.objects.get(id=3))
e.model = '$1'
e.save(update_fields=['model'])
print('workspace-3 answer model:', repr(e.model))
"
}

echo "==== resume start $(date -u)"
set_model ""            # platform default = Sol
run cb   cb-sol

set_model gpt-4o
run prod       prod-4o
run dense      dense-4o
run abl-title  abl-title-4o
run abl-rescue abl-rescue-4o

set_model ""            # restore platform default
echo "==== driver done $(date -u)"
touch "$OUT/DONE"
