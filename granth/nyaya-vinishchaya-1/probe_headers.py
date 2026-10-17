# -*- coding: utf-8 -*-
"""कई स्कैन-पृष्ठों की शीर्ष-पट्टी एक चादर में जोड़कर दीजिए — मुद्रित संख्या पढ़ने के लिए।

चलाइए:
    python probe_headers.py 520 521 522 523 524        # ये स्कैन-पृष्ठ
    python probe_headers.py --range 60 80              # यह परास
    python probe_headers.py --range 60 80 --step 5

यह **स्कैन-क्रमांक** लेता है, मुद्रित नहीं — पृष्ठ-मानचित्र अभी बन ही रहा है।

## यह क्यों चाहिए

इस ग्रन्थ का स्कैन धुँधला है और `मुद्रित = स्कैन − अन्तर` का अन्तर एक-सा नहीं है:
भाग 1 में अब तक 67 → 65 → 64 मिला है, अर्थात् प्रति में कहीं पृष्ठ नहीं हैं।
छेद कहाँ है यह केवल पन्ने-दर-पन्ने शीर्ष पढ़कर ही पक्का होता है, और शीर्ष सीधे
स्कैन से नहीं खुलता — विषमता सुधारनी पड़ती है। जोड़-घटाव से अनुमान मत लगाइए;
प्रमेयकमल में वही अनुमान दो बार ग़लत पन्ना भेज चुका है।

सम (बायाँ) पृष्ठ पर मुद्रित संख्या **बाएँ** छपती है, विषम पर **दाएँ** —
इसलिए पूरी चौड़ाई रखिए, किनारा मत काटिए।
"""
import pathlib
import sys

import fitz
from PIL import Image, ImageOps

HERE = pathlib.Path(__file__).resolve().parent
PDF = next(iter(sorted((HERE / "mool").glob("*.pdf"))))
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
    lo, hi = int(argv[i + 1]), int(argv[i + 2])
    step = int(argv[argv.index("--step") + 1]) if "--step" in argv else 1
    nums = list(range(lo, hi + 1, step))
else:
    nums = [int(a) for a in argv if not a.startswith("--")]
if not nums:
    sys.exit(__doc__)

OUT.mkdir(parents=True, exist_ok=True)
doc = fitz.open(PDF)
strips = []
for n in nums:
    if not 1 <= n <= doc.page_count:
        continue
    pm = doc[n - 1].get_pixmap(dpi=200)
    tmp = OUT / ("_t%03d.png" % n)
    pm.save(tmp)
    im = ImageOps.autocontrast(Image.open(tmp).convert("L"))
    # शीर्ष हर पन्ने पर एक ही ऊँचाई पर नहीं है (स्कैन टेढ़ा है), इसलिए ऊपर का
    # 13% लीजिए — इससे कम लेने पर आधे पन्नों का शीर्ष कट गया था।
    s = im.crop((0, 0, im.width, int(im.height * 0.13)))
    s = s.resize((int(s.width * 0.8), int(s.height * 0.8)))
    strips.append((n, s))
    tmp.unlink()

W = max(s.width for _, s in strips)
H = sum(s.height + 6 for _, s in strips)
sheet = Image.new("L", (W, H), 255)
y = 0
for n, s in strips:
    sheet.paste(s, (0, y))
    y += s.height + 6
name = OUT / ("hdr_%d_%d.png" % (nums[0], nums[-1]))
sheet.save(name)
print("क्रम (ऊपर से नीचे): %s" % ", ".join(str(n) for n in nums))
print("चादर: %s" % name)
