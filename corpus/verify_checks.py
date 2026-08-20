# Run inside `manage.py shell`: verifies candidate gold labels against corpus text.
from apps.library.models import LibraryChunk, LibraryDocument


def check(label, title_pat, text_pat):
    docs = LibraryDocument.objects.filter(title__icontains=title_pat, is_published=True)
    if not docs.exists():
        print(label + ": NO-DOC (" + title_pat + ")")
        return
    hit = LibraryChunk.objects.filter(document__in=docs, text__icontains=text_pat).first()
    status = "FOUND" if hit else "no-text"
    print(label + ": " + status + " | " + docs.first().title[:45])


checks = [
    ("PPC-365A-ransom", "Penal Code", "kidnapping or abduction for extorting"),
    ("PPC-376-rape", "Penal Code", "punishment for rape"),
    ("PPC-420-cheating", "Penal Code", "cheating and dishonestly inducing delivery"),
    ("PPC-506-intimidation", "Penal Code", "criminal intimidation"),
    ("PPC-193-false-evidence", "Penal Code", "false evidence"),
    ("PPC-342-confinement", "Penal Code", "wrongful confinement"),
    ("PPC-392-robbery", "Penal Code", "punishment for robbery"),
    ("PPC-395-dacoity", "Penal Code", "dacoity"),
    ("PPC-384-extortion", "Penal Code", "extortion"),
    ("PPC-323-diyat", "Penal Code", "value of diyat"),
    ("CrPC-54-arrest", "Criminal Procedure", "arrest without warrant"),
    ("CrPC-167-remand", "Criminal Procedure", "fifteen days"),
    ("CrPC-496-bailable", "Criminal Procedure", "bail in bailable"),
    ("CrPC-144", "Criminal Procedure", "apprehended danger"),
    ("CrPC-249A", "Criminal Procedure", "acquit the accused at any stage"),
    ("QSO-Art17-witnesses", "Qanun-e-Shahadat", "competence of"),
    ("QSO-confession-police", "Qanun-e-Shahadat", "confession"),
    ("Contract-2h", "Contract Act", "enforceable by law"),
    ("Contract-14-consent", "Contract Act", "free consent"),
    ("NI-days-of-grace", "Negotiable Instruments", "days of grace"),
    ("MFLO-talaq-notice", "Muslim Family", "talaq"),
    ("MFLO-polygamy", "Muslim Family", "arbitration council"),
    ("DMMA-grounds", "Dissolution of Muslim", "whereabouts of the husband"),
    ("Dowry-limit", "Dowry", "dowry"),
    ("PECA-s3-access", "Electronic Crimes", "unauthoris"),
    ("PECA-stalking", "Electronic Crimes", "stalking"),
    ("PECA-dignity", "Electronic Crimes", "dignity"),
    ("ATA-terrorism-def", "Anti-Terrorism", "terrorism"),
    ("NAB-corrupt", "National Accountability", "corrupt practices"),
    ("Zina-Ord", "Zina", "zina"),
    ("Companies-directors", "Companies Act", "directors"),
    ("SRA-spec-perf", "Specific Relief", "specific performance"),
    ("FCA-jurisdiction", "Family Courts", "exclusive jurisdiction"),
    ("CourtFees", "Court Fees", "fee"),
]
for c in checks:
    check(*c)

print("---absence checks---")
print("IHC judgments:", LibraryDocument.objects.filter(title__icontains="IHC").count())
print("Consumer Rights Act:", LibraryDocument.objects.filter(title__icontains="Consumer Rights").count())
print("Police Order docs:", LibraryDocument.objects.filter(title__icontains="Police Order").count())
