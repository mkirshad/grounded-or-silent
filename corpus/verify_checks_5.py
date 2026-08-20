# Fifth verification wave (run inside manage.py shell) — final S-REC golds.
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
    ("PPC-279-rash-driving", "Penal Code", "rash or negligent"),
    ("PPC-336B-acid", "Penal Code", "corrosive substance"),
    ("PPC-186-obstruct", "Penal Code", "obstructs any public servant"),
    ("PPC-415-cheating-def", "Penal Code", "deceives"),
    ("CrPC-491-habeas", "Criminal Procedure", "illegally or improperly detained"),
    ("CrPC-145-land-dispute", "Criminal Procedure", "breach of the peace"),
    ("Contract-126-guarantee", "Contract Act", "contract of guarantee"),
    ("Contract-148-bailment", "Contract Act", "bailment"),
    ("Contract-182-agency", "Contract Act", "agent"),
    ("TPA-105-lease", "Transfer of Property", "lease of immoveable property"),
    ("TPA-118-exchange", "Transfer of Property", "exchange"),
    ("Succession-probate", "Succession Act", "probate"),
    ("NI-holder-due-course", "Negotiable Instruments", "holder in due course"),
    ("Companies-single-member", "^Companies Act", "single member"),
    ("ITO-122-amend", "Income Tax Ordinance", "amend the assessment"),
    ("TradeMarks-infringe", "Trade ?Marks", "infringement"),
    ("Copyright-infringe", "Copyright", "infringement"),
    ("PECA-14-efraud", "Electronic Crimes", "electronic fraud"),
    ("Wages-1936", "Payment of Wages", "wages"),
    ("MinWages-1961", "Minimum Wages", "minimum"),
    ("Workmen-1923", "Workmen", "compensation"),
    ("IRA-2012", "Industrial Relations", "collective bargaining"),
    ("Zakat-1980", "Zakat", "nisab"),
    ("CNSA-1997", "Narcotic Substances", "possess"),
]
for c in checks:
    check(*c)
