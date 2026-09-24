"""JinAagam Encyclopedia — corpus indexer.

Walks every granth/<name> folder (markdown) plus the Pramana Pariksha .docx (no md source
survives) and produces one normalised dataset:

    data/meta.json          granth list + every section's id/number/title/page/group   (small, always loaded)
    data/full/<gid>.json    full text of every section of that granth                  (loaded on demand)
    data/terms.json         glossary entries merged from all granths
    data/stats.json         counts, for the About screen

Run:  python build_index.py
"""
import json, os, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # E:\Projects\JinAagam
OUT = Path(__file__).resolve().parent / "data"
DEV = "०१२३४५६७८९"


def dev2en(s: str) -> str:
    return "".join(str(DEV.index(c)) if c in DEV else c for c in s)


def clean(s: str) -> str:
    """Strip markdown emphasis/links so search and snippets stay readable."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    s = re.sub(r"`(.+?)`", r"\1", s)
    s = re.sub(r"\[(.+?)\]\(.*?\)", r"\1", s)
    return s.strip()


def page_of(title: str):
    m = re.search(r"मुद्रित पृष्ठ\s*([0-9०-९]+)", title)
    if m:
        return dev2en(m.group(1))
    m = re.search(r"\(पृष्ठ\s*([0-9०-९]+)\)", title)
    return dev2en(m.group(1)) if m else ""


# --------------------------------------------------------------------------- corpora

CORPORA = [
    # id, folder, display title (hi), display title (en), language of content
    ("asht",   "granth/ashtasahasri",    "अष्टसहस्री",                 "Ashtasahasri",              "hi"),
    ("bruhat", "granth/bruhat-sarvagya-siddhi", "बृहत् सर्वज्ञसिद्धि",          "Bruhat Sarvagya Siddhi",    "hi"),
    ("laghu",  "granth/laghu-sarvagya-siddhi", "लघु सर्वज्ञसिद्धि",           "Laghu Sarvagya Siddhi",     "hi"),
    ("nyaya",  "granth/nyayakumudachandra-1",      "न्यायकुमुदचन्द्र",            "Nyayakumudachandra",        "hi"),
    ("abhi",   "granth/abhishek-path-sangrah",        "अभिषेक पाठ संग्रह",           "Abhishek Path Sangrah",     "hi"),
]

PART_ORDER = ["मूल पाठ", "मूल संस्कृत पाठ", "हिन्दी अनुवाद", "जैनागम", "पूरक", "सरल उदाहरण",
              "तुलनात्मक", "सन्दर्भ"]


def part_key(head: str) -> str:
    """Normalise the '## 3. जैनागम के अनुसार विस्तृत व्याख्या' style headings."""
    h = re.sub(r"^[0-9०-९]+[.)]\s*", "", head).strip()
    return h


# --------------------------------------------------------------------------- markdown parsers

def parse_section_file(path: Path, sections: dict, order: list, group_state: dict):
    """Handles §-style files (ashtasahasri / bruhat / laghu / nyayakumud)."""
    cur = None
    part = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        s = line.strip()
        m = re.match(r"^§\s*([0-9०-९]+)\s*[—–-]\s*(.*)$", s)
        if m:
            num = dev2en(m.group(1))
            cur = num
            sections.setdefault(num, {"n": num, "t": clean(m.group(2)), "parts": {}, "grp": group_state.get("cur", "")})
            sections[num]["t"] = clean(m.group(2))
            sections[num]["p"] = page_of(m.group(2))
            if num not in order:
                order.append(num)
            part = None
            continue
        if cur is None:
            continue
        if s.startswith("## "):
            part = part_key(s[3:])
            sections[cur]["parts"].setdefault(part, [])
            continue
        if not s or s == "---":
            continue
        if part is None:
            part = "व्याख्या"
            sections[cur]["parts"].setdefault(part, [])
        sections[cur]["parts"][part].append(clean(s))


def parse_addenda(folder: Path, sections: dict):
    """addenda/sNNN.md supplements merge into the matching § as extra parts."""
    ad = folder / "addenda"
    if not ad.is_dir():
        return
    for f in sorted(ad.glob("s*.md")):
        m = re.match(r"s0*([0-9]+)", f.stem)
        if not m:
            continue
        num = str(int(m.group(1)))
        if num not in sections:
            continue
        part = None
        for raw in f.read_text(encoding="utf-8").splitlines():
            s = raw.strip()
            if s.startswith("## "):
                part = part_key(s[3:])
                sections[num]["parts"].setdefault(part, [])
                continue
            if not s or s == "---" or part is None:
                continue
            sections[num]["parts"][part].append(clean(s))


def parse_abhishek(folder: Path):
    """abhishek: '# <sub-granth>' groups, '## अनुच्छेद N — title' sections.
    Glossary/appendix files carry no अनुच्छेद headings, so any other '##'/'###'
    heading (and plain text right under a '#') also opens a section."""
    sections, order = {}, []
    group = ""
    idx = 0

    def new(title, num=""):
        nonlocal idx, cur
        idx += 1
        key = str(idx)
        sections[key] = {"n": num, "t": title, "p": "", "grp": group, "parts": {"पाठ": []}}
        order.append(key)
        cur = key
        return key

    for f in sorted((folder / "parts").glob("*.md")):
        cur = None
        in_anu = False          # inside a real अनुच्छेद? then '##' is a part, not a section
        part = "पाठ"
        for raw in f.read_text(encoding="utf-8").splitlines():
            s = raw.strip()
            if s.startswith("# ") and not s.startswith("## "):
                group = clean(s[2:])
                cur, in_anu, part = None, False, "पाठ"
                continue
            m = re.match(r"^##\s*(अनुच्छेद[^—–-]*)[—–-]\s*(.*)$", s)
            if m:
                label = clean(m.group(1))
                new(clean(m.group(2)), dev2en(re.sub(r"अनुच्छेद\s*", "", label)).strip())
                in_anu, part = True, "पाठ"
                continue
            head = None
            if s.startswith("### "):
                head = clean(s[4:])
            elif s.startswith("## "):
                head = clean(s[3:])
            if head is not None:
                if in_anu:                       # a part heading inside the अनुच्छेद
                    part = part_key(head)
                    sections[cur]["parts"].setdefault(part, [])
                else:                            # glossary / appendix heading
                    new(head)
                    part = "पाठ"
                continue
            if not s or s == "---":
                continue
            if cur is None:
                new(group or "—")
                part = "पाठ"
            sections[cur]["parts"].setdefault(part, []).append(clean(s))
    return sections, order


def parse_qa(folder: Path):
    """gagar / shantisagar English: '# Topic' then '**Question N.**' / 'Answer'."""
    sections, order = {}, []
    group = ""
    idx = 0
    cur = None
    for f in sorted((folder / "parts").glob("*.md")):
        for raw in f.read_text(encoding="utf-8").splitlines():
            s = raw.strip()
            if s.startswith("# ") and not s.startswith("## "):
                group = clean(s[2:])
                cur = None
                continue
            if s.startswith("## "):
                group = clean(s[3:])
                cur = None
                continue
            m = re.match(r"^\*\*Question\s*([0-9]+)[.\s—–-]*(.*)$", s)
            if m:
                idx += 1
                key = str(idx)
                sections[key] = {"n": m.group(1), "t": clean(m.group(2)).rstrip("*"),
                                 "p": "", "grp": group, "parts": {"Question": [clean(m.group(2)).rstrip('*')], "Answer": []}}
                order.append(key)
                cur = key
                continue
            if not s or s == "---":
                continue
            if cur is None:
                # prose section (preface, life-sketch, tables, pooja …)
                idx += 1
                key = str(idx)
                sections[key] = {"n": "", "t": group or "—", "p": "", "grp": group, "parts": {"Text": []}}
                order.append(key)
                cur = key
            tgt = "Answer" if "Answer" in sections[cur]["parts"] else list(sections[cur]["parts"])[-1]
            sections[cur]["parts"][tgt].append(clean(re.sub(r"^Ans(wer)?\s*[.—–-]*\s*", "", s)))
    return sections, order


def parse_backmatter(folder: Path):
    """Appendices / glossary / bibliography → their own pseudo-sections."""
    out, order = {}, []
    bm = folder / "backmatter"
    if not bm.is_dir():
        return out, order
    idx = 0
    for f in sorted(bm.glob("*.md")):
        cur = None
        group = ""
        for raw in f.read_text(encoding="utf-8").splitlines():
            s = raw.strip()
            if s.startswith("# ") and not s.startswith("## "):
                group = clean(s[2:])
                continue
            if s.startswith("## "):
                idx += 1
                key = f"b{idx}"
                out[key] = {"n": "", "t": clean(s[3:]), "p": "", "grp": group or "परिशिष्ट", "parts": {"पाठ": []}}
                order.append(key)
                cur = key
                continue
            if not s or s == "---":
                continue
            if cur is None:
                idx += 1
                key = f"b{idx}"
                out[key] = {"n": "", "t": group or "परिशिष्ट", "p": "", "grp": group or "परिशिष्ट", "parts": {"पाठ": []}}
                order.append(key)
                cur = key
            out[cur]["parts"]["पाठ"].append(clean(s))
    return out, order


# --------------------------------------------------------------------------- docx (Pramana Pariksha)

def parse_docx(path: Path):
    """Reconstruct sections from the finished .docx (Heading2 = §, Heading3 = part)."""
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError:
        print("  ! python-docx missing — skipping", path.name)
        return {}, []
    doc = Document(str(path))
    items = []
    for el in doc.element.body.iterchildren():
        if el.tag.endswith("}p"):
            items.append(Paragraph(el, doc))
        elif el.tag.endswith("}tbl"):
            items.append(Table(el, doc))
    sections, order = {}, []
    cur = part = None
    group = ""
    for it in items:
        if isinstance(it, Table):
            if cur and part:
                for row in it.rows:
                    cells = [c.text.strip() for c in row.cells]
                    if any(cells):
                        sections[cur]["parts"][part].append(" | ".join(cells))
            continue
        style = it.style.name if it.style is not None else ""
        text = it.text.strip()
        if not text:
            continue
        if style == "Heading 1":
            group = text
            continue
        if style == "Heading 2":
            m = re.match(r"^§\s*([0-9०-९]+)\s*[—–-]\s*(.*)$", text)
            if m:
                num = dev2en(m.group(1))
                cur = num
                sections[num] = {"n": num, "t": clean(m.group(2)), "p": "", "grp": group, "parts": {}}
                order.append(num)
                part = None
            else:
                cur = f"x{len(order)+1}"
                sections[cur] = {"n": "", "t": text, "p": "", "grp": group, "parts": {"पाठ": []}}
                order.append(cur)
                part = "पाठ"
            continue
        if style == "Heading 3":
            if cur:
                part = part_key(text)
                sections[cur]["parts"].setdefault(part, [])
            continue
        if cur is None:
            continue
        if part is None:
            part = "पाठ"
            sections[cur]["parts"].setdefault(part, [])
        sections[cur]["parts"][part].append(text)
    return sections, order


# --------------------------------------------------------------------------- glossary extraction

GLOSS_HINT = re.compile(r"शब्दावली|शब्द\s*\|\s*अर्थ|Glossary")


def harvest_terms(gid, gtitle, sections, order):
    """Pull '| term | meaning |' rows out of any glossary-ish section."""
    terms = []
    for key in order:
        sec = sections[key]
        blob = " ".join(" ".join(v) for v in sec["parts"].values())
        if not (GLOSS_HINT.search(sec.get("t", "")) or GLOSS_HINT.search(sec.get("grp", "")) or GLOSS_HINT.search(blob[:400])):
            continue
        for line in blob.split("\n"):
            pass
        for part_lines in sec["parts"].values():
            for line in part_lines:
                if line.count("|") < 2:
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 2 or not cells[0] or not cells[1]:
                    continue
                if re.fullmatch(r":?-{2,}:?", cells[0]) or cells[0] in ("शब्द", "Term", "क्रिया", "No.", "Nos."):
                    continue
                if len(cells[0]) > 60:
                    continue
                terms.append({"t": cells[0], "m": cells[1], "g": gid, "gt": gtitle, "s": key})
    return terms


# --------------------------------------------------------------------------- main

def flatten(sec):
    chunks = []
    for name, lines in sec["parts"].items():
        body = "\n".join(l for l in lines if l)
        if body.strip():
            chunks.append({"h": name, "b": body})
    return chunks


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "full").mkdir(exist_ok=True)
    granths, stats = [], {}
    all_terms = []

    for gid, folder, hi, en, lang in CORPORA:
        fp = ROOT / folder
        if not fp.is_dir():
            print(f"  - {folder}: missing, skipped")
            continue
        meta = {}
        mj = fp / "meta.json"
        if mj.exists():
            try:
                meta = json.loads(mj.read_text(encoding="utf-8"))
            except Exception:
                meta = {}
        groups = {}
        gj = fp / "groups.json"
        if gj.exists():
            try:
                groups = {dev2en(k): v for k, v in json.loads(gj.read_text(encoding="utf-8")).items()}
            except Exception:
                groups = {}

        if gid == "abhi":
            sections, order = parse_abhishek(fp)
        elif gid in ("gagar", "shanti"):
            sections, order = parse_qa(fp)
        else:
            sections, order = {}, []
            gstate = {"cur": ""}
            for f in sorted((fp / "parts").glob("*.md")):
                parse_section_file(f, sections, order, gstate)
            parse_addenda(fp, sections)
            # attach group headings by section number
            if groups:
                cur = ""
                for num in sorted(order, key=lambda x: int(x) if x.isdigit() else 0):
                    if num in groups:
                        cur = groups[num]
                    sections[num]["grp"] = cur
        bsec, border = parse_backmatter(fp)
        sections.update(bsec)
        order = order + border

        if not order:
            print(f"  - {folder}: no sections found, skipped")
            continue

        title_hi = meta.get("title", hi) if gid not in ("gagar", "shanti") else hi
        gdata = []
        for key in order:
            sec = sections[key]
            gdata.append({"k": key, "n": sec.get("n", ""), "t": sec.get("t", ""),
                          "p": sec.get("p", ""), "grp": sec.get("grp", ""),
                          "c": flatten(sec)})
        (OUT / "full" / f"{gid}.json").write_text(
            json.dumps(gdata, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

        all_terms += harvest_terms(gid, title_hi, sections, order)
        chars = sum(len(c["b"]) for s in gdata for c in s["c"])
        granths.append({"id": gid, "hi": title_hi, "en": en, "lang": lang,
                        "author": meta.get("author_line", ""), "subject": meta.get("subject", ""),
                        "basis": meta.get("basis", ""), "n": len(gdata), "chars": chars,
                        "idx": [{"k": s["k"], "n": s["n"], "t": s["t"], "p": s["p"], "grp": s["grp"]} for s in gdata]})
        print(f"  \u2713 {title_hi:28s} {len(gdata):5d} sections  {chars/1024:8.0f} KB")

    # Pramana Pariksha — only the finished docx survives
    pp = ROOT / "granth" / "pramana-pariksha" / "vyakhya" / "Pramana_Pariksha_Sampurna_Vyakhya.docx"
    if pp.exists():
        sections, order = parse_docx(pp)
        if order:
            gdata = [{"k": k, "n": sections[k].get("n", ""), "t": sections[k]["t"], "p": sections[k]["p"],
                      "grp": sections[k]["grp"], "c": flatten(sections[k])} for k in order]
            (OUT / "full" / "pramana.json").write_text(
                json.dumps(gdata, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            all_terms += harvest_terms("pramana", "प्रमाण-परीक्षा", sections, order)
            chars = sum(len(c["b"]) for s in gdata for c in s["c"])
            granths.append({"id": "pramana", "hi": "प्रमाण-परीक्षा", "en": "Pramana Pariksha", "lang": "hi",
                            "author": "श्रीमदाचार्यविद्यानन्द-विरचिता", "subject": "", "basis": "",
                            "n": len(gdata), "chars": chars,
                            "idx": [{"k": s["k"], "n": s["n"], "t": s["t"], "p": s["p"], "grp": s["grp"]} for s in gdata]})
            print(f"  \u2713 {'प्रमाण-परीक्षा':28s} {len(gdata):5d} sections  {chars/1024:8.0f} KB")

    # dedupe terms (same term+granth)
    seen, terms = set(), []
    for t in all_terms:
        k = (t["t"], t["g"])
        if k in seen:
            continue
        seen.add(k)
        terms.append(t)
    terms.sort(key=lambda x: x["t"])

    (OUT / "meta.json").write_text(json.dumps({"granths": granths}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (OUT / "terms.json").write_text(json.dumps(terms, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    stats = {"granths": len(granths), "sections": sum(g["n"] for g in granths),
             "chars": sum(g["chars"] for g in granths), "terms": len(terms)}
    (OUT / "stats.json").write_text(json.dumps(stats, ensure_ascii=False), encoding="utf-8")
    print(f"\n  {stats['granths']} granths | {stats['sections']} sections | "
          f"{stats['chars']/1048576:.1f} MB text | {stats['terms']} glossary terms")


main()
