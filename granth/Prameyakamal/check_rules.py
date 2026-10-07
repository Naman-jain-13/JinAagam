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

# ---------------------------------------------------------------- अनुच्छेद-क्रम
# Edit-कॉल का लंगर इच्छित जगह से पहले वाले पाठ से मेल खा जाए तो नया अनुच्छेद चुपचाप
# फ़ाइल के अन्त में जुड़ जाता है, क्रम में नहीं। एक एजेंट ने स्वयं पकड़ा था।
print()
_bad = 0
for _f in files:
    _nums = [int(_m.group(1)) for _m in
             re.finditer(r"^§(\d+)", pathlib.Path(_f).read_text(encoding="utf-8"), re.M)]
    if not _nums:
        continue
    _name = pathlib.Path(_f).name
    _desc = [(_nums[i-1], _nums[i]) for i in range(1, len(_nums)) if _nums[i] < _nums[i-1]]
    _dups = sorted({n for n in _nums if _nums.count(n) > 1})
    if _desc or _dups:
        _bad += 1
        print(f"** {_name}: " + (f"क्रम उलटा {_desc} " if _desc else "")
              + (f"दोहरे अनुच्छेद {_dups}" if _dups else ""))
if not _bad:
    print("   अनुच्छेद-क्रम: सब फ़ाइलें क्रम में, कोई दोहरा नहीं")

# ---------------------------------------------------------- अनुच्छेदों का आकार
# एक बैच में बारह पृष्ठों के लिए केवल बारह अनुच्छेद लिखे गए — पड़ोसी बैचों में वही
# बारह पृष्ठ इकतीस से चालीस अनुच्छेदों में बँटे हैं। हर § विषय-सूची की एक पंक्ति बनता
# है, इसलिए दुगुने आकार के अनुच्छेद उस हिस्से को बाक़ी पुस्तक से अलग और दुर्गम बना
# देते हैं। यह बात न एजेंट की रिपोर्ट में दिखती है, न फ़ाइल पढ़ने से — गिनने से दिखती है।
print()
_sizes = {}
for _f in files:
    _t = pathlib.Path(_f).read_text(encoding="utf-8")
    _secs = re.split(r"(?m)^§", _t)[1:]
    if _secs:
        _sizes[pathlib.Path(_f).name] = sum(len(s) for s in _secs) // len(_secs)
if _sizes:
    _vals = sorted(_sizes.values())
    _med = _vals[len(_vals) // 2]
    _odd = {k: v for k, v in _sizes.items() if v > _med * 1.6 or v < _med * 0.45}
    if _odd:
        print(f"** अनुच्छेद-आकार: माध्य {_med} अक्षर/§, पर इन बैचों में बहुत अलग —")
        for k, v in sorted(_odd.items(), key=lambda x: -x[1]):
            print(f"   {k}: {v} अक्षर/§  ({v/_med:.1f} गुना)")
        print("   (विषय-सूची की दृष्टि से इन्हें फिर से बाँटना बेहतर है)")
    else:
        print(f"   अनुच्छेद-आकार: सब बैच एक जैसे (माध्य {_med} अक्षर/§)")

# ------------------------------------------------- [अस्पष्ट] कहाँ चल सकता है
# यह चिह्न प्रति की सीमा बताता है, पाठक से बात करने का साधन नहीं।
#   भाग 1 — ठीक, वहीं उसकी जगह है।
#   भाग 2 — तभी ठीक जब उसी § के भाग 1 में भी गड्ढा हो; अनुवाद उस गड्ढे को छिपा नहीं
#           सकता, पर बिना गड्ढे के वहाँ चिह्न लगाना अनुवादक का हार मानना है।
#   भाग 3 — कभी नहीं। व्याख्या में "यह अंश पढ़ा नहीं गया" लिखना प्रक्रिया-भाषा है;
#           वह बात भाग 1 की पाद-टिप्पणी में जाती है।
print()
_MARK = "[अस्पष्ट]"


def _sections(path):
    cur, parts, part = None, None, 0
    for ln in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        m = re.match(r"(§\s*\d+)", s)
        if m:
            if cur:
                yield cur, parts
            cur, parts, part = m.group(1).replace(" ", ""), {1: [], 2: [], 3: []}, 0
            continue
        m = re.match(r"##\s*([123])\.", s)
        if m:
            part = int(m.group(1))
            continue
        if cur and part:
            parts[part].append(s)
    if cur:
        yield cur, parts


_bad3, _orphan = [], []
for _f in files:
    for _sec, _p in _sections(_f):
        _n1 = sum(l.count(_MARK) for l in _p[1])
        _n2 = sum(l.count(_MARK) for l in _p[2])
        _n3 = sum(l.count(_MARK) for l in _p[3])
        _name = pathlib.Path(_f).name
        if _n3:
            _bad3.append((_name, _sec, _n3))
        if _n2 and not _n1:
            _orphan.append((_name, _sec, _n2))
if _bad3 or _orphan:
    print(f"** [अस्पष्ट] ग़लत जगह: भाग 3 में {sum(n for _,_,n in _bad3)}, "
          f"भाग 2 में बिना मूल-गड्ढे के {sum(n for _,_,n in _orphan)}")
    for _name, _sec, _n in (_bad3 + _orphan)[:12]:
        print(f"   {_name} {_sec} × {_n}")
    print("   (भाग 3 की बात भाग 1 की पाद-टिप्पणी में जाए; भाग 2 केवल मूल का गड्ढा दिखाए)")
else:
    print("   [अस्पष्ट] की जगह: ठीक — भाग 3 में कोई नहीं, भाग 2 में सब मूल के गड्ढे पर")

# ----------------------------------- प्रक्रिया-शब्द, शब्द-सीमा के साथ
# ऊपर की PROCESS सूची पूरे वाक्यांश ढूँढ़ती है ("इस बैच"), इसलिए "प्रस्तुत बैच",
# "बैच-सीमा", "स्कैन में अस्पष्ट" जैसे रूप बच निकलते थे — चौबीस जगह बच निकले भी।
# ये शब्द अपने आप में काम की भाषा हैं और पाठक के सामने नहीं आने चाहिए।
#
# शब्द-सीमा आवश्यक है: "सत्र" को "सत्रह" में, और "विभाग" को वैशेषिक के गुण
# (संयोग-विभाग) में ढूँढ़ लेने से सौ झूठी चेतावनियाँ आती हैं। "विभाग" इसीलिए सूची
# में है ही नहीं — वह ग्रन्थ का अपना पारिभाषिक शब्द है।
print()
_DEV = "[ऀ-ॿ]"
_WORDS = ["स्कैन", "बैच", "एजेंट", "फ़ाइल", "सत्र"]
_pats = [(w, re.compile(f"(?<!{_DEV}){re.escape(w)}(?!{_DEV})")) for w in _WORDS]
_proc = []
for _f in files:
    _part, _sec = 0, "?"
    for _ln in pathlib.Path(_f).read_text(encoding="utf-8").splitlines():
        _s = _ln.strip()
        _m = re.match(r"(§\d+)", _s)
        if _m:
            _sec, _part = _m.group(1), 0
            continue
        _m = re.match(r"##\s*([123])\.", _s)
        if _m:
            _part = int(_m.group(1))
            continue
        # पाद-टिप्पणी भी पाठक के सामने छपती है, इसलिए वह भी जाँची जाती है —
        # तीन टिप्पणियाँ "स्कैन में अस्पष्ट" कहती मिली थीं।
        if _part in (1, 2, 3):
            for _w, _p in _pats:
                if _p.search(_s):
                    _proc.append((pathlib.Path(_f).name, _sec, _part, _w))
                    break
if _proc:
    print(f"** प्रक्रिया-शब्द भाग 2–3 में: {len(_proc)} जगह")
    for _n, _sec, _pt, _w in _proc[:10]:
        print(f"   {_n} {_sec} भाग{_pt}  «{_w}»")
    if len(_proc) > 10:
        print(f"   … और {len(_proc)-10}")
    print("   (यह काम की भाषा है; पाठक के लिए नहीं। कॉपी की सीमा बतानी हो तो वह")
    print("    भाग 1 की पाद-टिप्पणी में जाए, और 'स्कैन' नहीं 'प्रति' कहकर।)")
else:
    print("   प्रक्रिया-शब्द (भाग 2–3): साफ़")
