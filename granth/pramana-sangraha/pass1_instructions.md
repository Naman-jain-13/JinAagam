# Pass 1 — extraction spec (प्रमाणसंग्रह)

*Working document. Nothing here goes into the book.*

You are transcribing **प्रमाणसंग्रह** of **श्रीमद्भट्टाकलङ्कदेव** (अकलङ्क), a dense, wholly **Sanskrit** न्याय treatise in
**nine प्रस्ताव** — numbered **कारिका** (verses closing `॥ ३ ॥`) interleaved with the author's own prose **वृत्ति**, which the
editor has divided into numbered paragraphs `§ १.`, `§ २.` … There is **no Hindi and no छाया in the source.** Pass 2 will
translate what you transcribe and pass 3 audits that translation against it. **Anything you drop or alter is lost silently.**
Transcribe every word, exactly.

Source: `mool/Pramana_Sangraha_Akalanka.pdf` (32 pp; rendered `img/p01.png … p32.png`; **p01 is the title page**). Open
the images with the Read tool and zoom a doubtful conjunct:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Pramana_Sangraha_Akalanka.pdf'); d[IDX].get_pixmap(dpi=450, clip=pymupdf.Rect(60,100,560,400)).save(r'<scratch>/z.png')"
```
`IDX = page − 1`; the page box is 612×792 pt. The scan is cream-toned but clean and legible.

## What a page carries
- **Running header:** `कारिका ८–१०]  प्रमाणसङ्ग्रहः  ८६` / `२. द्वितीयः प्रस्तावः  ८६` — the कारिका range of the page and a printed
  page number (this book's own numbering, e.g. ८६ on scan p03). Record it.
- **प्रस्ताव headings:** `१. प्रथमः प्रस्तावः`, `२. द्वितीयः प्रस्तावः`, … and closings `इति प्रमाणसङ्ग्रहे प्रथमः प्रस्तावः ॥१॥`.
- **कारिका:** centred two-line verses closing `॥ N ॥` (numbered afresh in each प्रस्ताव). Some कारिका are printed in square
  brackets `[§ १. … ॥ २ ॥]` — keep the brackets.
- **वृत्ति paragraphs** opening `§ १.`, `§ २.` … (the editor's numbering; restarts in each प्रस्ताव), flowing prose in **small type**
  that glosses the preceding कारिका word by word and then argues.
- **Margin line-numbers** `5`, `10`, `15`, `20` … at the right edge: **ignore them entirely** (they are the editor's line counts).
- **Foot-of-page footnotes** (`* प्रत्यभिज्ञा स्मृति ऊह`, or numbered): the editor's variant readings / glosses, keyed to `*` or a
  number in the body. Transcribe them.
- **Editorial brackets inside the text:** `(अव्युत्पन्न)`, `[ चेः ]`, `(र्थ्या)` etc. are the editor's emendations/variants — keep every
  bracket and parenthesis exactly where printed. `।।छ।।` / `॥छ॥` is the scribe's closing mark — keep it.

## § division — YOU decide it, carefully
Divide each प्रस्ताव into **numbered § (key = 10000×B + running ordinal×10, where B is your batch number — see below)** of
**roughly one कारिका plus its वृत्ति paragraph** (about 1/4–1/3 of a page). Natural joints: a कारिका with the `§ N.` paragraph(s)
that follow it; an objection with its answer. Never end a § mid-sentence; **never separate a question from its answer nor a
quoted verse from its introduction.** Every word of the printed text must belong to exactly one §, in reading order, **nothing
repeated, nothing missing**. The `॥ N ॥` कारिका numbers in a प्रस्ताव run consecutively — if you see 3 then 5, you swallowed a 4.

**Keys.** Use `§<B><NNN>0` style: batch 1 → `§10, §20, …`; batch 2 → `§10010, §10020, …`; batch 3 → `§20010, §20020, …`.
(A batch's own ordinal restarts at 1; the builder sorts numerically so reading order is preserved.)

## What to write, per §
Reproduce these headings **verbatim** — a builder parses them.

```
§30 — <short descriptive Hindi title: what this passage establishes> (प्रमाणसंग्रह, प्रस्ताव 1, कारिका 3, मुद्रित पृष्ठ 13)

## 6. संस्कृत मूल पाठ (मूल)
(पृष्ठ 13)
(T1) <first segment, verbatim>
(T2) <second segment>

## 11. मुद्रित पाद-टिप्पणी
- * प्रत्यभिज्ञा स्मृति ऊह
```
- **The parenthesis at the end of the title must be exactly** `(प्रमाणसंग्रह, प्रस्ताव N, कारिका M, मुद्रित पृष्ठ P)` — where `M` is the
  printed कारिका number the § opens with (or the **last कारिका just closed** if the § is pure वृत्ति: write `कारिका 3 की वृत्ति`
  is NOT allowed — write `कारिका 3` and put the nuance in the Hindi title). For a § before any कारिका of the प्रस्ताव (headings, मङ्गल
  `॥ नमः श्रीवर्द्धमानाय ॥`), use `कारिका 0`. For two कारिका in one § write the first. **Never** use a different form: the
  contents-page is built from it.
- The title is **yours**, in Hindi, accurate: state what the passage claims or answers. Never "इसके बाद".
- **Segments** `(T1)`, `(T2)` …: a कारिका (both lines + `॥N॥`) is **one** segment; a वृत्ति paragraph is cut at its own `।`/`॥`
  joints into sentence-groups; **a question and its answer are one segment; a quoted verse with its introduction is one**. Aim for
  3–10 per §. Keep the `§ १.` marker at the head of the segment where it is printed. Concatenated, segments reproduce the text exactly.
- Keep the printed `।` and `॥` exactly; Devanagari digits stay as printed. A footnote mark `*`/number in the body → write `[*]`
  or `[१]` at that spot, no more.
- `## 11.` lists the footnotes whose marks fall inside this § (verbatim). Numbers restart per page — add `(पृष्ठ N)` if two pages
  land in one §. None → omit the block.
- **No bold `**…**` anywhere**; only parts 6 and 11 — nothing else.

## Batches
- **Batch 1 (B=1): scan p01–p11**, **Batch 2 (B=2): p12–p22**, **Batch 3 (B=3): p23–p32.** A § or sentence that runs onto the
  next page is yours if it **starts** on your last page; the next batch must not repeat it, and **starts at the first thing that
  begins on its first page** (skip the tail of a sentence begun on the previous page — the previous batch finished it). Finish
  the tail of your last page's last sentence even if it spills onto the next page's first lines.
- p01 is the title page: it belongs to batch 1 (`श्रीमदट्टाकलङ्कविरचितः । प्रमाणसङ्ग्रहः` = §10 `कारिका 0`).

## Accuracy guards
1. **Magnify before committing a doubtful conjunct. `[अस्पष्ट]` is a correct answer; a plausible guess is not.**
2. **Printed letters are the constraint.** Never delete or add a letter to reach a word; substitute only a letter the fount is
   known to confuse (`प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `ष`↔`प`, `ण`↔`न`, `ध`↔`घ`, `व`↔`ब`, `भ`↔`म`, रेफ lost/doubled,
   `ङ्क`↔`ङ्ग`). A word that parses to nothing is almost always your misreading — re-read; **if it still will not parse,
   transcribe as printed and flag it.**
3. **Grep your own earlier segments** (`grep` the file you are writing) for recurring formulas before guessing.
4. **A quoted verse has a received text** — if your reading differs from the text as normally transmitted, doubt yours first.
5. **Rejoin words broken across a line end** before reading them.
6. **Never "improve" the Sanskrit**; odd printed forms stay (the edition has `ऽ` avagraha dropped in places, `।।छ।।` marks, etc.).
7. The editor's brackets/parentheses are **content** — keep them; the later pass uses them to understand variant readings.

## Style
- English digits in your prose (§ 30, पृष्ठ 13); Devanagari digits only inside quoted Sanskrit.
- **Never write any sect name** anywhere. No bare आचार्य names in your own prose: `श्री अकलङ्कदेव`, `श्री धर्मकीर्ति` (non-Jain: plain).
  No working-process language in `parts/`.

## Writing the file
**Write after your FIRST §, then append** (Write first, then Edit). Output file: `parts/batchB_pXX-YY.md` (as named in your task).
Separate consecutive § with a blank line and `---`.

## Report back (under 250 words)
1. the § keys written and total segments; 2. exact first 6 and last 6 words of मूल with printed page numbers (for seam checks);
3. every `[अस्पष्ट]`, doubtful reading, and place the Sanskrit looked corrupt — flag, don't fix; 4. the **कारिका numbers
you covered per प्रस्ताव** (so continuity can be checked); 5. whether your boundary pages ran mid-§.
