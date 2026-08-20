# Second wave of gold-label verification (run inside manage.py shell).
# Lesson from wave 1: fuzzy title patterns, and confirm absences with iregex.
from apps.library.models import LibraryChunk, LibraryDocument


def check(label, title_pat, text_pat):
    docs = LibraryDocument.objects.filter(
        title__iregex=title_pat, is_published=True, doc_type="statute"
    )
    if not docs.exists():
        print(label + ": NO-DOC (" + title_pat + ")")
        return
    hit = LibraryChunk.objects.filter(document__in=docs, text__icontains=text_pat).first()
    status = "FOUND" if hit else "no-text"
    print(label + ": " + status + " | " + docs.first().title[:48])


checks = [
    ("Registration-compulsory", "Registration Act", "registration is compulsory"),
    ("TPA-sale-def", "Transfer of Property", "transfer of ownership"),
    ("Succession-certificate", "Succession Act", "succession certificate"),
    ("Guardians-welfare", "Guardians and Wards", "welfare of the minor"),
    ("Arbitration-agreement", "Arbitration", "arbitration agreement"),
    ("ITO-reference-HC", "Income Tax Ordinance", "reference to the High Court"),
    ("SalesTax-input", "Sales Tax", "input tax"),
    ("Customs-smuggling", "Customs Act", "smuggl"),
    ("Passports-act", "Passport", "passport"),
    ("Citizenship-1951", "Citizenship", "citizen of Pakistan"),
    ("Divorce-1869", "Divorce", "dissolution"),
    ("ETO-2002-signature", "Electronic Transactions", "electronic signature"),
    ("Copyright-ord", "Copyright", "copyright"),
    ("TradeMarks-ord", "Trade ?Marks", "trade mark"),
    ("Competition-2010", "Competition", "dominant position"),
    ("Juvenile-2018", "Juvenile", "juvenile"),
    ("Probation-1960", "Probation", "probation"),
    ("OfficialSecrets", "Official Secrets", "secret"),
    ("Extradition-1972", "Extradition", "extradition"),
    ("BarCouncils-1973", "Legal Practitioners", "advocate"),
    ("Emigration-1979", "Emigration", "emigrant"),
    ("Harassment-workplace-2010", "Harassment", "harassment"),
    ("AccessToInfo-2017", "Access to Information", "right of access"),
    ("Companies-2017", "^Companies Act", "director"),
    ("PPC-365A-check2", "Penal Code", "ransom"),
    ("CrPC-249A-check2", "Criminal Procedure", "249"),
]
for c in checks:
    check(*c)
