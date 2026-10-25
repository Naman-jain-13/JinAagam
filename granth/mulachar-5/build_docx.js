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
  Footer, Header, SimpleField, TabStopType, PageNumber, PageBreak
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
// English digits outside मूल text — but a verse number sitting inside dandas (॥१७॥) is quoted मूल
// wherever it appears, including in the अन्वयार्थ's closing "॥१७॥ = गाथा-क्रमांक" line, so it keeps
// its Devanagari digits. Without this guard that line rendered as the half-converted "॥17॥".
const toEn = t => EN_NUMERALS
  ? t.split(/(॥[^॥]*॥)/).map((seg, i) =>
      i % 2 ? seg : seg.replace(/[०-९]/g, d => String(DEV.indexOf(d)))).join('')
  : t;

// ---------- inline / paragraph helpers ----------
// **bold** and *italic*. The single-asterisk arm matters: the व्याख्या marks *दार्ष्टान्तिक*, *सीमा* and
// ग्रन्थ names that way — 700 spans across 159 files — and without it the asterisks print literally.
// The guards (?<![*\w]) … (?!\s) … (?<!\s) … (?![*\w]) stop it firing on ** delimiters or on an asterisk
// used as a footnote mark. Nested emphasis (*italic* inside **bold**) is NOT supported — the bold arm
// wins and the inner asterisks would print literally; write the inner phrase in ‘ ’ quotes instead.
function parseInline(line) {
  const out = [];
  // The third arm is for `backtick` spans. The व्याख्या cites a Sanskrit word or a printed reading
  // that way; without this the backticks printed literally (34 of them reached a build).
  // They render as italics, like *emphasis*, which is what a cited form wants.
  const re = /\*\*(.+?)\*\*|(?<![*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![*\w])|`([^`\n]+?)`/g;
  let last = 0, m;
  while ((m = re.exec(line)) !== null) {
    if (m.index > last) out.push({ text: line.slice(last, m.index), bold: false });
    if (m[1] !== undefined) out.push({ text: m[1], bold: true });
    else out.push({ text: m[2] !== undefined ? m[2] : m[3], bold: false, italics: true });
    last = re.lastIndex;
  }
  if (last < line.length) out.push({ text: line.slice(last), bold: false });
  if (!out.length) out.push({ text: line, bold: false });
  return out;
}
const MOOL_COLOR = '7A1F1F';
const runs = (line, extra) => {
  const keep = extra && extra.color === MOOL_COLOR;
  // पाद-टिप्पणी के अंक [१] / [*] पाठ में ऊपर-अंक (superscript) बनकर छपते हैं, ताकि पाठक देख सके कि कौन-सी
  // टिप्पणी किस शब्द पर है।
  const pieces = [];
  parseInline(line).forEach(r => {
    if (r.bold) { pieces.push(r); return; }
    r.text.split(/(\[[०-९0-9*]{1,3}\])/).forEach(part => {
      if (!part) return;
      const m = /^\[([०-९0-9*]{1,3})\]$/.exec(part);
      if (m) pieces.push({ text: m[1], bold: false, italics: !!r.italics, sup: true });
      else pieces.push({ text: part, bold: false, italics: !!r.italics });
    });
  });
  return pieces.map(r => new TextRun(Object.assign({ text: keep || r.sup ? r.text : toEn(r.text), bold: r.bold, italics: !!r.italics, size: BODY, font: FONT, superScript: !!r.sup }, extra || {})));
};
const pNormal = (line, extra) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 320 }, children: runs(line, extra) });
const pBullet = line => new Paragraph({ bullet: { level: 0 }, alignment: AlignmentType.JUSTIFIED, spacing: { after: 80, line: 320 }, children: runs(line) });
const pQuote = line => new Paragraph({
  indent: { left: 360 }, border: { left: { style: BorderStyle.SINGLE, size: 12, color: '1F4E79', space: 8 } },
  shading: { type: ShadingType.CLEAR, fill: 'EDF2F7' }, spacing: { after: 120, before: 80, line: 320 }, children: runs(line, { italics: true })
});
const pMool = line => new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360 }, spacing: { after: 80, line: 340 }, children: runs(line, { color: MOOL_COLOR }) });
// मूल पाठ — दोहा और उसकी संस्कृत छाया — शेष पाठ से एक आकार बड़ा और गहरा।
// पाठक ने कहा: "मूल संस्कृत पाठ bold करना है" तथा "मूल पाठ की बाकी पाठ से font size
// 1 size बड़ी रखनी है"। अब इनके ऊपर कोई शीर्षक नहीं रहा, इसलिए यही भार उन्हें
// पृष्ठ पर अलग पहचान देता है।
const pMoolBig = line => new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360 }, spacing: { after: 80, line: 360 }, children: runs(line, { color: MOOL_COLOR, bold: true, size: BODY + 2 }) });
// संस्कृत छाया — पाठक के कहने पर बाकी पाठ से छोटे आकार में (गाथा के नीचे सहायक पंक्ति की तरह)।
const pChhaya = line => new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360 }, spacing: { after: 60, line: 280 }, children: runs(line, { color: MOOL_COLOR, size: BODY - 4 }) });
// मुद्रित पाद-टिप्पणी — छोटे आकार में।
const pNote = line => new Paragraph({ alignment: AlignmentType.LEFT, indent: { left: 360 }, spacing: { after: 30, line: 240 }, children: runs(line, { size: 17, color: '444444' }) });
const pEmpty = () => new Paragraph({ text: '', spacing: { after: 60 } });

// keepNext on every heading: a heading must never sit alone at the bottom of a page.
const h1 = text => new Paragraph({ heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 200 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 32, font: FONT, color: '7A1F1F' })] });
const h2 = text => new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 320, after: 140 }, keepNext: true, children: [new TextRun({ text: toEn(text), bold: true, size: 28, font: FONT, color: '1F4E79' })] });
// दोहा-हेडिंग — दिखता वही "अधिकार 1, दोहा 47" रहता है, पर उसके बाद एक छुपी run में TOC_MARKER +
// विषय जोड़ दिया जाता है (देखें topicOf ऊपर) ताकि विषय-सूची में दोहा-क्रमांक के साथ विषय भी दिखे।
const h2Doha = (text, topic) => {
  const children = [new TextRun({ text: toEn(text), bold: true, size: 28, font: FONT, color: '1F4E79' })];
  if (topic) children.push(new TextRun({ text: TOC_MARKER + toEn(topic), vanish: true, size: 2, font: FONT }));
  return new Paragraph({ heading: HeadingLevel.HEADING_2, spacing: { before: 320, after: 140 }, keepNext: true, children });
};
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
      // पंक्ति-विभाजक को हर कोष्ठ पर अलग जाँचिए, जोड़कर नहीं। जोड़ने पर
      // |---|---:|---| का जुड़ा रूप "------:---" बनता है, जिसमें बिन्दु बीच में
      // पड़ जाता है और जाँच विफल हो जाती है — तब विभाजक ही एक पंक्ति बनकर छप
      // जाता है। संरेखण-चिह्न वाली हर तालिका इसी से टूटती थी।
      if (cells.length && cells.every(c => /^:?-{2,}:?$/.test(c.trim()))) continue;
      (tbl = tbl || []).push(cells); continue;
    }
    flush();
    if (mool === 'small' || mool === 'note') { out.push(mool === 'small' ? pChhaya(t) : pNote(t.replace(/^[-•*]\s+/, ''))); continue; }
    if (t.startsWith('> ')) { out.push(pQuote(t.slice(2))); continue; }
    if (t.startsWith('- ') || t.startsWith('• ') || t.startsWith('* ')) { out.push(pBullet(t.slice(2))); continue; }
    if (t.startsWith('#### ')) { out.push(pNormal(t.slice(5), { bold: true })); continue; }
    out.push(mool === 'small' ? pChhaya(t) : mool === 'note' ? pNote(t.replace(/^[-•*]\s+/, '')) : mool === 'big' ? pMoolBig(t) : mool ? pMool(t) : pNormal(t));
  }
  flush(); return out;
}

// This ग्रन्थ has THREE independent दोहा numberings — परमात्मप्रकाश अधिकार 1, अधिकार 2, and योगसार —
// so a § key cannot simply be the दोहा number as it is in a single-sequence text. The key encodes all
// three parts, which lets every agent compute its own keys with no coordination and no collisions:
//
//     key = अधिकार-base + दोहा x 10 + star
//     base: 10000 = परमात्मप्रकाश अ. 1 | 20000 = परमात्मप्रकाश अ. 2 | 30000 = योगसार
//     star: 0 normally; for an extra दोहा printed as "123*2" the star digit is 2
//
// so अ.1 दोहा 17 is 10170, अ.2 दोहा 39 is 20390, योगसार दोहा 29 is 30290, अ.1 दोहा 123*2 is 11232.
// Keys sort into reading order. The reader never sees them — sectionLabel turns each back into the
// reference actually printed in the book.
function sectionLabel(num) {
  const g = Math.floor(num / 10), star = num % 10;
  return `मूलाचार, गाथा ${g}${star ? '*' + star : ''}`;
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
        cur = { num, title: `${sectionLabel(num)} — ${m[2].trim()}`, secs: [] };
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
  if (h.includes('युक्तिसंगत') || h.includes('उद्देश्य')) return 7.6;   // क्रिया का तर्कसंगत प्रयोजन
  if (h.includes('आचरण-विधि') || h.includes('अभ्यास')) return 9.5;      // साधु-जीवन में उतारने की विधि
  if (h.includes('छाया')) return 2;
  if (h.includes('अन्वयार्थ')) return 4;
  if (h.includes('अन्वय')) return 3;
  if (h.includes('पाठभेद')) return 6;       // योगसार has no टीका; its slot 6 carries the edition's पाठान्तर
  if (h.includes('टीका')) return 6;          // before 'अनुवाद' — part 6's heading contains both
  if (h.includes('मूल')) return 1;
  if (h.includes('अनुवाद') || h.includes('भावार्थ')) return 5;
  if (h.includes('पूरक')) return 7.5;
  if (h.includes('व्याख्या') || h.includes('विश्लेषण') || h.includes('विवेचन')) return 7;
  if (h.includes('उदाहरण')) return 8;
  if (h.includes('तुलनात्मक') || h.includes('तालिका') || h.includes('सारणी') || h.includes('वर्गीकरण') || h.includes('चार्ट')) return 9;
  if (h.includes('सन्दर्भ') || h.includes('पाद-टिप्पणी') || h.includes('पाठान्तर')) return 10;
  if (h.includes('सार') || h.includes('नोट')) return 7.5;
  return 0;
};

// Sub-sections that are working notes for the next batch, not book content. They are dropped (with a
// warning) so process language never reaches the reader.
// Part 6 carries श्री ब्रह्मदेव's Sanskrit टीका and its Hindi.
//
// The Sanskrit is transcribed once, in parts/, under a heading containing "मूल", with each segment
// tagged (T1), (T2) … The Hindi is written separately, in addenda/, against the SAME tags, so the
// व्याख्या agent never re-types a word of Sanskrit — re-typing 450 dense Sanskrit commentaries is
// precisely where mistranslation gets a foothold.
//
// The printed form has changed twice, both times at the reader's word.
//
// First it was segment by segment — a Sanskrit line, then its Hindi directly beneath — so that a
// Sanskrit reader could check each line against its translation. He asked for the Sanskrit whole and
// the Hindi whole instead. Then, seeing that, he asked for the segments themselves to go:
// "T11, T12, … ऐसे टीका जो है उनको merge करदो, और उनके हिंदी अर्थ को भी merge करदो."
//
// So the टीका is now what श्री ब्रह्मदेव wrote: continuous prose. The (T…) division was never his —
// it is a transcription convenience, used to pair each Sanskrit segment with its Hindi without
// re-typing a word of Sanskrit. That pairing still happens here; it simply no longer shows.
//
// The tags therefore survive in the SOURCE and are still what addenda are written against. What they
// no longer do is anchor a citation: parts 7–10 used to say "(T11) में संस्कृत …", and those
// references were rewritten to quote the words instead, which a reader can actually find in flowing
// prose.
const TAG = /^\s*\((T\d+)\)\s*/;
// स्रोत में टीका के बाद "---" की पंक्ति पड़ी रहती है — markdown का विभाजक, पुस्तक का अंग नहीं।
// बिना टैग वाली हर पंक्ति चालू खण्ड में जुड़ जाती है, इसलिए वह अन्तिम खण्ड की पूँछ बनकर छप रही
// थी: "॥ २ ॥ ---"। पूरी पुस्तक में 304 जगह।
const RULE = /^\s*(-{3,}|_{3,}|\*{3,})\s*$/;
function splitTagged(secs) {
  const map = new Map(); let cur = null;
  for (const sec of secs) for (const raw of sec.lines) {
    const t = raw.replace(/\r$/, '');
    if (RULE.test(t)) continue;
    const m = TAG.exec(t);
    if (m) { cur = m[1]; map.set(cur, [t.replace(TAG, '')]); }
    else if (cur && t.trim()) map.get(cur).push(t);
  }
  return map;
}
function renderTika(secs) {
  const sans = splitTagged(secs.filter(x => x.head.includes('मूल')));
  const hind = splitTagged(secs.filter(x => !x.head.includes('मूल')));
  if (!sans.size && !hind.size) return [pNormal('मुद्रित प्रति में इस गाथा पर पृथक् वृत्ति नहीं है।')];
  const out = [];
  const keys = [...new Set([...sans.keys(), ...hind.keys()])]
    .sort((a, b) => parseInt(a.slice(1), 10) - parseInt(b.slice(1), 10));
  const join = m => keys.map(k => (m.get(k) || []).join(' ').trim()).filter(Boolean).join(' ');
  if (sans.size) {
    out.push(pNormal('**संस्कृत आचारवृत्ति —**'));
    out.push(...renderBlock([join(sans)], true));
  }
  if (hind.size) {
    out.push(pNormal('**हिन्दी अनुवाद —**'));
    out.push(...renderBlock([join(hind)]));
    // एक भी खण्ड का अनुवाद छूटा हो तो वह चुपचाप न निकले — पुस्तक में ही कह दिया जाए।
    const gaps = keys.filter(k => sans.get(k) && !hind.get(k));
    if (gaps.length) out.push(pNormal(`[वृत्ति के ${gaps.length} खण्डों का हिन्दी अनुवाद उपलब्ध नहीं]`));
  }
  return out;
}

const WORKNOTE = /आगे की दिशा|अगले बैच|अगली बैठक|बैच|progress|TODO/;
const missing = [], dropped = [];
// § का शीर्षक: वर्णनात्मक नाम और मुद्रित-पृष्ठ दोनों हटाकर केवल पहचान-सूत्र।
//
// पहले यह था — "§10020 — भविष्य में महाविदेह आदि क्षेत्रों में सिद्ध होने वाले अनंत जीवों को
// नमस्कार, जो … (अधिकार 1, दोहा 2, मुद्रित पृष्ठ 8-9)"। पाठक ने कहा कि भाग 1 पर दिया टाइटल और
// पेज नंबर हटा दिया जाए। दोहा अपनी बात स्वयं कहता है; उससे पहले उसका सारांश पढ़ाना बाधा थी।
//
// जो बचता है वही है जिससे दोहा उद्धृत किया जाता है — "अधिकार 1, दोहा 2" (योगसार में
// "योगसार, दोहा 5")। विषय-सूची भी इसी से बनती है, और वही परम्परागत उद्धरण-रीति है।
const titleOf = t => {
  const m = /\(((?:अधिकार|मूलगुणाधिकार)[^)]*?)(?:,\s*मुद्रित पृष्ठ[^)]*)?\)\s*$/.exec(t);
  if (m) return m[1].trim();
  const n = /^§\s*(\d+)/.exec(t);
  return n ? `§${n[1]}` : t;
};
// वही वर्णनात्मक वाक्य जो titleOf() ऊपर हटाता है — पाठक ने index/विषय-सूची में इसे दोहा-सन्दर्भ के
// साथ वापस चाहा (पाठ के ऊपर वाली हेडिंग में नहीं, सिर्फ़ TOC में)। इसे एक छुपी (vanish) run में
// हेडिंग पैराग्राफ़ के भीतर ही रख देते हैं — दिखती कहीं नहीं, पर finalize_big.py की TOC-हार्वेस्टिंग
// (जो पैराग्राफ़ के सारे <w:t> पढ़ती है, run-formatting से बेख़बर) इसे उठा लेती है।
const TOC_MARKER = '␟';
// एक लम्बा विषय-वाक्य पूरी पंक्ति भर देता है और डॉट-लीडर+पृष्ठ-संख्या के लिए जगह ही नहीं बचती —
// तब Word पृष्ठ-संख्या को बिना डॉट्स के अगली पंक्ति पर अकेला छोड़ देता है (देखा गया: 108-अक्षर
// वाला विषय ऐसा करता है)। साथ ही पाठक ने "topic ka naam" माँगा था, पूरा वाक्य नहीं — इसलिए छोटा
// रखना दोनों दृष्टि से सही है।
const TOPIC_MAX = 40;
const topicOf = t => {
  const body = t.replace(/^[^—]*—\s*/, '');
  const m = /^(.*?)\s*\((?:अधिकार|मूलगुणाधिकार)[^)]*\)\s*$/.exec(body);
  let topic = m ? m[1].trim() : '';
  if (topic.length > TOPIC_MAX) {
    let cut = topic.slice(0, TOPIC_MAX);
    const lastSpace = cut.lastIndexOf(' ');
    if (lastSpace > TOPIC_MAX * 0.5) cut = cut.slice(0, lastSpace);
    topic = cut.trim() + '…';
  }
  return topic;
};
// मूल पाठ के भीतर भी "(पृष्ठ 8)" जैसी पंक्ति पड़ी रहती है — वह भी पृष्ठ-संकेत ही है, वही हटाना है।
const PAGELINE = /^\s*\(\s*पृष्ठ[^)]*\)\s*$/;

function renderSection(s) {
  const out = [h2Doha(titleOf(s.title), topicOf(s.title))];
  const add = parseAddendum(s.num) || [];
  if (!add.length) missing.push(s.num);
  const all = [...s.secs, ...add].filter(x => { if (WORKNOTE.test(x.head)) { dropped.push(`§${s.num}: ${x.head}`); return false; } return true; });
  const byKind = k => all.filter(x => kind(x.head) === k);
  const misc = all.filter(x => kind(x.head) === 0 && s.secs.includes(x));
  const pg = x => { const m = /\((पृष्ठ[^)]*)\)/.exec(x.head); return m ? [pNormal(`**(${m[1]})**`)] : []; };

  // दोहा, छाया और हिन्दी अनुवाद एक ही प्रवाह में — बीच में कोई शीर्षक नहीं।
  //
  // पाठक का कहना था: "१ नम्बर पे जो टाइटल और पेज नंबर दिया है वो हटा दीजिए" और "२ नंबर, ३ नंबर,
  // ५ नंबर, इनकी हैडिंग भी हटा दो।" ये तीनों एक ही दोहा के तीन रूप हैं — मूल, छाया, अनुवाद — और
  // इन्हें शीर्षक से तोड़ना पढ़ने में बाधा ही था। अब ये लगातार पढ़े जाते हैं।
  //
  // अन्वय (भाग 3) और अन्वयार्थ (भाग 4) अब छपते नहीं — "अन्वयार्थ पदच्छेद सहित वाला पार्ट नहीं
  // चाइए" और "३ नंबर में जो दोहा का अन्वय किया है वो भी हटा दीजिए"। स्रोत में सामग्री यथावत् है,
  // केवल छपती नहीं; लौटानी हो तो यहीं से लौट आएगी।
  byKind(1).forEach(x => out.push(...renderBlock(x.lines.filter(l => !PAGELINE.test(l)), 'big')));
  // संस्कृत छाया व्याख्याकार-कृत है — यह बात भूमिका में एक बार कही गई है, प्रत्येक गाथा पर दोहराई नहीं जाती।
  byKind(2).forEach(x => out.push(...renderBlock(x.lines, 'small')));
  // स्रोत की छपी हुई हिन्दी (parts/ का भाग 5) इस पुस्तक में नहीं छपती: पाठक को केवल व्याख्याकार का स्वतन्त्र
  // अनुवाद चाहिए, किसी मौजूदा अनुवाद का प्रभाव नहीं। यहाँ केवल addenda/ का अपना भाग 5 (गाथा का स्वतन्त्र
  // हिन्दी अनुवाद) छपता है।
  byKind(5).filter(x => add.includes(x)).forEach(x => out.push(...renderBlock(x.lines)));
  out.push(h3('श्री वसुनन्दि-कृत संस्कृत आचारवृत्ति एवं उसका हिन्दी अनुवाद'));
  out.push(...renderTika(byKind(6)));
  // मुद्रित पाद-टिप्पणी पाठ के ठीक नीचे — पाठ में उनके ऊपर-अंक जहाँ लगे हैं वहीं से पहचानी जा सकें।
  if (misc.length) {
    out.push(pNormal('**मुद्रित पाद-टिप्पणी (ऊपर के पाठ के अंकों की):**'));
    misc.forEach(x => out.push(...renderBlock(x.lines, 'note')));
  }
  out.push(h3('जैनागम के अनुसार विस्तृत व्याख्या'));
  byKind(7).forEach(x => out.push(...renderBlock(x.lines)));
  byKind(7.5).forEach(x => out.push(...renderBlock(x.lines)));
  const yk = byKind(7.6);
  if (yk.length) { out.push(h3('क्रिया का युक्तिसंगत उद्देश्य')); yk.forEach(x => out.push(...renderBlock(x.lines))); }
  out.push(h3('सरल उदाहरण'));
  const ex = byKind(8);
  if (ex.length) ex.forEach(x => out.push(...renderBlock(x.lines))); else out.push(pNormal('इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।'));
  out.push(h3('तुलनात्मक तालिका / चार्ट'));
  const tb = byKind(9);
  if (tb.length) tb.forEach(x => out.push(...renderBlock(x.lines))); else out.push(pNormal('इस अनुच्छेद हेतु तालिका आवश्यक नहीं।'));
  const ac = byKind(9.5);
  if (ac.length) { out.push(h3('साधु-जीवन में उतारने की विधि — चिन्तन, अभ्यास एवं चर्चा')); ac.forEach(x => out.push(...renderBlock(x.lines))); }
  out.push(h3('सन्दर्भ एवं पाद-टिप्पणी'));
  const rf = byKind(10);
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

const RUNNING_HEAD = META.running_title || META.title;  // चलता शीर्षक: ग्रन्थ-नाम (बाएँ) + वर्तमान खण्ड (दाएँ)
const runHeader = new Header({ children: [new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: 9906 }],
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'D0D0D0', space: 2 } },
  children: [
    new TextRun({ text: RUNNING_HEAD, size: 18, color: 'A6A6A6', font: FONT }),
    new TextRun({ text: '	', size: 18, font: FONT }),
    new SimpleField('STYLEREF "Heading 1"', ''),
  ] })] });

const doc = new Document({
  creator: META.creator || 'JinAagam',
  title: META.title,
  features: { updateFields: true },
  styles: {
    // The heading styles go in `default`, NOT in `paragraphStyles`. Declaring them as paragraphStyles
    // with the ids Heading1-3 does not REPLACE the library's own built-in definitions — it appends,
    // leaving three styleIds defined twice in styles.xml. That is invalid OOXML, and what Word does
    // with a style it has two conflicting definitions of is undefined. `default` overrides instead,
    // and the emitted style element is otherwise identical, outlineLvl included.
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
  console.log('written:', OUT_FILE, '| bytes:', buf.length, '| §:', parts.size, '| § without addenda:', missing.length ? missing.join(',') : 'none');
  if (dropped.length) console.log('dropped working-note sub-sections (not book content):\n  ' + dropped.join('\n  '));
});
