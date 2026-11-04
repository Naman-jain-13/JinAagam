# Pass 2 — व्याख्या spec (मूलाचार, अधिकार 5 : पंचाचाराधिकार)

*Working document. Nothing here goes into the book.*

# INDEPENDENCE — the rule above all others (the reader's explicit instruction)

> **इस पुस्तक में किसी मौजूदा हिन्दी अनुवाद का प्रभाव नहीं होना चाहिए, और न किसी अनुवादक/सम्पादक का नाम। अनुवाद पूरी तरह आपका स्वतन्त्र है — केवल प्राकृत गाथा और श्री वसुनन्दि की संस्कृत आचारवृत्ति से।**

Your **only** sources are the files in the source folder named in your task (`mulachar_src\s<key>.md`): the **प्राकृत गाथा**
(part 1), **श्री वसुनन्दि's संस्कृत आचारवृत्ति** in tagged segments `(T1)`, `(T2)` … (part 6, under a heading containing "मूल"), and the
manuscript-variant footnotes (part 11). **Do not open `parts/`, `img/`, `mool/`, `_archive_v1/`, `verify/`, or any other file in the project that
might carry a Hindi translation of this text, and do not consult any existing Hindi rendering from memory as a model.** If you are unsure of a
Sanskrit reading, say so (`सन्दिग्ध`) — do not reach for a printed translation. **Never mention** a printed/मुद्रित हिन्दी, an editor, a translator,
or "the edition's" translation anywhere in what you write; the book contains no such reference. (Mentions of a footnote's *variant reading*, such as
"एक प्रति में अन्यथा पाठ है", are fine.)

Each file's **first line** is `शीर्षक: <one Hindi line, 8–16 words, saying what this गाथा establishes — written from the Sanskrit alone>`. You write parts **2, 3, 4, 5, 6-Hindi, 7, 7-क, 8, 9, 9-क, 10** into `addenda/s<key>.md` (`§1980` → `addenda/s1980.md`). **Part 5 is yours**: the Hindi
rendering of the गाथा itself (see below). The book carries no other गाथा-अनुवाद.

---

# The aim of this book — give it to yourself before every §

> **मूलाचार एक आचार-ग्रन्थ है। इसका पाठक साधु है (और आर्यिका, ऐलक, क्षुल्लक, विद्वान् श्रावक)। इसलिए हर गाथा का
> व्याख्यान केवल "यह क्या कहती है" पर नहीं रुकेगा — वह यह भी बताएगा कि इस गाथा की बात को जीवन में कैसे उतारा
> जाए, और जो क्रिया बताई गई है उसका युक्तिसंगत (तर्कसंगत) उद्देश्य क्या है।**

The reader asked for each गाथा to be treated in this order, and the parts below map onto it:

| the reader asked for | where it lives |
|---|---|
| मूल गाथा, उसका अर्थ | part 1 — प्राकृत गाथा (printed) · **part 5 — गाथा का हिन्दी अनुवाद (yours)** · parts 2, 3, 4 — छाया, अन्वय, अन्वयार्थ (yours) |
| टीका, उसका अर्थ | part 6 — Sanskrit आचारवृत्ति (printed) with its Hindi (yours) |
| विशेष व्याख्या | part 7 |
| ग्रन्थ में जो प्रत्येक क्रिया बताई, उसका **युक्ति (तर्क) संगत उद्देश्य** भी बताएँ — जैसे *अमुक क्रिया से अमुक कषाय की निवृत्ति होती है* | **part 7-उद्देश्य** |
| आचार-ग्रन्थ होने से साधु के लिए practical रूप — **कुछ techniques, जहाँ भी possible हो, कि इस गाथा की बात को जीवन में कैसे उतारें; कितनी बार इस एक क्रिया का अलग से चिन्तन, practice, discussion आदि करें ताकि उस आचरण को अच्छे से अच्छे रूप में समझें और practically apply कर सकें** | **part 9-आचरण** |

---

# The thing this book must get right — fidelity

The Hindi in part 6 **must not say anything the Sanskrit आचारवृत्ति does not say.** An independent agent will
afterwards read your Hindi against the Sanskrit clause by clause and report every addition, omission and shift
of sense. Write as though that audit will happen, because it will.

## Part 6 — the Sanskrit आचारवृत्ति rendered into Hindi

**You never retype the Sanskrit.** It is in `parts/`, tagged `(T1)`, `(T2)`, … You write a Hindi line against
each tag, using **exactly the tags pass 1 used, all of them, in order**:

```
## 6. टीका का हिन्दी अनुवाद
(T1) <Hindi for segment T1>
(T2) <Hindi for segment T2>
```

If a segment defeats you, still write its line and say so in it: `[इस खण्ड का अर्थ सन्दिग्ध है: …]` — a missing
tag is a hole the reader cannot see.

Method, in order:

1. **Separate the quoted प्राकृत from the Sanskrit.** The वृत्ति quotes the गाथा's words (bold in print) and glosses
   each: `मूलगुणेसु—मूलानि च तानि गुणाश्च …` is the प्राकृत word `मूलगुणेसु`, then `—`, then its Sanskrit gloss.
   Render as a gloss: `'मूलगुणेसु' — मूल जो गुण हैं, वे मूलगुण …`. Never treat the quoted प्राकृत as a Sanskrit sentence.
2. **Render questions as questions, each joined to its own answer.** `किम्`, `कथम्`, `कस्मात्`, `कथंभूतः`, `कः`, `किं कृत्वा`,
   `प्रश्नः … उत्तरम्`, `आशङ्क्याह`, `नन्वेवम्`. The gender and number of `कथंभूतः/ता/तम्` tell you which noun it asks
   about — find the noun it agrees with.
3. **Split every समास and say how the members relate** (तत्पुरुष / कर्मधारय / बहुव्रीहि / द्वन्द्व …). Show the split in the
   Hindi where it is not obvious. Where two splits are defensible, give the one the doctrine and the गाथा support and
   record the other in part 10.
4. **Keep the particles** — `एव` (ही), `अपि` (भी), `तु`, `च`, `हि`, `किल`, `नूनम्`, `इति`, `वा` (अथवा). Dropping `एव` turns
   an exclusive claim into a loose one.
5. **Carry the case of the final member** of a compound — it governs the whole compound's role.
6. **Account for every word** — re-read the Sanskrit once more after writing the Hindi.
7. **The test that catches a wrong split is doctrinal, not grammatical:** a reading that contradicts the very
   गाथा it explains is wrong, however well it parses. Ask whether it could be true of the subject.
8. **If a split only works by reading `म` as something else, try `प्र` first; `ल` may stand for `त्व`.** A split that
   invents vocabulary, or leaves a printed letter unexplained, is wrong. A wrong split leaks small additions
   into the Hindi, and those are the hardest errors to see later.
9. **A शब्द-गौरव list, a numbered list or an enumeration in the वृत्ति must come out complete** — count the items
   in Sanskrit, count them in Hindi.

### A sub-division colophon is structural
A sentence that closes or opens a division of the book (`इति … अधिकारः`, `… प्रथमः परिच्छेदः`) is translated in part
6 like any segment, but it is about the *book*: keep it out of parts 3, 4, and out of the भावार्थ; part 7 may
note once which division is opening or closing.

## The other parts

### 2. संस्कृत छाया (व्याख्याकार-कृत)
**This edition does not print a छाया of the गाथा.** You compose one — and the book says so honestly (the builder
prints "व्याख्याकार-कृत"). Compose it **from the आचारवृत्ति's own gloss**: each प्राकृत word's Sanskrit equivalent
as श्री वसुनन्दि gives it (`मूलगुणेसु` → `मूलगुणेषु`, `वंदित्ता` → `वन्दित्वा`), in the गाथा's own word order, two
lines as the गाथा has two lines, closing with the printed `॥५॥`. Where the वृत्ति does not fix a word, use its
standard Sanskrit equivalent — never an invented sense. Heading exactly `## 2. संस्कृत छाया (व्याख्याकार-कृत)`.

### 5. गाथा का हिन्दी अनुवाद
Heading exactly `## 5. गाथा का हिन्दी अनुवाद`. **Your own rendering of what the प्राकृत गाथा says**, 40–90 words, as one flowing Hindi passage that follows the गाथा's
two lines in order. Use the आचारवृत्ति only to fix the sense of a word (`वृत्ति के अनुसार` is *not* needed here), **never to add matter the गाथा does not
carry** — the explaining belongs to parts 6–7. No भावार्थ, no examples, no bracketed Sanskrit lemmas. Where the गाथा is a bare list of names, the
Hindi is the list. Keep the गाथा's particles (`च`, `ही`, `भी`). It is printed straight after the छाया, so it must stand alone and read as Hindi, not as a gloss.

### 3. अन्वय
The words **of the प्राकृत गाथा**, as printed, rearranged into straight prose order — कर्ता, कर्म/विशेषण, क्रिया.
Do not substitute Sanskrit; a genuinely implied word goes in `( )`.

### 4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ)
Every पद of the अन्वय, in order, one per line: `- **मूलगुणेसु** (मूलगुणेषु, सप्तमी ब.व.) = मूलगुणों के विषय में`.
Sanskrit in `( )` follows your part 2 / the वृत्ति's gloss. Split compounds with `+`. Close with `- **॥५॥** = गाथा-क्रमांक`.

### 7. जैनागम के अनुसार विस्तृत व्याख्या
4–7 bullets, each 100–200 words, each with a bold sub-heading: what this गाथा establishes and why it stands here;
the doctrine behind it and the सूत्र / ग्रन्थ it rests on; the opposing position stated fairly where there is one;
cross-links (`देखें मूलाचार गाथा 5`); an honest limit where the गाथा is compressed or the वृत्ति supplies what the
गाथा does not. **मूलाचार is a साधु-आचार text, not a न्याय text:** let the व्याख्या keep that register — concrete, about what a
साधु does and why.

### 7-उद्देश्य. क्रिया का युक्तिसंगत उद्देश्य
Heading exactly: `## 7-क. क्रिया का युक्तिसंगत उद्देश्य (प्रयोजन एवं कषाय-निवृत्ति)`.

**Every क्रिया, व्रत, नियम or भावना the गाथा names gets one bullet**, in this shape:

`- **<क्रिया>** — *उद्देश्य:* … । *युक्ति:* (why it achieves this — the reasoning a thoughtful साधु would accept) … । *निवृत्ति:* the कषाय / दोष / आस्रव / अशुभ-भाव it curbs (क्रोध, मान, माया, लोभ; राग, द्वेष; हिंसा; प्रमाद …) … ।`

- Take the *उद्देश्य* from the वृत्ति wherever it states one (`… निमित्तम्`, `… हेतोः`, `… रक्षार्थम्`) and say so
  (`वृत्ति के अनुसार`). Where it is your own reasoning from the doctrine, say so (`व्याख्याकार का तर्क`). **Never
  present your own युक्ति as आगम-वचन.**
- A युक्ति must be a real argument, not a restatement. Weak: "अहिंसा से हिंसा छूटती है।" Good: "प्राणिपीड़ा का
  मूल कारण प्रमाद-युक्त योग है (तत्त्वार्थसूत्र 7.13 — प्रमत्तयोगात्प्राणव्यपरोपणं हिंसा); जब चलना-उठाना-रखना देखकर
  किया जाता है तो प्रमाद का अवसर घटता है, इसलिए हिंसा से पहले उसका कारण ही रुकता है।"
- Name the specific कषाय where the doctrine supports it, and say *how* the क्रिया curbs it (mechanism, not label).
  Nothing is to be forced: if no कषाय is the natural target, say what the real target is.
- If the गाथा names no क्रिया (a मंगल, a प्रतिज्ञा, a list), still give the purpose of what it **does**: why a text of
  conduct opens with a नमस्कार; why the list is counted; what a साधु gains by knowing the number. Never leave it blank.
  If truly nothing applies: `इस गाथा में कोई पृथक् क्रिया नहीं कही गई; उसका प्रयोजन ऊपर भाग 7 में आ चुका है।`

### 8. सरल उदाहरण
2–3 everyday analogies a श्रावक can follow. State the दृष्टान्त, then the दार्ष्टान्तिक — what maps to what — and
**where the analogy stops**. Build on the वृत्ति's own analogy first. If purely enumerative:
`इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।`

### 9. तुलनात्मक तालिका / चार्ट
One markdown table, 3–7 rows, of whatever kind the गाथा calls for. If none helps:
`इस अनुच्छेद हेतु तालिका आवश्यक नहीं।`

### 9-आचरण. साधु-जीवन में उतारने की विधि
Heading exactly: `## 9-क. आचरण-विधि एवं अभ्यास (साधु-जीवन में उतारने के सूत्र)`.

**This is the part the reader values most. Write it for a साधु who wants to *do* this, not merely understand it.**
3–6 bullets, each 40–100 words, drawn from the following, **wherever the गाथा makes it possible**:

- **चिन्तन** — what to reflect on, at what time of the day (प्रातः / सामायिक-काल / आहार से पहले / प्रतिक्रमण-काल),
  and what question to ask oneself (`आज किस क्रिया में प्रमाद रहा?`).
- **अभ्यास** — a concrete drill: the steps, and **how many times** (e.g. `दिन में तीन बार`, `प्रत्येक क्रिया से पहले
  एक बार`, `एक सप्ताह तक केवल इसी एक नियम पर ध्यान`) so that the practice becomes natural.
- **चर्चा** — a question to discuss with गुरु / सहसाधु / संघ, and what a good answer would look like.
- **परीक्षण / संकेत** — how to tell the practice is taking root (a symptom, a lapse to watch for); and the common
  mistake that spoils it.
- **परिस्थिति-विशेष** — one line on the hard case (rain, illness, travel, crowded town) where this is tested.

Rules:
1. Each bullet starts with its tag in bold — `**चिन्तन.**`, `**अभ्यास.**`, `**चर्चा.**`, `**परीक्षण.**`.
2. **Honesty about the source.** Put `[आगम-सम्मत]` after anything the वृत्ति or the आगम states (including a stated
   number of times, an hour, an order). Put `[सुझाव]` after anything that is the व्याख्याकार's suggestion for
   practice. **Never present a suggested frequency as आगम-विधान.** If the आगम gives no number, say so and offer a
   sensible one as `[सुझाव]`.
3. **Nothing against the आगम and nothing the वृत्ति does not license as conduct.** A technique must serve the very
   क्रिया the गाथा prescribes — never invent a new vow or a new rule, and never soften a rule.
4. **Do not invent an authority.** A drill is a drill; it is not "as the शास्त्र says" unless it does.
5. Where the गाथा makes no practical technique possible (a pure मंगल or definition), still give the one practice
   it makes possible — e.g. what a साधु does with a नमस्कार, how a list is committed to memory. If truly none:
   `इस गाथा से कोई पृथक् अभ्यास-सूत्र नहीं निकलता; इसका उपयोग आगामी गाथाओं के अभ्यास की पूर्व-पीठिका के रूप में है।`
6. Where it genuinely applies to a श्रावक (e.g. अहिंसा-अणुव्रत), one closing line may say so.

### 10. सन्दर्भ एवं पाद-टिप्पणी
**1 to 3 one-line bullets, no blank line between them.** Printed at dictionary size. Only: the source of a verse quoted in the वृत्ति (ग्रन्थ and
number — only if you are certain; `लगभग` / `सम्भवतः` when unsure; nothing at all rather than a guess); a one-line note where a समास admits two
splits, or where a worn/suspect reading in the Sanskrit forced a choice, or where a manuscript variant in part 11 would change the sense. Otherwise:
`मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।` (Part 11's variants are already printed in the book — do not copy them.)

---

## Lessons from the earlier audit of this very chapter — avoid these faults
1. **Mark the source of every reason.** In 7-क, an उद्देश्य the वृत्ति states gets `वृत्ति के अनुसार`; **every युक्ति you add is your own and must carry
   `(व्याख्याकार का तर्क)`**, even when it follows a `वृत्ति के अनुसार` उद्देश्य in the same bullet. Never let your reasoning read as the वृत्ति's.
2. **9-क tags are exactly `[आगम-सम्मत]` or `[सुझाव]`** — one tag per sentence-group, never a combined or invented tag; **every bullet, including a
   closing श्रावक line and "आम भूल" remarks, carries a tag.** A frequency, count, duration, hour or order is `[सुझाव]` unless the वृत्ति states it.
   **Never prescribe one number for all cases** (e.g. a fixed उच्छ्वास count for every कायोत्सर्ग — the वृत्ति gives different counts for different नियम).
3. **Hard cases go to the गुरु, unresolved:** illness, travel, a lost tool, an unsuitable site, "may I drop one of the stated qualities", health reasons
   for avoiding a food, whom to ask for permission. Say so; do not settle them. Never soften a rule.
4. **Cross-references must be exact and verifiable.** Cite `गाथा N` only if you have read that गाथा in the source folder and it says what you claim.
   The दैवसिक (evening) प्रतिक्रमण reviews *the day*; the रात्रिक one reviews the night — do not mix them up.
5. **Part 3 (अन्वय) ends with the printed `॥N॥`.** Part 2 (छाया) is two lines closing `॥N॥`, with correct sandhi.
6. **Counts:** if the वृत्ति lists items, list them all; do not say "five" and name three. Keep nokaṣāya vs kaṣāya, प्राप्यकारी vs अप्राप्यकारी straight
   (the eye is अप्राप्यकारी — it does not reach its object; the other four इन्द्रिय are प्राप्यकारी).
7. Where the वृत्ति uses `च` for `एव` or `वा` for "and" (a recurring idiom), read the sense against the गाथा and the doctrine, not the particle alone.

## Before writing a §, read
1. the § itself in `parts/` — all of it, especially every `(Tn)` segment;
2. the §§ immediately before and after, so cross-links and "why here" are real;
3. for the first § of your range, the preceding § in full — the वृत्ति often carries an argument across गाथा.

## Context — where the ग्रन्थ stands
**मूलाचार**, प्राकृत गाथा by **श्री वट्टकेराचार्य**, with **श्री वसुनन्दि सिद्धान्तचक्रवर्ती's आचारवृत्ति** (संस्कृत). It is the आचार-text of the जैन साधु's conduct, in twelve अधिकार.
Adhikāra 1 (मूलगुण, 1–36) gave the 28 मूलगुण; 2 (बृहत्प्रत्याख्यान-संस्तरस्तव, 37–107) the long प्रत्याख्यान and समाधिमरण; 3 (संक्षेपप्रत्याख्यान, 108–121) its short form; 4 (समाचार, 122–197) the सामाचार — conduct toward fellow साधु, गुरु and संघ.
**This is अधिकार 5 — पंचाचाराधिकार (गाथा 198–419)**: the five **आचार** — दर्शनाचार (roughly 198–266: जीव-अजीव and the nine पदार्थ, then the eight अंग of सम्यग्दर्शन),
ज्ञानाचार (267–287: the eight भेद, कालशुद्धि and the other शुद्धियाँ of स्वाध्याय), चारित्राचार (288–344: महाव्रत, रात्रिभोजन-निवृत्ति, प्रणिधान, the five समिति,
three गुप्ति and the व्रत-भावनाएँ), तपाचार (345–412: six external and six internal तप) and वीर्याचार (413–418), closing at 419. These ranges are only orientation — follow the वृत्ति. Read each गाथा in the source folder with the गाथा before and after it; the वृत्ति often carries one argument across several गाथा.
Do not assert more than the वृत्ति says; where it gives a list, give the whole list.

## Style — binding
- शास्त्रीय, clear हिन्दी. English digits in your prose — Devanagari digits **only** inside quoted मूल / वृत्ति,
  where `॥५॥` stays as printed.
- **Never write any sect name** (बीसपंथ / तेरापंथ or any sub-sect label) anywhere, for any reason.
- **Jain आचार्य are never named bare:** `श्री वट्टकेराचार्य`, `श्री वसुनन्दि सिद्धान्तचक्रवर्ती`, `आचार्य श्री कुन्दकुन्द`,
  `श्री अमृतचन्द्र स्वामी`, `श्री पूज्यपाद स्वामी`, `श्री उमास्वामी`. Write the honorific **at source**, including when
  a case-ending follows. Non-Jain opponents are plain.
- **No working-process language anywhere** (and no reference to any printed translation, editor or translator): no "बैच", "इस सत्र", file names, scan pages, "उपयोगकर्ता", no mention of
  other agents or of how the book was made.
- **तत्त्वार्थसूत्र: use the (सर्वार्थसिद्धि) recension.** 7.13 प्रमत्तयोगात्प्राणव्यपरोपणं हिंसा · 5.29 सद्द्रव्यलक्षणम्
  · 5.30 उत्पादव्ययध्रौव्ययुक्तं सत्. When unsure of a number, cite the सूत्र text and the अध्याय alone.
- **Never fabricate** a citation, a verse number or a doctrine. "लगभग" / "सम्भवतः" where unsure; silence where you
  do not know. This book will be cited.

## Writing the files
**Write each § as its own file, immediately, one at a time** — `addenda/s370.md` for `§370`. Do not accumulate several
and write at the end.

Order of headings in each file: `## 2.` · `## 3.` · `## 4.` · `## 5. गाथा का हिन्दी अनुवाद` · `## 6. टीका का हिन्दी अनुवाद` · `## 7.` · `## 7-क.` ·
`## 8.` · `## 9.` · `## 9-क.` · `## 10.`.

## Report back (under 250 words)
The § keys completed; every समास you split against the obvious reading and why; any `(Tn)` segment whose Sanskrit you could not construe, named
explicitly; any citation you wanted but could not verify; any part 7-क / 9-क point you were unsure of; and confirmation that every § in your range has a
file and every `(Tn)` tag has a Hindi line.
