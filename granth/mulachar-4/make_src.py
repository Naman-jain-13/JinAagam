# -*- coding: utf-8 -*-
"""Build src/s<key>.md from parts/: only § ref, part 1 (Prakrit), part 6 (Sanskrit) and part 11 (variants). No title, no Hindi."""
import re, glob, os, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
os.makedirs('src', exist_ok=True)
n = 0
for f in sorted(glob.glob('parts/*.md')):
    t = open(f, encoding='utf-8').read().replace('\r\n', '\n')
    for m in re.finditer(r'(?ms)^§\s*(\d+)\s*—\s*(.*?)\n(.*?)(?=^---\s*$|^§\s*\d+\s*—|\Z)', t):
        key, title, body = m.group(1), m.group(2), m.group(3)
        ref = re.search(r'\((अधिकार[^)]*)\)\s*$', title).group(1)
        parts, cur = {}, None
        for l in body.split('\n'):
            h = re.match(r'^##\s*(\d+)\.', l)
            if h: cur = h.group(1); parts[cur] = []
            if cur: parts[cur].append(l)
        out = '§%s — (%s)\n\n' % (key, ref) + '\n'.join(parts['1']).rstrip() + '\n\n' + '\n'.join(parts['6']).rstrip() + '\n'
        if '11' in parts: out += '\n' + '\n'.join(parts['11']).rstrip() + '\n'
        open('src/s%s.md' % key, 'w', encoding='utf-8').write(out); n += 1
print(n, 'source files written')
