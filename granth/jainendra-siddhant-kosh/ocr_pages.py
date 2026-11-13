# -*- coding: utf-8 -*-
"""जैनेन्द्र सिद्धान्त कोश — Tesseract OCR, पृष्ठशः।
उपयोग:  python ocr_pages.py K [--from A --to B] [--force]
हर पृष्ठ: स्कैन-छवि निकालो → 2× बड़ा, ग्रे → ऊपर शीर्ष-पंक्ति, नीचे पाद-पंक्ति, बीच में दो स्तम्भ (गटर स्वयं खोजा जाता है)
→ हर भाग अलग से OCR (hin+san, LSTM) → TSV से पंक्तियाँ और अनुच्छेद → bhag-K/pages/p0NNN.md (build_pages.py का प्रारूप)।
कम-विश्वास वाले शब्द पुस्तक में नहीं जाते; वे bhag-K/verify/lowconf.tsv में प्रूफ़-रीडिंग के लिए लिखे जाते हैं।
"""
import io, os, re, sys, subprocess, csv
import pymupdf
from PIL import Image, ImageOps, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TESS = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSDATA = os.path.join(HERE, 'ocr', 'tessdata')
K = sys.argv[1]
arg = lambda n, d=None: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
BH = os.path.join(HERE, 'bhag-%s' % K)
pdf = pymupdf.open(os.path.join(BH, 'mool', 'Jainendra_Siddhant_Kosh_%s.pdf' % K))
A, B = int(arg('--from', 1)), int(arg('--to', len(pdf)))
FORCE = '--force' in sys.argv
TMP = os.path.join(BH, 'ocr_tmp'); os.makedirs(TMP, exist_ok=True)
os.makedirs(os.path.join(BH, 'pages'), exist_ok=True); os.makedirs(os.path.join(BH, 'verify'), exist_ok=True)
LOWCONF = 55

def page_image(i):
    p = pdf[i]
    imgs = p.get_images()
    if imgs:
        im = Image.open(io.BytesIO(pdf.extract_image(imgs[0][0])['image']))
    else:
        pm = p.get_pixmap(dpi=150); im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
    im = ImageOps.grayscale(im)
    im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
    return im

def ink_profile(im, axis):
    """fraction of dark pixels per row (axis=1) or column (axis=0)"""
    bw = im.point(lambda v: 1 if v < 140 else 0)
    w, h = bw.size; px = bw.load()
    if axis == 1:
        return [sum(px[x, y] for x in range(0, w, 3)) / (w / 3) for y in range(h)]
    return [sum(px[x, y] for y in range(0, h, 3)) / (h / 3) for x in range(w)]

def find_bands(im):
    """header bottom, footer top, gutter x"""
    h = im.height; w = im.width
    rows = ink_profile(im, 1)
    # header: first text band in top 8%, ended by the first blank gap after it
    y, top = 0, int(h * 0.09)
    while y < top and rows[y] < 0.002: y += 1
    while y < top and rows[y] >= 0.002: y += 1
    head_end = y if y < top else 0
    # footer: last text band in bottom 7%
    y, bot = h - 1, int(h * 0.93)
    while y > bot and rows[y] < 0.002: y -= 1
    while y > bot and rows[y] >= 0.002: y -= 1
    foot_start = y if y > bot else h
    body = im.crop((0, head_end, w, foot_start))
    cols = ink_profile(body, 0)
    lo, hi = int(w * 0.40), int(w * 0.60)
    # widest run of near-empty columns in the middle band
    best, cur, start = (0, w // 2), 0, lo
    for x in range(lo, hi):
        if cols[x] < 0.004:
            if cur == 0: start = x
            cur += 1
            if cur > best[0]: best = (cur, start + cur // 2)
        else: cur = 0
    return head_end, foot_start, best[1], best[0]

def ocr(img, name, psm=4, lang='hin+san'):
    path = os.path.join(TMP, name + '.png'); img.save(path)
    r = subprocess.run([TESS, path, 'stdout', '--tessdata-dir', TESSDATA, '-l', lang, '--oem', '1', '--psm', str(psm),
                        '-c', 'preserve_interword_spaces=1', 'tsv'], capture_output=True)
    rows = list(csv.DictReader(io.StringIO(r.stdout.decode('utf-8', 'replace')), delimiter='\t', quoting=csv.QUOTE_NONE))
    return rows

def to_paragraphs(rows, region_w, style="hanging"):
    """rows: tesseract TSV words → list of (line_text, left, right, height) → paragraphs"""
    lines, low = {}, []
    for r in rows:
        if r.get('level') != '5' or not (r.get('text') or '').strip(): continue
        key = (int(r['block_num']), int(r['par_num']), int(r['line_num']))
        L = lines.setdefault(key, {'w': [], 'l': 10**9, 'r': 0, 'h': 0, 't': int(r['top'])})
        L['w'].append(r['text']); L['l'] = min(L['l'], int(r['left'])); L['r'] = max(L['r'], int(r['left']) + int(r['width']))
        L['h'] = max(L['h'], int(r['height']))
        try:
            if float(r['conf']) < LOWCONF: low.append((r['text'], float(r['conf'])))
        except ValueError: pass
    seq = [lines[k] for k in sorted(lines, key=lambda k: (lines[k]['t'], lines[k]['l']))]
    if not seq: return [], low
    left_edge = min(L['l'] for L in seq); right_edge = max(L['r'] for L in seq)
    width = right_edge - left_edge
    hs = sorted(L['h'] for L in seq); med_h = hs[len(hs) // 2] or 1
    paras, cur = [], []
    for i, L in enumerate(seq):
        text = ' '.join(L['w']).strip()
        if L['h'] > med_h * 1.28 and len(text) < 90:          # larger type = heading line
            if cur: paras.append(cur); cur = []
            paras.append(['§H§' + text]); continue
        # hanging indent: an entry starts flush left, its continuation lines are indented
        flush_left = L['l'] - left_edge <= width * 0.02
        prev_short = cur and (seq[i - 1]['r'] < right_edge - width * 0.25)
        starts = flush_left if style == 'hanging' else (not flush_left)
        if cur and (starts or prev_short):
            paras.append(cur); cur = []
        cur.append(text)
    if cur: paras.append(cur)
    out = []
    for p in paras:
        s = ''
        for ln in p:
            if s.endswith('-') and not s.endswith(' -'): s = s[:-1] + ln      # rejoin hyphenated word
            else: s = (s + ' ' + ln).strip()
        s = re.sub(r'\s{2,}', ' ', s)
        if s.startswith('§H§'): out.append('### ' + s[3:].replace('§H§', '')); continue
        # numbered sub-headings: "१०. …" / "९ …" alone on a short line → heading
        if re.match(r'^[०-९]{1,3}\.?\s', s) and len(s) < 80: s = '### ' + s
        out.append(s)
    return out, low

lc = open(os.path.join(BH, 'verify', 'lowconf.tsv'), 'a', encoding='utf-8')
for i in range(A - 1, B):
    n = i + 1
    dst = os.path.join(BH, 'pages', 'p%04d.md' % n)
    if os.path.exists(dst) and not FORCE: continue
    im = page_image(i)
    he, fs, gx, gutter = find_bands(im)
    w, h = im.size
    head = im.crop((0, 0, w, he)) if he else None
    foot = im.crop((0, fs, w, h)) if fs < h else None
    c1 = im.crop((0, he, gx, fs)); c2 = im.crop((gx, he, w, fs))
    parts = {}
    single = gutter < 20          # no blank gutter → single-column page (front matter, prefaces)
    regions = (('c1', im.crop((0, he, w, fs))),) if single else (('c1', c1), ('c2', c2))
    parts['c2'] = []
    for nm, reg in regions:
        paras, low = to_paragraphs(ocr(reg, 'p%04d_%s' % (n, nm)), reg.width, 'firstindent' if single else 'hanging')
        parts[nm] = paras
        for t, c in low: lc.write('%d\t%s\t%s\t%.0f\n' % (n, nm, t, c))
    hl = hr = ft = ''
    # running head: faint thin print → raw scan strip, upscale 3×, thicken strokes, single-line OCR per half
    raw = Image.open(io.BytesIO(pdf.extract_image(pdf[i].get_images()[0][0])['image'])).convert('L') if pdf[i].get_images() else None
    if raw is not None:
        rw, rh = raw.size
        hd = raw.crop((0, int(rh * 0.02), rw, int(rh * 0.055)))
        hd = ImageOps.autocontrast(hd.resize((hd.width * 3, hd.height * 3), Image.LANCZOS).filter(ImageFilter.MinFilter(3)))
        words = lambda rows: ' '.join(x['text'] for x in rows if x.get('level') == '5' and (x.get('text') or '').strip())
        hl = words(ocr(hd.crop((0, 0, int(hd.width * 0.45), hd.height)), 'p%04d_hl' % n, 7))
        hr = words(ocr(hd.crop((int(hd.width * 0.40), 0, hd.width, hd.height)), 'p%04d_hr' % n, 7))
    if foot is not None:
        ft = 'जैनेन्द्र सिद्धान्त कोश'   # constant footer on every page
    alltext = ' '.join(parts['c1'] + parts['c2'])
    letters = [c for c in alltext if not c.isspace()]
    deva = sum(1 for c in letters if 'ऀ' <= c <= 'ॿ')
    ratio = deva / len(letters) if letters else 0
    avg_word = (len(letters) / max(1, len(alltext.split())))
    latin = sum(1 for c in letters if c.isascii() and c.isalpha())
    is_latin = letters and latin / len(letters) > 0.35
    if not is_latin and (ratio < 0.8 or len(letters) < 400):
        # Hindi OCR on English print yields Devanagari junk — ask Tesseract's script detector
        sp = os.path.join(TMP, 'p%04d_osd.png' % n); im.crop((0, he, w, fs)).save(sp)
        o = subprocess.run([TESS, sp, 'stdout', '--tessdata-dir', TESSDATA, '--psm', '0'], capture_output=True).stdout.decode('utf-8', 'replace')
        is_latin = 'Script: Latin' in o
    if is_latin:
        # English page (e.g. General Editorial): one column, English model first
        body_im = im.crop((0, he, w, fs))
        paras, low = to_paragraphs(ocr(body_im, 'p%04d_en' % n, 4, 'eng+hin'), body_im.width, 'firstindent')
        toks = re.findall(r'[A-Za-z]+', ' '.join(paras).lower())
        stop = sum(1 for t in toks if t in ('the', 'of', 'and', 'in', 'to', 'is', 'by', 'for', 'which', 'this', 'with'))
        if stop < max(5, 0.06 * len(toks)):     # junk from a table/figure page, not real English prose
            is_latin = False; letters = []
    if is_latin:
        md = ['<!-- PDF %d · OCR (Tesseract eng+hin, single column) -->' % n, '@head-left: ' + hl, '@head-right: ' + hr, '@foot: ' + ft, '',
              '@full', '\n\n'.join(paras), '', '@notes', '- कोई नहीं', '']
        io.open(dst, 'w', encoding='utf-8').write('\n'.join(md))
        print('p%04d  ENGLISH single-column, paras %d' % (n, len(paras)), flush=True)
        continue
    # page-wide table / genealogy chart: OCR flattens it into fragments and stray rule marks
    allp = parts['c1'] + parts['c2']
    short = sum(1 for q in allp if len(q) < 30) / max(1, len(allp))
    junk = len(re.findall(r'[|\[\]^+~=<>]', alltext)) / max(1, len(alltext)) * 100
    tabular = junk >= 1.0 or (short >= 0.6 and junk >= 0.8) or short >= 0.8
    if tabular or len(letters) < 400 or ratio < 0.72 or avg_word < 2.6:
        md = ['<!-- PDF %d · OCR quality too low (deva %.2f, chars %d, wlen %.1f) — original page image used -->' % (n, ratio, len(letters), avg_word),
              '@image', '', '@notes', '- कोई नहीं', '']
        io.open(dst, 'w', encoding='utf-8').write('\n'.join(md))
        io.open(os.path.join(BH, 'verify', 'image_pages.txt'), 'a', encoding='utf-8').write('%d\t%.2f\t%d\n' % (n, ratio, len(letters)))
        print('p%04d  IMAGE (deva %.2f chars %d wlen %.1f)' % (n, ratio, len(letters), avg_word), flush=True)
        continue
    if single:
        md = ['<!-- PDF %d · OCR (Tesseract hin+san, single column) -->' % n, '@head-left: ' + hl, '@head-right: ' + hr, '@foot: ' + ft, '',
              '@full', '\n\n'.join(parts['c1']), '', '@notes', '- कोई नहीं', '']
        io.open(dst, 'w', encoding='utf-8').write('\n'.join(md))
        print('p%04d  single-column, paras %d' % (n, len(parts['c1'])), flush=True)
        continue
    md = ['<!-- PDF %d · OCR (Tesseract hin+san) -->' % n, '@head-left: ' + hl, '@head-right: ' + hr, '@foot: ' + ft, '',
          '@col1', '\n\n'.join(parts['c1']), '', '@col2', '\n\n'.join(parts['c2']), '', '@notes', '- कोई नहीं', '']
    io.open(dst, 'w', encoding='utf-8').write('\n'.join(md))
    print('p%04d  head %d foot %d gutter %d  paras %d+%d' % (n, he, fs, gx, len(parts['c1']), len(parts['c2'])), flush=True)
lc.close()
