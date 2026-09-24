# Pass 1 — extraction spec (नयचक्र)

*Working document. Nothing here goes into the book.*

You are transcribing part of the Jain Prakrit ग्रन्थ **णयचक्को [नयचक्र]** (द्रव्यस्वभावप्रकाशक) by
**श्री माइल्लधवल**, edited and translated by सिद्धान्ताचार्य पं. कैलाशचन्द्र शास्त्री (भारतीय ज्ञानपीठ,
मूर्तिदेवी जैन ग्रन्थमाला, प्राकृत ग्रन्थांक 12, तृतीय संस्करण 2001). The finished book is a scholarly
हिन्दी व्याख्या for मुनि and विद्वान् श्रावक.

**Your job in this pass is extraction, not composition.** You write two of the book's nine parts — the
मूल पाठ and the printed हिन्दी — and the page's footnotes into a sidecar file. A later pass adds the
संस्कृत छाया, अन्वय, अन्वयार्थ, व्याख्या, उदाहरण, तालिका and सन्दर्भ. **Do not write those.** Fidelity to
the printed page is the entire value of what you produce.

## Page layout

One PNG = one printed page, single column. Order on a page:

1. **running header** — one side a gatha-range marker like `[ गा० ४०१–` or `–४२५ ]`; centre `नयचक्र` or
   `द्रव्यस्वभावप्रकाशक`; other side the **printed page number in Devanagari**. Record the printed number.
2. **a block of Prakrit गाथाएँ** at the top. Each is normally preceded by a short **Sanskrit उत्थानिका /
   अवतरण sentence** (e.g. `अथ पर्यायस्य लक्षणं भेदं च दर्शयति—`) and ends `॥17॥`. **Several gathas may
   stand together in this block before any Hindi appears.** Small superscript digits inside a gatha point
   to the page-bottom footnotes.
3. a horizontal rule.
4. the **Hindi part**: for each gatha — matched to it **by its ॥number॥, never by position** — an अनुवाद
   paragraph, then one or more `विशेषार्थ—` paragraphs, sometimes `शंका—` / `समाधान—` pairs, sometimes
   `कहा भी है—` followed by a quoted verse.
5. **footnotes** at the page bottom in small type, `१. … २. …` — मुद्रित पाठान्तर from the manuscripts
   (अ०, क०, ख०, मु०, ज०, प्रतौ) and source citations (पञ्चास्ति०, सर्वार्थसि०, आ० प० प्र०, जयसेन टीका …).
6. `इति <name>अधिकारः ।` marks the end of an अधिकार.

**Position on the page proves nothing; the `॥number॥` proves everything.** From about printed page 162 on
this gets severe: the edition prints a new अधिकार's मूल-block up front and lets the previous गाथा's हिन्दी
trail *below* it, so गाथा 326's विशेषार्थ sits underneath गाथा 327–328's मूल, and गाथा 328's underneath
गाथा 329–330's. A whole page can also carry no मूल at all, being pure continuation of an earlier
विशेषार्थ. Match every अनुवाद and विशेषार्थ to its गाथा by the verse number alone.

**Ignore completely:** (a) the library stamp `मार्गदर्शक :– आचार्य श्री सुविधिसागर जी महाराज` printed
diagonally across the middle of many pages; (b) the faint bleed-through of the reverse side's text.

## § numbering — this is how parallel agents avoid collisions

A **unit (§) = one गाथा, or the group of गाथाएँ the book explains together** (the printed translation ends
`॥16-17॥`, or one अनुवाद paragraph plainly covers two consecutive gathas).

**The § number is the number of the FIRST गाथा of the unit.** A unit covering गाथा 16 and 17 is `§16`, and
there is no `§17`. Gaps are intended and are explained in the front matter. Never renumber, never invent a
§ number, never write `§?`. Put the full group in the title: `(गाथा 16–17, मुद्रित पृष्ठ 9)`.

## The गाथा index is your second witness — use it

The book's own **परिशिष्ट 4, "नयचक्रगत गाथानुक्रमणी"**, is rendered for you at
`img\p0310.png` … `img\p0315.png`. It lists **every गाथा's opening words with its number**, alphabetically
by first letter, in a different typesetting from the body. That makes it an independent witness to the
first two or three words of each गाथा you transcribe.

**Whenever the opening words of a गाथा contain any glyph you are unsure of, look it up there.** Find the
आद्याक्षर section (`[ज]`, `[ण]`, `[द]` …) and the entry ending in your गाथा's number.

This has already settled one systematic error. Five गाथा openings had been transcribed `जह्रा` / `तह्रा`;
the index prints `जम्हा णएण विणा १७४` and `जम्हा एक्कसहावं ३७`, so the conjunct is **म्ह**, which this
typeface sets in a way that reads as ह-plus-subscript at body size. The index likewise confirms
`तिक्काले जं सत्तं ३६` (doubled क) and `कम्मक्खयदो सुद्धो ६५` (द्ध, not ढ्ढ).

It also verifies **गाथा numbers**, which matters more than it sounds: the § numbering of this whole book is
the गाथा numbering, so one misread number corrupts the structure silently. A printed number faded to look
like `११२` was confirmed from the index as `३१२`. Whenever a printed गाथा number is faint, damaged or
surprising, look it up.

Two limits: the index covers only the **opening** words, and the printed index has its own occasional
typos (`मिच्छत्तं` there against a clear `मिच्छेत्तं` in the body; a compressed `असुहसुहं` against `असुहं सुहं`).
Where index and body genuinely disagree on a *word*, transcribe the body as printed and report the
disagreement — do not silently follow either one.

## Your range's LAST page is yours — the most common way this pass goes wrong

**Every गाथा whose मूल appears anywhere on your last page belongs to you**, even when its हिन्दी अनुवाद and
विशेषार्थ run on to the following page. In that case read the following page and finish the unit there; you
are not "reading into the next agent's range", you are completing your own § — the next agent starts at the
first unit whose **मूल** begins on its own first page and will not pick yours up.

This has already cost this book two gaps. On one wave the agent owning pages up to p0049 stopped at गाथा 13
although p0049 printed गाथा १४ and १५, and the agent owning pages up to p0057 stopped at गाथा 29 although
p0057 printed गाथा ३० and ३१ — each assumed the other side of the seam would take them, and neither did.

So, before you write your report: list the गाथा numbers printed on your **last** page and confirm every one
of them has a § in your file. If one does not, you are not finished.

## What to write, per §

Reproduce these headings **verbatim** — a builder parses them.

```
§16 — <descriptive title: what this gatha establishes in the ग्रन्थ's scheme> (गाथा 16–17, मुद्रित पृष्ठ 9)

## 1. मूल पाठ (प्राकृत गाथा)
(पृष्ठ 9)
<the Sanskrit उत्थानिका sentence exactly as printed, if there is one, on its own line>
<the Prakrit gatha exactly as printed — line breaks as printed, sandhi as printed, ॥१६॥ in Devanagari digits>

## 5. हिन्दी अनुवाद
<the printed Hindi अनुवाद of this gatha. You are reproducing the editor's translation in clean शास्त्रीय
हिन्दी — not re-translating freely and not expanding it. Implied words in (…).>

**विशेषार्थ:** <the page's विशेषार्थ for this gatha, its substance, as one or more paragraphs>
**शंका:** … / **समाधान:** …   <only where the page has them, in the page's own order>
<a `कहा भी है—` quoted verse: give the verse as printed, then its meaning in one line>
```

Nothing else. No part 2, 3, 4, 6, 7, 8 or 9 in this file.

## The sidecar footnote file

For each § that has page-bottom footnotes, append to `footnotes/<your batch file name>`:

```
§16 (पृष्ठ 9)
१. सामान्यगुणेषु विशेषगुणेषु च पाठात् पौलहत्त्यम् ।
२. 'अन्तस्यादचत्वारो गुणाः स्वजात्यपेक्षया सामान्यगुणाः, विजात्यपेक्षया त एव विशेषगुणाः । आलाप० ।
```

Verbatim, in the printed order, with the printed numbers. This file is a working input for the next pass
and is never built into the book, so transcribe it plainly — no commentary.

## Accuracy guards — these are the two ways this pass is known to go wrong

0. **The confirmed confusion pairs on this book.** Every one of these has already produced a wrong reading
   here, and none is reliably distinguishable at normal zoom in this typeface. Magnify before committing any
   of them: **द्ध / ढ्ढ** (the page says `सुद्धणया`, `लद्धा`; `सुढ`/`लढ्ढा` are not words — but `वुड्ढ`,
   `वड्ढी`, `पुढवी` genuinely do have ढ), **च / व** (`चेदण` misread as `वेदण`), **ण / प**, **ध / घ**,
   **भ / म**, **ख / रव**, **द्द / ट्ठ**, and single vs doubled conjuncts (`तिकाले` vs `तिक्काले`).
   When a quoted verse comes from a text with a known received reading (पञ्चास्तिकाय, द्रव्यसंग्रह,
   नियमसार, त्रिलोकसार, गोम्मटसार, आप्तमीमांसा), a disagreement with that reading is a signal to magnify
   again — never licence to emend. Report the disagreement either way.

1. **Magnify every प्रति-संकेत before writing it.** The sigla `अ० क० ख० मु० ज० प्रतौ` are set in small worn
   type and `व`/`द`, `ख`/`रव`, `घ`/`ध` are routinely confused at normal zoom. On another text an agent
   wrote 15 `द` against 1 `व` and every one that was checked was wrong. Crop and re-render the footnote
   band before you transcribe it:
   ```
   python -c "import pymupdf; d=pymupdf.open(r'mool/Nayachakko [Naya Chakra] [Shree Maailladhaval].pdf'); d[IDX].get_pixmap(dpi=600, clip=pymupdf.Rect(60,640,560,780)).save(r'C:\Users\naman\AppData\Local\Temp\claude\fn.png')"
   ```
   `IDX = scan page − 1`; page box is 612×792 pt, so the footnote band is roughly y 640–780 and a gatha
   block roughly y 120–320. Then Read the PNG. Do the same for any doubtful conjunct or proper name.
2. **Rejoin words broken across a page break.** A word hyphenated at the foot of one page and continued at
   the head of the next is written whole, once, in the § it belongs to — never as two fragments.

3. **Mark editorial restitution with square brackets — never present a reconstruction as a reading.**
   A diagonal library stamp buries whole गाथा lines on some pages. Where you can work out the covered words
   from the book's own हिन्दी अनुवाद of that same गाथा, you may supply them — but you must put them in
   `[ ]` and add a `**पाठ-सूचना:**` line at the end of part 5 saying exactly which words were legible, that
   the bracketed text is सम्पादकीय पूर्ति from the printed Hindi, and that the reader should check the
   original. This happened at गाथा 91 and the reconstruction was right but was written as if read; the
   bracket and the note are what make it honest. Never supply covered words from a *different* text — a
   footnote quoting नियमसार or गोम्मटसार is not evidence for what this page printed; there, `[अस्पष्ट]`.

Beyond these: `[अस्पष्ट]` for a letter you genuinely cannot read is a **correct** answer and a plausible
guess is not. Never silently normalise a worn Prakrit form toward the Sanskrit you expect — if the page
shows `होह` write `होह` and flag it in your report; correcting print is the next pass's business, not yours.
`लगभग` / `सम्भवतः` for an uncertain number. Never invent a reading, a citation or a verse number.

## Style

- शास्त्रीय, clear हिन्दी. English digits in your own prose (§ 16, गाथा 17, पृष्ठ 9) — Devanagari digits
  **only** inside quoted मूल / संस्कृत / प्राकृत text, where `॥१७॥` stays exactly as printed.
- **Never write any sect name** (बीसपंथ / तेरापंथ or any sub-sect label) anywhere, for any reason.
- Jain आचार्य are never named bare: `श्री देवसेन स्वामी`, `आचार्य श्री कुन्दकुन्द`, `श्री अमृतचन्द्र स्वामी`,
  `श्री माइल्लधवल`, `श्री समन्तभद्र स्वामी`, `श्री पूज्यपाद स्वामी`. The मूल पाठ and the printed footnotes
  stay exactly as printed. Non-Jain opponents — कुमारिल, धर्मकीर्ति, उदयन, नैयायिक, बौद्ध — are plain.
- **No working-process language anywhere in `parts/`**: no "बैच", "इस सत्र", "अगले भाग में", file names,
  scan-page numbers, "उपयोगकर्ता", no mention of other agents. Cross-refer only as "§ 12",
  "पूर्व-वर्णित गाथा", "आगामी गाथाओं में". (The sidecar footnote file is exempt — it is not book text.)
- Every line of मूल in your range must appear in some § part 1. Do not summarise, skip a gatha, or merge
  two units the book keeps apart.

## Writing the file

**Write after your FIRST §, then append.** A response is capped at 64,000 output tokens, and a wave of
agents that batched up eight pages and wrote at the end was interrupted and left nothing on disk. So:
create the file with Write as soon as the first § is done, then append each further § with Edit
(`old_string` = the file's current last line, `new_string` = that line + the new § block). Separate
consecutive § with a blank line and `---`. Update the sidecar footnote file on the same rhythm.

## Report back (under 250 words)

1. the § numbers written and the गाथा range they cover;
2. the exact first 6 words of मूल you started with and the exact last 6 words you ended with, each with its
   printed page number — these are used to check the seams between agents;
3. every `इति …अधिकारः ।` line you saw, with its printed page — these become the book's खण्ड headers;
4. every `[अस्पष्ट]` spot; every place you suspect a misprint; every Prakrit form that looked wrong but
   that you transcribed as printed anyway;
5. how many footnote bands you magnified, and whether the boundary pages ended mid-unit.
