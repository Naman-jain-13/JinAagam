# -*- coding: utf-8 -*-
"""§ पुनःक्रमांकन — पुराने (जान-बूझकर गैप वाले) § अङ्कों को 1..N लगातार क्रम में बदलता है,
और शरीर में आने वाले "देखें §N" जैसे आन्तरिक सन्दर्भ भी साथ अद्यतन करता है।

चलाइए (dry-run पहले):  python renumber.py
असली बदलाव:             python renumber.py --apply
"""
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
PARTS = HERE.parent / "parts"

SEC_HEAD = re.compile(r"^(§)\s*(\d+)(\s*[—–-]\s*)", re.M)
SEE_REF = re.compile(r"(देखें\s*§\s*)(\d+)")


def main():
    apply = "--apply" in sys.argv
    files = sorted(PARTS.glob("batch*.md"))

    # पास 1 — फ़ाइल-क्रम में सारे पुराने § अङ्क इकट्ठा कीजिए, नया मानचित्र बनाइए।
    old_order = []
    for f in files:
        t = f.read_text(encoding="utf-8")
        for m in SEC_HEAD.finditer(t):
            old_order.append(int(m.group(2)))

    if len(old_order) != len(set(old_order)):
        dupes = [n for n in set(old_order) if old_order.count(n) > 1]
        print("रुकिए — पुराने § अङ्कों में दुहराव मिला:", dupes)
        return 1

    mapping = {old: i + 1 for i, old in enumerate(old_order)}
    print(f"{len(old_order)} § मिले, नया क्रम 1..{len(old_order)} बनेगा।")

    # पास 2 — हर फ़ाइल में शीर्षक और "देखें §N" दोनों बदलिए।
    for f in files:
        t = f.read_text(encoding="utf-8")

        def head_sub(m):
            old = int(m.group(2))
            return f"{m.group(1)}{mapping[old]}{m.group(3)}"

        def see_sub(m):
            old = int(m.group(2))
            new = mapping.get(old)
            if new is None:
                print(f"  ! {f.name}: 'देखें §{old}' — यह अङ्क किसी § शीर्षक में नहीं मिला, छोड़ा")
                return m.group(0)
            return f"{m.group(1)}{new}"

        t2 = SEC_HEAD.sub(head_sub, t)
        t2 = SEE_REF.sub(see_sub, t2)

        if t2 != t:
            if apply:
                f.write_text(t2, encoding="utf-8")
                print(f"  ✓ {f.name} अद्यतन")
            else:
                n_head = len(SEC_HEAD.findall(t))
                n_see = len(SEE_REF.findall(t))
                print(f"  (dry-run) {f.name}: {n_head} शीर्षक, {n_see} 'देखें' सन्दर्भ बदलेंगे")

    # मानचित्र सहेज दीजिए — भविष्य में addenda/sNNNN.md बनते समय यही नया अङ्क चाहिए।
    if apply:
        import json
        (HERE / "renumber_map.json").write_text(
            json.dumps({str(k): v for k, v in mapping.items()}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"\nमानचित्र सहेजा: {HERE / 'renumber_map.json'}")
    else:
        print("\nयह केवल पूर्वावलोकन है। असली बदलाव के लिए: python renumber.py --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
