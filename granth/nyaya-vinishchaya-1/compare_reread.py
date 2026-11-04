# -*- coding: utf-8 -*-
"""मूल की दूसरी (स्वतन्त्र) पढ़ाई को parts/ के मूल पाठ से पृष्ठ-दर-पृष्ठ, शब्दशः मिलाता है।

    python compare_reread.py                # reread/ की सब फ़ाइलें
    python compare_reread.py r309-314       # केवल यह फ़ाइल

हर पढ़े गए पृष्ठ के भेद verify2/diff_pNNN.md में: पहला पाठ (parts) बनाम दूसरा पाठ (reread), दोनों ओर कुछ
शब्दों का प्रसङ्ग, और वह § जिसमें पहला पाठ है। केवल वे भेद गिने जाते हैं जहाँ दोनों पढ़ाइयों ने अक्षर पढ़े
हों — `[अस्पष्ट]` बनाम कोई शब्द भी सूची में आता है (वहाँ एक पढ़ाई ने कुछ पढ़ा, दूसरी ने नहीं)।
"""
import difflib
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# "(पृष्ठ 237)", "(पृष्ठ 117 से 118)" / "(पृष्ठ 69 और 70)" (दो पृष्ठों में बँटा खण्ड), "(पृष्ठ 88:) …पाठ…",
# "(पृष्ठ 115) …पाठ…" (चिह्न के बाद उसी पंक्ति में पाठ) — पर "(पृष्ठ 327, 1)" टिप्पण-पंक्ति और "…की टिप्पणियाँ…" सूचना नहीं।
PAGE = re.compile(r'^\(पृष्ठ (\d+)(?:\s*(?:से|और|–|-)\s*(\d+))?(?![\d,])(?P<note>[^)]*)\)\s*(?P<rest>.*)$')
SPANS = set()                                               # ऐसे पृष्ठ-युगल — मिलान में चेतावनी के लिए
SEC = re.compile(r'^§(\d+)\b')


def norm_tokens(text):
    t = text.replace('**', '').translate(str.maketrans('0123456789', '०१२३४५६७८९'))  # अरबी/देवनागरी अङ्क एक
    t = re.sub(r'॥\s*([०-९]+)\s*॥', r'॥\1॥', t)
    t = re.sub(r'\[अस्पष्ट[^\]]*\]', ' UNCLEAR ', t)        # [अस्पष्ट], [अस्पष्ट पंक्ति], [अस्पष्ट पंक्ति-अंश]
    t = re.sub(r'\[[^\]]*\]', ' ', t)                        # टिप्पण-चिह्न, सम्पादक के स्थल-निर्देश [प्र० वा० …]
    t = re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]+', '', t)
    t = re.sub(r'[“”"\'‘’()`{}]', ' ', t)                     # उद्धरण-चिह्नों की शैली दोनों पढ़ाइयों में भिन्न
    t = re.sub(r'\s*([।॥;:,?!—–-])\s*', r' \1 ', t)
    t = re.sub(r'(?<=\S)\s+(?=ऽ)', '', t)
    toks = [w for w in t.split() if w not in ('।', ';', ',', ':', '—', '–', '-', '?', '!')]
    return ['⟨?⟩' if w == 'UNCLEAR' else w for w in toks]


def parts_by_page():
    pages = {}
    for f in sorted(glob.glob('parts/batch*.md')):
        sec, page, inblock = None, None, False
        for line in io.open(f, encoding='utf-8'):
            line = line.rstrip('\n')
            m = SEC.match(line)
            if m:
                sec, inblock = m.group(1), False
                continue
            if line.startswith('## 1.'):
                inblock = True
                continue
            if line.startswith('## '):
                inblock = False
                continue
            if not inblock:
                continue
            m = PAGE.match(line)
            if m and 'टिप्पण' not in m.group('note'):
                page = int(m.group(1))
                if m.group(2):
                    SPANS.update((page, int(m.group(2))))
                if m.group('rest').strip() and not m.group('note').strip():
                    pages.setdefault(page, []).append((sec, m.group('rest')))
                continue
            if line.startswith('सम्पादकीय टिप्पण') or line.startswith('(पृष्ठ ') or line.startswith('(छपाई') \
                    or line.startswith('[सूचना') or not line.strip() or page is None:
                if line.startswith('सम्पादकीय टिप्पण'):
                    page = None          # अगला "(पृष्ठ N)" आने तक टिप्पण-खण्ड
                continue
            pages.setdefault(page, []).append((sec, line))
    return pages


def reread_pages(names):
    pages = {}
    for f in names:
        page = None
        for line in io.open(f, encoding='utf-8'):
            m = re.match(r'^#\s*मुद्रित\s+(\d+)', line)
            if m:
                page = int(m.group(1))
                pages.setdefault(page, [])
                continue
            if page is not None and line.strip():
                pages[page].append(line.rstrip('\n'))
    return pages


def main():
    only = sys.argv[1:]
    files = sorted(glob.glob('reread/r*.md'))
    if only:
        files = [f for f in files if any(o in f for o in only)]
    first = parts_by_page()
    second = reread_pages(files)
    os.makedirs('verify2', exist_ok=True)
    total = 0
    for page in sorted(second):
        a_tok, a_sec = [], []
        for sec, line in first.get(page, []):
            ts = norm_tokens(line)
            a_tok += ts
            a_sec += [sec] * len(ts)
        b_tok = norm_tokens('\n'.join(second[page]))
        sm = difflib.SequenceMatcher(None, a_tok, b_tok, autojunk=False)
        out, n = [], 0
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal':
                continue
            a, b = ' '.join(a_tok[i1:i2]), ' '.join(b_tok[j1:j2])
            if a.replace('⟨?⟩', '') == '' and b.replace('⟨?⟩', '') == '':
                continue
            n += 1
            ctx_l = ' '.join(a_tok[max(0, i1 - 4):i1])
            ctx_r = ' '.join(a_tok[i2:i2 + 4])
            sec = a_sec[i1] if i1 < len(a_sec) else (a_sec[-1] if a_sec else '?')
            out.append('- D%d · §%s · …%s ⟦पहला: %s⟧ ⟦दूसरा: %s⟧ %s…' % (n, sec, ctx_l, a or '∅', b or '∅', ctx_r))
        ratio = sm.ratio()
        head = ['# मुद्रित %d — दो पढ़ाइयों का मिलान' % page, '',
                'पहला पाठ (parts) %d शब्द · दूसरा पाठ %d शब्द · समानता %.3f · भेद %d' % (
                    len(a_tok), len(b_tok), ratio, n), '']
        if not first.get(page):
            head.append('**सावधान:** parts में इस पृष्ठ का "(पृष्ठ %d)" चिह्न नहीं मिला।' % page)
        if page in SPANS:
            head.append('**सावधान:** parts में यह पृष्ठ "(पृष्ठ N से M)" वाले खण्ड का अंश है — उस खण्ड में स्कैन के असली '
                        'पृष्ठ-विराम पर "(पृष्ठ M)" चिह्न लगाइए, फिर यह मिलान दोबारा चलाइए।')
        io.open('verify2/diff_p%03d.md' % page, 'w', encoding='utf-8').write('\n'.join(head + out) + '\n')
        total += n
        print('मुद्रित %3d  समानता %.3f  भेद %3d' % (page, ratio, n))
    print('कुल भेद', total)


if __name__ == '__main__':
    main()
