---
name: granth-vyakhya
description: >
  End-to-end workflow for turning a scanned Sanskrit/Prakrit/Hindi ग्रन्थ (Jain शास्त्र, स्तोत्र, न्याय text,
  ritual manual, question-answer booklet) into a publish-ready Hindi (or English) व्याख्या book — Word + PDF
  with a real table of contents, page numbers, and for every अनुच्छेद: मूल पाठ → हिन्दी अनुवाद → जैनागम-सम्मत
  विस्तृत व्याख्या → सरल उदाहरण → तुलनात्मक तालिका → सन्दर्भ. Use this skill whenever the user gives a PDF
  or images of an old printed Jain/Indic text and asks for translation, अनुवाद, व्याख्या, explanation,
  paragraph-by-paragraph commentary, "explain this shastra", "make a book like Pramana Pariksha", or to
  translate a booklet into English keeping its format — even if they don't say "vyakhya". Also use it to
  fix or extend a book that was built with this workflow (add a page, change fonts/margins, rebuild the PDF).
compatibility: >
  Windows with Microsoft Word installed (needed to compute TOC page numbers and export the PDF).
  Python 3 with pymupdf + python-docx; Node.js with the `docx` package. Claude Code with the Agent tool
  (parallel subagents) for anything longer than ~15 scan pages.
---

# ग्रन्थ-व्याख्या — scanned शास्त्र → publish-ready book

You are producing a book that a मुनि or a विद्वान् श्रावक will read and cite. Three such books exist and set
the bar: *Pramana_Pariksha_Sampurna_Vyakhya* (458 pp), *Laghu/Bruhat_Sarvagya_Siddhi_Vyakhya*,
*Abhishek_Path_Sangrah_Vyakhya* (511 pp, 16 texts). The reader rejected an earlier version that lacked
the TOC, page numbers and parts 4–6 — so the *shape* of the deliverable matters as much as the content.

Read `references/format-standard.md` now (what "done" looks like) and skim `references/pitfalls.md`
(what went wrong before). Come back to `references/agent-prompts.md` when you launch agents.

## 0. Decide the mode

| The source is… | Mode | Builder |
|---|---|---|
| A philosophical/ritual text with verses, sūtras or commentary that needs explanation | **व्याख्या** (6 parts per §) | `scripts/build_docx.js` |
| A collection of several independent texts in one volume | **व्याख्या**, one Heading 1 per text | `scripts/build_docx.js` (or a Python builder; see abhishek notes in pitfalls) |
| A question-answer booklet or plain prose to be *translated* with format preserved | **translation-only** | `scripts/build_simple_docx.py` |

If unsure, ask one question: "व्याख्या (explanation + tables + references per paragraph) या केवल अनुवाद?"
Everything else below you can decide yourself.

## 1. Intake (15 minutes, do it yourself)

1. Create `<book>_work/` next to the PDF with `parts/ addenda/ backmatter/ frontmatter/ img/`, copy
   `assets/meta.example.json → meta.json`, `assets/groups.example.json → groups.json`, and start
   `progress.md` (rules · batch table · lessons). progress.md is your memory across sessions — keep it
   current; it never goes into the book.
2. `python scripts/render_pages.py "<book.pdf>" <work>/img 250` — tells you the page count and whether a
   text layer exists (usually not). Use 300 dpi for small dense print.
3. Read the first 3–4 images and the last one with the Read tool. Establish:
   - title, author, editor, publisher, year, printed page range (goes into `meta.json → basis`, and into
     a "मूल स्रोत-ग्रन्थ का परिचय" page if the reader wants one);
   - the **reading order** on a page (two printed pages per scan? two columns?) — write it down verbatim
     for the agent prompts;
   - the unit of division: verse+टीका, sūtra, argument step, प्रश्न/उत्तर pair, one text of a collection;
   - whether a TOC exists (its page numbers let you pre-assign § ranges and catch missing headings).
4. Record all of this in progress.md. Tell the user the plan in three lines (pages, batches, expected
   sittings) — a 470-page collection took 33 agents over 6 sittings; a 33-page booklet took 4 agents in one.

## 2. Pass 1 — मूल पाठ, अनुवाद, व्याख्या (parallel agents)

Split the scan pages into ranges of 8–14 pages (dense commentary) or up to 20 (plain verse/Q&A).
Launch 3–5 background agents per wave, all in one message, using template **A** in
`references/agent-prompts.md`. The parts that must be *identical* across the agents of a wave:

- the layout / reading-order note;
- the numbering scheme (hand each agent its starting § or let them write `§?`);
- any shared glossary (topic names for a booklet; the ग्रन्थ names in a collection);
- the style block: शास्त्रीय हिन्दी, English digits outside मूल verses, **no sect names**, **no
  working-process language** (बैच/सत्र/file names) — the reader will see every word.

Ask every agent to report its exact first and last words with printed page numbers. Agents cannot see
each other: seams are where duplication and gaps hide (2 of 33 seams duplicated a verse last time).

After each wave, before launching the next, do the **seam check** (template E): `grep -n "^§" parts/*.md`,
`python scripts/check_quality.py parts <work>`, compare reported first/last words, fix numbering and
delete duplicates with targeted edits. Update the batch table in progress.md.

## 3. Pass 2 — parts 4–6 (addenda) and back matter

- One agent per 10–15 § with template **B** → `addenda/sNN.md`. Give them one finished addendum (or
  `references/sample-section.md`) to match depth: a good § is ≈ 2.5–3 PDF pages in total.
- One agent (with *all* parts) with template **C** → `backmatter/01_saar … 04_shabdavali.md`, optionally
  `frontmatter/01_bhumika.md`. Book-wide summaries are never delegated to a batch agent that saw 10
  pages — it will guess authors and miss texts (this happened).
- For a collection, also write the ग्रन्थ-सार table (text · author · pages) yourself from progress.md.

## 4. Build → finalize → verify

```bash
cd <skill>/scripts && npm install            # once; installs the `docx` package
node scripts/build_docx.js <work>            # writes the .docx named in meta.json → out
python scripts/postprocess_docx.py <out.docx> # श्री … स्वामी honorifics + part-6 at dictionary size (7 pt)
python scripts/check_quality.py docx <out.docx>
powershell -File scripts/finalize_word.ps1 -Docx "<out.docx>"      # Word: TOC page numbers + PDF
python scripts/check_quality.py pdf <out.pdf>
```

`postprocess_docx.py` is not optional: the reader asked that every आचार्य of the guru-paramparā be written
respectfully ("श्री विद्यानन्द स्वामी", "श्री अकलंकदेव", "आचार्य श्री समन्तभद्र" — never a bare name), and
that the सन्दर्भ एवं पाद-टिप्पणी part of each § be set dictionary-size so references take minimal room.
The agents write names respectfully at source; the post-processor is the safety net that catches every
remaining bare name outside the मूल पाठ. Use `--dry-run` first to see the count and samples; add a newly met
आचार्य to its `NAMES` list. Run it on the *built* .docx, before Word — never on a .docx Word has open.

- `finalize_word.ps1` is slow on big books (30–60 min for 500 pages). Run it in the background, confirm
  `WINWORD` CPU time keeps climbing, and wait. Do not write to the .docx while Word has it open.
- Render 3–4 PDF pages (title, TOC, a mid-§, back matter) with pymupdf and *look* at them before
  reporting: footer "1, 2, 3" (not "11, 22"), no heading stranded at a page bottom, tables not clipped,
  TOC has page numbers.
- Every fix goes into `parts/`, `addenda/`, `meta.json` — never into the .docx — then rebuild. Otherwise
  the next rebuild silently discards it.

## 5. Report

Two or three sentences: files with paths, page count, what was verified, any [अस्पष्ट] spots or suspected
misprints for the reader to check against the original. Append a closing section to progress.md.

## Fixing or extending an existing book

Reader asks for a change (add a disclaimer bullet, reduce footnote font, tighter margins, stop headings
from orphaning, add a credit line, translate the same book to English)? Locate the corresponding
`meta.json` field / markdown file / builder style, change *that*, rebuild, finalize, verify with
`check_quality.py`. Show a 2-page standalone preview first when the change is a new page whose look the
reader hasn't approved (build a tiny docx from just that content; don't touch the master until yes).

## Hard rules (the reader set these; don't relitigate)

- Never write बीसपंथ / तेरापंथ or any sect label anywhere in a book.
- Jain आचार्य are always named with respect: "श्री … स्वामी" (or "श्री" alone when the name already carries
  देव/सूरि/स्वामी or follows आचार्य/भट्टारक). Opponent philosophers (कुमारिल, धर्मकीर्ति …) are unchanged;
  the मूल पाठ is never altered. `postprocess_docx.py` enforces this on the whole book.
- सन्दर्भ एवं पाद-टिप्पणी (part 6) is printed dictionary-size — 7 pt, single-spaced, 9 pt heading.
- Every § has all six headings; a heading with nothing to say gets the standard one-liner, not deletion.
- Real TOC page numbers and footer page numbers — only Word produces them; LibreOffice will not.
- Nothing about the *process* (batches, sessions, files, "the user") appears in the book.
- Faithfulness over fluency: [अस्पष्ट] where unreadable; "लगभग/सम्भवतः" where unsure; never invent a citation.
