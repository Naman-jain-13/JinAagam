# Pass 2 — व्याख्या spec (प्रमाणसंग्रह)

*Working document. Nothing here goes into the book.*

Pass 1 has transcribed, into `parts/`, the **संस्कृत मूल पाठ** in tagged segments `(T1)`, `(T2)` … (part 6, under a heading
containing "मूल") and the editor's printed one-word footnotes (part 11). **There is no printed Hindi and no छाया** — the
Hindi is entirely yours. Pass 1 text is finished and **must not be rewritten**.

You write parts **3, 4, 6-Hindi, 7, 7-क, 8, 9, 9-क, 10** into `addenda/s<key>.md` (`§30` → `addenda/s30.md`; keys of later batches are `§10010`, `§20010` … → `addenda/s10010.md`).
**Do not write parts 1, 2, 5** — Sanskrit is its own मूल here and nothing is composed beside it.

---

# What this book is for — keep it before you at every §

> **न्याय-ग्रन्थ का पाठक विद्वान् है, पर वह तर्क को *समझना* और *बरतना* दोनों चाहता है।** इसलिए हर अनुच्छेद केवल यह नहीं
> बताएगा कि "लेखक क्या कहते हैं", बल्कि (क) **हर तर्क, हेतु और खण्डन का युक्तिसंगत उद्देश्य** — कौन-सा दोष वह रोकता है, किस
> भ्रान्ति या अतिप्रसङ्ग से बचाता है, वाद में किस चाल का उत्तर है — और (ख) **उसे अपने चिन्तन, अध्ययन और वाद में कैसे
> *बरतें*** — कितनी बार, किस क्रम से, किस प्रश्न से — ताकि तर्क पढ़ा ही न जाए, **आत्मसात् हो**। और इन दोनों भागों के साथ **हर
> बिन्दु पर दृष्टान्त** हों।

| the reader asked for | where it lives |
|---|---|
| मूल पाठ, उसका हिन्दी अनुवाद | part 6 — Sanskrit (printed, by tag) with its Hindi (yours) |
| विशेष व्याख्या | part 7 |
| प्रत्येक तर्क/हेतु/खण्डन का **युक्तिसंगत उद्देश्य** (जैसे *इस हेतु से अमुक दोष का निराकरण होता है*), **दृष्टान्त सहित** | **part 7-क** |
| **practical** — तर्क को चिन्तन, अध्ययन और वाद में उतारने की techniques; कितनी बार चिन्तन, अभ्यास, चर्चा करें; **दृष्टान्त सहित** | **part 9-क** |

# The thing this book must get right — fidelity
The Hindi in part 6 **must not say anything the Sanskrit does not say.** An independent agent will read your Hindi against the
Sanskrit clause by clause. Method:

1. **You never retype the Sanskrit.** Write one Hindi line per `(Tn)` tag, **all tags, in order**:
   ```
   ## 6. टीका का हिन्दी अनुवाद
   (T1) <Hindi for T1>
   ```
   A segment that defeats you: still write its line, marked `[इस खण्ड का अर्थ सन्दिग्ध है: …]`. Never leave a hole.
2. **Syntax of a न्याय पङ्क्ति.** Identify at each segment: **पूर्वपक्षी का कथन / उत्तरपक्ष (अकलङ्कदेव का)**; the **अनुमान**
   (प्रतिज्ञा · हेतु · दृष्टान्त · उपनय · निगमन; पक्ष/साध्य/साधन); the **निग्रहस्थान / हेत्वाभास** being named (असिद्ध, विरुद्ध,
   अनैकान्तिक, अकिञ्चित्कर, कालात्ययापदिष्ट, प्रकरणसम); a **विकल्प-जाल** (`किम् … किं वा …`). Say who is speaking
   in the Hindi where it is not obvious (`नैयायिक कहते हैं —`, `इस पर जैन कहते हैं —`).
3. **Split every समास and give the relation** (तत्पुरुष / कर्मधारय / बहुव्रीहि / द्वन्द्व …), especially the abstract
   nouns in `-त्व`/`-ता` and `अ-`/`न-` negations: a न्याय sentence turns on whether the negative binds the member or the
   whole (`अप्रसिद्धावयवत्वम्` vs `प्रसिद्धावयवत्वाभावः`). Where two splits are defensible give the one the argument
   supports and record the other in part 10.
4. **Particles carry the argument:** `एव`, `अपि`, `तु`, `च`, `हि`, `इति`, `वा`, `नाम`, `खलु`, `नन्वेवम्`, `अथ`, `यदि … तर्हि`,
   `न चैतत्`. Never drop one. Count enumerations and the items of a विकल्प in Sanskrit and Hindi.
5. **A quoted verse ("तदुक्तं—") is quoted, not the author's:** say so (`जैसा कहा गया है —`), render it completely.
6. **Technical terms**: give the Hindi on first use with the Sanskrit in brackets (`हेतु (साधन)`, `साध्य`, `दृष्टान्त`,
   `निग्रहस्थान`, `पक्षधर्मत्व`, `सपक्षसत्त्व`, `विपक्षासत्त्व`), then keep it **consistent** across §.
7. **The sense test is doctrinal and logical:** a rendering that makes the author concede the very thesis he refutes is wrong
   however well it parses. Ask whether it could be true of the speaker.
8. **A suspect letter:** `म` for `प्र`, `ल` for `त्व`, `ष`/`प`, `ञ्च`/`श्च`. A split that invents a word or leaves a printed
   letter unexplained is wrong; prefer the reading that uses every printed letter, and note it in part 10.
9. **Printed footnotes (part 11)** are the editor's one-word glosses — use them to resolve pronouns and elided words.
   Do not copy them; the builder prints them.

# The other parts

### 3. अन्वय
For a **कारिका** only: its words in prose order (कर्ता/विशेषण/क्रिया), no added Sanskrit; a genuinely implied word in `( )`.
For a § that is pure वृत्ति: `यह अनुच्छेद गद्य है; पृथक् अन्वय आवश्यक नहीं।`

### 4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ)
For a कारिका: every पद of the अन्वय, one per line — `- **न** (न, अव्यय) = नहीं` — compounds split with `+`, grammatical form
where it decides the sense; close with `- **॥N॥** = कारिका-क्रमांक`. For pure वृत्ति: the **key terms only** (5–12 lines): the
technical words, split and glossed.

### 7. जैनागम / जैन-न्याय के अनुसार विस्तृत व्याख्या
4–7 bullets, each 100–200 words, each with a **bold** sub-heading: what this passage claims and why it stands here in the
argument; the doctrine/न्याय-सिद्धान्त behind it and the ग्रन्थ it rests on (प्रमाण/हेतु-लक्षण, अकलङ्क, धर्मकीर्ति, कुमारिल …
**cite only what you are sure of**); the opposing school stated fairly; cross-links (`देखें प्रमाणसंग्रह, प्रस्ताव 2, कारिका 5` (cite by the printed प्रस्ताव/कारिका, never by internal § key)); an honest limit where the
text is compressed. **न्याय is argument — keep the register of a reasoned walk-through, not paraphrase.**

### 7-क. तर्क का युक्तिसंगत उद्देश्य एवं दृष्टान्त
Heading exactly: `## 7-क. तर्क का युक्तिसंगत उद्देश्य एवं दृष्टान्त (प्रयोजन एवं दोष-निवृत्ति)`.

**Every हेतु, प्रतिज्ञा, दृष्टान्त, विकल्प-खण्डन, निग्रहस्थान-आरोप or definition the passage uses gets one bullet**, in this shape:

`- **<तर्क/पद>** — *उद्देश्य:* what this move is **for**. *युक्ति:* why it works — the reasoning a careful विद्वान् would accept. *निवृत्ति:* the **दोष / भ्रान्ति / अतिप्रसङ्ग / चाल** it blocks (हेत्वाभास, अनवस्था, अतिप्रसङ्ग, वाक्छल, अप्रतिपत्ति, अर्थान्तर …). *दृष्टान्त:* one concrete everyday or classroom example showing the move working — and, for a negative, the same case going wrong without it.`

- Take the *उद्देश्य* from the text where it states one (`तस्मात्…`, `इत्यर्थः`, `अतः…`) and say `ग्रन्थ के अनुसार`; where it is your own
  reasoning, say `व्याख्याकार का तर्क`. **Never present your reasoning as the ग्रन्थकार's.**
- A युक्ति must be a real argument, not a restatement. Weak: "हेतु साध्य को सिद्ध करता है।" Good: "पर्वत में अग्नि सिद्ध करनी हो तो
  प्रमाता को पहले यह दिखाना पड़ता है कि धूम और अग्नि का **अविनाभाव** है — वरना धूम पर अग्नि का दावा एक बेतुका सामान्यीकरण होगा; इसलिए
  हेतु का लक्षण अविनाभाव है, केवल त्रिरूपता नहीं।"
- If a passage is a mere transition or a quotation, give the purpose of *that* (why quote here; why this closing summary) — never blank.
  If truly nothing applies: `इस अनुच्छेद में कोई पृथक् तर्क-क्रिया नहीं; उसका प्रयोजन भाग 7 में आ चुका है।`

### 8. सरल उदाहरण
2–3 everyday analogies. State the दृष्टान्त, then the दार्ष्टान्तिक (what maps to what) and **where the analogy stops**. Build on the
text's own examples (घट-पट, धूम-अग्नि, कम्बल-नीलादि) first. If purely definitional: `इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।`

### 9. तुलनात्मक तालिका / चार्ट
One markdown table, 3–7 rows (दर्शन ↔ मान्यता; हेतु-दोष ↔ लक्षण ↔ उदाहरण; पक्ष ↔ उत्तर …). If none helps:
`इस अनुच्छेद हेतु तालिका आवश्यक नहीं।`

### 9-क. प्रयोग-विधि एवं अभ्यास (न्याय-अध्ययन में उतारने के सूत्र)
Heading exactly: `## 9-क. प्रयोग-विधि एवं अभ्यास (न्याय-अध्ययन में उतारने के सूत्र)`.

**Write this for a विद्यार्थी/विद्वान् who wants to *reason this way*, not merely understand it.** 3–6 bullets, each 40–100 words, **wherever
the text makes it possible**, each opening with a bold tag:

- **चिन्तन.** what to reflect on, when, and which question to put to oneself (`मेरा हेतु पक्ष में रहता है? सपक्ष में? विपक्ष में नहीं?`).
- **अभ्यास.** a concrete drill with its steps and **how many times** (e.g. `प्रतिदिन एक अनुमान को पाँच अङ्गों में तोड़ें; सात दिन`) so
  the pattern becomes automatic.
- **चर्चा.** a question to take to a गुरु / सहपाठी / वाद-गोष्ठी, and what a good answer looks like.
- **परीक्षण.** how you know the skill is taking root; the usual slip that spoils it.
- **दृष्टान्त.** *every bullet ends with a worked mini-example* — apply the technique to one small, concrete argument (an everyday
  or classroom one) so the reader sees the move done.

Rules: (1) tag every item **`[ग्रन्थ-सम्मत]`** (the text itself prescribes/states it, including a stated number or order) or **`[सुझाव]`**
(the व्याख्याकार's suggestion for practice). **Never present a suggested frequency as the ग्रन्थ's.** (2) Nothing against the text; no new
doctrine; a technique must serve the very argument the passage makes. (3) Never invent an authority; a drill is a drill. (4) Where the
passage is a pure definition, give the one practice it makes possible (memorise its शब्द-क्रम; apply it to three examples). If truly none:
`इस अनुच्छेद से कोई पृथक् अभ्यास-सूत्र नहीं निकलता; इसका उपयोग आगामी अनुच्छेदों के अभ्यास की पूर्व-पीठिका के रूप में है।`

### 10. सन्दर्भ एवं पाद-टिप्पणी
**1–3 one-line bullets, no blank line between them.** Source of a quoted verse (ग्रन्थ + number only if certain; `लगभग`/`सम्भवतः`
when unsure; nothing rather than a guess); one neutral line where a समास admits two splits, or a suspect reading was settled.
Otherwise: `मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।`

---

## Lessons from the audits of the sister books — avoid these faults
1. **Mark the source of every reason.** In 7-क an उद्देश्य the text states is `ग्रन्थ के अनुसार`; **every युक्ति you add is your own and carries `(व्याख्याकार का तर्क)`**, even when it follows a `ग्रन्थ के अनुसार` उद्देश्य in the same bullet.
2. **9-क tags are exactly `[ग्रन्थ-सम्मत]` or `[सुझाव]`** — never combined or invented; every bullet (including a closing note) carries one. A technique such as "कण्ठस्थ करें", a count, a duration or an order is `[सुझाव]` unless the text itself prescribes it. Never prescribe one number for all cases.
3. **Every drill and every दृष्टान्त must be logically sound:** a "test" must not itself commit the fallacy it names; a दृष्टान्त must illustrate *that* move, not a neighbouring one; do not use an example from one school to show another school's thesis unless you say so.
4. **Cross-references are exact.** Cite `प्रमाणसंग्रह, प्रस्ताव N, कारिका M` only for passages you have read in `parts/` and that say what you claim. The **कारिका numbers run on across the nine प्रस्ताव** (1–87); the `§ N` paragraph numbers are the editor's own and also run on. Never cite the internal `§<key>`.
5. **Part 3 (अन्वय) ends with the printed `॥N॥`** for a कारिका; for pure वृत्ति write the standard one-liner. Part 4 lists only words that are in the text.
6. **Counts and lists:** if the text lists items, list them all; do not say "four" and name three. Keep प्राप्यकारी/अप्राप्यकारी, साध्य/साधन, प्रतिज्ञा/हेतु straight.
7. **Hard doctrinal questions the text itself does not settle are said to be open** — do not resolve them; do not state a school's view as the author's unless the text does.
8. **Variant readings in `( )` / `[ ]`:** translate the main reading; if a variant changes the sense, note it in part 10 in one line. A [अस्पष्ट] stretch is rendered only as far as legible and marked `[अस्पष्ट पाठ के कारण यहाँ अनुवाद अपूर्ण]` — never guessed.

## Before writing a §, read
the § in `parts/` (every `(Tn)`), the §§ before and after (the argument carries across), and for the first § the preceding §.

## Context
**प्रमाणसंग्रह**, श्रीमद्भट्टाकलङ्कदेव's न्याय-ग्रन्थ in **nine प्रस्ताव**: कारिकाएँ with the author's own वृत्ति (the editor numbers the वृत्ति paragraphs `§ १.` …).
It gathers Akalanka's mature theory of **प्रमाण**: the two प्रमाण (प्रत्यक्ष and परोक्ष), the three kinds of श्रुत; स्मृति, प्रत्यभिज्ञा, तर्क as
प्रमाण; अनुमान with the single-mark हेतु **अन्यथानुपपत्ति / अविनाभाव** against the Buddhist त्रिरूप; the **हेत्वाभास**; वाद, जय-पराजय, निग्रह; the
**अनेकान्त** nature of the object; **सर्वज्ञसिद्धि**; **नय** and **प्रवचन**. Do not assert more than the passage says; where the text is
compressed (the वृत्ति often just glosses the कारिका), say so honestly in part 7. Sibling texts: पत्रपरीक्षा, आप्तपरीक्षा, प्रमाणपरीक्षा.
The editor's `( )` and `[ ]` inside the Sanskrit are **variant readings / emendations**: translate the main reading, mention a
meaning-changing variant in part 10 in one line. `॥छ॥` is the scribe's closing mark, not content.

## Style — binding
- शास्त्रीय, clear हिन्दी. English digits in your prose; Devanagari digits only inside quoted Sanskrit.
- **Never write any sect name** anywhere.
- **Jain आचार्य never named bare:** `श्री विद्यानन्द स्वामी`, `श्री अकलङ्कदेव`, `आचार्य श्री समन्तभद्र`, `श्री कुमारनन्दि भट्टारक`. Honorific
  **at source**. Non-Jain authors plain (`अक्षपाद`, `धर्मकीर्ति`, `कुमारिल`).
- **No working-process language** (बैच, सत्र, file names, scan pages, उपयोगकर्ता, other agents).
- **Never fabricate** a citation or doctrine. "लगभग"/"सम्भवतः" where unsure; silence where you do not know.

## Writing the files
One § at a time, immediately: `addenda/s30.md`. Heading order: `## 3.` · `## 4.` · `## 6. टीका का हिन्दी अनुवाद` · `## 7.` · `## 7-क.` ·
`## 8.` · `## 9.` · `## 9-क.` · `## 10.`.

## Report back (under 250 words)
§ keys completed; every `(Tn)` you could not construe (named); every समास split against the obvious reading and why; every citation you
wanted but could not verify; every 7-क/9-क point you were unsure of; and confirmation that every § has a file and every `(Tn)` has a Hindi line.
