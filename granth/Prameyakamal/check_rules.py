# -*- coding: utf-8 -*-
"""पुस्तक में जाने से पहले की स्वचालित जाँचें।

चलाइए:  python check_rules.py
"""
import re, glob, pathlib

SECTS = ["बीसपंथ", "तेरापंथ", "बीसपन्थ", "तेरापन्थ", "बिसपंथ"]
PROCESS = ["इस बैच", "अगले बैच", "अगला बैच", "इस सत्र", "उपयोगकर्ता",
           "अन्तिम वाक्य अगले", "पहले पृष्ठ का अन्तिम", "स्कैन फ़ाइल", ".png", ".md"]
BARE_ACHARYA = ["विद्यानन्द", "प्रभाचन्द्र", "माणिक्यनन्दि", "समन्तभद्र", "अकलङ्कदेव", "पूज्यपाद"]

files = sorted(glob.glob("parts/*.md"))
print(f"{len(files)} फ़ाइलें जाँची जा रही हैं\n")
bad = 0

def scan(label, terms, skip_mool=True):
    global bad
    hits = []
    for f in files:
        in_mool = False
        for i, ln in enumerate(pathlib.Path(f).read_text(encoding="utf-8").splitlines(), 1):
            s = ln.strip()
            if s.startswith("## 1."):
                in_mool = True; continue
            if s.startswith("## ") or s.startswith("§"):
                in_mool = False
            if skip_mool and in_mool:
                continue
            for t in terms:
                if t in s:
                    hits.append((pathlib.Path(f).name, i, t, s[:80]))
    if hits:
        bad += 1
        print(f"** {label}: {len(hits)} जगह")
        for n, i, t, s in hits[:6]:
            print(f"   {n}:{i}  «{t}»  {s}")
        if len(hits) > 6:
            print(f"   … और {len(hits)-6}")
        print()
    else:
        print(f"   {label}: साफ़")

scan("सम्प्रदाय-नाम (कहीं भी)", SECTS, skip_mool=False)
scan("प्रक्रिया-भाषा (मूल पाठ के बाहर भी नहीं चाहिए)", PROCESS, skip_mool=False)

# आचार्य-नाम बिना आदर — केवल भाग 2-3 में देखिए, मूल पाठ ज्यों का त्यों रहता है
print()
hits = []
for f in files:
    in_mool = False
    for i, ln in enumerate(pathlib.Path(f).read_text(encoding="utf-8").splitlines(), 1):
        s = ln.strip()
        if s.startswith("## 1."):
            in_mool = True; continue
        if s.startswith("## ") or s.startswith("§"):
            in_mool = False
        if in_mool or not s:
            continue
        for name in BARE_ACHARYA:
            for m in re.finditer(re.escape(name), s):
                before = s[max(0, m.start()-12):m.start()]
                if "श्री" in before or "आचार्य" in before:
                    continue
                hits.append((pathlib.Path(f).name, i, name, s[max(0,m.start()-30):m.start()+30]))
if hits:
    print(f"** आचार्य-नाम बिना 'श्री'/'आचार्य' (भाग 2–3 में): {len(hits)} जगह")
    for n, i, t, s in hits[:8]:
        print(f"   {n}:{i}  …{s}…")
    if len(hits) > 8:
        print(f"   … और {len(hits)-8}")
    print("\n   (postprocess_docx.py निर्माण के समय इन्हें ठीक कर देती है, पर स्रोत में भी सुधारना बेहतर है)")
else:
    print("   आचार्य-सम्बोधन: साफ़")

# ---------------------------------------------------------------- पृष्ठ-आवरण
# हर मुद्रित पृष्ठ का (पृष्ठ N) टैग होना चाहिए — वरना उस पन्ने का सन्दर्भ नहीं बनेगा।
# batch14 में 11 में से केवल 4 टैग थे; पाठ मौजूद था पर पृष्ठ-सन्दर्भ नहीं बनता।
import json as _json
print()
try:
    _mp = _json.load(open("pagemap.json", encoding="utf-8"))
    _RNG = _json.load(open("batch_ranges.json", encoding="utf-8"))
except FileNotFoundError:
    print("   पृष्ठ-आवरण: pagemap.json या batch_ranges.json नहीं मिली — छोड़ा")
else:
    _weak = []
    for _f in files:
        _key = pathlib.Path(_f).name.split("_")[0]
        if _key not in _RNG:
            continue
        _a, _b = _RNG[_key]
        _want = [int(_mp[str(s)]) for s in range(_a, _b + 1) if _mp.get(str(s), "").isdigit()]
        _got = set()
        for _m in re.finditer(r"\(\s*पृष्ठ\s*(\d+)\s*(?:[-–]\s*(\d+))?\s*\)",
                              pathlib.Path(_f).read_text(encoding="utf-8")):
            _lo = int(_m.group(1))
            _hi = int(_m.group(2)) if _m.group(2) else _lo
            _got.update(range(_lo, _hi + 1))
        _miss = [p for p in _want if p not in _got]
        if _miss:
            _weak.append((_key, _miss))
    if _weak:
        print(f"** पृष्ठ-टैग छूटे हुए: {len(_weak)} बैच")
        for _k, _m in _weak:
            print(f"   {_k}: {_m}")
    else:
        print("   पृष्ठ-आवरण: हर मुद्रित पृष्ठ का टैग मौजूद")
