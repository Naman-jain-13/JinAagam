# -*- coding: utf-8 -*-
"""addenda/sNNNN.md की जाँच: चार शीर्ष, कोई बैकटिक नहीं, कोई सम्प्रदाय-नाम नहीं,
आचार्य-नाम पर सम्मान-सूचक। चलाइए: python check_addenda.py"""
import io, pathlib, re, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
HEADS = ["## 3. पूरक व्याख्या", "## 4. सरल उदाहरण", "## 5. तुलनात्मक तालिका / चार्ट",
         "## 6. सन्दर्भ एवं पाद-टिप्पणी"]
SECT = ["दिगम्बर", "श्वेताम्बर", "बीसपंथ", "तेरापंथ", "दिगंबर", "श्वेतांबर"]
bad = 0; n = 0
for p in sorted((HERE/"addenda").glob("s*.md")):
    n += 1
    t = io.open(p, encoding="utf-8").read()
    heads = [l.strip() for l in t.splitlines() if l.startswith("## ")]
    errs = []
    if heads != HEADS: errs.append("शीर्ष: %s" % heads)
    if "`" in t: errs.append("बैकटिक")
    for s in SECT:
        if s in t: errs.append("सम्प्रदाय-नाम %s" % s)
    for nm in ["अकलङ्कदेव", "वादिराजसूरि", "विद्यानन्द", "समन्तभद्र", "अनन्तवीर्य"]:
        for m in re.finditer(nm, t):
            pre = t[max(0, m.start()-12):m.start()]
            if "श्री" not in pre:
                errs.append("बिना श्री: %s" % nm); break
    sec6 = t.split("## 6.")[-1].strip().splitlines()
    if len([l for l in sec6 if l.strip()]) > 4: errs.append("भाग 6 लम्बा")
    if errs:
        bad += 1; print("✗", p.name, "; ".join(errs))
print("जाँचे %d; खटके %d" % (n, bad))
