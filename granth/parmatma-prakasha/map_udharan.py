#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Attach the edition's own quotation-source list to the § that actually carry the quotations.

    python map_udharan.py

The printed edition ends with a three-page `पृष्ठांकाः` apparatus — an alphabetical index of every verse
श्री ब्रह्मदेव quotes in his टीका, by its प्रतीक (opening words), with the page it occurs on and, for about
55 of the 95 entries, the work it comes from. That apparatus is transcribed in
`backmatter/20_udharan_srot.md`.

Several extraction agents flagged quoted verses whose source they could not identify and correctly
declined to guess. This script answers them mechanically: it finds, for each प्रतीक, the § whose टीका
actually contains those words, and writes a per-§ list that the व्याख्या pass can cite from.

**Matching is by text, not by page.** A printed page often carries two दोहा, so the page number alone
cannot say which § a quotation belongs to. The प्रतीक is matched against the टीका text itself, which is
exact. The page number is kept only as a cross-check: if the text match lands on a § whose printed page
is far from the one the apparatus gives, that is reported rather than trusted.

Nothing here is a citation of our own. Everything printed is the edition's attribution, reproduced.
"""
import io, re, glob, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEV_DIGITS = str.maketrans('०१२३४५६७८९', '0123456789')


def dev_int(s):
    s = s.translate(DEV_DIGITS)
    m = re.search(r'\d+', s)
    return int(m.group()) if m else None


def norm(s):
    """Strip hyphens, danda and whitespace so a प्रतीक printed with a break still matches."""
    return re.sub(r'[\s।॥\-–—\.]+', '', s)


# ---- read the apparatus ----
SRC = 'backmatter/20_udharan_srot.md'
if not os.path.exists(SRC):
    sys.exit('%s not found — transcribe the apparatus first' % SRC)

rows = []
for line in io.open(SRC, encoding='utf-8'):
    if not line.startswith('|'):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if len(cells) < 3 or cells[0].startswith('---') or 'प्रतीक' in cells[0]:
        continue
    pratika, page, src = cells[0], dev_int(cells[1]), cells[2]
    if pratika:
        rows.append((pratika, page, src))

# ---- read every § with its टीका text and printed page ----
secs = []
for f in sorted(glob.glob('parts/batch*.md')):
    text = io.open(f, encoding='utf-8').read()
    hits = list(re.finditer(r'^§\s*(\d+)\s*[—–-]\s*(.*)$', text, re.M))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.end():end]
        title = m.group(2).strip()
        pg = re.search(r'मुद्रित पृष्ठ\s*([०-९\d]+)', title)
        secs.append({'key': int(m.group(1)), 'title': title,
                     'page': dev_int(pg.group(1)) if pg else None,
                     'flat': norm(body)})

found, missed, suspect = {}, [], []
for pratika, page, src in rows:
    needle = norm(pratika)
    # The apparatus prints a प्रतीक in its pausal form, but inside the टीका the same words are joined by
    # sandhi to whatever follows — the index's `कषायैरिन्द्रियैः` appears in the text as
    # `कषायैरिन्द्रियैर्दुष्टैः`, so a match on the full प्रतीक fails on its last syllable. Try the whole
    # thing first, then progressively shorter prefixes, and also a form with a trailing visarga dropped.
    # A long probe is preferred because a short one matches too freely; shortening is the fallback.
    hit = []
    for probe in [needle, needle.rstrip('ः'), needle[:18], needle[:14], needle[:11]]:
        if len(probe) < 8:
            continue
        hit = [s for s in secs if probe in s['flat']]
        if hit:
            break
    if not hit:
        missed.append((pratika, page, src))
        continue
    for s in hit[:2]:
        found.setdefault(s['key'], []).append((pratika, src, page))
        if page and s['page'] and abs(s['page'] - page) > 3:
            suspect.append((pratika, page, s['key'], s['page']))

out = ['# उद्धरण और उनके स्रोत — § के अनुसार',
       '',
       '*कार्य-सूची। यह फ़ाइल पुस्तक में नहीं जाती।*',
       '',
       'मुद्रित संस्करण स्वयं अपने अन्त में उद्धृत पद्यों की एक वर्णानुक्रम-सूची देता है, जिसमें प्रायः',
       'यह भी बताया गया है कि उद्धरण किस ग्रन्थ से लिया गया है। नीचे वही सूचना उस § के साथ जोड़ दी गई है',
       'जिसकी टीका में वह उद्धरण वस्तुतः आता है।',
       '',
       '**व्याख्या लिखते समय:** यदि आपके § के नीचे कोई पंक्ति दी गई है, तो भाग 10 में उसी ग्रन्थ का',
       'नाम दीजिये। जहाँ स्रोत "—" है, वहाँ संस्करण ने स्वयं कोई स्रोत नहीं दिया — ऐसी स्थिति में कोई',
       'स्रोत गढ़िये मत; केवल इतना लिखिये कि यह उद्धरण है।',
       '']
for key in sorted(found):
    s = next(x for x in secs if x['key'] == key)
    out.append('### §%d — %s' % (key, s['title']))
    for pratika, src, page in found[key]:
        # The apparatus indexes one occurrence of each verse; the टीका sometimes quotes the same verse
        # twice, far apart. Where the § we matched sits well away from the page the apparatus names,
        # say so rather than letting the attribution be used unexamined.
        far = page and s['page'] and abs(s['page'] - page) > 3
        note = '  **(सूची में यह उद्धरण मुद्रित पृष्ठ %s पर दर्ज है, यह § पृष्ठ %s का है — '                'सम्भवतः यही पद्य दो स्थानों पर उद्धृत है; उद्धरण मिलाकर ही स्रोत दीजिये)**'                % (page, s['page']) if far else ''
        out.append('- `%s…` — %s%s'
                   % (pratika, src if src and src != '—' else '**स्रोत संस्करण में नहीं दिया गया**', note))
    out.append('')

if missed:
    out += ['## जिनका § नहीं मिला', '',
            'इनका प्रतीक किसी § की टीका में अक्षरशः नहीं मिला — सम्भवतः मुद्रण-भेद या पंक्ति-विच्छेद के कारण।', '']
    for pratika, page, src in missed:
        out.append('- `%s` (मुद्रित पृष्ठ %s) — %s' % (pratika, page, src))
    out.append('')

io.open('verify/udharan_map.md', 'w', encoding='utf-8', newline='').write('\n'.join(out))

print('apparatus entries : %d' % len(rows))
print('matched to a §    : %d' % sum(len(v) for v in found.values()))
print('§ carrying a quote: %d' % len(found))
print('not matched       : %d' % len(missed))
if suspect:
    print('\n%d match(es) land far from the page the apparatus gives — check these:' % len(suspect))
    for pratika, page, key, spage in suspect[:10]:
        print('  %-28s apparatus p.%s vs §%d on p.%s' % (pratika[:28], page, key, spage))
print('\nwritten: verify/udharan_map.md')
