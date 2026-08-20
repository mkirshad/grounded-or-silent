# Run inside `manage.py shell`: sample judgments across years with head + disposition
# snippets, raw material for C-HOLD / C-FACT gold labels.
import re

from apps.library.models import LibraryChunk, LibraryDocument

for year in ["2022", "2023", "2024", "2025", "2026"]:
    docs = list(
        LibraryDocument.objects.filter(
            title__istartswith=year + " LHC", doc_type="judgment", is_published=True
        ).order_by("id")[3:5]
    )
    for d in docs:
        chunks = list(LibraryChunk.objects.filter(document=d).order_by("seq"))
        if len(chunks) < 3:
            continue
        head = re.sub(r"\s+", " ", chunks[0].text)[:260]
        tail = re.sub(r"\s+", " ", chunks[-1].text)[-320:]
        print("=" * 6, d.title[:90])
        print("HEAD:", head)
        print("TAIL:", tail)
        print()
