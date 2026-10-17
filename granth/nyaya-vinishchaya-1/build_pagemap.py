# -*- coding: utf-8 -*-
"""pagemap.json बनाइए — जाँचे हुए खण्डों से, जोड़-घटाव के एक नियम से नहीं।

चलाइए:  python build_pagemap.py          # जाँच कर के छापिए
        python build_pagemap.py --write  # pagemap.json लिखिए

## इस ग्रन्थ का अन्तर एक-सा नहीं है

भाग 1 में `मुद्रित = स्कैन − अन्तर` का अन्तर **चार बार बदलता है**, और चारों
बदलाव शीर्ष-कोने पढ़कर एक-एक पन्ने पर पक्के किए गए हैं (`probe_corners.py`):

| स्कैन | मुद्रित | अन्तर | क्यों बदला |
|---|---|---|---|
| 67–95 | 1–29 | 66 | — (स्कैन 67 पर शीर्ष नहीं छपा; ग्रन्थ का पहला पन्ना) |
| 96 | — | — | **मुद्रित 29 दुबारा स्कैन हुआ** — वही पाठ, वही शीर्ष |
| 97–530 | 30–463 | 67 | ऊपर की दुहरी प्रति के कारण |
| 531–585 | 466–520 | 65 | **मुद्रित 464, 465 प्रति में नहीं** |
| 586–609 | 522–545 | 64 | **मुद्रित 521 प्रति में नहीं** |

अर्थात् मुद्रित 545 पृष्ठों में से **464, 465, 521 उपलब्ध नहीं** — 542 ही हैं।

## यह सावधानी क्यों

प्रमेयकमल में यही अन्तर तीन बार बदला था और एक-सूत्र मान लेने से दो बार ग़लत
पन्ना निकला। यहाँ पहली जाँच में ही अन्तर 67 मान लिया गया था — वह आरम्भ के
उनतीस पन्नों पर ग़लत होता। अङ्क भी धोखा देते हैं: इस स्कैन में ३/५, ४/५ और
०/८ एक-से दिखते हैं, और स्कैन 100 पहले 35 पढ़ा गया था, निकला 33।

**कहीं मिलान न बैठे तो वहीं रुकिए।** हाथ से जोड़-घटाव करके आगे मत बढ़िए।
"""
import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent

# (स्कैन-आरम्भ, स्कैन-अन्त, अन्तर) — हर खण्ड कोने पढ़कर पक्का किया हुआ
RUNS = [(67, 95, 66), (97, 530, 67), (531, 585, 65), (586, 609, 64)]
DUPLICATE = {96: "मुद्रित 29 की दूसरी प्रति"}
MISSING = [464, 465, 521]

# जाँच-बिन्दु — आँख से पढ़े हुए; इनमें से एक भी न बैठे तो नक़्शा ग़लत है
CHECKS = {67: 1, 68: 2, 81: 15, 95: 29, 97: 30, 98: 31, 100: 33, 140: 73,
          180: 113, 200: 133, 260: 193, 300: 233, 350: 283, 420: 353,
          470: 403, 505: 438, 520: 453, 530: 463, 531: 466, 585: 520,
          586: 522, 595: 531, 609: 545}

scan_to_printed = {}
for lo, hi, off in RUNS:
    for s in range(lo, hi + 1):
        scan_to_printed[s] = s - off

bad = [(s, p, scan_to_printed.get(s)) for s, p in sorted(CHECKS.items())
       if scan_to_printed.get(s) != p]
printed = sorted(scan_to_printed.values())
gaps = [p for p in range(printed[0], printed[-1] + 1) if p not in set(printed)]

print("स्कैन पृष्ठ (मुख्य पाठ): %d" % len(scan_to_printed))
print("मुद्रित परास            : %d–%d" % (printed[0], printed[-1]))
print("दुहरी प्रति             : %s" % ", ".join(
    "स्कैन %d (%s)" % (k, v) for k, v in DUPLICATE.items()))
print("प्रति में अनुपलब्ध      : %s" % ", ".join(str(g) for g in gaps))
print("जाँच-बिन्दु             : %d, न बैठे %d" % (len(CHECKS), len(bad)))
for s, want, got in bad:
    print("   ✗ स्कैन %d: पढ़ा %s, नक़्शा कहता है %s" % (s, want, got))

if gaps != MISSING:
    sys.exit("\nरुकिए — अनुपलब्ध पृष्ठ %s निकले, अपेक्षित थे %s" % (gaps, MISSING))
if bad:
    sys.exit("\nरुकिए — जाँच-बिन्दु नहीं बैठे; नक़्शा मत लिखिए")
if len(set(scan_to_printed.values())) != len(scan_to_printed):
    sys.exit("\nरुकिए — एक मुद्रित पृष्ठ दो स्कैन पर आ रहा है")

print("\nसब बैठ गया।")
if "--write" in sys.argv:
    out = {str(s): str(p) for s, p in sorted(scan_to_printed.items())}
    (HERE / "pagemap.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("लिखा: pagemap.json (%d प्रविष्टियाँ)" % len(out))
