#!/usr/bin/env python3
# groups.json बनाता है: topic_map.md के विषय-विभाजनों को नए (पुनःक्रमांकित) § नम्बरों से जोड़कर।
import re, json, glob

WORK = str(__import__("pathlib").Path(__file__).resolve().parent)

HEADER_RE = re.compile(
    r'^§\s*(\d+)\s*[—–-]\s*(.*?)\s*\(.*?मुद्रित पृष्ठ\s*(\d+)', re.MULTILINE)

# 1) सभी § की (num, page) सूची, फ़ाइल-क्रम में
sections = []
for f in sorted(glob.glob(WORK + r"\parts\batch*.md")):
    text = open(f, encoding='utf-8').read()
    for m in HEADER_RE.finditer(text):
        num = int(m.group(1))
        page = int(m.group(3))
        sections.append((num, page))

sections.sort(key=lambda x: x[0])
assert [s[0] for s in sections] == list(range(1, len(sections) + 1))

def first_section_at_or_after(page):
    for num, p in sections:
        if p >= page:
            return num
    return sections[-1][0]

# 2) topic_map.md पार्स करें
tm_text = open(WORK + r"\topic_map.md", encoding='utf-8').read()
parichhed_blocks = re.split(r'^## (.+)$', tm_text, flags=re.MULTILINE)[1:]
# parichhed_blocks = [name1, body1, name2, body2, ...]

groups = {}
groups["1"] = "[ प्रथम परिच्छेद — मंगलाचरण, इष्टदेव-वन्दना एवं धर्मतीर्थंकरता की परीक्षा ]"

row_re = re.compile(r'^\|\s*(.+?)\s*\|\s*(\d+)–\d+\s*\|$', re.MULTILINE)

for i in range(0, len(parichhed_blocks), 2):
    parichhed_name = parichhed_blocks[i].strip()
    body = parichhed_blocks[i + 1]
    rows = row_re.findall(body)
    for idx, (topic, page_start) in enumerate(rows):
        num = first_section_at_or_after(int(page_start))
        label = topic
        if idx == 0 and parichhed_name == "द्वितीय परिच्छेद":
            label = f"द्वितीय परिच्छेद — {topic}"
        key = str(num)
        if key in groups:
            continue  # collision (topic starts at same § as an earlier heading) — keep first
        groups[key] = f"[ {label} ]"

# संख्या-क्रम से लिखें
ordered = {k: groups[k] for k in sorted(groups, key=int)}
json.dump(ordered, open(WORK + r"\groups.json", "w", encoding='utf-8'), ensure_ascii=False, indent=1)
print("कुल शीर्षक:", len(ordered))
for k, v in ordered.items():
    print(k, v)
