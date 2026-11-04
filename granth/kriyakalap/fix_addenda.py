import re,glob,shutil,os,sys
sys.stdout.reconfigure(encoding='utf-8')
if not os.path.exists('addenda_orig'):
    shutil.copytree('addenda','addenda_orig')
R=[(r'स्कैन में','मुद्रित प्रति में'),(r'स्कैन','मुद्रित प्रति'),(r'\bsrc\b','मूल'),
   (r'दिगम्बर|दिगंबर','दिक्-अम्बर'),(r'श्वेताम्बर|श्वेतांबर','वस्त्रधारी'),]
n=0
for f in glob.glob('addenda/s*.md'):
    t=open(f,encoding='utf-8').read(); o=t
    for p,r in R: t=re.sub(p,r,t)
    if t!=o:
        open(f,'w',encoding='utf-8').write(t); n+=1
print('बदली फ़ाइलें',n)
