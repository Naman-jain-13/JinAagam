# -*- coding: utf-8 -*-
"""चरण-1 निष्कर्षण की जाँच: § क्रम-भंग, पृष्ठ-लोप, हिन्दी-रिसाव, कार्य-प्रक्रिया की भाषा।
   प्रयोग:  python check_mool.py mool
"""
import glob, io, os, re, sys

d = sys.argv[1] if len(sys.argv) > 1 else "mool"
files = sorted(f for f in glob.glob(os.path.join(d, "b*.md")))
if not files:
    print("कोई निष्कर्षित फ़ाइल नहीं मिली।"); sys.exit(1)

PAGE = re.compile(r"<!--\s*मुद्रित पृष्ठ\s*(\d+)")
SEC  = re.compile(r"^§\s*(\d+)\.", re.M)
KAR  = re.compile(r"॥\s*([०-९0-9]+)\s*॥")
# हिन्दी-रिसाव के संकेतक (अनुवाद-क्षेत्र के विशिष्ट शब्द)
HIN  = re.compile(r"(शंका—|समाधान—|विशेषार्थ—|है\s*।|हैं\s*।|नहीं|इसलिये|क्योंकि|जाता है|करते हैं)")
PROC = re.compile(r"(बैच|batch|सत्र\b|एजेंट|फ़ाइल-नाम|b\d\d_p\d)")

pages, secs, kars, problems = [], [], [], []
for f in files:
    t = io.open(f, encoding="utf-8").read()
    fp = [int(x) for x in PAGE.findall(t)]
    fs = [int(x) for x in SEC.findall(t)]
    pages += fp; secs += fs; kars += KAR.findall(t)
    # हर फ़ाइल के भीतर पृष्ठ बढ़ते क्रम में हों
    if fp != sorted(fp):
        problems.append(f"{os.path.basename(f)}: पृष्ठ-चिह्न क्रम से नहीं — {fp}")
    body = "\n".join(l for l in t.splitlines() if not l.startswith("<!--"))
    h = HIN.findall(body)
    if len(h) > 3:
        problems.append(f"{os.path.basename(f)}: सम्भावित हिन्दी-रिसाव ({len(h)} संकेत: {set(h)})")
    p = PROC.findall(t)
    if p:
        problems.append(f"{os.path.basename(f)}: कार्य-प्रक्रिया की भाषा — {set(p)}")
    print(f"{os.path.basename(f):22s} पृष्ठ {min(fp) if fp else '—'}–{max(fp) if fp else '—'}  "
          f"§ {min(fs) if fs else '—'}–{max(fs) if fs else '—'}  ({len(fs)} §)")

# समग्र जाँच
print("\n--- समग्र ---")
want = list(range(1, 354))
miss = [p for p in want if p not in pages]
dupe = sorted({p for p in pages if pages.count(p) > 1})
print(f"मुद्रित पृष्ठ: {len(set(pages))}/353 उपस्थित")
if miss: print("  लुप्त पृष्ठ:", miss[:40], "…" if len(miss) > 40 else "")
if dupe: print("  दोहराए पृष्ठ:", dupe)

gaps = [(a, b) for a, b in zip(secs, secs[1:]) if b != a + 1]
print(f"§ कुल {len(secs)} (उच्चतम {max(secs) if secs else '—'})")
if gaps: print("  § क्रम-भंग:", gaps[:30], "…" if len(gaps) > 30 else "")

print(f"कारिका-चिह्न मिले: {len(kars)}")

if problems:
    print("\n--- ध्यान देने योग्य ---")
    for p in problems: print(" •", p)
else:
    print("\nकोई चेतावनी नहीं।")
