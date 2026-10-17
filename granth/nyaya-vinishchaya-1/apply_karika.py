# -*- coding: utf-8 -*-
"""§ शीर्षकों में कारिका-संख्या भरिए — `karika_anchors.md` के पक्के ठिकानों से।

चलाइए:  python apply_karika.py          # क्या बदलेगा
        python apply_karika.py --write

## यह किस पर टिका है

यहाँ की परासें **पाठ से पढ़ी गई कारिकाओं** पर बनी हैं, शीर्ष-कोने के नन्हे अङ्क
पर नहीं। हर आरम्भ-बिन्दु वह पृष्ठ है जहाँ कारिका स्वयं बड़े मोटे अक्षरों में
छपी मिली:

    ॥३॥ मु. 57 · ॥४॥ मु. 116 · ॥५॥ मु. 125 · ॥६॥ मु. 134 · ॥७॥ मु. 140

बीच के पृष्ठ इसलिए भरे जाते हैं कि उन परासों के बैचों ने स्वयं बताया कि उनके
पन्नों पर कोई मूल कारिका छपी नहीं मिली — अर्थात् वही कारिका चलती रही।

**मुद्रित 1–56 यहाँ नहीं भरा जाता।** वहाँ कारिका 1 और 2 कहीं हैं, पर किसी ने
उन्हें पाठ में छपा नहीं देखा; बिना ठिकाने के अङ्क भरना वही भूल दुहराना होगा
जो पहले शीर्ष-कोने से हुई थी। वे शीर्षक `[अङ्क अस्पष्ट]` ही रहते हैं।

मुद्रित 134 के आगे की परास तभी जुड़े जब ॥७॥ का ठिकाना मिल जाए।
"""
import glob
import io
import re
import sys
import time
import pathlib

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent
WRITE = "--write" in sys.argv

# (आरम्भ, अन्त, कारिका) — अन्त सहित। केवल पाठ से पक्की परासें।
RANGES = [(57, 115, "1।3"), (116, 124, "1।4"), (125, 133, "1।5"),
          (134, 139, "1।6"), (140, 146, "1।7"),
          (147, 162, "1।8"), (163, 176, "1।9"), (183, 186, "1।10"),
          (187, 193, "1।11"), (194, 200, "1।12"), (201, 206, "1।13"),
          (207, 207, "1।14–15"), (208, 208, "1।16"),
          (209, 209, "1।17–18"), (210, 210, "1।19"),
          (211, 223, "1।20"), (224, 225, "1।21"), (226, 226, "1।21–23"),
          (227, 228, "1।23"), (229, 230, "1।24"),
          # मुद्रित 231–236 जान-बूझकर खाली: वहाँ के शीर्ष `१।२५` पढ़े गए, पर
          # पाठ में छपी ॥२५॥ मुद्रित 237 पर `एतदेवाह—` के बाद **विवरण के आरम्भ**
          # में मिली। दोनों साथ नहीं बैठते; बिना सुलझे अङ्क भरना वही भूल है।
          (237, 237, "1।25"), (238, 240, "1।26"), (241, 242, "1।27"),
          (243, 247, "1।28"), (248, 248, "1।29"), (249, 250, "1।29–30"),
          (251, 252, "1।30–31"), (253, 254, "1।31–32"),
          (255, 256, "1।32"),
          # 267–272: शीर्ष **और** पाठ में छपी कारिका दोनों से पुष्ट — सबसे पक्की
          # परासें। (॥३५॥ का अङ्क मुद्रित 270 पर, ॥३६॥ का 272 पर।)
          (267, 270, "1।35"), (271, 276, "1।36"),
          (277, 277, "1।37–38"), (278, 278, "1।38")]
          # मुद्रित 257–260 खाली: 257 पर ॥३२॥ का अङ्क और कारिका 33 की पहली
          # पंक्ति दोनों हैं, और ॥३२॥ के अङ्क में ३/२ का भ्रम बाक़ी है। बैच ने
          # स्वयं शीर्षकों में `[अङ्क अस्पष्ट]` रखा — वही रहने दीजिए।

TITLE = re.compile(r"^(§\s*\d+\s*—\s*)(.*)$", re.M)
PAREN = re.compile(r"\s*\((?:मूल\s*)?(?:कारिका|सूत्र)[^)]*\)\s*$")
PAGE = re.compile(r"^\(पृष्ठ (\d+)\)", re.M)


def karika_for(pages):
    hits = set()
    for p in pages:
        for lo, hi, k in RANGES:
            if lo <= p <= hi:
                hits.add(k)
    return sorted(hits)


files = sorted(glob.glob(str(HERE / "parts" / "batch*.md")))
busy = [f for f in files if (time.time() - pathlib.Path(f).stat().st_mtime) < 600]
for f in busy:
    print("छोड़ी (हाल में बदली): %s" % pathlib.Path(f).name)
files = [f for f in files if f not in busy]

changed = 0
for f in files:
    text = io.open(f, encoding="utf-8").read()
    hits = list(TITLE.finditer(text))
    out, last, local = [], 0, 0
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.start():end]
        pages = sorted({int(p) for p in PAGE.findall(body)})
        ks = karika_for(pages)
        if not ks:
            continue                      # ठिकाना नहीं — छेड़िए मत
        label = ks[0] if len(ks) == 1 else "%s–%s" % (ks[0], ks[-1])
        desc = PAREN.sub("", m.group(2)).rstrip()
        new = "%s%s (कारिका %s)" % (m.group(1), desc, label)
        if new.strip() != m.group(0).strip():
            local += 1
            out.append(text[last:m.start()])
            out.append(new)
            last = m.end()
    if local:
        out.append(text[last:])
        changed += local
        print("%-28s %d शीर्षक" % (pathlib.Path(f).name, local))
        if WRITE:
            io.open(f, "w", encoding="utf-8", newline="").write("".join(out))

print("\n%s: %d शीर्षक" % ("भरे" if WRITE else "भरेंगे", changed))
if not WRITE and changed:
    print("लिखने के लिए: --write")
