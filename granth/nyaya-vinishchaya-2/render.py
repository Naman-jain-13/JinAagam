# -*- coding: utf-8 -*-
"""स्कैन PDF से पृष्ठ-छवियाँ बनाइए — img/pNNN.png (NNN = स्कैन-क्रमांक)।

चलाइए:
    python render.py              # पूरा PDF
    python render.py 150 200      # केवल यह परास (स्कैन-क्रमांक)
    python render.py 150 200 --out <dir>   # कहीं और डालिए (जाँच के लिए)

एजेंट को यही छवियाँ पढ़नी हैं, इसलिए dpi इतना रखा है कि संयुक्ताक्षर और
पाद-टिप्पणी के छोटे टाइप भी खुलें। जो पहले से बनी है उसे दुबारा नहीं बनाता,
इसलिए बीच में रुक जाने पर फिर से चला दीजिए।
"""
import pathlib
import sys

import fitz

HERE = pathlib.Path(__file__).resolve().parent
PDF = next(iter(sorted((HERE / "mool").glob("*.pdf"))))
DPI = 200

args = [a for a in sys.argv[1:] if not a.startswith("--")]
out = HERE / "img"
if "--out" in sys.argv:
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1])
out.mkdir(parents=True, exist_ok=True)

doc = fitz.open(PDF)
lo = int(args[0]) if args else 1
hi = int(args[1]) if len(args) > 1 else doc.page_count
made = skipped = 0
for n in range(lo, min(hi, doc.page_count) + 1):
    f = out / ("p%03d.png" % n)
    if f.exists():
        skipped += 1
        continue
    doc[n - 1].get_pixmap(dpi=DPI).save(f)
    made += 1
print("%s: %d pages | बनाईं %d | पहले से थीं %d | → %s"
      % (PDF.name, doc.page_count, made, skipped, out))
