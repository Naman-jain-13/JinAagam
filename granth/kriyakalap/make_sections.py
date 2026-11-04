# चेतावनी: src/ जम चुका है (addenda की कुंजियाँ इसी पर टिकी हैं); इसे दोबारा न चलाइए।
"""मूल-पाठ (mool/slice_k0N_*.md) को § में बाँटता है -> src/sNNNN.md + sections.json
नियम: पृष्ठ-चिह्न/पृष्ठ-शीर्ष/पृष्ठ-तल हटते हैं; शीर्ष ([शीर्ष: …]) पर नया § आरम्भ; अनुच्छेद-सीमा पर ही कटाव;
कटे वाक्य (⟶ … ⟵) जुड़ते हैं; लक्ष्य-आकार ~TARGET अक्षर, अधिकतम MAXC।
"""
import re, glob, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
TARGET, MAXC = 700, 1300
CH = {'1': 'वन्दनाध्याय', '2': 'प्रतिक्रमणाध्याय', '3': 'भक्त्यध्याय', '4': 'नैमित्तिकक्रियाप्रयोगविधि'}

def load(ch):
    out = []  # (scan, mudrit, para)
    for f in sorted(glob.glob(f'mool/slice_k0{ch}_*.md')):
        scan = mud = None
        buf = []
        for l in open(f, encoding='utf-8'):
            l = l.rstrip('\n'); l0 = l
            m = re.match(r'<!--PDF (\d+) \| मुद्रित ([^ >]+)', l)
            if m:
                scan, mud = int(m.group(1)), m.group(2)
                continue
            if re.match(r'\[(पृष्ठ-शीर्ष|पृष्ठ-तल)', l):
                continue
            if re.fullmatch(r'\[—[^\]]*अंश[^\]]*\]', l.strip()):
                continue
            l = re.sub(r'\[—[^\]]*अंश[^\]]*\]', '', l).strip() if '[—' in l else l
            if not l.strip() and l0.strip(): continue
            l = l.replace('[सम्पादकीय संस्कृत]', '').strip() if '[सम्पादकीय संस्कृत]' in l else l
            if re.fullmatch(r'\[शीर्ष: *क्रिया-?कलापे?[ —।\-]*\]', l.strip()):
                continue
            out.append((scan, mud, l))
    # ch4 की पहली फ़ाइल-सीमा आदि: अध्याय के बाहर के स्कैन (ch3 फ़ाइल में 321+) छाँटिए
    return out

def paras(lines):
    ps, cur, meta = [], [], None
    for scan, mud, l in lines:
        if not l.strip():
            if cur: ps.append((meta, '\n'.join(cur))); cur = []
            continue
        if not cur: meta = (scan, mud)
        cur.append(l)
    if cur: ps.append((meta, '\n'.join(cur)))
    # ⟶ ... ⟵ जोड़िए
    merged = []
    for meta, p in ps:
        if merged and p.lstrip().startswith('⟵') and merged[-1][1].rstrip().endswith('⟶'):
            prev = merged[-1]
            merged[-1] = (prev[0], prev[1].rstrip()[:-1].rstrip() + ' ' + p.lstrip()[1:].lstrip(), )
        else:
            merged.append((meta, p))
    out = []
    for meta, p in merged:
        if len(p) <= MAXC: out.append((meta, p)); continue
        parts, cur = [], ''
        for piece in re.split(r'(?<=[।॥])\s+', p):
            if cur and len(cur) + len(piece) > TARGET: parts.append(cur); cur = ''
            cur += (' ' if cur else '') + piece
        if cur: parts.append(cur)
        out += [(meta, x) for x in parts]
    return out

def sections(ps):
    secs, cur, size, first = [], [], 0, None
    def flush():
        nonlocal cur, size, first
        if cur: secs.append((first, cur)); cur, size, first = [], 0, None
    for meta, p in ps:
        head = p.strip().startswith('[शीर्ष:')
        if head and cur and size >= 120: flush()
        if cur and size + len(p) > MAXC: flush()
        if first is None: first = meta
        cur.append(p); size += len(p)
        if size >= TARGET and not head: flush()
    flush()
    return secs

def main():
    os.makedirs('src', exist_ok=True)
    meta, n = [], 0
    for ch in '1234':
        lines = load(ch)
        if ch == '3': lines = [x for x in lines if x[0] is None or x[0] <= 320]
        if ch == '4':
            # slice_k03_s317-324 के स्कैन 321–324 भी अध्याय 4 के हैं
            extra = [x for x in load('3') if x[0] and x[0] >= 321]
            lines = extra + lines
        for first, body in sections(paras(lines)):
            n += 1
            key = n * 10
            tagged = [f'(P{i}) {b}' for i, b in enumerate(body, 1)]
            txt = f'<!--ch {ch} | स्कैन {first[0]} | मुद्रित {first[1]}-->\n' + '\n\n'.join(tagged) + '\n'
            open(f'src/s{key}.md', 'w', encoding='utf-8').write(txt)
            meta.append({'key': key, 'ch': ch, 'scan': first[0], 'mudrit': first[1], 'chars': sum(map(len, body))})
    json.dump(meta, open('sections.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    from collections import Counter
    c = Counter(m['ch'] for m in meta)
    print(n, dict(c), 'max', max(m['chars'] for m in meta))

main()
