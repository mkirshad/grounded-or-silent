#!/usr/bin/env bash
# Full PakLegalQA experiment driver. Run detached inside WSL:
#   nohup bash /mnt/f/IrshadOS/research/grounded-or-silent/scripts/run_full_experiment.sh \
#     > /mnt/f/IrshadOS/research/grounded-or-silent/results/full/driver.log 2>&1 &
#
# Phases (generator model is held constant within every comparison):
#   Sol   : prod, cb          — the headline production numbers
#   gpt-4o: prod, dense, abl-title, abl-rescue — the ablation story (disclosed)
#
# The workspace-3 answer model is flipped to gpt-4o for the ablation phases and
# restored to the platform default (empty => Sol) at the end.
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
print('workspace-3 answer model set to:', repr(e.model) or 'platform default')
"
}

echo "==== driver start $(date -u)"
set_model ""            # platform default = Sol
run prod prod-sol
run cb   cb-sol

set_model gpt-4o
run prod       prod-4o
run dense      dense-4o
run abl-title  abl-title-4o
run abl-rescue abl-rescue-4o

set_model ""            # restore platform default
echo "==== driver done $(date -u)"
touch "$OUT/DONE"
