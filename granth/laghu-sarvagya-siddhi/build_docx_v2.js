// v2 builder: Laghu Sarvagya Siddhi vyakhya -> docx in the Pramana_Pariksha_Sampurna_Vyakhya format.
//
// Inputs
//   parts/batch*.md      : original § files (§ title line, "## N. ..." sub-sections, bullets, tables)
//   addenda/sNN.md       : per-§ supplements (## ३. पूरक व्याख्या | ## ४. सरल उदाहरण | ## ५. तुलनात्मक तालिका / चार्ट | ## ६. सन्दर्भ एवं पाद-टिप्पणी)
//   groups.json          : { "1": "[ खण्ड-शीर्षक ]", ... }  Heading1 group header inserted before §N
//   backmatter/*.md      : "# " Heading1, "## " Heading2, "### " Heading3, bullets, tables, paragraphs
//
// Output: ./vyakhya/Laghu_Sarvagya_Siddhi_Vyakhya.docx  (TOC + PAGE fields; run finalize_word.ps1 to update fields & export PDF)

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, TableOfContents,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, convertInchesToTwip,
  Footer, PageNumber, PageBreak
} = require('docx');

const FONT = 'Nirmala UI';
const BODY = 24;        // 12pt
const PARTS_DIR = path.join(__dirname, 'parts');
const ADD_DIR = path.join(__dirname, 'addenda');
const BACK_DIR = path.join(__dirname, 'backmatter');
const GROUPS = fs.existsSync(path.join(__dirname, 'groups.json'))
  ? JSON.parse(fs.readFileSync(path.join(__dirname, 'groups.json'), 'utf-8')) : {};
const OUT_FILE = process.env.OUT || path.join(__dirname, 'vyakhya', 'Laghu_Sarvagya_Siddhi_Vyakhya.docx');

const DEV = '०१२३४५६७८९';
const devToInt = s => parseInt(s.replace(/[०-९]/g, d => DEV.indexOf(d)), 10);
const intToDev = n => String(n).replace(/\d/g, d => DEV[d]);

// ---------- inline / paragraph helpers ----------
function parseInline(line) {
  const runs = []; const re = /\*\*(.+?)\*\*/g; let last = 0, m;
  while ((m = re.exec(line)) !== null) {
    if (m.index > last) runs.push({ text: line.slice(last, m.index), bold: false });
    runs.push({ text: m[1], bold: true }); last = re.lastIndex;
  }
  if (last < line.length) runs.push({ text: line.slice(last), bold: false });
  if (!runs.length) runs.push({ text: line, bold: false });
  return runs;
}
const runs = (line, extra) => parseInline(line).map(r => new TextRun(Object.assign({ text: r.text, bold: r.bold, size: BODY, font: FONT }, extra || {})));

const pNormal = (line, extra) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 320 }, children: runs(line, extra) });
const pBullet = line => new Paragraph({ bullet: { level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 320 }, children: runs(line) });
const pQuote = line => new Paragraph({
  indent: { left: 360 }, border: { left: { style: BorderStyle.SINGLE, size: 12, color: '1F4E79', space: 8 } },
  shading: { type: ShadingType.CLEAR, fill: 'EDF2F7' }, spacing: { after: 120, before: 80, line: 320 }, children: runs(line, { italics: true })
});
const pMool = line => new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360 }, spacing: { after: 80, line: 340 }, children: runs(line, { color: '7A1F1F' }) });
const pEmpty = () => new Paragraph({ text: '', spacing: { after: 60 } });

function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 200 },
    children: [new TextRun({ text, bold: true, size: 32, font: FONT, color: '7A1F1F' })] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 320, after: 140 }, keepNext: true,
    children: [new TextRun({ text, bold: true, size: 28, font: FONT, color: '1F4E79' })] });
}
function h3(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 180, after: 80 }, keepNext: true,
    children: [new TextRun({ text, bold: true, size: 25, font: FONT, color: '833C0B' })] });
}

function buildTable(rows) {
  const n = rows[0].length; const w = Math.floor(9200 / n);
  const widths = n === 2 ? [3200, 6000] : rows[0].map(() => w);
  const trs = rows.map((cells, ri) => new TableRow({
    tableHeader: ri === 0,
    children: Array.from({ length: n }, (_, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA },
      shading: ri === 0 ? { type: ShadingType.CLEAR, fill: 'DCE6F1' } : undefined,
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [new Paragraph({ spacing: { after: 20, line: 280 }, children: parseInline(cells[ci] || '').map(r => new TextRun({ text: r.text, bold: ri === 0 || r.bold, size: BODY - 3, font: FONT })) })]
    }))
  }));
  return new Table({ width: { size: 9200, type: WidthType.DXA }, columnWidths: widths, rows: trs });
}

// ---------- generic block renderer (lines -> paragraphs) ----------
function renderBlock(lines, mool) {
  const out = []; let tbl = null;
  const flush = () => { if (tbl && tbl.length) { out.push(buildTable(tbl)); out.push(pEmpty()); } tbl = null; };
  for (const raw of lines) {
    const t = raw.replace(/\r$/, '').trim();
    if (t === '' || t === '---') { flush(); continue; }
    if (t.startsWith('|')) {
      const cells = t.split('|').map(c => c.trim()); cells.shift(); if (cells[cells.length - 1] === '') cells.pop();
      if (/^:?-+:?$/.test(cells.join(''))) continue;
      (tbl = tbl || []).push(cells); continue;
    }
    flush();
    if (t.startsWith('> ')) { out.push(pQuote(t.slice(2))); continue; }
    if (t.startsWith('- ') || t.startsWith('• ')) { out.push(pBullet(t.slice(2))); continue; }
    if (t.startsWith('#### ')) { out.push(pNormal(t.slice(5), { bold: true })); continue; }
    out.push(mool ? pMool(t) : pNormal(t));
  }
  flush(); return out;
}

// ---------- parse § files ----------
// returns Map<num, {title, secs: [{head, lines}]}>
function parseParts() {
  const files = fs.readdirSync(PARTS_DIR).filter(f => f.endsWith('.md')).sort();
  const map = new Map(); let cur = null, sec = null;
  for (const f of files) {
    for (const raw of fs.readFileSync(path.join(PARTS_DIR, f), 'utf-8').split('\n')) {
      const t = raw.replace(/\r$/, '');
      const m = /^§([०-९]+)\s*—\s*(.*)$/.exec(t.trim());
      if (m) { cur = { num: devToInt(m[1]), title: `§ ${m[1]} — ${m[2].trim()}`, secs: [] }; map.set(cur.num, cur); sec = null; continue; }
      if (!cur) continue;
      if (t.trim().startsWith('## ')) { sec = { head: t.trim().slice(3).trim(), lines: [] }; cur.secs.push(sec); continue; }
      if (sec) sec.lines.push(t);
    }
  }
  return map;
}
function parseAddendum(num) {
  const f = path.join(ADD_DIR, `s${String(num).padStart(2, '0')}.md`);
  if (!fs.existsSync(f)) return null;
  const secs = []; let sec = null;
  for (const raw of fs.readFileSync(f, 'utf-8').split('\n')) {
    const t = raw.replace(/\r$/, '');
    if (t.trim().startsWith('## ')) { sec = { head: t.trim().slice(3).trim(), lines: [] }; secs.push(sec); continue; }
    if (sec) sec.lines.push(t);
  }
  return secs;
}
const kind = h => {
  if (h.includes('मूल संस्कृत')) return 1;
  if (h.includes('हिन्दी अनुवाद')) return 2;
  if (h.includes('पूरक')) return 3.5;
  if (h.includes('व्याख्या')) return 3;
  if (h.includes('सरल उदाहरण')) return 4;
  if (h.includes('तुलनात्मक')) return 5;
  if (h.includes('सन्दर्भ')) return 6;
  return 0; // misc note (आगे की दिशा / सन्तुलन-टिप्पणी / ईमानदार टिप्पणी) -> goes into ६
};

let missing = [];
function renderSection(s) {
  const out = [h2(s.title)];
  const add = parseAddendum(s.num) || [];
  if (!add.length) missing.push(s.num);
  const byKind = k => [...s.secs, ...add].filter(x => kind(x.head) === k);
  const misc = s.secs.filter(x => kind(x.head) === 0 && !x.head.includes('आगे की दिशा'));

  out.push(h3('१. मूल संस्कृत पाठ'));
  byKind(1).forEach(x => out.push(...renderBlock(x.lines, true)));
  out.push(h3('२. हिन्दी अनुवाद'));
  byKind(2).forEach(x => out.push(...renderBlock(x.lines)));
  out.push(h3('३. जैनागम के अनुसार विस्तृत व्याख्या'));
  byKind(3).forEach(x => out.push(...renderBlock(x.lines)));
  byKind(3.5).forEach(x => out.push(...renderBlock(x.lines)));
  out.push(h3('४. सरल उदाहरण'));
  const ex = byKind(4);
  if (ex.length) ex.forEach(x => out.push(...renderBlock(x.lines))); else out.push(pBullet('(इस अनुच्छेद हेतु उदाहरण अगले संस्करण में जोड़ा जाएगा।)'));
  out.push(h3('५. तुलनात्मक तालिका / चार्ट'));
  const tb = byKind(5);
  if (tb.length) tb.forEach(x => out.push(...renderBlock(x.lines))); else out.push(pNormal('इस अनुच्छेद हेतु तालिका आवश्यक नहीं।'));
  out.push(h3('६. सन्दर्भ एवं पाद-टिप्पणी'));
  const rf = byKind(6);
  rf.forEach(x => out.push(...renderBlock(x.lines)));
  misc.forEach(x => {
    const label = x.head.replace(/^[०-९]+\.\s*/, '');
    out.push(pNormal(`**${label}:**`));
    out.push(...renderBlock(x.lines));
  });
  if (!rf.length && !misc.length) out.push(pBullet('मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।'));
  out.push(pEmpty());
  return out;
}

// ---------- back matter ----------
function renderBackmatter() {
  if (!fs.existsSync(BACK_DIR)) return [];
  const out = [];
  for (const f of fs.readdirSync(BACK_DIR).filter(f => f.endsWith('.md')).sort()) {
    let buf = [];
    const flush = () => { if (buf.length) out.push(...renderBlock(buf)); buf = []; };
    for (const raw of fs.readFileSync(path.join(BACK_DIR, f), 'utf-8').split('\n')) {
      const t = raw.replace(/\r$/, '');
      if (t.startsWith('# ')) { flush(); out.push(h1(t.slice(2).trim())); continue; }
      if (t.startsWith('## ')) { flush(); out.push(h2(t.slice(3).trim())); continue; }
      if (t.startsWith('### ')) { flush(); out.push(h3(t.slice(4).trim())); continue; }
      buf.push(t);
    }
    flush();
  }
  return out;
}

// ---------- front matter ----------
const secCount = parseParts().size;
const front = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [new TextRun({ text: 'श्रीमदाचार्य-अनन्तकीर्ति-विरचिता', bold: true, size: 30, font: FONT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 240 }, children: [new TextRun({ text: 'लघु-सर्वज्ञ-सिद्धिः', bold: true, size: 48, font: FONT, color: '7A1F1F' })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: `सम्पूर्ण ग्रन्थ (§१ – §${intToDev(secCount)}): अनुच्छेदशः मूल संस्कृत पाठ, हिन्दी अनुवाद, जैनागम-सम्मत विस्तृत व्याख्या, सरल उदाहरण, तुलनात्मक तालिका/चार्ट एवं सन्दर्भ`, size: BODY, font: FONT })] }),
  pNormal('**आधार:** उपलब्ध 21-पृष्ठीय स्कैन — "लघु सर्वज्ञ सिद्धि [आचार्य अनन्तकीर्ति विरचित], सम्पादक पं. कल्लप्पा निटवे" (मुद्रित पृष्ठ १०७–१२७; किसी बड़े संग्रह-ग्रन्थ का अंश)। मूल पाठ स्कैन-छवियों को पढ़कर लिपिबद्ध किया गया है; जहाँ अक्षर अस्पष्ट थे वहाँ [अस्पष्ट] अंकित है। उपलब्ध स्कैन पृष्ठ १२७ पर वाक्य के मध्य समाप्त होता है — अध्ययन से पूर्व मूल पुस्तक से मिलान अवश्य करें।'),
  pNormal('**प्रत्येक अनुच्छेद की संरचना:** १. मूल संस्कृत पाठ → २. हिन्दी अनुवाद → ३. जैनागम के अनुसार विस्तृत व्याख्या → ४. सरल उदाहरण → ५. तुलनात्मक तालिका / चार्ट → ६. सन्दर्भ एवं पाद-टिप्पणी'),
  pNormal('**ग्रन्थ का विषय:** यह कृति केवल तर्क (अनुमान-प्रमाण) के बल पर सर्वज्ञ (केवलज्ञानी) के अस्तित्व की सिद्धि करती है और मीमांसक के "सर्वज्ञ है ही नहीं, वेद अपौरुषेय है" इस पूर्वपक्ष का चरणबद्ध खण्डन करती है। अनुच्छेद-विभाजन (§) एवं शीर्षक व्याख्याकार के हैं, मूल ग्रन्थ के नहीं।'),
  new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 160 }, children: [new TextRun({ text: 'विषय-सूची', bold: true, size: 32, font: FONT, color: '7A1F1F' })] }),
  new TableOfContents('विषय-सूची', { hyperlink: true, headingStyleRange: '1-2' }),
  new Paragraph({ children: [new PageBreak()] })
];

// ---------- assemble ----------
const parts = parseParts();
let body = [];
for (const num of [...parts.keys()].sort((a, b) => a - b)) {
  if (GROUPS[String(num)]) body.push(h1(GROUPS[String(num)]));
  body.push(...renderSection(parts.get(num)));
}
body.push(...renderBackmatter());

const doc = new Document({
  creator: 'JinAagam',
  title: 'लघु-सर्वज्ञ-सिद्धिः — सम्पूर्ण व्याख्या',
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: BODY } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 32, bold: true, color: '7A1F1F' }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 28, bold: true, color: '1F4E79' }, paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 25, bold: true, color: '833C0B' }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 } },
      { id: 'TOC1', name: 'toc 1', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 22, bold: true }, paragraph: { spacing: { before: 100, after: 40 } } },
      { id: 'TOC2', name: 'toc 2', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 20 }, paragraph: { indent: { left: 300 }, spacing: { after: 30 } } },
    ]
  },
  sections: [{
    properties: { page: { size: { width: convertInchesToTwip(8.27), height: convertInchesToTwip(11.69) }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 20, font: FONT })] })] }) },
    children: front.concat(body)
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT_FILE, buf);
  console.log('written:', OUT_FILE, 'bytes:', buf.length, '| sections:', parts.size, '| without addenda:', missing.length ? missing.join(',') : 'none');
});
