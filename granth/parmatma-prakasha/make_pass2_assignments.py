#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Split the § into pass-2 agent assignments and write pass2_assignments.json.

    python make_pass2_assignments.py [target_segments_per_agent]

Two things make this book different from a flat गाथा-sequence ग्रन्थ:

1. **Three independent दोहा sequences** share one key space (base 10000 = अधिकार 1, 20000 = अधिकार 2,
   30000 = योगसार). An assignment must never straddle a section boundary — the खण्ड an agent is writing
   in changes the register, and the अधिकार number appears in every § title it has to produce.

2. **टीका density varies about fourfold.** दोहा 1 alone carries 19 (Tn) segments; later दोहा carry 4 or 5.
   Pass 2's work is per *segment*, not per §, because every segment needs its own Hindi against the same
   tag. Splitting by § count would hand one agent 14 § of 70 segments and another 14 § of 200.

So assignments are balanced on **(Tn) segment count**, closed at section boundaries, and handed out as an
explicit list of § keys — keys have deliberate gaps (a merged § covering दोहा 19–21 is §10190, and
§10200/§10210 do not exist), so a range is not interpolable.
"""
import io, re, glob, json, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 90

SECTIONS = {1: 'परमात्मप्रकाश अधिकार 1', 2: 'परमात्मप्रकाश अधिकार 2', 3: 'योगसार'}


def sec_label(key):
    base, rest = key // 10000, key % 10000
    doha, star = rest // 10, rest % 10
    d = '%d%s' % (doha, '*%d' % star if star else '')
    return ('योगसार, दोहा %s' % d) if base == 3 else ('परमात्मप्रकाश %d.%s' % (base, d))


# ---- collect every § with its source file and its टीका segment count ----
secs = {}
for f in sorted(glob.glob('parts/batch*.md')):
    src = f.replace(os.sep, '/')
    text = io.open(f, encoding='utf-8').read()
    hits = list(re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', text, re.M))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.end():end]
        key = int(m.group(1))
        n = len(re.findall(r'^\s*\(T\d+\)', body, re.M))
        # योगसार has no टीका, so it has no (Tn) segments at all — balancing on segments alone would
        # sweep all 105 of its दोहा into a single agent. Its § still need अन्वय, अन्वयार्थ, the विस्तृत
        # व्याख्या, उदाहरण, तालिका and सन्दर्भ written, which is most of the work; only part 6's
        # translation is absent. Weight each at 5, a little under परमात्मप्रकाश's ~6-segment average.
        if key // 10000 == 3:
            n = 5
        secs[key] = {'file': src, 'title': m.group(2).strip(), 'segs': n}

if not secs:
    sys.exit('no § found in parts/ — run the extraction pass first')

# ---- pack into assignments, balanced on segments, never crossing a section ----
out = []
for base in sorted(SECTIONS):
    keys = sorted(k for k in secs if k // 10000 == base)
    if not keys:
        continue
    bucket, load = [], 0
    for k in keys:
        n = secs[k]['segs']
        # close the bucket before this § if adding it would overshoot more than leaving it out
        if bucket and load + n > TARGET and abs(load - TARGET) <= abs(load + n - TARGET):
            out.append((base, bucket, load))
            bucket, load = [], 0
        bucket.append(k)
        load += n
    if bucket:
        out.append((base, bucket, load))

assignments = []
for i, (base, g, load) in enumerate(out, 1):
    assignments.append({
        'agent': i,
        'section': SECTIONS[base],
        'first': g[0],
        'last': g[-1],
        'label_first': sec_label(g[0]),
        'label_last': sec_label(g[-1]),
        'count': len(g),
        'segments': load,
        'sections': g,
        'parts_files': sorted({secs[k]['file'] for k in g}),
        'footnote_files': sorted({secs[k]['file'].replace('parts/batch', 'footnotes/b') for k in g
                                  if os.path.exists(secs[k]['file'].replace('parts/batch', 'footnotes/b'))}),
    })

io.open('pass2_assignments.json', 'w', encoding='utf-8', newline='').write(
    json.dumps(assignments, ensure_ascii=False, indent=1))

tot_segs = sum(s['segs'] for s in secs.values())
print('total §: %d   टीका segments: %d   agents: %d   target %d segs/agent'
      % (len(secs), tot_segs, len(assignments), TARGET))
for a in assignments:
    print('W%02d  %-24s %s – %s   %2d §  %3d segs'
          % (a['agent'], a['section'], a['label_first'], a['label_last'], a['count'], a['segments']))
loads = [a['segments'] for a in assignments]
print('\nload spread: min %d, max %d, mean %d' % (min(loads), max(loads), sum(loads) // len(loads)))
