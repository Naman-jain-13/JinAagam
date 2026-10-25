# -*- coding: utf-8 -*-
"""Trimmed per-section corpus for the Kosh's AI-search Artifact.

data/full/<gid>.json carries full section text (98 MB total, several files over the
16 MB a single Artifact text file may hold) — too large to publish. This script keeps,
per section, only हिन्दी अनुवाद + व्याख्या (the parts that actually answer a question,
in Hindi) plus a short मूल पाठ snippet for authenticity, capped so the combined output
for all ~6,700 sections across all 10 granths fits in one file well under that limit.

Usage: python build_search_corpus.py   (run after build_index.py, from encyclopedia/)
"""
import json, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL_DIR = HERE / "data" / "full"
OUT = HERE / "data" / "search_corpus.json"

MOOL_CAP = 120
ANUVAD_CAP = 300
VYAKHYA_CAP = 350

ANUVAD_RE = re.compile(r"अनुवाद")
VYAKHYA_RE = re.compile(r"व्याख्या")
SKIP_VYAKHYA_RE = re.compile(r"पूरक|तुलनात्मक|सन्दर्भ")
MOOL_RE = re.compile(r"मूल")


def trim(s, cap):
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= cap:
        return s
    cut = s[:cap]
    sp = cut.rfind(" ")
    if sp > cap * 0.6:
        cut = cut[:sp]
    return cut.rstrip() + "…"


def section_excerpt(sec):
    mool = anuvad = vyakhya = ""
    for blk in sec.get("c", []):
        h = blk.get("h", "")
        b = blk.get("b", "")
        if not mool and MOOL_RE.search(h):
            mool = b
        elif not anuvad and ANUVAD_RE.search(h):
            anuvad = b
        elif not vyakhya and VYAKHYA_RE.search(h) and not SKIP_VYAKHYA_RE.search(h):
            vyakhya = b
    parts = []
    if mool:
        parts.append(trim(mool, MOOL_CAP))
    if anuvad:
        parts.append(trim(anuvad, ANUVAD_CAP))
    if vyakhya:
        parts.append(trim(vyakhya, VYAKHYA_CAP))
    if not parts:
        # fallback: no block matched the headings above — just trim the first block, if any
        blocks = sec.get("c", [])
        first = blocks[0].get("b", "") if blocks else ""
        if first:
            parts.append(trim(first, MOOL_CAP + ANUVAD_CAP))
    return " ".join(parts)


def main():
    meta = json.loads((HERE / "data" / "meta.json").read_text(encoding="utf-8"))
    granths = {g["id"]: g for g in meta["granths"]}
    out = {"granths": [], "sections": []}
    for gid, g in granths.items():
        fp = FULL_DIR / f"{gid}.json"
        if not fp.exists():
            print(f"  skip {gid}: no full/{gid}.json")
            continue
        secs = json.loads(fp.read_text(encoding="utf-8"))
        out["granths"].append({"id": gid, "hi": g["hi"], "en": g["en"],
                                "author": g.get("author", ""), "subject": g.get("subject", "")})
        prev_grp = None
        for sec in secs:
            grp = sec.get("grp", "")
            # repeated verbatim across every section of a group — keep it only where it changes;
            # the page carries the last-seen value forward when rendering/citing.
            grp_out = grp if grp != prev_grp else ""
            prev_grp = grp
            out["sections"].append({
                "g": gid, "k": sec["k"], "t": sec.get("t", ""), "p": sec.get("p", ""),
                "grp": grp_out, "x": section_excerpt(sec),
            })
        print(f"  {gid}: {len(secs)} sections")
    OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    size_mb = OUT.stat().st_size / 1e6
    print(f"written: {OUT} | {len(out['sections'])} sections | {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
