# -*- coding: utf-8 -*-
"""केवल शीर्ष के दोनों कोने — मुद्रित पृष्ठ-संख्या निश्चित रूप से पढ़ने के लिए।

चलाइए:
    python probe_corners.py 67 68 80 90
    python probe_corners.py --range 95 105

`probe_headers.py` पूरी शीर्ष-पंक्ति दिखाता है, जो विषय जानने के लिए अच्छा है;
पर उस आकार में इस स्कैन के **३ और ५, ४ और ५, ० और ८ एक-से दिखते हैं** और
मैं दो बार ग़लत पढ़ चुका हूँ (स्कैन 100 को पहले 35 पढ़ा, वह 33 निकला)। यह
केवल कोने काटकर बड़े रखता है, जिससे अङ्क पर सन्देह न रहे।

सम (बायाँ) पृष्ठ पर संख्या बाएँ कोने में, विषम पर दाएँ — इसीलिए दोनों कोने
साथ-साथ दिखाए जाते हैं। दूसरा कोना सूत्र-सन्दर्भ `[ १।१२२` देता है, जो
अनुच्छेद-विभाजन के काम आएगा।
"""
import pathlib
import sys

import fitz
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
PDF = next(iter(sorted((HERE / "mool").glob("*.pdf"))))
# दोनों भागों की चादरें अलग फ़ोल्डर में जाएँ, वरना एक ही नाम की फ़ाइल
# दूसरे भाग की चादर पर लिख देती है और ग़लत भाग का पन्ना पढ़ा जाता है।
OUT = (pathlib.Path(
    r"C:\Users\naman\AppData\Local\Temp\claude"
    r"\e--Projects-JinAagam\447635f5-72e1-4efb-9641-f5c3a36d91d3"
    r"\scratchpad") / ("nv" + HERE.name[-1] + "_headers"))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

argv = sys.argv[1:]
if "--range" in argv:
    i = argv.index("--range")
    nums = list(range(int(argv[i + 1]), int(argv[i + 2]) + 1))
else:
    nums = [int(a) for a in argv if not a.startswith("--")]
if not nums:
    sys.exit(__doc__)

try:
    FONT = ImageFont.truetype("arial.ttf", 44)
except OSError:
    FONT = ImageFont.load_default()

OUT.mkdir(parents=True, exist_ok=True)
doc = fitz.open(PDF)
rows = []
for n in nums:
    if not 1 <= n <= doc.page_count:
        continue
    tmp = OUT / ("_c%d.png" % n)
    doc[n - 1].get_pixmap(dpi=400).save(tmp)
    im = ImageOps.autocontrast(Image.open(tmp).convert("L"))
    # शीर्ष-पंक्ति पृष्ठ की ऊँचाई के 3.5% से 10.5% के बीच बैठती है। इससे ऊपर
    # काटने पर केवल स्कैन का काला किनारा आता है — एक बार वही हुआ था।
    band = im.crop((0, int(im.height * 0.035), im.width, int(im.height * 0.105)))
    left = band.crop((int(band.width * 0.06), 0, int(band.width * 0.34), band.height))
    right = band.crop((int(band.width * 0.66), 0, int(band.width * 0.94), band.height))
    # स्कैन-क्रमांक हर पंक्ति पर छापिए। बिना इसके, जिस पन्ने की पट्टी खाली आती है
    # उसकी पंक्ति गिनती से छूट जाती है और आगे की सब पंक्तियाँ एक-एक खिसक जाती हैं —
    # ऐसे ही एक बार अन्तर 65/66/67 के बीच डोलता दिखा था, जो असम्भव है।
    strip = Image.new("L", (160 + left.width + right.width + 60, left.height), 255)
    ImageDraw.Draw(strip).text((12, max(0, left.height // 2 - 20)),
                               "%d" % n, fill=0, font=FONT)
    strip.paste(left, (160, 0))
    strip.paste(right, (160 + left.width + 60, 0))
    rows.append((n, strip))
    tmp.unlink()

W = max(s.width for _, s in rows)
H = sum(s.height + 16 for _, s in rows)
sheet = Image.new("L", (W, H), 255)
y = 0
for n, s in rows:
    sheet.paste(s, (0, y))
    y += s.height + 16
name = OUT / ("corner_%d_%d.png" % (nums[0], nums[-1]))
sheet.save(name)
print("क्रम (ऊपर से नीचे): %s" % ", ".join(str(n) for n in nums))
print("हर पंक्ति में: बायाँ कोना | दायाँ कोना")
print("चादर: %s" % name)
