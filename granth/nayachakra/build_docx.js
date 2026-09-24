// Generic ग्रन्थ-व्याख्या builder: markdown parts -> .docx (TOC + page-number footer + Heading styles).
// Format = Pramana_Pariksha_Sampurna_Vyakhya standard (6 parts per §, खण्ड headers, back matter).
//
// Usage:  node build_docx.js <work_dir>
//   <work_dir>/meta.json      : title, author line, basis, subject, numerals ("en"|"dev"), out, credits ...
//   <work_dir>/parts/*.md     : § files  — "§N — title" line, then "## १. मूल ..." sub-sections, bullets, tables
//   <work_dir>/addenda/sNN.md : per-§ supplements (## 3. पूरक व्याख्या | ## 4. सरल उदाहरण | ## 5. तुलनात्मक तालिका | ## 6. सन्दर्भ)
//   <work_dir>/groups.json    : { "1": "[ खण्ड-शीर्षक ]", ... }  Heading 1 inserted before §N
//   <work_dir>/frontmatter/*.md (optional) : भूमिका etc. — "# " Heading 1, placed after TOC
//   <work_dir>/backmatter/*.md  : ग्रन्थ-सार, परिशिष्ट, सन्दर्भ-सूची, शब्दावली — "# " / "## " / "### "
// Then run finalize_word.ps1 to update TOC page numbers and export the PDF (Word COM; LibreOffice cannot).

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, TableOfContents,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, convertInchesToTwip,
  Footer, PageNumber, PageBreak
} = require('docx');

const WORK = path.resolve(process.argv[2] || '.');
const META = JSON.parse(fs.readFileSync(path.join(WORK, 'meta.json'), 'utf-8'));
const FONT = META.font || 'Nirmala UI';
const BODY = 24; // 12pt
const PARTS_DIR = path.join(WORK, 'parts');
const ADD_DIR = path.join(WORK, 'addenda');
const FRONT_DIR = path.join(WORK, 'frontmatter');
const BACK_DIR = path.join(WORK, 'backmatter');
const GROUPS = fs.existsSync(path.join(WORK, 'groups.json')) ? JSON.parse(fs.readFileSync(path.join(WORK, 'groups.json'), 'utf-8')) : {};
const OUT_FILE = process.env.OUT || path.resolve(WORK, META.out || path.join('vyakhya', 'Vyakhya.docx'));
const EN_NUMERALS = (META.numerals || 'en') === 'en';

const DEV = '०१२३४५६७८९';
const devToInt = s => parseInt(s.replace(/[०-९]/g, d => DEV.indexOf(d)), 10);
const intToDev = n => String(n).replace(/\d/g, d => DEV[d]);
// English numerals everywhere except inside मूल text (verse numbers like ॥१२॥ stay Devanagari there).
const toEn = t => EN_NUMERALS ? t.replace(/[०-९]/g, d => String(DEV.indexOf(d))) : t;

// ---------- inline / paragraph helpers ----------
function parseInline(line) {
  const out = []; const re = /\*\*(.+?)\*\*/g; let last = 0, m;
  while ((m = re.exec(line)) !== null) {
    if (m.index > last) out.push({ text: line.slice(last, m.index), bold: false });
    out.push({ text: m[1], bold: true }); last = re.lastIndex;
  }
  if (last < line.length) out.push({ text: line.slice(last), bold: false });
  if (!out.length) out.push({ text: line, bold: false });
  return out;
}
const MOOL_COLOR = '7A1F1F';
const runs = (line, extra) => {
  const keep = extra && extra.color === MOOL_COLOR;
  return parseInline(line).map(r => new TextRun(Object.assign({ text: keep ? r.text : toEn(r.text), bold: r.bold, size: BODY, font: FONT }, extra || {})));
};
const pNormal = (line, extra) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 320 }, children: runs(line, extra) });
const pBullet = line => new Paragraph({ bullet: { level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 320 }, children: runs(line) });
const pQuote = line => new Paragraph({
  indent: { left: 360 }, border: { left: { style: BorderStyle.SINGLE, size: 12, color: '1F4E79', space: 8 } },
  shading: { type: ShadingType.CLEAR, fill: 'EDF2F7' }, spacing: { after: 120, before: 80, line: 320 }, children: runs(line, { italics: true })
});
const pMool = line => new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360 }, spacing: { after: 80, line: 340 }, children: runs(line, { color: MOOL_COLOR }) });
const pEmpty = () => new Paragraph({ text: '', spacing: { after: 60 } });

// keepNext on every heading: a heading must never sit alone at the bottom of a page.
const h1 = text => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 200 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 32, font: FONT, color: '7A1F1F' })] });
const h2 = text => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 320, after: 140 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 28, font: FONT, color: '1F4E79' })] });
const h3 = text => new Paragraph({ heading: HeadingLevel.HEADING_3, spacing: { before: 180, after: 80 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 25, font: FONT, color: '833C0B' })] });

function buildTable(rows) {
  const n = Math.max(...rows.map(r => r.length)); const w = Math.floor(9200 / n);
  const widths = n === 2 ? [3200, 6000] : Array.from({ length: n }, () => w);
  const trs = rows.map((cells, ri) => new TableRow({
    tableHeader: ri === 0,
    children: Array.from({ length: n }, (_, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA },
      shading: ri === 0 ? { type: ShadingType.CLEAR, fill: 'DCE6F1' } : undefined,
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [new Paragraph({ spacing: { after: 20, line: 280 }, children: parseInline(cells[ci] || '').map(r => new TextRun({ text: toEn(r.text), bold: ri === 0 || r.bold, size: BODY - 3, font: FONT })) })]
    }))
  }));
  return new Table({ width: { size: 9200, type: WidthType.DXA }, columnWidths: widths, rows: trs });
}

// ---------- generic block renderer ----------
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
    if (t.startsWith('- ') || t.startsWith('• ') || t.startsWith('* ')) { out.push(pBullet(t.slice(2))); continue; }
    if (t.startsWith('#### ')) { out.push(pNormal(t.slice(5), { bold: true })); continue; }
    out.push(mool ? pMool(t) : pNormal(t));
  }
  flush(); return out;
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
function parseAddendum(num) {
  // addenda may be named s07.md, s007.md or s7.md — accept any zero-padding
  const f = [3, 2, 1].map(w => path.join(ADD_DIR, `s${String(num).padStart(w, '0')}.md`)).find(fs.existsSync);
  if (!f) return null;
  const secs = []; let sec = null;
  for (const raw of fs.readFileSync(f, 'utf-8').split('\n')) {
    const t = raw.replace(/\r$/, '');
    if (t.trim().startsWith('## ')) { sec = { head: t.trim().slice(3).trim(), lines: [] }; secs.push(sec); continue; }
    if (sec) sec.lines.push(t);
  }
  return secs;
}
// Classify a sub-section heading into one of the six parts (by keyword, so numbering style doesn't matter).
const kind = h => {
  if (h.includes('छाया')) return 2;
  if (h.includes('अन्वयार्थ')) return 4;
  if (h.includes('अन्वय')) return 3;
  if (h.includes('मूल')) return 1;
  if (h.includes('अनुवाद') || h.includes('भावार्थ')) return 5;
  if (h.includes('पूरक')) return 6.5;
  if (h.includes('व्याख्या') || h.includes('विश्लेषण') || h.includes('विवेचन')) return 6;
  if (h.includes('उदाहरण')) return 7;
  if (h.includes('तुलनात्मक') || h.includes('तालिका') || h.includes('सारणी') || h.includes('वर्गीकरण') || h.includes('चार्ट')) return 8;
  if (h.includes('सन्दर्भ') || h.includes('टिप्पणी') || h.includes('पाठान्तर')) return 9;
  if (h.includes('सार') || h.includes('नोट')) return 6.5;
  return 0;
};

// Sub-sections that are working notes for the next batch, not book content. They are dropped (with a
// warning) so process language never reaches the reader.
const WORKNOTE = /आगे की दिशा|अगले बैच|अगली बैठक|बैच|progress|TODO/;
const missing = [], dropped = [];
function renderSection(s) {
  const out = [h2(s.title)];
  const add = parseAddendum(s.num) || [];
  if (!add.length) missing.push(s.num);
  const all = [...s.secs, ...add].filter(x => { if (WORKNOTE.test(x.head)) { dropped.push(`§${s.num}: ${x.head}`); return false; } return true; });
  const byKind = k => all.filter(x => kind(x.head) === k);
  const misc = all.filter(x => kind(x.head) === 0 && s.secs.includes(x));
  const pg = x => { const m = /\((पृष्ठ[^)]*)\)/.exec(x.head); return m ? [pNormal(`**(${m[1]})**`)] : []; };

  out.push(h3('1. मूल पाठ (प्राकृत गाथा)'));
  byKind(1).forEach(x => out.push(...pg(x), ...renderBlock(x.lines, true)));
  out.push(h3('2. संस्कृत छाया'));
  const ch = byKind(2);
  if (ch.length) ch.forEach(x => out.push(...renderBlock(x.lines, true))); else out.push(pNormal('इस अनुच्छेद का मूल पाठ संस्कृत में ही है; पृथक् छाया अनावश्यक।'));
  out.push(h3('3. अन्वय'));
  const an = byKind(3);
  if (an.length) an.forEach(x => out.push(...renderBlock(x.lines, true))); else out.push(pNormal('इस अनुच्छेद हेतु पृथक् अन्वय आवश्यक नहीं।'));
  out.push(h3('4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ)'));
  const aa = byKind(4);
  if (aa.length) aa.forEach(x => out.push(...renderBlock(x.lines))); else out.push(pNormal('इस अनुच्छेद हेतु पृथक् अन्वयार्थ आवश्यक नहीं।'));
  out.push(h3('5. हिन्दी अनुवाद'));
  byKind(5).forEach(x => out.push(...pg(x), ...renderBlock(x.lines)));
  out.push(h3('6. जैनागम के अनुसार विस्तृत व्याख्या'));
  byKind(6).forEach(x => out.push(...renderBlock(x.lines)));
  byKind(6.5).forEach(x => out.push(...renderBlock(x.lines)));
  out.push(h3('7. सरल उदाहरण'));
  const ex = byKind(7);
  if (ex.length) ex.forEach(x => out.push(...renderBlock(x.lines))); else out.push(pNormal('इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।'));
  out.push(h3('8. तुलनात्मक तालिका / चार्ट'));
  const tb = byKind(8);
  if (tb.length) tb.forEach(x => out.push(...renderBlock(x.lines))); else out.push(pNormal('इस अनुच्छेद हेतु तालिका आवश्यक नहीं।'));
  out.push(h3('9. सन्दर्भ एवं पाद-टिप्पणी'));
  const rf = byKind(9);
  rf.forEach(x => out.push(...renderBlock(x.lines)));
  misc.forEach(x => { out.push(pNormal(`**${x.head.replace(/^[०-९0-9]+\.\s*/, '')}:**`)); out.push(...renderBlock(x.lines)); });
  if (!rf.length && !misc.length) out.push(pBullet('मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।'));
  out.push(pEmpty());
  return out;
}

// ---------- free markdown (front/back matter) ----------
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

// ---------- front matter (from meta.json) ----------
const parts = parseParts();
const center = (text, size, extra) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: extra && extra.after || 120 }, children: [new TextRun(Object.assign({ text: toEn(text), size, font: FONT }, extra || {}))] });
const front = [];
if (META.author_line) front.push(center(META.author_line, 30, { bold: true, after: 60 }));
front.push(center(META.title, 48, { bold: true, color: '7A1F1F', after: 240 }));
if (META.subtitle) front.push(center(META.subtitle.replace('{N}', String(parts.size)), BODY, { after: 200 }));
if (META.basis) front.push(pNormal(`**आधार:** ${META.basis}`));
front.push(pNormal(META.structure || '**प्रत्येक अनुच्छेद की संरचना:** 1. मूल पाठ → 2. हिन्दी अनुवाद → 3. जैनागम के अनुसार विस्तृत व्याख्या → 4. सरल उदाहरण → 5. तुलनात्मक तालिका / चार्ट → 6. सन्दर्भ एवं पाद-टिप्पणी'));
if (META.subject) front.push(pNormal(`**ग्रन्थ का विषय:** ${META.subject}`));
if (META.credits) front.push(pNormal(`**${META.credits.label || 'संकलन एवं सम्पादन'}:** ${META.credits.value}`));
if (META.disclaimer) front.push(pNormal(META.disclaimer));
front.push(h1('विषय-सूची'));
front.push(new TableOfContents('विषय-सूची', { hyperlink: true, headingStyleRange: '1-2' }));
front.push(new Paragraph({ children: [new PageBreak()] }));
front.push(...renderMarkdownDir(FRONT_DIR));

// ---------- assemble ----------
const body = [];
for (const num of [...parts.keys()].sort((a, b) => a - b)) {
  if (GROUPS[String(num)]) body.push(h1(GROUPS[String(num)]));
  body.push(...renderSection(parts.get(num)));
}
body.push(...renderMarkdownDir(BACK_DIR));

const doc = new Document({
  creator: META.creator || 'JinAagam',
  title: META.title,
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: FONT, size: BODY } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 32, bold: true, color: '7A1F1F' }, paragraph: { spacing: { before: 240, after: 200 }, outlineLevel: 0, keepNext: true } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 28, bold: true, color: '1F4E79' }, paragraph: { spacing: { before: 320, after: 140 }, outlineLevel: 1, keepNext: true } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 25, bold: true, color: '833C0B' }, paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2, keepNext: true } },
      { id: 'TOC1', name: 'toc 1', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 22, bold: true }, paragraph: { spacing: { before: 100, after: 40 } } },
      { id: 'TOC2', name: 'toc 2', basedOn: 'Normal', next: 'Normal', run: { font: FONT, size: 20 }, paragraph: { indent: { left: 300 }, spacing: { after: 30 } } },
    ]
  },
  sections: [{
    properties: { page: { size: { width: convertInchesToTwip(8.27), height: convertInchesToTwip(11.69) }, margin: { top: 900, bottom: 900, left: 1000, right: 1000 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 20, font: FONT })] })] }) },
    children: front.concat(body)
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT_FILE, buf);
  console.log('written:', OUT_FILE, '| bytes:', buf.length, '| §:', parts.size, '| § without addenda:', missing.length ? missing.join(',') : 'none');
  if (dropped.length) console.log('dropped working-note sub-sections (not book content):\n  ' + dropped.join('\n  '));
});
