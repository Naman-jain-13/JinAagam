# -*- coding: utf-8 -*-
"""§ शीर्षकों की कारिका-संख्या हटाकर `1।[अङ्क अस्पष्ट]` कीजिए।

चलाइए:  python neutralize_karika.py          # क्या बदलेगा
        python neutralize_karika.py --write

## यह क्यों

शीर्षकों में कारिका-संख्या दो रास्तों से आई थी, और **दोनों अविश्वसनीय निकले:**

1. कुछ एजेंटों ने पाठ के भीतर छपे `॥१४९॥` को कारिका मान लिया — वे श्री
   वादिराजसूरि के अपने विवरण-श्लोक हैं, मूल कारिका नहीं।
2. फिर `karika_map.md` से सुधार किया गया, पर वह तालिका शीर्ष-कोने के नन्हे अङ्क
   पढ़कर बनी थी — और इस स्कैन में **`१।३` तथा `१।१३` का भेद खुलता ही नहीं**,
   बीच का `१` दब जाता है। तालिका के भीतर विरोध भी है: मुद्रित 21 पर `1।9` और
   मुद्रित 57 पर `1।3` — कारिका घटती नहीं।

ग़लत अङ्क वाला शीर्षक पाठक को मूल ग्रन्थ में ग़लत जगह भेजता है, और वह उसे पकड़
नहीं सकता। **खाली स्थान ग़लत अङ्क से भला है** — इसलिए जब तक पाठ-आधारित नक़्शा न
बने, सब शीर्षकों में `1।[अङ्क अस्पष्ट]` रहेगा।

शीर्षक का वर्णनात्मक अंश ज्यों का त्यों रहता है; केवल कोष्ठक बदलता है।
"""
import glob
import io
import re
import sys
import pathlib
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent
WRITE = "--write" in sys.argv
TITLE = re.compile(r"^(§\s*\d+\s*—\s*)(.*)$", re.M)
PAREN = re.compile(r"\s*\((?:मूल\s*)?(?:कारिका|सूत्र)[^)]*\)\s*$")
NEUTRAL = "(कारिका 1।[अङ्क अस्पष्ट])"

# जो फ़ाइल अभी लिखी जा रही हो उसे मत छेड़िए — एक बार ऐसा करने पर एक एजेंट का
# लिखा हुआ मिट गया था।
files = sorted(glob.glob(str(HERE / "parts" / "batch*.md")))
busy = [f for f in files if (time.time() - pathlib.Path(f).stat().st_mtime) < 600]
for f in busy:
    print("छोड़ी (हाल में बदली): %s" % pathlib.Path(f).name)
files = [f for f in files if f not in busy]

changed = 0
for f in files:
    text = io.open(f, encoding="utf-8").read()
    local = 0

    def repl(m):
        global local
        desc = PAREN.sub("", m.group(2)).rstrip()
        new = "%s%s %s" % (m.group(1), desc, NEUTRAL)
        if new.strip() != m.group(0).strip():
            local += 1
            return new
        return m.group(0)

    new_text = TITLE.sub(repl, text)
    if local:
        changed += local
        print("%-28s %d शीर्षक" % (pathlib.Path(f).name, local))
        if WRITE:
            io.open(f, "w", encoding="utf-8", newline="").write(new_text)

print("\n%s: %d शीर्षक" % ("बदले" if WRITE else "बदलेंगे", changed))
if not WRITE and changed:
    print("लिखने के लिए: --write")
