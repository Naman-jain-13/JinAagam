"""Combine out/partNN.md into one .docx (headings, bullets, bold, pipe tables, code-block charts)."""
import glob, re, sys
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Cm

S = "C:/Users/naman/AppData/Local/Temp/claude/e--Projects-JinAagam/a79a24b2-a5b6-4255-b4f9-048c6811d25d/scratchpad/"
HERE = __import__("pathlib").Path(__file__).resolve().parent
OUT = sys.argv[1] if len(sys.argv) > 1 else str(HERE / "vyakhya" / "Abhishek_Path_Sangrah_Vyakhya.docx")
INPUT = sys.argv[2] if len(sys.argv) > 2 else str(HERE / "parts/batch*.md")
META = {
    "pre": "श्रीमदाचार्यविद्यानन्द-विरचिता",
    "title": "प्रमाण-परीक्षा",
    "subtitle": "सम्पूर्ण ग्रन्थ (§१ – §१८०): अनुच्छेदशः मूल संस्कृत पाठ, हिन्दी अनुवाद, जैनागम-सम्मत विस्तृत व्याख्या, सरल उदाहरण, तुलनात्मक तालिका/चार्ट एवं सन्दर्भ",
    "basis": "**आधार:** उपलब्ध 67-पृष्ठीय स्कैन (jainelibrary.org)। मूल पाठ स्कैन-छवियों को पढ़कर लिपिबद्ध किया गया है; जहाँ अक्षर अस्पष्ट थे वहाँ [अस्पष्ट] अंकित है। अध्ययन से पूर्व मूल पुस्तक से मिलान अवश्य करें।",
    "structure": "**प्रत्येक अनुच्छेद की संरचना:** १. मूल संस्कृत पाठ → २. हिन्दी अनुवाद → ३. जैनागम के अनुसार विस्तृत व्याख्या → ४. सरल उदाहरण → ५. तुलनात्मक तालिका / चार्ट → ६. सन्दर्भ एवं पाद-टिप्पणी",
}
if len(sys.argv) > 3:
    import json
    META.update(json.load(open(sys.argv[3], encoding="utf-8")))
FONT = "Nirmala UI"
MONO = "Nirmala UI"  # Devanagari in charts; Consolas lacks Devanagari glyphs


def set_font(run, name=FONT, size=None, bold=None, color=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)
    if size:
        run.font.size = Pt(size)
        szcs = OxmlElement("w:szCs")
        szcs.set(qn("w:val"), str(int(size * 2)))
        rpr.append(szcs)
    if bold is not None:
        run.bold = bold
        if bold:
            rpr.append(OxmlElement("w:bCs"))
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_inline(par, text, size=12, base_bold=False, color=None):
    for i, chunk in enumerate(re.split(r"\*\*", text)):
        if chunk:
            set_font(par.add_run(chunk), size=size, bold=base_bold or i % 2 == 1, color=color)


def shade(cell, hex_fill):
    tcpr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcpr.append(shd)


def add_table(doc, rows):
    rows = [r for r in rows if not re.fullmatch(r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?", r.strip())]
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    ncol = max(len(r) for r in cells)
    t = doc.add_table(rows=len(cells), cols=ncol)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, r in enumerate(cells):
        for j in range(ncol):
            cell = t.cell(i, j)
            p = cell.paragraphs[0]
            add_inline(p, r[j] if j < len(r) else "", size=10.5, base_bold=(i == 0))
            if i == 0:
                shade(cell, "F3E3C3")
    doc.add_paragraph()


def add_code(doc, lines):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    cell = t.cell(0, 0)
    shade(cell, "F5F5F0")
    p = cell.paragraphs[0]
    for k, ln in enumerate(lines):
        r = p.add_run(ln)
        set_font(r, name=MONO, size=10.5)
        if k < len(lines) - 1:
            r.add_break()
    doc.add_paragraph()


def add_footer(doc):
    """Centered page-number field in the footer, set once on the first section only.
    Later sections default to is_linked_to_previous=True and share this same footer
    part — touching sec.footer on each of them would append a second PAGE field into
    the SAME paragraph (producing "11", "22", "33" ...), so we deliberately do this
    only for doc.sections[0]."""
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run()
    set_font(r, size=10)
    for tag, attr, txt in (("w:fldChar", "begin", None), ("w:instrText", None, " PAGE "), ("w:fldChar", "separate", None), ("w:t", None, "1"), ("w:fldChar", "end", None)):
        el = OxmlElement(tag)
        if attr:
            el.set(qn("w:fldCharType"), attr)
        if txt:
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        r._r.append(el)


def add_page_border(section, color="8B4513", sz="18"):
    """Decorative single-rule border around the given section's pages (used for the cover section only)."""
    sectPr = section._sectPr
    pgBorders = OxmlElement("w:pgBorders")
    pgBorders.set(qn("w:offsetFrom"), "page")
    for side in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "24")
        el.set(qn("w:color"), color)
        pgBorders.append(el)
    sectPr.append(pgBorders)


def add_centered(doc, text, size, color=None, bold=False, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    add_inline(p, text, size=size, base_bold=bold, color=color)
    return p


def add_cover_page(doc, meta):
    """A dedicated, decorative cover page — separate from the title/publication page that follows."""
    add_page_border(doc.sections[0])
    for _ in range(5):
        doc.add_paragraph()
    add_centered(doc, "॥ णमो जिणाणं ॥", 15, color="8B4513", space_after=6)
    add_centered(doc, meta.get("cover_pre", meta["pre"]), 15, color="8B4513", space_after=18)
    add_centered(doc, meta.get("cover_title", meta["title"]), 40, color="7A2E00", bold=True, space_after=10)
    add_centered(doc, meta.get("cover_subtitle", ""), 16, color="8B4513", space_after=26)
    add_centered(doc, "❧ ❦ ❧", 16, color="D9C9A8", space_after=26)
    for line in meta.get("cover_lines", []):
        add_centered(doc, line, 12.5, space_after=6)
    for _ in range(6):
        doc.add_paragraph()
    add_centered(doc, "❧ ❦ ❧", 16, color="D9C9A8", space_after=10)
    if meta.get("cover_footer"):
        add_centered(doc, meta["cover_footer"], 11, color="8B4513")
    # Start a fresh section for everything after the cover, so the decorative
    # border above stays on the cover page only.
    new_sec = doc.add_section(WD_SECTION.NEW_PAGE)
    new_sec.left_margin = new_sec.right_margin = Cm(1.5)
    new_sec.top_margin = new_sec.bottom_margin = Cm(1.3)


def add_source_info_page(doc, meta):
    """'मूल स्रोत-ग्रन्थ का परिचय' — publication details of the original scanned book (verso-style page)."""
    if not meta.get("source_info"):
        return
    si = meta["source_info"]
    doc.add_heading("मूल स्रोत-ग्रन्थ का परिचय", level=1)
    add_centered(doc, si.get("mangal", ""), 13, color="7A2E00", space_after=10)
    add_centered(doc, si.get("title", ""), 20, bold=True, color="7A2E00", space_after=4)
    if si.get("granthamala"):
        add_centered(doc, si["granthamala"], 11.5, space_after=14)
    t = doc.add_table(rows=len(si.get("rows", [])), cols=2)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (label, value) in enumerate(si.get("rows", [])):
        c0, c1 = t.cell(i, 0), t.cell(i, 1)
        add_inline(c0.paragraphs[0], f"**{label}**", size=11)
        add_inline(c1.paragraphs[0], value, size=11)
        shade(c0, "F3E3C3")
    doc.add_paragraph()
    for note in si.get("notes", []):
        p = doc.add_paragraph(style="List Bullet")
        add_inline(p, note, size=10.5)
    doc.add_page_break()


def add_toc(doc):
    p = doc.add_paragraph()
    r = p.add_run()
    for tag, attr in (("w:fldChar", "begin"), ("w:instrText", None), ("w:fldChar", "separate")):
        el = OxmlElement(tag)
        if attr:
            el.set(qn("w:fldCharType"), attr)
        else:
            el.set(qn("xml:space"), "preserve")
            el.text = 'TOC \\o "1-2" \\h \\z \\u'
        r._r.append(el)
    t = OxmlElement("w:t")
    t.text = "(विषय-सूची देखने के लिए: यहाँ राइट-क्लिक करके 'Update Field' चुनें)"
    r._r.append(t)
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    r._r.append(end)


# सन्दर्भ एवं पाद-टिप्पणी का आकार — पाठक ने कहा: शीर्षक छोटा, और बुलेट अगली पंक्ति में
# जाने के बजाय उसी पंक्ति में दो स्पेस छोड़कर बहते रहें, ताकि जगह बचे।
REF_HEAD_PT = 8.5
REF_BODY_PT = 6.5


def is_ref_heading(text):
    return "सन्दर्भ" in text and "पाद-टिप्पणी" in text


def add_ref_notes(doc, entries):
    """सब टिप्पणियाँ एक ही अनुच्छेद में — '• पहली।  • दूसरी।  • तीसरी।'"""
    if not entries:
        return
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(4)
    pf.line_spacing = 1.0
    pf.left_indent = Cm(0.4)
    for k, e in enumerate(entries):
        if k:
            set_font(p.add_run("  "), size=REF_BODY_PT)   # दो पतले स्पेस
        set_font(p.add_run("• "), size=REF_BODY_PT, color="777777")
        add_inline(p, e, size=REF_BODY_PT)


# चलता-शीर्षक (running head): हर ग्रन्थ के पन्नों के ऊपर उसी ग्रन्थ का नाम,
# अति-लघु अक्षरों में, बाहरी किनारे पर। यह ऊपर के हाशिये के अन्दर बैठता है,
# इसलिए मुख्य पाठ के लिए एक भी पंक्ति की जगह नहीं लेता।
RUN_HEAD_PT = 6.5
RUN_HEAD_COLOR = "8A8A8A"


def short_title(h1):
    """'ग्रन्थ-५: जैनाभिषेकः (श्री गजांकुश कवि …)' -> 'ग्रन्थ-५: जैनाभिषेकः'"""
    s = re.sub(r"\*\*", "", h1)
    s = re.sub(r"\s*\(.*$", "", s).strip(" —-–:;,")
    return s if len(s) <= 62 else s[:60].rstrip() + "…"


def start_chapter_section(doc, title, first):
    """नया खण्ड आरम्भ कीजिए और उसके पन्नों पर ग्रन्थ-नाम लगाइए।
    फ़ुटर को छूना नहीं है — वह खण्ड 0 से जुड़ा रहता है, वरना PAGE फ़ील्ड दुगुनी हो जाती है।"""
    sec = doc.add_section(WD_SECTION.CONTINUOUS if first else WD_SECTION.NEW_PAGE)
    sec.left_margin = sec.right_margin = Cm(1.5)
    sec.top_margin = sec.bottom_margin = Cm(1.3)
    sec.header.is_linked_to_previous = False
    sec.header_distance = Cm(0.55)
    p = sec.header.paragraphs[0]
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    set_font(p.add_run(short_title(title)), size=RUN_HEAD_PT, color=RUN_HEAD_COLOR)
    return sec


def main():
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(1.5)
    sec.top_margin = sec.bottom_margin = Cm(1.3)
    for sname, size, color, space_before, space_after in (
        ("Heading 1", 18, "7A2E00", 6, 6),
        ("Heading 2", 15, "8B4513", 18, 6),
        ("Heading 3", 12.5, "1F4E79", 10, 4),
    ):
        st = doc.styles[sname]
        st.font.name = FONT
        st.font.size = Pt(size)
        st.font.color.rgb = RGBColor.from_string(color)
        st.paragraph_format.space_before = Pt(space_before)
        st.paragraph_format.space_after = Pt(space_after)
        # Keep a heading on the same page as the first line of what follows it,
        # so it never sits alone at the bottom of a page.
        st.paragraph_format.keep_with_next = True
        rpr = st.element.get_or_add_rPr()
        rf = rpr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            rpr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            rf.set(qn(a), FONT)
        # thin rule above each अनुच्छेद heading (Heading 2) to mark the gap without a page break
        if sname == "Heading 2":
            pbdr = OxmlElement("w:pBdr")
            top = OxmlElement("w:top")
            top.set(qn("w:val"), "single")
            top.set(qn("w:sz"), "6")
            top.set(qn("w:space"), "4")
            top.set(qn("w:color"), "D9C9A8")
            pbdr.append(top)
            st.element.get_or_add_pPr().append(pbdr)

    if META.get("cover_title") or META.get("cover_lines"):
        add_cover_page(doc, META)
    add_footer(doc)
    add_source_info_page(doc, META)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p, META["pre"], size=14, color="7A2E00")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p, META["title"], size=28, base_bold=True, color="7A2E00")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline(p, META["subtitle"], size=13)
    p = doc.add_paragraph()
    add_inline(p, META["basis"], size=11)
    p = doc.add_paragraph()
    add_inline(p, META["structure"], size=11)
    doc.add_heading("विषय-सूची", level=1)
    add_toc(doc)
    doc.add_page_break()

    files = sorted(glob.glob(INPUT))
    first_h2 = True
    after_h1 = False
    for f in files:
        lines = open(f, encoding="utf-8").read().splitlines()
        i = 0
        while i < len(lines):
            ln = lines[i]
            s = ln.strip()
            if s.startswith("```"):
                block = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("```"):
                    block.append(lines[i].rstrip())
                    i += 1
                add_code(doc, block)
            elif s.startswith("|"):
                rows = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append(lines[i])
                    i += 1
                add_table(doc, rows)
                continue
            elif s.startswith("### "):
                title = s[4:]
                if is_ref_heading(title):
                    h = doc.add_heading(level=3)
                    h.paragraph_format.space_before = Pt(4)
                    h.paragraph_format.space_after = Pt(0)
                    add_inline(h, title, size=REF_HEAD_PT, color="1F4E79")
                    i += 1
                    notes = []
                    while i < len(lines):
                        nxt = lines[i]
                        if re.match(r"^\s*[-*] ", nxt):
                            notes.append(re.sub(r"^\s*[-*] ", "", nxt).rstrip())
                            i += 1
                        elif not nxt.strip():
                            i += 1
                            if any(l.strip() and not re.match(r"^\s*[-*] ", l)
                                   for l in lines[i:i + 1]):
                                break
                        else:
                            break
                    add_ref_notes(doc, notes)
                    continue
                h = doc.add_heading(level=3)
                add_inline(h, title, size=12.5, color="1F4E79")
            elif s.startswith("## "):
                # अनुच्छेद-स्तरीय शीर्षक: कोई पृष्ठ-विभाजन नहीं, केवल दृश्य-अन्तराल (ऊपर पतली रेखा + स्पेसिंग)
                first_h2 = after_h1 = False
                h = doc.add_heading(level=2)
                add_inline(h, s[3:], size=15, color="8B4513")
            elif s.startswith("# "):
                # ग्रन्थ/अध्याय-स्तरीय शीर्षक: नया खण्ड — नया पृष्ठ + इस ग्रन्थ का चलता-शीर्षक
                start_chapter_section(doc, s[2:], first=first_h2)
                first_h2, after_h1 = False, True
                h = doc.add_heading(level=1)
                add_inline(h, s[2:], size=18, color="7A2E00")
            elif re.match(r"^\s*[-*] ", ln):
                indent = len(ln) - len(ln.lstrip())
                p = doc.add_paragraph(style="List Bullet 2" if indent >= 2 else "List Bullet")
                add_inline(p, re.sub(r"^\s*[-*] ", "", ln))
            elif re.match(r"^\s*\d+[.)] ", ln):
                p = doc.add_paragraph(style="List Number")
                add_inline(p, re.sub(r"^\s*\d+[.)] ", "", ln))
            elif s.startswith("> "):
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(1)
                add_inline(p, s[2:], color="444444")
            elif s == "---" or not s:
                pass
            else:
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(6)
                add_inline(p, s)
            i += 1
    doc.save(OUT)
    print("saved", OUT, "from", len(files), "parts")


main()
