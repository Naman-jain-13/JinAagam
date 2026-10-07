# -*- coding: utf-8 -*-
"""हर § की सूची — कौन-से बैच में, कौन-से मुद्रित पृष्ठ पर, कितना बड़ा।

addenda लिखने वालों को यही बताती है कि किस § पर कितना लिखना है (छोटे § पर कम,
बड़े पर अधिक), और मुझे यह कि कितना काम बाकी है।

चलाइए:  python make_index.py              # section_index.json लिखिए
        python make_index.py --todo       # जिनकी addenda अभी नहीं बनी
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def sections():
    """(§ संख्या, शीर्षक, बैच, मुद्रित पृष्ठ, मूल की लम्बाई, पूरे § की लम्बाई)"""
    for f in sorted(HERE.glob("parts/batch*.md")):
        text = f.read_text(encoding="utf-8")
        blocks = re.split(r"(?m)^(?=§\d)", text)
        for b in blocks:
            m = re.match(r"§(\d+)\s*—?\s*(.*)", b)
            if not m:
                continue
            num, title = int(m.group(1)), m.group(2).strip()
            mool = re.search(r"##\s*1\..*?\n(.*?)(?=\n##\s*2\.|\Z)", b, re.S)
            mool_text = mool.group(1) if mool else ""
            pages = [int(x) for x in re.findall(r"\(पृष्ठ\s*(\d+)", b)]
            yield {
                "n": num,
                "title": title,
                "batch": f.name,
                "page": pages[0] if pages else None,
                "mool_lines": len([l for l in mool_text.splitlines() if l.strip()]),
                "mool_chars": len(mool_text),
                "chars": len(b),
            }


def size_band(rec):
    """निर्देश-पत्र के तीन वर्ग — किस § पर कितना लिखना है।"""
    if rec["mool_chars"] < 600:
        return "छोटा"       # छोटा
    if rec["mool_chars"] > 2000:
        return "बड़ा"       # बड़ा
    return "सामान्य"   # सामान्य


def main(todo=False):
    recs = list(sections())
    for r in recs:
        r["band"] = size_band(r)
    if todo:
        add = HERE / "addenda"
        done = {int(p.stem[1:]) for p in add.glob("s*.md") if p.stem[1:].isdigit()}
        left = [r for r in recs if r["n"] not in done]
        print(f"कुल §: {len(recs)} | addenda बनी: {len(done)} | "
              f"बाकी: {len(left)}")
        by_batch = {}
        for r in left:
            by_batch.setdefault(r["batch"], []).append(r["n"])
        for b in sorted(by_batch):
            ns = by_batch[b]
            print(f"  {b}: {len(ns)}  (§{ns[0]}–§{ns[-1]})")
        return
    out = HERE / "section_index.json"
    out.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
    bands = {}
    for r in recs:
        bands[r["band"]] = bands.get(r["band"], 0) + 1
    print(f"section_index.json — {len(recs)} §")
    for k, v in bands.items():
        print(f"   {k}: {v}")


if __name__ == "__main__":
    main("--todo" in sys.argv)
