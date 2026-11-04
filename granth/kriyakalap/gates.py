import re,glob,sys,json
sys.stdout.reconfigure(encoding='utf-8')
bad=[]
for f in sorted(glob.glob('addenda/s*.md')):
    t=open(f,encoding='utf-8').read()
    k=f.split('/')[-1][:-3]
    # 1 शीर्षक/सन्दर्भ lines
    ls=t.split('\n')
    if not ls[0].startswith('शीर्षक:'): bad.append((k,'no शीर्षक'))
    if not any(l.startswith('सन्दर्भ-संकेत:') for l in ls[:4]): bad.append((k,'no सन्दर्भ'))
    # 2 required headings
    heads=re.findall(r'^## (.+)$',t,re.M)
    for need in ['7.','8.','9.','10.']:
        if not any(h.startswith(need) for h in heads): bad.append((k,'missing part '+need))
    # 3 9-क tags
    m=re.search(r'^## 9-क.*?$(.*?)(?=^## |\Z)',t,re.S|re.M)
    if m:
        for b in re.findall(r'^- .*$',m.group(1),re.M):
            if '[आगम-सम्मत]' not in b and '[सुझाव]' not in b: bad.append((k,'9-क untagged: '+b[:60]))
    # 4 forbidden
    for p,label in [(r'स्कैन|एजेंट|बैच|पायलट|\bsrc\b','process'),(r'`','backtick'),(r'दिगम्बर|दिगंबर|श्वेताम्बर|श्वेतांबर|श्वेतपट|बीसपंथ|तेरापंथ','sect'),(r'पन्नालाल|माताजी','name')]:
        mm=re.search(p,t)
        if mm: bad.append((k,label+': '+t[max(0,mm.start()-25):mm.end()+25].replace('\n',' ')))
    # 5 part 6 vs src tags (only if src has tika paragraphs)
print(len(bad))
for b in bad: print(b)
