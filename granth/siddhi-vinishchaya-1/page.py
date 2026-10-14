# -*- coding: utf-8 -*-
"""मुद्रित पृष्ठ ↔ स्कैन पृष्ठ — pagemap.json से, हाथ से जोड़े बिना।

इस ग्रन्थ में अन्तर अभी तक पूरे पाठ में एक-सा मिला है (मुद्रित = स्कैन − 311,
छह स्थानों पर जाँचा गया)। फिर भी गणना यहीं से कीजिए, हाथ से नहीं — प्रमेयकमल में
यही अन्तर तीन बार बदला था (151 → 149 → 147) क्योंकि प्रति में नौ पृष्ठ नहीं थे,
और एक-सूत्र मान लेने से दो बार ग़लत पन्ना निकला। **यदि कहीं मिलान न बैठे तो वह
चेतावनी है — वहीं रुककर जाँचिए।**

चलाइए:  python page.py 17 120 300        # मुद्रित → स्कैन
        python page.py --scan 328 500    # स्कैन → मुद्रित
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
    return f"img/p{s}.png" if s else None


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
                  f"स्कैन {s}   img/p{s}.png"
                  if s else f"  मुद्रित {a}: "
                            f"सारणी में नहीं")
