# -*- coding: utf-8 -*-
"""मुद्रित पृष्ठ ↔ स्कैन पृष्ठ — pagemap.json से, हाथ से जोड़े बिना।

इस ग्रन्थ की पृष्ठ-सारणी एक सीधा जोड़ नहीं है: स्कैन 152–196 तक अन्तर 151 है और
197 से आगे 147। "मुद्रित + 147" मान लेने से दो बार ग़लत पन्ना निकला (मुद्रित 29 के
लिए p176 भेजा गया जबकि वह p180 है)। इसलिए गणना हमेशा यहीं से कीजिए।

चलाइए:  python page.py 29 203 435        # मुद्रित → स्कैन
        python page.py --scan 180 350    # स्कैन → मुद्रित
"""
import json
import pathlib
import sys

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
