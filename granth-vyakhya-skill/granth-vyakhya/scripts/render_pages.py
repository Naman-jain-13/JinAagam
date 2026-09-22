"""Render every page of a scanned PDF to PNG so Claude can read the images.

Usage:  python render_pages.py "<book.pdf>" <out_dir> [dpi]
Prints page count and whether the PDF already has a text layer (it usually does not for old scans).
250 dpi is enough for Devanagari; 300 for small/dense print.
"""
import os, sys
import pymupdf  # pip install pymupdf

pdf, out = sys.argv[1], sys.argv[2]
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 250
os.makedirs(out, exist_ok=True)
doc = pymupdf.open(pdf)
text_chars = sum(len(p.get_text()) for p in doc)
for i, page in enumerate(doc):
    page.get_pixmap(dpi=dpi).save(os.path.join(out, f"p{i + 1:03d}.png"))
print(f"pages: {doc.page_count} | text layer: {'yes' if text_chars > 200 else 'NO (scan only — read images)'} | written to {out}")
