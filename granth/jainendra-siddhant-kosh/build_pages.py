# -*- coding: utf-8 -*-
"""जैनेन्द्र सिद्धान्त कोश — पृष्ठशः पुनर्निर्माण।
bhag-K/pages/p0NNN.md  →  bhag-K/out/Kosh_K.html  →  (Chrome headless)  bhag-K/out/Jainendra_Siddhant_Kosh_K.pdf

PDF पृष्ठ N = मूल PDF पृष्ठ N। हर पृष्ठ का पाठ उसी पृष्ठ में समाता है (फ़ॉन्ट आवश्यकता अनुसार छोटा होता है),
@notes पाद-टिप्पणी बनते हैं (पाठ में उद्धृत अंश पर ऊपर-अंक), और लम्बी टिप्पणियाँ परिशिष्ट में (अन्तिम पृष्ठ के बाद)।
उपयोग:  python build_pages.py K [--from A --to B] [--no-pdf]
"""
import io, os, re, sys, glob, html, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
K = sys.argv[1]
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
A, B = int(arg('--from', 1)), int(arg('--to', 99999))
BH = os.path.join(HERE, 'bhag-%s' % K)
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
LONG_NOTE = 220          # notes longer than this go to the परिशिष्ट, with a pointer in the footnote

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\*\w])\*([^*\s][^*]*?)\*(?!\*)', r'<i>\1</i>', s)
    return s

def block(md):
    out, para, rows = [], [], []
    def flush():
        if para: out.append('<p>%s</p>' % inline(' '.join(para))); para.clear()
        if rows:
            body = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c.strip()) for c in r.strip().strip('|').split('|'))
                           for r in rows if not re.match(r'^\s*\|?\s*:?-{2,}', r))
            out.append('<table>%s</table>' % body); rows.clear()
    for l in md.split('\n'):
        if l.strip().startswith('|'):
            if para: flush()
            rows.append(l); continue
        if rows: flush()
        if not l.strip(): flush(); continue
        m = re.match(r'^#{1,4}\s+(.*)$', l)
        if m: flush(); out.append('<h3>%s</h3>' % inline(m.group(1))); continue
        para.append(l.strip())
    flush()
    return '\n'.join(out)

def parse(path):
    t = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
    d = {'head-left': '', 'head-right': '', 'foot': '', 'full-top': '', 'col1': '', 'col2': '', 'full-bottom': '', 'notes': []}
    cur, seen_cols = None, False
    buf = {}
    for l in t.split('\n'):
        m = re.match(r'^@(head-left|head-right|foot):\s*(.*)$', l)
        if m: d[m.group(1)] = m.group(2).strip(); continue
        m = re.match(r'^@(col1|col2|full|notes)\s*$', l.strip())
        if m:
            k = m.group(1)
            if k in ('col1', 'col2'): seen_cols = True
            if k == 'full': k = 'full-bottom' if seen_cols else 'full-top'
            cur = k; buf.setdefault(cur, []); continue
        if l.startswith('<!--'): continue
        if cur: buf[cur].append(l)
    for k, v in buf.items():
        if k == 'notes':
            d['notes'] = [x[2:].strip() for x in v if x.startswith('- ') and 'कोई नहीं' not in x]
        else:
            d[k] = '\n'.join(v).strip()
    return d

def page_v2(path, n):
    """v2 page file (surya_pages.py): ordered segments of @full / @col1+@col2, each line already-clean HTML"""
    t = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
    head = dict(re.findall(r'^@(head-left|head-center|head-right|foot|rotate):[ \t]*(.*)$', t, re.M))
    segs, cur, notes = [], None, []
    for l in t.split('\n'):
        s = l.strip()
        if s in ('@full', '@col1', '@col2', '@notes'):
            cur = s[1:]
            if cur == 'full': segs.append(['full', []])
            elif cur == 'col1': segs.append(['cols', [], []])
            continue
        if not s or s.startswith('@') or s.startswith('<!--'): continue
        if cur == 'notes':
            if s.startswith('- ') and 'कोई नहीं' not in s: notes.append(s[2:])
        elif cur == 'full': segs[-1][1].append(s)
        elif cur == 'col1': segs[-1][1].append(s)
        elif cur == 'col2': segs[-1][2].append(s)
    body = ''.join('<div class="full">%s</div>' % ''.join(sg[1]) if sg[0] == 'full' else
                   '<div class="cols"><div class="col">%s</div><div class="col">%s</div></div>' % (''.join(sg[1]), ''.join(sg[2]))
                   for sg in segs)
    if head.get('rotate'):   # printed sideways in the original: lay the content out landscape, turned the same way
        body = '<div class="rotbox">%s</div>' % body
    fns = []
    for i, note in enumerate(notes, 1):
        text = note
        if len(note) > LONG_NOTE:
            appendix.append((n, i, note)); text = note[:120].rstrip() + ' … (विस्तार परिशिष्ट में)'
        fns.append('<div class="fn"><sup>%d</sup> %s</div>' % (i, inline(text)))
    return ('<section class="page%s" data-n="%d"><div class="hd"><span>%s</span><span>%s</span><span>%s</span></div>'
            '<div class="body">%s</div><div class="fns">%s</div><div class="ft">%s</div></section>') % (
        ' rot' if head.get('rotate') else '', n, inline(head.get('head-left', '')), inline(head.get('head-center', '')), inline(head.get('head-right', '')),
        body, ''.join(fns), inline(head.get('foot', '')) or 'जैनेन्द्र सिद्धान्त कोश')

pages, appendix = [], []
files = sorted(glob.glob(os.path.join(BH, 'pages', 'p*.md')))
for f in files:
    n = int(re.search(r'p(\d+)\.md$', f).group(1))
    if not (A <= n <= B): continue
    if '\n@image' in '\n' + io.open(f, encoding='utf-8').read():
        # OCR could not read this page reliably (rotated table, figure…): carry the original page image
        img = os.path.join(BH, 'out', 'img', 'p%04d.png' % n)
        if not os.path.exists(img):
            import pymupdf
            os.makedirs(os.path.dirname(img), exist_ok=True)
            pymupdf.open(os.path.join(BH, 'mool', 'Jainendra_Siddhant_Kosh_%s.pdf' % K))[n - 1].get_pixmap(dpi=150).save(img)
        pages.append('<section class="page imgpage" data-n="%d"><img src="img/p%04d.png"></section>' % (n, n))
        continue
    if '\n@v2' in io.open(f, encoding='utf-8').read():
        pages.append(page_v2(f, n)); continue
    d = parse(f)
    regions ={k: block(d[k]) for k in ('full-top', 'col1', 'col2', 'full-bottom')}
    fns = []
    for i, note in enumerate(d['notes'], 1):
        q = re.match(r'^["“\']?(.+?)["”\']?\s+—', note)
        if q:   # put the mark after the quoted words where they first occur in the rendered text
            word = html.escape(q.group(1).strip().strip('`'), quote=False)
            for k in ('full-top', 'col1', 'col2', 'full-bottom'):
                if word and word in regions[k]:
                    regions[k] = regions[k].replace(word, word + '<sup class="fm">%d</sup>' % i, 1); break
        text = note
        if len(note) > LONG_NOTE:
            appendix.append((n, i, note)); text = note[:120].rstrip() + ' … (विस्तार परिशिष्ट में)'
        fns.append('<div class="fn"><sup>%d</sup> %s</div>' % (i, inline(text)))
    pages.append('''<section class="page" data-n="%d">
 <div class="hd"><span>%s</span><span>%s</span></div>
 <div class="body">
  <div class="full">%s</div>
  <div class="cols"><div class="col">%s</div><div class="col">%s</div></div>
  <div class="full">%s</div>
 </div>
 <div class="fns">%s</div>
 <div class="ft">%s</div>
</section>''' % (n, inline(d['head-left']), inline(d['head-right']), regions['full-top'], regions['col1'], regions['col2'],
                regions['full-bottom'], ''.join(fns), inline(d['foot'])))

if appendix:
    rows = ''.join('<p><b>मूल पृष्ठ %d, टिप्पणी %d —</b> %s</p>' % (n, i, inline(t)) for n, i, t in appendix)
    pages.append('<section class="page appx"><div class="hd"><span>परिशिष्ट</span><span>विस्तृत टिप्पणियाँ</span></div>'
                 '<div class="body"><h2>परिशिष्ट — विस्तृत टिप्पणियाँ</h2>%s</div><div class="fns"></div><div class="ft"></div></section>' % rows)

CSS = '''
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Nirmala UI", "Noto Sans Devanagari", sans-serif; color: #111; }
.page { width: 210mm; height: 297mm; padding: 11mm 12mm 9mm; display: flex; flex-direction: column;
        page-break-after: always; break-after: page; overflow: hidden; position: relative; }
.hd { display: flex; justify-content: space-between; font-size: 8pt; color: #777; border-bottom: 0.4pt solid #bbb;
      padding-bottom: 1.2mm; margin-bottom: 2mm; }
.body { flex: 1 1 auto; overflow: hidden; font-size: var(--fs, 9.5pt); line-height: 1.38; text-align: justify; }
.cols { display: flex; gap: 6mm; }
.col { flex: 1 1 0; min-width: 0; }
.col + .col { border-left: 0.3pt solid #ccc; padding-left: 6mm; }
p { margin: 0 0 0.35em; }
h3 { font-size: 1.12em; margin: 0.45em 0 0.25em; }
h2 { font-size: 13pt; margin: 0 0 4mm; }
table { border-collapse: collapse; width: 100%; margin: 0.3em 0; font-size: 0.92em; }
.squeeze table { table-layout: fixed; } .squeeze td, .squeeze th { overflow-wrap: anywhere; }
td, th { border: 0.4pt solid #999; padding: 0.15em 0.3em; vertical-align: top; }
th { font-weight: 600; background: #f3f3f3; }
.body img { max-width: 100%; display: block; margin: 0.3em auto; }
/* sideways page: a landscape box (body height × body width) turned 90° anticlockwise, as printed */
.rot .body { position: relative; } .rotbox { font-size: var(--fs, 9.5pt); }
.rot .rotbox { position: absolute; top: 0; left: 0; width: 265mm; height: 186mm; overflow: hidden;
               transform-origin: top left; transform: translateY(265mm) rotate(-90deg); }
sup.fm { font-size: 0.7em; color: #555; }
.fns { font-size: 7pt; line-height: 1.25; color: #333; border-top: 0.4pt solid #bbb; margin-top: 1.5mm; padding-top: 1mm; }
.fns:empty { display: none; }
.fn sup { font-size: 0.85em; }
.imgpage { padding: 0; } .imgpage img { width: 210mm; height: 297mm; object-fit: contain; }
.ft { font-size: 7.5pt; color: #888; text-align: center; margin-top: 1.5mm; }
'''
# shrink each page's text until nothing overflows its box (columns are measured separately)
JS = '''
document.querySelectorAll('.page').forEach(pg => {
  const body = pg.querySelector('.rotbox') || pg.querySelector('.body');
  if (!body) return;
  let fs = 9.5;
  const over = () => body.scrollHeight > body.clientHeight + 1 || body.scrollWidth > body.clientWidth + 1;
  body.style.setProperty('--fs', fs + 'pt');
  while (over() && fs > 5.2) { fs -= 0.15; body.style.setProperty('--fs', fs.toFixed(2) + 'pt'); }
  if (over()) { pg.classList.add('squeeze'); }   // still too wide at the smallest size: let table cells wrap
  pg.dataset.fs = fs.toFixed(2);
  if (over()) pg.dataset.overflow = '1';
});
document.title = 'fit-done';
'''
doc = '<!doctype html><html lang="hi"><head><meta charset="utf-8"><title>Kosh %s</title><style>%s</style></head><body>\n%s\n<script>%s</script></body></html>' % (
    K, CSS, '\n'.join(pages), JS)
os.makedirs(os.path.join(BH, 'out'), exist_ok=True)
htm = os.path.join(BH, 'out', 'Kosh_%s.html' % K)
io.open(htm, 'w', encoding='utf-8').write(doc)
print('pages', len(pages), '| appendix notes', len(appendix), '|', htm)

if '--no-pdf' not in sys.argv:
    pdf = os.path.join(BH, 'out', 'Jainendra_Siddhant_Kosh_%s%s.pdf' % (K, '' if (A, B) == (1, 99999) else '_p%d-%d' % (A, B)))
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=20000',
                    '--print-to-pdf=' + pdf, 'file:///' + htm.replace('\\', '/')], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('pdf', pdf)
