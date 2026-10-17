# -*- coding: utf-8 -*-
"""§ शीर्षकों की कारिका-संख्या `karika_map.md` से ठीक कीजिए।

चलाइए:  python fix_karika_titles.py          # क्या बदलेगा, केवल दिखाइए
        python fix_karika_titles.py --write  # बदल दीजिए

## यह क्यों

पास-1 के एजेंट शीर्षक में प्रायः **विवरण-श्लोक** का अङ्क लिख बैठे (`कारिका 149`,
`कारिका 1।53–1।94`), जबकि वहाँ चल रही मूल कारिका `1।12` थी। कारण समझ में आता है:
दोनों अङ्क पाठ में पास-पास छपे हैं, और पृष्ठ-शीर्ष का अङ्क इस धुँधले स्कैन में
प्रायः नहीं खुलता, जबकि भीतर का ॥१४९॥ साफ़ दिखता है।

यह सुधार यान्त्रिक है और इसीलिए यहाँ किया जा रहा है, एजेंट से नहीं: **शीर्षक का
वर्णनात्मक अंश ज्यों का त्यों रहता है**, केवल कोष्ठक का अङ्क बदलता है, और वह
`karika_map.md` से आता है — जो शीर्ष-कोने एक-एक पढ़कर बना और जिसकी पूर्व-पक्की
प्रविष्टियों से कोई टकराव नहीं निकला।

जहाँ नक़्शा `?` कहता है, वहाँ `1।[अङ्क अस्पष्ट]` लिखा जाता है — गढ़ा नहीं जाता।
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

ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|")
TITLE = re.compile(r"^(§\s*\d+\s*—\s*)(.*)$", re.M)
PAGE = re.compile(r"^\(पृष्ठ (\d+)\)", re.M)
# शीर्षक के अन्त का कोष्ठक, जिसमें कारिका का दावा है
PAREN = re.compile(r"\s*\((?:मूल\s*)?(?:कारिका|सूत्र)[^)]*\)\s*$")

kmap = {}
for line in io.open(HERE / "karika_map.md", encoding="utf-8"):
    m = ROW.match(line)
    if not m or not m.group(1).isdigit():
        continue
    v = m.group(2).strip()
    kmap[int(m.group(1))] = None if ("?" in v or v == "—") else v

# ---- पहरा: जो फ़ाइल अभी लिखी जा रही है, उसे मत छेड़िए ----
# एक बार यह चलाया गया जब छह बैच-एजेंट अपनी फ़ाइलें लिख ही रहे थे। उनमें से एक ने
# लौटकर बताया कि "मेरे शीर्षक किसी और प्रक्रिया ने बदल दिए" — और वह ठीक कहता था।
# आधी लिखी फ़ाइल पर चलने से शीर्षक आधे-अधूरे बदलते हैं और एजेंट का अपना काम भी
# उलझता है। इसलिए हाल ही में छुई गई फ़ाइलें अपने आप छोड़ दी जाती हैं।
import time

FRESH_MIN = 10
files = sorted(glob.glob(str(HERE / "parts" / "batch*.md")))
busy = [f for f in files
        if (time.time() - pathlib.Path(f).stat().st_mtime) < FRESH_MIN * 60]
if busy:
    print("ये फ़ाइलें पिछले %d मिनट में बदली हैं — सम्भव है कोई एजेंट अभी लिख रहा हो।"
          % FRESH_MIN)
    for f in busy:
        print("   छोड़ी: %s" % pathlib.Path(f).name)
    print("बैच पूरे होने पर फिर चलाइए।\n")
    files = [f for f in files if f not in busy]

changed = untouched = 0
for f in files:
    text = io.open(f, encoding="utf-8").read()
    hits = list(TITLE.finditer(text))
    out, last, local = [], 0, 0
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        body = text[m.start():end]
        pages = sorted({int(p) for p in PAGE.findall(body)})
        ks = [kmap.get(p) for p in pages]
        known = [k for k in ks if k]
        if known:
            lo, hi = known[0], known[-1]
            label = lo if lo == hi else "%s–%s" % (lo, hi)
            # नक़्शे में इस § का कोई पृष्ठ `?` हो तो वह भी बता दीजिए
            if len(known) < len(ks):
                label += " — कुछ पृष्ठों का अङ्क अस्पष्ट"
        else:
            label = "1।[अङ्क अस्पष्ट]"
        # पुराने कोष्ठक का वर्णन बचाने की कोशिश की गई थी, पर वह टूटे शीर्षक
        # बनाती है ("(कारिका 1।1; पर विवरण)") — क्योंकि अङ्क हटते ही बचा
        # हुआ टुकड़ा अपने आप में वाक्य नहीं रहता। विवरण-श्लोक के अङ्क
        # वैसे भी § के पाठ में ॥N॥ रूप में बने रहते हैं, इसलिए कोष्ठक
        # पूरा बदल देना ही साफ़ है।
        tail = ""
        desc = PAREN.sub("", m.group(2)).rstrip()
        new_title = "%s%s (कारिका %s%s)" % (m.group(1), desc, label, tail)
        if new_title.strip() != m.group(0).strip():
            local += 1
            out.append(text[last:m.start()])
            out.append(new_title)
            last = m.end()
    if not local:
        untouched += 1
        continue
    out.append(text[last:])
    new = "".join(out)
    changed += local
    print("%-28s %d शीर्षक" % (pathlib.Path(f).name, local))
    if WRITE:
        io.open(f, "w", encoding="utf-8", newline="").write(new)

print("\n%s: %d शीर्षक | अछूती फ़ाइलें %d"
      % ("बदले" if WRITE else "बदलेंगे", changed, untouched))
if not WRITE and changed:
    print("लिखने के लिए: python fix_karika_titles.py --write")
