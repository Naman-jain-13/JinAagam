# Pass 1 — extraction spec (प्रमाणनिर्णय)

*Working document. Nothing here goes into the book.*

You are transcribing **प्रमाणनिर्णय** of **श्री वादिराजसूरि** (11th c.), a wholly **Sanskrit** न्याय treatise in prose, in four
निर्णय: **प्रमाणलक्षणनिर्णय**, **प्रत्यक्षनिर्णय**, **परोक्षनिर्णय**, **आगमनिर्णय** (confirm each heading on the page; there may be
sub-headings). The edition prints each **Sanskrit paragraph** (bold) closing with a running number `॥N॥` (`।।61।।` — Devanagari or
Arabic digits as printed), and **after it a modern Hindi translation** of that paragraph by the editor.

**The finished book is an independent Hindi व्याख्या: it must contain no existing Hindi translation and no editor's name. In this
pass you transcribe ONLY the Sanskrit. You never transcribe, summarise or paraphrase the printed Hindi paragraphs — skip every one of
them, and do not let them shape anything you write, including the § title.** Pass 2 translates what you transcribe and pass 3 audits
that translation against it. **Anything you drop or alter is lost silently.** Transcribe every Sanskrit word, exactly.

Source: `mool/Pramana_Nirnaya.pdf` (129 scan pp; **the text runs scan p21 → p129; printed page = scan page − 20**; scan p1–20 are the
editor's Hindi introduction — not yours). Page box 612×792 pt. Render / zoom with:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Pramana_Nirnaya.pdf'); d[IDX].get_pixmap(dpi=200).save(r'<scratch>/bNN_pXXX.png')"
python -c "import pymupdf; d=pymupdf.open(r'mool/Pramana_Nirnaya.pdf'); d[IDX].get_pixmap(dpi=450, clip=pymupdf.Rect(60,100,560,300)).save(r'<scratch>/bNN_z.png')"
```
`IDX = scan page − 1`. Prefix every scratch file with your batch tag (`bNN_`) — other batches share the scratchpad.

## What a page carries
- **Sanskrit paragraphs** — bold, denser type; each ends `॥N॥` with the running paragraph number. **Yours.**
- **Hindi paragraphs** — regular weight, directly after each Sanskrit paragraph, also ending `।।N।।`. **Skip entirely.**
- **Headings** — `मंगलाचरणम्`, `प्रमाणलक्षणनिर्णयः। (प्रथम लक्षण निर्णय)` etc. Transcribe only the Sanskrit heading (`प्रमाणलक्षणनिर्णयः।`),
  not its Hindi gloss in brackets. Ignore the faint grey watermark line `मार्गदर्शक :- …` and the bilingual title block's Hindi lines.
- **Foot-of-page notes** (numbered `¹ ² ³`, keyed to superscripts in the Sanskrit). Transcribe ONLY notes that **quote a source text or
  give a variant reading** (a quoted verse/sūtra, `इत्यमरः`, a named work, `पाठान्तरम्`). **Skip** notes that are the editor's own
  explanatory gloss in Sanskrit or Hindi (`अनध्यवसाय।`, `उद्धृत इति शेषः।`, `इन्द्रियलिङ्गादावपि।` and the like). When unsure, skip.

## § division
Each printed Sanskrit paragraph `॥N॥` is the natural unit: **one § = one printed paragraph** (merge two only when a paragraph is a
single short line that only makes sense with the next; split never). The running `॥N॥` numbers must be consecutive — 3 then 5 means you
missed 4.

**Keys:** `§<B×10000 + ordinal×10>` where B = batch number minus 1: batch 1 → `§10, §20, …`; batch 2 → `§10010, §10020, …`; batch 3 →
`§20010 …` and so on (ordinal restarts in each batch; the builder sorts numerically).

## What to write, per §
Reproduce these headings **verbatim** — a builder parses them.

```
§30 — <short descriptive Hindi title: what this passage establishes> (प्रमाणनिर्णय, निर्णय 1, अनुच्छेद 3, मुद्रित पृष्ठ 1)

## 6. संस्कृत मूल पाठ (मूल)
(पृष्ठ 1)
(T1) <first segment, verbatim>
(T2) <second segment>

## 11. मुद्रित पाद-टिप्पणी
- (पृष्ठ 1) ३. "प्रश्नावधारणानुज्ञानुनयामंत्रणे ननु" इत्यमरः।
```
- The parenthesis is exactly `(प्रमाणनिर्णय, निर्णय K, अनुच्छेद N, मुद्रित पृष्ठ P)` — K = 1–4 by the निर्णय; N = the printed `॥N॥` of the
  paragraph (merged pair: the first); for a heading/मंगल § before paragraph 1 use `अनुच्छेद 0`. The contents page is built from it.
- **The title is yours**, in Hindi, from the Sanskrit alone — what the paragraph claims or answers. Never "इसके बाद".
- **Segments** `(T1)…`: a मंगल verse is one segment; prose is cut at its `।` joints into sentence-groups; **an objection (`ननु … इति चेत्`)
  with its answer is one segment**; a quoted verse with its introduction is one. Aim for 2–8 per §. Concatenated, segments reproduce the
  paragraph exactly, including the closing `॥N॥`. A footnote superscript in the Sanskrit → `[१]` / `[२]` at that spot.
- `## 11.` only when a kept note's mark falls in this §; otherwise omit the block. **No bold `**…**`; only parts 6 and 11.**
- A निर्णय heading (`प्रत्यक्षनिर्णयः।`) goes as `(T1)` of the first § of that निर्णय.

## Batches and seams
Your task names your scan range. **A paragraph is yours if its Sanskrit begins on one of your pages**; finish it even if it runs onto the
next page. Start at the first Sanskrit paragraph that **begins** on your first page — skip a Sanskrit tail continuing from the previous
page (the previous batch finishes it).

## Accuracy guards
1. **Magnify before committing a doubtful conjunct (450 dpi). `[अस्पष्ट]` is a correct answer; a plausible guess is not.**
2. **Printed letters are the constraint.** Never add or drop a letter to reach a word; substitute only a letter the fount is known to confuse
   (`प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `ष`↔`प`, `ण`↔`न`, `ध`↔`घ`, `व`↔`ब`, `भ`↔`म`, रेफ lost/doubled, a dropped `अ`/avagraha). A word that
   parses to nothing is almost always a misreading — re-read; if it still will not parse, transcribe as printed and flag it.
3. **Do not use the Hindi paragraph to settle a Sanskrit reading** — settle it on the page, or flag it.
4. Rejoin words broken across a line end. Grep your own earlier segments for recurring formulas before guessing.
5. A quoted verse has a received text — if your reading differs, doubt yours first and say so.
6. Never "improve" the Sanskrit; odd printed forms stay.

## Style
English digits in your prose; Devanagari/Arabic digits inside quoted Sanskrit exactly as printed. **Never write any sect name.** No bare
आचार्य names in your own prose (`श्री वादिराजसूरि`, `श्री अकलङ्कदेव`; non-Jain names plain). No working-process language in `parts/`.

## Writing the file
**Write after your FIRST §, then append** (Write, then Edit). Output `parts/<file named in your task>`. Separate § with a blank line and `---`.
If an image read ever returns a request-limit / media-removed notice, stop writing immediately and report the page — never write text you did not read.

## Report back (under 250 words)
1. § keys written and total segments; 2. exact first 6 and last 6 Sanskrit words with printed pages (seam check); 3. the `॥N॥` numbers covered
(consecutive?) and any निर्णय heading met; 4. every `[अस्पष्ट]` and doubtful reading; 5. whether the boundary pages ran mid-paragraph.
