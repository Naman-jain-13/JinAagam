# जैनेन्द्र सिद्धान्त कोश — पृष्ठशः लिप्यन्तरण : कार्य-विनिर्देश

*Working document. Nothing here goes into the book.*

**Rights:** the project owner holds the permissions for this re-typeset edition of जैनेन्द्र सिद्धान्त कोश (confirmed
to the coordinator on 2026-11-03); full page-by-page transcription is the authorised task.

Goal: a new PDF of each भाग in which **PDF page N carries exactly the content of the original's PDF page N** —
same text, same order, same two-column split. You transcribe pages; a builder lays them out. Doubtful readings and
obvious printing errors are reported in a notes block and become पाद-टिप्पणी on that same page.

## Source
`bhag-K\mool\Jainendra_Siddhant_Kosh_K.pdf` (scan, no text layer, A4, 1241×1754 px images ≈ 150 dpi).
Render to read — **always zoom**; the type is small and dense:
```
python -c "import pymupdf; d=pymupdf.open(r'mool\Jainendra_Siddhant_Kosh_K.pdf'); p=d[IDX]; r=p.rect; d[IDX].get_pixmap(dpi=300, clip=pymupdf.Rect(0,0,r.width/2,r.height/3)).save(r'<scratch>\<prefix>_z.png')"
```
`IDX = PDF page − 1`. Read each column in strips (top/middle/bottom thirds, left and right halves) at 300 dpi;
zoom to 400–500 dpi on any doubtful word, conjunct, number or citation. Put scratch files in the session scratchpad
with your batch prefix.

## What to write — one file per page: `bhag-K\pages\p0NNN.md` (NNN = PDF page, 4 digits)
```
<!-- PDF 251 -->
@head-left: आगम
@head-right: २२६ ६. आगमकी प्रामाणिकताके हेतुओंमें उपस्थित शंका-समाधान
@foot: जैनेन्द्र सिद्धान्त कोश

@col1
… left column, top to bottom …

@col2
… right column, top to bottom …

@notes
- <exact quoted text> — <what is wrong / doubtful> — <likely reading, if obvious>
```
Rules:
1. **Everything printed on the page, in reading order**: running head (left/right), page number, column 1 then
   column 2, footer. Full-width elements (a page title, a table spanning both columns) go under `@full` before or
   after the columns, in the position they occupy.
2. **The print governs, letter for letter.** Never "correct" a word toward grammar or toward what it should be —
   transcribe what is printed, and report the problem under `@notes`. Keep Devanagari digits as printed
   (२२६, ६/२/३), punctuation (।, ॥, —, =), spacing of citation strings (ध. १/४,१,४५/१२६/४), parentheses and brackets.
3. Structure marks: numbered headings (`१०. विचित्र द्रव्यों …`, `९ अर्वाचीन पुरुषों…`) → `### ` line;
   bold text → `**…**`; an indented sub-entry → keep its own paragraph. One blank line between paragraphs.
   A word hyphenated across a line end → rejoin it. A word or sentence that continues on the next page → leave it
   cut exactly where the page ends (do not complete it), and start the next page file where the print starts.
4. Tables → markdown table in the same position. Diagrams/figures you cannot render → `[चित्र: short description]`.
5. **Doubt**: a letter/word you cannot read with confidence even at 500 dpi → `[अस्पष्ट]` in place (or `वर्ध[?]मान`
   for a single doubtful letter) and a line under `@notes`. Never guess silently.
6. `@notes` (→ पाद-टिप्पणी): obvious printing errors (wrong/dropped मात्रा, duplicated word, broken citation,
   wrong cross-reference page), illegible spots, and anything a reader must be told. One line each, short. If none,
   write `- कोई नहीं`.
7. Known scan traps (from earlier books): a full consonant + hyphen at a line end means अ follows (तद-/प्रयोजक);
   द/द्व/ढ, घ/ध, भ/म, ब/व, ष/प, ङ/ड, रेफ above vs र् ; ऽ (अवग्रह) easily lost; ० vs ०, १/९, ६/६. Zoom before deciding.
8. Write each page file as soon as that page is done (do not accumulate). Do not open other batches' files.

## Report (≤150 words)
Pages done; count of `[अस्पष्ट]`; pages with tables/figures; anything structurally odd (blank page, plate, index).
