# -*- coding: utf-8 -*-
"""दो स्वतन्त्र लिप्यन्तरणों का मिलान — केवल वहाँ ध्यान दीजिए जहाँ दोनों अलग हैं।

पहला पाठ  parts/batchNN_*.md  के "## 1. मूल पाठ" खण्डों से,
दूसरा     _recheck/<name>_second.md  से ("=== पृष्ठ N (स्कैन M) ===" ब्लॉक)।

भेद दो तरह के छाँटे जाते हैं:
  वर्तनी  — ऽ, अनुस्वार, विराम-स्थान जैसा अन्तर; अर्थ नहीं बदलता, छोड़ा जा सकता है
  पाठ-भेद — सचमुच अलग शब्द; केवल इन्हें स्कैन से मिलाना है

चलाइए:  python compare_readings.py parts/batch05_p200-211.md _recheck/p200-211_second.md
"""
import re, sys, pathlib, difflib

DEV = "०१२३४५६७८९"
SPELL_THRESHOLD = 0.82      # इससे ऊपर मिलते-जुलते शब्द = केवल वर्तनी-भेद


def dev2en(s):
    return "".join(str(DEV.index(c)) if c in DEV else c for c in s)


def norm(s):
    s = re.sub(r"\[अस्पष्ट\]", "□", s)
    s = re.sub(r"\*\*|\*|`", "", s)
    s = re.sub(r"पाद-टिप्पणी:.*", "", s)
    s = re.sub(r"टीका\s*—", " ", s)
    s = re.sub(r"[‘’“”'\"()\[\]]", " ", s)
    s = re.sub(r"[-–—]", " ", s)
    s = re.sub(r"\s+([?।॥,;:])", r"\1", s)        # विराम से पहले का स्थान हटाइए
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def skeleton(w):
    """वर्तनी-भेद मिटाकर शब्द का ढाँचा — तुलना के लिए।

    `ब` और `व` इस संस्करण में बिल्कुल एक जैसे छपते हैं (बाधक प्रायः वाधक दिखता है),
    इसलिए दोनों को एक ही मान लिया जाता है — वरना हर पन्ने पर दर्जनों झूठे भेद आते हैं।
    `ष`/`श` और `ऋ`/`रि` भी इसी तरह के छपाई-भेद हैं।
    """
    w = w.replace("ऽ", "").replace("ं", "").replace("ँ", "")
    w = w.replace("ब", "व").replace("ष", "श")
    w = re.sub(r"[?।॥,;:]", "", w)
    for a, b in (("न्न", "न"), ("म्म", "म"), ("ण्ण", "ण"), ("त्त", "त"), ("द्द", "द"),
                 ("ञ्च", "च"), ("ङ्क", "क"), ("ण्ड", "ड"), ("न्द", "द"), ("म्व", "व")):
        w = w.replace(a, b)
    return w


def is_spelling_only(xs, ys):
    if len(xs) != len(ys):
        return False
    for a, b in zip(xs, ys):
        if skeleton(a) == skeleton(b):
            continue
        if difflib.SequenceMatcher(None, a, b).ratio() >= SPELL_THRESHOLD:
            continue
        return False
    return True


def first_reading(path):
    """{मुद्रित पृष्ठ: पाठ} — भाग 1 से; (पृष्ठ N) टैग पंक्ति के बीच में भी चल जाता है।"""
    chunks, keep, buf = [], False, []
    for ln in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("## 1. मूल पाठ"):
            keep = True; continue
        if s.startswith("## ") or s.startswith("§"):
            keep = False; continue
        if keep and s:
            buf.append(s)
    text = " ".join(buf)
    parts = re.split(r"\(\s*पृष्ठ\s*([0-9०-९]+)\s*\)", text)
    out = {}
    for i in range(1, len(parts), 2):
        p = int(dev2en(parts[i]))
        out.setdefault(p, []).append(parts[i + 1])
    return {k: norm(" ".join(v)) for k, v in out.items()}


def second_reading(path):
    out, cur = {}, None
    for ln in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        m = re.match(r"^===\s*पृष्ठ\s*(\d+)", ln.strip())
        if m:
            cur = int(m.group(1)); out[cur] = []; continue
        if cur and ln.strip():
            out[cur].append(ln.strip())
    return {k: norm(" ".join(v)) for k, v in out.items()}


def main(a, b, show_spelling=False):
    A, B = first_reading(a), second_reading(b)
    pages = sorted(set(A) & set(B))
    print(f"पहला पाठ: {len(A)} पृष्ठ | दूसरा: {len(B)} | साझे: {len(pages)}")
    only = set(A) ^ set(B)
    if only:
        print("  केवल एक पाठ में:", sorted(only))
    real, spell = 0, 0
    for p in pages:
        wa, wb = A[p].split(), B[p].split()
        sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
        rows = []
        for t, i1, i2, j1, j2 in sm.get_opcodes():
            if t == "equal":
                continue
            x, y = wa[i1:i2], wb[j1:j2]
            if t == "replace" and is_spelling_only(x, y):
                spell += 1
                if show_spelling:
                    rows.append(("वर्तनी", x, y))
                continue
            real += 1
            rows.append(("पाठ-भेद", x, y))
        head = f"\n--- मुद्रित {p}: शब्द {len(wa)}/{len(wb)} | समानता {sm.ratio():.0%}"
        if not rows:
            print(head + " | कोई पाठ-भेद नहीं")
            continue
        print(head + f" | {sum(1 for r in rows if r[0]=='पाठ-भेद')} पाठ-भेद")
        for kind, x, y in rows:
            sx, sy = " ".join(x), " ".join(y)
            if len(sx) > 72: sx = sx[:69] + "…"
            if len(sy) > 72: sy = sy[:69] + "…"
            print(f"    [{kind}]  पहला : {sx or '—'}")
            print(f"              दूसरा: {sy or '—'}")
    print(f"\n==== {real} पाठ-भेद (स्कैन से मिलाइए) · {spell} वर्तनी-भेद (छोड़े जा सकते हैं) ====")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--all" in sys.argv)
