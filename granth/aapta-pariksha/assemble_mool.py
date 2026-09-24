# -*- coding: utf-8 -*-
"""mool/b*.md को मुद्रित-पृष्ठ क्रम में जोड़कर पुस्तक-योग्य markdown बनाता है।
   पृष्ठ-चिह्न वाक्य के भीतर भी हो सकता है, अतः विभाजन regex-split से होता है।
   प्रयोग: python assemble_mool.py
"""
import glob, io, os, re

PAGE = re.compile(r'<!--\s*मुद्रित पृष्ठ\s*(\d+)(?:\s*·\s*(.*?))?\s*-->')
SEC  = re.compile(r'^§\s*(\d+)\.?\s')

PRAKARAN = [
    (0,   "[ 1. परमेष्ठि-गुण-स्तोत्र — मङ्गलाचरण (कारिका 1) ]"),
    (1,   "[ 2. परमेष्ठि-गुण-स्तोत्र का प्रयोजन — मङ्गल की निरुक्ति एवं सार्थकता (कारिका 2–5) ]"),
    (23,  "[ 3. ईश्वर-परीक्षा — वैशेषिकाभिमत ईश्वर के सर्वज्ञत्व एवं मोक्षमार्ग-प्रणेतृत्व का निरास (कारिका 6–79) ]"),
    (186, "[ 4. कपिल-परीक्षा — सांख्याभिमत कपिल एवं प्रधान का निरास (कारिका 80–83) ]"),
    (196, "[ 5. सुगत-परीक्षा — सौगत, सौत्रान्तिक एवं योगाचार मतों की समीक्षा (कारिका 84–85) ]"),
    (235, "[ 6. परमपुरुष-परीक्षा — ब्रह्माद्वैत एवं चित्राद्वैत का निरास (कारिका 86) ]"),
    (244, "[ 7. अर्हत्-सर्वज्ञ-सिद्धि — बाधकाभाव से सर्वज्ञ-सिद्धि; भट्ट के सर्वज्ञाभाववाद का निराकरण (कारिका 87–109) ]"),
    (289, "[ 8. अर्हत्-कर्मभूभृत्-भेतृत्व-सिद्धि — संवर-निर्जरा द्वारा कर्म-पर्वतों का भेदन (कारिका 110–115) ]"),
    (302, "[ 9. अर्हत्-मोक्षमार्ग-नेतृत्व-सिद्धि — मोक्ष एवं मोक्षमार्ग का स्वरूप (कारिका 116–118) ]"),
    (320, "[ 10. अर्हत्-वन्द्यत्व-सिद्धि — 'वन्दे तद्गुणलब्धये' का व्याख्यान (कारिका 119–121) ]"),
    (325, "[ 11. उपसंहार — ग्रन्थ-समापन एवं टीका-प्रशस्ति (कारिका 122–124) ]"),
]

blocks = {}
for f in sorted(glob.glob(os.path.join('mool', 'b*.md'))):
    parts = PAGE.split(io.open(f, encoding='utf-8').read())
    i = 1
    while i + 2 <= len(parts):
        pg = int(parts[i]); blocks[pg] = blocks.get(pg, '') + parts[i + 2]; i += 3

out, done = [], set()
out.append("# " + PRAKARAN[0][1]); done.add(0)
for pg in sorted(blocks):
    out.append("<!--PG %d-->" % pg)
    for line in blocks[pg].splitlines():
        m = SEC.match(line)
        if m:
            n = int(m.group(1))
            for start, title in PRAKARAN:
                if n == start and start not in done:
                    out += ["", "# " + title, ""]; done.add(start)
        out.append(line)
    out.append("")

txt = re.sub(chr(10)+"{3,}", chr(10)*2, chr(10).join(out))
os.makedirs(os.path.join('mool_book', 'parts'), exist_ok=True)
io.open(os.path.join('mool_book', 'parts', '01_mool.md'), 'w', encoding='utf-8').write(txt)
print("पृष्ठ जोड़े:", len(blocks), "/353 | प्रकरण:", len(done), "/", len(PRAKARAN), "| वर्ण:", len(txt))
miss = sorted(set(range(1, 354)) - set(blocks))
if miss: print("!! लुप्त पृष्ठ:", miss)
