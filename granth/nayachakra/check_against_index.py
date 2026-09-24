#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cross-check every § in parts/ against the ग्रन्थ's own गाथा index (परिशिष्ट 4).

    python check_against_index.py

`gatha_index.md` holds the index's `गाथा -> आद्य-पद` (opening words), transcribed from
img/p0310–p0315. The § number in parts/ IS the गाथा number, so for each § we ask: do the
index's opening words for that number name the same verse the § actually contains?

WHAT THIS IS FOR — and what it is not for.

A misread गाथा NUMBER is invisible to check_coverage.py: the § sequence still looks
contiguous while pointing at the wrong verse. Only an independent witness catches that, and
the index is the one the book itself provides. So this check asks one question — "is §N the
verse the index calls N?" — and answers it by comparing CONSONANT SKELETONS of the first few
syllables.

It deliberately does NOT adjudicate spelling. The first version compared the words literally
and produced 111 "disagreements" out of 300, nearly all of them noise in the *index*
transcription rather than errors in the body (`तण्णं` for `तच्चं`, `देहामार` for `देहायार`,
`एदेहि` for `ऐदेहिं`, and सandhi splits like `अगुरुलहुगा अणंता` against `अगुरुलहुगाणंता`).
That is unsurprising: the index is itself a stamped scan, and one agent read ~420 tiny
entries across six dense pages, where each batch agent read eight pages. Using the noisier
copy to adjudicate the careful one is backwards. Word-level accuracy belongs to the per-batch
reading and to targeted lookups against the index IMAGE, which is how it has actually paid off.

The index transcription's own error rate is visible in its totals: 27 गाथा numbers absent and
19 numbers carrying two different openings — a signature of misread digits (342 read as 242,
326 as 226, 378 as 278).
"""
import io, re, sys, glob, os, unicodedata

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Every matra, anusvara, visarga, nukta and virama — dropped.
MARKS = set('ािीुूृॄॅॆेै'
            'ॉॊोौ्ँंः़')
# Independent vowels — also dropped, so sandhi at a word join cannot cause a false alarm.
VOWELS = set('अआइईउऊऋऌएऐओऔ')


def consonants(t):
    t = unicodedata.normalize('NFC', t)
    return ''.join(ch for ch in t
                   if ('क' <= ch <= 'ह' or 'क़' <= ch <= 'य़')
                   and ch not in MARKS and ch not in VOWELS)


SIG = 6   # first six consonants is enough to identify a verse, loose enough to ignore spelling


def load_index():
    if not os.path.exists('gatha_index.md'):
        print('gatha_index.md not found — run the index transcription first')
        sys.exit(1)
    idx, dupes = {}, {}
    for line in io.open('gatha_index.md', encoding='utf-8'):
        m = re.match(r'^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|', line)
        if not m:
            continue
        n, pada = int(m.group(1)), m.group(2).strip()
        if 'अस्पष्ट' in pada:
            continue
        if n in idx and consonants(idx[n])[:SIG] != consonants(pada)[:SIG]:
            dupes.setdefault(n, [idx[n]]).append(pada)
        idx[n] = pada
    return idx, dupes


def load_sections():
    secs = {}
    for f in sorted(glob.glob('parts/batch*.md')):
        text = io.open(f, encoding='utf-8').read()
        hits = list(re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', text, re.M))
        for i, mm in enumerate(hits):
            end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
            body = text[mm.end():end]
            mool = re.search(r'##\s*1\.[^\n]*\n(.*?)(?=\n##\s|\Z)', body, re.S)
            secs[int(mm.group(1))] = (os.path.basename(f), mool.group(1) if mool else '')
    return secs


index, dupes = load_index()
secs = load_sections()

ok = absent = 0
problems = []
for n in sorted(secs):
    f, mool = secs[n]
    if n not in index:
        absent += 1
        continue
    sig = consonants(index[n])[:SIG]
    if sig and sig in consonants(mool):
        ok += 1
    else:
        problems.append((n, f, index[n], ' '.join(mool.split())[:60]))

print('§ cross-checked against the index : %d' % (ok + len(problems)))
print('  verse identity confirmed         : %d' % ok)
print('  POSSIBLE NUMBER MISMATCH         : %d' % len(problems))
print('  § the printed index omits        : %d' % absent)
print('  index numbers with two openings  : %d  (index-side digit misreads)' % len(dupes))

if problems:
    print('\nCheck these against the page — the index may be the wrong witness:')
    for n, f, pada, got in problems:
        print('  §%-4d %-24s index: %-30s parts: %s' % (n, f, pada, got))
sys.exit(1 if problems else 0)
