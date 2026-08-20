# Fourth verification wave (run inside manage.py shell) — batch-05 S-REC golds.
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
    ("PPC-448-house-trespass", "Penal Code", "house-trespass"),
    ("PPC-468-forgery-cheating", "Penal Code", "forgery for purpose of cheating"),
    ("PPC-511-attempt", "Penal Code", "attempting to commit offences"),
    ("PPC-34-common-intention", "Penal Code", "common intention"),
    ("CrPC-265K", "Criminal Procedure", "265-K"),
    ("QSO-cross-examination", "Qanun-e-Shahadat", "cross-examination"),
    ("Contract-73-damages", "Contract Act", "compensation for loss"),
    ("Contract-124-indemnity", "Contract Act", "indemnity"),
    ("TPA-58-mortgage", "Transfer of Property", "mortgage"),
    ("TPA-52-lis-pendens", "Transfer of Property", "pendency"),
    ("Succession-372", "Succession Act", "application for certificate"),
    ("Companies-AGM", "^Companies Act", "annual general meeting"),
    ("Companies-memorandum", "^Companies Act", "memorandum of association"),
    ("ITO-114-return", "Income Tax Ordinance", "return of income"),
    ("SalesTax-registration", "Sales Tax", "required to be registered"),
    ("PECA-16-identity", "Electronic Crimes", "identity information"),
    ("PECA-10-cyberterror", "Electronic Crimes", "cyber terrorism"),
    ("Passports-refusal", "Passport", "refuse"),
]
for c in checks:
    check(*c)
