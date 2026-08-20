# Third mini-wave of gold verification (run inside manage.py shell).
from apps.library.models import LibraryChunk, LibraryDocument


def check(label, title_pat, text_pat):
    docs = LibraryDocument.objects.filter(
        title__iregex=title_pat, is_published=True, doc_type="statute"
    )
    if not docs.exists():
        print(label + ": NO-DOC (" + title_pat + ")")
        return
    hit = LibraryChunk.objects.filter(document__in=docs, text__icontains=text_pat).first()
    print(label + ": " + ("FOUND" if hit else "no-text") + " | " + docs.first().title[:48])


checks = [
    ("CNSA-narcotics", "Narcotic", "narcotic drug"),
    ("MFLO-s10-dower", "Muslim Family", "dower"),
    ("Contract-s11-minor", "Contract Act", "age of majority"),
    ("FCA-appeal", "Family Courts", "appeal"),
    ("CrPC-61-24hours", "Criminal Procedure", "twenty-four hours"),
    ("CrPC-154-refusal-JoP", "Criminal Procedure", "22-A"),
    ("PPC-509-modesty", "Penal Code", "insult the modesty"),
    ("TPA-123-gift", "Transfer of Property", "gift"),
    ("QSO-retracted-confession", "Qanun-e-Shahadat", "retracted"),
    ("Defamation-Ord-2002", "Defamation", "defamation"),
]
for c in checks:
    check(*c)
