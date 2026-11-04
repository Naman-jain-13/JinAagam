# -*- coding: utf-8 -*-
"""दोनों भागों के parts/ से परिशिष्ट बनाता है — backmatter/51, 52, 53.

    python build_parishisht.py            # तीनों फ़ाइलें फिर से लिखता है
    python build_parishisht.py --review   # अस्वीकृत कारिका-पंक्तियाँ भी छापता है

स्रोत केवल हमारा अपना लिपिबद्ध पाठ है (हर § का "## 1. मूल पाठ" खण्ड, आलोकार्थ-टिप्पण
से पहले तक)। छपे संस्करण की परिशिष्ट-तालिकाएँ नहीं ली गईं — उनकी पृष्ठ-संख्याएँ इस
पुस्तक पर लागू नहीं होतीं।

50_prashasti.md हाथ से लिखी गई है; यह स्क्रिप्ट उसे नहीं छूती।
"""
import glob
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
VOLS = [(1, HERE.parent / 'siddhi-vinishchaya-1'), (2, HERE)]
OUT = HERE / 'backmatter'

# प्रस्ताव के पहले § (groups.json से) — भाग 1: 1–5, भाग 2: 6–12
PRASTAVA_START = {
    1: [(1, 1), (375, 2), (554, 3), (727, 4), (1041, 5)],
    2: [(1, 6), (216, 7), (377, 8), (539, 9), (718, 10), (787, 11), (903, 12)],
}
DEV = str.maketrans('०१२३४५६७८९', '0123456789')


def prastava(vol, sec):
    p = None
    for first, n in PRASTAVA_START[vol]:
        if sec >= first:
            p = n
    return p


def mula_sections():
    """(भाग, §, [मूल-पाठ की पंक्तियाँ]) — आलोकार्थ-टिप्पण से पहले तक।"""
    for vol, d in VOLS:
        for f in sorted(glob.glob(str(d / 'parts' / '*.md'))):
            num, sec, buf, stop = None, None, [], False
            for raw in open(f, encoding='utf-8'):
                line = raw.rstrip('\n').rstrip('\r')
                m = re.match(r'^§\s*([0-9०-९]+)\s*[—–-]', line)
                if m:
                    if num is not None and buf:
                        yield vol, num, buf
                    num, sec, buf, stop = int(m.group(1).translate(DEV)), None, [], False
                    continue
                if line.startswith('## '):
                    sec = line[3:].strip()
                    continue
                if sec and sec.startswith('1') and not stop:
                    if line.strip().startswith('आलोकार्थ-टिप्पण'):
                        stop = True
                        continue
                    buf.append(line)
            if num is not None and buf:
                yield vol, num, buf


def clean(s):
    s = s.replace('**', '').replace('*', '')
    s = re.sub(r'\[[०-९0-9]+\s*[कख]\]', '', s)           # पत्र-संख्या [३२२ख]
    s = re.sub(r'^\s*[०-९0-9]{1,2}\s+(?=\S)', '', s)      # पंक्ति-संख्या "२०"
    s = s.strip().lstrip('[').strip()
    s = re.sub(r'\s*\]\s*$', '', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip(' ,')


def sort_key(s):
    s = re.sub(r'^[^अ-ह]+', '', s)
    return s


# ---------------------------------------------------------------- 51 कारिका
END_RE = re.compile(r'॥\s*([०-९0-9]+)\s*॥')


# जहाँ मुद्रित पाठ में कारिका टीका-गद्य से अलग नहीं होती, वहाँ केवल पहचाना जा सकने वाला अंश
OVERRIDE = {
    (2, 93): ['प्रतिपक्षैकान्तवत् तद्भावैश्चाद्यलक्षणैर्भाव्यमप्रमादिभिः'],
    (2, 98): ['मिथ्यैकान्तक्रियाऽनर्थासिद्धौ …'],
}
ACCEPT = {(1, 1203): 27}      # प्रस्ताव 5 की 27वीं कारिका, पर अंक ॥२४॥ छपा है


def karikas(review=False):
    rows, rejected = [], []
    last = {}
    for vol, num, lines in mula_sections():
        pr = prastava(vol, num)
        for i, line in enumerate(lines):
            t = line.strip()
            if t.startswith('(') or t.startswith('- '):
                continue
            m = END_RE.search(t)
            if not m:
                continue
            # टीकाकार के अपने मङ्गल-पद्य और प्रस्ताव-समापन के वाक्य कारिका नहीं हैं
            if (vol == 1 and num == 1) or 'इति ' in t[:12] and 'प्रस्तावः' in t:
                continue
            n = int(m.group(1).translate(DEV))
            # पीछे चलकर पद्य का आरम्भ खोजिए — "[" वाली पंक्ति, या खाली पंक्ति/पिछला पद्य-अन्त
            verse = [t[:m.end()]]
            bracket = t.lstrip('*').lstrip().startswith('[') or re.match(r'^[०-९0-9 ]*\*?\*?\s*\[', t)
            j = i - 1
            while not bracket and j >= 0 and len(verse) < 4:
                p = lines[j].strip()
                if not p or END_RE.search(p) or p.startswith('('):
                    break
                verse.insert(0, p)
                if re.match(r'^[०-९0-9 ]*\*?\*?\s*\[', p):
                    bracket = True
                    break
                j -= 1
            # पद्य का भीतरी "[" (एक-पंक्ति पद्य) — जैसे "… इत्यादि। [ कार्यकारणता … ॥३॥ ]"
            first = verse[0]
            k = first.rfind('[ ') if not bracket else -1
            if k > 0 and '॥' not in first[:k]:
                verse[0] = first[k:]
                bracket = True
            prev = last.get(pr, 0)
            ok = (prev < n <= prev + 3) or (bracket and n == prev and n > 0)
            text = [clean(v) for v in verse]
            text = [x for x in text if x]
            # पद्य के बीच-बीच की टीका-पंक्ति (लम्बा गद्य) — पद्य नहीं
            if any(len(x) > 140 and '।' not in x for x in text) and not bracket:
                ok = False
            # कारिका-अंश से पहले की टीका-पंक्ति ("यदि नाम", "तदेतदस्मिन्नेकान्ते–")
            while len(text) > 1 and (text[0].endswith(('–', '—')) or text[0] in ('यदि नाम', 'यदि पुनः')):
                text.pop(0)
            if (vol, num) in OVERRIDE:
                text = OVERRIDE[(vol, num)]
            if (vol, num) in ACCEPT:          # छपा अंक क्रम से हटकर, पर पद्य कारिका ही है
                rows.append((vol, num, pr, ACCEPT[(vol, num)], text, n))
                continue
            if ok:
                last[pr] = n
                rows.append((vol, num, pr, n, text, n))
            else:
                rejected.append((vol, num, pr, n, prev, ' / '.join(text)[:150]))
    if review:
        for r in rejected:
            print('REJ', r)
    return rows


def halves(text):
    """पद्य को श्लोकार्धों में बाँटिए: हर छपी पंक्ति एक अर्ध; एक-पंक्ति पद्य "।" पर।"""
    out = []
    for x in text:
        x = END_RE.sub('', x).strip(' ।॥,')
        parts = [p.strip(' ,') for p in re.split(r'।', x) if p.strip(' ,')]
        for p in parts:   # लम्बे छन्द की दो चरण एक पंक्ति में ", " से जुड़े हों तो अलग
            out.extend(q.strip(' ,') for q in (p.split(', ') if len(p) > 60 else [p]) if q.strip(' ,'))
    return [p for p in out if len(re.sub(r'[^अ-ह]', '', p)) >= 3]


def write_51(rows):
    entries = []
    for vol, num, pr, n, text, printed in rows:
        k = f'{pr}.{n}' if n == printed else f'{pr}.{n} (छपा अंक {printed})'
        for h in halves(text):
            entries.append((sort_key(h), h, k, f'भाग {vol} · §{num}'))
    entries.sort(key=lambda e: e[0])
    got = {}
    for vol, num, pr, n, *_ in rows:
        got.setdefault(pr, set()).add(n)
    miss = []
    for pr in sorted(got):
        miss += [f'{pr}.{n}' for n in range(1, max(got[pr]) + 1) if n not in got[pr]]
    md = ['# परिशिष्ट 1 — मूल-कारिकार्ध अनुक्रमणी', '',
          'श्री भट्ट अकलङ्कदेव की मूल कारिकाओं के श्लोकार्ध (छपी पंक्ति-क्रम से) अकारादि क्रम में। '
          '"प्रस्ताव.कारिका" में कारिका-संख्या वही है जो मूल पाठ में छपी है; § इस व्याख्या के अनुच्छेद हैं — '
          'प्रस्ताव 1–5 के § भाग 1 में, प्रस्ताव 6–12 के § इस भाग में।', '',
          'लम्बे छन्द की कारिकाओं में प्रत्येक चरण अलग पंक्ति है। जहाँ मूल प्रति में पाठ खण्डित है, वहाँ अंश '
          'अधूरा ही दिया गया है; 6.19 और 6.20 में कारिका टीका-वाक्य से अलग नहीं होती, इसलिए वहाँ केवल पहचाना '
          'जा सकने वाला अंश है। क्रम-संख्या ' + ', '.join(miss) + ' की कारिकाएँ इस पाठ में अलग अंक सहित नहीं मिलतीं '
          '(9.24–9.25 सम्भवतः मुद्रित पृष्ठ 636–637 पर थीं, जो उपलब्ध प्रति में नहीं हैं)।', '',
          '| कारिकार्ध | प्रस्ताव.कारिका | अनुच्छेद |', '|---|---|---|']
    for _, h, k, s in entries:
        md.append(f'| {h.replace("|", "/")} | {k} | {s} |')
    (OUT / '51_karika_anukram.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    return len(rows), len(entries)


# ---------------------------------------------------------------- 52 उद्धरण
Q_RE = re.compile(r'["“]([^"“”]{3,900})["”]\s*(\[[^\]]{1,70}\])?')
HINDI_NOTE = re.compile(r'\[[^\[\]]*(?: है| हैं| के | की | में | का | से )[^\[\]]*\]')
PH_RE = re.compile(r'\[उद्धरण\s*[—–-]\s*([^\]]+)\]')


def quotations():
    quotes, holders = {}, {}
    for vol, num, lines in mula_sections():
        s = joined(lines)
        s = HINDI_NOTE.sub(' ', s)              # व्याख्याकार की कोष्ठक-टिप्पणियाँ
        for m in Q_RE.finditer(s):
            body = clean(m.group(1))
            body = re.sub(r'^[^अ-ह\[(]+', '', body).strip()
            if len(re.sub(r'[^ऀ-ॿ]', '', body)) < 6:
                continue
            src = norm_src((m.group(2) or '').strip('[] '))
            if 'सिद्धिवि' in src:          # मूल ग्रन्थ का ही उद्धरण — परिशिष्ट 1 में है
                continue
            if src and not re.search(r'[०-९0-9]|०|॰', src):
                src = src if len(src) < 40 else ''
            words = body.split()
            short = ' '.join(words[:10]) + (' …' if len(words) > 10 else '')
            short = short.replace('|', '/')
            key = ' '.join(words[:6])
            e = quotes.setdefault(key, {'text': short, 'src': set(), 'at': []})
            if src:
                e['src'].add(src)
            ref = (vol, num)
            if ref not in e['at']:
                e['at'].append(ref)
        for m in PH_RE.finditer(s):
            name = re.sub(r'\s+', ' ', m.group(1)).strip()
            name = re.split(r',\s*(?:पाठ|स्रोत|सन्दर्भ)', name)[0].strip()
            if ';' in name or name.startswith('('):   # तुलनात्मक स्थल-सूची, उद्धरण नहीं
                continue
            holders.setdefault(name, [])
            if (vol, num) not in holders[name]:
                holders[name].append((vol, num))
    return quotes, holders


def joined(lines):
    """मूल-पाठ की पंक्तियाँ एक धारा में — पृष्ठ-सूचक छोड़कर, पंक्त्यन्त के "-" पर शब्द जोड़कर।"""
    out = ''
    for l in lines:
        t = l.strip()
        if not t or re.match(r'^\(पृष्ठ', t):
            continue
        out = out[:-1] + t if out.endswith('-') else (out + ' ' + t if out else t)
    return out


def norm_src(src):
    src = re.sub(r'\s+', ' ', src).strip()
    src = re.sub(r'([०॰])\s*(?=\S)', r'\1 ', src)
    return src


def fmt_refs(refs):
    out = []
    for v in (1, 2):
        ns = [n for vv, n in refs if vv == v]
        if ns:
            out.append(f'भाग {v}: ' + ', '.join(f'§{n}' for n in ns))
    return '; '.join(out)


def write_52(quotes, holders):
    items = sorted(quotes.values(), key=lambda e: sort_key(e['text']))
    md = ['# परिशिष्ट 2 — टीका में उद्धृत श्लोक और वाक्य', '',
          'श्री अनन्तवीर्याचार्य की टीका में उद्धृत पद्य और वाक्य (पूर्वपक्ष के उद्धृत कथन सहित), आरम्भ के शब्दों से '
          'अकारादि क्रम में। स्रोत वहीं दिया है जहाँ मूल पाठ में उद्धरण के साथ उसका निर्देश छपा है; बाकी स्थान खाली है। '
          '§ इस व्याख्या के अनुच्छेद हैं — "भाग 1" के § पहले भाग में, "भाग 2" के इस भाग में।', '',
          '## (क) उद्धरण — अकारादि क्रम', '',
          '| उद्धरण (आरम्भ) | स्रोत-निर्देश | अनुच्छेद |', '|---|---|---|']
    for e in items:
        md.append(f"| {e['text']} | {'; '.join(sorted(e['src']))} | {fmt_refs(e['at'])} |")
    md += ['', '## (ख) स्रोत-निर्देश, जिनका पाठ मूल में उद्धृत नहीं', '',
           'कुछ स्थलों पर मूल पाठ में उद्धरण का केवल स्रोत-संकेत है, पाठ नहीं। वे स्रोत-क्रम से:', '',
           '| स्रोत | अनुच्छेद |', '|---|---|']
    for name in sorted(holders, key=sort_key):
        md.append(f'| {name.replace("|", "/")} | {fmt_refs(holders[name])} |')
    (OUT / '52_uddharan_suchi.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    return len(items), len(holders)


# ---------------------------------------------------------------- 53 नाम
# (सूची-शीर्ष, वर्ग, खोज-रूप) — खोज-रूप मूल-पाठ के शब्दों के आरम्भ से मिलाए जाते हैं।
NAMES = [
    # आचार्य / ग्रन्थकार
    ('श्री समन्तभद्र स्वामी', 'आचार्य', ['समन्तभद्र']),
    ('श्री सिद्धसेन स्वामी', 'आचार्य', ['सिद्धसेन']),
    ('श्री पूज्यपाद (देवनन्दि) स्वामी', 'आचार्य', ['पूज्यपाद', 'देवनन्दि']),
    ('श्री पात्रकेसरी स्वामी', 'आचार्य', ['पात्रकेसरि', 'पात्रकेशरि', 'पात्रस्वामि']),
    ('श्री भट्ट अकलङ्कदेव', 'आचार्य', ['अकलङ्क', 'अकलंक']),
    ('श्री रविभद्र स्वामी', 'आचार्य', ['रविभद्र']),
    ('श्री अनन्तवीर्य स्वामी', 'आचार्य', ['अनन्तवीर्य']),
    ('धर्मकीर्ति', 'ग्रन्थकार', ['धर्मकीर्ति']),
    ('दिङ्नाग', 'ग्रन्थकार', ['दिङ्नाग', 'दिग्नाग']),
    ('धर्मोत्तर', 'ग्रन्थकार', ['धर्मोत्तर']),
    ('प्रज्ञाकरगुप्त', 'ग्रन्थकार', ['प्रज्ञाकर']),
    ('अर्चट', 'ग्रन्थकार', ['अर्चट']),
    ('कर्णकगोमि', 'ग्रन्थकार', ['कर्णक']),
    ('शान्तभद्र', 'ग्रन्थकार', ['शान्तभद्र']),
    ('देवेन्द्रबुद्धि', 'ग्रन्थकार', ['देवेन्द्रबुद्धि']),
    ('शान्तरक्षित', 'ग्रन्थकार', ['शान्तरक्षित']),
    ('कुमारिल', 'ग्रन्थकार', ['कुमारिल']),
    ('प्रभाकर', 'ग्रन्थकार', ['प्रभाकर']),
    ('शबर', 'ग्रन्थकार', ['शबर']),
    ('मण्डनमिश्र', 'ग्रन्थकार', ['मण्डन']),
    ('भर्तृहरि', 'ग्रन्थकार', ['भर्तृहरि']),
    ('जैमिनि', 'ग्रन्थकार', ['जैमिनि']),
    ('अक्षपाद', 'ग्रन्थकार', ['अक्षपाद']),
    ('वात्स्यायन', 'ग्रन्थकार', ['वात्स्यायन']),
    ('उद्योतकर', 'ग्रन्थकार', ['उद्योतकर']),
    ('कणाद', 'ग्रन्थकार', ['कणाद', 'काणाद']),
    ('प्रशस्तपाद', 'ग्रन्थकार', ['प्रशस्तपाद', 'प्रशस्तकर']),
    ('कपिल', 'ग्रन्थकार', ['कपिल', 'कापिल']),
    ('ईश्वरकृष्ण', 'ग्रन्थकार', ['ईश्वरकृष्ण']),
    ('बृहस्पति', 'ग्रन्थकार', ['बृहस्पति', 'बार्हस्पत्य']),
    ('सुगत / बुद्ध (शुद्धोदनि)', 'ग्रन्थकार', ['सुगत', 'शुद्धोदनि', 'शौद्धोदनि']),
    # ग्रन्थ
    ('प्रमाणवार्तिक', 'ग्रन्थ', ['प्रमाणवार्तिक', 'वार्तिक']),
    ('प्रमाणविनिश्चय', 'ग्रन्थ', ['प्रमाणविनिश्चय']),
    ('न्यायबिन्दु', 'ग्रन्थ', ['न्यायबिन्दु']),
    ('हेतुबिन्दु', 'ग्रन्थ', ['हेतुबिन्दु']),
    ('न्यायविनिश्चय', 'ग्रन्थ', ['न्यायविनिश्चय']),
    ('प्रमाणसंग्रह', 'ग्रन्थ', ['प्रमाणसंग्रह', 'प्रमाणसङ्ग्रह']),
    ('लघीयस्त्रय', 'ग्रन्थ', ['लघीयस्त्रय']),
    ('तत्त्वार्थ', 'ग्रन्थ', ['तत्त्वार्थसूत्र', 'तत्त्वार्थवार्तिक', 'तत्त्वार्थभाष्य']),
    ('आप्तमीमांसा / देवागम', 'ग्रन्थ', ['आप्तमीमांसा', 'देवागम']),
    ('स्वयम्भूस्तोत्र', 'ग्रन्थ', ['स्वयम्भूस्तोत्र', 'स्वयंभूस्तोत्र', 'बृहत्स्वयम्भू']),
    ('युक्त्यनुशासन', 'ग्रन्थ', ['युक्त्यनुशासन']),
    ('जैनेन्द्र (व्याकरण)', 'ग्रन्थ', ['जैनेन्द्र', 'जेनेन्द्र']),
    ('श्लोकवार्तिक', 'ग्रन्थ', ['श्लोकवार्तिक', 'मीमांसाश्लोकवार्तिक']),
    ('वाक्यपदीय', 'ग्रन्थ', ['वाक्यपदीय']),
    ('न्यायसूत्र', 'ग्रन्थ', ['न्यायसूत्र']),
    ('वैशेषिकसूत्र', 'ग्रन्थ', ['वैशेषिकसूत्र']),
    ('सांख्यकारिका', 'ग्रन्थ', ['सांख्यकारिका']),
    ('पिटकत्रय', 'ग्रन्थ', ['पिटकत्रय', 'त्रिपिटक']),
    ('वेद', 'ग्रन्थ', ['वेदाः', 'वेदस्य', 'वेदे ', 'वेदं', 'वेदान् ', 'वेदात्', 'वेदो', 'वेदेन', 'वेदानां',
                        'वेदानाम्', 'वेदवाक्य', 'वेदप्रामाण्य', 'वेदार्थ', 'वेदापौरुषेय', 'वेदाध्ययन', 'ऋग्वेद']),
    # मत
    ('सौगत / बौद्ध', 'मत', ['सौगत', 'बौद्ध', 'ताथागत', 'शाक्य']),
    ('योगाचार / विज्ञानवादी', 'मत', ['योगाचार', 'विज्ञानवादि']),
    ('सौत्रान्तिक', 'मत', ['सौत्रान्तिक']),
    ('वैभाषिक', 'मत', ['वैभाषिक']),
    ('माध्यमिक / शून्यवादी', 'मत', ['माध्यमिक', 'शून्यवादि']),
    ('नैयायिक', 'मत', ['नैयायिक']),
    ('वैशेषिक', 'मत', ['वैशेषिक']),
    ('यौग', 'मत', ['यौग']),
    ('मीमांसक', 'मत', ['मीमांसक']),
    ('भाट्ट', 'मत', ['भाट्ट']),
    ('प्राभाकर', 'मत', ['प्राभाकर']),
    ('सांख्य', 'मत', ['सांख्य', 'साङ्ख्य']),
    ('चार्वाक / लौकायतिक', 'मत', ['चार्वाक', 'लौकायतिक', 'लोकायत']),
    ('ब्रह्मवादी / वेदान्ती', 'मत', ['ब्रह्मवादि', 'ब्रह्माद्वैत', 'वेदान्त', 'औपनिषद']),
    ('शब्दाद्वैतवादी / वैयाकरण', 'मत', ['शब्दाद्वैत', 'वैयाकरण', 'शब्दब्रह्म']),
    ('स्याद्वादी', 'मत', ['स्याद्वादि', 'स्याद्वादिन']),
]
# खोज-रूप जिनके बाद ये अक्षर आएँ तो वह दूसरा शब्द है (जैसे "वेद" के बाद "न" = वेदन)
BAD_NEXT = {'यौग': 'प', 'शबर': 'ल', 'वार्तिक': 'ाल', 'सुगत': 'ि',
            'कपिल': '', 'प्रभाकर': 'गुप', 'मण्डन': ''}
BOUND = r'(?:^|[\s\-–—(\["\'“‘*।,;?:])'


def names():
    found = {n[0]: [] for n in NAMES}
    for vol, num, lines in mula_sections():
        s = joined(lines).replace('**', '')
        s = HINDI_NOTE.sub(" ", s)
        s = PH_RE.sub(' ', s)                                # स्रोत-संकेत सम्पादकीय हैं
        s = re.sub(r'\[[^\]]*[०-९0-9॰०][^\]]*\]', ' ', s)    # [प्र० वा० …], पत्र-संख्या
        s = re.sub(r'(?<=[क-ह]) (?=[क-ह][ा-ौ]? )', '', s)  # "दि ग् ना गा" जैसे विरल-अक्षर
        for title, cat, forms in NAMES:
            for fm in forms:
                for m in re.finditer(BOUND + re.escape(fm), s):
                    nxt = s[m.end():m.end() + 1]
                    if fm in BAD_NEXT and nxt and nxt in BAD_NEXT[fm]:
                        continue
                    if (vol, num) not in found[title]:
                        found[title].append((vol, num))
                    break
    return found


def write_53(found):
    md = ['# परिशिष्ट 3 — टीका में निर्दिष्ट आचार्य, ग्रन्थकार, ग्रन्थ और मत', '',
          'मूल पाठ (कारिका और टीका) में जिन आचार्यों, ग्रन्थकारों, ग्रन्थों और दार्शनिक मतों का नाम आता है, वे '
          'वर्ग-वार; प्रत्येक के आगे वे अनुच्छेद जहाँ नाम (किसी विभक्ति-रूप में) आया है। § इस व्याख्या के हैं — '
          '"भाग 1" के § पहले भाग में, "भाग 2" के इस भाग में। उद्धरणों के साथ छपे स्रोत-संकेत यहाँ नहीं गिने गए।', '']
    total = 0
    for cat, head in [('आचार्य', 'जैन आचार्य'), ('ग्रन्थकार', 'अन्य ग्रन्थकार'),
                      ('ग्रन्थ', 'ग्रन्थ'), ('मत', 'दार्शनिक मत')]:
        md += [f'## {head}', '', '| नाम | अनुच्छेद |', '|---|---|']
        for title, c, _ in NAMES:
            if c != cat or not found[title]:
                continue
            total += 1
            md.append(f'| {title} | {fmt_refs(found[title])} |')
        md.append('')
    (OUT / '53_nyay_nama_suchi.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    return total


if __name__ == '__main__':
    review = '--review' in sys.argv
    OUT.mkdir(exist_ok=True)
    rows = karikas(review)
    nk, nh = write_51(rows)
    nq, nph = write_52(*quotations())
    nn = write_53(names())
    per = {}
    for vol, num, pr, n, *_ in rows:
        per[pr] = per.get(pr, 0) + 1
    print(f'51: {nk} कारिकाएँ, {nh} अर्ध; प्रस्ताव-वार {dict(sorted(per.items()))}')
    print(f'52: {nq} उद्धरण, {nph} पाठ-रहित स्रोत')
    print(f'53: {nn} नाम')
