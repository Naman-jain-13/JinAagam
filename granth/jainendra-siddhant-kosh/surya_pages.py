# -*- coding: utf-8 -*-
"""जैनेन्द्र सिद्धान्त कोश — Surya OCR (VLM, llama.cpp CUDA), पृष्ठशः।
उपयोग:  python surya_pages.py K [--from A --to B] [--force] [--convert-only]
हर पृष्ठ: मूल PDF से 192 dpi छवि → Surya full-page OCR (layout + पाठ + सारणी एक साथ) → bhag-K/surya/p0NNN.json
→ bhag-K/pages/p0NNN.md (प्रारूप v2: खण्डशः @full / @col1 / @col2, हर खण्ड में साफ़ किया हुआ HTML)।
सारणी HTML-सारणी बनती है; चित्र (Picture/Figure) मूल स्कैन से काटकर लगाया जाता है; जिस खण्ड को Surya न पढ़ पाए
उसका भी मूल अंश ही लगता है और verify/surya_issues.tsv में दर्ज होता है।
"""
import io, os, re, sys, json, html
import pymupdf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
K = sys.argv[1]
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
BH = os.path.join(HERE, 'bhag-%s' % K)
pdf = pymupdf.open(os.path.join(BH, 'mool', 'Jainendra_Siddhant_Kosh_%s.pdf' % K))
A, B = int(arg('--from', 1)), int(arg('--to', len(pdf)))
FORCE = '--force' in sys.argv
DPI = 192
JS = os.path.join(BH, 'surya'); PG = os.path.join(BH, 'pages'); IMG = os.path.join(BH, 'out', 'img')
for d in (JS, PG, IMG, os.path.join(BH, 'verify')): os.makedirs(d, exist_ok=True)

os.environ.setdefault('SURYA_INFERENCE_BACKEND', 'llamacpp')
os.environ.setdefault('LLAMA_CPP_BINARY', os.path.join(HERE, 'ocr', 'llama-cuda', 'llama-server.exe'))
os.environ.setdefault('SURYA_GGUF_MODEL_FILE', 'surya-2.5.gguf')
os.environ.setdefault('SURYA_INFERENCE_PARALLEL', '3')
os.environ.setdefault('HF_HUB_DISABLE_SYMLINKS_WARNING', '1')

# sideways-printed pages (wide tables): Tesseract OSD result from ocr/detect_rotation.py; OCR sees them upright
ROT = {}
_rt = os.path.join(BH, 'verify', 'rotation.tsv')
if os.path.exists(_rt):
    for l in io.open(_rt, encoding='utf-8'):
        p = l.split('\t')
        if len(p) >= 2 and p[1] in ('90', '180', '270'): ROT[int(p[0])] = int(p[1])

def render(n):
    pm = pdf[n - 1].get_pixmap(dpi=DPI)
    im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
    return im.rotate(-ROT[n], expand=True) if n in ROT else im

# ---------- OCR ----------
def run_ocr(todo):
    from surya.inference import SuryaInferenceManager
    from surya.recognition import RecognitionPredictor
    manager = SuryaInferenceManager()
    rec = RecognitionPredictor(manager)
    BATCH = 6
    try:
        for s in range(0, len(todo), BATCH):
            ns = todo[s:s + BATCH]
            res = rec([render(n) for n in ns], full_page=True)
            for n, r in zip(ns, res):
                io.open(os.path.join(JS, 'p%04d.json' % n), 'w', encoding='utf-8').write(json.dumps(r.model_dump(), ensure_ascii=False))
                convert(n)
            print('done', ns[0], '-', ns[-1], flush=True)
    finally:
        try: manager.stop()
        except Exception: pass

# ---------- JSON → page file ----------
OK_TAGS = {'b', 'i', 'u', 'sup', 'sub', 'br', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'p', 'span', 'img'}
def clean(h):
    """keep only harmless formatting / table tags; drop attributes except rowspan/colspan/src"""
    def tag(m):
        close, name, attrs = m.group(1), m.group(2).lower(), m.group(3) or ''
        if name not in OK_TAGS: return ''
        keep = ' '.join(a for a in re.findall(r'(?:rowspan|colspan)="\d+"', attrs))
        return '<%s%s%s>' % (close, name, (' ' + keep) if keep and not close else '')
    h = re.sub(r'(<|&lt;)\|[^|<>&]*\|(>|&gt;)', '', h)        # leaked model control tokens
    # math printed as LaTeX: \frac{a}{b} → a/b, \text{x} → x, other commands dropped
    for _ in range(3): h = re.sub(r'\\text\{([^{}]*)\}', r'\1', h)
    for _ in range(3): h = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', r'\1/\2', h)
    h = re.sub(r'\\[a-zA-Z]+', '', h).replace('\\(', '').replace('\\)', '')
    h = re.sub(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*)>', tag, h)
    return re.sub(r'\s*\n\s*', ' ', h).strip()

def text_of(h): return html.unescape(re.sub(r'<[^>]+>', ' ', h)).strip()

def crop(n, k, bbox, im=None):
    im = im or render(n)
    x0, y0, x1, y1 = [int(v) for v in bbox]
    p = 'p%04d_b%02d.png' % (n, k)
    im.crop((max(0, x0 - 4), max(0, y0 - 4), min(im.width, x1 + 4), min(im.height, y1 + 4))).save(os.path.join(IMG, p))
    return '<img src="img/%s">' % p

def convert(n):
    r = json.load(io.open(os.path.join(JS, 'p%04d.json' % n), encoding='utf-8'))
    W = r['image_bbox'][2]; mid = W / 2
    blocks = sorted(r['blocks'], key=lambda b: b['reading_order'])
    heads, foots, segs, issues = [], [], [], []
    im = None
    def put(where, h):
        if where == 'full':
            segs.append(['full', [h]]) if not segs or segs[-1][0] != 'full' else segs[-1][1].append(h)
        else:
            if not segs or segs[-1][0] != 'cols': segs.append(['cols', [], []])
            segs[-1][1 if where == 'c1' else 2].append(h)
    for k, b in enumerate(blocks):
        lab = b['label']; x0, y0, x1, y1 = b['bbox']; h = b.get('html') or ''
        if lab == 'PageHeader': heads.append((x0, text_of(h))); continue
        if lab == 'PageFooter': foots.append((x0, text_of(h))); continue
        where = 'full' if (x0 < mid - 30 and x1 > mid + 30) else ('c1' if (x0 + x1) / 2 < mid else 'c2')
        if b.get('skipped') or b.get('error') or lab in ('Picture', 'Figure') or not text_of(h):
            if lab not in ('Picture', 'Figure'): issues.append((n, k, lab, 'unread'))
            im = im or render(n); put(where, crop(n, k, b['bbox'], im)); continue
        c = clean(h)
        if lab == 'SectionHeader': c = '<h3>%s</h3>' % re.sub(r'</?p>', '', c)
        elif lab == 'Table': c = c if c.startswith('<table') else '<table>%s</table>' % c
        elif not c.startswith('<p'): c = '<p>%s</p>' % c
        put(where, c)
    # dense chart/number grid the VLM could not read (little text for a lot of ink) → keep the original page image
    chars = sum(len(text_of(h)) for s in segs for part in s[1:] for h in part if not h.startswith('<img'))
    pm = pdf[n - 1].get_pixmap(dpi=40, colorspace=pymupdf.csGRAY)
    ink = sum(1 for v in pm.samples if v < 128) / len(pm.samples)
    if ink > 0.03 and chars < 8100 * ink:
        io.open(os.path.join(PG, 'p%04d.md' % n), 'w', encoding='utf-8').write(
            '<!-- PDF %d · Surya read only %d chars of a dense page (ink %.3f) — original page image used -->\n@image\n\n@notes\n- कोई नहीं\n' % (n, chars, ink))
        with io.open(os.path.join(BH, 'verify', 'surya_issues.tsv'), 'a', encoding='utf-8') as f: f.write('%d\t-\tpage\timage\n' % n)
        return
    heads.sort()
    hl =heads[0][1] if heads else ''
    hc = ' '.join(t for x, t in heads[1:] if x < W * 0.6) if len(heads) > 1 else ''
    hr = ' '.join(t for x, t in heads[1:] if x >= W * 0.6)
    foots.sort()
    out = ['<!-- PDF %d · OCR (Surya 2.5) -->' % n, '@v2', '@head-left: ' + hl, '@head-center: ' + hc, '@head-right: ' + hr,
           '@foot: ' + ' · '.join(t for x, t in foots)] + (['@rotate: %d' % ROT[n]] if n in ROT else []) + ['']
    for s in segs:
        if s[0] == 'full': out += ['@full'] + s[1] + ['']
        else: out += ['@col1'] + s[1] + ['', '@col2'] + s[2] + ['']
    out += ['@notes', '- कोई नहीं', '']
    io.open(os.path.join(PG, 'p%04d.md' % n), 'w', encoding='utf-8').write('\n'.join(out))
    if issues:
        with io.open(os.path.join(BH, 'verify', 'surya_issues.tsv'), 'a', encoding='utf-8') as f:
            for t in issues: f.write('%d\t%d\t%s\t%s\n' % t)

pages = list(range(A, B + 1))
if '--convert-only' in sys.argv:
    for n in pages:
        if os.path.exists(os.path.join(JS, 'p%04d.json' % n)): convert(n)
    print('converted'); sys.exit()
todo = [n for n in pages if FORCE or not os.path.exists(os.path.join(JS, 'p%04d.json' % n))]
print('pages to OCR:', len(todo), flush=True)
if todo: run_ocr(todo)
