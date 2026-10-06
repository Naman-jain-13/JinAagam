#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Draft groups.json — the खण्ड headings — from the ग्रन्थ's own स्थल-colophons.

    python make_groups.py          # print a draft
    python make_groups.py --write  # write groups.json

श्री ब्रह्मदेव divides his own commentary and says so at every seam, closing each **स्थल** with a sentence
that names it and counts its दोहा. Those sentences, not an editor's guesses, are where this book's section
headings come from.

Method: take each CLOSING colophon (the opening ones cannot be harvested cleanly — the regex that finds them
also matches ordinary Hindi भावार्थ prose), read its count N and the दोहा it sits on, and place a heading at
दोहा − N + 1. The name is the descriptive compound the colophon itself uses.

The स्थल nest: a 41-दोहा महास्थल contains अन्तरस्थल of 5, 15, 8 and 13. Headings are emitted for the inner
divisions, which is the level that actually helps a reader navigate ~450 sections; the four top-level
divisions are added by hand because the text marks them differently.

**This writes a draft.** The extracted names are long Sanskrit compounds and want editing into readable
Hindi before they go in a book. Nothing here is final.
"""
import io, re, json, glob, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

NUMERALS = [
    ('एकाधिकचत्वारिंशत्', 41), ('एकचत्वारिंशत्', 41), ('एकत्रिंशत्', 31), ('एकोनविंशति', 19),
    ('नविंशति', 19), ('चतुर्दश', 14), ('सप्तदशक', 17), ('पञ्चदश', 15), ('त्रयोदश', 13),
    ('अष्टादश', 18), ('द्वादश', 12), ('एकादश', 11), ('षोडश', 16), ('विंशति', 20), ('दशक', 10),
    ('नवक', 9), ('अष्टक', 8), ('ष्टक', 8), ('ष्ठक', 8), ('सप्तक', 7), ('षट्क', 6), ('षटक', 6),
    ('पञ्चक', 5), ('चतुष्टय', 4), ('सूत्रत्रय', 3), ('त्रिक', 3), ('द्वय', 2), ('एकं', 1),
]
_MATRA = {'ए': ['े', 'ै'], 'अ': ['ा'], 'ओ': ['ो']}
NUMERALS = NUMERALS + [(m + w[1:], n) for w, n in NUMERALS for m in _MATRA.get(w[0], [])]

COLOPHON = re.compile(r'[^।"]*(?:स्थल|महाधिकार)[^।"]*(?:समाप्तम्|समाप्तः|गतम्|गतः)\s*(?:॥\s*\d+\s*॥)?\s*।')

# The four divisions the text marks differently from its स्थल, keyed by where each begins.
TOP = {
    10010: 'परमात्मप्रकाश — प्रथम महाधिकार : त्रिविध आत्मा का प्रतिपादन',
    20010: 'परमात्मप्रकाश — द्वितीय महाधिकार : मोक्ष, मोक्षफल और मोक्षमार्ग',
    21080: 'परमात्मप्रकाश — चूलिका : एक सौ सात दोहों का उपसंहार-प्रकरण',
    30010: 'योगसार',
}


def value(text):
    best = None
    for word, n in NUMERALS:
        i = text.rfind(word)
        if i < 0:
            continue
        end, length = i + len(word), len(word)
        if best is None or (end, length) > (best[0], best[1]):
            best = (end, length, n)
    return best[2] if best else None


def name_of(s):
    """The descriptive compound a colophon uses for its own स्थल."""
    m = re.search(r'(?:मध्ये|एवं|इति|तत्रैव)\s*(.*?)(?:मुख्यत्वेन|मुख्यतया|व्याख्यानस्थल|स्थल)', s)
    n = (m.group(1) if m else s).strip()
    n = re.sub(r'^(?:एवं|इति|तदनन्तरं|पुनः)\s*', '', n)
    n = re.sub(r'(?:प्रथम|द्वितीय|तृतीय|चतुर्थ|पञ्चम|षष्ठ|सप्तम)म?(?:महाधिकार|अन्तरस्थल)\S*', '', n)
    return ' '.join(n.split())[:70]


rows = []
for f in sorted(glob.glob('parts/batch*.md')):
    t = io.open(f, encoding='utf-8').read()
    hits = list(re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', t, re.M))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(t)
        for c in COLOPHON.finditer(t[m.end():end]):
            s = ' '.join(c.group().split())
            if len(s) >= 30:
                rows.append((int(m.group(1)), s))
rows.sort()

groups = dict(TOP)
drafted = []
for key, s in rows:
    n = value(s)
    if not n:
        continue
    base, doha = key // 10000, (key % 10000) // 10
    lo = doha - n + 1
    if lo < 1:
        continue
    start = base * 10000 + lo * 10
    if start in groups:
        continue
    groups[start] = '[स्थल] ' + name_of(s)
    drafted.append((start, n, lo, doha, groups[start]))

print('top-level divisions : %d' % len(TOP))
print('स्थल headings drafted: %d\n' % len(drafted))
for start, n, lo, hi, label in sorted(drafted):
    print('  §%-6d दोहा %3d–%-3d (%2d)  %s' % (start, lo, hi, n, label))

if '--write' in sys.argv:
    io.open('groups.json', 'w', encoding='utf-8', newline='').write(
        json.dumps({str(k): v for k, v in sorted(groups.items())}, ensure_ascii=False, indent=1))
    print('\nwritten: groups.json  (%d headings) — EDIT THE NAMES BEFORE BUILDING' % len(groups))
