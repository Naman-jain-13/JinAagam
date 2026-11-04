# Pass 2 — व्याख्या spec (प्रतिक्रमण-ग्रन्थत्रयी, v2 — मूलाचार-पद्धति)

*Working document. Nothing here goes into the book.*

# INDEPENDENCE — the rule above all others (the reader's explicit instruction)

> **इस पुस्तक में किसी मौजूदा हिन्दी अनुवाद का प्रभाव नहीं होना चाहिए, और न किसी अनुवादक/सम्पादक/मुनि/माताजी का नाम। अनुवाद पूरी तरह आपका स्वतन्त्र है — केवल प्राकृत सूत्र और श्री प्रभाचन्द्राचार्य की संस्कृत टीका से।**

Your **only** sources are the files in the source folder named in your task (`src\s<key>.md`, made by `make_src.py`): the
**प्राकृत सूत्र / दण्डक** as printed in the book's परिशिष्ट (part 1), **श्री प्रभाचन्द्राचार्य's संस्कृत टीका** in tagged segments
`(T1)`, `(T2)` … (part 6, under a heading containing "मूल"), and the printed variant footnotes (part 11). **Do not open `parts/`, `img/`,
`mool/`, `_v1/`, `verify/`, or any other file in the project** — `mool/` and `img/` carry the printed Hindi translation of this very text,
and `_v1/` carries an earlier व्याख्या that this edition replaces. **Do not consult any existing Hindi rendering from memory as a model.** If you
are unsure of a Sanskrit reading, say so (`सन्दिग्ध`) — do not reach for a printed translation. **Never mention** a printed/मुद्रित हिन्दी, an
editor, a translator, a मुनि or माताजी, or "the edition's" translation anywhere in what you write; the book contains no such reference.
(Mentions of a footnote's *variant reading*, such as "एक प्रति में अन्यथा पाठ है", are fine.)

Each file's **first line** is `शीर्षक: <one Hindi line, 8–16 words, saying what this सूत्र/खण्ड establishes — written from the Sanskrit alone>`.
Its **second line** is `सन्दर्भ-संकेत: <ग्रन्थ>, मुद्रित पृष्ठ <as in the src header>; <which दण्डक/प्रकरण of the प्रतिक्रमण this is and its opening
words, e.g. "दैवसिक प्रतिक्रमण का पीठिका-दण्डक — 'इच्छामि भंते आलोचेदुं …'">; <a certain parallel in the आगम, only if certain>` — it is printed at the
top of the § (the reader asked for references at the top as well). Then you write parts **2, 3, 4, 5, 6-Hindi, 7, 7-क, 8, 9, 9-क, 10** into
`addenda/s<key>.md` (`§30` → `addenda/s30.md`). **Part 5 is yours**: the Hindi rendering of the सूत्र itself (see below). The book carries
no other सूत्र-अनुवाद.

---

# The aim of this book — give it to yourself before every §

> **प्रतिक्रमण साधु का नित्य आवश्यक है — व्रत, समिति, गुप्ति, शील आदि में प्रमाद से लगे दोषों की आलोचना करके उनसे लौटना।
> इसका पाठक साधु है (और आर्यिका, ऐलक, क्षुल्लक, विद्वान् श्रावक)। इसलिए हर सूत्र का व्याख्यान केवल "यह क्या कहता है" पर नहीं
> रुकेगा — वह यह भी बताएगा कि इस सूत्र को प्रतिक्रमण-काल में और दिन भर कैसे जिया जाए, और जो क्रिया/दोष-निवृत्ति इसमें कही
> गई है उसका युक्तिसंगत (तर्कसंगत) उद्देश्य क्या है।**

The reader asked for each सूत्र to be treated in this order, and the parts below map onto it:

| the reader asked for | where it lives |
|---|---|
| मूल सूत्र, उसका अर्थ | part 1 — प्राकृत सूत्र (printed) · **part 5 — सूत्र का हिन्दी अनुवाद (yours)** · parts 2, 3, 4 — छाया, अन्वय, अन्वयार्थ (yours) |
| टीका, उसका अर्थ | part 6 — Sanskrit टीका (printed) with its Hindi (yours) |
| विशेष व्याख्या | part 7 |
| ग्रन्थ में जो प्रत्येक क्रिया बताई, उसका **युक्ति (तर्क) संगत उद्देश्य** भी बताएँ — जैसे *अमुक क्रिया से अमुक कषाय की निवृत्ति होती है* | **part 7-क** |
| आचार-ग्रन्थ होने से साधु के लिए practical रूप — **कुछ techniques, जहाँ भी possible हो, कि इस सूत्र की बात को जीवन में कैसे उतारें; कितनी बार इस एक क्रिया का अलग से चिन्तन, practice, discussion आदि करें ताकि उस आचरण को अच्छे से अच्छे रूप में समझें और practically apply कर सकें** | **part 9-क** |

---

# The thing this book must get right — fidelity

The Hindi in part 6 **must not say anything the Sanskrit टीका does not say.** An independent agent will afterwards read your Hindi against
the Sanskrit clause by clause and report every addition, omission and shift of sense. Write as though that audit will happen, because it will.

## Part 6 — the Sanskrit टीका rendered into Hindi

**You never retype the Sanskrit.** It is in the source, tagged `(T1)`, `(T2)`, … You write a Hindi line against each tag, using **exactly the
tags the source uses, all of them, in order**:

```
## 6. टीका का हिन्दी अनुवाद
(T1) <Hindi for segment T1>
(T2) <Hindi for segment T2>
```

If a segment defeats you, still write its line and say so in it: `[इस खण्ड का अर्थ सन्दिग्ध है: …]` — a missing tag is a hole the reader cannot see.
A segment that is only a heading or a closing line (`**प्रतिक्रमणग्रन्थत्रयी**`, `॥ इति निषीधिकादण्डकविवरणम् ॥`, `॥ श्री पार्श्वनाथाय नमः ॥`) still gets
its line — a plain Hindi rendering of what it says.

Method, in order:

1. **Separate the quoted प्राकृत from the Sanskrit.** The टीका quotes the सूत्र's words — set in bold (`**…**`) in the source — and glosses each,
   usually with no dash: `**भंते** भगवन्।` is the प्राकृत word `भंते`, then its Sanskrit gloss `भगवन्`. Render as a gloss:
   `'भंते' — हे भगवन्।` Never treat the quoted प्राकृत as a Sanskrit sentence, and never translate the प्राकृत word separately from the gloss
   the टीका gives it. A bold phrase may also be a whole verse or a heading; read it in context.
2. **Render questions as questions, each joined to its own answer.** `किम्`, `कथम्`, `कस्मै`, `क्व`, `किं कर्तुम्`, `कथम्भूतम्`, `किंविशिष्टम्`,
   `इति चेत्`, `ननु`. The टीका's standard frame is `इच्छामि अभिलषामि। किं कर्तुम्? आलोचेदुं आलोचयितुम्।` — the question asks about the verb
   or noun just glossed; the gender/number/case of `कथम्भूतम्/ताय/ते` tell you which noun it qualifies — find the noun it agrees with.
3. **Split every समास and say how the members relate** (तत्पुरुष / कर्मधारय / बहुव्रीहि / द्वन्द्व …). Show the split in the Hindi where it is not
   obvious. Where two splits are defensible, give the one the doctrine and the सूत्र support and record the other in part 10.
4. **Keep the particles** — `एव` (ही), `अपि` (भी), `तु`, `च`, `हि`, `किल`, `इति`, `वा` (अथवा). Dropping `एव` turns an exclusive claim into a loose one.
5. **Carry the case of the final member** of a compound — it governs the whole compound's role. Prakrit `-ए`/`-सु` endings of a list of दोष
   (`इरियासमिदीए`, `बावीसाए परीसहेसु`) are mostly locative "in / with regard to"; the टीका's gloss (`तस्याम्`, `तेषु`) fixes it — follow the gloss.
6. **Account for every word** — re-read the Sanskrit once more after writing the Hindi.
7. **The test that catches a wrong split is doctrinal, not grammatical:** a reading that contradicts the very सूत्र it explains is wrong, however
   well it parses. Ask whether it could be true of the subject.
8. **If a split only works by reading `म` as something else, try `प्र` first; `ल` may stand for `त्व`.** A split that invents vocabulary, or leaves a
   printed letter unexplained, is wrong. A wrong split leaks small additions into the Hindi, and those are the hardest errors to see later.
9. **A list, a numbered set or an enumeration in the टीका must come out complete** — the प्रतिक्रमण is built of counted sets (पाँच महाव्रत, पच्चीस
   क्रिया, बाईस परीषह, अठारह हज़ार शील, तैंतीस अत्यासादना …). Count the items in Sanskrit, count them in Hindi; never say "पच्चीस" and name twenty.
10. **Quoted verses** (`तदुक्तं — ‘‘…’’`, `गाथा—`) are rendered completely, verse by verse; name the source only if the टीका names it.
11. The source keeps the print exactly — `[अस्पष्ट]`, an editor's `( )` alternative, an odd spelling, a `(?)`. Translate what is printed; where
    the print is doubtful say `सन्दिग्ध` in part 10. Never quietly translate a "corrected" reading.

### Division headings and colophons are structural
A line that names or closes a division of the book (`प्रतिक्रमणपीठिकादण्डकविवरणम्`, `इति गणधरवलयाख्यः …`, `इति-श्रीगौतमस्वामि-विरचित-…
समाप्तः`, the टीकाकार's opening and closing verses) is translated in part 6 like any segment, but it is about the *book*: keep it out of parts 3,
4 and out of the भावार्थ; part 7 may note once which division is opening or closing.

## The other parts

### 2. संस्कृत छाया
Heading exactly `## 2. संस्कृत छाया`. **This edition does not print a छाया of the सूत्र.** You compose one; the book says once, in its भूमिका,
that the छाया is the व्याख्याकार's (so **never** write "व्याख्याकार-कृत" or any note in the § itself — the reader asked for that). Compose it
**from the टीका's own gloss**: each प्राकृत word's Sanskrit equivalent as श्री प्रभाचन्द्राचार्य gives it (`भंते` → `भदन्त`, `आलोचेदुं` →
`आलोचयितुम्`, `दिवसियम्हि` → `दैवसिके`), in the सूत्र's own word order and with its own breaks (`।`, `॥`), keeping the editor's printed `( )`
alternatives as `( )`. Where the टीका does not fix a word, use its standard Sanskrit equivalent — never an invented sense. It is printed in small type.
**If part 1 is already Sanskrit** (the मङ्गल-श्लोक `श्रीमते वर्धमानाय…`, the स्तुति-पद्य `ये लोकेऽष्टसहस्र…`, `व्रतसमुदयमूलः…`) or **there is no part 1**,
omit part 2 entirely (no heading).

### 5. सूत्र का हिन्दी अनुवाद
Heading exactly `## 5. सूत्र का हिन्दी अनुवाद`. **Your own rendering of what the प्राकृत सूत्र says**, as one flowing Hindi passage that follows the
सूत्र in order, as long as the सूत्र needs (a five-word दण्डक-पद: one line; a long दण्डक: a paragraph). Use the टीका only to fix the sense of a word,
**never to add matter the सूत्र does not carry** — the explaining belongs to parts 6–7. No भावार्थ, no examples, no bracketed Sanskrit lemmas.
Where the सूत्र is a bare list (`कोहेण वा। माणेण वा। …`), the Hindi is the list. Keep the सूत्र's particles. It is printed straight after the छाया,
so it must stand alone and read as Hindi. **No part 1 → no part 5.**

### 3. अन्वय
The words **of the प्राकृत सूत्र**, as printed, rearranged into straight prose order — कर्ता, कर्म/विशेषण, क्रिया; for a list-दण्डक, the governing
verb supplied once in `( )` (`(आलोचेदुं इच्छामि)`). Do not substitute Sanskrit; a genuinely implied word goes in `( )`. For a very long दण्डक
(over ~40 पद) you may give the अन्वय of its frame and say `(शेष पद इसी क्रम से)` — but part 4 still covers every पद. No part 1 → omit.

### 4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ)
Every पद of the सूत्र, in order, one per line: `- **दिवसियम्हि** (दैवसिके, सप्तमी ए.व.) = दिन-सम्बन्धी (दोष) के विषय में`. Sanskrit in `( )` follows
your part 2 / the टीका's gloss. Split compounds with `+`. A closing verse number `॥1॥` → `- **॥1॥** = श्लोक-क्रमांक`. No part 1 → omit.

### 7. जैनागम के अनुसार विस्तृत व्याख्या
4–7 bullets, each 100–200 words, each with a bold sub-heading: what this सूत्र establishes and why it stands here in the प्रतिक्रमण; the doctrine
behind it and the सूत्र / ग्रन्थ it rests on (तत्त्वार्थसूत्र, मूलाचार, भगवती आराधना, षट्खण्डागम … — only what you are sure of); the opposing
position stated fairly where there is one; cross-links (`देखें § 30`); an honest limit where the सूत्र is compressed or the टीका supplies what the सूत्र
does not. **The प्रतिक्रमण is a साधु-आचार text, not a न्याय text:** keep that register — concrete, about what a साधु does, what दोष is meant, and why
it is confessed.

### 7-क. क्रिया का युक्तिसंगत उद्देश्य
Heading exactly: `## 7-क. क्रिया का युक्तिसंगत उद्देश्य (प्रयोजन एवं कषाय-निवृत्ति)`.

**Every क्रिया, व्रत, समिति, गुप्ति, नियम, भावना or दोष-निवृत्ति the सूत्र names gets one bullet** (for a long list-दण्डक, group the items as the
सूत्र groups them — e.g. one bullet for the five समिति — but leave none out), in this shape:

`- **<क्रिया>** — *उद्देश्य:* … । *युक्ति:* (why it achieves this — the reasoning a thoughtful साधु would accept) … । *निवृत्ति:* the कषाय / दोष / आस्रव / अशुभ-भाव it curbs (क्रोध, मान, माया, लोभ; राग, द्वेष; हिंसा; प्रमाद …) … ।`

- Take the *उद्देश्य* from the टीका wherever it states one (`… अर्थम्`, `… निमित्तम्`, `… हेतोः`, `विशुद्धिं कर्तुम्`) and say so (`टीका के अनुसार`).
  Where it is your own reasoning from the doctrine, say so (`व्याख्याकार का तर्क`). **Never present your own युक्ति as आगम-वचन.**
- **The प्रतिक्रमण's own act needs its purpose too:** आलोचना (दोष को गुरु/स्वयं के सामने यथावत् कहना), निन्दा, गर्हा, प्रतिक्रमण ("मिच्छा मे
  दुक्कडं"), प्रत्याख्यान, कायोत्सर्ग, भक्ति (सिद्ध-, वीर-, चारित्र-, चतुर्विंशति-तीर्थंकर-भक्ति). Say what each removes and *how*.
- A युक्ति must be a real argument, not a restatement. Weak: "अहिंसा से हिंसा छूटती है।" Good: "प्राणिपीड़ा का मूल कारण प्रमाद-युक्त योग है
  (तत्त्वार्थसूत्र 7.13 — प्रमत्तयोगात्प्राणव्यपरोपणं हिंसा); जब दिन के अन्त में ईर्यापथ के प्रत्येक दोष को नाम लेकर स्मरण किया जाता है तो
  अगले दिन वही प्रमाद पहचाना जाता है, इसलिए हिंसा से पहले उसका कारण ही रुकता है।"
- Name the specific कषाय where the doctrine supports it, and say *how* the क्रिया curbs it (mechanism, not label). Nothing is to be forced:
  if no कषाय is the natural target, say what the real target is.
- If the सूत्र names no क्रिया (a मङ्गल, a नमस्कार to ऋद्धिधारी, a heading), still give the purpose of what it **does**: why a प्रतिक्रमण opens with
  नमस्कार; what a साधु gains by counting the दोष-स्थान. Never leave it blank. If truly nothing applies:
  `इस सूत्र में कोई पृथक् क्रिया नहीं कही गई; उसका प्रयोजन ऊपर भाग 7 में आ चुका है।`

### 8. सरल उदाहरण
2–3 everyday analogies a श्रावक can follow. State the दृष्टान्त, then the दार्ष्टान्तिक — what maps to what — and **where the analogy stops**.
Build on the टीका's own example first (it tells several कथा: मातंगी, मल्लि, चण्डिम … — use them as the टीका tells them, adding nothing).
If purely enumerative: `इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।`

### 9. तुलनात्मक तालिका / चार्ट
One markdown table, 3–7 rows (a counted set may run longer: one row per item), of whatever kind the सूत्र calls for. If none helps:
`इस अनुच्छेद हेतु तालिका आवश्यक नहीं।`

### 9-क. साधु-जीवन में उतारने की विधि
Heading exactly: `## 9-क. आचरण-विधि एवं अभ्यास (साधु-जीवन में उतारने के सूत्र)`.

**This is the part the reader values most. Write it for a साधु who wants to *do* this, not merely understand it.** 3–6 bullets, each 40–100 words,
drawn from the following, **wherever the सूत्र makes it possible**:

- **चिन्तन** — what to reflect on, at what time (दैवसिक प्रतिक्रमण-काल / रात्रिक प्रतिक्रमण-काल / सामायिक / आहार से पहले-बाद / विहार के बाद),
  and what question to ask oneself (`आज ईर्यापथ में कहाँ बिना देखे पैर पड़ा?`).
- **अभ्यास** — a concrete drill: the steps, and **how many times** (e.g. `प्रत्येक प्रतिक्रमण में इस पद पर रुककर एक श्वास`, `एक सप्ताह तक केवल इसी
  एक दोष-स्थान पर ध्यान`) so that the confession becomes recognition, not recitation.
- **चर्चा** — a question to discuss with गुरु / सहसाधु / संघ, and what a good answer would look like.
- **परीक्षण / संकेत** — how to tell the practice is taking root (a symptom, a lapse to watch for); and the common mistake that spoils it
  (the commonest for प्रतिक्रमण: पाठ का यन्त्रवत् उच्चारण, दोष का नाम लेकर भी उसे न पहचानना).
- **परिस्थिति-विशेष** — one line on the hard case (illness, travel, a missed प्रतिक्रमण-काल, a crowded town) where this is tested.

Rules:
1. Each bullet starts with its tag in bold — `**चिन्तन.**`, `**अभ्यास.**`, `**चर्चा.**`, `**परीक्षण.**`, `**परिस्थिति.**`.
2. **Honesty about the source.** Put `[आगम-सम्मत]` after anything the टीका or the आगम states (including a stated number of times, an hour, an order —
   e.g. दैवसिक and रात्रिक प्रतिक्रमण, the पाक्षिक/चातुर्मासिक/सांवत्सरिक cycle the ग्रन्थ itself names). Put `[सुझाव]` after anything that is the
   व्याख्याकार's suggestion for practice. **Never present a suggested frequency as आगम-विधान.** If the आगम gives no number, say so and offer a sensible
   one as `[सुझाव]`.
3. **Nothing against the आगम and nothing the टीका does not license as conduct.** A technique must serve the very क्रिया or दोष-निवृत्ति the सूत्र names —
   never invent a new vow, a new प्रायश्चित्त or a new rule, and never soften one. **प्रायश्चित्त is the गुरु's to give** — never prescribe one.
4. **Do not invent an authority.** A drill is a drill; it is not "as the शास्त्र says" unless it does.
5. Where the सूत्र makes no practical technique possible (a pure मङ्गल or a heading), still give the one practice it makes possible — e.g. how a साधु
   holds the नमस्कार in mind while reciting it, how a counted set is committed to memory. If truly none:
   `इस सूत्र से कोई पृथक् अभ्यास-सूत्र नहीं निकलता; इसका उपयोग आगामी सूत्रों के अभ्यास की पूर्व-पीठिका के रूप में है।`
6. **The प्रतिक्रमण is the साधु's आवश्यक; 9-क addresses the साधु.** Where the आगम genuinely supports it for a श्रावक (सामायिक, the श्रावक's अणुव्रत and
   प्रतिमा named in the दण्डक, a श्रावक's own प्रतिक्रमण), one closing line may say so — tagged like every other line.

### 10. सन्दर्भ एवं पाद-टिप्पणी
**1 to 3 one-line bullets, no blank line between them.** Printed at dictionary size. Only: the source of a verse quoted in the टीका (ग्रन्थ and number —
only if you are certain; `लगभग` / `सम्भवतः` when unsure; nothing at all rather than a guess); a one-line note where a समास admits two splits, or where a
worn/suspect reading in the print forced a choice (`सन्दिग्ध`), or where a printed variant in part 11 would change the sense. Otherwise:
`मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।` (Part 11's variants are already printed in the book — do not copy them.)

---

## Lessons from earlier books in this series (मूलाचार अधिकार 1–4 and the v1 of this book) — avoid these faults
1. **Mark the source of every reason.** In 7-क, an उद्देश्य the टीका states gets `टीका के अनुसार`; **every युक्ति you add is your own and must carry
   `(व्याख्याकार का तर्क)`**, even when it follows a `टीका के अनुसार` उद्देश्य in the same bullet. Never let your reasoning read as the टीका's.
2. **9-क tags are exactly `[आगम-सम्मत]` or `[सुझाव]`** — one tag per sentence-group, never a combined or invented tag; **every bullet, including a closing
   श्रावक line and "आम भूल" remarks, carries a tag.** A frequency, count, duration, hour or order is `[सुझाव]` unless the टीका states it.
   **Never prescribe one number for all cases** (e.g. one उच्छ्वास count for every कायोत्सर्ग — the आगम gives different counts for different occasions).
3. **Hard cases go to the गुरु, unresolved:** illness, travel, a missed प्रतिक्रमण, which प्रायश्चित्त a दोष needs, "may I shorten the दण्डक". Say so; do not
   settle them. Never soften a rule.
4. **Cross-references must be exact and verifiable.** Cite `§ N` only if you have read that § in the source folder and it says what you claim. **दैवसिक
   (evening) प्रतिक्रमण reviews *the day*; रात्रिक (morning) reviews *the night*; पाक्षिक/चातुर्मासिक/सांवत्सरिक the longer periods** — do not mix them up.
5. **Part 3 (अन्वय) uses only the सूत्र's own words; part 2 (छाया) keeps the सूत्र's breaks and correct sandhi.**
6. **Counts:** if the टीका lists items, list them all. Keep नोकषाय vs कषाय, अतिक्रम / व्यतिक्रम / अतिचार / अनाचार, आभोग / अनाभोग straight — the टीका
   defines each; follow its definitions, not a general memory.
7. Where the टीका uses `च` for `एव` or `वा` for "and" (a recurring idiom), read the sense against the सूत्र and the doctrine, not the particle alone.
8. **The printed text governs.** If the Sanskrit looks wrong, translate what is printed and flag it in part 10 — an earlier agent in this series twice
   "fixed" the print to fit the sense and reversed the book's meaning.
9. **No working-process language** and no name of any modern translator/editor/मुनि/माताजी — anywhere, including part 10.

## Known source quirk
In a few places a footnote mark `[n]` in the टीका sits in the § *after* the one whose part 11 carries that note (e.g. §1520 vs §1500, §1640 vs §1630) — the printed page puts them so. If a mark in your § has no matching note, look in the previous §'s src file and mention the variant there; never move text between §.

## Before writing a §, read
1. the § itself in `src\` — all of it, especially every `(Tn)` segment;
2. the §§ immediately before and after, so cross-links and "why here" are real (a § may carry no part 1 because it only continues the previous
   § 's टीका — then its parts 2–5 are omitted, and part 7 says how it continues the previous सूत्र);
3. for the first § of your range, the preceding § in full — the टीका often carries one explanation across §.

## Context — where the ग्रन्थ stands
**प्रतिक्रमण-ग्रन्थत्रयी**: the प्राकृत प्रतिक्रमण-सूत्र (गद्य दण्डक, with some गाथा and Sanskrit स्तुति-पद्य) ascribed to **श्री गौतमस्वामी** (गणधर),
with **श्री प्रभाचन्द्राचार्य's संस्कृत टीका**, which glosses the सूत्र word by word (`**पद** gloss। किं कर्तुम्? …`), defines technical sets, and
tells illustrative कथा. Three ग्रन्थ, 229 अनुच्छेद (§ key = अनुच्छेद × 10):
- **ग्रन्थ 1 — दैवसिक-रात्रिक प्रतिक्रमण (§10–§1050)**: टीकाकार's opening verse and the मङ्गल `श्रीमते वर्धमानाय`; the आलोचना-दण्डक `इच्छामि भंते
  आलोचेदुं दिवसियम्हि` (महाव्रत, समिति, गुप्ति, कषाय-कारण, the counted sets from 1 to 33); the प्रतिक्रमण-पीठिका (निषीधिका-दण्डक, `णमोत्थु दे`, the
  मङ्गल-सम्बोधन); the day's दोष (ईर्यापथ, एषणा, स्वप्न, विकथा, ध्यान, संज्ञा, लेश्या …) each closing `तस्स मिच्छा मे दुक्कडं`; the counted दोष-स्थान
  `एक्के भावे … तेत्तीसाए अच्चासणदाए`; गर्हा, the praise of the निर्ग्रन्थ-प्रवचन (`इच्छामि भंते इमं णिग्गंथं पावयणं`), the oath `समणोमि संजदोमि`;
  कायोत्सर्ग, वीर-भक्ति, चारित्र-भक्ति, धर्म-स्तुति, चतुर्विंशति-तीर्थंकर-स्तुति; the टीकाकार's closing verse.
- **ग्रन्थ 2 — बृहत्प्रतिक्रमण (§1060–§1880)**: the गणधरवलय-मङ्गल (`णमो जिणाणं, णमो ओहिजिणाणं …` — ऋद्धिधारी महर्षियों को नमस्कार), the सुधर्म-सम्बोधन,
  the five महाव्रत and रात्रिभोजन-विरमण each with its दण्डक and भावना, the चूलिका, क्षमायाचना (`एसो पडिक्कमणविहि …`), the अत्यासादना of the मूल-पद, the
  अतिचार-गणना.
- **ग्रन्थ 3 — आलोचना (§1890–§2320)**: आष्टमिक / पाक्षिक / चातुर्मासिक / सांवत्सरिक आलोचना; the पञ्चाचार — ज्ञान, दर्शन, तप, वीर्य, चारित्र (जीव-निकाय,
  महाव्रत, समिति, गुप्ति) — each `परिहाविदो … तस्स मिच्छा मे दुक्कडं`; the counted अतिचार-स्थान; the टीकाकार's closing verse.
**Part 1 comes from the book's परिशिष्ट**, where the editor printed the whole मूल पाठ continuously (often word by word between `॥`, with variant
words in `( )`); the टीका quotes the same words in bold. Where the two differ in spelling (`छठ्ठं` / `छट्ठं`), the टीका's form is what it glosses — say so in
part 10 if it matters; never alter either. Do not assert more than the टीका says; where it gives a list, give the whole list.

## Style — binding
- शास्त्रीय, clear हिन्दी. English digits in your prose — Devanagari digits **only** inside quoted मूल / टीका, where `॥१॥` stays as printed.
- **Never write any sect name** (दिगम्बर / श्वेताम्बर / बीसपंथ / तेरापंथ or any sub-sect label) anywhere, for any reason. Differences in neutral words.
- **Jain आचार्य are never named bare:** `श्री गौतमस्वामी` (गणधर), `श्री प्रभाचन्द्राचार्य`, `श्री कुन्दकुन्द स्वामी`, `श्री वट्टकेराचार्य`, `श्री शिवार्य`,
  `श्री पूज्यपाद स्वामी`, `श्री उमास्वामी`, `श्री अकलङ्कदेव`, `श्री समन्तभद्र स्वामी`. Write the honorific **at source**, including when a case-ending follows.
  Non-Jain opponents are plain.
- **No working-process language anywhere**: no "बैच", "इस सत्र", file names, scan/pdf pages, "स्लाइस", "उपयोगकर्ता", no mention of other agents or of how
  the book was made. "मुद्रित पृष्ठ" references are fine.
- **तत्त्वार्थसूत्र: use the सर्वार्थसिद्धि recension.** 7.13 प्रमत्तयोगात्प्राणव्यपरोपणं हिंसा · 9.2 स गुप्तिसमितिधर्मानुप्रेक्षापरीषहजयचारित्रैः ·
  9.5 ईर्याभाषैषणादाननिक्षेपोत्सर्गाः समितयः. When unsure of a number, cite the सूत्र text and the अध्याय alone (`../_shared/citation_rules.md`).
- **Never fabricate** a citation, a verse number or a doctrine. "लगभग" / "सम्भवतः" where unsure; silence where you do not know. This book will be cited.
- No backticks in the files.

## Writing the files
**Write each § as its own file, immediately, one at a time** — `addenda/s30.md` for `§30`. Do not accumulate several and write at the end.

Order in each file: `शीर्षक:` line · `सन्दर्भ-संकेत:` line · `## 2.` · `## 3.` · `## 4.` · `## 5. सूत्र का हिन्दी अनुवाद` · `## 6. टीका का हिन्दी अनुवाद` ·
`## 7.` · `## 7-क.` · `## 8.` · `## 9.` · `## 9-क.` · `## 10.` (2–5 only when the § has a part 1; 2 only when part 1 is प्राकृत).

## Report back (under 250 words)
The § keys completed; every समास you split against the obvious reading and why; any `(Tn)` segment whose Sanskrit you could not construe, named
explicitly; any print reading you flagged `सन्दिग्ध`; any citation you wanted but could not verify; any part 7-क / 9-क point you were unsure of; and
confirmation that every § in your range has a file and every `(Tn)` tag has a Hindi line.
