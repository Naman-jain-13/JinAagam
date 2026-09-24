import re,glob,sys
sys.stdout.reconfigure(encoding='utf-8')
files=sorted(glob.glob('parts/batch*.md'))
def mool_blocks(f):
    t=open(f,encoding='utf-8').read()
    return [m.group(1).strip() for m in re.finditer(r'## 1\. मूल पाठ\n(.*?)\n## 2\.', t, re.S)]
prev=None
for f in files:
    b=mool_blocks(f)
    if not b: print(f,'— कोई मूल खण्ड नहीं'); continue
    first=re.sub(r'^\(पृष्ठ[^)]*\)\s*','',b[0]).strip()
    if prev:
        pt=' '.join(prev[1].split())[-90:]
        ft=' '.join(first.split())[:90]
        # duplicate check: does the next file's opening repeat the tail of the previous?
        norm=lambda w: w.replace('ं','').replace('म्','').replace('।','').replace(';','').replace(',','')
        pw=[norm(w) for w in ' '.join(prev[1].split()).split()]
        fw=[norm(w) for w in ' '.join(first.split()).split()]
        dup=''
        for n in range(min(12,len(pw),len(fw)),2,-1):
            if pw[-n:]==fw[:n]: dup=f'  *** दोहराव: अन्तिम {n} शब्द दोनों में ***'; break
        print(f'\n{prev[0]}  →  {f}{dup}')
        print(f'   अन्त : …{pt}')
        print(f'   आरम्भ: {ft}…')
    prev=(f,b[-1])
print(f'\nकुल फ़ाइलें: {len(files)} | कुल §: {sum(len(mool_blocks(f)) for f in files)}')
