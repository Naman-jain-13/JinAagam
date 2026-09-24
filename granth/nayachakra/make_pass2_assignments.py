#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Split the 369 § into pass-2 agent assignments and write pass2_assignments.json.

    python make_pass2_assignments.py [per_agent]

§ numbers have gaps (a merged § covering गाथा 234-236 is §234, and there is no §235),
so each agent is handed an explicit list of § numbers, not a range to interpolate.
"""
import io, re, glob, json, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PER = int(sys.argv[1]) if len(sys.argv) > 1 else 14

secs = {}
for f in sorted(glob.glob('parts/batch*.md')):
    src = f.replace(os.sep, '/')
    for m in re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', io.open(f, encoding='utf-8').read(), re.M):
        secs[int(m.group(1))] = (src, m.group(2).strip())

ns = sorted(secs)
groups = [ns[i:i + PER] for i in range(0, len(ns), PER)]

out = []
for i, g in enumerate(groups, 1):
    out.append({
        'agent': i,
        'first': g[0],
        'last': g[-1],
        'count': len(g),
        'sections': g,
        'parts_files': sorted({secs[n][0] for n in g}),
        'footnote_files': sorted({secs[n][0].replace('parts/batch', 'footnotes/b').replace('_p', '_p')
                                  for n in g}),
    })

io.open('pass2_assignments.json', 'w', encoding='utf-8').write(
    json.dumps(out, ensure_ascii=False, indent=1))

print('total §: %d   agents: %d   per agent: %d' % (len(ns), len(out), PER))
for a in out:
    print('W%02d  §%d–§%d (%d)  %s' % (
        a['agent'], a['first'], a['last'], a['count'],
        ', '.join(x.split('/')[-1] for x in a['parts_files'])))
