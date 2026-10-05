# -*- coding: utf-8 -*-
"""बैच-सन्धियों पर दोहराव ढूँढ़िए।

नियम यह है कि अगला बैच पिछले बैच द्वारा पूरा किया गया वाक्य छोड़ दे। पर अगर वह
वाक्य अगले पन्ने पर *शुरू* होता है (जैसे कोई सूत्र), तो दोनों एजेंट उसे अपना मान
लेते हैं और वह दो बार छप जाता है। batch19/batch20 की सन्धि पर ऐसा हुआ था।

यह स्क्रिप्ट हर जोड़ी के अन्तिम और पहले अनुच्छेदों के लम्बे शब्द-समूह मिलाती है।
चलाइए:  python check_seams.py
"""
import re, glob, pathlib

TAIL_WORDS = 40          # पिछले बैच के अन्त से इतने शब्द
HEAD_WORDS = 40          # अगले बैच के आरम्भ से इतने शब्द
MIN_RUN = 5              # इतने शब्द लगातार मिलें तो दोहराव मानिए


def part1_words(path):
    keep, buf = False, []
    for ln in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("## 1. मूल पाठ"):
            keep = True; continue
        if s.startswith("## ") or s.startswith("§"):
            keep = False; continue
        if keep and s and not s.startswith("पाद-टिप्पणी"):
            buf.append(re.sub(r"\(\s*पृष्ठ[^)]*\)", " ", s))
    return " ".join(buf).split()


def longest_overlap(tail, head):
    best = []
    for i in range(len(tail)):
        for j in range(len(head)):
            k = 0
            while i + k < len(tail) and j + k < len(head) and tail[i + k] == head[j + k]:
                k += 1
            if k > len(best):
                best = tail[i:i + k]
    return best


files = sorted(glob.glob("parts/batch*.md"))
print(f"{len(files)} बैच, {len(files)-1} सन्धियाँ\n")
bad = 0
for a, b in zip(files, files[1:]):
    tail = part1_words(a)[-TAIL_WORDS:]
    head = part1_words(b)[:HEAD_WORDS]
    ov = longest_overlap(tail, head)
    na, nb = pathlib.Path(a).name.split("_")[0], pathlib.Path(b).name.split("_")[0]
    if len(ov) >= MIN_RUN:
        bad += 1
        print(f"** {na} -> {nb}: {len(ov)} शब्द दोहराए गए")
        print(f"   {' '.join(ov)[:150]}\n")
    else:
        print(f"   {na} -> {nb}: ठीक")
print(f"\n{'कोई दोहराव नहीं' if not bad else str(bad) + ' सन्धियों पर दोहराव'}")
