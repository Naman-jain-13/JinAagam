# -*- coding: utf-8 -*-
"""[अस्पष्ट] स्थानों की चालू सूची — हाथ से रखी सूची पुरानी पड़ जाती है।

ये वे जगहें हैं जहाँ प्रति स्वयं हमें हरा देती है। निपटारे के समय यहीं से शुरू
कीजिए, क्योंकि यहाँ ठीक-ठीक पता है कि क्या देखना है। हर पंक्ति में मुद्रित पृष्ठ
और स्कैन का चित्र भी दिया जाता है, ताकि सीधे वहीं जाया जा सके।

केवल भाग 1 (मूल पाठ) के चिह्न गिने जाते हैं। भाग 2–3 में [अस्पष्ट] लिखना नियम-विरुद्ध
है, इसलिए यदि वे वहाँ मिलें तो अलग से चेतावनी दी जाती है — वह अपने आप में एक दोष है।

चलाइए:  python list_aspasht.py            # सूची छापिए
        python list_aspasht.py --write    # _recheck/aspasht_list.md में लिखिए
"""
import re
import sys
import pathlib

import page as P

HERE = pathlib.Path(__file__).resolve().parent
MARK = "[अस्पष्ट]"


def walk(path):
    """(§, मुद्रित पृष्ठ, भाग, पंक्ति) — फ़ाइल को क्रम से पढ़ते हुए।"""
    sec, page, part = "?", None, 0
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        m = re.match(r"(§\s*\d+)", s)
        if m:
            sec = m.group(1).replace(" ", "")
            part = 0
            continue
        m = re.match(r"##\s*([123])\.", s)
        if m:
            part = int(m.group(1))
            continue
        for mm in re.finditer(r"\(\s*पृष्ठ\s*(\d+)", s):
            page = int(mm.group(1))
        if MARK in s:
            yield sec, page, part, s


def main(write=False):
    rows, stray = [], []
    for f in sorted(HERE.glob("parts/batch*.md")):
        for sec, pg, part, line in walk(f):
            n = line.count(MARK)
            for _ in range(n):
                (rows if part == 1 else stray).append(
                    (f.name.split("_")[0], sec, pg, part, line))

    out = ["# [अस्पष्ट] स्थानों की सूची", "",
           f"मूल पाठ में {len(rows)} चिह्न। "
           "ये वे जगहें हैं जहाँ प्रति स्वयं हमें हरा देती है।", "",
           "| बैच | § | मुद्रित | चित्र | सन्दर्भ |",
           "|---|---|---|---|---|"]
    for b, sec, pg, _part, line in rows:
        img = P.img(pg) if pg else ""
        i = line.find(MARK)
        ctx = re.sub(r"\s+", " ", line[max(0, i - 44):i + len(MARK) + 34])
        out.append(f"| {b} | {sec} | {pg or '?'} | {img} | …{ctx}… |")

    if stray:
        out += ["", "## ** भाग 2 के चिह्न — ये मूल के गड्ढे को दिखाते हैं, दोष नहीं", ""]
        for b, sec, pg, part, line in stray:
            out.append(f"- {b} {sec} (मु. {pg}, भाग {part}) — "
                       f"{re.sub(r'\s+', ' ', line)[:110]}")

    text = "\n".join(out) + "\n"
    if write:
        d = HERE / "_recheck"
        d.mkdir(exist_ok=True)
        (d / "aspasht_list.md").write_text(text, encoding="utf-8")
        print(f"_recheck/aspasht_list.md — {len(rows)} स्थान"
              + (f", {len(stray)} भाग 2 में" if stray else ""))
    else:
        print(text)


if __name__ == "__main__":
    main("--write" in sys.argv)
