// Generic batch-markdown -> docx builder for Laghu Sarvagya Siddhi vyakhya project.
// Reads all parts/batch*.md files (sorted), converts a constrained markdown subset
// into a Word doc matching the Pramana Pariksha style (Heading2 = §section, Heading3 = subsection,
// bullet lists, simple tables, blockquote notes), and writes the final docx.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, convertInchesToTwip
} = require('docx');

const FONT = 'Nirmala UI';
const BODY_SIZE = 26;   // 13pt
const PARTS_DIR = path.join(__dirname, 'parts');
const OUT_FILE = path.join(__dirname, 'vyakhya', 'Bruhat_Sarvagya_Siddhi_Vyakhya.docx');

function parseInline(line) {
  // returns array of {text, bold}
  const runs = [];
  let rest = line;
  const re = /\*\*(.+?)\*\*/g;
  let lastIndex = 0, m;
  while ((m = re.exec(line)) !== null) {
    if (m.index > lastIndex) runs.push({ text: line.slice(lastIndex, m.index), bold: false });
    runs.push({ text: m[1], bold: true });
    lastIndex = re.lastIndex;
  }
  if (lastIndex < line.length) runs.push({ text: line.slice(lastIndex), bold: false });
  if (runs.length === 0) runs.push({ text: line, bold: false });
  return runs;
}

function textRuns(line, extra) {
  return parseInline(line).map(r => new TextRun(Object.assign({
    text: r.text, bold: r.bold, size: BODY_SIZE, font: FONT
  }, extra || {})));
}

function paraNormal(line) {
  return new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 160, line: 340 },
    children: textRuns(line)
  });
}

function paraBullet(line) {
  return new Paragraph({
    bullet: { level: 0 },
    spacing: { after: 120, line: 340 },
    children: textRuns(line)
  });
}

function paraQuote(line) {
  return new Paragraph({
    indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 12, color: '1F4E79', space: 8 } },
    shading: { type: ShadingType.CLEAR, fill: 'EDF2F7' },
    spacing: { after: 160, before: 120, line: 340 },
    children: textRuns(line, { italics: true })
  });
}

function paraMool(line) {
  // Sanskrit root-text paragraph: slightly larger, bold-ish tone via color
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 100, line: 360 },
    children: textRuns(line, { color: '7A1F1F' })
  });
}

function buildTable(rows) {
  const colCount = rows[0].length;
  const colWidth = Math.floor(9000 / colCount);
  const trs = rows.map((cells, ri) => new TableRow({
    children: cells.map(c => new TableCell({
      width: { size: colWidth, type: WidthType.DXA },
      shading: ri === 0 ? { type: ShadingType.CLEAR, fill: 'DCE6F1' } : undefined,
      children: [ new Paragraph({
        spacing: { after: 40 },
        children: [ new TextRun({ text: c, bold: ri === 0, size: BODY_SIZE - 2, font: FONT }) ]
      }) ]
    }))
  }));
  return new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: rows[0].map(() => colWidth),
    rows: trs
  });
}

function parseMarkdown(md) {
  const lines = md.split('\n');
  const children = [];
  let i = 0;
  let inMoolBlock = false;
  let tableBuffer = null;

  function flushTable() {
    if (tableBuffer && tableBuffer.length) {
      children.push(buildTable(tableBuffer));
      children.push(new Paragraph({ text: '', spacing: { after: 120 } }));
    }
    tableBuffer = null;
  }

  while (i < lines.length) {
    let raw = lines[i];
    const line = raw.replace(/\r$/, '');
    const trimmed = line.trim();

    if (trimmed === '') { flushTable(); i++; continue; }

    if (trimmed === '---') {
      flushTable();
      children.push(new Paragraph({
        spacing: { before: 200, after: 200 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'AAAAAA', space: 6 } },
        children: [ new TextRun({ text: '', size: 4 }) ]
      }));
      i++; continue;
    }

    if (trimmed.startsWith('§')) {
      flushTable();
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { before: 300, after: 160 },
        children: [ new TextRun({ text: trimmed, bold: true, size: 32, font: FONT, color: '1F4E79' }) ]
      }));
      i++; continue;
    }

    if (trimmed.startsWith('## ')) {
      flushTable();
      const label = trimmed.slice(3).trim();
      children.push(new Paragraph({
        heading: HeadingLevel.HEADING_3,
        spacing: { before: 200, after: 100 },
        children: [ new TextRun({ text: label, bold: true, size: 28, font: FONT, color: '833C0B' }) ]
      }));
      inMoolBlock = label.includes('मूल संस्कृत पाठ');
      i++; continue;
    }

    if (trimmed.startsWith('|')) {
      const cells = trimmed.split('|').map(c => c.trim()).filter((c, idx, arr) => !(idx === 0 && c === '') && !(idx === arr.length - 1 && c === ''));
      if (/^:?-+:?$/.test(cells.join(''))) { i++; continue; } // separator row
      if (!tableBuffer) tableBuffer = [];
      tableBuffer.push(cells);
      i++; continue;
    } else {
      flushTable();
    }

    if (trimmed.startsWith('> ')) {
      children.push(paraQuote(trimmed.slice(2)));
      i++; continue;
    }

    if (trimmed.startsWith('- ')) {
      children.push(paraBullet(trimmed.slice(2)));
      i++; continue;
    }

    // plain paragraph
    if (inMoolBlock) children.push(paraMool(trimmed));
    else children.push(paraNormal(trimmed));
    i++;
  }
  flushTable();
  return children;
}

// ---- assemble ----
const files = fs.readdirSync(PARTS_DIR).filter(f => f.endsWith('.md')).sort();
if (files.length === 0) { console.error('No batch files found in parts/'); process.exit(1); }

const titleChildren = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 80 },
    children: [ new TextRun({ text: 'श्रीमदाचार्य-अनन्तकीर्ति-विरचिता', bold: true, size: 30, font: FONT }) ]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 300 },
    children: [ new TextRun({ text: 'बृहत्-सर्वज्ञ-सिद्धिः', bold: true, size: 44, font: FONT, color: '1F4E79' }) ]
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 160, line: 340 },
    children: [ new TextRun({
      text: 'अनुच्छेदशः मूल संस्कृत पाठ, हिन्दी अनुवाद, जैनागम-सम्मत विस्तृत व्याख्या, सरल उदाहरण एवं तुलनात्मक तालिका सहित। आधार: 75-पृष्ठीय स्कैन (मुद्रित पृष्ठ १३०–२०४ अनुमानित) — Laghu Sarvagya Siddhi के ठीक बाद, उसी संग्रह-ग्रन्थ में। यह कार्य बैचों में प्रगतिशील है; प्रगति-विवरण के लिए granth/bruhat-sarvagya-siddhi/progress.md देखें।',
      size: BODY_SIZE, font: FONT, italics: true
    }) ]
  }),
  new Paragraph({
    spacing: { before: 100, after: 300 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: '1F4E79', space: 8 } },
    children: [ new TextRun({ text: '', size: 4 }) ]
  })
];

let bodyChildren = [];
for (const f of files) {
  const md = fs.readFileSync(path.join(PARTS_DIR, f), 'utf-8');
  bodyChildren = bodyChildren.concat(parseMarkdown(md));
}

const doc = new Document({
  sections: [{
    properties: {
      page: {
        size: { width: convertInchesToTwip(8.27), height: convertInchesToTwip(11.69) },
        margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 }
      }
    },
    children: titleChildren.concat(bodyChildren)
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT_FILE, buf);
  console.log('written:', OUT_FILE, 'bytes:', buf.length, 'batches:', files.length);
});
