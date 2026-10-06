#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read the ग्रन्थ's own arithmetic back to us.

    python check_colophons.py

श्री ब्रह्मदेव closes each **स्थल** with a sentence that names it and **states how many दोहा it held**:

    एवं … दशकेन मोक्षस्वरूपनिरूपणस्थलं समाप्तम् ।            (10)
    एवं … भेदभावनास्थलसूत्रनवकं गतम् ।                        (9)
    इत्येकत्रिंशत्सूत्रैश्चूलिकास्थलं गतम् ।                    (31)
    एवं … चतुर्दशसूत्रैः स्थलं समाप्तम् ।                       (14)

That is the author stating, in his own words, how many दोहा each division holds — a free check on the
extraction, and on the खण्ड structure that `groups.json` will be built from.

**The स्थल nest.** A महास्थल of 41 दोहा contains अन्तरस्थल of 5 and 15, so counts legitimately overlap and
a colophon's स्थल does *not* simply begin where the previous one ended. This script therefore makes no
assumption about where a स्थल started: for each colophon it prints the दोहा range the stated count
**implies**, ending at the दोहा the colophon is attached to. Matching nested ranges up is then a reading
job, not a guess — and a count that implies a range crossing an अधिकार boundary, or starting before दोहा 1,
is a real problem worth chasing.

Nothing is corrected here. Where this and the text disagree, read the page.
"""
import io, re, glob, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Number words as these colophons spell them, longest first so 'सप्तदशक' is not eaten by 'सप्तक'.
NUMERALS = [
    ('एकाधिकचत्वारिंशत्', 41), ('एकचत्वारिंशत्', 41), ('एकत्रिंशत्', 31), ('एकोनविंशति', 19), ('नविंशति', 19), ('चतुर्दश', 14),
    ('सप्तदशक', 17), ('पञ्चदश', 15), ('त्रयोदश', 13), ('अष्टादश', 18), ('द्वादश', 12), ('एकादश', 11),
    ('षोडश', 16), ('विंशति', 20), ('दशक', 10), ('नवक', 9), ('अष्टक', 8), ('ष्टक', 8), ('सप्तक', 7),
    ('षट्क', 6), ('षटक', 6), ('पञ्चक', 5), ('चतुष्टय', 4), ('सूत्रत्रय', 3), ('त्रिक', 3),
    ('द्वय', 2), ('एकं', 1),
]
# Sandhi swallows a numeral's initial vowel when it follows another word inside the compound:
# सूत्रम् + एकं -> सूत्रम‌ेकं, स्वरूप + अष्टकं -> स्वरूपाष्टकं, इति + एकत्रिंशत् -> इत्यekत्रिंशत्.
# So the bare spelling never matches. Add the matra form of every vowel-initial numeral.
# अ + ए also vrddhies to ऐ ('मुख्यत्वेन + एकचत्वारिंशत्' -> 'मुख्यत्वेनैकचत्वारिंशत्'), so a
# vowel-initial numeral needs BOTH matra forms or the महास्थल colophon reads as having no count.
_MATRA = {'ए': ['े', 'ै'], 'अ': ['ा'], 'ओ': ['ो']}
NUMERALS = NUMERALS + [(m + w[1:], n) for w, n in NUMERALS
                       for m in _MATRA.get(w[0], [])]
# 'ष्ठक' kept as a fallback for 'अष्टक'. One colophon was transcribed `स्वरूपष्ठकं`; the audit pass
# showed it is simply `स्वरूपाष्टकं` (eight, दोहा 8-15) and `parts/` is corrected, but the entry costs
# nothing and would catch the same misreading again.
NUMERALS.append(('ष्ठक', 8))
NUMERALS.sort(key=lambda x: -len(x[0]))

# A colophon names a स्थल or महाधिकार and says it is finished. Require both, so that an ordinary
# भावार्थ sentence ending '… समाप्तम्' is not mistaken for one.
# A colophon may close with । OR ॥ — requiring । alone missed seven of the thirty-eight
# divisions in this ग्रन्थ, including the five-दोहा शुद्धोपयोग अन्तरस्थल.
COLOPHON = re.compile(r'[^।॥"]*(?:स्थल|महाधिकार)[^।॥"]*(?:समाप्तम्|समाप्तः|गतम्|गतः)\s*(?:॥\s*\d+\s*॥)?\s*[।॥]')

# The edition prints a हिन्दी twin of every colophon, and it states the SAME arithmetic independently:
#   "इकतालीस दोहोंके महास्थलमें … आठ दोहोंका तीसरा अंतरस्थल पूर्ण हुआ"
# That makes the two streams independent witnesses to the ग्रन्थ's structure. A स्थल that shows up in one
# language but not the other means a colophon was lost — which is exactly what happens when one sits on a
# batch seam and each neighbouring agent leaves it to the other.
HINDI_COLOPHON = re.compile(r'[^।]*(?:स्थल|महाधिकार|अधिकार)[^।]*(?:पूर्ण हुए|पूर्ण हुआ|समाप्त हुआ|समाप्त हुए|पूरा हुआ)[^।]*।')
HINDI_NUM = [('इकतालीस', 41), ('इकतीस', 31), ('चौदह', 14), ('सत्रह', 17), ('उन्नीस', 19), ('तेरह', 13),
             ('बारह', 12), ('ग्यारह', 11), ('पंद्रह', 15), ('पन्द्रह', 15), ('सोलह', 16), ('अठारह', 18),
             ('बीस', 20), ('दस', 10), ('नौ', 9), ('आठ', 8), ('सात', 7), ('छह', 6), ('पाँच', 5),
             ('पांच', 5), ('चार', 4), ('तीन', 3), ('दो', 2), ('एक', 1)]
HINDI_NUM.sort(key=lambda x: -len(x[0]))


def value(text, table=None):
    """The count of the स्थल being closed is the LAST number word in the sentence, not the first.

    These colophons nest, and a nested one names its container before itself:

        एवम्-एकचत्वारिंशत्-सूत्रैः … महास्थलमध्ये … सूत्राष्टकेन तृतीयम् अन्तरस्थलं समाप्तम् ।
             \_ the containing महास्थल (41)              \_ THIS स्थल (8)

    Taking the first match returns 41 for a स्थल of 8. Taking the last also steps past descriptive
    numbers that are not counts at all, such as the षोडश of षोडशवर्णिकासुवर्ण ("sixteen-carat gold",
    a simile) in the colophon that actually closes a त्रयोदश-सूत्र स्थल.
    """
    # Pick by where the match ENDS, and on a tie prefer the LONGER word. Sorting the table
    # longest-first is not enough once matches are ranked by position: 'सप्तदशक' (17) contains
    # 'दशक' (10), both end at the same place, and taking the rightmost START made the shorter one
    # win — reporting a 17-दोहा स्थल as 10. Nesting has the same shape as substring overlap here,
    # so both have to be handled explicitly.
    best = None
    for word, n in (table or NUMERALS):
        i = text.rfind(word)
        if i < 0:
            continue
        end, length = i + len(word), len(word)
        if best is None or (end, length) > (best[0], best[1]):
            best = (end, length, n, word)
    return (best[2], best[3]) if best else (None, None)


def decode(key):
    return key // 10000, (key % 10000) // 10, key % 10


SEC = {1: 'अ.1', 2: 'अ.2', 3: 'योग'}

rows, hindi = [], []
for f in sorted(glob.glob('parts/batch*.md')):
    text = io.open(f, encoding='utf-8').read()
    hits = list(re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', text, re.M))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.end():end]
        for c in COLOPHON.finditer(body):
            s = ' '.join(c.group().split())
            if len(s) >= 30:
                rows.append((int(m.group(1)), s, 'sa'))
        for c in HINDI_COLOPHON.finditer(body):
            s = ' '.join(c.group().split())
            if len(s) >= 25 and value(s, HINDI_NUM)[0] is not None:
                hindi.append((int(m.group(1)), s))

rows.sort()
if not rows:
    sys.exit('no स्थल colophon found in parts/ yet')

# Which (अधिकार, दोहा) actually have commentary written? A merged § titled "दोहा 19-21" covers three,
# so read the claim from the title exactly as check_coverage.py does — otherwise a legitimate merge
# reads as a gap.
written = set()
for f in glob.glob('parts/batch*.md'):
    for m in re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', io.open(f, encoding='utf-8').read(), re.M):
        k, title = int(m.group(1)), m.group(2)
        base, doha, star = decode(k)
        if star:
            continue                      # starred प्रक्षेपक sit outside the ग्रन्थ's own counts
        g = re.search(r'दोहा\s*(\d+)(?:\s*[–—-]\s*(\d+))?', title)
        lo = int(g.group(1)) if g else doha
        hi = int(g.group(2)) if (g and g.group(2)) else lo
        for d in range(lo, hi + 1):
            written.add((base, d))

print('स्थल colophons found: %d\n' % len(rows))
problems = 0
for key, s, _lang in rows:
    base, doha, _ = decode(key)
    n, word = value(s)
    where = '%s %d' % (SEC.get(base, '?'), doha)
    if n is None:
        print('  ?   %-8s no count word     %s' % (where, s[:95]))
        continue
    lo = doha - n + 1
    gap = [d for d in range(max(lo, 1), doha + 1) if (base, d) not in written]
    flag = ''
    if lo < 1:
        flag = '  <-- implies a start before दोहा 1'
        problems += 1
    elif gap:
        flag = '  <-- no § for दोहा %s' % ','.join(str(d) for d in gap[:6])
        problems += 1
    print('  %s %-8s says %-2d (%-12s) -> दोहा %d-%d%s'
          % ('!!' if flag else 'ok', where, n, word, lo, doha, flag))

print('\nस्थल nest, so these ranges are expected to overlap — a 41-दोहा महास्थल contains the 5- and')
print('15-दोहा अन्तरस्थल inside it. Only the flagged lines need chasing.')
if problems:
    print('\n%d colophon(s) imply a दोहा with no § written.' % problems)
    sys.exit(1)
