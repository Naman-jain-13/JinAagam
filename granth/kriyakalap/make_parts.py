"""src/ (मूल) + addenda/ (व्याख्या) -> parts/ (build_docx.js के लिए § फ़ाइलें)
- हर § : `§N — <शीर्षक>` (N = कुंजी÷10), `## 1. मूल पाठ` (टीका-रहित अनुच्छेद), `## 6. … टीका (मूल)` (टीका के अनुच्छेद, (Tn) टैग सहित)
- टीका-अनुच्छेद = वे (Pn) जिनका Hindi addenda के भाग 6 में उसी टैग से है।
- addenda के भाग 6 में (Pn) -> (Tn) (build_docx.js यही पहचानता है)।
"""
import re, os, json, sys, glob
sys.stdout.reconfigure(encoding='utf-8')
M = json.load(open('sections.json', encoding='utf-8'))
os.makedirs('parts', exist_ok=True)
os.makedirs('addenda_b', exist_ok=True)

def clean_mool(p):
    p = re.sub(r'\[शीर्ष:\s*([^\]]*)\]', lambda m: '**' + m.group(1).strip(' —।') + '**', p)
    p = p.replace('⟵', '').replace('⟶', '')
    p = re.sub(r'\*\(पृष्ठ-शीर्ष\)\*', '', p)
    return p

TIKA_MARK = re.compile(r'(?<![^\s])टीका\s*[:—\-]')
VEND = re.compile(r'॥\s*[०-९0-9]+(?:\s*[-–]\s*[०-९0-9]+)?\s*॥')
def split_verse(body):
    """टीका-अनुच्छेद से उसका मूल श्लोक/गाथा अलग: (श्लोक, शेष टीका)."""
    m = TIKA_MARK.search(body)
    if not m: return '', body
    pre = body[:m.start()]
    ends = list(VEND.finditer(pre))
    if not ends: return '', body
    ve = ends[-1].end()
    seg = pre[:ve]
    intro = ''
    b = re.search(r'—\s*\n', seg[:220])
    if b:
        intro = seg[:b.end()].strip(); seg = seg[b.end():]
    verse = seg.strip()
    rest = (intro + ' ' if intro else '') + body[m.start():]
    return verse, rest.strip()

TAGP = re.compile(r'^\(P(\d+)\)\s*')
out_files = []
miss = []
for x in M:
    k = x['key']
    sp = f'src/s{k}.md'
    ap = f'addenda/s{k}.md'
    if not os.path.exists(ap):
        miss.append(k); continue
    src = open(sp, encoding='utf-8').read().split('\n', 1)[1]
    add = open(ap, encoding='utf-8').read()
    # भाग 6 के (Pn) टैग
    sec6 = re.search(r'^## 6\..*?$(.*?)(?=^## |\Z)', add, re.S | re.M)
    tika_tags = set(re.findall(r'^\(P(\d+)\)', sec6.group(1), re.M)) if sec6 else set()
    paras = [p for p in re.split(r'\n\s*\n', src) if p.strip()]
    mool, tika = [], []
    for p in paras:
        m = TAGP.match(p.strip())
        n = m.group(1) if m else None
        body = clean_mool(TAGP.sub('', p.strip()))
        if n in tika_tags:
            v, t = split_verse(body)
            if v: mool.append(v)
            tika.append(f'(T{n}) {t}')
        else:
            mool.append(body)
    title = add.split('\n', 1)[0].replace('शीर्षक:', '').strip()
    num = k // 10
    lines = [f"§{k} — {title}", ""]
    ref = [l for l in add.split('\n')[:4] if l.startswith('सन्दर्भ-संकेत:')]
    if ref: lines += [ref[0], '']
    lines += ['## 1. मूल पाठ', ''] + ['\n\n'.join(mool) if mool else '', '']
    if tika:
        lines += ['## 6. संस्कृत टीका (मूल)', ''] + ['\n\n'.join(tika), '']
    open(f'parts/s{k:05d}.md', 'w', encoding='utf-8').write('\n'.join(lines))
    # addenda: भाग 6 में (Pn) -> (Tn); शीर्षक/सन्दर्भ पंक्तियाँ parts में हैं, पर बिल्डर addenda से भी पढ़ता है -> रखें
    if sec6:
        a2 = add.replace(sec6.group(0), re.sub(r'^\(P(\d+)\)', r'(T\1)', sec6.group(0), flags=re.M))
    else:
        a2 = add
    open(f'addenda_b/s{k}.md', 'w', encoding='utf-8').write(a2)
    out_files.append(k)
print('parts बने:', len(out_files), 'बिना addenda:', miss)
