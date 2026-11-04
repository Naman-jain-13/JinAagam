# -*- coding: utf-8 -*-
"""v2 pass-1 builder: mool/slice_*.md (print-faithful, stage 1) -> parts/pNN_*.md in the मूलाचार pass-1 format.

Working script — nothing here goes into the book.

The § divisions are v1's (read from _v1/parts/b*.md), keyed x10 (§10 … §2320).
  * part 6 (Sanskrit टीका) = the MAIN text stream (slices p021–p220), cut at each v1 §'s anchor (the start of
    its v1 part 3, or part 1 when it has no part 3). Everything between two anchors goes to the earlier §, so
    nothing in the slices is dropped even where v1 dropped, normalised or re-ordered something.
  * part 1 (Prakrit सूत्र) = the APPENDIX stream (slices p221–p233 = the परिशिष्ट, where the whole मूल पाठ is printed
    continuously), cut at anchors taken from v1 part 1, else from the first bold सूत्र-पद of the § in the main text.
    § without an anchor of their own (टीकाकार's verses, colophons) get no part 1.
  * printed footnotes `(टिप्पण N)` -> inline `[N]` + part 11 line `- (पृष्ठ P) N. …`.
Markers that are not book text are dropped: page comments, `[— हिन्दी अंश छोड़ा —]`, `[सूत्र-पद: …]`, ⟵ / ⟶,
a printed rule `____`, and the परिशिष्ट's own editorial heads `परिशिष्ट`, `परिशिष्ट-प्रथम` ….
The part-1 text drops the `**` bold marks (the whole परिशिष्ट is bold); part 6 KEEPS them — in the टीका they are
the only sign of which words are the quoted प्राकृत सूत्र-पद.

usage:  python make_pass1.py --force    -> (re)writes parts/*.md, verify/pass1_alignment.md  (refuses without --force if parts/ exists)
        python make_pass1.py --check    -> coverage check only (parts vs slices)
"""
import re, glob, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

GRANTH = [(1, 105, 'दैवसिक-रात्रिक प्रतिक्रमण'), (106, 188, 'बृहत्प्रतिक्रमण'), (189, 232, 'आलोचना')]
def granth_of(n): return next(g for a, b, g in GRANTH if a <= n <= b)

# v1 §112–114 repeat what v1 §109 (end), §110 and §111 already hold — a seam duplicate in v1 (the print has that
# text once: one occurrence of each सूत्र-पद in the टीका). They are not carried into v2.
DROP = {112, 113, 114}
# manual appendix anchors (v1 § -> the परिशिष्ट words that open its मूल), where v1's part 1 was a reconstruction
APPX_MANUAL = {143: '=सग्गंथं', 144: '=( कोहं ) ॥ ( खंति )', 146: '=( अखंतिं ) ॥ ( खंतिं ) ॥ अगुत्तिं',
               206: '=पंचें-( चि ) दिया', 103: 'पुष्पदन्तं स्तौमि', 104: 'कुंथुं। शरणमहमितो',
               # each ग्रन्थ's colophon in the परिशिष्ट goes with the § that holds the same colophon / closing verse
               105: 'इति-श्रीगौतमस्वामि-विरचित-दैवसिकादि', 188: 'इति-श्रीगौतमस्वामि-विरचित-बृहत्प्रतिक्रमणा',
               232: 'श्रीगौतमस्वामिकृत-प्रतिक्रमण'}
# output files: (first v1 §, last v1 §, file stem)
FILES = [(1, 21, 'p01'), (22, 39, 'p02'), (40, 55, 'p03'), (56, 69, 'p04'), (70, 82, 'p05'), (83, 96, 'p06'),
         (97, 105, 'p07'), (106, 124, 'p08'), (125, 141, 'p09'), (142, 161, 'p10'), (162, 178, 'p11'),
         (179, 188, 'p12'), (189, 205, 'p13'), (206, 219, 'p14'), (220, 232, 'p15')]

# ---------------- v1 § ----------------
def v1_sections():
    secs = []
    for f in sorted(glob.glob('_v1/parts/b*.md')):
        t = open(f, encoding='utf-8').read().replace('\r\n', '\n')
        for m in re.finditer(r'(?ms)^§\s*(\d+)\s*—\s*(.*?)\n(.*?)(?=^§\s*\d+\s*—|\Z)', t):
            parts, cur = {}, None
            for l in m.group(3).split('\n'):
                h = re.match(r'^##\s*(\d+)\.', l)
                if h: cur = h.group(1); parts[cur] = []; continue
                if cur: parts[cur].append(l)
            secs.append(dict(n=int(m.group(1)), p={k: '\n'.join(v).strip() for k, v in parts.items()}))
    return secs

# ---------------- slice streams ----------------
FN_INLINE = re.compile(r'\(टिप्पण\s*(\d+)\)')
SKIP_LINE = re.compile(r'^(\[— हिन्दी अंश छोड़ा —\]|\[सूत्र-पद:.*\]|\[\(संस्कृत मोटे पद\):.*\]|_{3,}|परिशिष्ट(-प्रथम|-द्वितीय|-तृतीय)?)$')
# headings printed at the top of a HINDI page (the translation's own page head) — not टीका text
HINDI_PAGE_HEADS = {(3, '**प्रतिक्रमणग्रन्थत्रयी**'), (99, '**बृहत् प्रतिक्रमणम्**'), (163, '**आलोचना**')}
PAGE_RE = re.compile(r'^<!--PDF\s*(\d+)\s*\|\s*मुद्रित\s*(\d+)\s*-->')

def stream(files):
    """-> text (paragraphs joined by \\n), page marks [(offset, printed page)], footnotes [(page, num, text)]"""
    paras, fns, page = [], [], None      # paras: [text, [(local offset, page)]]
    for f in files:
        for raw in open(f, encoding='utf-8'):
            s = raw.strip()
            m = PAGE_RE.match(s)
            if m: page = int(m.group(2)); continue
            if not s: continue
            lead = s.startswith('⟵')
            s = s.lstrip('⟵').strip()
            s = re.sub(r'\s*⟶\s*$', '', s)
            if not s or SKIP_LINE.match(s) or (page, s) in HINDI_PAGE_HEADS: continue
            fm = re.match(r'^\(टिप्पण\s*(\d+)\)\s*(.*)$', s)
            if fm: fns.append((page, fm.group(1), fm.group(2).strip())); continue
            s = FN_INLINE.sub(lambda mm: '[%s]' % mm.group(1), s)
            if lead and paras:
                # a sentence continued from the previous page: a printed hyphen/dash at the break joins directly
                sep = '' if re.search(r'[-–]$', paras[-1][0]) else ' '
                paras[-1][1].append((len(paras[-1][0]) + len(sep), page))
                paras[-1][0] += sep + s
            else:
                paras.append([s, [(0, page)]])
    text, marks, pos = [], [], 0
    for t, pm in paras:
        marks += [(pos + o, p) for o, p in pm]
        text.append(t); pos += len(t) + 1
    return '\n'.join(text), marks, fns

def page_at(marks, off):
    p = marks[0][1]
    for o, pg in marks:
        if o <= off: p = pg
        else: break
    return p

def is_dev(ch): return 'ऀ' <= ch <= 'ॿ' and ch not in '।॥०१२३४५६७८९॰'

def norm_map(text):
    """letters/signs only (no danda, no digits, no footnote marks) + map to raw offsets"""
    masked = re.sub(r'\[\d+\]', lambda m: ' ' * len(m.group(0)), text)
    out, idx = [], []
    for i, ch in enumerate(masked):
        if is_dev(ch): out.append(ch); idx.append(i)
    return ''.join(out), idx

def norm(t):
    t = re.sub(r'\(टिप्पण\s*\d+\)|\[\d+\]', '', t)
    return ''.join(ch for ch in t if is_dev(ch))

def clean_v1(t):
    """v1 wrote editorial notes / supplied words in ( ); they are not print text."""
    t = '\n'.join(l for l in t.split('\n') if not re.match(r'^\s*\(.*\)\s*$', l))
    return re.sub(r'\([^)]*\)', '', t)

def find_anchor(ns, cands, start, window, K=(24, 16, 10)):
    for c in cands:
        nc = norm(c[1:]) if c.startswith('=') else norm(clean_v1(c))   # = = exact print words, keep ( )
        if len(nc) < 5: continue
        for off in (0, 4, 10, 20):
            for k in list(K) + [len(nc) - off]:
                a = nc[off:off + k]
                if len(a) < min(k, 7) or len(a) < 5: continue
                j = ns.find(a, start, start + window)
                if j >= 0: return j, off
    return None, None

def snap_back(text, r, lo):
    """move a raw boundary back over opening markup/quotes so '**', '‘' stay with the word they open"""
    while r > lo and (text[r - 1] in '*‘“\'"(' or (text[r - 1] == ' ' and r - 2 >= lo and text[r - 2] == '(')):
        r -= 1
    return r

def snap_sentence(text, r, lo):
    """for an approximate (offset) hit: boundary just after the nearest danda / line start before r"""
    k = max(text.rfind('।', lo, r), text.rfind('॥', lo, r), text.rfind('\n', lo, r))
    if k < 0: return r
    k += 1
    while k < r and text[k] in '।॥* \n’”':
        if text[k] == '*' and text[k:k + 2] == '**' and text.count('**', 0, k) % 2 == 0: break   # an opening **
        k += 1
    return k

# ---------------- segmentation of the टीका ----------------
INTERROG = re.compile(r'^(किं|किम्|कथं|कथम्|कस्य|कस्मै|कस्मात्|कुतः|क्व|कैः|केन|का|कः|के|काः|कीदृश)')

def split_points(p):
    """candidate cut offsets inside one paragraph: after a danda (outside bold and quotes) where a bold
    सूत्र-पद opens the next sentence."""
    pts, bold, q = [], False, 0
    i = 0
    while i < len(p):
        if p.startswith('**', i): bold = not bold; i += 2; continue
        ch = p[i]
        if ch in '‘“': q += 1
        elif ch in '’”': q = max(0, q - 1)
        if ch in '।॥' and not bold and q == 0:
            j = i + 1
            while j < len(p) and p[j] in '।॥०१२३४५६७८९0123456789 ': j += 1
            if p.startswith('**', j) or (INTERROG.match(p[j:]) and '?' in p[j:j + 30]):
                pts.append(j)
        i += 1
    return sorted(set(pts))

def secondary_points(p, lo, hi):
    """sentence ends (outside bold/quotes) usable to break an over-long segment p[lo:hi]"""
    pts, bold, q = [], False, 0
    i = 0
    while i < hi:
        if p.startswith('**', i): bold = not bold; i += 2; continue
        ch = p[i]
        if ch in '‘“': q += 1
        elif ch in '’”': q = max(0, q - 1)
        if i >= lo and ch in '।॥' and not bold and q == 0:
            j = i + 1
            while j < len(p) and p[j] in '।॥ ': j += 1
            if lo < j < hi and not INTERROG.match(p[j:]) and not p[j:].startswith(('इति', 'तदुक्त', 'उक्तं')):
                pts.append(j)
        i += 1
    return pts

MIN_SEG, MAX_SEG = 40, 480

def segments(text):
    segs = []
    for para in text.split('\n'):
        para = para.strip()
        if not para: continue
        cuts = [0] + split_points(para) + [len(para)]
        pieces = [para[a:b].strip() for a, b in zip(cuts, cuts[1:]) if para[a:b].strip()]
        merged = []
        for pc in pieces:                      # merge short pieces forward (keep sūtra-word + gloss together)
            if merged and len(merged[-1]) < MIN_SEG:
                merged[-1] = merged[-1] + ' ' + pc
            else:
                merged.append(pc)
        if len(merged) > 1 and len(merged[-1]) < MIN_SEG // 2:
            tail = merged.pop(); merged[-1] += ' ' + tail
        out = []
        for pc in merged:                      # break over-long pieces at plain sentence ends
            while len(pc) > MAX_SEG:
                pts = [x for x in secondary_points(pc, 180, len(pc) - 120)]
                if not pts: break
                x = min(pts, key=lambda v: abs(v - min(len(pc) // 2, 320)))
                out.append(pc[:x].strip()); pc = pc[x:].strip()
            out.append(pc)
        segs += out
    return segs

def balance_bold(s):
    """a § cut that falls inside a **bold** span leaves one '**' unpaired — close/open it at the edge"""
    if s.count('**') % 2 == 0: return s
    first = s.find('**')
    # unpaired opening at the end?  heuristic: if the text before the first ** has Devanagari, the span began in the previous §
    return ('**' + s) if norm(s[:first]) else (s + '**')

# ---------------- main ----------------
MAIN = sorted(f for f in glob.glob('mool/slice_p*.md') if int(re.search(r'p(\d+)-', f).group(1)) < 221)
APPX = sorted(f for f in glob.glob('mool/slice_p*.md') if int(re.search(r'p(\d+)-', f).group(1)) >= 221)

def build():
    secs = [s for s in v1_sections() if s['n'] not in DROP]
    mtext, mmarks, mfns = stream(MAIN)
    atext, amarks, afns = stream(APPX)
    mn, mi = norm_map(mtext)
    an, ai = norm_map(atext)
    log = []
    # --- main boundaries
    mb = []
    last = 0
    for i, s in enumerate(secs):
        if i == 0: mb.append(0); continue
        cands = [s['p'][k] for k in ('3', '1') if s['p'].get(k)]
        j, off = find_anchor(mn, cands, last, 30000)
        if j is None: raise SystemExit('main anchor not found for v1 §%d' % s['n'])
        r = mi[j]
        r = snap_sentence(mtext, r, mi[last] if last else 0) if off else snap_back(mtext, r, mb[-1])
        mb.append(r); last = j + 1
        if off: log.append('§%d: टीका-आरम्भ v1 से %d अक्षर बाद मिला; सीमा वाक्य-आरम्भ पर रखी' % (s['n'] * 10, off))
    mb.append(len(mtext))
    # a § must not end on a bare सूत्र-पद whose gloss opens the next § (v1 cut some glosses that way): move such a
    # trailing **पद** over to the next §. Only where checked by hand: at other § ends a closing bold word is the last
    # word of a verse being glossed (e.g. 'वीराय नमः') and stays.
    for i in range(1, len(secs)):
        if secs[i]['n'] not in (144, 146): continue
        b = mb[i]
        m = re.search(r'(?<=[^\n])\*\*([^*\n]{1,40})\*\*[।॥\s]*$', mtext[max(mb[i - 1], b - 80):b])
        if m:
            nb = b - len(m.group(0))
            if nb > mb[i - 1]:
                mb[i] = nb
                log.append('§%d: पिछले § के अन्त का सूत्र-पद «%s» इस § में लाया (उसकी टीका यहीं है)' % (secs[i]['n'] * 10, m.group(1)))
    # --- appendix boundaries
    ab = [None] * len(secs)
    lasta = 0
    for i, s in enumerate(secs):
        cands = []
        if s['n'] in APPX_MANUAL: cands.append(APPX_MANUAL[s['n']])
        if s['p'].get('1'): cands.append(s['p']['1'])
        # first bold सूत्र-पद of this § in the main text
        body = mtext[mb[i]:mb[i + 1]]
        bolds = re.findall(r'\*\*(.+?)\*\*', body)
        bolds = [b for b in bolds if not b.startswith('टीका') and len(norm(b)) >= 5][:2]
        cands += bolds
        if s['n'] in (1,): cands = [s['p']['1']]
        # a § that only continues the previous §'s टीका (v1 repeated the same सूत्र, or the § quotes no सूत्र-पद) has no मूल of its own
        if i and s['n'] not in APPX_MANUAL and (not bolds or norm(clean_v1(s['p'].get('1', ''))) == norm(clean_v1(secs[i - 1]['p'].get('1', '')))):
            continue
        j, off = find_anchor(an, cands, lasta, 2500, K=(20, 14, 9))
        if j is None: continue
        if i == 0: ab[i] = 0; lasta = 0; continue
        r = ai[j]
        r = snap_sentence(atext, r, ai[lasta]) if off else snap_back(atext, r, 0)
        if any(x is not None and x >= r for x in ab[:i]):
            log.append('§%d: परिशिष्ट-अनुरूप स्थान क्रम-विरुद्ध — छोड़ा' % (s['n'] * 10)); continue
        ab[i] = r; lasta = j + 1
        if off: log.append('§%d: मूल-पाठ (परिशिष्ट) v1 से %d अक्षर बाद मिला; सीमा वाक्य-आरम्भ पर रखी' % (s['n'] * 10, off))
    # appendix spans: from each anchor to the next anchor
    aspan = [None] * len(secs)
    idxs = [i for i in range(len(secs)) if ab[i] is not None]
    for k, i in enumerate(idxs):
        end = ab[idxs[k + 1]] if k + 1 < len(idxs) else len(atext)
        aspan[i] = (ab[i], end)
    if idxs and idxs[0] != 0: aspan[idxs[0]] = (0, aspan[idxs[0]][1])
    # --- footnotes: attach to the § whose span holds the [N] mark on that page
    fn_by_sec = {}
    for (pg, num, txt) in mfns:
        hit = None
        for mm in re.finditer(r'\[%s\]' % num, mtext):
            if page_at(mmarks, mm.start()) == pg: hit = mm.start(); break
        if hit is None:
            # no mark in the text: attach to the § holding the end of that page
            hit = max(o for o, p in mmarks if p <= pg)
            log.append('पृष्ठ %d टिप्पण %s: पाठ में चिह्न नहीं मिला — पृष्ठ के § से जोड़ी' % (pg, num))
        si = max(i for i in range(len(secs)) if mb[i] <= hit)
        fn_by_sec.setdefault(si, []).append((pg, num, txt))
    # --- write
    out_files = {}
    for i, s in enumerate(secs):
        key = s['n'] * 10
        a, b = mb[i], mb[i + 1]
        tika = balance_bold(mtext[a:b].strip())
        if mtext[a:b].count('**') % 2:
            log.append('§%d: § की सीमा किसी मोटे (**) अंश के भीतर पड़ी — चिह्न सन्तुलित किया' % key)
        p1 = p2 = page_at(mmarks, a)
        p2 = page_at(mmarks, max(a, b - 2))
        pages = '%d' % p1 if p1 == p2 else '%d–%d' % (p1, p2)
        g = granth_of(s['n'])
        L = ['§%d — सूत्र %d (%s, मुद्रित पृष्ठ %s)' % (key, s['n'], g, pages), '']
        ref = 'सन्दर्भ-संकेत: प्रतिक्रमण-ग्रन्थत्रयी — %s, मुद्रित पृष्ठ %s (टीका-सहित पाठ)' % (g, pages)
        if aspan[i]:
            x, y = aspan[i]
            q1, q2 = page_at(amarks, x), page_at(amarks, max(x, y - 2))
            ref += '; मूल पाठ परिशिष्ट, मुद्रित पृष्ठ %s' % (q1 if q1 == q2 else '%d–%d' % (q1, q2))
        L += [ref + '।', '']
        if aspan[i]:
            x, y = aspan[i]
            mool = atext[x:y].strip()
            mool = re.sub(r'\*\*', '', mool)
            mool = '\n'.join(l.strip() for l in mool.split('\n') if l.strip())
            if norm(mool):
                q1, q2 = page_at(amarks, x), page_at(amarks, max(x, y - 2))
                L += ['## 1. मूल पाठ (प्राकृत सूत्र)', '(पृष्ठ %s, परिशिष्ट)' % (q1 if q1 == q2 else '%d–%d' % (q1, q2)), mool, '']
        L += ['## 6. श्री प्रभाचन्द्र-कृत संस्कृत टीका (मूल)']
        for k, sg in enumerate(segments(tika), 1):
            L.append('(T%d) %s' % (k, sg))
        if i in fn_by_sec:
            L += ['', '## 11. मुद्रित पाद-टिप्पणी']
            for pg, num, txt in fn_by_sec[i]:
                L.append('- (पृष्ठ %d) %s. %s' % (pg, num, txt))
        stem = next(f for lo, hi, f in FILES if lo <= s['n'] <= hi)
        out_files.setdefault(stem, []).append('\n'.join(L).rstrip() + '\n')
    os.makedirs('parts', exist_ok=True)
    for f in glob.glob('parts/*.md'): os.remove(f)
    for lo, hi, stem in FILES:
        if stem not in out_files: continue
        name = 'parts/%s_s%04d-%04d.md' % (stem, lo * 10, hi * 10)
        open(name, 'w', encoding='utf-8', newline='\n').write('\n---\n\n'.join(out_files[stem]))
    return secs, mtext, atext, mfns, log, aspan

# ---------------- coverage check ----------------
def raw_slice_text(files):
    """Independent of stream(): every Devanagari character of the slice files, minus only the stage-1 markers
    (page comments, [— हिन्दी अंश छोड़ा —], [सूत्र-पद: …], ⟵ ⟶, (टिप्पण N) marks) and minus footnote lines,
    which are returned separately."""
    body, fns = [], []
    for f in files:
        for l in open(f, encoding='utf-8'):
            s = l.strip().lstrip('⟵').rstrip('⟶').strip()
            if not s or s.startswith('<!--') or s.startswith('[— हिन्दी') or s.startswith('[सूत्र-पद') or s.startswith('[(संस्कृत मोटे पद)'): continue
            if s.startswith('(टिप्पण'): fns.append(s); continue
            body.append(s)
    return '\n'.join(body), fns

def letters(t):
    t = re.sub(r'\(टिप्पण\s*\d+\)|\[\d+\]', '', t)
    return ''.join(ch for ch in t if 'ऀ' <= ch <= 'ॿ')

def check():
    """concatenated part 6 vs the main slices, concatenated part 1 vs the परिशिष्ट slices — every Devanagari
    character (letters, signs, dandas, digits) compared in order; whitespace, ** and footnote marks ignored."""
    import difflib
    msrc, mfns = raw_slice_text(MAIN)
    asrc, _ = raw_slice_text(APPX)
    p1, p6, fn = [], [], []
    for f in sorted(glob.glob('parts/*.md')):
        cur = None
        for l in open(f, encoding='utf-8').read().split('\n'):
            if l.startswith('§') or l.strip() == '---': cur = None; continue
            h = re.match(r'^##\s*(\d+)\.', l)
            if h: cur = h.group(1); continue
            if cur == '1' and not re.match(r'^\(पृष्ठ', l): p1.append(l)
            elif cur == '6': p6.append(re.sub(r'^\(T\d+\)\s*', '', l))
            elif cur == '11' and l.strip(): fn.append(re.sub(r'^- \(पृष्ठ \d+\) \d+\. ', '', l))
    res = []
    for name, mine, src in (('भाग 6 (टीका) बनाम मुख्य पाठ की स्लाइस p021–220', '\n'.join(p6), msrc),
                            ('भाग 1 (मूल) बनाम परिशिष्ट की स्लाइस p221–233', '\n'.join(p1), asrc)):
        a, b = letters(mine), letters(src)
        if a == b:
            res.append('%s: स्लाइस %d अक्षर = parts %d अक्षर — पूर्ण मेल (100%%)' % (name, len(b), len(a)))
            continue
        # word tokens (fast); characters counted for the percentage
        wa = [w for w in re.split(r'[^ऀ-ॿ]+', re.sub(r'\(टिप्पण\s*\d+\)|\[\d+\]', '', mine)) if w]
        wb = [w for w in re.split(r'[^ऀ-ॿ]+', re.sub(r'\(टिप्पण\s*\d+\)', '', src)) if w]
        sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
        same = sum(len(''.join(wb[x.b:x.b + x.size])) for x in sm.get_matching_blocks())
        res.append('%s: स्लाइस %d अक्षर, parts में %d; मेल %d (%.3f%%)' % (name, len(b), len(a), same, 100.0 * same / max(1, len(b))))
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != 'equal':
                res.append('    भेद (%s): parts «%s» ↔ स्लाइस «%s»' % (op, ' '.join(wa[i1:i2])[:60], ' '.join(wb[j1:j2])[:60]))
    srcfn = [re.sub(r'^\(टिप्पण\s*\d+\)\s*', '', x) for x in mfns]
    res.append('पाद-टिप्पणी: स्लाइस %d, parts %d, पाठ-मेल %s' % (len(srcfn), len(fn), 'हाँ' if [letters(x) for x in srcfn] == [letters(x) for x in fn] else 'नहीं'))
    return res

if __name__ == '__main__':
    if '--check' not in sys.argv:
        if glob.glob('parts/*.md') and '--force' not in sys.argv:
            raise SystemExit('parts/ already exists (and may hold RECHECK corrections) — not overwriting. Use --check, or --force to regenerate.')
        secs, mtext, atext, mfns, log, aspan = build()
        no1 = [s['n'] * 10 for i, s in enumerate(secs) if not aspan[i]]
        os.makedirs('verify', exist_ok=True)
        with open('verify/pass1_alignment.md', 'w', encoding='utf-8') as f:
            f.write('# पास-1 (v2) — v1 विभाजन से संरेखण की टिप्पणियाँ\n\n*(कार्य-फ़ाइल; पुस्तक में नहीं जाती। make_pass1.py द्वारा लिखित।)*\n\n')
            f.write('- § कुल: %d (v1 के 232 में से §1120, §1130, §1140 छोड़े — v1 में दोहराव)\n' % len(secs))
            f.write('- भाग 1 (मूल पाठ, परिशिष्ट से) रहित §: %s\n\n' % ', '.join('§%d' % k for k in no1))
            f.write('\n'.join('- ' + l for l in log) + '\n')
        print('§ written:', len(secs), '| without part 1:', len(no1))
    print('\n'.join(check()))
