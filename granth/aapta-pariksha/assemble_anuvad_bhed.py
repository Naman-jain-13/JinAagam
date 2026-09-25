# anuvad_bhed/aNN.md → backmatter/02b_anuvad_bhed.md (अनुवाद-भेद सूची; postprocess_docx.py इसे 7 pt में छापता है)
# उपयोग: python assemble_anuvad_bhed.py
import glob, io, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS = {int(k): v for k, v in json.load(io.open(os.path.join(HERE, 'groups.json'), encoding='utf-8')).items()}
KOTI = ['अर्थ-भेद', 'पाठ-आधार', 'छूट', 'मुद्रण-दोष', 'प्रस्तुत-संशोधन']

entries, checked = [], set()
for f in sorted(glob.glob(os.path.join(HERE, 'anuvad_bhed', 'a[0-9][0-9].md'))):
    txt = io.open(f, encoding='utf-8').read().split('\n## मूल-पाठ सूचना')[0]
    m = re.search(r'जाँचे गए § (\d+)\s*[–-]\s*(\d+)', txt)
    if m: checked.update(range(int(m.group(1)), int(m.group(2)) + 1))
    for blk in re.split(r'\n(?=### § )', txt):
        h = re.match(r'### § (\d+)\s*·\s*मु॰\s*पृ॰\s*([\d–-]+)', blk)
        if not h: continue
        sec, pg = int(h.group(1)), h.group(2)
        for item in re.split(r'\n\s*\n(?=- मूल:)', blk):
            d = dict(re.findall(r'^- (मूल|मुद्रित|प्रस्तुत|कोटि|टिप्पणी):\s*(.*)$', item, re.M))
            if 'कोटि' in d and 'मूल' in d:
                entries.append((sec, pg, d))

cell = lambda s: (s or '—').replace('|', '/').strip()
out = ['# अनुवाद-भेद सूची (मुद्रित एवं प्रस्तुत हिन्दी अनुवाद)', '',
       'इस व्याख्या का हिन्दी अनुवाद केवल मूल संस्कृत पाठ से, स्वतन्त्र रूप में किया गया है। अनुवाद पूर्ण होने के '
       'पश्चात् उसका मिलान आधार-संस्करण में प्रकाशित हिन्दी अनुवाद (पं. दरबारीलाल जैन कोठिया) से किया गया। यह सूची '
       'केवल उन स्थलों की है जहाँ दोनों अनुवादों में **अर्थ का** भेद है — शब्द-चयन, शैली अथवा विस्तार का भेद इसमें '
       'नहीं लिया गया। प्रत्येक स्थल पर मूल अंश, दोनों अनुवादों के सम्बद्ध अंश (यथावत्) तथा मूल के आधार पर संक्षिप्त '
       'टिप्पणी दी गई है। मुद्रित अनुवाद और उसके विद्वान् अनुवादक के प्रति पूर्ण आदर के साथ यह तुलना केवल अध्येता की '
       'सुविधा हेतु प्रस्तुत है।', '',
       '**कोटियाँ —** *अर्थ-भेद:* किसी पद/वाक्य का अर्थ भिन्न समझा गया · *पाठ-आधार:* दोनों ने भिन्न पाठ के आधार पर '
       'अनुवाद किया · *छूट:* मूल का कोई अर्थवान् अंश एक अनुवाद में नहीं आया · *मुद्रण-दोष:* मुद्रित अनुवाद में अर्थ '
       'बदलने वाला मुद्रण-भेद · *प्रस्तुत-संशोधन:* मुद्रित अनुवाद मूल के अधिक अनुकूल पाया गया और प्रस्तुत अनुवाद '
       'उसके अनुसार सुधारा गया।', '']
c = Counter(d['कोटि'].strip() for _, _, d in entries)
out += ['**सारांश —** मिलान किए गए अनुच्छेद: %d · भेद-स्थल: %d (%s)' % (
    len(checked), len(entries), ', '.join('%s %d' % (k, c[k]) for k in KOTI if c[k])), '']

head = ['| § (मु॰ पृ॰) | मूल अंश | मुद्रित अनुवाद | प्रस्तुत अनुवाद | कोटि एवं टिप्पणी |', '|---|---|---|---|---|']
starts = sorted(GROUPS)
cur = None
for sec, pg, d in sorted(entries, key=lambda e: e[0]):
    g = max(s for s in starts if s <= sec)
    if g != cur:
        cur = g; out += ['', '## ' + GROUPS[g].strip('[] ').strip(), ''] + head
    out.append('| %d (%s) | %s | %s | %s | **%s** — %s |' % (
        sec, pg, cell(d.get('मूल')), cell(d.get('मुद्रित')), cell(d.get('प्रस्तुत')),
        cell(d.get('कोटि')), cell(d.get('टिप्पणी'))))
io.open(os.path.join(HERE, 'backmatter', '02b_anuvad_bhed.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('entries', len(entries), dict(c), '| checked §', len(checked))
