# Pitfalls learned across four books (≈1,100 scan pages)

Each of these cost real time once. Read before starting; re-read before the final build.

## Reading the scans
- **No text layer.** Old scans have none; `get_text()` returns "". Render to PNG (250–300 dpi) and *read the
  images*. Never OCR-guess dense Devanagari at low dpi — conjuncts and matras get misread (e.g. मालरापाटन
  for झालरापाटन). If a proper name looks odd, zoom (crop + re-render at 400 dpi) before writing it down.
- **Two printed pages per scan** is common; each printed page may have two columns. Establish the reading
  order on the first content page and put it in every agent prompt.
- **Missing boxed headings.** A booklet's TOC may list a topic whose boxed heading was never printed
  (Gagar Saar topic 4). Trust TOC page numbers + content shift; insert the heading editorially and say so
  in a note.
- **Verse cut at a page top** belongs to the previous batch. Make every agent read one page *before* its
  range and start at the first complete unit.

## Parallel agents
- **Numbering collisions.** Agents cannot see each other; two will both write "§ 4" / "ग्रन्थ-4". Either
  hand each agent its starting number (when you can count units from the TOC) or make them write `§?` and
  renumber at consolidation. Always `grep -n "^§"` across parts/ after every wave.
- **Boundary duplication.** Despite instructions, adjacent agents both wrote the same verse twice on two
  occasions out of 33 seams. Ask each agent to report its exact first/last words; compare; delete the later
  copy with a line-range `sed -i`.
- **Answer/verse split across agents.** The tail of an answer landing at the top of the next agent's range
  arrives as an orphan fragment. Merge it into the previous file's last unit, remove the fragment and the
  duplicated heading from the next file.
- **Agents guess when they lack context.** The final agent of the अभिषेक project invented a "ग्रन्थ-सार"
  table with a wrong author for ग्रन्थ-1 and 6 missing texts. Summary tables that span the whole book are
  written by *you* (or an agent given *all* parts), never by a batch agent that saw 10 pages.
- **Identity by evidence, not assumption.** A running header can be a poetic title while the colophon gives
  the real name (नित्यमहोद्योतम् / अर्हद्दैवमहाभिषेकविधिः). Confirm a text's name/author from its
  colophon or a printed serial number before naming it in a heading.

- **64k output cap per response.** An agent that drafts 8 dense pages and then writes the whole file in one
  Write call dies with "exceeded the 64000 output token maximum" and leaves nothing on disk. Template A now
  tells agents to save every 2–3 § (Write once, then Edit-append). Keep ranges <= 8 pages for dense prose.

## Content rules that were enforced by the reader
- **No sect names** (बीसपंथ/तेरापंथ) anywhere — the reader stopped the work to say so.
- **No working-process language** leaks into the book. 100+ occurrences of "बैच", "अगले बैच में", "batch04"
  had to be scrubbed after the fact. Put the ban in every agent prompt; grep for it before every build
  (`check_quality.py parts`). Cross-refer with § numbers, "पूर्व-वर्णित", "आगामी अंश".
- **All six parts, every §.** A build with only parts 1–3 and no TOC/page numbers was rejected outright.
- **Real page numbers in the TOC.** Only Word can compute them; LibreOffice will not update the field.

- **Honorifics and reference size are a post-build step.** Writing "श्री … स्वामी" at source is not enough —
  110 bare names slipped through in one book. `postprocess_docx.py` runs on the built .docx (before Word)
  and is idempotent; `check_quality.py docx` fails if it was skipped. Watch hyphenated compounds
  ("श्रीमदाचार्य-अनन्तकीर्ति") — an early version doubled the श्री there; the title page is the place to look.

## Word / DOCX mechanics
- **Footer page numbers "11, 22, 33".** Adding a second section (cover page) and then touching `.footer` on
  *both* linked sections appends two PAGE fields to the shared footer. Set the footer once on section 0 only.
- **Orphaned headings.** A heading sitting alone as the last line of a page was reported on 5 pages. Set
  keep-with-next on every heading style (both builders do). Verify with `check_quality.py pdf`.
- **Blank half-pages.** Forcing a page break before every § wasted space and was reported. Page breaks only
  before Heading 1 (खण्ड / ग्रन्थ); § flow continuously with a thin rule above.
- **Word COM is slow.** 450–500 pages of Devanagari + tables: TOC update + PDF export takes 30–60 minutes.
  Run it in the background; check that `WINWORD` CPU time keeps rising; do not kill it because it "looks
  stuck". Never write to the .docx while Word has it open (EBUSY). If a run is aborted, `Stop-Process WINWORD`
  before retrying.
- **Windows paths in Python.** The Windows Python does not understand `/tmp` or `/c/Users/...`. Use
  `C:/Users/...` paths inside scripts; `PYTHONIOENCODING=utf-8` when printing Devanagari.

## Process
- **Rebuild everything from parts/.** Never hand-edit the .docx — every fix goes into the markdown and the
  book is regenerated; otherwise the next rebuild silently loses it.
- **Preview before merging.** When a reader is unsure about a new page (cover, credits), build a 2-page
  standalone .docx/.pdf for approval first; don't touch the master until they say yes.
- **progress.md** in the work folder: rules, batch table (file → pages → contents), lessons. It is what lets
  a fresh session pick up after a context reset. Keep it out of the book.
- **Token budget.** ~10–14 dense pages per Sonnet agent ≈ 110–150 k tokens each. A 470-page collection took
  33 agents across 6 sittings; a 33-page Q&A booklet took 4 agents in one sitting.
