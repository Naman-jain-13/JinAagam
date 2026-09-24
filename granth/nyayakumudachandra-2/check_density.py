# हर मुद्रित पृष्ठ के लिए मूल पाठ की मात्रा नापता है। भीतर का "(पृष्ठ N)" चिह्न न हो तो § के
# शीर्षक का "मुद्रित पृष्ठ N" प्रयोग करता है। घना मुद्रित पृष्ठ ~1200-1800 अक्षर देता है।
import re,glob,sys
sys.stdout.reconfigure(encoding='utf-8')
from collections import defaultdict
chars=defaultdict(float); owner=defaultdict(set)
for f in sorted(glob.glob('parts/batch*.md')):
    t=open(f,encoding='utf-8').read()
    for sec in re.split(r'\n(?=§\d)', t):
        if not sec.startswith('§'): continue
        head=sec.split('\n')[0]
        hm=re.search(r'मुद्रित पृष्ठ\s*([0-9]+)(?:\s*[-–]\s*([0-9]+))?', head)
        hp=list(range(int(hm.group(1)), (int(hm.group(2)) if hm.group(2) else int(hm.group(1)))+1)) if hm else None
        m=re.search(r'## 1\. मूल पाठ\n(.*?)\n## 2\.', sec, re.S)
        if not m: continue
        cur=None
        for line in m.group(1).split('\n'):
            pm=re.match(r'\s*\(पृष्ठ\s*([0-9]+)(?:\s*[-–से]+\s*([0-9]+))?[^)]*\)\s*(.*)$', line)
            if pm:
                a=int(pm.group(1)); b=int(pm.group(2)) if pm.group(2) else a
                cur=list(range(a,b+1)); line=pm.group(3)
            pages=cur or hp
            if pages and line.strip():
                share=len(re.sub(r'\[[^\]]*\]','',line))/len(pages)
                for p in pages: chars[p]+=share; owner[p].add(head.split('—')[0].strip())
mx=max(chars) if chars else 0
low=[(p,int(chars.get(p,0))) for p in range(1,mx+1) if chars.get(p,0)<600]
print(f'पृष्ठ 1–{mx} | औसत अक्षर/पृष्ठ: {int(sum(chars.values())/len(chars))}')
print(f'सन्दिग्ध पृष्ठ (<600 अक्षर): {len(low)}')
for p,c in low: print(f'   मु.पृ. {p}: {c} अक्षर  {sorted(owner.get(p,[]))[:3]}')
