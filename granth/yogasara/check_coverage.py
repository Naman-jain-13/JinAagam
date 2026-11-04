#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Coverage and hygiene gate for the परमात्मप्रकाश pass-1 files.

    python check_coverage.py [--quiet]

Run it only once every agent of a wave has REPORTED. An agent still appending its last § looks
exactly like a gap.

The § key encodes three independent दोहा sequences:

    key = base + दोहा x 10 + star
    base 10000 = परमात्मप्रकाश अधिकार 1 | 20000 = अधिकार 2 | 30000 = योगसार

A § may cover several दोहा where the edition gives them one shared टीका (printed त्रिकलम् / तिघलं).
Its title then says "दोहा 19–21" and the keys for 20 and 21 are legitimately unused, so coverage is
tested against the दोहा a § CLAIMS, not against its key alone.

Expected totals come from the ग्रन्थ's own पीठिका, where श्री ब्रह्मदेव sets out his divisions with
their दोहा-counts: अधिकार 1 = 25+24+43+31 = 123, अधिकार 2 = 30+36+41+107 = 214. Those sums were
verified against the printed text. योगसार's count is not declared there, so it is left open.

Checks
  1. every § key decodes to a sane (अधिकार, दोहा, star)
  2. no duplicate keys, no दोहा claimed twice
  3. दोहा contiguous within each section, measured against the पीठिका's totals
  4. every § carries parts 1, 2, 5 and the टीका (part 6 मूल)
  5. (Tn) tags start at T1 and are contiguous — a gap means a lost segment of टीका
  6. forbidden vocabulary
"""
import io, re, sys, glob, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
QUIET = '--quiet' in sys.argv

SECTIONS = {1: ('परमात्मप्रकाश अधिकार 1', 123), 2: ('परमात्मप्रकाश अधिकार 2', 214), 3: ('योगसार', None)}
FORBIDDEN = ['बीसपंथ', 'तेरापंथ', 'बैच', 'उपयोगकर्ता', 'इस सत्र', 'अगले भाग में', 'progress.md']

problems, warnings = [], []


def decode(key):
    base, rest = key // 10000, key % 10000
    return base, rest // 10, rest % 10


secs = {}           # key -> (file, title, body)
claimed = {}        # (base, doha) -> key
for f in sorted(glob.glob('parts/batch*.md')):
    text = io.open(f, encoding='utf-8').read()
    hits = list(re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', text, re.M))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        key, title = int(m.group(1)), m.group(2).strip()
        body = text[m.end():end]
        base, doha, star = decode(key)
        if base not in SECTIONS or not (1 <= doha <= 400):
            problems.append('§%d in %s does not decode to a sane section/दोहा' % (key, os.path.basename(f)))
            continue
        if key in secs:
            problems.append('duplicate §%d (%s and %s)' % (key, secs[key][0], os.path.basename(f)))
        secs[key] = (os.path.basename(f), title, body)

        # which दोहा does this § claim? "दोहा 19–21" claims three.
        # "दोहा 19–21" claims three; "दोहा 65*1" is a starred EXTRA verse, distinct from दोहा 65 and
        # not part of the 1..N sequence. Capture the star so the two never collide.
        # The authoritative reference is the PARENTHETICAL "(अधिकार 2, दोहा 111*2, मुद्रित पृष्ठ 229)",
        # not the first "दोहा N" in the title. A § may open with a descriptive prefix that contains its
        # own number — "प्रक्षेपक दोहा 1: ..." — and reading that one silently reassigns the § to दोहा 1.
        # Three प्रक्षेपक were mis-slotted this way before the parenthetical was made to win.
        paren = re.search(r'\(([^)]*(?:अधिकार|योगसार)[^)]*)\)', title)
        scope = paren.group(1) if paren else title
        g = re.search(r'दोहा\s*(\d+)(?:\*(\d+))?(?:\s*[–—-]\s*(\d+))?', scope)
        if g:
            lo = int(g.group(1)); t_star = int(g.group(2) or 0); hi = int(g.group(3) or g.group(1))
        else:
            lo = hi = doha; t_star = star
        if not g:
            warnings.append('§%d has no "दोहा N" in its title — coverage assumed from the key' % key)
        elif lo != doha or t_star != star:
            problems.append('§%d titled "दोहा %d%s" — key and title disagree (%s)'
                            % (key, lo, '*%d' % t_star if t_star else '', secs[key][0]))
        for d in range(lo, hi + 1):
            slot = (base, d, t_star)
            if slot in claimed:
                problems.append('%s दोहा %d%s claimed by §%d and §%d'
                                % (SECTIONS[base][0], d, '*%d' % t_star if t_star else '', claimed[slot], key))
            claimed[slot] = key

if not secs:
    print('no § found in parts/ — nothing to check')
    sys.exit(1)

# ---- per-section contiguity against the पीठिका's own totals ----
summary = []
for base, (label, expected) in SECTIONS.items():
    got = sorted(d for (b, d, st) in claimed if b == base and st == 0)
    extras = sorted((d, st) for (b, d, st) in claimed if b == base and st)
    if not got:
        continue
    hi = max(got)
    missing = [d for d in range(1, hi + 1) if d not in got]
    for d in missing:
        problems.append('%s दोहा %d has no §' % (label, d))
    tail = ''
    if expected:
        tail = ' | पीठिका says %d' % expected
        if hi > expected:
            warnings.append('%s reaches दोहा %d but the पीठिका declares only %d — check for starred extras'
                            % (label, hi, expected))
    if extras:
        tail += ' | %d starred extra%s' % (len(extras), '' if len(extras) == 1 else 's')
    summary.append('  %-28s दोहा 1–%-4d (%d written)%s' % (label, hi, len(got), tail))

# ---- per-§ structure ----
for key in sorted(secs):
    f, title, body = secs[key]
    for need, label in (('## 1. मूल पाठ', 'part 1 मूल'), ('## 2. संस्कृत छाया', 'part 2 छाया'),
                        ('## 5. हिन्दी अनुवाद', 'part 5 हिन्दी')):
        if need not in body:
            problems.append('§%d is missing %s (%s)' % (key, label, f))
    base_of = key // 10000
    if base_of == 3:
        # योगसार has no commentary. The edition gives each दोहा a पाठान्तर line instead, and that is
        # what its § must carry — checked here so a योगसार § cannot quietly ship with neither.
        if 'पाठभेद' not in body and 'पाठान्तर' not in body:
            problems.append('§%d (योगसार) has no पाठान्तर block (%s)' % (key, f))
    elif 'टीका' not in body:
        problems.append('§%d has no टीका block (%s)' % (key, f))
    elif True:
        tags = [int(t) for t in re.findall(r'^\s*\(T(\d+)\)', body, re.M)]
        if not tags:
            problems.append('§%d has a टीका heading but no (Tn) segments (%s)' % (key, f))
        else:
            want = list(range(1, max(tags) + 1))
            if sorted(set(tags)) != want:
                problems.append('§%d टीका tags are not contiguous from T1: %s (%s)'
                                % (key, sorted(set(tags)), f))
            if len(tags) != len(set(tags)):
                problems.append('§%d repeats a (Tn) tag (%s)' % (key, f))
    for w in FORBIDDEN:
        if w in body:
            problems.append('§%d contains forbidden word "%s" (%s)' % (key, w, f))

if not QUIET:
    print('§ written        : %d' % len(secs))
    print('टीका segments    : %d' % sum(len(re.findall(r'^\s*\(T\d+\)', b, re.M)) for _, _, b in secs.values()))
    for line in summary:
        print(line)
    if warnings:
        print('\n%d note(s):' % len(warnings))
        for w in warnings[:20]:
            print('  ~ ' + w)

if problems:
    print('\n%d PROBLEM(S):' % len(problems))
    for p in problems[:50]:
        print('  ! ' + p)
    if len(problems) > 50:
        print('  … and %d more' % (len(problems) - 50))
    sys.exit(1)
print('\nOK — keys sane, दोहा contiguous, every § has मूल/छाया/हिन्दी/टीका, (Tn) tags contiguous.')
