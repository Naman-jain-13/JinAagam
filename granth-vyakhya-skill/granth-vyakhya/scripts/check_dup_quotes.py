# -*- coding: utf-8 -*-
"""एक ही श्लोक दो जगह उद्धृत — और दोनों जगह हमारा पाठ अलग।

ग्रन्थकार बड़े ग्रन्थ में कई श्लोक दो-तीन बार उद्धृत करते हैं। यदि हमारे दो
लिप्यन्तरण आपस में ही भिन्न हैं तो एक अवश्य ग़लत है — और यह बात किसी बाहरी संस्करण
के बिना, केवल अपने पाठ के भीतर से पकड़ी जा सकती है। इसलिए यह जाँच सबसे सस्ती है:
न स्कैन देखना पड़ता है, न कोई संस्करण उतारना पड़ता है।

जहाँ दोनों पाठ पूरे मिल जाते हैं वहाँ चुप रहती है; जहाँ मिलते-जुलते हैं पर एक-दो
शब्द बदले हैं, वहीं बताती है — वही जगह स्कैन में देखने की है।

चलाइए:  python check_dup_quotes.py
        python check_dup_quotes.py --min 0.80
"""
import sys
import difflib
import collections

import check_citations as CC

SAME = 0.999        # इससे ऊपर = दोनों पाठ एक ही; कुछ कहने की ज़रूरत नहीं
NEAR = 0.75         # इससे नीचे = अलग-अलग श्लोक, संयोग से मिलते-जुलते
MIN_LEN = 24


def collect():
    out = []
    for f in sorted(CC.HERE.glob("parts/batch*.md")):
        for sec, page, q in CC.part1_quotes(f):
            sk = CC.skeleton_of(q)
            if len(sk) >= MIN_LEN:
                out.append((sk, f.name, sec, page, " ".join(q.split())))
    return out


def main(near=NEAR):
    items = collect()
    print(f"{len(items)} उद्धरण जाँचे "
          f"जा रहे हैं\n")

    # पहले मोटी छँटाई — साझा अक्षर-टुकड़े से, वरना हर जोड़ी तोलनी पड़ती
    buckets = collections.defaultdict(list)
    K = 14
    for i, (sk, *_rest) in enumerate(items):
        for j in range(0, max(1, len(sk) - K), 3):
            buckets[sk[j:j + K]].append(i)

    pairs = set()
    for idxs in buckets.values():
        if len(idxs) < 2 or len(idxs) > 40:
            continue
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                pairs.add((min(idxs[a], idxs[b]), max(idxs[a], idxs[b])))

    same = 0
    found = []
    for a, b in pairs:
        ska, skb = items[a][0], items[b][0]
        r = difflib.SequenceMatcher(None, ska, skb, autojunk=False).ratio()
        if r >= SAME:
            same += 1
            continue
        if r < near:
            continue
        found.append((r, a, b))

    print(f"दो जगह पूरी तरह "
          f"समान: {same} | "
          f"मिलते-जुलते पर "
          f"भिन्न: {len(found)}\n")

    for r, a, b in sorted(found):
        _, fa, sa, pa, qa = items[a]
        _, fb, sb, pb, qb = items[b]
        print(f"--- {sa} (मु. {pa}, {fa})  ↔  "
              f"{sb} (मु. {pb}, {fb})   मेल {r:.0%}")
        sm = difflib.SequenceMatcher(None, qa.split(), qb.split(), autojunk=False)
        for t, i1, i2, j1, j2 in sm.get_opcodes():
            if t == "equal":
                continue
            x = " ".join(qa.split()[i1:i2]) or "—"
            y = " ".join(qb.split()[j1:j2]) or "—"
            print(f"    {sa}: {x[:80]}")
            print(f"    {sb}: {y[:80]}")
        print()


if __name__ == "__main__":
    n = NEAR
    if "--min" in sys.argv:
        n = float(sys.argv[sys.argv.index("--min") + 1])
    main(n)
