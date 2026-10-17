# -*- coding: utf-8 -*-
"""पास 1 कहाँ पहुँचा — एक नज़र में।  चलाइए: python status.py

यह `parts/*.md` से स्वयं गिनता है, किसी हाथ से लिखी सूची से नहीं — इसलिए यह
पुराना नहीं पड़ता। `progress.md` की स्थिति-तालिका इसी से भरिए।


और 464, 465, 521 प्रति में ही नहीं हैं — दोनों छेद गिनती से बाहर रखे जाते हैं।
"""
import glob, io, re, sys, pathlib
try: sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError): pass

HERE = pathlib.Path(__file__).resolve().parent
ABSENT = {162, 163}             # प्रति में नहीं
LAST = 369                      # भाग 2 का अन्तिम मुद्रित पृष्ठ
RESERVED = set()                # यहाँ कुछ रोका नहीं

pages, secs, unclear, files = {}, 0, 0, 0
for f in sorted(glob.glob(str(HERE / "parts" / "batch*.md"))):
    t = io.open(f, encoding="utf-8").read()
    files += 1
    secs += len(re.findall(r"^§\s*\d+\s*—", t, re.M))
    unclear += t.count("[अस्पष्ट]")
    for p in re.findall(r"^\(पृष्ठ (\d+)\)", t, re.M):
        pages.setdefault(int(p), pathlib.Path(f).name)

want = [p for p in range(1, LAST + 1) if p not in ABSENT and p not in RESERVED]
done = [p for p in want if p in pages]
left = [p for p in want if p not in pages]

print("बैच फ़ाइलें : %d" % files)
print("§          : %d" % secs)
print("[अस्पष्ट]   : %d  (प्रति पृष्ठ औसत %.0f)"
      % (unclear, unclear / max(len(done), 1)))
print("पृष्ठ       : %d / %d ढके  (%.0f%%)"
      % (len(done), len(want), 100.0 * len(done) / len(want)))

# छेद — ढके हुए सबसे आगे के पृष्ठ **से पहले** के, यानी सचमुच छूटे हुए
if done:
    holes = [p for p in left if p < max(done)]
    print("बीच के छेद : %s" % (holes if holes else "कोई नहीं"))
    if holes:
        print("              (चलते हुए बैच की परास भी यहाँ दिखती है — "
              "वह छेद नहीं। पहले देख लीजिए कि कोई बैच उस परास पर चल रहा है या नहीं।)")
    print("आगे बाक़ी   : मुद्रित %d से %d  (%d पृष्ठ, ~%d बैच)"
          % (max(done) + 1, LAST, len([p for p in left if p > max(done)]),
             round(len([p for p in left if p > max(done)]) / 6.0)))

