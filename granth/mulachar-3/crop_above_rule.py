# -*- coding: utf-8 -*-
"""Crop a scan page to the Sanskrit/Prakrit area ABOVE the horizontal rule only.

    python crop_above_rule.py <pdf> <scan_page> <out.png> [dpi=220] [x0 y0 x1 y1]

The optional box (in PDF points, page box 504 x 666) selects a zoom region *inside the above-rule area*;
anything below the rule is cut off no matter what box you give. If no rule is found the whole page is
returned and a WARNING is printed (title/continuation pages, or a rule too faint to detect): then look
carefully and use none of any Hindi you see below the Sanskrit.
"""
import sys, numpy as np, pymupdf
from PIL import Image

pdf, page, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
dpi = int(sys.argv[4]) if len(sys.argv) > 4 else 220
box = [float(x) for x in sys.argv[5:9]] if len(sys.argv) >= 9 else None
d = pymupdf.open(pdf); pg = d[page - 1]
H = pg.rect.height; W = pg.rect.width
# detect the rule on a coarse render: a thin row with a long unbroken dark run (the rule is faint, so try
# progressively looser settings); text rows never have a long unbroken run.
pm = pg.get_pixmap(dpi=100, colorspace=pymupdf.csGRAY)
a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width)

def longest_run(row):
    best = run = 0
    for v in row:
        run = run + 1 if v else 0
        if run > best: best = run
    return best

ys = None
for thr, frac in ((200, 0.28), (225, 0.28), (235, 0.22), (240, 0.18)):
    dark = a < thr
    hits = []
    for y in range(int(0.06 * a.shape[0]), int(0.95 * a.shape[0])):
        r = longest_run(dark[y])
        if r > frac * a.shape[1]: hits.append((r, y))
    if hits:
        # the rule is the LONGEST unbroken dark run on the page (a bold गाथा heading or an underline
        # can produce shorter hits earlier on the page); ties go to the upper row
        best = max(r for r, y in hits)
        ys = min(y for r, y in hits if r >= best - 2)
        break
if ys is None:
    print('WARNING: no horizontal rule found on this page — whole page returned; ignore any Hindi below the Sanskrit.')
    cut = H
else:
    cut = (ys - 2) * H / a.shape[0]
    print('rule at y=%.1f pt (of %.0f); returning only the area above it' % (cut, H))
x0, y0, x1, y1 = (0, 0, W, cut)
if box:
    x0 = max(0, box[0]); y0 = max(0, box[1]); x1 = min(W, box[2]); y1 = min(cut, box[3])
    if y1 <= y0: sys.exit('box lies below the rule: nothing to show')
pg.get_pixmap(dpi=dpi, clip=pymupdf.Rect(x0, y0, x1, y1)).save(out)
print('saved', out)
