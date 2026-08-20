# Run inside `manage.py shell`: harvest C-HOLD gold material at scale by finding
# explicit disposition sentences anywhere in judgment text (not only the last
# chunk, which is often just signatures).
import re

from apps.library.models import LibraryChunk

PAT = re.compile(
    r"[^.]{10,240}\b(?:petition|appeal|revision|reference|application)s?\b"
    r"[^.]{0,120}\b(?:is|are|stands?|hereby)\b[^.]{0,80}"
    r"\b(?:allowed|dismissed|accepted|partly allowed)\b[^.]{0,160}\.",
    re.I,
)

seen_docs = set()
shown = 0
qs = (
    LibraryChunk.objects.filter(
        document__doc_type="judgment",
        text__iregex="(petition|appeal|revision)s? (is|are|stands|hereby) ",
    )
    .select_related("document")
    .order_by("-document_id")
)
for chunk in qs.iterator(chunk_size=200):
    if chunk.document_id in seen_docs:
        continue
    m = PAT.search(chunk.text)
    if not m:
        continue
    seen_docs.add(chunk.document_id)
    sent = re.sub(r"\s+", " ", m.group(0)).strip()
    print("======", chunk.document.title[:95])
    print("DISP:", sent[:320])
    print()
    shown += 1
    if shown >= 22:
        break
