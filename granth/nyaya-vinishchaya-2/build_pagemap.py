# -*- coding: utf-8 -*-
"""pagemap.json बनाइए — जाँचे हुए खण्डों से, जोड़-घटाव के एक नियम से नहीं।

चलाइए:  python build_pagemap.py          # जाँच कर के छापिए
        python build_pagemap.py --write  # pagemap.json लिखिए

## भाग 2 का ढाँचा

| स्कैन | क्या है |
|---|---|
| 1–66 | पुस्तकालय-पत्र, प्रकाशन-विवरण, हिन्दी प्रस्तावना (अपनी अलग पृष्ठ-संख्या) |
| **67–433** | **मुख्य संस्कृत पाठ — मुद्रित 1–369** (द्वितीय तथा तृतीय प्रस्ताव) |
| 434–521 | सम्पादकीय अनुक्रमणिकाएँ — "भाग पृष्ठ श्लो॰सं॰" वाले स्तम्भ |

मुख्य पाठ का अन्तर एक बार बदलता है, और वह बदलाव एक-एक पन्ने पर पक्का किया गया है:

| स्कैन | मुद्रित | अन्तर | क्यों |
|---|---|---|---|
| 67–227 | 1–161 | 66 | (स्कैन 67 पर शीर्ष नहीं; ग्रन्थ का पहला पन्ना) |
| 228–433 | 164–369 | 64 | **मुद्रित 162, 163 प्रति में नहीं** |

**अनुक्रमणिका-भाग यहाँ नहीं जोड़ा गया।** वह व्याख्या का विषय नहीं है, और उसमें
बिना-संख्या वाले खण्ड-पृष्ठ (स्कैन 434, 447) हैं जिनसे अन्तर 63 और 62 तक जाता है।
उसमें से कुछ चाहिए तो पहले `probe_corners.py` से वहीं का नक़्शा बनाइए — यहाँ के
नियम को आगे मत बढ़ाइए।
"""
import json
import pathlib
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent

RUNS = [(67, 227, 66), (228, 433, 64)]
MISSING = [162, 163]
CHECKS = {68: 2, 80: 14, 100: 34, 120: 54, 150: 84, 170: 104, 200: 134,
          210: 144, 211: 145, 227: 161, 228: 164, 229: 165, 250: 186,
          270: 206, 290: 226, 300: 236, 320: 256, 360: 296, 400: 336,
          410: 346, 420: 356, 430: 366, 431: 367, 433: 369}

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
