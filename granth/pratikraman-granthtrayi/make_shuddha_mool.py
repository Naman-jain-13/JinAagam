"""Regenerate backmatter/03_shuddha_mool.md (परिशिष्ट — शुद्ध मूल-पाठ) from the CURRENT parts/*.md.

Takes only part 1 ("## 1. मूल पाठ …") of every §, in key order, so whatever the re-collation
corrected in parts/ is carried here too. Never retype this file by hand — rerun:

    python make_shuddha_mool.py            # writes backmatter/03_shuddha_mool.md
    python make_shuddha_mool.py --check    # only reports counts

The टीका (part 6) is NOT included: v1's file carried only the मूल, and the reader wants the
continuous सूत्र-पाठ for recitation and for checking the § against the print.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'backmatter', '03_shuddha_mool.md')
PAGELINE = re.compile(r'^\(\s*पृष्ठ\s*([0-9०-९–-]+)[^)]*\)\s*$')
SEC_RE = re.compile(r'^§\s*([0-9]+)\s*[—–-]')

GRANTHS = [
    (10, 1050, 'परिशिष्ट-क — प्रथम ग्रन्थ : दैवसिक-रात्रिक प्रतिक्रमण'),
    (1060, 1880, 'परिशिष्ट-ख — द्वितीय ग्रन्थ : बृहत्प्रतिक्रमण'),
    (1890, 2320, 'परिशिष्ट-ग — तृतीय ग्रन्थ : आलोचना'),
]

INTRO = (
    'मुद्रित प्रति के अन्त में तीनों ग्रन्थों का अनुवाद-रहित, लगातार मूल-पाठ छपा है। वही पाठ यहाँ अनुच्छेद-क्रम से '
    'एक साथ दिया जा रहा है, ताकि पाठक एक बैठक में पूरे सूत्र-क्रम का पाठ कर सके। प्रत्येक खण्ड के आरम्भ में उस '
    'अनुच्छेद (§) का क्रमांक है जिसमें वह खण्ड व्याख्यात है, और जहाँ मुद्रित पृष्ठ बदलता है वहाँ परिशिष्ट का मुद्रित '
    'पृष्ठ-अङ्क दिया गया है। यह पाठ मुद्रित प्रति से अक्षरशः दुबारा मिलाया गया है; मुद्रित वर्तनी, सम्पादक के कोष्ठक '
    'में दिए वैकल्पिक पाठ "( )" और मुद्रण की स्पष्ट भूलें भी यथावत् रखी गई हैं, कुछ भी चुपचाप सुधारा नहीं गया। '
    'टीका जिस रूप को उद्धृत करती है और परिशिष्ट जिस रूप को छापता है, उनमें जहाँ वर्तनी का अन्तर है, उसका उल्लेख '
    'सम्बन्धित अनुच्छेद के सन्दर्भ-भाग में है।'
)


def collect():
    secs = {}
    for f in sorted(glob.glob(os.path.join(HERE, 'parts', '*.md'))):
        cur = None
        in1 = False
        for raw in open(f, encoding='utf-8').read().split('\n'):
            line = raw.rstrip('\r')
            m = SEC_RE.match(line.strip())
            if m:
                cur = int(m.group(1))
                in1 = False
                continue
            if cur is None:
                continue
            if line.strip().startswith('## '):
                in1 = line.strip()[3:].startswith('1.')
                if in1:
                    secs.setdefault(cur, [])
                continue
            if in1 and line.strip() and line.strip() != '---':
                secs[cur].append(line.strip())
    return secs


def main():
    secs = collect()
    out = ['# परिशिष्ट — शुद्ध मूल-पाठ', '', INTRO, '']
    n_sec = n_line = 0
    for lo, hi, title in GRANTHS:
        out += [f'## {title}', '']
        last_page = None
        for k in sorted(x for x in secs if lo <= x <= hi):
            body = []
            for t in secs[k]:
                pm = PAGELINE.match(t)
                if pm:
                    page = pm.group(1)
                    pp = re.split(r'[–-]', page)
                    # a range "203–204" means the § runs onto the next page: show the range once
                    if pp[0] != last_page or pp[-1] != last_page:
                        body.append(('page', page))
                    last_page = pp[-1]
                    continue
                body.append(('text', t))
            texts = [t for kind, t in body if kind == 'text']
            if not texts:
                continue
            n_sec += 1
            first_text = True
            for kind, t in body:
                if kind == 'page':
                    out.append(f'*[परिशिष्ट, मुद्रित पृष्ठ {t}]*')
                    continue
                n_line += 1
                # every line bold like the print; § number plain, on the first line only
                prefix = f'§ {k // 10} — ' if first_text else ''
                out.append(f'{prefix}**{t}**')
                first_text = False
            out.append('')
    text = '\n'.join(out).rstrip() + '\n'
    print(f'§ with part 1: {n_sec} | lines: {n_line} | chars: {len(text)}')
    if '--check' in sys.argv:
        return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print('written:', OUT)


if __name__ == '__main__':
    main()
