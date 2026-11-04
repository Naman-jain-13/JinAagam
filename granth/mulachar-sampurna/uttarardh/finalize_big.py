#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Finalise a book too large for Word to paginate in one piece: chunked PDF export + a real TOC.

    python finalize_big.py vyakhya/Book_Vyakhya.docx            # full run
    python finalize_big.py vyakhya/Book_Vyakhya.docx --plan      # show the chunking, touch nothing
    python finalize_big.py vyakhya/Book_Vyakhya.docx --resume    # keep chunk PDFs already exported

**Why this exists.** finalize_word.ps1 asks Word to open the whole book, update the TOC field and
repaginate. Word needs roughly 10 MB of memory per page of these books — measured, on halves of
परमात्मप्रकाश: 975 pages at 9.4 GB peak, 946 pages at 7.8 GB. A ~1,900-page book therefore wants
~18 GB. This machine has 15.4 GB of RAM and a 22 GB commit limit, so Word exhausts memory about
two-thirds of the way through pagination and dies — every time, after about five and a half minutes,
with `0x800706BE` (the RPC call fails because the process is gone) and an Office failfast in
mso20win32client.dll in the event log. It is not a corrupt file and not a bad element: both halves of
the book open perfectly on their own, and no structural variant (no TOC, no tables, deduplicated
styles, freshly built, un-postprocessed) survives whole.

**The way around it.** Never hand Word more than it can hold.

  1. The book's body is cut at खण्ड/§ boundaries into chunks of a few thousand paragraphs.
  2. Each chunk becomes a standalone .docx — same styles, same section properties, its page numbering
     started at the right offset via `w:pgNumType w:start` — and Word exports that alone.
  3. Word is asked for heading bookmarks in each chunk's PDF. Those bookmarks ARE the page numbers:
     adding the chunk's offset to a bookmark's page gives the heading's page in the finished book. So
     the table of contents is computed from what Word actually laid out, without Word ever paginating
     the book whole.
  4. The front matter plus a generated TOC (real paragraphs in the TOC1/TOC2 styles, not a field) is
     exported the same way, and everything is merged with PyMuPDF.

The merged PDF gets a full bookmark tree built from the same data, and the TOC lines are given link
annotations, so it navigates like the single-pass output did.

**The circularity, and how it is settled.** The body's page offsets depend on how many pages the front
matter and TOC occupy, and the TOC's page numbers depend on the body's offsets. The front is therefore
exported first with the real entry titles and placeholder numbers — the entry count, and so the page
count, does not depend on the digits — then the body, then the front again with real numbers. If that
second front export changes the page count, the body is re-exported against the corrected offset. It
converges in one round in practice, and the loop is capped.

Everything written goes under <book>_chunks/ and nothing touches the .docx being read.
"""
import io, os, re, sys, json, shutil, zipfile, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_CHILDREN = 20            # lowered twice: a dense region crashed Word's PDF export at ~151-152
                              # children (अधिकार 8, citation-heavy 9-क bullets), then AGAIN at just
                              # 75-76 children in a different region (अधिकार 12, stacked गाथा-citation
                              # sub-blocks). Both confirmed by bisection — no single bad paragraph,
                              # just cumulative formatting/run-switching density, and the danger
                              # threshold varies by region so no universal constant is provably
                              # safe. 20 bounds the worst-case chunk (largest single § is 48
                              # children) at ~68 — below the lowest danger point found so far, with
                              # some margin. If a chunk still hangs, bisect it (see bisect_chunk.py
                              # in scratchpad) and lower this further.
MAX_ROUNDS = 3

args = [a for a in sys.argv[1:] if not a.startswith('--')]
PLAN = '--plan' in sys.argv
RESUME = '--resume' in sys.argv
if not args:
    sys.exit(__doc__)

DOCX = os.path.abspath(args[0])
STEM = os.path.splitext(DOCX)[0]
WORKDIR = STEM + '_chunks'
PDF_OUT = STEM + '.pdf'

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
TAG = re.compile(r'<(/?)([A-Za-z0-9]+:[A-Za-z0-9]+)((?:[^>"]|"[^"]*")*?)(/?)>')


# ----------------------------------------------------------------- reading the book

class Book(object):
    """The .docx, with its body split into top-level children, byte for byte.

    The children are sliced out of the raw markup rather than re-serialised through ElementTree.
    ElementTree drops namespace declarations it believes unused, which leaves the document element's
    `mc:Ignorable="w14 w15 …"` naming prefixes that are no longer declared; Word then refuses the file
    ("appears to be corrupted"). Three rounds of this diagnosis were wasted on variants Word would not
    open. Here every byte that survives into a chunk is a byte Word has already accepted.
    """

    def __init__(self, path):
        self.zip = zipfile.ZipFile(path)
        self.raw = self.zip.read('word/document.xml').decode('utf-8')
        open_tag = re.search(r'<w:body[^>]*>', self.raw)
        self.prefix = self.raw[:open_tag.end()]
        self.suffix = self.raw[self.raw.rindex('</w:body>'):]
        self.inner = self.raw[open_tag.end():self.raw.rindex('</w:body>')]
        self.kids = self._children()
        assert ''.join(m for _, m in self.kids) == self.inner, 'child scan is not byte-exact'
        self.sect = [m for t, m in self.kids if t == 'w:sectPr'][0]

    def _children(self):
        out, depth, start, top = [], 0, 0, None
        for m in TAG.finditer(self.inner):
            closing, tag, selfclose = m.group(1), m.group(2), m.group(4)
            if selfclose:
                if depth == 0:
                    out.append((tag, self.inner[m.start():m.end()]))
                continue
            if not closing:
                if depth == 0:
                    start, top = m.start(), tag
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    out.append((top, self.inner[start:m.end()]))
        return out

    def document_xml(self, markup, page_start):
        """A whole document.xml out of the given child markup, numbered from page_start."""
        # The builder already emits an empty <w:pgNumType/>, so restarting the numbering is one
        # attribute. Nothing else in the section properties changes: same page size, margins and footer.
        sect = self.sect.replace('<w:pgNumType/>', '<w:pgNumType w:start="%d"/>' % page_start)
        assert 'w:start' in sect, 'no pgNumType to set in sectPr'
        return (self.prefix + markup + sect + self.suffix).encode('utf-8')

    def write(self, out, markup, page_start, banner=None):
        # banner: a खण्ड chunk that does not itself open with a Heading 1 would make the running header's
        # STYLEREF find nothing and print "Error! No text of specified style in document." on every page.
        # For such a chunk the field is replaced, in the same faint style, by the banner text that is in
        # force there (the nearest Heading 1 before it).
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as o:
            for n in self.zip.namelist():
                if n == 'word/document.xml':
                    o.writestr(n, self.document_xml(markup, page_start))
                elif banner is not None and re.fullmatch(r'word/header\d*\.xml', n):
                    hx = self.zip.read(n).decode('utf-8')
                    b = re.search(r'<w:r>(<w:rPr>(?:(?!</w:rPr>).)*</w:rPr>)<w:fldChar w:fldCharType="begin"/></w:r>', hx, re.S)
                    e = re.search(r'<w:fldChar w:fldCharType="end"/></w:r>', hx)
                    if b and e:
                        run = '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (b.group(1), esc(banner))
                        hx = hx[:b.start()] + run + hx[e.end():]
                    o.writestr(n, hx.encode('utf-8'))
                else:
                    o.writestr(n, self.zip.read(n))


def style_of(markup):
    m = re.search(r'<w:pStyle w:val="([^"]+)"', markup)
    return m.group(1) if m else ''


def text_of(markup):
    t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', markup))
    t = (t.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
          .replace('&apos;', "'").replace('&quot;', '"'))
    return re.sub(r'\s+', ' ', t).strip()


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


# ----------------------------------------------------------------- the generated TOC

FONT = 'Nirmala UI'
TAB_POS = 9850        # text width is 11908 - 1000 - 1000 twips; leave a little room for the number

# A दोहा heading carries its visible "अधिकार 1, दोहा 47" text plus a hidden (w:vanish) run holding
# TOC_MARKER + the descriptive sentence that titleOf() in build_docx.js strips out of the body heading
# (the reader found that sentence a distraction sitting right above the दोहा itself, but wanted it back
# in the index). text_of() below reads every <w:t> regardless of run formatting, so the hidden run's
# text arrives here concatenated onto the visible text, split apart again by TOC_MARKER.
TOC_MARKER = '␟'
NUM_TAB = 750          # right-aligned column: bare दोहा number ("47", "19-21", "111*2" — no "अधिकार N,")
TOPIC_TAB = 950        # left-aligned: the descriptive sentence starts here


def toc_paragraph(level, title, page):
    """One TOC line: title, dot leader, page number — in the TOC1/TOC2 styles the builder defines.

    A दोहा entry (level 2, title carrying TOC_MARKER) instead gets three columns — number, topic,
    page — so the reference itself ("अधिकार 1,") need not be repeated on every line; the अधिकार/
    प्रकरण banner immediately above already gives that context.
    """
    style = 'TOC1' if level == 1 else 'TOC2'
    rpr = ('<w:rPr><w:rFonts w:ascii="%s" w:cs="%s" w:eastAsia="%s" w:hAnsi="%s"/></w:rPr>'
           % (FONT, FONT, FONT, FONT))
    # a युग्म (paired-दोहा) reference like "166–167" (en dash, U+2013 — NOT the plain hyphen of
    # "19-21", which is fine) breaks Word's layout in this 3-column form: the topic and dot-leader
    # runs vanish from the render and the page number is orphaned alone on the next line with no
    # leader dots, so nothing can link to it. Swapping the dash for a hyphen did not fix it either —
    # the cause is some Word layout quirk specific to that character in this tab position, not
    # something this script can predict further, so these rare entries (2 of 520) fall back to the
    # plain single-run TOC line instead of chasing it. The visible in-body heading is unaffected.
    if level == 2 and TOC_MARKER in title and '–' not in title.split(TOC_MARKER, 1)[0]:
        ref, topic = title.split(TOC_MARKER, 1)
        m = re.search(r'(?:दोहा|गाथा|§|कारिका)\s+([^\s,]+)\s*$', ref)
        num = m.group(1) if m else ref
        tabs = ('<w:tabs>'
                '<w:tab w:val="right" w:pos="%d"/>'
                '<w:tab w:val="left" w:pos="%d"/>'
                '<w:tab w:val="right" w:leader="dot" w:pos="%d"/>'
                '</w:tabs>') % (NUM_TAB, TOPIC_TAB, TAB_POS)
        return (
            '<w:p><w:pPr><w:pStyle w:val="%s"/>%s</w:pPr>'
            '<w:r>%s<w:tab/><w:t xml:space="preserve">%s</w:t></w:r>'
            '<w:r>%s<w:tab/><w:t xml:space="preserve">%s</w:t></w:r>'
            '<w:r>%s<w:tab/><w:t>%s</w:t></w:r></w:p>'
            % (style, tabs, rpr, esc(num), rpr, esc(topic), rpr, page)
        )
    # fallback (level 1, or a level-2 title with no TOC_MARKER, or the en-dash edge case above):
    # plain single-run line. A level-2 title still carrying TOC_MARKER here (the en-dash case) must
    # have its hidden topic text dropped — only the visible "अधिकार N, दोहा M" reference is shown.
    plain = title.split(TOC_MARKER, 1)[0] if TOC_MARKER in title else title
    return (
        '<w:p><w:pPr><w:pStyle w:val="%s"/>'
        '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs>'
        '</w:pPr>'
        '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
        '<w:r>%s<w:tab/><w:t>%s</w:t></w:r></w:p>'
        % (style, TAB_POS, rpr, esc(plain), rpr, page)
    )


# ----------------------------------------------------------------- Word, one chunk at a time

def export(docx, pdf):
    # LimitSec lowered from the 1200s default: with MAX_CHILDREN this small, a healthy chunk
    # exports in 5-15s, so a hang is detected (and the retry loop can recover) far sooner.
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                        '-File', os.path.join(HERE, 'export_chunk.ps1'),
                        '-Docx', docx, '-Pdf', pdf, '-LimitSec', '150'],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    line = r.stdout.decode('utf-8', 'replace').strip()
    print('   ' + line.replace('\n', '\n   '))
    if r.returncode != 0 or not os.path.exists(pdf):
        raise SystemExit('export failed: %s' % docx)
    return pdf


HEADING_LEVEL = {'Heading1': 1, 'Heading2': 2, 'Heading3': 3}


def pdf_info(pdf, doc_headings=None):
    """(page count, [(level, title, page-within-this-pdf)]) for a chunk's headings.

    The page numbers come from the PDF's heading bookmarks, but the LEVELS do not. Word renumbers
    outline levels per document: a chunk that happens to begin at a § makes that § level 1 and its ten
    part-headings level 2, so taking the PDF's levels put 1,890 entries in a table of contents that
    should have 521 — every part-heading of every §, and the TOC grew from 17 pages to 47.

    So the level comes from the document's own pStyle and is paired with the bookmark by position.
    That pairing is exact — in all seven chunks the heading count and the bookmark count agree to the
    one — and the assertion below refuses to guess if a future book ever breaks it.
    """
    import fitz
    d = fitz.open(pdf)
    marks = d.get_toc()
    n = d.page_count
    d.close()
    if doc_headings is None:
        return n, [(lvl, title, pg) for lvl, title, pg in marks]
    if len(doc_headings) != len(marks):
        raise SystemExit('%s: %d headings in the document but %d bookmarks in the PDF — cannot pair '
                         'them, so the TOC levels would be guesses'
                         % (os.path.basename(pdf), len(doc_headings), len(marks)))
    return n, [(lvl, title, pg) for (lvl, title), (_, _, pg) in zip(doc_headings, marks)]


def without_leading_blanks(children):
    """Drop empty paragraphs from the front of a chunk.

    In the single-document layout an empty paragraph carrying a page break separated the TOC field
    from भूमिका. Once the contents becomes its own document that break has nothing in front of it, and
    it printed a blank page 19 — the only blank page in the book. A chunk already starts on a fresh
    page, so a leading break is always redundant.
    """
    i = 0
    while i < len(children):
        tag, markup = children[i]
        if tag != 'w:p' or re.search(r'<w:t[^>]*>[^<]', markup):
            break
        i += 1
    return children[i:]


def headings_in(children):
    """(level, text) for every heading paragraph, in reading order."""
    return [(HEADING_LEVEL[style_of(m)], text_of(m))
            for t, m in children if t == 'w:p' and style_of(m) in HEADING_LEVEL]


LEADER = re.compile(r'\d+$')
_meta = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), '..', 'meta.json')
BOOK_TITLES = ({json.load(io.open(_meta, encoding='utf-8')).get(k, '') for k in ('title', 'running_title')}
               if os.path.exists(_meta) else set())


def link_toc(out, p0, entries):
    """Make the generated TOC lines clickable, as the Word field's \\h switch did.

    Entries are matched to rendered lines **structurally and positionally**, never by text.

    Not by text because PDF text extraction of Devanagari returns glyphs in visual order: the TOC page
    that reads मुद्रित इन्द्रियसुख comes back as मुहित इन्तन्द्रयसुख. Matching on that found nothing at
    all — 0 of 520 — and an earlier attempt at searching for an entry's title instead put 10,431 links
    on an 1,890-entry contents, most pointing at the wrong § (titles repeat; every § has a '1. मूल पाठ').

    Structurally: each entry ends with the line carrying its dot leader and page number, so the line to
    link is the one ending in digits that is not itself a bare page-number footer. On this book that
    detector finds exactly as many lines as there are entries, and the assertion below refuses to link
    anything if a future book disagrees — a contents whose links point at the wrong § is worse than one
    with no links, and both wrong-link bugs above were silent.
    """
    import fitz
    leaders = []
    for pno in range(p0):
        lines = []
        for block in out[pno].get_text('dict')['blocks']:
            for line in block.get('lines', []):
                txt = ''.join(s['text'] for s in line['spans']).strip()
                # a book title such as "… अधिकार 1–7" also ends in a digit; it is not a contents line
                if txt and not txt.isdigit() and LEADER.search(txt) and txt not in BOOK_TITLES:
                    lines.append((fitz.Rect(line['bbox']), txt))
        lines.sort(key=lambda L: (round(L[0].y0, 1), L[0].x0))
        leaders.extend((pno, rect, txt) for rect, txt in lines)

    if len(leaders) != len(entries):
        print('   NOT linking the TOC: found %d leader lines for %d entries, so the mapping would be '
              'a guess (bookmarks still navigate the whole book)' % (len(leaders), len(entries)))
        if os.environ.get('TOC_DEBUG'):
            i = j = 0
            while i < len(leaders) and j < len(entries):
                lp = LEADER.search(leaders[i][2]).group()
                ep = entries[j][2]
                if lp == ep:
                    i += 1; j += 1
                else:
                    print('   DEBUG divergence at leader#%d text=%r (pg %s) vs entry#%d %r (expected pg %s)'
                          % (i, leaders[i][2][-40:], lp, j, entries[j][1][:60], ep))
                    break
            print('   DEBUG tail: %d leaders left, %d entries left' % (len(leaders) - i, len(entries) - j))
            for k in range(max(0, j - 2), min(len(entries), j + 6)):
                print('      entry#%d: %r -> pg %s' % (k, entries[k][1][:70], entries[k][2]))
        return 0
    for (pno, rect, _), (_, _, pg) in zip(leaders, entries):
        out[pno].insert_link({'kind': fitz.LINK_GOTO, 'from': rect, 'page': int(pg) - 1})
    return len(leaders)


# ----------------------------------------------------------------- plan the chunks

book = Book(DOCX)
kids = book.kids

# The front block is everything up to the TOC field: the title page and the विषय-सूची heading. The
# field itself is dropped — a field cannot know page numbers that Word never computed, so the TOC is
# generated as text instead.
sdt_at = [i for i, (t, _) in enumerate(kids) if t == 'w:sdt']
if len(sdt_at) != 1:
    raise SystemExit('expected exactly one TOC field, found %d' % len(sdt_at))
SDT = sdt_at[0]
front_kids = [m for t, m in kids[:SDT]]
body_kids = [(t, m) for t, m in kids[SDT + 1:] if t != 'w:sectPr']

# Cut only where a reader would cut: at a खण्ड (Heading1) or a § (Heading2). A chunk that began
# mid-section would still export, but its first page would open on a continuation paragraph.
breaks = [i for i, (t, m) in enumerate(body_kids) if t == 'w:p' and style_of(m) in ('Heading1', 'Heading2')]
if not breaks or breaks[0] != 0:
    breaks = [0] + breaks

chunks, start = [], 0
def _is_h1(i):
    return i < len(body_kids) and style_of(body_kids[i][1]) == 'Heading1'


for b in breaks[1:] + [len(body_kids)]:
    # also cut at every Heading 1, so a chunk never holds a खण्ड banner except as its first element:
    # then every page of a chunk shows one and the same banner in the running header.
    if b - start >= MAX_CHILDREN or (_is_h1(b) and b > start):
        chunks.append((start, b))
        start = b
if start < len(body_kids):
    chunks.append((start, len(body_kids)))

print('%s' % os.path.basename(DOCX))
print('body children : %d  (front %d, body %d)' % (len(kids), len(front_kids), len(body_kids)))
print('chunks        : %d' % len(chunks))
for i, (a, b) in enumerate(chunks, 1):
    head = next((text_of(m) for t, m in body_kids[a:b] if style_of(m) in ('Heading1', 'Heading2')), '')
    print('  %2d  children %6d-%-6d (%5d)  %s' % (i, a, b, b - a, head[:54]))

if PLAN:
    sys.exit(0)

if not RESUME and os.path.isdir(WORKDIR):
    shutil.rmtree(WORKDIR)
if not os.path.isdir(WORKDIR):
    os.makedirs(WORKDIR)


def chunk_path(i, ext):
    return os.path.join(WORKDIR, '%02d.%s' % (i, ext))


# All headings, in reading order, for the placeholder TOC. Level 3 and below are not listed: the
# original field said \o "1-2", and the § part-headings would swamp the list.
def front_markup(entries):
    toc = ''.join(toc_paragraph(lvl, title, page) for lvl, title, page in entries)
    return ''.join(front_kids) + toc


placeholder = [(1 if style_of(m) == 'Heading1' else 2, text_of(m), '0')
               for t, m in body_kids if t == 'w:p' and style_of(m) in ('Heading1', 'Heading2')]
print('TOC entries   : %d' % len(placeholder))

p0, entries, chunk_pdfs, round_no = None, placeholder, [], 0
while round_no < MAX_ROUNDS:
    round_no += 1
    print('\nround %d' % round_no)

    # front matter + TOC, always page 1. --resume exists to skip re-exporting the expensive body
    # chunks (minutes each); this one is ~10s and its content (the TOC's real page numbers) changes
    # every round by design, so it is always re-exported, resume or not.
    fdocx, fpdf = chunk_path(0, 'docx'), chunk_path(0, 'pdf')
    book.write(fdocx, front_markup(entries), 1)
    export(fdocx, fpdf)
    new_p0, _ = pdf_info(fpdf)          # only the page count matters here; the TOC lists the body
    print('   front matter + TOC: %d pages' % new_p0)

    if p0 is not None and new_p0 == p0:
        break                      # offsets already used for the body are still right: done
    p0 = new_p0

    # body chunks, each numbered from where the previous one ended
    offset, chunk_pdfs, found = p0, [], []
    for i, (a, b) in enumerate(chunks, 1):
        dx, pf = chunk_path(i, 'docx'), chunk_path(i, 'pdf')
        kids_here = without_leading_blanks(body_kids[a:b])
        first_is_h1 = bool(kids_here) and style_of(kids_here[0][1]) == 'Heading1'
        banner = None
        if not first_is_h1:
            banner = next((text_of(m) for t, m in reversed(body_kids[:a]) if t == 'w:p' and style_of(m) == 'Heading1'), '')
        book.write(dx, ''.join(m for _, m in kids_here), offset + 1, banner)
        if not (RESUME and os.path.exists(pf)):
            export(dx, pf)
        n, toc = pdf_info(pf, headings_in(kids_here))
        print('   chunk %2d: %4d pages, pages %d-%d, %d bookmarks' % (i, n, offset + 1, offset + n, len(toc)))
        for lvl, title, pg in toc:
            found.append((lvl, title, pg + offset))
        chunk_pdfs.append(pf)
        offset += n

    entries = [(lvl, title, str(pg)) for lvl, title, pg in found if lvl <= 2]
    print('   headings located: %d (levels 1-2: %d)' % (len(found), len(entries)))
    all_headings = found

if round_no >= MAX_ROUNDS and p0 != new_p0:
    raise SystemExit('front matter page count will not settle; stopping rather than shipping a wrong TOC')

# ----------------------------------------------------------------- merge
import fitz

out = fitz.open()
for p in [chunk_path(0, 'pdf')] + chunk_pdfs:
    out.insert_pdf(fitz.open(p))
print('\nmerged: %d pages' % out.page_count)

# One bookmark tree for the whole book, from the same data the TOC was built from. insert_pdf does
# not carry outlines across, so without this the merged PDF would have no navigation at all.
# Levels must not jump (1 -> 3 is rejected), so each level is clamped to one more than the previous.
# A दोहा heading's title still carries TOC_MARKER + topic at this point (same raw text_of() output
# toc_paragraph split on) — the PDF outline panel is a single-line label, not a table, so join the two
# with a dash rather than showing the marker character raw.
tree, prev = [], 0
for lvl, title, pg in all_headings:
    lvl = min(lvl, prev + 1)
    title = title.replace(TOC_MARKER, ' — ')
    tree.append([lvl, title, pg])
    prev = lvl
out.set_toc(tree)

linked = link_toc(out, p0, entries)
print('TOC links inserted: %d of %d entries' % (linked, len(entries)))

out.save(PDF_OUT, garbage=3, deflate=True)
out.close()
print('pdf: %s (%.1f MB)' % (PDF_OUT, os.path.getsize(PDF_OUT) / 1048576.0))
print('front matter + TOC: pages 1-%d | body: pages %d-%d' % (p0, p0 + 1, offset))
