# -*- coding: utf-8 -*-
"""Pass-1 gate for the मूलगुणाधिकार: gatha continuity, one part 1/5/6 per §, tag continuity, Devanagari closers."""
import re, glob, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
files = sorted(glob.glob('parts/*.md'))
secs = {}
for f in files:
    cur = None
    for ln in open(f, encoding='utf-8'):
        m = re.match(r'^§\s*(\d+)\s*[—–-]\s*(.*)', ln)
        if m: cur = int(m.group(1)); secs[cur] = {'file': f, 'title': m.group(2), 'body': []}; continue
        if cur: secs[cur]['body'].append(ln)
prob = []
keys = sorted(secs)
print('§ count', len(keys), 'first', keys[:1], 'last', keys[-1:])
# gatha coverage from titles
covered = set()
for k in keys:
    t = secs[k]['title']
    m = re.search(r'गाथा\s*(\d+)(?:\s*[–-]\s*(\d+))?', t)
    if not m: prob.append('§%d: no गाथा in title' % k); continue
    a = int(m.group(1)); b = int(m.group(2) or a)
    if a*10 != k: prob.append('§%d: key != गाथा %d x10' % (k, a))
    covered |= set(range(a, b+1))
for g in range(1, 37):
    if g not in covered: prob.append('गाथा %d missing' % g)
for k in keys:
    body = ''.join(secs[k]['body'])
    for h in ['## 1.', '## 5.', '## 6.']:
        if h not in body: prob.append('§%d lacks %s' % (k, h))
    tags = [int(x) for x in re.findall(r'^\(T(\d+)\)', body, re.M)]
    if tags != list(range(1, len(tags)+1)): prob.append('§%d tags not 1..n: %s' % (k, tags[:12]))
    if '**भावार्थ:**' in body: prob.append('§%d has bold भावार्थ:' % k)
    for w in ['बैच', 'बीसपंथ', 'तेरापंथ', 'scan', 'उपयोगकर्ता']:
        if w in body: prob.append('§%d contains %s' % (k, w))
    print(k, '| tags', len(tags), '| chars', len(body), '|', secs[k]['title'][:60])
print('\nPROBLEMS' if prob else '\nOK'); [print(' ', p) for p in prob]
