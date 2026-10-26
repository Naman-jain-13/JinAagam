# Pass 1 — extraction spec (कातन्त्र, दुर्गसिंह-वृत्ति)

*Working document. Nothing here goes into the book.*

You are transcribing the **कातन्त्र-व्याकरण** (सूत्र) with the **वृत्ति of श्री दुर्गसिंह** from J. Eggeling's 1874 Calcutta edition. The text is wholly
**Sanskrit**: each **सूत्र** is printed in large type ending `॥N॥` (N = its number within the पाद), followed by Durgasimha's **वृत्ति** in smaller type
(explanation, कारिका/श्लोक, examples, objections `किमर्थम्`, `इति किम्`). Books: **अध्याय 1–4**, each in पाद; a vṛtti cross-reference is printed in
square brackets as `[का° 1.1.7]` = अध्याय.पाद.सूत्र. The running head of every page gives the current reference, e.g. `कातन्त्रे [का° 2.4.47.`.

**The finished book is an independent Hindi व्याख्या written from your Sanskrit alone. Transcribe ONLY the Sanskrit text of the सूत्र and वृत्ति.** The
edition's English (the manuscript-variant footnotes `B. F. om. …`, `D. adds …`, the preface, the NOTES section, indexes) is never transcribed or used.
**Anything you drop or alter is lost silently.** Transcribe every Sanskrit word, exactly.

Source: `mool/Katantra_Durgasimha.pdf` (549 scan pp, page box 1191×1684 pt, no text layer). **The text runs scan p7 → p431** (scan p5–6 are plates/stamps;
scan p432 is blank; from p433 on = English NOTES and index — NOT yours). Printed page numbers sit in the running head (Devanagari digits in the main text);
read them off the page — they are not a fixed offset from the scan page. **Reading depth (binding):** the scan is a poor 1-bit image (stains, clipped right edge, margin rules). Render every page at **150 dpi minimum** and zoom to **250 dpi on every line that holds a doubtful
conjunct, an example form or a bracketed reference**. A § read only at thumbnail resolution is a defect — never report "unverified" readings; re-read them. Render / zoom with:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Katantra_Durgasimha.pdf'); d[IDX].get_pixmap(dpi=150).save(r'<scratch>/bNN_pXXX.png')"
python -c "import pymupdf; d=pymupdf.open(r'mool/Katantra_Durgasimha.pdf'); d[IDX].get_pixmap(dpi=250, clip=pymupdf.Rect(200,250,1000,700)).save(r'<scratch>/bNN_z.png')"
```
`IDX = scan page − 1`. Prefix every scratch file with your batch tag (`bNN_`) — other batches share the scratchpad.

## What a page carries
- **Running head** — printed page number, `कातन्त्रे`, `[का° A.P.N.]`: ignore, but read the page number and the reference from it.
- **सूत्र** — large type, ends `॥N॥`. **Yours.** A सूत्र may stretch over two printed lines.
- **वृत्ति** — smaller type under it; ends with `॥`, contains `।` joints, examples separated by `।` and `॥`, quoted श्लोक, and bracketed cross-references
  `[का° 1.1.7]`. **Yours, all of it**, until the next सूत्र.
- **Pāda / adhyāya headings and colophons** — e.g. `अथ नामिनः पादः`, `इति … पादः`, `इति दौर्गसिंह्यां वृत्तौ … समाप्तः`: **yours**, as separate segments (see § division).
- **Superscript numerals `(१)`, `(२)` … in the Sanskrit** point at the English variant footnotes: **drop the mark**; read the main text as printed.
  **Do not write `[१]` marks and do not transcribe the footnotes at all.** (The only footnote you may ever keep is one that is itself running Sanskrit
  prose naming a work — if unsure, skip. Report any such note.)
- **Paper defects** — stains, ruled lines at the left edge, library stamps, ink bleed: **zoom before reading** a doubtful conjunct.

## Missing printed pages (scan gaps)
About 28 printed pages are absent from this scan. **Watch the printed page number in the running head of every page**: if it jumps (e.g. 250 → 252) a page is missing there.
- Write nothing for the lost text and never reconstruct it from memory. Put a line `SCAN GAP: printed p<N> missing between सूत्र <a> and <b>` in your report.
- If the first thing on the page after the gap is the **tail of a वृत्ति whose सूत्र and beginning are on the lost page**, record it as a § of its own, keyed by that सूत्र's reference (A.P.N, counting on from the
  previous सूत्र), with title ending `(अंशतः उपलब्ध)`, and make `(T1)` exactly `[स्कैन में मुद्रित पृष्ठ <N> अनुपलब्ध; इस सूत्र का आरम्भ यहाँ उपलब्ध नहीं है]` followed by the tail as `(T2)…`.
- Likewise if a § you are finishing breaks off at the page before a gap, end it with the segment `[आगे का अंश स्कैन में अनुपलब्ध (मुद्रित पृष्ठ <N>)]`.
- Check that सूत्र numbers continue across your batch; list every gap in the report.

## § division
**One § = one सूत्र with its entire वृत्ति** (up to the next सूत्र). The सूत्र numbers in a पाद must be consecutive — a jump means you missed one.
A heading (`अथ … पादः`, adhyāya title) goes as the **first** segment `(T1)` of the first § after it; a closing colophon goes as the **last** segment of the last §
before it. The opening of the book (scan p7: `अथ श्रीदुर्गसिंहविरचितवृत्तिसहितं कातन्त्रम् ॥ ॥गणेशाय नमः॥` + the मङ्गल verse) is a § of its own with `सूत्र 0`.
If a § runs onto the next page, finish it (the next batch skips that tail). **A § is yours if its सूत्र begins on one of your pages.**
Start at the first सूत्र that **begins** on your first page; skip a वृत्ति tail continuing from the previous page.

**Keys:** `§<B×10000 + ordinal×10>` where B = batch number − 1: batch 1 → `§10, §20, …`; batch 2 → `§10010, §10020, …` (ordinal restarts in each batch).

## What to write, per §
Reproduce these headings **verbatim** — a builder parses them.

```
§30 — <short descriptive Hindi title: what this सूत्र lays down> (कातन्त्र, अध्याय 1, पाद 1, सूत्र 3, मुद्रित पृष्ठ 2)

## 6. संस्कृत मूल पाठ (मूल)
(पृष्ठ 2)
(T1) <the सूत्र exactly, with its ॥N॥>
(T2) <first piece of the वृत्ति, verbatim>
(T3) <next piece>
```
- The parenthesis is exactly `(कातन्त्र, अध्याय A, पाद P, सूत्र N, मुद्रित पृष्ठ M)` with **Arabic digits**; A.P.N is the सूत्र's own reference (read the running head or
  count from the previous सूत्र); M is the printed page where the § begins (Arabic digits). For the opening § use `सूत्र 0`.
- **The title is yours**, in Hindi, from the सूत्र and its वृत्ति alone — what the rule lays down (e.g. «सन्धि-प्रकरण का आरम्भ: वर्णसमाम्नाय सिद्ध है»). Never "इसके बाद".
- **Segments** `(T1)…`: **(T1) is always the सूत्र** (or the heading, if there is one — then the सूत्र is (T2)). The वृत्ति is cut at its `॥` joints and where it changes
  function (explanation | example list | objection `किमर्थम्` + answer | `इति किम्` + counter-examples | quoted श्लोक | cross-reference). Aim for 2–8 segments;
  a long list of examples is one segment. Concatenated, the segments reproduce the § exactly, including every `।` and `॥`.
- **No bold `**…**`; only part 6.** Do not write part 11 at all (no footnotes are kept).

## Accuracy guards
1. **`[अस्पष्ट]` is a correct answer; a plausible guess is not.** Zoom (220 dpi) before committing a doubtful conjunct. This is a dense old fount at modest resolution.
2. **Printed letters are the constraint.** Never add or drop a letter to reach a word; substitute only a letter the fount confuses (`प`↔`ष`, `ब`↔`व`, `भ`↔`म`, `घ`↔`ध`,
   `ण`↔`न`, `त्त`↔`न्त`, `ञ्च`↔`श्च`, `ख`↔`रव`, `ऽ` avagraha vs `ड`). In a grammar the **examples are the point**: a word that "parses to nothing" is often a deliberate
   example (a form being derived) — keep it exactly; flag it only if it is clearly a misreading.
3. A quoted श्लोक or वार्त्तिक has a received text — if your reading differs, doubt yours first and say so.
4. Rejoin words broken across a line end. Never "improve" the Sanskrit; odd printed forms stay.
5. Check every सूत्र against the running head's reference and against the numbering of the previous सूत्र.

## Style
English digits in your prose; Devanagari digits only inside the quoted Sanskrit exactly as printed. **Never write any sect name.** No working-process language in `parts/`.

## Writing the file
**Write after your FIRST §, then append** (Write, then Edit). Output `parts/<file named in your task>`. Separate § with a blank line and `---`.
If an image read ever returns a request-limit / media-removed notice, stop writing immediately and report the page — never write text you did not read.

## Report back (under 250 words)
1. § keys written and total segments; 2. exact first 6 and last 6 Sanskrit words with printed pages (seam check); 3. the सूत्र references A.P.N covered
(consecutive?) and every पाद/अध्याय heading or colophon met (exact text); 4. every `[अस्पष्ट]` and doubtful reading; 5. whether the boundary pages ran mid-§;
6. any footnote you found that is Sanskrit prose (not an English variant list).
