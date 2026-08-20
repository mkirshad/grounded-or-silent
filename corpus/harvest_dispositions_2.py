# Disposition harvest round 2 (run inside manage.py shell): ascending document_id
# so the pool differs from round 1 (which took the newest). Skips already-used ids.
import re

from apps.library.models import LibraryChunk

USED_TITLES = [
    "2026 LHC 9 ", "2026 LHC 73 ", "2026 LHC 66 ", "2026 LHC 58 ", "2026 LHC 53 ",
    "2026 LHC 4874", "2026 LHC 4800", "2026 LHC 4789", "2026 LHC 4758",
    "2026 LHC 4741", "2026 LHC 4722", "2026 LHC 47 ", "2026 LHC 4694",
    "2026 LHC 4681", "2026 LHC 4650", "2026 LHC 4635", "2026 LHC 4593",
    "2026 LHC 4586", "2026 LHC 4578", "2026 LHC 4569", "2026 LHC 999",
]

PAT = re.compile(
    r"[^.]{10,240}\b(?:petition|appeal|revision|reference|application|suit)s?\b"
    r"[^.]{0,120}\b(?:is|are|stands?|hereby)\b[^.]{0,80}"
    r"\b(?:allowed|dismissed|accepted|decreed|partly allowed)\b[^.]{0,160}\.",
    re.I,
)

seen_docs = set()
shown = 0
qs = (
    LibraryChunk.objects.filter(
        document__doc_type="judgment",
        text__iregex="(petition|appeal|revision|suit)s? (is|are|stands|hereby) ",
    )
    .select_related("document")
    .order_by("document_id")
)
for chunk in qs.iterator(chunk_size=200):
    if chunk.document_id in seen_docs:
        continue
    title = chunk.document.title
    if any(title.startswith(u.strip()) for u in USED_TITLES):
        continue
    m = PAT.search(chunk.text)
    if not m:
        continue
    seen_docs.add(chunk.document_id)
    print("======", title[:95])
    print("DISP:", re.sub(r"\s+", " ", m.group(0)).strip()[:300])
    print()
    shown += 1
    if shown >= 26:
        break
