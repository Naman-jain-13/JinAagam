#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Find व्याख्या notes that still describe a printed reading since corrected in parts/.

    python check_stale_notes.py

**Why this exists.** Correcting `parts/` after its Hindi has been written does not correct the Hindi — and
worse, it does not correct the *notes* that describe the old reading. Three such notes reached the book
before an auditor happened to notice:

  §10870 — part 6 was fixed, part 10 still called the passage सन्दिग्ध
  §21140 — `parts/` was fixed, the Hindi still printed the wrong reading as primary in three places
  §21900 — part 6 was fixed, part 10 still asserted the reading part 6 had just rejected

Each time the book contradicted itself on one page. The audit pass caught all three, but only because a
reader happened to look; nothing checked for it.

**The check.** Notes cite the printed form explicitly — `मुद्रित 'X'`, `मुद्रित पाठ 'X'`, `'X' छपा है`.
If `X` cannot be found anywhere in `parts/`, either the text was corrected after the note was written, or
the note quotes something that was never there. Both want a human eye.

False positives are expected and harmless: a note may quote a form with added spacing or in a longer
context. The point is to make the list short enough to read.
"""
import io, re, glob, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

parts = ''.join(io.open(f, encoding='utf-8').read() for f in glob.glob('parts/batch*.md'))
parts_flat = re.sub(r'\s+', '', parts)

# The ways a note names the printed reading. Group 1 is always the quoted form.
QUOTE = [
    re.compile(r"मुद्रित(?:\s+(?:पाठ|प्रति(?:\s+में)?|संस्कृत|छाया|हिन्दी))?\s*['‘’“”]([^'‘’“”]{4,60})['‘’“”]"),
    re.compile(r"['‘’“”]([^'‘’“”]{4,60})['‘’“”]\s*छपा\s+है"),
]

DEV = re.compile(r'[ऀ-ॿ]')
hits = []
for f in sorted(glob.glob('addenda/s*.md')):
    text = io.open(f, encoding='utf-8').read()
    for rx in QUOTE:
        for m in rx.finditer(text):
            q = m.group(1).strip()
            # only Devanagari quotations, and only ones long enough to be a real citation
            if len(DEV.findall(q)) < 4:
                continue
            # Notes also quote the edition's printed HINDI, which is prose and will rarely match
            # verbatim. Those are noise here. Keep only citations that look like a single Sanskrit
            # or अपभ्रंश reading: no ellipsis, at most two spaces, no Hindi postpositions.
            if '…' in q or q.count(' ') > 2:
                continue
            if re.search(r'(के|का|की|को|में|से|है|हैं|कहा|यह)', q):
                continue
            flat = re.sub(r'\s+', '', q)
            # strip editorial brackets the note may have added around its own supplements
            flat = re.sub(r'[\[\]\(\)…]', '', flat)
            if flat and flat not in parts_flat:
                hits.append((os.path.basename(f), q))

print('notes quoting a printed form not now in parts/: %d\n' % len(hits))
for f, q in hits:
    print('  %-14s %s' % (f, q[:80]))
if hits:
    print('\nMOST OF THESE ARE CORRECT, and the list is meant to be read, not acted on wholesale.')
    print('A note saying "the page prints X, so we read Y" is DOCUMENTING an emendation — exactly what')
    print('it should do — and X is then expected to be absent from the corrected parts/.')
    print('\nWhat to look for is the opposite: a note that still presents the old reading as the current')
    print('one, or still calls a settled passage doubtful. Three such reached the book — §10870, §21140,')
    print('§21900 — and each contradicted its own part 6 on the same page. Nothing is edited here.')
print('\n(no exit status: this is a review aid, not a gate)')
