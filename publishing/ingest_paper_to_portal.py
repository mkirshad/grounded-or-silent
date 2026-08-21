# Run inside manage.py shell: add the Grounded or Silent paper to the
# web-published "Muhammad Kashif Irshad Research Preprints" folder so the
# site's Ask widget can answer about it, following the folder's naming style.
import io

from apps.knowledge.embeddings import index_document
from apps.knowledge.models import Document, Folder

f = Folder.objects.get(id=5)
title = (
    "Research-Preprint-English-Grounded or Silent Citation-Faithful Legal "
    "Question Answering for Pakistani Law.pdf"
)
src = io.open(
    "/mnt/f/IrshadOS/IrshadOS-Main-Site/src/content/ebooks/grounded-or-silent-paklegalqa.md",
    encoding="utf-8",
).read()
body = src.split("---", 2)[2].strip()
header = (
    "Grounded or Silent: Citation-Faithful Legal Question Answering for "
    "Pakistani Law. Research preprint by Muhammad Kashif Irshad (IrshadOS "
    "Research, Lahore), August 2026. DOI 10.5281/zenodo.22037183. Introduces "
    "PakLegalQA, the first citation-grounded question-answering benchmark for "
    "Pakistani law, and evaluates the deployed Irshad AI Employee system.\n\n"
)
existing = Document.objects.filter(folder=f, title=title).first()
if existing:
    existing.content = header + body
    existing.save()
    doc = existing
    print("updated existing document", doc.id)
else:
    doc = Document.objects.create(company=f.company, folder=f, title=title, content=header + body)
    print("created document", doc.id)
index_document(doc)
print("indexed:", doc.title[:60], "chars:", len(doc.content))
