# -*- coding: utf-8 -*-
"""मुद्रित पृष्ठ <-> स्कैन पृष्ठ — pagemap.json से, हाथ से जोड़े बिना।

**इस भाग में अन्तर एक-सा नहीं है। हाथ से जोड़-घटाव बिलकुल मत कीजिए।**

    स्कैन  17-280  ->  मुद्रित = स्कैन + 355
    स्कैन 281-453  ->  मुद्रित = स्कैन + 357

बदलाव का बिन्दु पाँच लगातार शीर्ष पढ़कर पक्का किया गया है:
278->633, 279->634, 280->635, फिर 281->638, 282->639।

अर्थात् **मुद्रित 636 और 637 स्कैन में हैं ही नहीं।** विषम 635 के बाद सीधे सम 638
आता है, इसलिए यह एक पूरा पत्र (उसके दोनों पृष्ठ) है जो स्कैन से छूट गया — दो
अलग-अलग कोरे फ़्रेम नहीं। उस पत्र की सामग्री इस प्रति में उपलब्ध नहीं है; जहाँ वह
आएगा वहाँ पाठ में छेद रहेगा और उसे **छेद ही लिखना है, जोड़ना नहीं।**

399->756, 420->777, 440->797, 448->805 तक जाँचा गया — आगे कोई दूसरा छेद नहीं।

चलाइए:  python page.py 638 757         # मुद्रित -> स्कैन
        python page.py --scan 281 400  # स्कैन -> मुद्रित
"""
import json
import pathlib
import sys

# Windows का console cp1252 में होता है, इसलिए देवनागरी छापते ही UnicodeEncodeError
# आता था। हर एजेंट को PYTHONIOENCODING लिखना याद रहे, यह मानना ठीक नहीं।
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent
_MAP = json.loads((HERE / "pagemap.json").read_text(encoding="utf-8"))

scan_to_printed = {int(k): int(v) for k, v in _MAP.items()
                   if str(v).isdigit()}
printed_to_scan = {}
for s, p in sorted(scan_to_printed.items()):
    printed_to_scan.setdefault(p, s)


def scan(printed):
    """मुद्रित पृष्ठ का स्कैन-क्रमांक।"""
    return printed_to_scan.get(int(printed))


def printed(scan_no):
    """स्कैन पृष्ठ का मुद्रित क्रमांक।"""
    return scan_to_printed.get(int(scan_no))


def img(printed_no):
    """सीधे चित्र का पथ — एजेंट को यही देना है।"""
    s = scan(printed_no)
    return f"img/p{s:03d}.png" if s else None


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--scan" in sys.argv:
        for a in args:
            print(f"  स्कैन {a}  →  "
                  f"मुद्रित {printed(a)}")
    else:
        for a in args:
            s = scan(a)
            print(f"  मुद्रित {a}  →  "
                  f"स्कैन {s}   img/p{s:03d}.png"
                  if s else f"  मुद्रित {a}: "
                            f"सारणी में नहीं")
