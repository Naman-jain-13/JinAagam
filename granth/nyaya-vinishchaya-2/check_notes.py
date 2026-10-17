# -*- coding: utf-8 -*-
"""बैच-फ़ाइलों की तीन यान्त्रिक जाँचें — जो आँख से नहीं पकड़ी जातीं।

चलाइए:  python check_notes.py

## क्या जाँचा जाता है, और क्यों

**1. टिप्पण-अङ्क हर पृष्ठ पर 1 से N तक लगातार हों।**
इस छपाई में टिप्पण-अङ्क हर पृष्ठ पर फिर से (1) से आरम्भ होते हैं। यदि किसी पृष्ठ
पर दर्ज टिप्पणियों की गिनती उसके सबसे बड़े अङ्क के बराबर है, तो कोई टिप्पणी न छूटी
है न दुहराई गई — और यही बात अङ्कों में छेद देखकर पकड़ी जा सकती है। मुद्रित पृष्ठ 18
पर उन्नीस टिप्पण हैं; गिनती और अधिकतम अङ्क दोनों 19 निकले, तभी भरोसा हुआ।

**2. परास का कोई मुद्रित पृष्ठ छूटा तो नहीं।**
फ़ाइल का नाम ही परास बताता है, इसलिए अपेक्षित पृष्ठ-सूची उसी से बनती है।

**3. दो बैचों की सन्धि पर पाठ दुहराया तो नहीं।**
वाक्य प्रायः पृष्ठ के बीच टूटता है। पिछला बैच वाक्य पूरा कर देता है और अगला उसी
अधूरे टुकड़े से फिर आरम्भ कर देता है — तब वही शब्द दो बार छप जाते हैं। बैच 02/03 की
सन्धि पर 'त्रापि समाना' ठीक इसी तरह दो बार आ गया था।
"""
import pathlib
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, OSError):
    pass

HERE = pathlib.Path(__file__).resolve().parent
NOTE = re.compile(r"\(पृष्ठ (\d+), (\d+)\)")
# छपाई में वही अङ्क दो बार हो तो लिखने वाला यह चिह्न लगाता है; तब दुहराव दोष नहीं।
PRINTDUP = "छपे में यह अङ्क दो बार है"
# खाली या नाममात्र की प्रविष्टि — अङ्क तो लगातार रहते हैं, पर पाठ कुछ नहीं।
# एक बार 48 टिप्पण "[सम्पादक की टिप्पणी; यहाँ उद्धृत नहीं]" रूप में लिखे गए
# और जाँच चुप रही, क्योंकि गिनती और क्रम दोनों ठीक थे।
# केवल वही वाक्यांश जो लिखने वाला जान-बूझकर 'यहाँ पाठ नहीं है' कहने को लिखता है।
# '...' यहाँ नहीं रखा जा सकता — वह उद्धरणों के भीतर सर्वत्र आता है और भरी-पूरी
# टिप्पणियों को खाली बता देता था।
EMPTYISH = ("यहाँ उद्धृत नहीं", "उद्धृत नहीं किया", "टिप्पणी का पाठ नहीं",
            "पाठ नहीं लिखा", "पाठ नहीं उतारा", "यहाँ नहीं दिया")
# "(पृष्ठ 46, पूर्व-पृष्ठ की टिप्पणी का शेष)" जैसी प्रविष्टि — अङ्क के स्थान पर शब्द।
# लम्बा उद्धरण पृष्ठ के नीचे पूरा न बैठने पर अगले पृष्ठ पर बिना अङ्क के चलता है।
# वह अलग टिप्पणी नहीं; उसे आरम्भ वाले पृष्ठ की प्रविष्टि में मिलाना है।
CONT = re.compile(r"\(पृष्ठ (\d+),\s*([^)\d\s][^)]*)\)")
# '(पृष्ठ N, जारी)' मूल-पाठ का अपना पृष्ठ-सन्धि चिह्न है (मूल एक पृष्ठ पर
# दुहराया जाता है), टिप्पण-पूँछ नहीं — उसे यहीं छोड़ दीजिए।
CONT_SKIP = {"जारी"}
PAGE = re.compile(r"^\(पृष्ठ (\d+)\)", re.M)
NAME = re.compile(r"batch(\d+)_p(\d+)-(\d+)")
# इस ग्रन्थ में बैच-फ़ाइल का नाम **मुद्रित** पृष्ठ बताता है (batch01_p003-008 =
# मुद्रित 3–8), स्कैन नहीं। सहोदर ग्रन्थ में नाम स्कैन-संख्या का था और यहाँ से
# `मुद्रित = स्कैन − 311` घटाया जाता था; वह पंक्ति ज्यों की त्यों चली आई थी और
# हर बैच पर ✗ दे रही थी, क्योंकि 3 − 311 ऋणात्मक है।
#
# यहाँ कोई अन्तर घटाना ही नहीं है। और घटाना होता भी तो एक अङ्क से नहीं चलता —
# इस ग्रन्थ का अन्तर 66/67/65/64 बदलता है; उसके लिए `page.py` है।


def mool(text):
    """हर § का भाग 1 — टिप्पण और कोष्ठक-सूचनाएँ हटाकर।"""
    out = []
    for blk in re.split(r"(?m)^##\s", text):
        if not blk.startswith("1. मूल पाठ"):
            continue
        body = blk.split("\n", 1)[1]
        body = NOTE.sub("", body)
        body = re.sub(r"^\(.*?\)\s*$", "", body, flags=re.M)
        body = re.sub(r"सम्पादकीय टिप्पण:.*", "", body, flags=re.S)
        out.append(body)
    return "\n".join(out)


def overlap(a, b, lo=12, hi=90):
    """a के अन्त और b के आरम्भ का सबसे लम्बा साझा टुकड़ा।"""
    a = re.sub(r"\s+", " ", a).strip()
    b = re.sub(r"\s+", " ", b).strip()
    for n in range(min(hi, len(a), len(b)), lo - 1, -1):
        if a[-n:] == b[:n]:
            return a[-n:]
    return None


def main():
    files = sorted((HERE / "parts").glob("batch*.md"))
    if not files:
        print("कोई बैच-फ़ाइल नहीं मिली।")
        return 1
    bad = 0
    prev_name = prev_mool = None
    for f in files:
        m = NAME.search(f.name)
        if not m:
            print(f"  {f.name}: नाम से परास नहीं निकली — छोड़ा")
            continue
        s_from, s_to = int(m.group(2)), int(m.group(3))
        want = list(range(s_from, s_to + 1))
        t = f.read_text(encoding="utf-8")

        notes, note_txt = {}, {}
        for m in NOTE.finditer(t):
            p, n = int(m.group(1)), int(m.group(2))
            notes.setdefault(p, []).append(n)
            tail = t[m.end(): t.find(chr(10), m.end())]
            note_txt.setdefault((p, n), []).append(tail)
        seen = sorted(set(int(x) for x in PAGE.findall(t)))

        probs = []
        missing = [p for p in want if p not in seen]
        if missing:
            probs.append(f"मुद्रित पृष्ठ दर्ज नहीं: {missing}")
        extra = [p for p in seen if p not in want]
        if extra:
            probs.append(f"परास से बाहर के पृष्ठ: {extra}")
        for p in sorted(notes):
            got = sorted(notes[p])
            dup = sorted({n for n in got if got.count(n) > 1})
            # छपाई की अपनी भूल, जिसे लिखने वाले ने चिह्नित कर दिया हो, दोष नहीं।
            # गेट लिप्यन्तरण की भूल पकड़ने के लिए है, छपाई को सुधारने के लिए नहीं।
            dup = [n for n in dup
                   if not any(PRINTDUP in x for x in note_txt.get((p, n), []))]
            if dup:
                probs.append(f"पृष्ठ {p}: टिप्पण-अङ्क दुहराया — {dup} "
                             f"(यदि छपे में ही दो बार है तो उस टिप्पणी के अन्त में "
                             f"[{PRINTDUP}] लिख दीजिए)")
            hole = [n for n in range(1, max(got) + 1) if n not in got]
            if hole:
                probs.append(f"पृष्ठ {p}: टिप्पण-अङ्क बीच से गायब — {hole} "
                             f"(दर्ज {len(set(got))}, अधिकतम {max(got)})")

        # टिप्पण-रहित पृष्ठ — इस ग्रन्थ में ऐसा पृष्ठ प्रायः होता ही नहीं।
        # मुद्रित 86 की पूरी टिप्पण-पंक्ति एक बार छूट गई थी और जाँच चुप रही,
        # क्योंकि पृष्ठ मूल में दर्ज था और शेष पृष्ठों के अङ्क लगातार थे।
        # जिस पृष्ठ पर छपे में सचमुच कोई पाद-टिप्पण नहीं है, उसे `no_notes_pages.txt`
        # में एक पंक्ति में पृष्ठ-संख्या लिखकर घोषित कीजिए (`#` के बाद कारण)।
        # घोषणा पुस्तक में नहीं जाती — इसलिए अलग फ़ाइल है, § के भीतर कुछ नहीं जोड़ना पड़ता।
        # चेतावनी इसलिए बनी रहती है कि छूटी हुई पंक्ति बिना घोषणा पकड़ी जाए।
        declared = set()
        _f = pathlib.Path(__file__).resolve().parent / "no_notes_pages.txt"
        if _f.exists():
            for _ln in _f.read_text(encoding="utf-8").splitlines():
                _m = re.match(r"\s*(\d+)", _ln)
                if _m:
                    declared.add(int(_m.group(1)))
        for p in seen:
            if p in want and not notes.get(p) and p not in declared:
                probs.append(f"पृष्ठ {p}: एक भी सम्पादकीय टिप्पण दर्ज नहीं — "
                             f"इस ग्रन्थ में ऐसा पृष्ठ विरल है; छपे पृष्ठ के नीचे "
                             f"देख लीजिए कि सचमुच कोई टिप्पणी नहीं है")

        empty = []
        for (p, n), xs in note_txt.items():
            if p not in want:
                continue
            body = " ".join(xs).strip()
            # [अस्पष्ट] से आरम्भ होने वाली टिप्पणी खाली नहीं है — वह ईमानदारी से
            # 'यह पढ़ा नहीं गया' कहती है, और वह दर्ज करने योग्य बात है।
            if "अस्पष्ट" in body:
                continue
            # [उद्धरण — ...] अब टिप्पणी की असली सामग्री है (स्थल-निर्देश नीति,
            # 2026-10-15) — उसे खाली मानकर मत हटाइए। केवल हमारे अपने
            # प्रक्रिया-चिह्न ([छपे में...], [यह टिप्पणी...], [NN]) हटाकर नापिए।
            core = re.sub(r"\[(?!उद्धरण)[^\]]*\]", "", body).strip(" ।|")
            if len(core) < 3 or any(e in body for e in EMPTYISH):
                empty.append((p, n))
        if empty:
            pages = sorted({p for p, _ in empty})
            probs.append(f"{len(empty)} टिप्पण खाली या नाममात्र के हैं "
                         f"(पृष्ठ {pages[:6]}{'…' if len(pages) > 6 else ''}) — "
                         f"अङ्क भर देने से टिप्पणी नहीं बनती; पाठ चाहिए")

        for p, what in CONT.findall(t):
            if what.strip() in CONT_SKIP:
                continue
            probs.append(f"पृष्ठ {p}: बिना अङ्क की टिप्पणी-पूँछ ‘{what.strip()[:34]}…’ — "
                         f"यह मुद्रित {int(p)-1} की किसी टिप्पणी का शेष है; "
                         f"उसी प्रविष्टि में मिला दीजिए")

        cur = mool(t)
        if prev_mool is not None:
            ov = overlap(prev_mool, cur)
            if ov:
                probs.append(f"{prev_name} की सन्धि पर पाठ दुहराया: ‘{ov[:60]}…’")

        n_notes = sum(len(v) for v in notes.values())
        if probs:
            bad += 1
            print(f"\n✗ {f.name}  ({len(seen)} पृष्ठ, {n_notes} टिप्पण)")
            for p in probs:
                print(f"    - {p}")
        else:
            print(f"✓ {f.name}  — {len(seen)} पृष्ठ, {n_notes} टिप्पण, अङ्क लगातार")
        prev_name, prev_mool = f.name, cur

    print(f"\n{len(files)} फ़ाइलें; {bad} में कुछ खटका।")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
