# परमात्मप्रकाश एवं योगसार — व्याख्या progress log

*Working notes only. Nothing from this file goes into the book.*

## Source — and why this edition

Two scans were in `mool/`. **Use `Parmatmaprakash_and_Yogsara_001876.pdf` (550 pp).** The other,
`06575 Parmatma Prakasha, Yogendo.pdf` (332 pp), is set in an old fount with systematic glyph
substitutions — **अ prints as a ग्र-like glyph** (`ग्रहं` = अहं, `ग्रथ` = अथ) and **ण as a रा-like one**
(`परिरगामो` = परिणामो). Transcribing from it would seed errors into every downstream Hindi rendering.
Confirmed at 500 dpi. Do not use it, not even for collation, without allowing for the fount.

The chosen edition is A. N. Upadhye's, Paramaśruta Prabhāvaka Maṇḍala / Rajchandra Jain Śāstramālā:
clean modern fount, no text layer (the embedded text is only the library watermark).

## What each printed page carries — verbatim for agent prompts

Above a horizontal rule:
1. the **अपभ्रंश दोहा** in bold, ending `॥ ३९ ॥`;
2. its **संस्कृत छाया**, two lines, smaller type — *already printed in this edition*, so it is transcribed,
   never reconstructed;
3. **श्री ब्रह्मदेव's संस्कृत टीका**, dense, with the दोहा's own अपभ्रंश words set in bold and glossed inline.
   It runs in the **कथंभूत catechetical style**: a statement, then `किं कृत्वा ।` / `कथंभूतः ।` / `कस्मात् ।` /
   `कः ।` / `कान् ।` and the answer to each.

Below the rule:
4. the **हिन्दी अनुवाद**, which prints the Sanskrit lemma in **square brackets** before each rendering —
   `[पुराकृतं कर्म] पूर्व उपार्जित कर्मोंको [क्षपयति] क्षय करता है` — an explicit Sanskrit↔Hindi alignment;
5. **भावार्थ**.

Running header: `–दोहा १९० ]  परमात्मप्रकाशः  २९५` or `योगीन्दुदेवविरचितः  [ अ० २, दोहा ३९–`.

## Scan map (established from a header contact sheet; offset is 161 throughout)

| section | scan | printed | in this book |
|---|---|---|---|
| English introduction (Upadhye) | 1–161 | — | **no** |
| **परमात्मप्रकाश, अधिकार 1** | 162–~275 | 1–~114 | yes |
| **परमात्मप्रकाश, अधिकार 2** | ~276–478 | ~115–317 | yes |
| **श्री ब्रह्मदेव's own epilogue — टीकाकारस्यान्तिमकथनम्** | **477–478** | **316–317** | **yes — back matter** |
| श्रीमद् राजचन्द्र quotations page | 479 | — | no |
| परमप्प-पयासु — critical अपभ्रंश text with ms. variants | **480**–~513 | ~319–~352 | no (verification witness only) |
| परमात्मप्रकाशदोहादीनां वर्णानुक्रमसूची | ~514–519 | ~353–358 | no (verification witness only) |
| **योगसार** | **520**–545 | **359**–384 | yes |
| योगसारदोहादीनां वर्णानुक्रमसूची | 546 | 385 | no |
| publisher's back matter | 547–550 | — | no |

**The map above is corrected. The first version was wrong in three places**, and one of them cost real work:

- **योगसार begins on scan 520, not 521.** Scan 520 is its title page (`श्रीमद्-योगीन्दुदेव-विरचितः /
  योगसारः / हिन्दीभाषानुवादसहितः`) **and carries दोहा 1, 2 and 3 beneath the title block**. Because the map
  called 514–520 "index", no batch was assigned that page and those three दोहा were simply never read. The
  agent that started at 521 reported honestly that its first दोहा was 4 and that it could not see 1–3; the
  coverage gate then named the three missing दोहा outright. **A title page is not an empty page** — in this
  volume it carries content, and a map built from running headers cannot see that, because a title page has
  no running header. That is exactly the blind spot of the header contact-sheet method.
- the critical अपभ्रंश text starts at **480**, not 481;
- **scan 477–478 is श्री ब्रह्मदेव's own epilogue**, `टीकाकारस्यान्तिमकथनम्` — two Sanskrit paragraphs with
  a Hindi rendering, a मंगल दोहा, and a second colophon `इति श्रीब्रह्मदेवविरचिता परमात्मप्रकाशवृत्तिः समाप्ता`,
  followed by the edition's publication facts (ग्रन्थसंख्या 4000; the संस्कृत टीका at 5004 श्लोक and
  पं. दौलतरामजी's भाषाटीका at 6890). **This is the commentator's own closing statement and belongs in the
  book as back matter** — it was initially classed as "not this book" and should not have been.

Images rendered at 300 dpi for the two content ranges only: `img/p0162.png`–`p0479.png` and
`img/p0521.png`–`p0547.png` (345 files).

**Two witnesses the volume gives us for free**, both outside the book but valuable for checking:
the critical अपभ्रंश text with manuscript variants (scan 481+) and the alphabetical दोहा index (scan 514+).
Render them when a reading needs settling.

## The three passes

The reader's standing instruction on this ग्रन्थ is that **the Hindi must not say anything the Sanskrit
टीका does not**. The failure they saw before was Sanskrit mistranslated — wrong sense, a समास split
wrongly, or a `कथंभूत` question attached to the wrong phrase. The passes are built around that.

| pass | model | writes | into |
|---|---|---|---|
| 1 — extraction | **Sonnet 5** | अपभ्रंश दोहा · मुद्रित संस्कृत छाया · ब्रह्मदेव टीका · मुद्रित हिन्दी · भावार्थ — all verbatim | `parts/` |
| 2 — व्याख्या | **Opus 5** | अन्वय · अन्वयार्थ · **टीका का खण्डशः हिन्दी अनुवाद** · विस्तृत व्याख्या · उदाहरण · तालिका · सन्दर्भ | `addenda/` |
| 3 — **verification** | **Opus 5** | an independent Sanskrit↔Hindi audit of every § written by pass 2 | `verify/` |

Pass 3 is new to this project and is the whole point. A *different* agent from the one that wrote the
Hindi reads the Sanskrit टीका and the Hindi side by side, clause by clause, and reports every place the
Hindi adds, drops or alters sense. Nothing self-certifies.

## Findings from the opening batch

- **printed pages 1–4 are a पीठिका**, not दोहा content: a synoptic table of the whole ग्रन्थ's
  अधिकार/प्रकरण structure, given in श्री ब्रह्मदेव's Sanskrit and in पं. दौलतरामजी's Hindi. It has no
  मूल/छाया/टीका shape, so it gets no §. **It belongs in the book as front matter** — it is the ग्रन्थ's own
  table of contents and worth having. Commission it separately.
- **The पातनिका** — a short Sanskrit sentence of श्री ब्रह्मदेव's printed *above* each दोहा — is commentary
  and becomes `(T1)` of that दोहा's टीका. The टीका names it: `इत्यनेन क्रमेण पातनिकास्वरूपं सर्वत्र ज्ञातव्यम्`.
- **Density varies hugely.** दोहा 1 fills printed pages 5–7 and took 19 टीका segments; later pages carry
  two दोहा each. Nine-page batches will yield 3 § near the front and perhaps 15 near the back.
- **The worked example that justifies pass 3.** दोहा 2's टीका has `तान् सिद्धगणान् कर्मतापन्नान् अहं वन्दे ।`
  `कर्मतापन्नान्` is **कर्मता + आपन्नान्** — "which have become the grammatical object" of `वन्दे`, a note
  about the sentence. Split as **कर्म + तापन्नान्**, "afflicted by karma", it yields fluent Hindi that says
  the सिद्ध are afflicted by the karma the verse says they burnt away. The transcription was right; the
  gloss in the batch report was not. **A reading that cannot be true of its subject is wrong however well
  it parses** — now the headline test in both the व्याख्या and the audit specs.

## Lessons

**`प्र` prints as a plain `म` in the टीका fount — and no amount of zooming resolves it.** The scan simply
does not carry the resolution; at 1100 dpi the `प्र` ligature's lower stroke has already merged into the
bowl. Four readers hit it independently before anyone named it, and 14 instances had to be corrected after
the fact (`सर्वमकारेण`, `मतिपक्ष…`, `आत्ममतिपादक`, `विषयमभृति`, `अभिमायो`, `मत्ययः`).

The thing that settled it was not a sharper image but **the corpus itself**: the same words print legibly
elsewhere in the same volume, and a count showed `प्रतिपक्ष` clean 9 times against 6 degraded `मतिपक्ष`,
`अभिप्राय` clean 12 times against 1 `अभिमायो`, `प्रतिपादक` 7 against 3. Page 75 even gives a minimal pair
in one view — the टीका's `इत्यभि?ायः` above the rule and the हिन्दी's unmistakable `अभिप्राय` below it.
**Generalise: when a fount fault is systematic, the fix is lexical and statistical, not optical.** A
whole-corpus sweep for impossible letter sequences finds in one pass what page-by-page zooming never will.
The sweep must be triaged by hand, though — `समभाव`, `परमभाव`, `माया`, `कर्मणाम्`, `निरुपम`, `समाप्तम्`,
`परिणमति` all contain the same sequence and are perfectly good words.

**The टीका and the हिन्दी are two independent streams on every page**, separated by the horizontal rule and
*not* page-synchronised: a page's टीका can be closing दोहा 57 and opening 58 while the हिन्दी below it is
still finishing 57. दोहा boundaries must be tracked per stream by its own `॥ N ॥` closings. A consequence:
some pages carry no new दोहा at all, which is not a gap.

**The हिन्दी has its own पातनिका too.** The transitional sentence `इसके बाद … कहते हैं–` printed at the tail
of one दोहा's हिन्दी block introduces the **next** दोहा. Easy to mis-attribute to the दोहा it follows.

**The edition's own shorthand is not a misprint.** The टीका writes `संपितं` / `संपिताः` for `संपादितं` /
`संपादिताः` consistently, with the दोहा's अपभ्रंश `संपिय` behind it. Reproduced as printed.

**दिगम्बर / श्वेताम्बर in दोहा 88 stay.** The standing rule is that no **sub-sect** label (बीसपंथ, तेरापंथ)
is ever written. दोहा 88's whole argument is that the आत्मा is none of the लिंग — बौद्ध, दिगम्बर, श्वेताम्बर —
so the names are the ग्रन्थ's own subject matter, not an editorial intrusion. Transcribed verbatim; the
व्याख्या must present them as the मूल does, as लिंग-भेद the आत्मा transcends, and must not take a side.

## groups.json — build the खण्ड headings from the ग्रन्थ's own colophons

Do not invent section headings for this book. श्री ब्रह्मदेव marks every **स्थल** himself, closing it with a
sentence that names it and counts its दोहा (`…दशकेन मोक्षस्वरूपनिरूपणस्थलं समाप्तम्`,
`…भेदभावनास्थलसूत्रनवकं गतम्`, `इत्येकत्रिंशत्सूत्रैश्चूलिकास्थलं गतम्`) and opening the next with
`अथानन्तरम् … कथ्यते तद्यथा`. अधिकार 2 even opens by declaring its own total:
`…चतुर्दशाधिकशतद्वयमितैर्दोहकसूत्रैः … द्वितीयमहाधिकारः प्रारभ्यते` — 214, matching the पीठिका.

So once pass 1 is complete, harvest every `स्थल` / `महाधिकार` colophon out of `parts/`, pair each closing
with the following opening, and write `groups.json` from them: the heading is the स्थल's own name and the
दोहा it starts at is the key. This also gives a **free arithmetic check** — each colophon states how many
दोहा its स्थल held (`दशकेन` = 10, `सूत्रनवकं` = 9, `एकत्रिंशत्सूत्रैः` = 31), which must equal the number of §
written between the two markers. A mismatch means a दोहा was lost or double-counted.

`check_colophons.py` now does this harvest and reads the count word out of each colophon. Three things
it had to learn, all of which cost a wrong answer first:

- **The स्थल nest.** A 41-दोहा महास्थल contains अन्तरस्थल of 5 and 15. So a colophon's स्थल does *not* begin
  where the previous one ended, and the script must not assume it does. It reports the range each stated
  count **implies**, ending at the दोहा the colophon sits on, and leaves the matching-up to a reader.
- **Sandhi swallows the numeral's initial vowel.** `सूत्रम् + एकं` prints as `सूत्रमेकं`, `स्वरूप + अष्टकं`
  as `स्वरूपाष्टकं`, `इति + एकत्रिंशत्` as `इत्येकत्रिंशत्`. A search for the bare numeral finds none of
  them. The table now carries the matra form of every vowel-initial numeral.
- **A merged § must count as all the दोहा it claims**, or a legitimate सूत्रत्रय merge reads as a gap.

As of अधिकार 2 दोहा 58, all 16 colophons resolve and every दोहा they imply has a § written. The ग्रन्थ's
own arithmetic and the extraction agree.

## The structure of अधिकार 2, confirmed from two directions

The पीठिका declares अधिकार 2 = **30 + 36 + 41 + 107 = 214**. All four blocks have now been met in the text
and they agree:

- the colophons found so far close स्थल of 10, 1, 19, 3, 12 and 14 दोहा inside the first blocks;
- a **41-दोहा महास्थल** closes at दोहा 107, made of four अन्तरस्थल (5 + 15 + … + 13), exactly the third figure;
- दोहा 108 opens with `अत ऊर्ध्वं … सप्ताधिकशतसूत्रपर्यन्ते …` — a **107-दोहा चूलिका** running to the end,
  exactly the fourth figure, and 108 + 107 − 1 = 214.

The edition's हिन्दी calls that चूलिका "तीसरा महाधिकार" outright: *"आगे 'परु जाणंतु वि' इत्यादि एकसौ सात
दोहा पर्यंत **तीसरा महाधिकार** कहते हैं, उसीमें ग्रंथको समाप्त करते हैं"*. **Keep it keyed to अधिकार 2
regardless** (base 20000). Four witnesses say so against the हिन्दी's one:

1. the दोहा numbering continues unbroken to 214;
2. the पीठिका counts it inside अधिकार 2 (30+36+41+107 = 214);
3. the Sanskrit colophon calls the section just closed `द्वितीयमहाधिकारमध्ये` and what follows a
   `चूलिकाव्याख्यानम्` — an appendix *within* the same discussion, introduced by `अत ऊर्ध्वम्`;
4. **the running header on that very page still reads `[ अ० २, दोहा १०८–`.**

Two agents reached this seam independently and both flagged it rather than deciding alone, which is the
behaviour the spec asks for. The हिन्दी's label is worth a sentence in the front matter — it is a real
feature of the edition — but not a change to the keys.

## परमात्मप्रकाश verified against its own closing colophon

श्री ब्रह्मदेव ends the वृत्ति by counting everything he has written:

> `… प्रथमस्तावत् … त्रयोविंशत्यधिकशतसूत्रेण प्रक्षेपकत्रयसहितेन प्रथममहाधिकारो गतः । तदनन्तरं
> चतुर्दशाधिकशतद्वयेन प्रक्षेपकपञ्चकसहितेन द्वितीयोऽपि महाधिकारो गतः । एवं
> पञ्चाधिकचत्वारिंशत्सहितशतत्रयमित…दोहकसूत्राणां विवरणभूता परमात्मप्रकाशवृत्तिः समाप्ता ॥`

Every figure matches the extraction:

| the colophon says | we have |
|---|---|
| अधिकार 1 = 123 दोहा | 123 |
| **+ प्रक्षेपकत्रय** (3) | 3 starred — §10651, §11232, §11233 |
| अधिकार 2 = 214 दोहा | 214 |
| **+ प्रक्षेपकपञ्चक** (5) | 5 starred — §20461, §21112, §21113, §21114, §21375 |
| grand total **345** | 123 + 3 + 214 + 5 = **345** |

and the चूलिका's own arithmetic closes too: 81 + 24 + 2 = 107, the fourth figure of the पीठिका's
30+36+41+107 = 214. The author, the पीठिका, the running headers and 35 independently-written batch files
all agree.

**One real error in the edition, left as printed.** The closing **हिन्दी** colophon renders अधिकार 2's body
as "एकसौ चौदह दोहे … ११९ दोहोंमें दूसरा महाधिकार" (114 + 5 = 119) where the Sanskrit immediately above it
says `चतुर्दशाधिकशतद्वयेन` = **214**. 214 is the figure consistent with the पीठिका and with the grand total;
the हिन्दी appears to have dropped "दो सौ". Transcribed verbatim and recorded in the flags — the edition's
inconsistencies are reproduced, not harmonised.

## A gate bug worth remembering: read the authoritative field, not the first match

`check_coverage.py` reassigned three प्रक्षेपक to दोहा 1, 2 and 3. The data was fine. The titles read

> `§21112 — प्रक्षेपक दोहा 1: नग्नरूप धारण कर … (अधिकार 2, दोहा 111*2, मुद्रित पृष्ठ 229–230)`

and the gate's `दोहा\s*(\d+)` found the **descriptive prefix** before reaching the parenthetical that
actually carries the reference. The fix is to extract the parenthetical first and search only inside it.

This is the **same class of bug** as `check_colophons.py` reading the first number word in a nested
colophon and reporting a स्थल of 8 as 41. Both times a regex found *a* match where the *right* match lay
further on. When a field appears more than once in a string, say which occurrence is authoritative —
never let position decide by accident.
