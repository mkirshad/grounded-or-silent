# Run inside `manage.py shell`: second sampling wave — subject-diverse judgments,
# head + disposition, raw material for batch-03 C-HOLD / C-FACT golds.
import re

from apps.library.models import LibraryChunk, LibraryDocument


def show(d):
    chunks = list(LibraryChunk.objects.filter(document=d).order_by("seq"))
    if len(chunks) < 3:
        return
    head = re.sub(r"\s+", " ", chunks[0].text)[:240]
    tail = re.sub(r"\s+", " ", chunks[-1].text)[-340:]
    print("=" * 6, d.title[:95])
    print("HEAD:", head)
    print("TAIL:", tail)
    print()


seen = set()
# Subject filters: family, tax, service/writ, criminal appeal, rent/civil
filters = [
    ("khula OR family", LibraryDocument.objects.filter(doc_type="judgment", title__iregex="Judge Family|khula")),
    ("tax", LibraryDocument.objects.filter(doc_type="judgment", title__icontains="Commissioner Inland Revenue")),
    ("service/govt", LibraryDocument.objects.filter(doc_type="judgment", title__icontains="Province of Punjab")),
    ("criminal appeal", LibraryDocument.objects.filter(doc_type="judgment", title__istartswith="2024 LHC", title__icontains="THE STATE VS")),
    ("rent/landlord", LibraryDocument.objects.filter(doc_type="judgment", title__iregex="rent|tenan")),
    ("bank/finance", LibraryDocument.objects.filter(doc_type="judgment", title__iregex="bank")),
]
for label, qs in filters:
    print("#### FILTER:", label)
    for d in qs.order_by("id")[:3]:
        if d.id in seen:
            continue
        seen.add(d.id)
        show(d)
