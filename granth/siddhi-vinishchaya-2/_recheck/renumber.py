# -*- coding: utf-8 -*-
"""§ पुनःक्रमांकन — हर बैच के अपने स्थानीय § अङ्कों को 1..N लगातार क्रम में बदलता है,
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

    # पास 1 — फ़ाइल-क्रम में सारे पुराने (स्थानीय, दुहराए हुए) § अङ्क इकट्ठा
    # कीजिए; हर फ़ाइल अपने आप में 1 से गिनती शुरू करती है, इसलिए यहाँ
    # "कौन-सा टोकन किस फ़ाइल का है" याद रखना है, केवल अङ्क नहीं।
    old_order = []   # [(file_index, local_num), ...] फ़ाइल-क्रम और पाठ-क्रम में
    for fi, f in enumerate(files):
        t = f.read_text(encoding="utf-8")
        for m in SEC_HEAD.finditer(t):
            old_order.append((fi, int(m.group(2))))

    mapping_by_file = [dict() for _ in files]  # mapping_by_file[fi][local_num] = new_num
    for i, (fi, local) in enumerate(old_order):
        mapping_by_file[fi][local] = i + 1

    print(f"{len(old_order)} § मिले, नया क्रम 1..{len(old_order)} बनेगा।")

    # पास 2 — हर फ़ाइल में शीर्षक और "देखें §N" दोनों बदलिए (अपनी ही फ़ाइल के
    # मानचित्र से — "देखें §N" सदा उसी फ़ाइल के भीतर की किसी पुरानी § को
    # इंगित करता है, दूसरी फ़ाइल को नहीं, क्योंकि अङ्क स्वयं हर फ़ाइल में दुहराए
    # गए हैं और बिना फ़ाइल-सन्दर्भ के यह पता नहीं चल सकता कि कौन-सी असली है)।
    for fi, f in enumerate(files):
        t = f.read_text(encoding="utf-8")
        mapping = mapping_by_file[fi]

        def head_sub(m):
            old = int(m.group(2))
            return f"{m.group(1)}{mapping[old]}{m.group(3)}"

        def see_sub(m):
            old = int(m.group(2))
            new = mapping.get(old)
            if new is None:
                print(f"  ! {f.name}: 'देखें §{old}' — यह अङ्क इस फ़ाइल की किसी § शीर्षक में नहीं मिला, छोड़ा")
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

    if apply:
        import json
        flat = {}
        for fi, f in enumerate(files):
            for local, new in mapping_by_file[fi].items():
                flat[f"{f.name}:{local}"] = new
        (HERE / "renumber_map.json").write_text(
            json.dumps(flat, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nमानचित्र सहेजा: {HERE / 'renumber_map.json'}")
    else:
        print("\nयह केवल पूर्वावलोकन है। असली बदलाव के लिए: python renumber.py --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
