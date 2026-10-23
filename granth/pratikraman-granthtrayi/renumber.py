# -*- coding: utf-8 -*-
"""parts/b*.md के § को 1 से लगातार क्रमांक दीजिए (भीतरी §-सन्दर्भ सहित).  python renumber.py [--write]"""
import re,glob,sys,pathlib
HERE=pathlib.Path(__file__).resolve().parent
files=sorted(glob.glob(str(HERE/'parts'/'b*.md')))
TITLE=re.compile(r'(?m)^§\s*(\d+)\s*—')
old=[]
for f in files:
    old+= [int(x) for x in TITLE.findall(open(f,encoding='utf-8').read())]
mp={o:i+1 for i,o in enumerate(old)}
extra={1501:mp.get(1417)}      # हटाया गया दोहरा § → पहला रूप
def sub(m):
    o=int(m.group(2))
    n=mp.get(o) or extra.get(o)
    return m.group(1)+str(n) if n else m.group(0)
REF=re.compile(r'(§\s*)(\d+)')
print('§ कुल',len(old),'पुराना',old[0],'–',old[-1],'→ 1 –',len(old))
if '--write' in sys.argv:
    for f in files:
        t=open(f,encoding='utf-8',newline='').read()
        t2=REF.sub(sub,t)
        open(f,'w',encoding='utf-8',newline='').write(t2)
    print('लिखा')
