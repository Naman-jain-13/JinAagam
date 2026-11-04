# -*- coding: utf-8 -*-
"""दो स्वतन्त्र पढ़ाइयों (mool/slice_*.md बनाम mool/reread_*.md) का पृष्ठ-दर-पृष्ठ शब्दशः मिलान → verify/diff_sNNN.md

    python compare_slices.py                # सब
    python compare_slices.py 15 16 17       # केवल ये स्कैन-पृष्ठ
"""
import difflib, glob, io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
MARK = re.compile(r'^<!--\s*PDF\s+(\d+)\b.*?-->\s*$')

def load(pattern):
    pages = {}
    for f in sorted(glob.glob(pattern)):
        cur = None
        for line in io.open(f, encoding='utf-8'):
            m = MARK.match(line.strip())
            if m:
                cur = int(m.group(1)); pages.setdefault(cur, []); continue
            if cur is not None and line.strip():
                pages[cur].append(line.rstrip('\n'))
    return pages

def toks(lines):
    t = '\n'.join(lines).replace('**', '').translate(str.maketrans('0123456789', '०१२३४५६७८९'))
    t = re.sub(r'\[— हिन्दी अंश छोड़ा —\]', ' ', t)
    t = re.sub(r'\[अस्पष्ट[^\]]*\]', ' UNCLEAR ', t)
    t = re.sub(r'\[शीर्ष:\s*([^\]]*)\]', r' \1 ', t)
    t = re.sub(r'[⟵⟶“”"\'‘’()`{}\[\]]', ' ', t)
    t = re.sub(r'॥\s*([०-९]+)\s*॥', r'॥\1॥', t)
    t = re.sub(r'\s*([।॥;:,?!—–-])\s*', r' \1 ', t)
    w = [x for x in t.split() if x not in ('।', ';', ',', ':', '—', '–', '-', '?', '!')]
    return ['⟨?⟩' if x == 'UNCLEAR' else x for x in w]

def main():
    only = {int(a) for a in sys.argv[1:]}
    A, B = load('mool/slice_k*.md'), load('mool/reread_*.md')
    os.makedirs('verify', exist_ok=True)
    tot = 0
    for p in sorted(set(B) & set(A)):
        if only and p not in only: continue
        a, b = toks(A[p]), toks(B[p])
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        out, n = [], 0
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == 'equal': continue
            x, y = ' '.join(a[i1:i2]), ' '.join(b[j1:j2])
            if x.replace('⟨?⟩', '').strip() == '' and y.replace('⟨?⟩', '').strip() == '': continue
            n += 1
            out.append('- D%d · …%s ⟦पहला: %s⟧ ⟦दूसरा: %s⟧ %s…' % (n, ' '.join(a[max(0,i1-4):i1]), x or '∅', y or '∅', ' '.join(a[i2:i2+4])))
        head = ['# स्कैन %d — दो पढ़ाइयों का मिलान' % p, '', 'पहला %d शब्द · दूसरा %d शब्द · समानता %.3f · भेद %d' % (len(a), len(b), sm.ratio(), n), '']
        io.open('verify/diff_s%03d.md' % p, 'w', encoding='utf-8').write('\n'.join(head + out) + '\n')
        tot += n
        print('स्कैन %3d  समानता %.3f  भेद %3d' % (p, sm.ratio(), n))
    print('कुल भेद', tot)
if __name__ == '__main__':
    main()
