"""Build the shareable online edition: index.html + an inlined, trimmed dataset.

The offline edition fetches data/ (full text, ~24 MB). A published page has a 16 MB
budget and has to load over the network, so this build keeps every title, group,
glossary term and citation, and samples the opening of each part of each section —
enough for search to find a passage and for the reader to see what it says, with a
note pointing to the printed book for the rest.

Run:  python build_online.py   ->  online.html
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
PER_PART = 260          # chars kept from each part
PER_SECTION = 950       # hard cap per section


def trim(sec):
    out, used = [], 0
    for c in sec["c"]:
        if used >= PER_SECTION:
            break
        room = min(PER_PART, PER_SECTION - used)
        body = c["b"]
        cut = body[:room]
        if len(body) > room:
            sp = cut.rfind(" ")
            if sp > room * 0.6:
                cut = cut[:sp]
            cut += " …"
        out.append({"h": c["h"], "b": cut})
        used += len(cut)
    return {"k": sec["k"], "n": sec["n"], "t": sec["t"], "p": sec["p"], "grp": sec["grp"], "c": out}


def main():
    meta = json.loads((DATA / "meta.json").read_text(encoding="utf-8"))
    terms = json.loads((DATA / "terms.json").read_text(encoding="utf-8"))
    stats = json.loads((DATA / "stats.json").read_text(encoding="utf-8"))
    full = {}
    for g in meta["granths"]:
        rows = json.loads((DATA / "full" / f"{g['id']}.json").read_text(encoding="utf-8"))
        full[g["id"]] = [trim(s) for s in rows]

    payload = {"granths": meta["granths"], "terms": terms, "stats": stats, "full": full, "lite": True}
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))

    html = (HERE / "index.html").read_text(encoding="utf-8")
    inject = "<script>window.__KOSH__=" + blob + ";</script>\n"
    # place the data immediately before the app script
    i = html.rindex("<script>")
    out = html[:i] + inject + html[i:]
    (HERE / "online.html").write_text(out, encoding="utf-8")
    mb = len(out.encode("utf-8")) / 1048576
    print(f"online.html  {mb:.2f} MB   ({stats['sections']} sections, {len(terms)} terms)")
    if mb > 15:
        print("  ! close to the 16 MB page limit — lower PER_PART / PER_SECTION")


main()
