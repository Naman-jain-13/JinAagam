# -*- coding: utf-8 -*-
"""parts/*.md की जाँच (चरण 2 के बाद)।  python check_parts.py [फ़ाइलें…]"""
import sys,re,glob,pathlib,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
HERE=pathlib.Path(__file__).resolve().parent
files=[pathlib.Path(a) for a in sys.argv[1:]] or sorted((HERE/'parts').glob('*.md'))
SECT=['दिगम्बर','श्वेताम्बर','बीसपंथ','तेरापंथ']
PROC=['बैच','एजेंट','स्कैन','स्लाइस','परास','pdf','PDF','फ़ाइल']
NAMES=['गौतमस्वामी','गौतम स्वामी','प्रभाचन्द्र','कुन्दकुन्द','अकलङ्क','समन्तभद्र','विद्यानन्द','वट्टकेर','माणिक्यनन्दि']
REQ=[r'^## 1\.',r'^## 4\.',r'^## 5\.',r'^## 6\.',r'^## 7\.',r'^## 8\.']
bad=0;secs=0
for f in files:
    t=f.read_text(encoding='utf-8')
    blocks=re.split(r'(?m)^(?=§\s*\d+\s*—)',t)
    for b in blocks:
        m=re.match(r'§\s*(\d+)\s*—',b)
        if not m: continue
        secs+=1;n=m.group(1);p=[]
        lines=b.split('\n')
        if not any(l.startswith('सन्दर्भ-संकेत:') for l in lines[:4]): p.append('सन्दर्भ-संकेत पहली पंक्ति में नहीं')
        for r in REQ:
            if not re.search(r,b,re.M): p.append('heading गायब: '+r)
        if '`' in b: p.append('बैकटिक')
        for w in SECT:
            if w in b: p.append('सम्प्रदाय-नाम '+w)
        for w in PROC:
            if w in b: p.append('प्रक्रिया-शब्द '+w)
        if 'श्री श्री' in b: p.append('श्री श्री')
        for w in NAMES:
            for mm in re.finditer(w,b):
                pre=b[max(0,mm.start()-8):mm.start()]
                if 'श्री' not in pre and 'श्रीमद्' not in pre and 'आचार्य' not in pre:
                    p.append('बिना श्री: '+w); break
        m8=re.search(r'(?m)^## 8\..*?\n(.*)$',b,re.S)
        if m8:
            bl=[l for l in m8.group(1).split('\n') if l.strip().startswith('-')]
            if len(bl)>4: p.append('भाग 8 में %d बिन्दु'%len(bl))
        if p: bad+=1; print('✗ §%s (%s): %s'%(n,f.name,'; '.join(p)))
print('§ जाँचे %d; खटके %d'%(secs,bad))
