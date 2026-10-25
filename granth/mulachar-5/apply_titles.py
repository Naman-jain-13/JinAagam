# -*- coding: utf-8 -*-
"""Copy each addendum's first line `शीर्षक: …` into the § title in parts/ (pass 1 left only `गाथा N`)."""
import re, glob, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
titles = {}
for f in glob.glob('addenda/s*.md'):
    k = re.search(r's(\d+)\.md', f).group(1)
    first = open(f, encoding='utf-8').readline().strip()
    m = re.match(r'^शीर्षक:\s*(.+)$', first)
    if m: titles[k] = m.group(1).strip()
n = 0
for f in sorted(glob.glob('parts/*.md')):
    t = open(f, encoding='utf-8').read(); crlf = '\r\n' in t; t = t.replace('\r\n', '\n')
    def sub(m):
        global n
        k = m.group(1)
        if k in titles:
            n += 1
            return '§%s — %s %s' % (k, titles[k], m.group(3))
        return m.group(0)
    t2 = re.sub(r'(?m)^§\s*(\d+)\s*—\s*(.*?)\s*(\(अधिकार[^)]*\))\s*$', sub, t)
    if t2 != t: open(f, 'w', encoding='utf-8', newline='').write(t2.replace('\n', '\r\n') if crlf else t2)
print(n, 'titles applied;', len(titles), 'found; missing:', [os.path.basename(x) for x in []])
