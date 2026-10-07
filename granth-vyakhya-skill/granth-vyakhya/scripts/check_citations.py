# -*- coding: utf-8 -*-
"""उद्धृत श्लोकों का मुद्रित संस्करणों से मिलान।

प्रमेयकमलमार्तण्ड में डेढ़ सौ से अधिक उद्धरण हैं — श्लोकवार्त्तिक, प्रमाणवार्त्तिक,
न्यायसूत्र, सांख्यकारिका, वाक्यपदीय। इन्हें एक-एक पन्ना स्कैन में देखकर जाँचने की
ज़रूरत नहीं: उन ग्रन्थों के संस्करण उपलब्ध हैं, इसलिए सैकड़ों उद्धरण एक ही बार में
जाँचे जा सकते हैं। यही सबसे सस्ती जाँच है, और जहाँ हमारा पाठ संस्करण से अलग निकले
वहीं स्कैन देखना पड़ता है।

दो चेतावनियाँ ध्यान में रहें —
  1. GRETIL के पाठ स्वयं प्रूफ़-शुद्ध नहीं हैं (श्लोकवार्त्तिक की फ़ाइल में तो यह
     साफ़ लिखा है)। अतः भेद का अर्थ "हमारा पाठ ग़लत" नहीं; भेद का अर्थ "यहाँ स्कैन
     देखिए" है। जहाँ संस्करण हमसे मिल जाता है वहीं पाठ निश्चित माना जा सकता है।
  2. ये संस्करण शब्द-सन्धि तोड़कर नहीं छापते, इसलिए मिलान शब्द-स्तर पर नहीं,
     अक्षर-स्तर पर होता है।

चलाइए:  python check_citations.py                 # सब बैच
        python check_citations.py batch15         # एक बैच
        python check_citations.py --aspasht       # केवल वे उद्धरण जिनमें [अस्पष्ट] है
"""
import re
import sys
import pathlib
import difflib
import collections

import translit as T

HERE = pathlib.Path(__file__).resolve().parent
CORPUS_DIR = HERE.parent.parent / "_scratch" / "gretil"

SOURCES = {
    "sa_kumArila-mImAMsazlokavArttika-comm.txt": "श्लोकवार्त्तिक (का० ५,४–५,९)",
    "sa_sucaritamizra-mImAMsAzlokavArttika.txt": "श्लोकवार्त्तिक-काशिका",
    "sa_dharmakIrti-pramANavArttikakArikA.txt": "प्रमाणवार्त्तिक-कारिका",
    "sa_pramANavArttika.txt": "प्रमाणवार्त्तिक (वृत्ति-सहित)",
    "sa_gautama-nyAyasUtra.txt": "न्यायसूत्र",
    "sa_IzvarakRSNa-sAMkhyakArikA.txt": "सांख्यकारिका",
    "sa_bhartRhari-vAkyapadIya.txt": "वाक्यपदीय",
}

LETTERS = set("abcdefghijklmnopqrstuvwxyz"
              "āīūṛṝḷḹ"      # ā ī ū ṛ ṝ ḷ ḹ
              "ṅñṭḍṇśṣ"      # ṅ ñ ṭ ḍ ṇ ś ṣ
              "ḥṃ")                                   # ḥ ṃ

FOLD = {"b": "v", "ṣ": "ś", "ṇ": "n", "ṭ": "t",
        "ḍ": "d", "ṅ": "n", "ñ": "n",
        "ṃ": "", "ḥ": "",
        "ā": "a", "ī": "i", "ū": "u",
        "ṝ": "ṛ", "ḹ": "ḷ"}

GAP = "\u0001"          # [अस्पष्ट] की जगह — किसी अक्षर से मेल नहीं खाएगा
KGRAM = 12
STEP = 4
MIN_LEN = 24            # अक्षरों में; इससे छोटे उद्धरण पर भरोसा नहीं
GOOD = 0.62             # इससे कम मेल = यह उद्धरण उस ग्रन्थ का नहीं
EXACT = 0.985

QUOTE = re.compile(
    '"([^"]{12,700})"'
    "|'([^']{12,700})'"
    "|‘([^’]{12,700})’"
    "|“([^”]{12,700})”")

REF = re.compile(r"(?://\s*)?((?:msv|BVaky|SK|pv|nb|sv)[_0-9A-Za-z,.]*|\d+\.\d+\.\d+)")


def fold(ch):
    return FOLD.get(ch, ch)


class Corpus:
    """एक संस्करण — अक्षर-स्तर पर खोजने योग्य।"""

    def __init__(self, path, label):
        self.label = label
        lines = [ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()
                 if not ln.lstrip().startswith("#") and "GRETIL" not in ln
                 and "http" not in ln]
        self.raw = "\n".join(lines)
        sk, pos = [], []
        for i, ch in enumerate(self.raw.lower()):
            if ch in LETTERS:
                f = fold(ch)
                if f:
                    sk.append(f)
                    pos.append(i)
        self.sk = "".join(sk)
        self.pos = pos
        self.index = collections.defaultdict(list)
        for i in range(0, len(self.sk) - KGRAM, STEP):
            self.index[self.sk[i:i + KGRAM]].append(i)

    def locate(self, q):
        """सबसे सम्भावित स्थान — k-अक्षर टुकड़ों के मतदान से।"""
        votes = collections.Counter()
        for j in range(0, len(q) - KGRAM):
            for p in self.index.get(q[j:j + KGRAM], ()):
                votes[p - j] += 1
        if not votes:
            return None
        start, hits = votes.most_common(1)[0]
        if hits < 2:
            return None
        pad = max(6, len(q) // 8)
        lo = max(0, start - pad)
        hi = min(len(self.sk), start + len(q) + pad)
        return lo, hi

    def match(self, q):
        """मेल का अनुपात — खिड़की को ठीक उद्धरण के बराबर काटकर।

        पहले मोटे तौर पर जगह ढूँढ़ी जाती है, पर उस खिड़की में दोनों ओर कुछ
        अतिरिक्त अक्षर रहते हैं; उन्हें गिनने से सही मेल भी 90% से नीचे दिखता था।
        इसलिए दूसरी बार संरेखण करके खिड़की को उद्धरण की लम्बाई तक छाँटा जाता है।
        """
        span = self.locate(q)
        if not span:
            return None
        lo, hi = span
        sm = difflib.SequenceMatcher(None, q, self.sk[lo:hi], autojunk=False)
        blocks = [b for b in sm.get_matching_blocks() if b.size > 3]
        if blocks:
            b = max(blocks, key=lambda x: x.size)
            start = lo + b.b - b.a
            lo = max(0, start)
            hi = min(len(self.sk), lo + len(q))
        r = difflib.SequenceMatcher(None, q, self.sk[lo:hi], autojunk=False).ratio()
        return r, lo, hi

    def passage(self, lo, hi):
        a = self.pos[lo]
        b = self.pos[min(hi, len(self.pos) - 1)]
        return " ".join(self.raw[a:b + 1].split())

    def ref_near(self, hi):
        """पास का सन्दर्भ-चिह्न — जैसे msv_5,4.1 या BVaky_2.1।"""
        a = self.pos[min(hi, len(self.pos) - 1)]
        m = REF.search(self.raw, a, a + 400)
        return m.group(1) if m else ""


def skeleton_of(dev):
    """देवनागरी उद्धरण → खोजने योग्य अक्षर-शृंखला; [अस्पष्ट] एक रिक्त स्थान बन जाता है।"""
    marked = dev.replace("[अस्पष्ट]", GAP)
    iast = T.dev2iast(marked).lower()
    out = []
    for ch in iast:
        if ch == GAP:
            out.append(GAP)
        elif ch in LETTERS:
            f = fold(ch)
            if f:
                out.append(f)
    return "".join(out)


def part1_quotes(path):
    """भाग 1 के भीतर के उद्धरण — § और मुद्रित पृष्ठ के साथ।"""
    keep, sec, page, out = False, "?", "?", []
    for ln in path.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if s.startswith("§"):
            m = re.match(r"(§\s*\d+)", s)
            if m:
                sec = m.group(1).replace(" ", "")
            keep = False
            continue
        if s.startswith("## 1."):
            keep = True
            continue
        if s.startswith("## "):
            keep = False
            continue
        if not (keep and s) or s.startswith("पाद-"):
            continue
        for m in re.finditer(r"\(\s*पृष्ठ\s*([\d०-९]+)", s):
            page = m.group(1)
        for m in QUOTE.finditer(s):
            out.append((sec, page, next(g for g in m.groups() if g)))
    return out


def main(only=None, aspasht_only=False):
    corpora = []
    for fn, label in SOURCES.items():
        p = CORPUS_DIR / fn
        if p.exists() and p.stat().st_size > 10000:
            corpora.append(Corpus(p, label))
    print(f"संस्करण: {len(corpora)}  "
          f"({sum(len(c.sk) for c in corpora):,} अक्षर)\n")

    files = sorted(HERE.glob("parts/batch*.md"))
    if only:
        files = [f for f in files if only in f.name]

    tried = exact = 0
    hits = []
    for f in files:
        for sec, page, q in part1_quotes(f):
            qs = skeleton_of(q)
            if len(qs) < MIN_LEN:
                continue
            if aspasht_only and GAP not in qs:
                continue
            tried += 1
            best = None
            for c in corpora:
                m = c.match(qs)
                if m and (best is None or m[0] > best[0][0]):
                    best = (m, c)
            if not best or best[0][0] < GOOD:
                continue
            (r, lo, hi), c = best
            if r >= EXACT and GAP not in qs:
                exact += 1
                continue
            hits.append((r, f.name, sec, page, q, c, lo, hi))

    gaps = sum(1 for h in hits if GAP in skeleton_of(h[4]))
    print(f"जाँचे गए: {tried} | "
          f"अक्षरशः समान: {exact} | "
          f"मिलान-योग्य भेद: {len(hits)} "
          f"(इनमें [अस्पष्ट] वाले: {gaps})\n")

    for r, name, sec, page, q, c, lo, hi in sorted(hits, key=lambda x: (GAP not in skeleton_of(x[4]), x[0])):
        flag = " ← [अस्पष्ट]" if GAP in skeleton_of(q) else ""
        ref = c.ref_near(hi)
        print(f"--- {name}  {sec}  मुद्रित {page}  "
              f"[{c.label} {ref}]  मेल {r:.0%}{flag}")
        print(f"    हमारा : {' '.join(q.split())[:300]}")
        print(f"    संस्करण: {c.passage(lo, hi)[:300]}")
        print()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else None, "--aspasht" in sys.argv)
