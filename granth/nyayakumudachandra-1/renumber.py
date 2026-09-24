#!/usr/bin/env python3
"""§ का अन्तिम, सतत पुनःक्रमांकन (1..N) — parts/, addenda/, backmatter/ तीनों में।
मूल आधार: parts/batchNN_*.md में § शीर्षकों का फ़ाइल-नाम-क्रम (= मुद्रित-पृष्ठ-क्रम) ही नया क्रम है।
"""
import re, os, glob, json, shutil, sys

WORK = str(__import__("pathlib").Path(__file__).resolve().parent)
PARTS = os.path.join(WORK, "parts")
ADDENDA = os.path.join(WORK, "addenda")
BACKMATTER = os.path.join(WORK, "backmatter")

HEADER_RE = re.compile(r'^§\s*(\d+)\s*[—–-]', re.MULTILINE)
ANY_SECTION_RE = re.compile(r'§\s*(\d+)')

def build_mapping():
    parts_files = sorted(glob.glob(os.path.join(PARTS, "batch*.md")))
    mapping = {}
    new_num = 1
    order_log = []
    for f in parts_files:
        text = open(f, encoding='utf-8').read()
        seen_in_file = []
        for m in HEADER_RE.finditer(text):
            old = int(m.group(1))
            if old not in mapping:
                mapping[old] = new_num
                seen_in_file.append((old, new_num))
                new_num += 1
        order_log.append((os.path.basename(f), seen_in_file))
    return mapping, order_log, new_num - 1

def substitute_in_text(text, mapping):
    def repl(m):
        old = int(m.group(1))
        new = mapping.get(old)
        if new is None:
            return m.group(0)  # leave unmapped numbers untouched (shouldn't happen)
        return f"§{new}"
    return ANY_SECTION_RE.sub(repl, text)

def main():
    mapping, order_log, total = build_mapping()
    print(f"कुल §: {total}")

    json.dump({str(k): v for k, v in mapping.items()},
               open(os.path.join(WORK, "renumber_map.json"), "w", encoding="utf-8"),
               ensure_ascii=False, indent=0)

    # sanity: mapping must be a bijection onto 1..total
    assert sorted(mapping.values()) == list(range(1, total + 1)), "मैपिंग सतत नहीं है!"

    # 1) parts/*.md — सभी §-उल्लेख (शीर्षक + आन्तरिक सन्दर्भ) बदलें
    for f in sorted(glob.glob(os.path.join(PARTS, "batch*.md"))):
        text = open(f, encoding='utf-8').read()
        new_text = substitute_in_text(text, mapping)
        if new_text != text:
            open(f, "w", encoding='utf-8').write(new_text)
    print("parts/ अद्यतन।")

    # 2) backmatter/*.md — सभी §-उल्लेख बदलें
    for f in sorted(glob.glob(os.path.join(BACKMATTER, "*.md"))):
        text = open(f, encoding='utf-8').read()
        new_text = substitute_in_text(text, mapping)
        if new_text != text:
            open(f, "w", encoding='utf-8').write(new_text)
    print("backmatter/ अद्यतन।")

    # 3) addenda/*.md — फ़ाइल के भीतर का पाठ (यदि कहीं § उल्लेख बचा हो) + फ़ाइल का नाम दोनों बदलें
    addenda_files = sorted(glob.glob(os.path.join(ADDENDA, "s*.md")))
    file_num_re = re.compile(r'^s0*(\d+)\.md$', re.IGNORECASE)
    rename_plan = []  # (old_path, old_num)
    missing = []
    for f in addenda_files:
        base = os.path.basename(f)
        m = file_num_re.match(base)
        if not m:
            print("अनपहचाना नाम:", base)
            continue
        old_num = int(m.group(1))
        if old_num not in mapping:
            missing.append(old_num)
            continue
        rename_plan.append((f, old_num))

    if missing:
        print("मैपिंग में नहीं मिले (छोड़े गए):", missing)

    # पहले content substitute करें (नाम बदलने से पहले, पुराने पथ पर)
    for f, old_num in rename_plan:
        text = open(f, encoding='utf-8').read()
        new_text = substitute_in_text(text, mapping)
        if new_text != text:
            open(f, "w", encoding='utf-8').write(new_text)

    # collision-safe rename: पहले सब temp नाम पर, फिर final नाम पर
    tmp_paths = []
    for f, old_num in rename_plan:
        tmp = f + ".tmp"
        shutil.move(f, tmp)
        tmp_paths.append((tmp, mapping[old_num]))

    for tmp, new_num in tmp_paths:
        final = os.path.join(ADDENDA, f"s{new_num:04d}.md")
        shutil.move(tmp, final)

    print(f"addenda/ अद्यतन — {len(rename_plan)} फ़ाइलें renamed.")

    # rename summary sample
    print("नमूना (पहले 5 एवं अन्तिम 5):")
    for old_num, new_num in list(mapping.items())[:5]:
        pass

if __name__ == "__main__":
    main()
