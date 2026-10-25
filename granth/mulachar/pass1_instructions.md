# Pass 1 — extraction spec (मूलाचार, प्रथम अधिकार : मूलगुणाधिकार)

*Working document. Nothing here goes into the book.*

You are transcribing part of **मूलाचार** by **श्री वट्टकेराचार्य** (प्राकृत गाथा) together with
**श्री वसुनन्दि-सिद्धान्तचक्रवर्ती's संस्कृत टीका, the आचारवृत्ति**, and the **Hindi translation by
गणिनी आर्यिका श्री ज्ञानमती माताजी** printed in the same volume. The finished book is a scholarly हिन्दी
व्याख्या for मुनि, आर्यिका and विद्वान् श्रावक.

**Your job in this pass is extraction, not composition.** You transcribe what is printed. A later pass
writes the संस्कृत छाया, अन्वय, अन्वयार्थ, the Hindi rendering of the Sanskrit आचारवृत्ति, and the व्याख्या.
**Do not write any of those.**

**The single most important thing you produce is the संस्कृत आचारवृत्ति**, transcribed completely and
exactly. The next pass translates it into Hindi and a third pass audits that translation against what you
wrote. If you drop a clause, the Hindi silently loses it and no later check can recover it, because nobody
re-reads the page. Transcribe every word.

Source: `mool/Mulachar_Purvardh_Aryika_Jnanmati.pdf`. Rendered pages are in `img/p0059.png … p0109.png`
(`p<scan page>`; **printed page = scan page − 57**). Open them with the Read tool. If a conjunct is
doubtful, re-render that region at 400–600 dpi:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Mulachar_Purvardh_Aryika_Jnanmati.pdf'); d[IDX].get_pixmap(dpi=500, clip=pymupdf.Rect(40,100,470,260)).save(r'<scratch>/z.png')"
```
`IDX = scan page − 1`; the page box is 504×666 pt.

## What a printed page carries

Running header `मूलगुणाधिकारः]` … `[ मूलाचारे`, printed page number in the corner. The page has two
streams separated by a **horizontal rule** — and the two are **not page-synchronised**:

**Above the rule — Sanskrit.**
1. an optional **पातनिका** in small Sanskrit type introducing the गाथा (`अथ … आह`, `तावदाह`, `अनन्तरं … प्रतिपादयति`);
2. the **प्राकृत गाथा** in large bold type, centred, two lines, closing `॥१॥`;
3. **श्री वसुनन्दि's आचारवृत्ति**, dense small type: it glosses the गाथा word by word —
   `मूलगुणेसु—मूलानि च तानि गुणाश्च …` — the गाथा's own प्राकृत words set in **bold** and followed by `—` and
   the Sanskrit gloss; then the construction (`इति सम्बन्धः`), objections and answers, quoted verses,
   कथंभूत-style questions, and often a closing summary sentence.

**Below the rule — Hindi (ज्ञानमती माताजी).** In this order, each marked by a bold run-in label:
- a Hindi पातनिका paragraph introducing the गाथा (it prints before the गाथा's `गाथार्थ`);
- **`गाथार्थ—`** the Hindi meaning of the गाथा, closing `॥१॥`;
- **`आचारवृत्ति—`** the Hindi rendering/explanation of Vasunandi's वृत्ति (long);
- then, where present: **`विशेष—` / `विशेषार्थ—` / `भावार्थ—` / `प्रश्न … उत्तर …` / `समाधान—`**, `शंका … समाधान`,
  tables, lists, quoted verses, and **numbered footnotes** at the foot of the page (`१. क "आचार"` — manuscript
  variants and source citations).

Page content routinely runs across a page break, and the Hindi stream usually lags the Sanskrit stream:
**follow each stream separately**, tracking its own `॥N॥`. Expect to read a page or two past the end of your
range to finish the Hindi of the last गाथा whose गाथा-text you transcribed.

## § numbering

One global sequence. **key = गाथा × 10** (+ star for an extra गाथा `N*2`). गाथा 1 → `§10`, गाथा 36 → `§360`.
Put the human reference in the § title as well: `(अधिकार 1, गाथा 5, मुद्रित पृष्ठ 5)`.

Where the edition explains **several गाथा under one वृत्ति and one Hindi block** (look for a combined
पातनिका `अथ … गाथाद्वयेन` and one `गाथार्थ`), write **one §** keyed to the first गाथा, carrying every गाथा
text, and say so in the title: `(अधिकार 1, गाथा 6–7, मुद्रित पृष्ठ 8)`. Merge **only** when they genuinely
share one वृत्ति and one Hindi block; if each has its own, write one § per गाथा.

## What to write, per गाथा

Reproduce these headings **verbatim** — a builder parses them.

```
§50 — <descriptive title in Hindi: what this गाथा establishes> (अधिकार 1, गाथा 5, मुद्रित पृष्ठ 7)

## 1. मूल पाठ (प्राकृत गाथा)
(पृष्ठ 7)
<the गाथा exactly as printed, line breaks as printed, ॥५॥ in Devanagari digits>

## 5. हिन्दी अनुवाद
<the printed Hindi stream for this गाथा, in the order printed: its Hindi पातनिका paragraph,
 then गाथार्थ—, आचारवृत्ति—, and every विशेष/भावार्थ/प्रश्न-उत्तर/शंका-समाधान block, verbatim, with the run-in labels
 kept as plain text (गाथार्थ—, आचारवृत्ति—). Tables stay as markdown tables. Quoted Sanskrit/Prakrit verses inside
 the Hindi stay as printed.>

## 6. श्री वसुनन्दि-कृत संस्कृत टीका — आचारवृत्ति (मूल)
(T1) <first segment, verbatim>
(T2) <second segment>
(T3) <…>

## 11. मुद्रित पाद-टिप्पणी
- <each printed footnote that belongs to this गाथा's text, verbatim, with its number and siglum>
```

If a गाथा has no printed footnote, omit the `## 11.` block. Nothing else: no parts 2, 3, 4, 7, 8, 9, 10.

**Never write `**भावार्थ:**` in bold with a colon** — the builder treats that exact form specially. Write a
printed `भावार्थ—` / `विशेषार्थ—` as plain text exactly as it prints.

### Hindi पातनिका goes with the गाथा it introduces
The Hindi paragraph that introduces a गाथा is printed at the end of the *previous* गाथा's block. It belongs to
the **incoming** गाथा: put it first in that गाथा's part 5. Likewise the Sanskrit पातनिका printed above a गाथा
is `(T1)` of that गाथा's part 6.

### How to segment the आचारवृत्ति
Tag each segment `(T1)`, `(T2)` … on its own line. A segment is normally:
- the Sanskrit पातनिका (`अथ …`);
- **a गाथा-pada word and its gloss** (`मूलगुणेसु—मूलानि च तानि गुणाश्च … विषयभूतेषु कारणभूतेषु वा सत्सु ।`) —
  one segment per प्राकृत word-group, as the gloss runs;
- **a question together with its answer** — never separate `प्रश्न/शङ्का` from `उत्तर/समाधान`, and never
  split a `कथंभूत`/`किमर्थम्` question from the words that answer it;
- a quoted verse together with its introduction (`तथा चोक्तम्` / `उक्तं च`) and the source it names;
- the closing summary / `इति सम्बन्धः` / `तात्पर्यम्` sentence.

Aim for 6–25 segments per गाथा (a long वृत्ति, such as the opening गाथा's, needs more). **Every word of the
printed Sanskrit must fall inside some segment** — the segments concatenated must reproduce it exactly, with
nothing added and nothing dropped. The प्राकृत words inside the वृत्ति (bold in print) are kept exactly as
printed; mark nothing, translate nothing.

Where the वृत्ति for one गाथा is continued across a page break, join it seamlessly. Where a footnote
number (`१`, `२`) is printed inside the Sanskrit text, transcribe it as `[१]` at that spot — no more.

## Completeness checks — do both before reporting

1. The `॥N॥` closings of the गाथा in your pages are numbered by the edition and **do not skip**. Your § must run
   consecutively (allowing for merged groups). A गाथा that sits wholly inside one page may never appear in
   any header — count the `॥N॥`.
2. Every गाथा you open must carry a part 6 with **its own Sanskrit वृत्ति** and a part 5 with **its own Hindi**.
   If the Sanskrit stream and Hindi stream of one गाथा finish on different pages, finish both.

The first गाथा of your range may already be underway at the top of your first page (its Prakrit text printed
on the previous page, its वृत्ति or Hindi continuing). Do **not** claim it; the previous agent does. Claim it
only if its **गाथा text** is printed on one of your pages. Conversely, you finish every गाथा you opened, even
if that needs pages past your range.

## The chapter marks its own divisions — keep them

The चरण-ending sentences — `इति मूलगुणाधिकारः`, `इत्याचारवृत्तौ … प्रथमः परिच्छेदः`, `एवं … समाप्तम्`, the
ग्रन्थकार's `अथ … प्रतिपादयति` openers, and the Hindi twins (`इस प्रकार से … प्रथम अधिकार पूर्ण हुआ`) — are the
text naming its own structure. Never drop one and never merge one into a neighbouring sentence: a closing one is
the last segment of the last गाथा it follows; an opening one is `(T1)` of the गाथा it introduces.

## Accuracy guards

1. **Magnify before committing a doubtful conjunct.** Never silently normalise a worn form; `[अस्पष्ट]` for a
   letter you genuinely cannot read is a correct answer, a plausible guess is not.
2. **The Hindi below the rule is your witness for the Sanskrit above it.** It glosses the वृत्ति's own words.
   When a Sanskrit glyph is doubtful, read the Hindi first; it settles most doubts at once.
3. **Rejoin words broken across a line end** (`…द्वेषाद्रा-` / `गाच्च…`) before reading them.
4. **Printed letters are the constraint.** Substitute a letter the fount is known to confuse, rejoin what the
   line-break split, or flag — never change the letter count to reach a word. Typical confusions in this
   type: `प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `भ`↔`म`, `व`↔`ब`, `ण`↔`न`, `ध`↔`घ`, रेफ lost or doubled. If a word
   sits where no Sanskrit word can, suspect the fount before the author.
5. **Grep your own earlier segments** and the other `parts/` files for a recurring idiom before guessing — the
   वृत्ति reuses a small stock of formulas (`मूलगुणेषु विषयभूतेषु कारणभूतेषु वा`, `इति सम्बन्धः`, `प्रमत्तसंयतादयः`).
6. **A quotation has a received text** — if your reading of a quoted verse differs from the text as normally
   transmitted, doubt your reading first, and say so in the report either way.
7. **Never "improve" the Sanskrit or the Hindi.** If a printed form is odd, print it as it stands and say so in
   the report. A form that recurs consistently is the edition's own.

## Style

- English digits in your own prose (§ 50, गाथा 5, पृष्ठ 7) — Devanagari digits **only** inside quoted
  मूल / वृत्ति / Hindi, where `॥५॥` stays exactly as printed.
- **Never write any sect name** (बीसपंथ / तेरापंथ or any sub-sect label) anywhere, for any reason.
- Jain आचार्य are never named bare in **your own prose** (titles and notes): `श्री वट्टकेराचार्य`,
  `श्री वसुनन्दि सिद्धान्तचक्रवर्ती`, `आचार्य श्री कुन्दकुन्द`. Printed text stays as printed.
- **No working-process language anywhere in `parts/`**: no "बैच", "इस सत्र", file names, scan-page numbers,
  "उपयोगकर्ता", no mention of other agents. Cross-refer only as "गाथा 5", "पूर्व-वर्णित गाथा".
- The § title is **yours**: a short Hindi sentence stating what the गाथा establishes. Make it accurate —
  titles are the first thing a reader meets and the weakest part of earlier books.

## Writing the file

**Write after your FIRST गाथा, then append.** A response is capped at 64,000 output tokens, and an agent that
batches ten pages and writes at the end can lose everything. Create `parts/<batch file>.md` with Write as soon
as the first § is done, then append each further § with Edit. Separate consecutive § with a blank line and `---`.

## Report back (under 250 words)

1. the § keys written and the गाथा range covered;
2. the exact first 6 and last 6 words of मूल you transcribed, with printed page numbers — for seam checks;
3. how many वृत्ति segments you wrote in total, and any गाथा whose वृत्ति you found hard to segment;
4. every `[अस्पष्ट]`; every place the printed Sanskrit looked corrupt or ungrammatical; every place the printed
   Hindi seemed to say something the वृत्ति does not — flag it, do not fix it;
5. whether the boundary pages ran mid-गाथा, and any page carrying no new गाथा.
