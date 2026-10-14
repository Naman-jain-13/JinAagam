# -*- coding: utf-8 -*-
"""तत्त्वार्थसूत्र के अङ्क किस परम्परा के हैं — और क्या वे आपस में मिल तो नहीं गए।

चलाइए:  python _shared/check_citations.py            # सब ग्रन्थ
        python _shared/check_citations.py Prameyakamal

## बात क्या है

तत्त्वार्थसूत्र की दो परम्पराएँ हैं और पाँचवें अध्याय में उनके अङ्क एक नहीं हैं:

| सूत्र | दिगम्बर | श्वेताम्बर |
|---|---|---|
| उत्पादव्ययध्रौव्ययुक्तं सत् | 5.30 | 5.29 |
| गुणपर्यायवद् द्रव्यम् | 5.38 | 5.37 |

दोनों अपने-अपने भीतर ठीक हैं। **दोष तब है जब एक ही ग्रन्थ दोनों के अङ्क मिला
दे** — जैसे उत्पाद-व्यय के लिए 5.29 (श्वेताम्बर) और गुण-पर्याय के लिए 5.38
(दिगम्बर)। तब पाठक जिस भी संस्करण से मिलाएगा, एक सन्दर्भ ग़लत निकलेगा।

यह जाँच यही बताती है: हर ग्रन्थ किस परम्परा पर बैठा है, और कहीं दोनों तो नहीं
मिल गईं। **यह स्वयं कुछ सुधारती नहीं** — कौन-सी परम्परा अपनानी है, यह निर्णय
ग्रन्थ के सम्पादक का है, लिपि का नहीं।
"""
import collections
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

GRANTH = pathlib.Path(__file__).resolve().parent.parent
UTPAD = re.compile(r"उत्पाद(?:व्यय|-व्यय)[^\n]{0,34}?[\(\s]5[.।]\s*(\d+)")
GUNA = re.compile(r"गुणपर्य[यााय]*वद्?\s*द्रव्यम्[^\n]{0,30}?5[.।]\s*(\d+)")
DIG, SVE = {"उत्पाद": "30", "गुण": "38"}, {"उत्पाद": "29", "गुण": "37"}


def audit(book):
    u, g = collections.Counter(), collections.Counter()
    for md in book.rglob("*.md"):
        if md.name in ("batch_task.md", "citation_rules.md"):
            continue
        t = md.read_text(encoding="utf-8", errors="replace")
        for m in UTPAD.finditer(t):
            u[m.group(1)] += 1
        for m in GUNA.finditer(t):
            g[m.group(1)] += 1
    if not (u or g):
        return None
    dig = u[DIG["उत्पाद"]] + g[DIG["गुण"]]
    sve = u[SVE["उत्पाद"]] + g[SVE["गुण"]]
    other = sum(u.values()) + sum(g.values()) - dig - sve
    if dig and sve:
        verdict, mark = "दोनों परम्पराएँ मिली हुई हैं", "✗"
    elif dig:
        verdict, mark = "दिगम्बर क्रम", "✓"
    elif sve:
        verdict, mark = "श्वेताम्बर क्रम", "✓"
    else:
        verdict, mark = "कोई जाना-पहचाना अङ्क नहीं", "?"
    if other:
        verdict += f"; {other} अङ्क किसी भी परम्परा से नहीं मिलते"
        mark = "✗"
    return mark, verdict, dict(u), dict(g)


def main(argv):
    books = ([GRANTH / a for a in argv] if argv else
             [d for d in sorted(GRANTH.iterdir())
              if d.is_dir() and not d.name.startswith("_")])
    bad = 0
    for b in books:
        r = audit(b)
        if not r:
            continue
        mark, verdict, u, g = r
        if mark == "✗":
            bad += 1
        print(f"{mark} {b.name:<24} {verdict}")
        print(f"    उत्पाद-व्यय {u or '—'}   गुण-पर्याय {g or '—'}")
    print(f"\n{bad} ग्रन्थों में अङ्क आपस में नहीं बैठते।")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
