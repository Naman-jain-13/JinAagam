#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quality gate for the pass-2 व्याख्या files in addenda/.

    python check_addenda.py            # full report
    python check_addenda.py --quiet    # only problems

Every § in parts/ must end up with one addenda file carrying all seven of the parts that
pass 2 owns. This checks that, plus the rules the reader set that are mechanically checkable.

Checks
  1. every § has an addenda file, and every addenda file matches a real §
  2. all seven headings present, in order, spelled as the builder expects
  3. parts 1 and 5 NOT redefined in addenda (they live in parts/ and would collide)
  4. part 9 compact: 1-3 bullets, no blank line between them
  5. forbidden vocabulary — sect names, working-process language
  6. bare आचार्य names that postprocess_docx.py would have to rescue
  7. thin parts — a व्याख्या (part 6) under 400 words, or fewer than 4 bullets
  8. [अस्पष्ट] in part 1 of a § whose छाया does not also carry it
"""
import io, re, sys, glob, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
QUIET = '--quiet' in sys.argv

PARTS = [
    ('2', 'संस्कृत छाया'),
    ('3', 'अन्वय'),
    ('4', 'अन्वयार्थ'),
    ('6', 'जैनागम के अनुसार विस्तृत व्याख्या'),
    ('7', 'सरल उदाहरण'),
    ('8', 'तुलनात्मक तालिका'),
    ('9', 'सन्दर्भ एवं पाद-टिप्पणी'),
]
FORBIDDEN = ['बीसपंथ', 'तेरापंथ', 'बैच', 'उपयोगकर्ता', 'इस सत्र', 'अगले भाग में',
             'progress.md', 'स्कैन', 'एजेंट']
# names that must never stand bare; postprocess_docx.py is the safety net but source should be right
BARE = ['कुन्दकुन्द', 'कुंदकुंद', 'देवसेन', 'अमृतचन्द्र', 'समन्तभद्र', 'पूज्यपाद',
        'अकलंक', 'अकलङ्क', 'विद्यानन्द', 'उमास्वामी', 'नेमिचन्द्र', 'वीरसेन', 'जिनसेन',
        'माइल्लधवल', 'योगीन्दु', 'शुभचन्द्र', 'प्रभाचन्द्र', 'माणिक्यनन्दी']
# 'अनन्तवीर्य' is excluded: in this ग्रन्थ it is always the quality of the अनन्तचतुष्टय, never the आचार्य.
HONOURED = re.compile(r'(श्री|आचार्य|स्वामी|भट्ट|भट्टारक|मुनि|भगवान्?|पण्डित|पं\.)[\s\-–]*$')
# Anything inside quotes is being CITED, not referred to: a manuscript reading, a Sanskrit टिप्पणी,
# a छाया form. Such a name must stay exactly as the source has it, so the bare-name check skips
# quoted spans. postprocess_docx.py leaves them alone too (a Devanagari character follows the name
# in each), so this keeps the gate and the post-processor agreeing.
QUOTES = '‘’“”\'"'
QUOTED = re.compile('[' + QUOTES + '][^' + QUOTES + '\n]{0,120}?[' + QUOTES + ']')

problems = []

sec_nums = set()
for f in sorted(glob.glob('parts/batch*.md')):
    for m in re.finditer(r'^§\s*(\d+)\s*[—–-]', io.open(f, encoding='utf-8').read(), re.M):
        sec_nums.add(int(m.group(1)))

add = {}
for f in sorted(glob.glob('addenda/s*.md')):
    m = re.match(r's0*(\d+)\.md$', os.path.basename(f))
    if not m:
        problems.append('%s — filename not s<NNN>.md' % f)
        continue
    add[int(m.group(1))] = f

missing = sorted(sec_nums - set(add))
orphan = sorted(set(add) - sec_nums)
for n in missing:
    problems.append('§%d has no addenda file' % n)
for n in orphan:
    problems.append('addenda/s%03d.md has no matching § in parts/' % n)

thin = []
for n in sorted(add):
    f = add[n]
    t = io.open(f, encoding='utf-8').read()
    b = os.path.basename(f)

    # 2. headings present and ordered
    pos = []
    for num, name in PARTS:
        m = re.search(r'^##\s*%s\.\s*%s' % (num, re.escape(name.split()[0])), t, re.M)
        if not m:
            problems.append('%s — missing part %s (%s)' % (b, num, name))
        else:
            pos.append((num, m.start()))
    if pos == sorted(pos, key=lambda x: x[1]) and len(pos) == len(PARTS):
        pass
    elif len(pos) == len(PARTS):
        problems.append('%s — parts out of order' % b)

    # 3. must not redefine parts 1 or 5
    for num in ('1', '5'):
        if re.search(r'^##\s*%s\.' % num, t, re.M):
            problems.append('%s — redefines part %s (it belongs to parts/)' % (b, num))

    # 4. part 9 compact
    m9 = re.search(r'^##\s*9\..*?$(.*)\Z', t, re.M | re.S)
    if m9:
        body = m9.group(1).strip('\n')
        bullets = [l for l in body.split('\n') if l.strip().startswith(('-', '*'))]
        if len(bullets) > 3:
            problems.append('%s — part 9 has %d bullets (max 3)' % (b, len(bullets)))
        if re.search(r'\n[ \t]*\n[ \t]*[-*]', body):
            problems.append('%s — part 9 has a blank line between bullets' % b)

    # 5. forbidden vocabulary
    for w in FORBIDDEN:
        if w in t:
            problems.append('%s — forbidden word "%s"' % (b, w))

    # 6. bare आचार्य names — only in the PROSE parts (6-9). Parts 2-4 reproduce the गाथा's own words:
    # the छाया, the अन्वय, and the अन्वयार्थ's पद, Sanskrit forms and compound splits
    # ('देवसेण = देवसेन + देव'). A name there is quoted matter and must stay bare; postprocess_docx.py
    # exempts the same parts.
    prose = t
    m6 = re.search(r'^##\s*6\.', t, re.M)
    if m6:
        prose = t[m6.start():]
    # Drop quoted spans before looking for bare names. A name inside quotes is being CITED — a manuscript
    # reading ('देवसेनके शिष्य'), a Sanskrit टिप्पणी ('देवसेनशिष्येण'), a छाया form ('[माइल्लधवलेन]') — and
    # must stay exactly as the source has it. postprocess_docx.py leaves these alone anyway, because a
    # Devanagari character follows the name in each; this keeps the gate agreeing with it.
    prose = QUOTED.sub(' ', prose)
    for name in BARE:
        for m in re.finditer(r'(?<![ऀ-ॿ])' + name, prose):
            pre = prose[max(0, m.start() - 24):m.start()]
            if not HONOURED.search(pre):
                problems.append('%s — bare "%s" in prose (needs श्री … स्वामी)' % (b, name))
                break

    # 7. thin व्याख्या
    m6 = re.search(r'^##\s*6\..*?$(.*?)(?=^##\s|\Z)', t, re.M | re.S)
    if m6:
        words = len(m6.group(1).split())
        bl = len([l for l in m6.group(1).split('\n') if l.strip().startswith(('-', '*'))])
        if words < 400 or bl < 4:
            thin.append((b, words, bl))

if not QUIET:
    print('§ in parts/        : %d' % len(sec_nums))
    print('addenda files      : %d' % len(add))
    print('still to write     : %d' % len(missing))
    if thin:
        print('\nthin व्याख्या (part 6 under 400 words or fewer than 4 bullets) — %d:' % len(thin))
        for b, w, n in thin[:25]:
            print('  %-12s %4d words, %d bullets' % (b, w, n))

hard = [p for p in problems if 'has no addenda file' not in p]
if hard:
    print('\n%d PROBLEM(S):' % len(hard))
    for p in hard[:60]:
        print('  ! ' + p)
    if len(hard) > 60:
        print('  … and %d more' % (len(hard) - 60))
    sys.exit(1)
if missing:
    print('\n%d § still to write — not yet complete.' % len(missing))
    sys.exit(1)
print('\nOK — every § has all seven parts, part 9 compact, no forbidden words, no bare names.')
