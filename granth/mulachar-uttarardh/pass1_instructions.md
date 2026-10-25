# Pass 1 — extraction spec (मूलाचार, उत्तरार्ध : अधिकार 8–12)

*Working document. Nothing here goes into the book.*

You are transcribing part of **मूलाचार** by **श्री वट्टकेराचार्य** (प्राकृत गाथा) together with **श्री वसुनन्दि-सिद्धान्तचक्रवर्ती's
संस्कृत आचारवृत्ति**. The finished book is an **independent** Hindi व्याख्या: it must contain no existing Hindi translation and no translator's
name (including आर्यिकारत्न ज्ञानमती जी, who edited and translated the printed source edition — her name and her Hindi translation must never
appear anywhere in what you write). **Therefore in this pass you transcribe ONLY the प्राकृत गाथा, the संस्कृत आचारवृत्ति, and the manuscript-variant
footnotes. You never transcribe, summarise or paraphrase the printed Hindi.** (Every scan page carries Hindi below a horizontal rule — you will see
it; ignore it completely, do not copy any of it, and do not let it shape what you write, including the § title.)

**The single most important thing you produce is the संस्कृत आचारवृत्ति, transcribed completely and exactly.** A later pass translates it into Hindi
and a third pass audits that translation against what you wrote; if you drop or alter a word nothing can recover it. Earlier chapters of this book
were found to contain misreadings of this kind once an auditor compared the scan — read every doubtful conjunct at high zoom.

Source: `mool/Mulachar_Uttarardh_Aryika_Jnanmati.pdf`; rendered pages `img/p0035.png … p0454.png` (`p<scan page>`; **printed page = scan page − 34**).
Zoom a doubtful region:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Mulachar_Uttarardh_Aryika_Jnanmati.pdf'); d[IDX].get_pixmap(dpi=500, clip=pymupdf.Rect(40,100,470,260)).save(r'<scratch>/z.png')"
```
`IDX = scan page − 1`; page box 504×666 pt.

## The five अधिकार in this volume (गाथा 683–1249, 567 गाथा total)

This is the **उत्तरार्ध** (latter half) of मूलाचार — the whole ग्रन्थ ends at the close of अधिकार 12. Note: पूर्वार्ध (already covered by
`mulachar`/`mulachar-2`…`mulachar-5`) actually runs अधिकार **1–7**, not 1–5 — अधिकार 6 (पिण्डशुद्धि) and 7 (षडावश्यक) are not in this PDF and are a
separate, not-yet-done gap; do not confuse them with the five अधिकार below.

| अधिकार | नाम | गाथा range | opens (scan/printed) | closes (scan/printed) | closing कोलोफ़न (exact, for recognising the boundary) |
|---|---|---|---|---|---|
| 8 | द्वादशानुप्रेक्षाधिकार | 683–768 | 35 / 1 | 72 / 38 | `इति श्रीमद्वट्टकेराचार्यवर्यविनिर्मितमूलाचारे वसुनन्द्याचार्यप्रणीतटीकासहिते द्वादशानुप्रेक्षकनामाऽष्टमः परिच्छेदः समाप्तः।` |
| 9 | अनगारभावनाधिकार | 769–893 | 73 / 39 | 140 / 106 | `इति श्रीमद्वट्टकेराचार्यवर्यप्रणीते मूलाचारे वसुनन्द्याचार्य-प्रणीताचार-वृत्त्याख्यटीकासहिते नवमः परिच्छेदः॥` |
| 10 | समयसाराधिकार | 894–1017 | 141 / 107 | 208 / 174 | `इति श्रीमद्वट्टकेराचार्यवर्यप्रणीते मूलाचारे श्रीवसुनन्द्याचार्यप्रणीताचारवृत्त्याख्यटीका-सहिते दशमः समयसाराधिकारः॥` |
| 11 | शीलगुणाधिकार | 1018–1043 | 209 / 175 | 237 / 203 | `इति श्रीमद्वट्टकेर्याचार्यवर्यप्रणीतमूलाचारे वसुनन्द्याचार्यप्रणीताचारवृत्त्याख्यटीकासहिते शीलगुणव्याख्याननामैकादशोऽधिकारः॥` |
| 12 | पर्याप्त्यधिकार | 1044–1249 | 238 / 204 | 425 / 391 | `इति श्रीमदाचार्यवर्यवट्टकेरिप्रणीतमूलाचारे श्रीवसुनन्दिप्रणीत-टीकासहिते द्वादशोऽधिकारः॥१२॥` — immediately followed by a स्रग्धरा verse and the colophन for the WHOLE ग्रन्थ (both भाग). Scan 426 onward is endmatter (परिशिष्ट) — **not** गाथा text; stop at गाथा 1249. |

A footnote in this edition notes that in the फलटन-published edition द्वादशानुप्रेक्षा/अनगारभावना are numbered 9th/8th (swapped) and शीलगुण/पर्याप्ति are
12th/11th (swapped), with 2–3 extra गाथा at some chapter ends. **Ignore that edition entirely — number and transcribe strictly from what is printed
on these scans.**

## What you transcribe from each page

**Above the horizontal rule only:**
1. an optional **Sanskrit पातनिका** in small type introducing a गाथा (`अथ … आह`, `तावदाह`, `अनन्तरं … प्रतिपादयति`);
2. the **प्राकृत गाथा** in large bold type, centred, two lines, closing `॥N॥` (N = the global गाथा number, 683 through 1249);
3. **श्री वसुनन्दि's आचारवृत्ति**, dense small type — it glosses the गाथा word by word (the गाथा's own प्राकृत words set in bold and followed by `—`
   and the Sanskrit gloss), then the construction (`इति सम्बन्धः`), objections and answers, quoted verses, closing summary.

**Not the Hindi stream below the rule** (हिन्दी पातनिका, `गाथार्थ—`, `आचारवृत्ति—`, `विशेष—`/`भावार्थ—`, शंका-समाधान, tables).

**Footnotes at the foot of the page** (numbered `१. क "…"`): transcribe only the **manuscript variants, Sanskrit/Prakrit readings and source citations**
(`क "आचार"`, `२. अस्य स्थाने … पाठः`, `* धवला पु. प्र. पृ. २५१`, a quoted गाथा in Prakrit). **Skip any footnote that is a Hindi explanation** (a sentence of Hindi
describing meaning or story, `अर्थ—`, `भावार्थ—`). If a footnote quotes an extra Prakrit/Sanskrit गाथा, keep the गाथा text (not its Hindi meaning).

Page content runs across page breaks; the Sanskrit stream and the Hindi stream are not page-synchronised — **follow only the Sanskrit stream** and its `॥N॥`
closings. Expect to read a page past your range to finish a गाथा whose वृत्ति you opened.

## Citation verses are not new गाथा
The आचारवृत्ति sometimes quotes an earlier verse as supporting evidence (introduced by `यस्मात्`, `यथोक्तम्`, `तथा चोक्तम्` and similar), closing with its own old `॥N॥`. **This is not a new sequential गाथा** — it belongs inside a `(Tn)` segment of whichever गाथा's वृत्ति is still open, not its own §. Only start a new § when you have confirmed the verse's number is genuinely the next one in sequence (exactly one more than the previous गाथा you wrote) — a verse-shaped block ending in `॥N॥` is not by itself enough evidence. When in doubt, re-zoom the digit and cross-check it against another confirmed digit on the same page (the printed page-number header is a reliable reference) rather than assuming.

## § numbering — key = गाथा × 10

`§6830` = गाथा 683, `§12490` = गाथा 1249. Where the वृत्ति explains **several गाथा together under one combined पातनिका and one वृत्ति block**
(not separate वृत्ति for each), write one § keyed to the first गाथा and give the title `(अधिकार 8, गाथा 700–701, मुद्रित पृष्ठ 23)` (use the actual
अधिकार number for wherever your range falls — see the table above). Merge only when they truly share one वृत्ति; if each has its own, one § per गाथा.

## What to write, per गाथा

Reproduce these headings **verbatim** — a builder parses them.

```
§6830 — गाथा 683 (अधिकार 8, गाथा 683, मुद्रित पृष्ठ 1)

## 1. मूल पाठ (प्राकृत गाथा)
(पृष्ठ 1)
<the गाथा exactly as printed, two lines, ॥६८३॥ in Devanagari digits>

## 6. श्री वसुनन्दि-कृत संस्कृत टीका — आचारवृत्ति (मूल)
(T1) <first segment, verbatim>
(T2) <second segment>

## 11. मुद्रित पाद-टिप्पणी
- (पृष्ठ 1) १. क "…"
```
- **The § title is just `गाथा N`** (plus the parenthesis) — **do not write a descriptive title**; the later pass writes it from the Sanskrit alone, so no Hindi can leak
  through the title. The parenthesis form `(अधिकार <अ.संख्या>, गाथा N, मुद्रित पृष्ठ P)` is exact — the contents page is built from it.
- Part 6's heading must contain `टीका` (the builder keys on it). Nothing else: no parts 2, 3, 4, 5, 7–10. Omit `## 11.` when the गाथा has no variant footnote.
- **Never write a bold `**…**` anywhere.**
- Where an opening or closing sentence names a division (an `इति … अधिकारः` colophन, an `अथ … अधिकारः`/`कथ्यते` opening — see the table above for the
  exact wording of each of the five), keep it: a closing one is the last segment of the last गाथा it follows; an opening one is `(T1)` of the गाथा it
  introduces. **If your batch's range crosses one of these five boundaries, write both sides correctly — the closing colophन belongs to the previous
  अधिकार's last गाथा, the opening line belongs to the next अधिकार's first गाथा — and use the correct अधिकार number in the parenthesis on each side.**

### Segmenting the आचारवृत्ति
Tag `(T1)`, `(T2)` … each on its own line. A segment is: the पातनिका; **a गाथा-pada word with its gloss**, one segment per प्राकृत word-group as the
gloss runs; **a question together with its answer** (never split शङ्का from समाधान, nor a `कथंभूत`/`किमर्थम्` question from its answer); a quoted verse
with its introduction and named source; the closing summary / `इति सम्बन्धः`. Aim for 6–25 segments per गाथा. **Every printed Sanskrit word must fall
inside some segment; concatenated, the segments reproduce the text exactly.** The प्राकृत words inside the वृत्ति stay exactly as printed. A printed
footnote mark `१`/`*` inside the Sanskrit text → write `[१]` / `[*]` at that spot.

## Completeness — do both before reporting
1. the `॥N॥` closings are consecutive and do not skip (merged groups aside): a गाथा wholly inside one page may never appear in a header — count the `॥N॥`;
2. every गाथा you open has both its गाथा text (part 1) and its **own** Sanskrit वृत्ति (part 6).
The first गाथा of your range may already be underway at the top of your first page (text printed on the previous page; वृत्ति continuing). Do **not** claim it — the previous
agent does. Claim a गाथा only if its **गाथा text** is printed on one of your pages. You finish every गाथा you opened even if that needs a page beyond your range.

## Accuracy guards
1. **Magnify before committing a doubtful conjunct** (450–500 dpi). `[अस्पष्ट]` for a letter you genuinely cannot read is correct; a plausible guess is not.
2. **Never normalise.** Keep printed forms: `ञ्च`/`श्च`, `व`/`ब`, anusvara, avagraha-less sandhi, odd spellings, editor's `( )` and `[ ]` (they are variant readings or emendations — keep them exactly).
   In this fount a ligature's lower stroke often vanishes: known confusions — `प्र`↔`म`, `त्व`↔`ल`, `ष`↔`प`, `न`↔`त`, `व`/`ब`, `द्व`/`ट`, a lost रेफ, `त्त`↔`च्च`,
   `ध`↔`घ`, `भ`↔`म`, and a **dropped letter inside a conjunct**. Recheck any word that does not construe; but the printed letters are the constraint —
   never delete or add a letter just to reach a word; if it still will not parse, transcribe as printed and flag it.
3. **Rejoin words broken across a line end** before reading them.
4. **Grep your own earlier segments** for a recurring formula before guessing (`इति सम्बन्धः`, `दर्शनाचारः`, `ज्ञानाचारः …`).
5. **A quoted verse has a received text** — if your reading differs from the normally transmitted text, doubt your reading first and say so.
6. **Never "improve" the Sanskrit.** Odd forms stay; mention them in the report.
7. Do **not** consult the Hindi to settle a Sanskrit reading — settle it on the page (zoom), by metre/sandhi/context, or by flagging it.

## Style
- English digits in your own prose (§ 6830, गाथा 683, पृष्ठ 1); Devanagari digits only inside quoted text, where `॥६८३॥` stays as printed.
- **Never write any sect name.** No bare आचार्य names in your own prose. **No working-process language** in `parts/` (no बैच / सत्र / file names / scan numbers / उपयोगकर्ता / other agents).

## Writing the file
**Write after your FIRST गाथा, then append** (Write first, then Edit). Output `parts/<batch file>.md`. Separate consecutive § with a blank line and `---`.

## Report back (under 250 words)
1. the § keys written and गाथा range covered; 2. exact first 6 and last 6 words of मूल with printed page numbers (seam checks); 3. segments written in total and any hard गाथा;
4. every `[अस्पष्ट]`, every doubtful reading (quote it, say why), every place the Sanskrit looked corrupt; 5. whether the boundary pages ran mid-गाथा; whether your range crossed
an अधिकार boundary (say which, and confirm both sides are written correctly per the table above).
