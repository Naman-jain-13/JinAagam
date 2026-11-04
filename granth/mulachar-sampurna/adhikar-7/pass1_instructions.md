# Pass 1 — extraction spec (मूलाचार, अधिकार 7 : षडावश्यकाधिकार)

*Working document. Nothing here goes into the book.*

You are transcribing part of **मूलाचार** by **श्री वट्टकेराचार्य** (प्राकृत गाथा) together with **श्री वसुनन्दि-सिद्धान्तचक्रवर्ती's
संस्कृत आचारवृत्ति**. The finished book is an **independent** Hindi व्याख्या: it must contain no existing Hindi translation and no translator's
name. **Therefore in this pass you transcribe ONLY the प्राकृत गाथा, the संस्कृत आचारवृत्ति, and the manuscript-variant footnotes. You never
transcribe, summarise or paraphrase the printed Hindi.** (Every scan page carries Hindi below a horizontal rule — you will see it; ignore it
completely, do not copy any of it, and do not let it shape what you write, including the § title.)

**The single most important thing you produce is the संस्कृत आचारवृत्ति, transcribed completely and exactly.** A later pass translates it into Hindi
and a third pass audits that translation against what you wrote; if you drop or alter a word nothing can recover it. Chapter 1 of this book was
found to contain ~25 misreadings of this kind once an auditor compared the scan — read every doubtful conjunct at high zoom.

Source: `mool/Mulachar_Purvardh_Aryika_Jnanmati.pdf`; rendered pages `img/p0442.png … p0563.png` (`p<scan page>`; **printed page = scan page − 58**).
Zoom a doubtful region:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Mulachar_Purvardh_Aryika_Jnanmati.pdf'); d[IDX].get_pixmap(dpi=500, clip=pymupdf.Rect(40,100,470,260)).save(r'<scratch>/z.png')"
```
`IDX = scan page − 1`; page box 504×666 pt.

## What you transcribe from each page

**Above the horizontal rule only:**
1. an optional **Sanskrit पातनिका** in small type introducing a गाथा (`अथ … आह`, `तावदाह`, `अनन्तरं … प्रतिपादयति`);
2. the **प्राकृत गाथा** in large bold type, centred, two lines, closing `॥N॥` (N = the global गाथा number: this अधिकार holds गाथा 502 … 692; it begins on scan p0442 with the title `७. षडावश्यकाधिकारः` and ends with `इति श्रीवट्टकेराचार्यवर्यप्रणीतमूलाचारस्य वसुनन्दाचार्यविरचितायामाचारवृत्तावावश्यकनिर्युक्तिनामकः सप्तमः परिच्छेदः ॥७॥` at the top of scan p0562 (scan p0559–0561 between the last गाथा 692 on p0558 and that closing carry Hindi विशेषार्थ and Prakrit कृतिकर्म/भक्ति prayer text with no numbered गाथा — transcribe any Prakrit/Sanskrit that is part of the वृत्ति stream, flag the rest in your report); scan p0563 onward is the गाथानुक्रमणिका — do not transcribe it on scan p0562);
3. **श्री वसुनन्दि's आचारवृत्ति**, dense small type — it glosses the गाथा word by word (`तिहुयणमंदरमहिदे—मन्दरे …`, the गाथा's own प्राकृत words set in bold and
   followed by `—` and the Sanskrit gloss), then the construction (`इति सम्बन्धः`), objections and answers, quoted verses, closing summary.

**Not the Hindi stream below the rule** (हिन्दी पातनिका, `गाथार्थ—`, `आचारवृत्ति—`, `विशेष—`/`भावार्थ—`, शंका-समाधान, tables).

**Footnotes at the foot of the page** (numbered `१. क "…"`): transcribe only the **manuscript variants, Sanskrit/Prakrit readings and source citations**
(`क "आचार"`, `२. अस्य स्थाने … पाठः`, `* धवला पु. प्र. पृ. २५१`, a quoted गाथा in Prakrit). **Skip any footnote that is a Hindi explanation** (a sentence of Hindi
describing meaning or story, `अर्थ—`, `भावार्थ—`). If a footnote quotes an extra Prakrit/Sanskrit गाथा, keep the गाथा text (not its Hindi meaning).

Page content runs across page breaks; the Sanskrit stream and the Hindi stream are not page-synchronised — **follow only the Sanskrit stream** and its `॥N॥`
closings. Expect to read a page past your range to finish a गाथा whose वृत्ति you opened.

## § numbering — key = गाथा × 10

`§5020` = गाथा 502, `§6920` = गाथा 692. Where the वृत्ति explains **several गाथा together under one combined पातनिका and one वृत्ति block**
(not separate वृत्ति for each), write one § keyed to the first गाथा and give the title `(अधिकार 7, गाथा 200–201, मुद्रित पृष्ठ 164)`. Merge only when they truly share one
वृत्ति; if each has its own, one § per गाथा.

## What to write, per गाथा

Reproduce these headings **verbatim** — a builder parses them.

```
§5020 — गाथा 502 (अधिकार 7, गाथा 502, मुद्रित पृष्ठ 384)

## 1. मूल पाठ (प्राकृत गाथा)
(पृष्ठ 161)
<the गाथा exactly as printed, two lines, ॥१९८॥ in Devanagari digits>

## 6. श्री वसुनन्दि-कृत संस्कृत टीका — आचारवृत्ति (मूल)
(T1) <first segment, verbatim>
(T2) <second segment>

## 11. मुद्रित पाद-टिप्पणी
- (पृष्ठ 161) १. क "…"
```
- **The § title is just `गाथा N`** (plus the parenthesis) — **do not write a descriptive title**; the later pass writes it from the Sanskrit alone, so no Hindi can leak
  through the title. The parenthesis form `(अधिकार 7, गाथा N, मुद्रित पृष्ठ P)` is exact — the contents page is built from it.
- Part 6's heading must contain `टीका` (the builder keys on it). Nothing else: no parts 2, 3, 4, 5, 7–10. Omit `## 11.` when the गाथा has no variant footnote.
- **Never write a bold `**…**` anywhere.**
- Where an opening or closing sentence names a division (`इति … सप्तमः प्रस्तावः`, `अथ … कथ्यते`), keep it: a closing one is the last segment of the
  last गाथा it follows; an opening one is `(T1)` of the गाथा it introduces.

### Segmenting the आचारवृत्ति
Tag `(T1)`, `(T2)` … each on its own line. A segment is: the पातनिका; **a गाथा-pada word with its gloss** (`तिहुयणमंदरमहिदे—मन्दरे …`, one segment per प्राकृत
word-group as the gloss runs); **a question together with its answer** (never split शङ्का from समाधान, nor a `कथंभूत`/`किमर्थम्` question from its answer);
a quoted verse with its introduction and named source; the closing summary / `इति सम्बन्धः`. Aim for 6–25 segments per गाथा. **Every printed Sanskrit word must fall inside
some segment; concatenated, the segments reproduce the text exactly.** The प्राकृत words inside the वृत्ति stay exactly as printed. A printed footnote mark `१`/`*` inside the
Sanskrit text → write `[१]` / `[*]` at that spot.

## Completeness — do both before reporting
1. the `॥N॥` closings are consecutive and do not skip (merged groups aside): a गाथा wholly inside one page may never appear in a header — count the `॥N॥`;
2. every गाथा you open has both its गाथा text (part 1) and its **own** Sanskrit वृत्ति (part 6).
The first गाथा of your range may already be underway at the top of your first page (text printed on the previous page; वृत्ति continuing). Do **not** claim it — the previous
agent does. Claim a गाथा only if its **गाथा text** is printed on one of your pages. You finish every गाथा you opened even if that needs a page beyond your range.

## Accuracy guards
1. **Magnify before committing a doubtful conjunct** (450–500 dpi). `[अस्पष्ट]` for a letter you genuinely cannot read is correct; a plausible guess is not.
2. **Never normalise.** Keep printed forms: `ञ्च`/`श्च`, `व`/`ब`, anusvara, avagraha-less sandhi, odd spellings, editor's `( )` and `[ ]` (they are variant readings or emendations — keep them exactly).
   In this fount a ligature's lower stroke often vanishes: confusions seen in chapter 1 — `प्र`↔`म`, `त्व`↔`ल`, `ष`↔`प`, `न`↔`त`, `व`/`ब`, `द्व`/`ट`, a lost रेफ, `त्त`↔`च्च`,
   `ध`↔`घ`, `भ`↔`म`, and a **dropped letter inside a conjunct** (e.g. `…ग्रन्थीनां` for `…विवर्त्तग्रन्थीनां`). Recheck any word that does not construe; but the printed letters are the constraint —
   never delete or add a letter just to reach a word; if it still will not parse, transcribe as printed and flag it.
3. **Rejoin words broken across a line end** before reading them.
4. **Grep your own earlier segments** for a recurring formula before guessing (`इति सम्बन्धः`, `दर्शनाचारः`, `ज्ञानाचारः …`).
5. **A quoted verse has a received text** — if your reading differs from the normally transmitted text, doubt your reading first and say so.
6. **Never "improve" the Sanskrit.** Odd forms stay; mention them in the report.
7. Do **not** consult the Hindi to settle a Sanskrit reading — settle it on the page (zoom), by metre/sandhi/context, or by flagging it.

## Style
- English digits in your own prose (§ 370, गाथा 37, पृष्ठ 49); Devanagari digits only inside quoted text, where `॥३७॥` stays as printed.
- **Never write any sect name.** No bare आचार्य names in your own prose. **No working-process language** in `parts/` (no बैच / सत्र / file names / scan numbers / उपयोगकर्ता / other agents).

## Writing the file
**Write after your FIRST गाथा, then append** (Write first, then Edit). Output `parts/<batch file>.md`. Separate consecutive § with a blank line and `---`.

## Report back (under 250 words)
1. the § keys written and गाथा range covered; 2. exact first 6 and last 6 words of मूल with printed page numbers (seam checks); 3. segments written in total and any hard गाथा;
4. every `[अस्पष्ट]`, every doubtful reading (quote it, say why), every place the Sanskrit looked corrupt; 5. whether the boundary pages ran mid-गाथा; the scan page on which this
अधिकार ends (last गाथा number printed) if your range reached it.
