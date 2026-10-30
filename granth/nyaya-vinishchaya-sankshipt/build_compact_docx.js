// Compact "verse + gloss" builder: for a sankshipt (condensed) edition distilled from a full
// granth-vyakhya book. Each § has exactly two parts: मूल कारिका (verbatim verse) and विशेषार्थ
// (a short, synthesized gloss) — no addenda/ folder, no 6-part structure.
//
// Usage:  node build_compact_docx.js <work_dir>
//   <work_dir>/meta.json   : title, author line, basis, subject, numerals, out, credits ...
//   <work_dir>/parts/*.md  : "§K — title (सूत्र N.M)" then "## 1. मूल कारिका" / "## 2. विशेषार्थ"
//   <work_dir>/groups.json : { "1": "[ खण्ड-शीर्षक ]", ... }  Heading 1 inserted before §K
//   <work_dir>/frontmatter/*.md, backmatter/*.md (optional)
// Then run finalize_word.ps1 (or finalize_big.py for big books) to update TOC page numbers + PDF.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, TableOfContents,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, convertInchesToTwip,
  Footer, Header, SimpleField, TabStopType, PageNumber, PageBreak
} = require('docx');

const WORK = path.resolve(process.argv[2] || '.');
const META = JSON.parse(fs.readFileSync(path.join(WORK, 'meta.json'), 'utf-8'));
const FONT = META.font || 'Nirmala UI';
const BODY = 24; // 12pt
const PARTS_DIR = path.join(WORK, 'parts');
const FRONT_DIR = path.join(WORK, 'frontmatter');
const BACK_DIR = path.join(WORK, 'backmatter');
const GROUPS = fs.existsSync(path.join(WORK, 'groups.json')) ? JSON.parse(fs.readFileSync(path.join(WORK, 'groups.json'), 'utf-8')) : {};
const OUT_FILE = process.env.OUT || path.resolve(WORK, META.out || path.join('..', 'Vyakhya.docx'));
const EN_NUMERALS = (META.numerals || 'en') === 'en';

const DEV = '०१२३४५६७८९';
const devToInt = s => parseInt(s.replace(/[०-९]/g, d => DEV.indexOf(d)), 10);
const intToDev = n => String(n).replace(/\d/g, d => DEV[d]);
const toEn = t => EN_NUMERALS ? t.replace(/[०-९]/g, d => String(DEV.indexOf(d))) : t;

function parseInline(line) {
  line = line.replace(/`([^`]+)`/g, '$1');
  const out = []; const re = /\*\*(.+?)\*\*|\*([^*\s](?:[^*]*?[^*\s])?)\*/g; let last = 0, m;
  while ((m = re.exec(line)) !== null) {
    if (m.index > last) out.push({ text: line.slice(last, m.index), bold: false });
    if (m[1] !== undefined) out.push({ text: m[1], bold: true });
    else out.push({ text: m[2], bold: false, italics: true });
    last = re.lastIndex;
  }
  if (last < line.length) out.push({ text: line.slice(last), bold: false });
  if (!out.length) out.push({ text: line, bold: false });
  return out;
}
const MOOL_COLOR = '7A1F1F';
const runs = (line, extra) => {
  const keep = extra && extra.color === MOOL_COLOR;
  return parseInline(line).map(r => new TextRun(Object.assign({ text: keep ? r.text : toEn(r.text), bold: r.bold, italics: r.italics, size: BODY, font: FONT }, extra || {})));
};
const pNormal = (line, extra) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 320 }, children: runs(line, extra) });
const pMool = line => new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360 }, spacing: { after: 80, line: 340 }, children: runs(line, { color: MOOL_COLOR }) });
const pEmpty = () => new Paragraph({ text: '', spacing: { after: 60 } });

const h1 = text => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 200 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 32, font: FONT, color: '7A1F1F' })] });
const h2 = text => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 320, after: 140 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 28, font: FONT, color: '1F4E79' })] });
const h3 = text => new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 180, after: 80 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 25, font: FONT, color: '833C0B' })] });

function renderBlock(lines, mool) {
  const out = [];
  for (const raw of lines) {
    const t = raw.replace(/\r$/, '').trim();
    if (t === '' || t === '---') continue;
    out.push(mool ? pMool(t) : pNormal(t));
  }
  return out;
}

// ---------- parse § files ----------
function parseParts() {
  if (!fs.existsSync(PARTS_DIR)) return new Map();
  const files = fs.readdirSync(PARTS_DIR).filter(f => f.endsWith('.md')).sort();
  const map = new Map(); let cur = null, sec = null;
  for (const f of files) {
    for (const raw of fs.readFileSync(path.join(PARTS_DIR, f), 'utf-8').split('\n')) {
      const t = raw.replace(/\r$/, '');
      const m = /^§\s*([०-९0-9]+)\s*[—–-]\s*(.*)$/.exec(t.trim());
      if (m) {
        const num = /[०-९]/.test(m[1]) ? devToInt(m[1]) : parseInt(m[1], 10);
        cur = { num, title: `§ ${EN_NUMERALS ? num : intToDev(num)} — ${m[2].trim()}`, secs: [] };
        if (map.has(num)) console.warn(`WARNING: duplicate §${num} (file ${f}) — later copy overrides`);
        map.set(num, cur); sec = null; continue;
      }
      if (!cur) continue;
      if (t.trim().startsWith('## ')) { sec = { head: t.trim().slice(3).trim(), lines: [] }; cur.secs.push(sec); continue; }
      if (sec) sec.lines.push(t);
    }
  }
  return map;
}
const kind = h => (h.includes('मूल') || h.includes('कारिका')) && !h.includes('विशेष') ? 1 : (h.includes('विशेषार्थ') ? 2 : 0);

const missing = [];
function renderSection(s) {
  const out = [h2(s.title)];
  const byKind = k => s.secs.filter(x => kind(x.head) === k);
  out.push(h3('1. मूल कारिका'));
  const mool = byKind(1);
  if (mool.length) mool.forEach(x => out.push(...renderBlock(x.lines, true))); else out.push(pNormal('[मूल कारिका न मिला — मैन्युअल जाँच ज़रूरी]'));
  out.push(h3('2. विशेषार्थ'));
  const vis = byKind(2);
  if (vis.length) vis.forEach(x => out.push(...renderBlock(x.lines))); else { missing.push(s.num); out.push(pNormal('[विशेषार्थ न मिला]')); }
  out.push(pEmpty());
  return out;
}

function renderMarkdownDir(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const f of fs.readdirSync(dir).filter(f => f.endsWith('.md')).sort()) {
    let buf = [];
    const flush = () => { if (buf.length) out.push(...renderBlock(buf)); buf = []; };
    for (const raw of fs.readFileSync(path.join(dir, f), 'utf-8').split('\n')) {
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

const parts = parseParts();
const center = (text, size, extra) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: extra && extra.after || 120 }, children: [new TextRun(Object.assign({ text: toEn(text), size, font: FONT }, extra || {}))] });
const front = [];
if (META.author_line) front.push(center(META.author_line, 30, { bold: true, after: 60 }));
front.push(center(META.title, 48, { bold: true, color: '7A1F1F', after: 240 }));
if (META.subtitle) front.push(center(META.subtitle.replace('{N}', String(parts.size)), BODY, { after: 200 }));
if (META.basis) front.push(pNormal(`**आधार:** ${META.basis}`));
front.push(pNormal(META.structure || '**प्रत्येक कारिका की संरचना:** 1. मूल कारिका → 2. विशेषार्थ।'));
if (META.subject) front.push(pNormal(`**ग्रन्थ का विषय:** ${META.subject}`));
if (META.credits) front.push(pNormal(`**${META.credits.label || 'संकलन एवं सम्पादन'}:** ${META.credits.value}`));
if (META.disclaimer) front.push(pNormal(META.disclaimer));
front.push(h1('विषय-सूची'));
front.push(new TableOfContents('विषय-सूची', { hyperlink: true, headingStyleRange: '1-2' }));
front.push(new Paragraph({ children: [new PageBreak()] }));
front.push(...renderMarkdownDir(FRONT_DIR));

const body = [];
for (const num of [...parts.keys()].sort((a, b) => a - b)) {
  if (GROUPS[String(num)]) body.push(h1(GROUPS[String(num)]));
  body.push(...renderSection(parts.get(num)));
}
body.push(...renderMarkdownDir(BACK_DIR));

const RUNNING_HEAD = META.running_title || META.title;
const runHeader = new Header({ children: [new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: 9270 }],
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: '999999', space: 2 } },
  children: [
    new TextRun({ text: RUNNING_HEAD, size: 18, color: '555555', font: FONT }),
    new TextRun({ text: '\t', size: 18, font: FONT }),
    new SimpleField('STYLEREF "Heading 1"', ''),
  ] })] });

const doc = new Document({
  creator: META.creator || 'JinAagam',
  title: META.title,
  features: { updateFields: true },
  styles: {
    default: {
      document: { run: { font: FONT, size: BODY } },
      heading1: { run: { font: FONT, size: 32, bold: true, color: '7A1F1F' }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0, keepNext: true } },
      heading2: { run: { font: FONT, size: 28, bold: true, color: '1F4E79' }, paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 1, keepNext: true } },
      heading3: { run: { font: FONT, size: 25, bold: true, color: '833C0B' }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2, keepNext: true } },
    },
    paragraphStyles: [
      { id: 'TOC1', name: 'toc 1', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 22, bold: true }, paragraph: { spacing: { before: 100, after: 40 } } },
      { id: 'TOC2', name: 'toc 2', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 20 }, paragraph: { indent: { left: 300 }, spacing: { after: 30 } } },
    ]
  },
  sections: [{
    properties: { page: { size: { width: convertInchesToTwip(8.27), height: convertInchesToTwip(11.69) }, margin: { top: 900, bottom: 900, left: 1000, right: 1000 } } },
    headers: { default: runHeader },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 20, font: FONT })] })] }) },
    children: front.concat(body)
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT_FILE, buf);
  console.log('written:', OUT_FILE, '| bytes:', buf.length, '| §:', parts.size, '| § without विशेषार्थ:', missing.length ? missing.join(',') : 'none');
});
