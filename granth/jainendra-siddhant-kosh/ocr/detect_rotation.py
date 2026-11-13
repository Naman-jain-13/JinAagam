# हर पृष्ठ की दिशा (Tesseract OSD) → bhag-K/verify/rotation.tsv  (पृष्ठ, घुमाव-डिग्री, विश्वास)
import io, os, re, sys, subprocess, pymupdf
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = sys.argv[1]; BH = os.path.join(HERE, 'bhag-%s' % K)
TESS = r'C:\Program Files\Tesseract-OCR\tesseract.exe'; TD = os.path.join(HERE, 'ocr', 'tessdata')
d = pymupdf.open(os.path.join(BH, 'mool', 'Jainendra_Siddhant_Kosh_%s.pdf' % K))
tmp = os.path.join(BH, 'ocr_tmp', 'osd.png'); os.makedirs(os.path.dirname(tmp), exist_ok=True)
out = io.open(os.path.join(BH, 'verify', 'rotation.tsv'), 'w', encoding='utf-8')
for n in range(1, len(d) + 1):
    d[n - 1].get_pixmap(dpi=150).save(tmp)
    o = subprocess.run([TESS, tmp, 'stdout', '--tessdata-dir', TD, '--psm', '0'], capture_output=True).stdout.decode('utf-8', 'replace')
    rot = re.search(r'Rotate: (\d+)', o); conf = re.search(r'Orientation confidence: ([\d.]+)', o)
    out.write('%d\t%s\t%s\n' % (n, rot.group(1) if rot else '0', conf.group(1) if conf else '0')); out.flush()
