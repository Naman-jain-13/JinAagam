# Pass 1 — extraction spec (परमात्मप्रकाश एवं योगसार)

*Working document. Nothing here goes into the book.*

You are transcribing part of **परमात्मप्रकाश** by **श्री योगीन्दुदेव** (अपभ्रंश दोहा) together with
**श्री ब्रह्मदेव's संस्कृत टीका**, from Dr. A. N. Upadhye's edition (परमश्रुत प्रभावक मण्डल / श्रीमद्
राजचन्द्र जैन शास्त्रमाला). The finished book is a scholarly हिन्दी व्याख्या for मुनि and विद्वान् श्रावक.

**Your job in this pass is extraction, not composition.** You transcribe what is printed. A later pass
writes the अन्वय, the अन्वयार्थ, the Hindi rendering of the Sanskrit टीका, and the व्याख्या. **Do not write
any of those.**

**The single most important thing you produce is the संस्कृत टीका**, transcribed completely and exactly.
The next pass translates it into Hindi and a third pass audits that translation against what you wrote.
If you drop a clause, the Hindi silently loses it and no later check can recover it, because nobody
re-reads the page. Transcribe every word.

## What a printed page carries

Above a horizontal rule:

1. the **अपभ्रंश दोहा** in bold type, ending `॥ ३९ ॥`;
2. its **संस्कृत छाया** — two lines in smaller type, *already printed in this edition*. You transcribe it.
   Never compose one;
3. **श्री ब्रह्मदेव's संस्कृत टीका**. The दोहा's own अपभ्रंश words are set in **bold** inside it and are
   glossed in Sanskrit immediately after. It runs in the **कथंभूत catechetical style**: a statement,
   then a one-word question — `किं कृत्वा ।` `कथंभूतः ।` `कस्मात् ।` `कः ।` `कान् ।` `किं करोति ।` — and
   its answer. Those questions are the skeleton of the commentary's argument; transcribe each one and
   keep the `।` dandas exactly where they are printed, because they mark where each answer ends.

Below the rule:

4. the **हिन्दी अनुवाद**, which prints the Sanskrit lemma in **square brackets** before each rendering:
   `[पुराकृतं कर्म] पूर्व उपार्जित कर्मोंको [क्षपयति] क्षय करता है`. Keep the brackets — they are the
   edition's own Sanskrit↔Hindi alignment and the next two passes depend on them;
5. **भावार्थ**, introduced by `भावार्थ–`.

Running header: `–दोहा १९० ]  परमात्मप्रकाशः  २९५` or `योगीन्दुदेवविरचितः  [ अ० २, दोहा ३९–`. Record the
printed page number. A दोहा's material often runs across a page break — follow it.

## § numbering — three independent sequences, one key

This ग्रन्थ numbers its दोहा from 1 three separate times: परमात्मप्रकाश अधिकार 1, अधिकार 2, and योगसार.
A bare दोहा number would therefore collide. Compute the § key arithmetically:

```
key = base + दोहा × 10 + star

base : 10000  परमात्मप्रकाश, अधिकार 1
       20000  परमात्मप्रकाश, अधिकार 2
       30000  योगसार
star : 0 normally. For an extra दोहा printed "123*2", star = 2.
```

So अधिकार 1 दोहा 17 → `§10170`; अधिकार 2 दोहा 39 → `§20390`; योगसार दोहा 29 → `§30290`;
अधिकार 1 दोहा 123*2 → `§11232`.

The reader never sees the key — the builder prints `परमात्मप्रकाश 2.39` or `योगसार, दोहा 29`. But **put the
human reference in your § title too**, so the seam checks can read it: `(अधिकार 2, दोहा 39, मुद्रित पृष्ठ 160)`.

The running header tells you which अधिकार you are in (`[ अ० २, दोहा ३९–`). Check it on every page; the
अधिकार changes mid-volume and getting it wrong puts a whole batch in the wrong half of the book.

## What to write, per दोहा

Reproduce these headings **verbatim** — a builder parses them.

```
§20390 — <descriptive title: what this दोहा establishes> (अधिकार 2, दोहा 39, मुद्रित पृष्ठ 160)

## 1. मूल पाठ (अपभ्रंश दोहा)
(पृष्ठ 160)
<the दोहा exactly as printed, line breaks as printed, ॥ ३९ ॥ in Devanagari digits>

## 2. संस्कृत छाया (मुद्रित)
<the two छाया lines exactly as printed>

## 5. हिन्दी अनुवाद
<the printed हिन्दी अनुवाद, with its [square-bracketed] Sanskrit lemmas kept exactly where they stand>

**भावार्थ:** <the printed भावार्थ, if there is one>

## 6. श्री ब्रह्मदेव-कृत संस्कृत टीका (मूल)
(T1) <first segment of the टीका, verbatim>
(T2) <second segment>
(T3) <…>
```

Nothing else. No part 3, 4, 7, 8, 9 or 10 in this file.

### How to segment the टीका

Break it at its own joints, and tag each segment `(T1)`, `(T2)`, … on its own line. A segment is normally:

- the opening `<pratīka> इत्यादि ।` formula;
- a statement together with the अपभ्रंश words it glosses;
- **a कथंभूत question together with its answer** — `पुनरपि किं करोति । अहिणव पेसु ण देइ अभिनवं कर्म
  प्रवेशं न ददाति ।` is **one** segment, never two. Splitting a question from its answer is the single
  most damaging thing you can do here, because the next pass translates segment by segment and would
  then have a question with nothing to answer it;
- a quoted verse (`तथा चोक्तम् — "…"`) together with its introduction.

Aim for 4–12 segments per दोहा. Where the टीका is a single long sentence, one segment is right. **Every
word of the printed टीका must fall inside some segment** — the segments concatenated must reproduce it
exactly, with nothing added and nothing dropped.

## The running header is your checklist — use it

Every page carries a header like `–दोहा १२ ]  परमात्मप्रकाशः  १९` or `योगीन्दुदेवविरचितः  [ अ० २, दोहा ३९–`.
The number in it is the दोहा the page runs **to** (bracket on the right) or **from** (bracket on the left),
and the `अ० १ / अ० २` tells you the अधिकार.

**Before writing your report, list the दोहा numbers that appear in the headers of your pages, and confirm
every one of them has a § in your file.** This is not optional bookkeeping — it is the check that catches
the one failure this project has already had: दोहा 12 sits wholly on printed page 19, whose header says
`–दोहा १२ ]`, and it was dropped because one agent thought its मूल began on the previous page and the
agent who owned page 19 thought the same. Both reports read as internally consistent. The header would
have caught it in a second.

**But the header is not sufficient on its own, so do this as well.** A दोहा whose मूल, टीका and हिन्दी all
open and close inside a single page may **never appear in any running header** — the header names whatever
दोहा the page runs to. दोहा 16 of अधिकार 2 is exactly this: it sits entirely within the page whose header
says दोहा 17, and the header checklist would have passed with it missing.

So check **two** things before reporting:

1. every दोहा named in your pages' headers has a §; **and**
2. the दोहा numbers of the § you wrote run **consecutively** — if you wrote दोहा 14, 15, 17, the 16 you
   never saw is sitting inside one of your pages. Go back and find it.

The second check is the one that catches a swallowed दोहा. Count the `॥ N ॥` closings in the मूल stream as
you go: they are numbered by the edition and they do not skip.

## दोहा the edition explains together

The edition sometimes gives **one टीका and one हिन्दी for several दोहा** — दोहा 19–21 are printed as a
सूत्रत्रय, marked `त्रिकलम्` / `तिघलं` after the third verse's छाया. Where that happens, write **one §**,
keyed to the **first** दोहा of the group, carrying all the मूल+छाया pairs and the single shared टीका and
हिन्दी. Say so in the § title: `(अधिकार 1, दोहा 19–21, मुद्रित पृष्ठ 24)`. Do not invent separate § for
the others and do not repeat the commentary three times. The keys for the covered दोहा simply go unused —
gaps in the key sequence are expected and correct.

**But the marker alone is not the test — one shared commentary is.** From दोहा 44 onward the edition also
prints `त्रिकलं` / `चतुःकलं` पातनिका that merely *announce a themed group of verses*, after which **each दोहा
still carries its own मूल, छाया, टीका and हिन्दी**. Those are not merged दोहा and must stay as separate §;
merging them would throw away three-quarters of the commentary.

So decide by what follows, not by the label: **merge only when the दोहा share a single टीका and a single
हिन्दी block between them.** If each verse has its own commentary, write one § per verse however the group
is announced, and mention the group in the § titles instead.

## The टीका and the हिन्दी are two independent streams

Each page has a horizontal rule across it. **Above it runs the संस्कृत टीका; below it runs the हिन्दी
अनुवाद — and the two are not page-synchronised.** A page's टीका portion and its हिन्दी portion routinely
belong to different दोहा: on printed page 57 the टीका above the rule finishes दोहा 57 and begins दोहा 58,
while the हिन्दी below that same rule is still finishing दोहा 57.

So **never derive a दोहा's boundaries from page position.** Follow each stream separately, tracking its own
`॥ ५७ ॥` closings, and assemble the § from the two streams independently. Expect to read a page or two
past the end of your range to finish a दोहा's हिन्दी after its टीका has already closed — that is normal
and correct, and it is not a reason to claim the next दोहा.

The same asymmetry means **a page can carry no new दोहा at all** — printed page 55 is entirely the tail of
दोहा 56's टीका and हिन्दी. That is not a gap; say so in your report and move on.

**The Hindi has its own पातनिका, and it sits at the end of the previous दोहा's block.** Just as the Sanskrit
पातनिका is printed above the दोहा it introduces, the हिन्दी stream ends a दोहा's block with a transitional
sentence — `इसके बाद मिथ्यादृष्टिके लक्षणके कथनकी मुख्यतासे आठ दोहे कहते हैं–` — that introduces the **next**
दोहा. It is printed in the outgoing दोहा's paragraph but it belongs to the incoming one. Attach it to the
दोहा it introduces, not to the one it follows.

## Two things the opening batch established

**The पातनिका belongs to the टीका.** Before each दोहा the edition prints a short Sanskrit sentence of
श्री ब्रह्मदेव's own — `अथ संसारसमुद्रोत्तरणोपायभूतं …` — introducing what the दोहा will say. The टीका
itself names this a **पातनिका** and tells you it recurs: `इत्यनेन क्रमेण पातनिकास्वरूपं सर्वत्र ज्ञातव्यम्`.
It is printed *above* the दोहा but it is commentary, so make it **`(T1)` of that दोहा's टीका**. Do not drop
it and do not attach it to the previous दोहा.

**दोहा density varies enormously.** श्री ब्रह्मदेव's commentary on the opening दोहा runs for pages — दोहा 1
alone fills printed pages 5–7 and needed 19 segments — while later pages carry two दोहा each. So a
nine-page batch may yield three § near the front of the book and fifteen near the back. Both are correct.
Transcribe what is on your pages; do not pad or compress to hit a count.

## The ग्रन्थ marks its own sub-sections — keep every colophon

श्री ब्रह्मदेव closes each **स्थल** (sub-section) with a sentence of his own counting the दोहा it held:

> `एवं मोक्षमोक्षफलमोक्षमार्गादिप्रतिपादकद्वितीयमहाधिकारमध्ये दशकेन मोक्षस्वरूपनिरूपणस्थलं समाप्तम् ।`
> `एवं त्रिविधात्मप्रतिपादकप्रथममहाधिकारमध्ये … भेदभावनास्थलसूत्रनवकं गतम् ।`
> `इत्येकत्रिंशत्सूत्रैश्चूलिकास्थलं गतम् ।`

and opens the next with `अथानन्तरम् … व्याख्यानस्थलं कथ्यते तद्यथा ।` or `… प्रारभ्यते ।`

**These are the most valuable sentences in the book for its structure** — they are the ग्रन्थ naming its own
divisions and telling you how many दोहा each holds, which is how the printed खण्ड headings will be built.
Never drop one, and never merge one into a neighbouring sentence.

Where to put them:

- a **closing** colophon (`…समाप्तम् ।` / `…गतम् ।`) is the **last segment** of the दोहा it follows;
- an **opening** one (`अथ… कथ्यते तद्यथा ।`) is **`(T1)` of the दोहा it introduces**, exactly like a पातनिका —
  and if the दोहा has a पातनिका of its own as well, both go in, opening colophon first;
- an अधिकार-closing colophon (`…प्रथममहाधिकारः समाप्तः ॥१॥`) is the last segment of the last दोहा of that
  अधिकार.

They are also the one place the edition's own दोहा arithmetic is stated, so they are worth quoting in your
report: `दशकेन` means that स्थल held ten, and the count is checkable against the § you wrote.

## योगसार is a different text with a different shape — read this if your range is scan 521+

योगसार is the second work in this volume, by the same श्री योगीन्दुदेव, and the edition treats it quite
differently. **It has no commentary at all** — no श्री ब्रह्मदेव टीका, no कथंभूत questions, nothing of what
fills परमात्मप्रकाश. Do not go looking for one.

What each दोहा carries, in this order:

1. the **अपभ्रंश दोहा**, two lines in bold, closing `॥ ४ ॥`;
2. the **संस्कृत छाया**, two lines, **printed inside square brackets** `[ … ]` — transcribe it without the
   outer brackets but keep any brackets *inside* it, such as the `(इति)` in दोहा 6;
3. a **`पाठान्तर—`** line: the edition's manuscript variants, numbered, each tagged with a manuscript
   siglum — `पाठान्तर—१) अपब-सायर. २) अप–अणंतो. ३) अ–मोहि, पब-मोहिउ.`;
4. an **`अर्थ—`** line: the Hindi. Note it is *not* the bracketed-lemma style परमात्मप्रकाश uses; it is
   continuous prose closing with `॥ ४ ॥`.

Not every दोहा has a पाठान्तर line. Where there is none, say so rather than leaving the part out.

### The § template for योगसार

Keys use base **30000** (key = 30000 + दोहा × 10 + star). The running header reads `-योगीन्दु-विरचितः-` with
`[ दो॰ ४–८` giving the दोहा range, and `योगसारः` on the recto.

```
§30040 — <title> (योगसार, दोहा 4, मुद्रित पृष्ठ 360)

## 1. मूल पाठ (अपभ्रंश दोहा)
(पृष्ठ 360)
<दोहा verbatim, both lines, with ॥ ४ ॥>

## 2. संस्कृत छाया (मुद्रित)
<छाया verbatim, both lines>

## 5. हिन्दी अनुवाद
<the printed अर्थ, verbatim>

## 6. मुद्रित पाठभेद
<the पाठान्तर line verbatim, sigla and numbering intact>
```

**Write the part-6 heading exactly as `## 6. मुद्रित पाठभेद`.** The builder keys on the word पाठभेद to put
it in the right slot, and the coverage gate requires it — a योगसार § without one fails the build.

### The पाठान्तर is scholarly apparatus — reproduce it, do not tidy it

Those sigla (`अ`, `ब`, `प`, and combinations like `अपब`, `पब`) are manuscript designations, and the whole
value of the line is that it records what each manuscript actually reads. So:

- keep the numbering `१)`, `२)`, `३)` and the sigla exactly as printed, including the hyphens;
- keep any `(?)` the edition prints — that is **its** uncertainty, not yours, and it is evidence;
- do **not** expand, translate, reorder or explain anything here. Part 10 is where it gets explained.

A variant that looks like a misprint is still what that manuscript reads. This is the one place in the whole
book where "transcribe exactly as printed" is not a fallback but the entire point.

## Accuracy guards

1. **This edition's fount is clean**, unlike the other scan of this text in `mool/`. If you ever find
   yourself reading `ग्र` where `अ` belongs, or `रा` where `ण` belongs, you have opened the wrong PDF —
   use only `Parmatmaprakash_and_Yogsara_001876.pdf`.
2. **Magnify before committing a doubtful conjunct.** The scan is about 300 dpi as rendered; above roughly
   600 dpi you are only interpolating.
   ```
   python -c "import pymupdf; d=pymupdf.open(r'mool/Parmatmaprakash_and_Yogsara_001876.pdf'); d[IDX].get_pixmap(dpi=600, clip=pymupdf.Rect(40,120,470,260)).save(r'C:\Users\naman\AppData\Local\Temp\claude\z.png')"
   ```
   `IDX = scan page − 1`; the page box is 504×684 pt.
3. **Two witnesses in the same volume settle a doubtful दोहा reading**, and both are rendered on request:
   the **critical अपभ्रंश text with manuscript variants** at scan 481–513, and the **alphabetical दोहा
   index** at scan 514–520. Use them before writing `[अस्पष्ट]` in a दोहा.
4. `[अस्पष्ट]` for a letter you genuinely cannot read is a **correct** answer; a plausible guess is not.
   Never silently normalise a worn अपभ्रंश form toward the Sanskrit you expect — the छाया printed beside
   it already gives the Sanskrit, and the whole value of the दोहा is that it is what the page says.
5. **The confirmed confusion pairs in this fount.** Each has already produced a wrong reading here, and
   none is safe at normal zoom. Magnify before committing any of them:

   | read as | is often | example found |
   |---|---|---|
   | `हृ`, or a chandrabindu | **रेफ + consonant** (`र्ह`, `र्द`) | `अत्राहृगुण…` → **`अत्रार्हद्गुण…`** (अत्र + अर्हद्गुण) |
   | `त्रि` | **वि** (व with the इ-matra) | `त्रिषयानुभव…` → **`विषयानुभव…`** |
   | `ल्ल` | **ल्ह** | `मेल्लहि` → **`मेल्हहि`** |
   | `ल` | **`त्व`** — the abstract-noun suffix, at small size | `कविलवादिलगमकलवाग्मिल` → **`कवित्व-वादित्व-गमकत्व-वाग्मित्व`** · `देहममलं` → **`देहममत्वं`** · `कृल्ला` → **`कृत्वा`** · `स्थिला` → **`स्थित्वा`** · `भिन्नलात्` → **`भिन्नत्वात्`**. Beware `कर्ममल` (कर्म+मल), which is genuine |
   | `श्च` / `श्व` | **`ञ्च`** | `पश्चपरमेष्ठि` → **`पञ्चपरमेष्ठि`** · `पश्वमकारसंसारे` → **`पञ्चप्रकारसंसारे`**. Beware `तपश्चरण` and `पश्चात्`, both genuine and frequent |
   | **`म`** | **`प्र`** — *the highest-yield error in this fount* | `सर्वमकारेण` → **`सर्वप्रकारेण`** · `मतिपक्ष…` → **`प्रतिपक्ष…`** · `आत्ममतिपादक` → **`आत्मप्रतिपादक`** · `विषयमभृति` → **`विषयप्रभृति`** · `अभिमायो` → **`अभिप्रायो`** · `मत्ययः` → **`प्रत्ययः`** |
   | `भ` / `म` | each other | throughout |
   | `व` / `ब` / `च` | each other | throughout; also `ष`-like loops for `व` (`सिष-पय` → `सिव-पय`) |
   | `छ` | **`ह`** | `छुइ भवति` → **`हुइ भवति`** (the मूल's own word is `हुइ`) |

   The pattern behind the first two is the same: **a mark that belongs to a conjunct gets read as a
   separate sign, or vice versa.** When a word will not construe, suspect the conjunct before the printing.

   **The `प्र` → `म` substitution deserves its own warning.** In the small टीका fount this edition uses,
   the `प्र` ligature's lower stroke merges into the bowl and the whole conjunct reads as a plain `म` at
   any magnification the scan supports — zooming does **not** resolve it, because the resolution is not
   there. Four separate readers hit it independently before it was named. Fourteen instances had to be
   corrected after the fact.

   So do not try to settle it by zooming. Settle it **lexically**: `मतिपक्ष`, `मत्यय`, `अभिमाय`, `मभृति`,
   `मकारेण` are not Sanskrit words at all, while `प्रतिपक्ष`, `प्रत्यय`, `अभिप्राय`, `प्रभृति`, `प्रकारेण` are
   common ones. **If a `म` sits where no Sanskrit word can have one, it is a `प्र`.** The same words print
   legibly elsewhere in the volume — in this corpus `प्रतिपक्ष` appears cleanly nine times against six
   degraded `मतिपक्ष`, and `अभिप्राय` twelve times against one `अभिमायो`. A parallel occurrence settles it.

   Beware the reverse, though: `समभाव`, `परमभाव`, `आत्मभाव`, `माया`, `कर्मणाम्`, `निरुपम`, `समाप्तम्`,
   `परिणमति`, `कर्मबन्ध` are all genuine and must be left alone. The test is whether the word exists, not
   whether it contains a `म`.

6. **Grep the corpus before you guess — this टीका repeats its idioms constantly.** When a phrase will not
   parse, search `parts/` for the surrounding words: श्री ब्रह्मदेव reuses a small stock of formulas, and the
   one you are staring at has almost certainly been printed legibly somewhere else.

   Worked case: `कं कर्मतापत्वम्` / `कानि कर्मसापत्तानि` parse to nothing. A grep across the batches showed
   the recurring idiom **`किं कर्मतापन्नम्` / `कानि कर्मतापन्नानि`** — `कर्मता + आपन्न`, the commentary's
   marker for "which has become the grammatical object" — used dozens of times. That settled both readings
   without a single zoom.

   Note this is the very phrase whose *mistranslation* in दोहा 2 prompted the audit pass: split wrongly as
   `कर्म + तापन्न` it yields "afflicted by karma", which cannot be true of the सिद्ध. Treat `कर्मता`,
   `कर्तृत्व`, `कर्मत्व`, `अभिधेय`, `वाच्य` as **grammatical** vocabulary here unless context forces otherwise.

7. **The हिन्दी below the rule is your witness for the संस्कृत above it — use it first.** This edition
   prints, for every दोहा, a हिन्दी rendering that glosses the टीका's own terms, with the Sanskrit lemma in
   square brackets. **When a Sanskrit glyph is doubtful, read the Hindi on the same page before you zoom.**
   It is the same editor rendering the same sentence, and it settles most doubts in seconds.

   Both doubtful readings on printed page 106 fell to this at once. The टीका appeared to read
   `…कविलवादिलगमकलवाग्मिल…`; the हिन्दी below says *"कविकलाका मद, वादमें जीतनेका मद, शास्त्रकी टीका
   बनानेका मद, शास्त्रके व्याख्यान करनेका मद, **ये चार तरहका** शब्द-गौरव"* — four abstracts, so
   `कवित्व-वादित्व-गमकत्व-वाग्मित्व`. And a quoted verse appeared to read `द्वेषाद्रोहाच्च`; the हिन्दी says
   *"जो द्वेषसे परके मारनेका … चिंतवन करे, और **रागभावसे** परस्त्री आदिका चिंतवन करे"* — so `द्वेषाद्रागाच्च`,
   the ordinary राग/द्वेष pair. No magnification was needed for either.

8. **A word broken across a line end is a trap — rejoin the halves before reading them.** The verse above
   is printed `…द्वेषाद्रा-` at the end of one line and `गाच्च…` at the start of the next. Read as one
   visual unit it yields the non-word `रोह`; rejoined it is plainly `रागात् + च`. **Whenever a doubtful word
   sits at the very start or very end of a line, check the other half before concluding anything.**

9. **A quotation from another ग्रन्थ has a received text — recall it.** The टीका quotes constantly, usually
   inside `"…"` and often closing with a verse number. That verse exists elsewhere and is usually
   well known; this one is श्री समन्तभद्र स्वामी's रत्नकरण्डश्रावकाचार. If your reading of a quoted verse
   differs from the text as it is normally transmitted, your reading is the thing to doubt first. Say so in
   your report either way.

10. **If the Sanskrit does not parse, re-read it before blaming the printing.** श्री ब्रह्मदेव writes
   correct Sanskrit; a sequence that construes to nothing is far more likely your reading than his.
   Confirmed cases from the opening batches:
   - `अत्राहृगुणस्वरूप…` would not parse. The page has **`अत्रार्हद्गुणस्वरूप…`** — `अत्र + अर्हद्गुण`, "the
     qualities of the अर्हत्". What looked like a chandrabindu is the **रेफ of अर्हत्**, and the `द्` went
     with it. A रेफ sitting above the following consonant is the commonest thing lost in this fount —
     whenever a word seems to begin `अह…`, `कह…`, `धह…`, check for a रेफ that makes it `अर्ह…`, `कर्ह…`.
   - A doubtful word often recurs in clean print a page or two later. Search for it before magnifying
     further: a parallel occurrence settles more than another zoom level.
   - **A form that recurs consistently is the edition's, not a misprint.** The टीका writes `संपितं` /
     `संपिताः` where classical Sanskrit wants `संपादितं` / `संपादिताः`, and does so every time, with the
     दोहा's own अपभ्रंश `संपिय` behind it. One odd spelling is a suspect; the same odd spelling four times
     over is the text. Print it and note it — do not regularise it.

   When a reading still will not parse after that, transcribe it exactly as printed **and say so in your
   report** — the audit pass is told to treat unparseable Sanskrit as a suspected transcription error and
   send it back. Do not quietly emend it into something that does parse.

11. **Never emend by adding or deleting a printed letter.** Both directions are the same mistake, and both
    always look reasonable.

    *Deleting*: the page prints `मोहो ममलादिविकल्पजालं`; `ममल` is not a word, so an agent dropped one `म`
    and wrote `मलादि` — which *is* a word, and is not what the page says. The confusion table gives
    **`ममत्वादि`** (ल = त्व), using every printed letter.

    *Adding*: a line ends `…स्थित्वा गृहादि-` and the next begins `ममत्वं त्यक्त्वा`. An agent bridged it as
    `गृहादौ ममत्वं`, inventing a `ौ` that is nowhere on the page. Simply rejoining the hyphen gives
    **`गृहादिममत्वं`** — one compound, every letter accounted for, nothing invented.

    **The printed letters are the constraint.** Substitute one the fount is known to confuse, rejoin what
    the line-break split, or flag it — but never change the letter count to reach a word. This is the one correction that always looks reasonable
    and is always wrong. The page prints `मोहो ममलादिविकल्पजालं`; `ममल` is not a word, so an agent dropped
    one `म` and wrote `मलादि` — which *is* a word, and is not what the page says. The right move was the
    confusion table: `ल` renders `त्व`, giving **`ममत्वादि`**, which uses every printed letter, is standard
    Jain vocabulary, and occurs fourteen times elsewhere in this very corpus.

    So when a word will not parse, **the printed letters are the constraint**. Substitute a letter the fount
    is known to confuse, or flag it — never silently delete one to make the remainder a word. A reading that
    throws away ink is a worse reading than one that admits defeat.

12. **Never "improve" the टीका's Sanskrit.** If it is ungrammatical as printed, print it as it stands and
   say so in your report. The next pass needs to know what the page actually has.

## Style

- English digits in your own prose (§ 20390, दोहा 39, पृष्ठ 160) — Devanagari digits **only** inside
  quoted मूल / छाया / टीका / हिन्दी, where `॥ ३९ ॥` stays exactly as printed.
- **Never write any sect name** (बीसपंथ / तेरापंथ or any sub-sect label) anywhere, for any reason.
- Jain आचार्य are never named bare in your own prose: `श्री योगीन्दुदेव`, `श्री ब्रह्मदेव`,
  `आचार्य श्री कुन्दकुन्द`, `श्री अमृतचन्द्र स्वामी`. The printed मूल, छाया, टीका and हिन्दी stay exactly
  as printed, honorifics or not.
- **No working-process language anywhere in `parts/`**: no "बैच", "इस सत्र", file names, scan-page numbers,
  "उपयोगकर्ता", no mention of other agents. Cross-refer only as "दोहा 39", "पूर्व-वर्णित दोहा".
- Every दोहा in your range must appear. Do not summarise, skip, or merge two दोहा the book keeps apart.

## Writing the file

**Write after your FIRST दोहा, then append.** A response is capped at 64,000 output tokens, and an agent
that batches eight pages and writes at the end can lose everything. Create the file with Write as soon as
the first § is done, then append each further § with Edit. Separate consecutive § with a blank line and `---`.

## Report back (under 250 words)

1. the § keys written and the अधिकार/दोहा range they cover;
2. the exact first 6 and last 6 words of मूल you transcribed, with printed page numbers — for seam checks;
3. **how many टीका segments you wrote in total, and any दोहा whose टीका you found hard to segment**;
4. every `[अस्पष्ट]`; every place the printed Sanskrit looked corrupt or ungrammatical; every place the
   printed हिन्दी seemed to say something the टीका does not — flag it, do not fix it;
5. whether the boundary pages ran mid-दोहा, and any page carrying no new दोहा.
