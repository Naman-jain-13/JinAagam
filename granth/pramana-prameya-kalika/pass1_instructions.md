# Pass 1 — extraction spec (प्रमाणप्रमेयकलिका)

*Working document. Nothing here goes into the book.*

You are transcribing **प्रमाणप्रमेयकलिका** of **श्री नरेन्द्रसेन** (Jain न्याय prose treatise), a wholly **Sanskrit** text. It is divided
into परीक्षा headed `[१. प्रमाणतत्त्व-परीक्षा]`, `[२. …]` and so on (confirm each heading on the page). The editor numbers the running
text `§ १.`, `§ २.` … (Devanagari digits, one sequence through the whole book); each `§` is one passage of Sanskrit.

**The finished book is an independent Hindi व्याख्या. In this pass you transcribe ONLY the Sanskrit of the text itself. The editor's
Hindi (the footnotes' Hindi glosses) is never transcribed, summarised or paraphrased, and must not shape any § title.** Pass 2 translates
what you transcribe and pass 3 audits it. **Anything you drop or alter is lost silently.** Transcribe every Sanskrit word, exactly.

Source: `mool/Pramana_Prameya_Kalika.pdf` (157 scan pp; page box 342×494 pt, so render at 220+ dpi). **The text runs scan p104 → p149;
printed page = scan page − 103** (scan p104 = printed 1, title + मंगल verse). Render / zoom with:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Pramana_Prameya_Kalika.pdf'); d[IDX].get_pixmap(dpi=220).save(r'<scratch>/bNN_pXXX.png')"
python -c "import pymupdf; d=pymupdf.open(r'mool/Pramana_Prameya_Kalika.pdf'); d[IDX].get_pixmap(dpi=500, clip=pymupdf.Rect(20,60,320,200)).save(r'<scratch>/bNN_z.png')"
```
`IDX = scan page − 1`. Prefix every scratch file with your batch tag (`bNN_`) — other batches share the scratchpad.

## What a page carries
- **Running Sanskrit text** — the main block. **Yours.** It contains: the author's prose; quoted verses (indented, with `॥N॥`); the
  editor's **square-bracket insertions** `[ … ]` — both connecting sentences in Sanskrit at the start of a topic (`[प्रमाण-प्रमेयद्वैविध्यात्
  … प्रस्तूयते—]`) and bracketed source references inside the line (`[ छान्दो० ३।१४।१ ]`, `[ बृहदा० ४-३-१४ ]`). **Keep every bracket exactly as
  printed** — brackets are the editor's, not the author's, and the book will say so. Superscript numerals in the line mark footnotes.
- **Headings** — `[१. प्रमाणतत्त्व-परीक्षा]` and sub-headings in brackets; transcribe as printed, as `(T1)` of the § they open.
- **Running head** — `प्रमाणप्रमेयकलिका` + `[१. § १-` and the page number: **ignore** (but use it to read the page number and the § range).
- **Foot-of-page notes** (numbered `१. २. ३.` keyed to superscripts; also a last line of variants `1 'तेनैव' पाठः। 2 'प्रतिपादकत्वात्'`).
  Transcribe ONLY notes that **quote a source text or give a variant reading or name a work and its page** (`'…' इत्यमरः`, `न्यायसूत्र…`,
  `'आ' प्रतौ …`, `पाठः`). **Skip** the editor's own Hindi explanations and discussion. When unsure, skip.
- The type is a dense old fount at small size: conjuncts blur. **Zoom before committing any doubtful conjunct.**

## § division
**One § = one editor's `§ N.` passage.** The editor's number is printed at its start. If a `§` is very long (more than ~1 full page of
text), split it at a `।`/`॥` joint into two keys (`§…0`, `§…5`) and say so in the report; never split short ones, never merge two.
The editor's `§` numbers must be consecutive across your batch — a jump means you missed one. A bracketed editor connective that sits
**before** a `§ N.` (and after the previous § ended) belongs to the § it introduces, as its first segment `(T1)`.

**Keys:** `§<B×10000 + ordinal×10>` where B = batch number − 1: batch 1 → `§10, §20, …`; batch 2 → `§10010, §10020, …`; and so on
(ordinal restarts in each batch; the builder sorts numerically).

## What to write, per §
Reproduce these headings **verbatim** — a builder parses them.

```
§30 — <short descriptive Hindi title: what this passage establishes> (प्रमाणप्रमेयकलिका, परीक्षा 1, अनुच्छेद 3, मुद्रित पृष्ठ 2)

## 6. संस्कृत मूल पाठ (मूल)
(पृष्ठ 2)
(T1) <first segment, verbatim>
(T2) <second segment>

## 11. मुद्रित पाद-टिप्पणी
- (पृष्ठ 2) ३. "प्रमाणतः सिद्धेः प्रमाणानां प्रमाणान्तरसिद्धिप्रसंगः" — न्यायसूत्र २-१-१०।
```
- The parenthesis is exactly `(प्रमाणप्रमेयकलिका, परीक्षा K, अनुच्छेद N, मुद्रित पृष्ठ P)` — K = the number of the परीक्षा the § sits in;
  N = the editor's printed `§ N` (Arabic digits in this line); a मंगल verse before `§ १` is `अनुच्छेद 0`. P = printed page where the § begins.
- **The title is yours**, in Hindi, from the Sanskrit alone — what the passage claims, asks or answers. Never "इसके बाद".
- **Segments** `(T1)…`: prose is cut at its `।` joints into sentence-groups; **an objection (`ननु … इति चेत्`, `अथ …`) with its answer is one
  segment**; a quoted verse with its introduction is one; a bracketed editor connective is its own segment. Aim for 2–8 per §. Concatenated,
  segments reproduce the § exactly. A footnote superscript → `[१]` / `[२]` at that spot (Devanagari digits, as the note is numbered).
- `## 11.` only when a kept note's mark falls in this §; otherwise omit the block. **No bold `**…**`; only parts 6 and 11.**

## Batches and seams
Your task names your scan range. **A § is yours if its `§ N.` mark begins on one of your pages**; finish it even if it runs onto the
next page. Skip a Sanskrit tail continuing from the previous page (the previous batch finishes it). Batch 1 starts at the title.

## Accuracy guards
1. **`[अस्पष्ट]` is a correct answer; a plausible guess is not.** Magnify (500 dpi) before committing a doubtful conjunct.
2. **Printed letters are the constraint.** Never add or drop a letter to reach a word; substitute only a letter the fount is known to
   confuse (`प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `ष`↔`प`, `ण`↔`न`, `ध`↔`घ`, `व`↔`ब`, `भ`↔`म`, `त्त`↔`न्त`, रेफ lost/doubled, a dropped
   `अ`/avagraha). A word that parses to nothing is almost always a misreading — re-read; if it still will not parse, transcribe as printed and flag it.
3. A quoted verse or sūtra has a received text — if your reading differs, doubt yours first and say so.
4. Rejoin words broken across a line end. Never "improve" the Sanskrit; odd printed forms stay.
5. Do not use the foot-of-page Hindi to settle a reading — settle it on the page, or flag it.

## Style
English digits in your prose; Devanagari digits inside quoted Sanskrit exactly as printed. **Never write any sect name.** No bare आचार्य
names in your own prose (`श्री नरेन्द्रसेन`, `श्री अकलङ्कदेव`; non-Jain names plain). No working-process language in `parts/`.

## Writing the file
**Write after your FIRST §, then append** (Write, then Edit). Output `parts/<file named in your task>`. Separate § with a blank line and `---`.
If an image read ever returns a request-limit / media-removed notice, stop writing immediately and report the page — never write text you did not read.

## Report back (under 250 words)
1. § keys written and total segments; 2. exact first 6 and last 6 Sanskrit words with printed pages (seam check); 3. the editor's `§ N`
numbers covered (consecutive?) and any परीक्षा heading met; 4. every `[अस्पष्ट]` and doubtful reading; 5. whether the boundary pages ran mid-§.
