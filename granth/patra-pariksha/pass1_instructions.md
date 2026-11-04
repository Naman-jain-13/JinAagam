# Pass 1 — extraction spec (पत्रपरीक्षा)

*Working document. Nothing here goes into the book.*

You are transcribing **पत्रपरीक्षा** of **श्री विद्यानन्द स्वामी** (सनातन जैन ग्रन्थमाला, 2): a short, dense, wholly
**Sanskrit** न्याय treatise — mixed **कारिका** (verses numbered `॥ १ ॥`) and the author's own prose **वृत्ति**. There is
**no Hindi and no छाया in the source.** The finished book is a scholarly हिन्दी व्याख्या for विद्वान् readers; pass 2 will
translate what you transcribe, and pass 3 audits that translation against it. **Anything you drop or alter is lost
silently.** Transcribe every word, exactly.

Source: `mool/Patra_Pariksha_Vidyananda.pdf` (13 pages; rendered at `img/p01.png … p13.png`; printed page = scan page,
printed header `पत्रपरीक्षा।` or `सनातनजैनग्रंथमालायां–`). Open the images with the Read tool; zoom a doubtful conjunct:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Patra_Pariksha_Vidyananda.pdf'); d[IDX].get_pixmap(dpi=500, clip=pymupdf.Rect(30,100,480,300)).save(r'<scratch>/z.png')"
```
`IDX = page − 1`; page box 504×774 pt.

## What a page carries
Top: Kobatirth library header/footer watermark (ignore). Body: Sanskrit prose and verses, two kinds of paragraph —
indented **कारिका** blocks, centred, two lines each, closing `॥ १ ॥`, and flowing **वृत्ति** paragraphs. A page may carry
no printed page number except as `पत्रपरीक्षा। … ३` in the header. At the foot: a ruled **numbered footnote block**
(`१ स्वाभाविकमेव । २ आगच्छत् । …`) — the *editor's one-word Sanskrit glosses*, keyed to superscript numerals in the
body. Pages 1–13 form the whole book; the colophon is on page 13.

## § division — YOU decide it, carefully
The book is one continuous argument. Divide it into **numbered § (key = running ordinal × 10: §10, §20, §30 …)** of
**roughly 1/4–1/3 of a page each**, at natural joints: a कारिका together with the वृत्ति paragraph that explains it;
a pūrvapakṣa objection (`नन्वक्षपादादीनाम् …`) together with its answer; one numbered कारिका group (the long verse set
`यत्र … ॥ १ ॥ … ॥ २७ ॥` on pages 11–12 should be split into groups of ~4–6 verses). Never end a § mid-sentence;
**never split a question from its answer, nor a quoted verse from its introduction.** Aim for **30–45 §**. Every word of
the printed text must belong to exactly one §, in reading order, with **nothing repeated and nothing missing**.

## What to write, per §
Reproduce these headings **verbatim** — a builder parses them.

```
§30 — <short descriptive Hindi title: what this passage establishes> (पत्रपरीक्षा, § 3, मुद्रित पृष्ठ 2)

## 6. संस्कृत मूल पाठ (टीका-पाठ) (मूल)
(पृष्ठ 2)
(T1) <first segment, verbatim>
(T2) <second segment>
…

## 11. मुद्रित पाद-टिप्पणी
- १ स्वाभाविकमेव ।
- २ …
```
- The title is **yours**, in Hindi, accurate: titles are the first thing a reader meets and the weakest part of earlier
  books. State what the passage claims or answers, not "इसके बाद".
- **Segments** `(T1)`, `(T2)` … each on its own line: a कारिका (both lines + its `॥N॥`) is **one** segment; a वृत्ति
  sentence-group is one segment, broken at its own `।` joints; **a question and its answer are one segment**; a quoted
  verse with its introduction is one segment. Aim for 3–10 segments per §. Concatenated, the segments must reproduce
  the printed text exactly.
- Keep the printed `।` and `॥` exactly. Superscript footnote numerals in the body → write `[१]` at that spot, no more.
  Devanagari digits stay as printed inside the Sanskrit.
- **Footnotes:** `## 11.` lists the foot-of-page footnotes whose reference marks fall inside *this* § (each bullet = its
  printed number and its gloss, verbatim). Numbers restart on each page — add `(पृष्ठ N)` after a number if two pages'
  notes land in one §. No footnotes → omit the `## 11.` block.
- **Never write bold `**…**` anywhere**; no parts other than 6 and 11 — nothing else.

## Accuracy guards
1. **Magnify before committing a doubtful conjunct. `[अस्पष्ट]` is a correct answer; a plausible guess is not.**
2. **Printed letters are the constraint.** Substitute only a letter this fount is known to confuse; never delete or add
   a letter to reach a word. Typical confusions: `प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `ष`↔`प`, `ण`↔`न`, `ध`↔`घ`, `व`↔`ब`,
   `भ`↔`म`, रेफ lost/doubled, `ङ्क`/`ङ्ग`. A word that parses to nothing is almost always the reader's error, not the
   author's — re-read it; but **if it still will not parse, transcribe it as printed and flag it in the report.**
3. **Grep your own earlier segments** for a recurring formula (`तदुक्तं—`, `इति वचनात्`, `प्रसिद्धावयववत्त्व…`,
   `स्वेष्टार्थसाधनस्य`) before guessing; the author reuses his terms constantly.
4. **A quoted verse has a received text** (many are from the author's own or कुमारनन्दि's works). If your reading differs
   from the text as normally transmitted, doubt your reading first, and say so.
5. **Rejoin words broken across a line end** before reading them.
6. **Never "improve" the Sanskrit.** Odd printed forms stay; say so in the report.
7. The pages have **two footnote conventions**: a numbered block at the foot (transcribe) and sometimes *italic/bold
   headwords*. Do not transcribe bold as `**`.

## Style
- English digits in your own prose (§ 30, पृष्ठ 2); Devanagari digits only inside quoted Sanskrit.
- **Never write any sect name** anywhere. No bare आचार्य names in your own prose: `श्री विद्यानन्द स्वामी`,
  `श्री अकलङ्कदेव`, `श्री धर्मकीर्ति` (non-Jain opponents: plain). No working-process language in `parts/`.

## Writing the file
**Write after your FIRST § , then append** (Write first, then Edit). Output file: `parts/patra_pariksha.md`. Separate
consecutive § with a blank line and `---`.

## Report back (under 250 words)
1. the § keys written and total segments; 2. the exact first 6 and last 6 words of मूल with printed page numbers;
3. every `[अस्पष्ट]`, every doubtful reading and every place the Sanskrit looked corrupt — flag, don't fix;
4. confirm every printed page 1–13 is covered and that no passage is repeated; list pages whose first/last line fell
   mid-§.
