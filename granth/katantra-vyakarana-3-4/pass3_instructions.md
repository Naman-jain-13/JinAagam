# Pass 3 — independent audit spec (कातन्त्र, दुर्गसिंह-वृत्ति, अध्याय 3–4)

*Working document. Nothing here goes into the book.*

Two earlier agents worked on each § of your range: one **transcribed the Sanskrit from a blurred scan** (`parts/`), another **wrote the Hindi व्याख्या** from that transcription (`addenda/`). You saw neither.
**You are the only reader who holds the scan.** Your job has two halves, and the first matters more in this book, because a grammar's examples *are* its proof and the scan is poor:

**A. Sanskrit ↔ scan (the transcription).** **B. Hindi ↔ Sanskrit (the translation and the व्याख्या).** You **report; you do not edit `parts/` or `addenda/`**.

For each § key in your range read: `parts/batch*_*.md` (the § block: सूत्र + वृत्ति in `(Tn)` segments) and `addenda/s<key>.md`. The scan is `mool/Katantra_Durgasimha.pdf` (page box 1191×1684 pt, 1-bit, blurred; **the scan→printed offset varies**: printed = scan−6 up to scan ≈188, then irregular up to scan ≈204 (see `verify/pagemap_1.txt`, `pagemap_2.txt`: ≈40 printed pages of adhyāya 3 are missing from the scan), printed = scan+31 for scan 250–315, +32 from scan 316 (`pagemap_3..6.txt`; printed 347 is lost). Always read the running head `कातन्त्रे [का° A.P.N]` and the printed number; `IDX = scan − 1`). **The title's `मुद्रित पृष्ठ` of many § were set from agent readings and may be off — check each against the page and report the right number.** Some titles carry a wrong अध्याय/पाद/सूत्र number from a misread running head: check it. The edition's English footnotes are variant lists — **never use them to judge anything**; the English notes after scan p432 are not in this book.

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Katantra_Durgasimha.pdf'); d[IDX].get_pixmap(dpi=150).save(r'<scratch>/aNN_pXXX.png')"
python -c "import pymupdf; d=pymupdf.open(r'mool/Katantra_Durgasimha.pdf'); d[IDX].get_pixmap(dpi=300, clip=pymupdf.Rect(150,250,1050,700)).save(r'<scratch>/aNN_z.png')"
```
Prefix scratch files with your tag (`aNN_`).

## A. Sanskrit ↔ scan — do this FIRST, line by line
Read the scan page for each § (zoom to 300 dpi in half-page crops; **zoom to 450 dpi on every example form and every doubtful conjunct**) and compare with `parts/`:
- **ट्रांसक्रिप्शन-त्रुटि:** a letter, word, `॥`/`।`, a whole example, a numeral or a bracketed reference `[का° A.P.N]` that differs from the print — give **the exact printed reading** and a confidence (`स्पष्ट` / `सम्भावित`). Fount confusions to test first: `क्ष`↔`च`, `त्व`↔`ल्व`, `श्च`↔`स्व`, `ष`↔`प`, `ण`↔`न`, `घ`↔`ध`, `थ`↔`य`, `ब`↔`व`, `भ`↔`म`, `त्र`↔`च`, `इ`↔`द`, `ऋ`↔`ॠ`, anusvāra/visarga lost.
- **Dropped or added text:** a line of the वृत्ति missing, a segment out of order, a tail that belongs to the next/previous §.
- **`[अस्पष्ट]` that you can read** → give the reading and confidence; **a reading that looks confident in `parts/` but is not what the print shows** → report.
- **Normalisations:** the printed form was "corrected" silently (e.g. the print `सवत्र` written `सर्वत्र`) → report for restoration. **Printed oddities stay as printed**; do not report a misprint as an error of the transcription — report it only as a note ("मुद्रित रूप ऐसा है").
- The vowel/consonant class name printed `घुड्`/`घुट्`: settle on the scan whether the print has घ or ध, wherever it occurs in your range, and say which.
- **Cross-reference numbers** in `[का° A.P.N]` inside the वृत्ति: read the digits carefully; the vṛtti's own numbering may differ from the printed ॥N॥ of the सूत्र — that is a feature of the edition, not an error (note it, don't "fix" it).
- **Printed page numbers** in each § title line (`मुद्रित पृष्ठ P`): check against the running head.
Settle every flag in `verify_flags.md` that falls in your range: `RESOLVED → <reading>` with evidence, or `STANDS AS PRINTED`.

## B. Hindi ↔ Sanskrit — after A, with the *corrected* Sanskrit
**Read the Sanskrit first and construe it yourself before reading the Hindi.** Finding types: **त्रुटि** (the Hindi states what the Sanskrit does not / contradicts it: wrong समास split, wrong विभक्ति, a negation or particle dropped, an `इति किम्` answer attached to the wrong word, a wrong anuvṛtti) · **लोप** (a word, qualifier or segment with no Hindi counterpart; any `(Tn)` without a Hindi line) · **वर्धन** (Hindi adds in part 6 what that segment does not say) · **सन्देह** (defensible, another reading at least as good).
Check especially:
1. **Part 6:** सूत्रार्थ right (test it against the वृत्ति's own examples — a reading under which the rule would not give those examples is wrong); every example translated/glossed; quoted verses complete; enumerations complete.
2. **Part 7:** पदच्छेद, समास-विग्रह and विभक्ति of the सूत्र words; the anuvṛtti claimed (check the earlier सूत्र in `parts/`); `का° A.P.N` cross-references exact (they must name a सूत्र you can find in `parts/` that says what is claimed); no claim that the text does not support; Pāṇini parallels hedged.
3. **Part 7-क (सिद्धि-प्रक्रिया):** every derivation step must follow from a rule that exists in the book (check the cited सूत्र in `parts/`) or be marked `(सूत्र उपलब्ध पाठ में नहीं)`; **the writer's own reasons are marked `(व्याख्याकार का तर्क)`, only the वृत्ति's stated purposes are `ग्रन्थ के अनुसार`** — report any reversal; a derivation that would give a wrong form is a त्रुटि.
4. **Part 8/9/9-क:** every example, table row and drill is grammatically sound (derive it yourself); tags exactly `[ग्रन्थ-सम्मत]`/`[सुझाव]`, never both, never a suggested count presented as the text's.
5. **Part 10:** notes about doubtful readings match what you saw on the scan: a note that blames the print for a slip of the transcription is a त्रुटि (the print is the authority — if the scan clearly reads X and `parts/` says Y, the note is wrong).
6. **Titles** (first line of each § in `parts/`): must say what THAT सूत्र lays down; report wrong titles with a corrected one.
7. **Honorifics/style:** `श्री दुर्गसिंह`, `श्री शर्ववर्मा`, `श्री रत्नेश्वरचक्रवर्ती`; no sect names; no process words.

**Not findings:** a different but equally faithful wording; idiom; free expansion that the Sanskrit supports. **Never invent a finding** — each must be checkable by someone holding the page. **Never report a gap in the text as missing text** unless the scan page shows the text.

## Special cases in this range
- **Missing/tail-only §:** § whose सूत्र is lost (only the वृत्ति tail survives) and `[स्कैन में … अनुपलब्ध]` markers are real: never report them as errors, and **never supply the missing text**. Report only if the Hindi invents the lost sūtra/examples.
- **Scrambled pages:** printed 405–406 (§360250–§360320) are physically scrambled in the scan with ~37 `[अस्पष्ट]`; fill only what you can read, check that the Hindi did not fill the rest.
- **Known doubtful forms** are listed per § in `progress.md` (pass-1/pass-2 notes); fount slips (क्ष/च, श/श्र, स/श्व, ध/घ, इ/द, ल/त्व, स/म, ज्/न) are frequent — test each flagged form on the scan at 450 dpi.
- **Cross-references** `[का° A.P.N]` printed in the वृत्ति sometimes disagree with the volume's own numbering (e.g. वृत्ति cites 4.2.25 for a rule that is 4.2.35 here); note, don't 'fix', unless the Hindi cites the wrong sūtra.
- The राजादि-गण sub-sūtras (keys §130160–§130280, §140010–§140460) are numbered within their own list and belong to the **राजादि-वृत्ति of रत्नेश्वरचक्रवर्ती** (printed colophon `इति रत्नेश्वरचक्रवर्तिविरचितराजादिवृत्तिः समाप्ता`, §140460) — not Durgasimha's; check the Hindi never calls them Durgasimha's.
- §10 is the मङ्गल (no सूत्र); the last § (§140550) ends with the colophon of अध्याय 2.
- The adhyāya-1/pāda colophons are real printed text: `इति दौर्गसिंह्यां वृत्तौ … पादः समाप्तः`.

## Output — one file per range: `verify/v_<tag>.md`
```
# <tag> — <first key>…<last key> (का° …)
## सारांश — counts: Sanskrit-पाठ-सुधार N · त्रुटि N · लोप N · वर्धन N · सन्देह N
## A. पाठ-सुधार (parts/)
- §key · (Tn) · parts reads «…» → print reads «…» · scan p<N> · विश्वास: स्पष्ट/सम्भावित
## B. हिन्दी
- §key · part · type · the exact wrong text → replacement line (ready to paste) · basis
## verify_flags: RESOLVED / STANDS list
## शीर्षक सुझाव
```
Give every finding a **ready replacement** (Sanskrit line or Hindi line). Under 12 findings are fine for a clean § — do not pad.

## Report back (under 250 words)
Counts per type; the 5 most important findings; every flag you could not settle; whether any § needs a re-read of a *neighbouring* page you did not have.
