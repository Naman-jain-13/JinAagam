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
MAX_CHILDREN = 4200          # ~300 pages a chunk: well inside memory, measured peak ~3 GB
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

    def write(self, out, markup, page_start):
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as o:
            for n in self.zip.namelist():
                if n == 'word/document.xml':
                    o.writestr(n, self.document_xml(markup, page_start))
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


def toc_paragraph(level, title, page):
    """One TOC line: title, dot leader, page number — in the TOC1/TOC2 styles the builder defines."""
    style = 'TOC1' if level == 1 else 'TOC2'
    rpr = ('<w:rPr><w:rFonts w:ascii="%s" w:cs="%s" w:eastAsia="%s" w:hAnsi="%s"/></w:rPr>'
           % (FONT, FONT, FONT, FONT))
    return (
        '<w:p><w:pPr><w:pStyle w:val="%s"/>'
        '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs>'
        '</w:pPr>'
        '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
        '<w:r>%s<w:tab/><w:t>%s</w:t></w:r></w:p>'
        % (style, TAB_POS, rpr, esc(title), rpr, page)
    )


# ----------------------------------------------------------------- Word, one chunk at a time

def export(docx, pdf):
    r = subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                        '-File', os.path.join(HERE, 'export_chunk.ps1'),
                        '-Docx', docx, '-Pdf', pdf],
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


def headings_in(children):
    """(level, text) for every heading paragraph, in reading order."""
    return [(HEADING_LEVEL[style_of(m)], text_of(m))
            for t, m in children if t == 'w:p' and style_of(m) in HEADING_LEVEL]


def link_toc(out, p0, entries):
    """Make the generated TOC lines clickable, as the Word field's \\h switch did.

    The entries are matched to the rendered lines IN READING ORDER, never by searching the page for an
    entry's text. Titles repeat — every § has a '1. मूल पाठ' — and a text search inserted 10,431 links
    on an 1,890-entry contents, most pointing at the wrong §. Sequential matching cannot do that: a
    line that does not match the next expected entry is skipped rather than linked.
    """
    import fitz
    idx = linked = 0
    for pno in range(p0):
        page = out[pno]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                if idx >= len(entries):
                    break
                txt = ''.join(s['text'] for s in line['spans'])
                _, title, pg = entries[idx]
                key = title[:12].strip()
                if key and key in txt:
                    page.insert_link({'kind': fitz.LINK_GOTO,
                                      'from': fitz.Rect(line['bbox']), 'page': int(pg) - 1})
                    idx += 1
                    linked += 1
    return linked


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
for b in breaks[1:] + [len(body_kids)]:
    if b - start >= MAX_CHILDREN:
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

    # front matter + TOC, always page 1
    fdocx, fpdf = chunk_path(0, 'docx'), chunk_path(0, 'pdf')
    book.write(fdocx, front_markup(entries), 1)
    if not (RESUME and os.path.exists(fpdf)):
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
        book.write(dx, ''.join(m for _, m in body_kids[a:b]), offset + 1)
        if not (RESUME and os.path.exists(pf)):
            export(dx, pf)
        n, toc = pdf_info(pf, headings_in(body_kids[a:b]))
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
tree, prev = [], 0
for lvl, title, pg in all_headings:
    lvl = min(lvl, prev + 1)
    tree.append([lvl, title, pg])
    prev = lvl
out.set_toc(tree)

linked = link_toc(out, p0, entries)
print('TOC links inserted: %d of %d entries' % (linked, len(entries)))

out.save(PDF_OUT, garbage=3, deflate=True)
out.close()
print('pdf: %s (%.1f MB)' % (PDF_OUT, os.path.getsize(PDF_OUT) / 1048576.0))
print('front matter + TOC: pages 1-%d | body: pages %d-%d' % (p0, p0 + 1, offset))
