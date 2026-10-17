# -*- coding: utf-8 -*-
"""सब § को 1 से लगातार क्रम में लाइए।

चलाइए:  python renumber.py          # क्या बदलेगा
        python renumber.py --write

## यह क्यों चाहिए

पास 1 में हर बैच को सौ का अपना खण्ड दिया गया था — batch01 → §101, batch02 → §201,
batch03 → §301 … — ताकि समानान्तर चलते बैचों के क्रमांक आपस में न टकराएँ। उसका
काम हो चुका; अब वे खण्ड केवल छेद हैं।

**यह addenda लिखने से पहले चलना चाहिए।** पास 2 में हर § की अपनी फ़ाइल बनती है
(`addenda/s0007.md`), और वह नाम § के क्रमांक से बनता है। एक बार addenda बन जाने
के बाद क्रमांक बदलना दोनों को अलग कर देगा।

## यह क्या सँभालता है

- **भीतरी सन्दर्भ।** § की व्याख्या में "देखें §207" जैसे सन्दर्भ हैं; वे भी
  साथ बदलते हैं। बिना इसके वे किसी और अनुच्छेद पर जा गिरते।
- **क्रम।** फ़ाइलें मुद्रित-पृष्ठ के क्रम में पढ़ी जाती हैं (`batchNN_pSSS-EEE`),
  इसलिए नया क्रमांक पुस्तक के अपने क्रम में बैठता है।

## यह क्या नहीं करता

भाग 1 (मूल पाठ) में छपे `॥५७३॥` जैसे अङ्क **विवरण-श्लोक** के हैं और उन्हें यह
नहीं छूता। केवल `§` से आरम्भ होने वाले क्रमांक बदलते हैं।
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
WRITE = "--write" in sys.argv
NAME = re.compile(r"batch(\d+)_p(\d+)-(\d+)")
TITLE = re.compile(r"^§\s*(\d+)\s*—", re.M)
REF = re.compile(r"§\s*(\d+)")

files = sorted(glob.glob(str(HERE / "parts" / "batch*.md")),
               key=lambda f: int(NAME.search(pathlib.Path(f).name).group(2)))

# पहले पूरा नक़्शा बनाइए — पुराना क्रमांक → नया — तभी सन्दर्भ भी ठीक बदलेंगे
old_order = []
for f in files:
    text = io.open(f, encoding="utf-8").read()
    old_order.extend(int(m.group(1)) for m in TITLE.finditer(text))

if len(old_order) != len(set(old_order)):
    dup = sorted({n for n in old_order if old_order.count(n) > 1})
    sys.exit("रुकिए — ये § क्रमांक एक से अधिक बार हैं: %s" % dup[:20])

# ---- पहरा: पास 1 पूरा हुए बिना मत चलाइए ----
# चलते हुए बैच अपने सौ-वाले खण्ड लेकर आते हैं (§3301, §3401 …)। बीच में
# पुनःक्रमांकन कर देने से वे खण्ड पहले से भरे हुए निकलेंगे और क्रमांक टकराएँगे।
# इसलिए यह तभी चलता है जब मुद्रित 3 से 545 तक कोई पृष्ठ छूटा न हो।
pages = set()
for f in files:
    pages.update(int(p) for p in re.findall(
        r"^\(पृष्ठ (\d+)\)", io.open(f, encoding="utf-8").read(), re.M))
missing = [p for p in range(3, 546) if p not in pages and p not in (464, 465, 521)]
if missing and "--anyway" not in sys.argv:
    lo = missing[0]
    print("पास 1 अभी पूरा नहीं है — मुद्रित %d से आगे %d पृष्ठ बाक़ी हैं।"
          % (lo, len(missing)))
    print("पुनःक्रमांकन **पास 1 पूरा होने के बाद** और **addenda लिखने से पहले**")
    print("चलता है। अभी चलाने पर चलते हुए बैचों के क्रमांक टकराएँगे।")
    print("(सचमुच चलाना हो तो --anyway जोड़िए — पर पहले सोच लीजिए।)")
    sys.exit(1)

mapping = {old: new for new, old in enumerate(old_order, start=1)}
print("§ कुल: %d  (पुराना %d–%d → नया 1–%d)"
      % (len(old_order), min(old_order), max(old_order), len(old_order)))

shifted = sum(1 for o, n in mapping.items() if o != n)
print("बदलेंगे: %d" % shifted)

if not WRITE:
    print("\nनमूना (पहले दस):")
    for o in old_order[:10]:
        print("   §%-5d → §%d" % (o, mapping[o]))
    print("\nलिखने के लिए: python renumber.py --write")
    sys.exit(0)

changed_refs = 0
for f in files:
    text = io.open(f, encoding="utf-8").read()

    def sub(m):
        global changed_refs
        o = int(m.group(1))
        if o not in mapping:
            return m.group(0)           # किसी और ग्रन्थ का § — छेड़िए मत
        if mapping[o] != o:
            changed_refs += 1
        return "§%d" % mapping[o]

    io.open(f, "w", encoding="utf-8", newline="").write(REF.sub(sub, text))

print("लिखा। § और भीतरी सन्दर्भ मिलाकर %d स्थान बदले।" % changed_refs)
print("अब `python check_notes.py` और `python check_shloka.py` एक बार चला लीजिए।")
