# -*- coding: utf-8 -*-
"""पूरे खण्ड का एक साथ मिलान — पृष्ठ-टैग पर निर्भर नहीं।

compare_readings.py पृष्ठ-दर-पृष्ठ मिलाती है, जो तभी ठीक है जब दोनों ओर
(पृष्ठ N) टैग सही लगे हों। एक बैच में एजेंट ने पृष्ठ 75 का टैग लिखा ही नहीं था,
जिससे पाठ ग़लत पन्ने के नीचे गिना गया और 41% पाठ ग़ायब दिखने लगा — जबकि असल में
केवल 8% कम था। यह स्क्रिप्ट दोनों पाठ पूरे जोड़कर एक ही बार मिलाती है, इसलिए
टैग की गड़बड़ी से नतीजा नहीं बिगड़ता।

चलाइए:  python compare_whole.py parts/batchNN_pXXX-YYY.md _recheck/pXXX-YYY_second.md
"""
import sys
import difflib
import importlib.util
import pathlib

_spec = importlib.util.spec_from_file_location(
    "cr", str(pathlib.Path(__file__).resolve().parent / "compare_readings.py"))
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)


def joined(d):
    return " ".join(d[k] for k in sorted(d))


def all_part1(path):
    """भाग 1 का सारा पाठ — पृष्ठ-टैग की परवाह किए बिना।

    cr.first_reading() केवल वह पाठ उठाती है जो किसी (पृष्ठ N) टैग के बाद आता है,
    इसलिए टैग से पहले लिखा हुआ अंश छूट जाता है। पूरे खण्ड की तुलना में पृष्ठ-विभाजन
    की ज़रूरत नहीं, इसलिए यहाँ सब कुछ लिया जाता है।
    """
    import re
    keep, buf = False, []
    for ln in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("## 1. मूल पाठ"):
            keep = True
            continue
        if s.startswith("## ") or s.startswith("§"):
            keep = False
            continue
        if keep and s and not s.startswith("पाद-टिप्पणी"):
            buf.append(re.sub(r"\(\s*पृष्ठ[^)]*\)", " ", s))
    return cr.norm(" ".join(buf))


def main(a, b):
    A, B = cr.first_reading(a), cr.second_reading(b)

    # श्रेणी-टैग भी गिनिए। एजेंट प्रायः (पृष्ठ 130-131) लिखते हैं और यह इस परियोजना
    # में चलन में है (अष्टसहस्री में 85, न्यायकुमुदचन्द्र में 66 ऐसे टैग हैं)।
    # केवल एकल टैग गिनने से बार-बार झूठी चेतावनी आती थी।
    import re as _re
    raw = pathlib.Path(a).read_text(encoding="utf-8")
    tagged = set()
    for _m in _re.finditer(r"\(\s*पृष्ठ\s*(\d+)\s*(?:[-–]\s*(\d+))?\s*\)", raw):
        _lo = int(_m.group(1))
        _hi = int(_m.group(2)) if _m.group(2) else _lo
        tagged.update(range(_lo, _hi + 1))

    missing = sorted(set(B) - tagged)
    if missing:
        print(f"** इन पृष्ठों का कोई टैग नहीं (श्रेणी-टैग भी गिने): {missing}")
        print("   इनका पृष्ठ-सन्दर्भ ग़लत निकलेगा — टैग जोड़िए।\n")

    wa, wb = all_part1(a).split(), joined(B).split()
    sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    print(f"पूरे खण्ड का मिलान — शब्द {len(wa)}/{len(wb)} | समानता {sm.ratio():.0%}")

    real, spell, rows = 0, 0, []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        x, y = wa[i1:i2], wb[j1:j2]
        if tag == "replace" and cr.is_spelling_only(x, y):
            spell += 1
            continue
        real += 1
        rows.append((x, y))

    print(f"  {real} पाठ-भेद · {spell} वर्तनी-भेद")
    print()
    for x, y in rows:
        sx, sy = " ".join(x), " ".join(y)
        if len(sx) > 74:
            sx = sx[:71] + "…"
        if len(sy) > 74:
            sy = sy[:71] + "…"
        print(f"  पहला : {sx or '—'}")
        print(f"  दूसरा: {sy or '—'}")
        print()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
