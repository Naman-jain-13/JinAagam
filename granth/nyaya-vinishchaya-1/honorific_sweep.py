# -*- coding: utf-8 -*-
"""parts/ के भाग 2-3 (अनुवाद, व्याख्या) में जैन आचार्यों के नाम पर 'श्री' लगाइए।
भाग 1 (मूल पाठ) और सम्पादकीय टिप्पण को नहीं छूता।
चलाइए: python honorific_sweep.py [--write]"""
import glob, io, re, sys, collections
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
WRITE = "--write" in sys.argv
L = r"[\u0900-\u097F]"
NAMES = [("वादिराजसूरि", "श्री वादिराजसूरि"), ("वादिराज", "श्री वादिराजसूरि"),
         ("अकलङ्कदेव", "श्री अकलङ्कदेव"), ("अकलङ्क", "श्री अकलङ्कदेव"),
         ("माणिक्यनन्दि", "श्री माणिक्यनन्दि"), ("माणिक्यनन्दी", "श्री माणिक्यनन्दि"),
         ("विद्यानन्द", "श्री विद्यानन्द स्वामी"), ("समन्तभद्र", "श्री समन्तभद्र स्वामी"),
         ("अनन्तवीर्य", "श्री अनन्तवीर्याचार्य")]
cnt = collections.Counter()
for f in sorted(glob.glob("parts/batch*.md")):
    lines = io.open(f, encoding="utf-8").read().split("\n")
    sec = 0; out = []
    for ln in lines:
        if ln.startswith("## 1."): sec = 1
        elif ln.startswith("## 2."): sec = 2
        elif ln.startswith("## 3."): sec = 3
        elif ln.startswith("सम्पादकीय टिप्पण") or ln.startswith("(पृष्ठ ") or ln.startswith("§"): sec = 0 if ln.startswith("सम्पादकीय") or ln.startswith("(पृष्ठ ") else 0
        if sec in (2, 3):
            for old, new in NAMES:
                pat = re.compile(r"(?<!श्री )(?<!%s)%s(?!%s)" % (L, re.escape(old), L))
                def sub(m):
                    cnt[old] += 1
                    return new
                # केवल पूर्ण-शब्द पर
                ln = pat.sub(sub, ln)
        out.append(ln)
    if WRITE: io.open(f, "w", encoding="utf-8", newline="").write("\n".join(out))
for k, v in cnt.items(): print(k, v)
print("लिखा" if WRITE else "सूखा-परीक्षण")
