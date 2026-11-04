# RECHECK — मूल पाठ को मुद्रित प्रति से अक्षरशः मिलाना (v2, पास 2 से पहले)

*Working document. Nothing here goes into the book.*

## Why this pass exists
The प्राकृत सूत्र and the संस्कृत टीका in `parts/` were transcribed once (stage 1, `mool/slice_*.md`) and never independently re-read; the reader now
wants them checked against the original print before any व्याख्या is written. In every earlier book of this series a scan-allowed re-read found
real misreadings (~10 per 70 §, e.g. `सन्तापो` for printed `सन्तोषो`). **Your job: make every Prakrit and Sanskrit character in your range of
`parts/` equal to the print — letter for letter — and log each change.** Pass 2 translates exactly what you leave; nothing downstream can recover a
letter you miss.

## Your range
Each batch is a range of **pdf pages** (see the batch table in `progress.md`, section "v2 …"). For the टीका pages (pdf 21–219, odd pages + the
exceptions below) you check **part 6 `(Tn)` segments**; for the परिशिष्ट pages (pdf 221–233) you check **part 1 (मूल पाठ)** and part 11 footnotes.
Find the § whose text lies on your pages from the `सन्दर्भ-संकेत:` line / title page numbers (**pdf = मुद्रित + 19**) — a § may start on the page before
your range or run past its end; check only the text printed on your pages, but finish a sentence that crosses your last page.

## The page images — and the Hindi
- Source: `mool/Pratikraman_Granthtriyi.pdf` (234 pp, landscape, page box 792×612 pt). `img/pNNN.png` are 200-dpi renders — fine for orientation,
  too coarse for conjuncts. **Zoom every line you check** at 400–500 dpi:
  ```
  python -c "import pymupdf; d=pymupdf.open(r'mool/Pratikraman_Granthtriyi.pdf'); d[PDF-1].get_pixmap(dpi=450, clip=pymupdf.Rect(x0,y0,x1,y1)).save(r'<scratch>/<prefix>_z.png')"
  ```
  Work in strips (e.g. 6–8 horizontal bands per page) so each crop is readable; cover the whole text block.
- **Layout:** pdf 21–220: odd pages = Sanskrit टीका (with the प्राकृत सूत्र-पद in bold); even pages = the printed Hindi translation. **Do not read the even
  pages**, except pdf 116 (टीकाकार's closing verse + ग्रन्थ-1 colophon; a modern translator's line there is not ours) — the four even pages 22, 118, 182
  carry only a page head we already dropped. pdf 117 = बृहत्प्रतिक्रमण title + its opening verse. pdf 221–233 = परिशिष्ट (मूल पाठ only).
- **Ignore the Hindi entirely** — do not transcribe it, do not use it to decide a reading, do not let it shape a word.
- **Unique scratch prefix per batch** (e.g. `rc07_`) for every image you save, in your own scratch folder — several batches run at once.
- If an image ever comes back as `[media removed …]` or unreadable, stop on that page and report it; never "check" a page you could not see.

## What you compare, and the rules (hard-won — follow all)
1. **The printed text governs.** Change `parts/` only to make it match the print. **Never normalise toward grammar, sandhi, metre or the "correct"
   form** — not even when the print looks wrong. An earlier agent in this series twice "fixed" the print to fit the sense and reversed the book's meaning.
   A misprint stays; you may add `(?)` only if the print itself has it.
2. **Line-break hyphens.** A full consonant + hyphen at a printed line end means **अ follows**: `तद-` / `प्रयोजक` is **तदप्रयोजक**, not तत्प्रयोजक. Stage 1
   kept such hyphens inside words (`ता-वत्`, `मोक्ष-लक्षण`, `वेज्जा-( आ ) वच्चं`): where the hyphen is only a printed line-break, write the word joined as the
   print reads it (`तावत्`, `मोक्षलक्षण`) and log it; where the print has a real hyphen inside a line, keep it.
3. **Watch especially:** dropped `अ` (after avagraha-less sandhi, after a hyphen), dropped `न`/`ण` in a conjunct, `द्व` vs `दव`/`द्वि` vs `दवि`, a lost or
   misplaced **रेफ** (र्), `ञ्च`/`श्च`, `प्र`↔`म`, `त्व`↔`ल`, `ष`↔`प`, `ध`↔`घ`, `भ`↔`म`, `त्त`↔`च्च`, `ट्ठ`/`ठ्ठ`, `ड्ढ`/`ढ्ढ`, anusvara vs half-nasal, `ऽ`
   present or absent, `।` vs `॥`, digits (`॥1॥` Arabic vs `॥१॥` Devanagari — as printed).
4. **Mark genuine doubt `[अस्पष्ट]`** (or keep the existing `[अस्पष्ट]`) rather than guess. Remove an existing `[अस्पष्ट]` only if you can read the letters
   at 450–500 dpi.
5. **Bold:** in part 6, `**…**` marks the words the print sets in bold (the सूत्र-पद the टीका glosses). Fix a bold span only if it plainly disagrees with
   the print (a bold word left plain or vice versa) — pass 2 relies on it to separate प्राकृत from Sanskrit. Part 1 carries no bold.
6. **Footnote marks:** where the print has a footnote number in the Sanskrit text, put `[N]` right after the word (N = the printed number, Arabic digit) if it
   is not there yet; check each part-11 footnote line against the page foot. Footnotes that are Hindi explanations are not transcribed.
7. **Do not move text between §, do not re-segment, do not touch `(Tn)` tags, titles, the `सन्दर्भ-संकेत:` line or `## ` headings.** Edit only inside the
   text of a segment / of part 1 / of a part-11 line. If text is **missing** (a line stage 1 skipped) insert it in the right segment at the right place; if text
   is **extra** (a Hindi word, a page head, a duplicated line), delete it — and log both.
8. **Never consult the printed Hindi, `_v1/`, or memory of a published edition** to decide a reading.
9. Grep `parts/` for a recurring formula before deciding a doubtful letter (`तस्स मिच्छा मे दुक्कडं`, `इत्यादि सुगमम्`, `तमालोचयितुमिच्छामि`).
10. Keep the file's encoding (UTF-8) and line endings; use exact string edits, one change at a time.

## Log — `verify/recheck_NN.md` (NN = batch number)
```markdown
# पुनर्मिलान बैच NN — pdf <a>–<b>
| § | खण्ड | पहले | अब | स्थिति |
|---|---|---|---|---|
| §300 | T3 | दोषपरिणामे | द्वेषपरिणामे | स्पष्ट |
| §1430 | भाग 1 | अलोच | अलोचं | स्पष्ट |
| §1960 | T5 | उवगूहण | उवगूहण[अस्पष्ट] | अस्पष्ट |
```
`स्थिति` = **स्पष्ट** (the print is clear at zoom) or **अस्पष्ट** (worn/broken type; you chose the likeliest reading or marked `[अस्पष्ट]`). Quote enough of
the word that the change can be found. Log **every** change, including joined hyphens and inserted/deleted lines. End with: pages checked, lines/segments
checked, changes (स्पष्ट / अस्पष्ट), any page you could not read.

## Before reporting
Do **not** run `python make_pass1.py` (without `--check` it regenerates `parts/` from the slices and would wipe every correction). Its `--check`
will now show your changes as differences — that is expected. Confirm instead that every `(Tn)` tag and `## ` heading in your range is untouched
(`git diff parts/` shows only text changes inside lines) and that every change is in your log.

## Report back (under 150 words)
Batch, pdf pages, § touched; number of changes (स्पष्ट / अस्पष्ट); the 3–5 most consequential corrections (a word whose sense changed); any page or line
you could not read; anything that looks like a stage-1 omission larger than a word.
