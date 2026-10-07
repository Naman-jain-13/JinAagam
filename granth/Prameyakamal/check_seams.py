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


# ------------------------------------------- एक ही फ़ाइल के भीतर § -से-§ दोहराव
# ऊपर की जाँच केवल बैच-सन्धियों पर देखती है, क्योंकि दोहराव वहीं अपेक्षित था —
# दो अलग पाठक, एक ही कटा वाक्य। पर दोहराव एक ही फ़ाइल के भीतर भी हुआ: §1083 का
# अन्तिम वाक्य "इति व्यासवचनसद्भावाच्च।" §1084 के आरम्भ में फिर से लिखा मिला।
# वह सन्धि-जाँच की पकड़ से बाहर था और किसी और जाँच की पकड़ में आ ही नहीं सकता था।
def mool_of(block):
    m = re.search(r"##\s*1\..*?\n(.*?)(?=\n##\s*2\.|\Z)", block, re.S)
    if not m:
        return ""
    t = re.sub(r"\(\s*पृष्ठ[^)]*\)", " ", m.group(1))
    t = re.sub(r"(?m)^पाद-टिप्पणी.*$", " ", t)
    return t


print()
_dup = []
for _f in sorted(pathlib.Path(".").glob("parts/batch*.md")):
    _blocks = re.split(r"(?m)^(?=§\d)", _f.read_text(encoding="utf-8"))
    _prev_sec, _prev_tail = None, []
    for _b in _blocks:
        _m = re.match(r"§(\d+)", _b)
        if not _m:
            continue
        _words = mool_of(_b).split()
        if _prev_tail and _words:
            # पिछले § के अन्तिम 25 शब्दों में से कोई लम्बी शृंखला इसके आरम्भ में?
            _head = _words[:25]
            _best = 0
            for _i in range(len(_prev_tail)):
                _n = 0
                while (_n < len(_head) and _i + _n < len(_prev_tail)
                       and _prev_tail[_i + _n] == _head[_n]):
                    _n += 1
                _best = max(_best, _n)
            if _best >= 3:
                _dup.append((_f.name, _prev_sec, _m.group(1), _best,
                             " ".join(_head[:_best])))
        _prev_sec, _prev_tail = _m.group(1), _words[-25:]
if _dup:
    print(f"** एक ही फ़ाइल के भीतर § -दोहराव: {len(_dup)}")
    for _n, _a, _b2, _c, _s in _dup[:10]:
        print(f"   {_n.split('_')[0]} §{_a} → §{_b2}: {_c} शब्द — {_s[:70]}")
else:
    print("   § -से-§ दोहराव (फ़ाइल के भीतर): कोई नहीं")


# --------------------------------- अक्षर-स्तर पर भी, क्योंकि टुकड़े शब्द नहीं होते
# §1180 "…विपाकादिना विभक्तरूपेण सन्ति," पर समाप्त होता है और §1181 "दिना विभक्तरूपेण
# सन्ति, तर्हि…" से आरम्भ — दोहराव केवल दो शब्द और एक अधूरा टुकड़ा ("दिना") था,
# इसलिए शब्द गिनने वाली जाँच से निकल गया। अक्षर गिनने से वह भी पकड़ में आता है।
print()
_c_dup = []
for _f in sorted(pathlib.Path(".").glob("parts/batch*.md")):
    _blocks = re.split(r"(?m)^(?=§\d)", _f.read_text(encoding="utf-8"))
    _prev_sec, _prev_tail = None, ""
    for _b in _blocks:
        _m = re.match(r"§(\d+)", _b)
        if not _m:
            continue
        _txt = re.sub(r"\s+", "", mool_of(_b))
        _head = _txt[:140]
        if _prev_tail and _head:
            _best, _at = 0, ""
            for _i in range(len(_prev_tail)):
                for _j in range(_i + _best + 1, len(_prev_tail) + 1):
                    _sub = _prev_tail[_i:_j]
                    if _sub in _head and len(_sub) > _best:
                        _best, _at = len(_sub), _sub
                    elif len(_sub) > _best:
                        break
            if _best >= 18:
                _c_dup.append((_f.name, _prev_sec, _m.group(1), _best, _at))
        _prev_sec, _prev_tail = _m.group(1), _txt[-140:]
if _c_dup:
    print(f"** § -दोहराव (अक्षर-स्तर): {len(_c_dup)}")
    for _n, _a, _b2, _c, _s in _c_dup[:10]:
        print(f"   {_n.split('_')[0]} §{_a} → §{_b2}: {_c} अक्षर — {_s[:46]}")
else:
    print("   § -दोहराव (अक्षर-स्तर): कोई नहीं")
