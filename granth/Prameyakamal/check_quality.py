"""Quality gate for a built व्याख्या — run BEFORE finalize (on parts/) and AFTER finalize (on the PDF).

Usage:
  python check_quality.py parts <work_dir>        # § sequence, duplicates, missing 6-part headings, forbidden words
  python check_quality.py pdf  <book.pdf>         # headings stranded alone at the bottom of a page
  python check_quality.py docx <book.docx>        # heading counts, duplicate § titles, forbidden words in the final doc

Exit code 1 if anything fails, so it can gate a build.
"""
import glob, os, re, sys

# Working-process language and sect names must never reach the reader.
FORBIDDEN = [
    "बीसपंथ", "तेरापंथ", "बीसपन्थ", "तेरापन्थ",
    "बैच", "batch", "अगले बैच", "अगले सत्र", "बैठक", "progress.md", "हमने पिछली बातचीत",
    "उपयोगकर्ता", "user asked", "TODO", "अगले संस्करण में जोड़ा जाएगा",
]
DEV = "०१२३४५६७८९"
dev2int = lambda s: int("".join(str(DEV.index(c)) if c in DEV else c for c in s))


def check_parts(work):
    ok = True
    files = sorted(glob.glob(os.path.join(work, "parts", "*.md")))
    nums, titles = [], {}
    for f in files:
        txt = open(f, encoding="utf-8").read()
        for m in re.finditer(r"^§\s*([०-९0-9]+)\s*[—–-]\s*(.+)$", txt, re.M):
            n = dev2int(m.group(1)); nums.append(n); titles.setdefault(n, []).append(os.path.basename(f))
        for w in FORBIDDEN:
            for m in re.finditer(re.escape(w), txt):
                line = txt[:m.start()].count("\n") + 1
                print(f"FORBIDDEN '{w}' in {os.path.basename(f)}:{line}"); ok = False
    dups = [n for n, fs in titles.items() if len(fs) > 1]
    if dups: print("DUPLICATE §:", {n: titles[n] for n in dups}); ok = False
    if nums:
        expected = list(range(min(nums), max(nums) + 1))
        gaps = sorted(set(expected) - set(nums))
        if gaps: print("GAPS in § numbering:", gaps); ok = False
        print(f"§ range: {min(nums)}–{max(nums)} ({len(set(nums))} sections) in {len(files)} part files")
    add = set(int(os.path.basename(f)[1:3]) for f in glob.glob(os.path.join(work, "addenda", "s*.md")))
    if add:
        no_add = sorted(set(nums) - add)
        if no_add: print("§ without addenda:", no_add)
    return ok


def check_pdf(pdf):
    """A heading is the LAST line on a page => it is stranded (its content went to the next page).
    Headings are recognised by typography, not text (PDF text extraction of Devanagari is unreliable):
    both builders render headings >= 12.5 pt in a colour, body text is 12 pt black."""
    import pymupdf
    doc = pymupdf.open(pdf)
    stranded = []
    for i, page in enumerate(doc):
        lines = []
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if spans:
                    lines.append((ln["bbox"][1], spans))
        lines.sort(key=lambda x: x[0])
        # drop the footer page number (a short all-digit line at the very bottom)
        while lines and re.fullmatch(r"\s*[\d०-९]+\s*", "".join(s["text"] for s in lines[-1][1])):
            lines.pop()
        if not lines:
            continue
        last = max(lines[-1][1], key=lambda s: len(s["text"]))
        if last["size"] >= 12.4 and last["color"] != 0:
            stranded.append((i + 1, "".join(s["text"] for s in lines[-1][1])[:60]))
    print(f"pages: {doc.page_count} | headings stranded at page bottom: {len(stranded)}")
    for p, t in stranded: print(f"  page {p}: {t}")
    return not stranded


def check_docx(path):
    from docx import Document
    ok = True
    doc = Document(path)
    sname = lambda p: p.style.name if p.style is not None else ""
    h = {lvl: [p.text for p in doc.paragraphs if sname(p) == f"Heading {lvl}"] for lvl in (1, 2, 3)}
    print("Heading 1:", len(h[1]), "| Heading 2 (§):", len(h[2]), "| Heading 3:", len(h[3]))
    dups = sorted({t for t in h[2] if h[2].count(t) > 1})
    if dups: print("DUPLICATE § titles:", dups); ok = False
    n_sec = len([t for t in h[2] if t.lstrip().startswith("§")])
    six = [t for t in h[3] if re.match(r"^\s*[1-6१-६]\.\s", t)]
    if n_sec and len(six) != 6 * n_sec:
        print(f"WARNING: {n_sec} § but {len(six)} six-part sub-headings (expected {6 * n_sec}) — some § are missing a part"); ok = False
    elif n_sec:
        print(f"six-part structure OK: {n_sec} § x 6 = {len(six)} sub-headings")
    texts = [p.text for p in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells]
    for w in FORBIDDEN:
        hits = [t[:70] for t in texts if w in t]
        if hits: print(f"FORBIDDEN '{w}': {len(hits)} hit(s), e.g. {hits[0]!r}"); ok = False
    # --- honorifics + part-6 size: was postprocess_docx.py run? ---
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("pp", os.path.join(os.path.dirname(os.path.abspath(__file__)), "postprocess_docx.py"))
        pp = importlib.util.module_from_spec(spec); spec.loader.exec_module(pp)
        sec, bare, ref_sizes = "other", [], []
        for p in doc.paragraphs:
            st = sname(p)
            if st == "Heading 3":
                sec = "mool" if "मूल" in p.text else ("ref" if "सन्दर्भ" in p.text and "टिप्पणी" in p.text else "other")
                continue
            if st.startswith("Heading") or st.lower().startswith("toc"):
                sec = "other"; continue
            if sec != "mool" and pp.honor(p.text, "", "") != p.text and len(bare) < 5:
                bare.append(p.text[:70])
            if sec == "ref":
                ref_sizes += [r.font.size.pt for r in p.runs if r.font.size]
        if bare: print(f"BARE आचार्य NAME(S) (run postprocess_docx.py): e.g. {bare[0]!r}"); ok = False
        if ref_sizes and max(ref_sizes) > 9.5:
            print(f"PART 6 NOT AT DICTIONARY SIZE (max {max(ref_sizes)} pt; run postprocess_docx.py)"); ok = False
        elif ref_sizes:
            print(f"part 6 size OK (max {max(ref_sizes)} pt over {len(ref_sizes)} runs)")
    except Exception as e:
        print("honorific/size check skipped:", e)
    return ok


if __name__ == "__main__":
    mode, target = sys.argv[1], sys.argv[2]
    res = {"parts": check_parts, "pdf": check_pdf, "docx": check_docx}[mode](target)
    print("RESULT:", "OK" if res else "PROBLEMS FOUND")
    sys.exit(0 if res else 1)
