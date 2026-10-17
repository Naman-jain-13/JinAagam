# -*- coding: utf-8 -*-
"""§ शीर्षक की कारिका-संख्या को `karika_map.md` से मिलाइए।

चलाइए:  python check_karika.py                 # सब बैच
        python check_karika.py parts/batch04*  # केवल ये

## यह क्यों बना

इस ग्रन्थ में दो अलग क्रम चलते हैं और वे मिलाए जा चुके हैं:

- **पृष्ठ-शीर्ष में** `[ १।१२` — श्री अकलङ्कदेव की **मूल कारिका**
- **पाठ के भीतर** `॥१३९॥` — श्री वादिराजसूरि के **अपने विवरण-श्लोक**

एक बैच ने मुद्रित 21–26 को "कारिका 1।53–1।94" लिख दिया था; वे विवरण-श्लोक 53–94
थे और कारिका 1।9–1।11 चल रही थी। शीर्षक ग़लत हो तो पाठक मूल ग्रन्थ में वह कारिका
ढूँढ़ ही नहीं पाएगा — और यह भूल आँख से नहीं पकड़ी जाती, क्योंकि दोनों अङ्क
दिखने में एक-से हैं।

मूल कारिकाएँ बहुत धीरे बढ़ती हैं। भाग 1 में कारिका 1।13 अकेली मुद्रित 57 से 115
तक फैली है — उनसठ पृष्ठ। इसलिए **यदि किसी बैच में हर § की कारिका बदल रही है, वही
सन्देह का कारण है**: वह प्रायः विवरण-श्लोक का अङ्क होता है।

`karika_map.md` में जहाँ `?` है, वहाँ जाँच चुप रहती है — वह अङ्क स्कैन से खुला
ही नहीं, इसलिए उस पर कोई दावा नहीं।
"""
import glob
import io
import re
import sys
import pathlib

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent

# karika_map.md की पंक्ति:  | 27 | 1।12 | … |
ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|")
# § शीर्षक:  §401 — … (कारिका 1।9)   /   (कारिका 1।[अङ्क अस्पष्ट])
TITLE = re.compile(r"^§\s*(\d+)\s*—\s*(.*)$", re.M)
KARIKA_IN_TITLE = re.compile(r"कारिका\s*([\d।\-–\s]+)")
PAGE = re.compile(r"^\(पृष्ठ (\d+)\)", re.M)

kmap = {}
for line in io.open(HERE / "karika_map.md", encoding="utf-8"):
    m = ROW.match(line)
    if not m or not m.group(1).isdigit():
        continue
    val = m.group(2).strip()
    kmap[int(m.group(1))] = None if ("?" in val or val == "—") else val

args = [a for a in sys.argv[1:] if not a.startswith("--")]
files = []
for a in (args or ["parts/batch*.md"]):
    files.extend(glob.glob(str(HERE / a)) or glob.glob(a))

bad = ok = skipped = 0
for f in sorted(set(files)):
    text = io.open(f, encoding="utf-8").read()
    name = pathlib.Path(f).name
    # § के खण्ड काटिए, ताकि हर § के अपने पृष्ठ मिलें
    hits = list(TITLE.finditer(text))
    probs = []
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.start():end]
        kt = KARIKA_IN_TITLE.search(m.group(2))
        if not kt:
            continue
        claimed = kt.group(1).strip()
        if "अस्पष्ट" in m.group(2):
            skipped += 1
            continue
        pages = [int(p) for p in PAGE.findall(body)]
        expect = {kmap.get(p) for p in pages if kmap.get(p)}
        if not expect:
            skipped += 1
            continue
        # शीर्षक में परास भी हो सकती है ("1।9–1।11"); कोई भी अपेक्षित अङ्क मिले तो ठीक
        if any(e.replace(" ", "") in claimed.replace(" ", "") for e in expect):
            ok += 1
        else:
            probs.append("§%s: शीर्षक कहता है 'कारिका %s', पर मुद्रित %s पर %s है"
                         % (m.group(1), claimed,
                            ",".join(str(p) for p in sorted(set(pages))[:4]),
                            " / ".join(sorted(expect))))
    if probs:
        bad += len(probs)
        print("\n✗ %s" % name)
        for p in probs[:8]:
            print("    - %s" % p)
        if len(probs) > 8:
            print("    … और %d" % (len(probs) - 8))
    else:
        print("✓ %s" % name)

print("\nमिले %d | न मिले %d | बिना दावे के छोड़े %d" % (ok, bad, skipped))
if bad:
    print("\nशीर्षक का अङ्क पृष्ठ-शीर्ष से लीजिए, पाठ के भीतर के ॥N॥ से नहीं।")
sys.exit(1 if bad else 0)
