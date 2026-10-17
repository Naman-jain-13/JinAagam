# -*- coding: utf-8 -*-
"""मुद्रित पृष्ठ ↔ स्कैन पृष्ठ — pagemap.json से, हाथ से जोड़े बिना।

चलाइए:  python page.py 17 120 300        # मुद्रित → स्कैन
        python page.py --scan 328 500    # स्कैन → मुद्रित

**इस ग्रन्थ में अन्तर एक-सा नहीं है।** भाग 1 में वह 66 → 67 → 65 → 64 बदलता है
(मुद्रित 29 दो बार स्कैन हुआ; मुद्रित 464, 465, 521 प्रति में हैं ही नहीं), और
भाग 2 में 66 → 64 (मुद्रित 162, 163 नहीं हैं)। इसलिए गणना यहीं से कीजिए।
पूरा ब्यौरा `build_pagemap.py` के शीर्ष पर है।

जिस मुद्रित पृष्ठ का उत्तर `None` आए, वह **प्रति में नहीं है** — उसे छोड़कर आगे
बढ़िए और बैच-फ़ाइल में वैसा लिख दीजिए; उसका पाठ गढ़िए मत।
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

scan_to_printed = {int(k): int(v) for k, v in _MAP.items() if str(v).isdigit()}
printed_to_scan = {}
for s, p in sorted(scan_to_printed.items()):
    printed_to_scan.setdefault(p, s)


def scan(printed):
    """मुद्रित पृष्ठ का स्कैन-क्रमांक (न हो तो None)।"""
    return printed_to_scan.get(int(printed))


def printed(scan_no):
    """स्कैन पृष्ठ का मुद्रित क्रमांक (न हो तो None)।"""
    return scan_to_printed.get(int(scan_no))


def img(printed_no):
    """सीधे चित्र का पथ — एजेंट को यही देना है।"""
    s = scan(printed_no)
    return "img/p%03d.png" % s if s else None


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--scan" in sys.argv:
        for a in args:
            p = printed(a)
            print("  स्कैन %s  →  मुद्रित %s" % (a, p if p else "— (मुख्य पाठ में नहीं)"))
    else:
        for a in args:
            s = scan(a)
            if s:
                print("  मुद्रित %s  →  स्कैन %d   img/p%03d.png" % (a, s, s))
            else:
                print("  मुद्रित %s  →  प्रति में नहीं है" % a)
