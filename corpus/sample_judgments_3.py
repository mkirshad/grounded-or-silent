# Third sampling wave (run inside manage.py shell): fresh filters + year offsets.
import re

from apps.library.models import LibraryChunk, LibraryDocument


def show(d):
    chunks = list(LibraryChunk.objects.filter(document=d).order_by("seq"))
    if len(chunks) < 3:
        return False
    head = re.sub(r"\s+", " ", chunks[0].text)[:200]
    tail = re.sub(r"\s+", " ", chunks[-1].text)[-340:]
    print("=" * 6, d.title[:95])
    print("HEAD:", head)
    print("TAIL:", tail)
    print()
    return True


seen = set()
filters = [
    ("federation", LibraryDocument.objects.filter(doc_type="judgment", title__icontains="Federation of Pakistan")),
    ("utilities", LibraryDocument.objects.filter(doc_type="judgment", title__iregex="WAPDA|LESCO|GEPCO|FESCO")),
    ("university", LibraryDocument.objects.filter(doc_type="judgment", title__icontains="University")),
    ("sessions-judge", LibraryDocument.objects.filter(doc_type="judgment", title__icontains="Additional Sessions Judge")),
    ("nab", LibraryDocument.objects.filter(doc_type="judgment", title__icontains="National Accountability")),
    ("customs-fbr", LibraryDocument.objects.filter(doc_type="judgment", title__iregex="Customs|Federal Board of Revenue")),
]
for label, qs in filters:
    print("#### FILTER:", label)
    shown = 0
    for d in qs.order_by("-id"):
        if d.id in seen or shown >= 3:
            continue
        seen.add(d.id)
        if show(d):
            shown += 1
        if shown >= 3:
            break
