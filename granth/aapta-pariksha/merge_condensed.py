# भाग 6 (सन्दर्भ एवं पाद-टिप्पणी) को addenda/condensed/*.md के संक्षिप्त रूप से बदलता है।
# पूर्ण विस्तृत रूप addenda/bhag6_vistrit_sangrah.md में सुरक्षित है। भाग 1–5 अछूते रहते हैं।
# उपयोग: python merge_condensed.py [--dry]
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DRY = '--dry' in sys.argv

cond = {}
for f in sorted(glob.glob(os.path.join(HERE, 'addenda', 'condensed', '*.md'))):
    cur = None
    for line in open(f, encoding='utf-8').read().split('\n'):
        m = re.match(r'^##\s*§\s*(\d+)\s*$', line.strip())
        if m:
            cur = int(m.group(1)); cond[cur] = []; continue
        if cur is not None and line.strip().startswith('- '):
            cond[cur].append(line.strip())

HDR = re.compile(r'^§\s*(\d+)\s*[—–-]')
P6 = re.compile(r'^##\s*6\.')
done, missing, bad = [], [], []
for f in sorted(glob.glob(os.path.join(HERE, 'parts', '*.md'))):
    lines = open(f, encoding='utf-8').read().split('\n')
    out, i, num, changed = [], 0, None, False
    while i < len(lines):
        t = lines[i]
        m = HDR.match(t.strip())
        if m: num = int(m.group(1))
        if P6.match(t.strip()) and num is not None:
            # skip old body up to the next ## / --- / § header
            j = i + 1
            while j < len(lines) and not (lines[j].strip().startswith('## ') or lines[j].strip() == '---'
                                           or HDR.match(lines[j].strip())):
                j += 1
            if num in cond and 1 <= len(cond[num]) <= 3:
                out.append('## 6. सन्दर्भ एवं पाद-टिप्पणी')
                out.extend(cond[num]); out.append('')
                done.append(num); changed = True
            else:
                (bad if num in cond else missing).append(num)
                out.extend(lines[i:j])
            i = j; continue
        out.append(t); i += 1
    if changed and not DRY:
        open(f, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))

print('बदले गए §:', len(done))
print('संक्षिप्त रूप नहीं मिला (यथावत्):', missing)
print('bullet-संख्या 1–3 से बाहर (यथावत्):', bad, [len(cond[n]) for n in bad])
