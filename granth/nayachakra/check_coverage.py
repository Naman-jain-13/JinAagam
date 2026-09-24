#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Coverage and hygiene gate for the नयचक्र pass-1 files.

    python check_coverage.py            # everything
    python check_coverage.py --quiet    # only problems

Run it only once every agent of a wave has REPORTED. An agent that is still appending
its last § looks exactly like a seam gap, and that false alarm has already cost one
wasted repair agent on this book.

Checks
  1. duplicate गाथा across §
  2. missing गाथा in the covered range
  3. § number != the first गाथा in its own title
  4. § present in a footnotes/ sidecar but absent from parts/  <- catches the गाथा 109-110
     failure, where an agent transcribed a page's footnotes and never wrote its units
  5. forbidden vocabulary (sect names, working-process language) anywhere in parts/
  6. § missing part 1 or part 5
"""
import io, re, sys, glob, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
QUIET = '--quiet' in sys.argv
FORBIDDEN = ['बीसपंथ', 'तेरापंथ', 'बैच', 'उपयोगकर्ता', 'इस सत्र', 'अगले भाग में', 'progress.md']
problems = []


def say(msg):
    if not QUIET:
        print(msg)


def sections(path):
    """[(num, title, body)] for one markdown file."""
    text = io.open(path, encoding='utf-8').read()
    hits = list(re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', text, re.M))
    out = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        out.append((int(m.group(1)), m.group(2).strip(), text[m.end():end]))
    return out


# ---- gather ----
parts = {}                      # gatha-number -> § number
sec_of = {}                     # § number -> (file, title, body)
for f in sorted(glob.glob('parts/batch*.md')):
    for num, title, body in sections(f):
        if num in sec_of:
            problems.append('DUPLICATE §%d: %s and %s' % (num, sec_of[num][0], f))
        sec_of[num] = (f, title, body)
        g = re.search(r'गाथा\s*(\d+)\s*(?:[–—-]\s*(\d+))?', title)
        if not g:
            problems.append('§%d has no गाथा in its title (%s)' % (num, f))
            continue
        a, b = int(g.group(1)), int(g.group(2) or g.group(1))
        if a != num:
            problems.append('§%d titled "गाथा %d" — number/title mismatch (%s)' % (num, a, f))
        for x in range(a, b + 1):
            if x in parts:
                problems.append('गाथा %d claimed by §%d and §%d' % (x, parts[x], num))
            parts[x] = num

if not parts:
    print('no § found in parts/ — nothing to check')
    sys.exit(1)

# ---- 2. missing gathas ----
hi = max(parts)
missing = [x for x in range(1, hi + 1) if x not in parts]
for x in missing:
    problems.append('गाथा %d has no § (gap in parts/)' % x)

# ---- 4. sidecar mentions a गाथा that parts/ never wrote ----
# A sidecar keys footnotes by the individual गाथा number, but parts/ merges गाथा that share one
# विशेषार्थ into a single § named for the first of them (§234 covers गाथा 234–236). So the test is
# "is this गाथा covered by SOME §" — i.e. is it in the `parts` gatha->§ map — not "does a § with
# exactly this number exist". Testing the latter reports every merged § as a skipped unit.
for f in sorted(glob.glob('footnotes/*.md')):
    for m in re.finditer(r'^§\s*(\d+)\b', io.open(f, encoding='utf-8').read(), re.M):
        n = int(m.group(1))
        if n not in parts:
            problems.append('गाथा %d has footnotes in %s but no § covers it — unit skipped' % (n, f))

# ---- 5 & 6 ----
for num, (f, title, body) in sec_of.items():
    if '## 1. मूल पाठ' not in body:
        problems.append('§%d is missing part 1 (%s)' % (num, f))
    if '## 5. हिन्दी अनुवाद' not in body:
        problems.append('§%d is missing part 5 (%s)' % (num, f))
    for w in FORBIDDEN:
        if w in body:
            problems.append('§%d contains forbidden word "%s" (%s)' % (num, w, f))

# ---- report ----
say('§ written      : %d' % len(sec_of))
say('गाथा covered   : 1–%d' % hi)
grouped = []
for n, (f, t, b) in sorted(sec_of.items()):
    m = re.search(r'गाथा\s*\d+\s*[–—-]\s*\d+', t)
    if m:
        grouped.append('§%d=%s' % (n, m.group(0)))
say('grouped §      : %s' % (', '.join(grouped) or '(none)'))
say('')
for f in sorted(glob.glob('parts/batch*.md')):
    ns = [n for n, v in sec_of.items() if v[0] == f]
    if ns:
        say('  %-28s §%d–§%d  (%d §)' % (os.path.basename(f), min(ns), max(ns), len(ns)))

if problems:
    print('\n%d PROBLEM(S):' % len(problems))
    for p in problems:
        print('  ! ' + p)
    sys.exit(1)
print('\nOK — no gaps, no duplicates, no forbidden words, every § has parts 1 and 5.')
