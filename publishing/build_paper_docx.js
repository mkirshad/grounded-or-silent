// Build paper.docx in the house preprint style (title page, Contents,
// running headers, Page X of Y footers). Two-pass: run with TOC page numbers
// in publishing/toc-pages.json (heading -> page); absent entries print "–".
const fs = require("fs");
const path = require("path");
const D = require("docx");

const TEAL = "155E75";
const DARK = "111111";
const GREY = "555555";

let tocPages = {};
try { tocPages = JSON.parse(fs.readFileSync(path.join(__dirname, "toc-pages.json"), "utf8")); } catch (e) {}

const T = (text, opts = {}) => new D.TextRun({ text, font: "Calibri", size: 22, color: DARK, ...opts });
const P = (children, opts = {}) => new D.Paragraph({ spacing: { after: 140, line: 300 }, alignment: D.AlignmentType.JUSTIFIED, ...opts, children });

const H1 = (text) => new D.Paragraph({
  spacing: { before: 320, after: 160 },
  children: [new D.TextRun({ text, font: "Calibri", size: 30, bold: true, color: TEAL })],
});
const H2 = (text) => new D.Paragraph({
  spacing: { before: 240, after: 120 },
  children: [new D.TextRun({ text, font: "Calibri", size: 25, bold: true, color: TEAL })],
});

// Inline mini-markdown: **bold** and *italic*
function runs(text, base = {}) {
  const out = [];
  const parts = text.split(/(\*\*[^*]+\*\*|\*[^*]+\*)/g);
  for (const part of parts) {
    if (!part) continue;
    if (part.startsWith("**")) out.push(T(part.slice(2, -2), { bold: true, ...base }));
    else if (part.startsWith("*")) out.push(T(part.slice(1, -1), { italics: true, ...base }));
    else out.push(T(part, base));
  }
  return out;
}
const para = (text, opts = {}) => P(runs(text), opts);

function table(headers, rows, widths) {
  const total = widths.reduce((a, b) => a + b, 0);
  const cell = (txt, head) => new D.TableCell({
    width: { size: 1, type: D.WidthType.DXA },
    shading: head ? { type: D.ShadingType.CLEAR, fill: "EEF2F6" } : undefined,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    children: [new D.Paragraph({ children: runs(txt).map(r => { r.root; return r; }).map(r => r) , spacing: { after: 0 } })],
  });
  // rebuild cells with smaller font
  const mk = (txt, head) => new D.TableCell({
    width: { size: 1, type: D.WidthType.DXA },
    shading: head ? { type: D.ShadingType.CLEAR, fill: "EEF2F6" } : undefined,
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    children: [new D.Paragraph({ spacing: { after: 0 }, children: txt.split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map(p => p.startsWith("**") ? new D.TextRun({ text: p.slice(2, -2), bold: true, font: "Calibri", size: 18 }) : new D.TextRun({ text: p, font: "Calibri", size: 18, bold: head })) })],
  });
  return new D.Table({
    width: { size: total, type: D.WidthType.DXA },
    columnWidths: widths,
    rows: [
      new D.TableRow({ children: headers.map(h => mk(h, true)), tableHeader: true }),
      ...rows.map(r => new D.TableRow({ children: r.map(c => mk(c, false)) })),
    ],
  });
}

const tocEntry = (label, indent = 0) => new D.Paragraph({
  spacing: { after: 90 },
  indent: { left: indent },
  children: [new D.TextRun({
    text: label, font: "Calibri", size: 22,
    }),
    new D.TextRun({
      children: [new D.PositionalTab({ alignment: D.PositionalTabAlignment.RIGHT, relativeTo: D.PositionalTabRelativeTo.MARGIN, leader: D.PositionalTabLeader.DOT })],
      font: "Calibri", size: 22,
    }),
    new D.TextRun({ text: String(tocPages[label] ?? "–"), font: "Calibri", size: 22 }),
  ],
});

const ABSTRACT = "Legal AI tools are known to hallucinate: audits of commercial legal research products report fabricated or misgrounded authorities in 17–33% of responses (Magesh et al., 2024). Existing legal QA benchmarks cover well-resourced jurisdictions; for Pakistan — a mixed common-law system of 240 million people — no benchmark spans its statutes and case law. We present **PakLegalQA**, the first citation-grounded question-answering benchmark for Pakistani law: 300 questions over 946 federal statutes (Pakistan Code) and 2,503 reported Lahore High Court judgments (2022–2026), with gold statute sections and neutral citations, an unanswerable subset whose only correct response is a refusal, and a 60-question code-switched Roman-Urdu overlay reflecting how users actually type. Using PakLegalQA we evaluate a deployed, production grounded-or-refuse RAG system and ablations of its retrieval stack against closed-book and vanilla-RAG baselines. The production system attains 74.5% gold-source retrieval — 14.5 points above vanilla dense retrieval, with title-affinity re-ranking and lexical rescues (citation lookup, name matching, deep reading of named judgments) contributing roughly 7 and 9 points respectively — while over-refusing on only 5.3% (Sol) to 0.6% (gpt-4o) of answerable questions. The closed-book baseline refuses just 7 of 84 unanswerable questions, answering the rest from parametric memory — the grounding-discipline gap the benchmark is designed to expose; grounded systems refuse or honestly signal insufficiency on the large majority. A 24-item stratified manual audit finds 87.5% correct answers and zero fabricated citations: the grounded system's failure mode is mis-selection or silence, never invention. We additionally document a query-rewrite-stage hallucination (the rewrite model injecting a wrong-jurisdiction statute), a failure stage named but unmeasured in prior work, and an infrastructure-failure episode that masqueraded as a calibration collapse — motivating positional sanity checks in LLM evaluation harnesses. The benchmark, harness, and corpus manifest are released.";

const S = JSON.parse(fs.readFileSync(path.join(__dirname, "paper-body.json"), "utf8"));

const body = [];
body.push(H1("1. Abstract"));
body.push(para(ABSTRACT));
body.push(P(runs("**Keywords:** legal question answering; retrieval-augmented generation; benchmark; Pakistani law; refusal calibration; citation grounding; Roman Urdu; legal NLP"), { indent: { left: 400, right: 400 } }));

for (const sec of S.sections) {
  if (sec.h1) body.push(H1(sec.h1));
  if (sec.h2) body.push(H2(sec.h2));
  for (const p of sec.paras || []) body.push(para(p));
  if (sec.table) { body.push(table(sec.table.headers, sec.table.rows, sec.table.widths)); if (sec.table.caption) body.push(P(runs(sec.table.caption).map(r => r), { spacing: { before: 80, after: 200 } })); }
  for (const p of sec.after || []) body.push(para(p));
}
body.push(H1("12. References"));
for (const ref of S.references) body.push(new D.Paragraph({ spacing: { after: 90 }, indent: { left: 360, hanging: 360 }, children: runs(ref) }));

const headerDefault = new D.Header({
  children: [new D.Paragraph({
    tabStops: [{ type: D.TabStopType.RIGHT, position: 9350 }],
    border: { bottom: { style: D.BorderStyle.SINGLE, size: 6, color: "888888", space: 4 } },
    children: [
      new D.TextRun({ text: "Muhammad Kashif Irshad", italics: true, font: "Calibri", size: 19 }),
      new D.TextRun({ text: "\tGrounded or Silent — PakLegalQA", italics: true, font: "Calibri", size: 19 }),
    ],
  })],
});
const footerDefault = new D.Footer({
  children: [new D.Paragraph({
    alignment: D.AlignmentType.CENTER,
    children: [
      new D.TextRun({ text: "Page ", font: "Calibri", size: 19 }),
      new D.TextRun({ children: [D.PageNumber.CURRENT], font: "Calibri", size: 19, bold: true }),
      new D.TextRun({ text: " of ", font: "Calibri", size: 19 }),
      new D.TextRun({ children: [D.PageNumber.TOTAL_PAGES], font: "Calibri", size: 19, bold: true }),
    ],
  })],
});
const footerFirst = new D.Footer({
  children: [
    new D.Paragraph({ spacing: { after: 60 }, children: [
      new D.TextRun({ text: "Cite as: ", bold: true, font: "Calibri", size: 19 }),
      new D.TextRun({ text: "Irshad, Muhammad Kashif. \"Grounded or Silent: Citation-Faithful Legal Question Answering for Pakistani Law.\" IrshadOS Research, 2026. DOI: 10.5281/zenodo.22037183.", font: "Calibri", size: 19 }),
    ]}),
    new D.Paragraph({ children: [
      new D.TextRun({ text: "Web edition, data and evaluation harness: ", font: "Calibri", size: 19 }),
      new D.TextRun({ text: "https://irshados.com/ebooks/grounded-or-silent-paklegalqa/", font: "Calibri", size: 19, color: "0B4F6C" }),
    ]}),
  ],
});

const titlePage = [
  new D.Paragraph({ spacing: { before: 2200, after: 200 }, alignment: D.AlignmentType.CENTER,
    children: [new D.TextRun({ text: "Grounded or Silent: Citation-Faithful Legal", font: "Calibri", size: 52 })] }),
  new D.Paragraph({ spacing: { after: 480 }, alignment: D.AlignmentType.CENTER,
    children: [new D.TextRun({ text: "Question Answering for Pakistani Law", font: "Calibri", size: 52 })] }),
  new D.Paragraph({ alignment: D.AlignmentType.CENTER, spacing: { after: 300 }, children: [
    new D.TextRun({ text: " DOI ", font: "Consolas", size: 20, color: "FFFFFF", shading: { type: D.ShadingType.CLEAR, fill: "444444" } }),
    new D.TextRun({ text: " 10.5281/zenodo.22037183 ", font: "Consolas", size: 20, color: "FFFFFF", shading: { type: D.ShadingType.CLEAR, fill: "1F7BB6" } }),
  ]}),
  new D.Paragraph({ alignment: D.AlignmentType.CENTER, spacing: { after: 220 }, children: [new D.TextRun({ text: "Muhammad Kashif Irshad", font: "Calibri", size: 26 })] }),
  new D.Paragraph({ alignment: D.AlignmentType.CENTER, spacing: { after: 220 }, children: [
    new D.TextRun({ text: "Correspondence: ", bold: true, font: "Calibri", size: 22 }),
    new D.TextRun({ text: "dev@irshados.com – Lahore, Pakistan", font: "Calibri", size: 22 }),
  ]}),
  new D.Paragraph({ alignment: D.AlignmentType.CENTER, spacing: { after: 220 }, children: [new D.TextRun({ text: "ORCID 0009-0008-9161-9875", font: "Calibri", size: 22 })] }),
  new D.Paragraph({ alignment: D.AlignmentType.CENTER, spacing: { after: 220 }, children: [new D.TextRun({ text: "Preprint | 2026-08-21", font: "Calibri", size: 22 })] }),
  new D.Paragraph({ alignment: D.AlignmentType.CENTER, spacing: { after: 220 }, children: [new D.TextRun({ text: "IrshadOS Research", font: "Calibri", size: 22 })] }),
  new D.Paragraph({ alignment: D.AlignmentType.CENTER, children: [new D.TextRun({ text: "irshados.com", font: "Calibri", size: 22, color: "0B4F6C" })] }),
  new D.Paragraph({ children: [new D.PageBreak()] }),
];

const contents = [
  new D.Paragraph({ spacing: { after: 240 }, children: [new D.TextRun({ text: "Contents", font: "Calibri", size: 34, bold: true, color: TEAL })] }),
  ...S.toc.map(e => tocEntry(e.label, e.indent || 0)),
  new D.Paragraph({ children: [new D.PageBreak()] }),
];

const doc = new D.Document({
  styles: { default: { document: { run: { font: "Calibri", size: 22 } } } },
  sections: [{
    properties: { titlePage: true, page: { margin: { top: 1300, bottom: 1300, left: 1300, right: 1300 } } },
    headers: { default: headerDefault, first: new D.Header({ children: [] }) },
    footers: { default: footerDefault, first: footerFirst },
    children: [...titlePage, ...contents, ...body],
  }],
});

D.Packer.toBuffer(doc).then(buf => {
  const out = path.join(__dirname, "paper.docx");
  fs.writeFileSync(out, buf);
  console.log("wrote", out, buf.length, "bytes");
});
