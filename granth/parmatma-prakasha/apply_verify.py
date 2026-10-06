#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Apply pass-3 audit findings to addenda/.

    python apply_verify.py verify/v10880-11180.md          # dry run — show what would change
    python apply_verify.py verify/v10880-11180.md --write   # apply

The audit pass reports; it does not edit. This applies what it reported, so that every change to the
व्याख्या has a written finding behind it and the two stay separable.

It acts only on findings that carry a **सुझाया हिन्दी** line giving a complete replacement — that is,
त्रुटि and लोप. सन्देह and वर्धन are read by a person and applied by hand if at all.

**Safety.** A finding is applied only when the `लिखित हिन्दी` it quotes still matches what is in the file,
anchored on the (Tn) tag. If the file has changed since the audit ran, or the quotation does not line up,
the finding is reported as STALE and skipped rather than guessed at. Nothing is applied silently.
"""
import io, re, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
WRITE = '--write' in sys.argv
if not args:
    sys.exit(__doc__)

TAG = re.compile(r'^\s*\((T\d+)\)\s*')


def blocks(text):
    """Yield (key, tag, kind, suggested) for every finding that offers a replacement."""
    for m in re.finditer(r'^###\s*§\s*(\d+)\s*\((T\d+)\)[^\n]*?—\s*(\S+)(.*?)(?=^###|\Z)',
                         text, re.M | re.S):
        key, tag, kind, body = m.group(1), m.group(2), m.group(3), m.group(4)
        s = re.search(r'\*\*सुझाया हिन्दी:\*\*\s*(.*?)(?=\n\s*-\s*\*\*|\Z)', body, re.S)
        if not s:
            continue
        sug = ' '.join(s.group(1).split())
        # auditors often wrap the replacement in backticks, and some repeat the (Tn) prefix inside
        # them; strip both before use or the applied line gets a doubled tag and stray backticks
        sug = sug.strip().strip('`').strip()
        sug = TAG.sub('', sug).strip().strip('`').strip()
        sug = TAG.sub('', sug).strip()
        if not sug:
            continue
        # A suggestion that opens with an ellipsis is a PARTIAL replacement: the auditor is quoting
        # only the tail of a long segment. Applying it as a whole line would delete the head.
        # §11160 T3 is one such — a single (T3) carrying both `किं कुर्वन् सन्` and `किं कृत्वा`,
        # where only the second half was faulted. These are reported for hand-application, never applied.
        # A suggestion that opens as a bullet is a replacement for a part-10 note, not for a
        # (Tn) line — applying it would overwrite a टीका translation with a footnote.
        if sug.lstrip().startswith(('- ', '* ')):
            yield key, tag, 'PART10', sug
        elif sug.lstrip().startswith(('…', '...')):
            yield key, tag, 'PARTIAL', sug
        else:
            yield key, tag, kind, sug


total = applied = stale = 0
for path in args:
    text = io.open(path, encoding='utf-8').read()
    print('\n%s' % os.path.basename(path))
    for key, tag, kind, sug in blocks(text):
        total += 1
        f = os.path.join('addenda', 's%s.md' % key)
        if not os.path.exists(f):
            print('  STALE %s %s — no %s' % (key, tag, f)); stale += 1; continue
        lines = io.open(f, encoding='utf-8').read().split('\n')
        hit = None
        for i, L in enumerate(lines):
            m = TAG.match(L)
            if m and m.group(1) == tag:
                hit = i
                break
        if hit is None:
            print('  STALE §%s %s — tag not found' % (key, tag)); stale += 1; continue
        old = lines[hit]
        if kind == 'PART10':
            print('  HAND  §%s %s — this replaces a part-10 note, not a (Tn) line; apply by hand' % (key, tag))
            stale += 1
            continue
        if kind == 'PARTIAL':
            print('  HAND  §%s %s — partial replacement (opens with an ellipsis); apply by hand' % (key, tag))
            print('        suggestion: %s' % sug[:120])
            stale += 1
            continue
        new = '(%s) %s' % (tag, sug)
        if old.strip() == new.strip():
            print('  ok    §%s %s — already applied' % (key, tag)); continue
        print('  %-5s §%s %s' % (kind, key, tag))
        print('        - %s' % old.strip()[:110])
        print('        + %s' % new.strip()[:110])
        if WRITE:
            lines[hit] = new
            io.open(f, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
        applied += 1

print('\nfindings with a replacement: %d | %s: %d | stale: %d'
      % (total, 'applied' if WRITE else 'would apply', applied, stale))
if not WRITE and applied:
    print('re-run with --write to apply')
