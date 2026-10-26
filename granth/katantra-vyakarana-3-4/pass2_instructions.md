# Pass 2 — व्याख्या spec (कातन्त्र, दुर्गसिंह-वृत्ति: अध्याय 3–4)

*Working document. Nothing here goes into the book.*

Pass 1 has transcribed, into `src/`, one file per सूत्र: the **सूत्र and Durgasimha's वृत्ति** in tagged segments `(T1)`, `(T2)` … (under a heading
containing "मूल"). `(T1)` is normally the सूत्र itself (with its `॥N॥`); a pāda/adhyāya heading or an opening verse may come first; the last segment may be a pāda colophon.
**The edition has no Hindi; the Hindi is entirely yours, from the Sanskrit in `src/` alone. You must never open `parts/`, `mool/`, `img/` or any scan.** Pass 1 text is finished and **must not be rewritten**.

You write parts **6-Hindi, 7, 7-क, 8, 9, 9-क, 10** into `addenda/s<key>.md` (`§150010` → `addenda/s150010.md`; keys run §150010 … §420120).
**Do not write parts 1–5** — Sanskrit is its own मूल and the builder prints no अन्वय/अन्वयार्थ/छाया. Do not write part 11 (it is empty in this book).

---

# What this book is for — keep it before you at every §

> **पाठक एक विद्यार्थी/जिज्ञासु है जो संस्कृत व्याकरण को *समझना* और *बरतना* चाहता है।** इसलिए हर सूत्र की व्याख्या केवल "सूत्र का अर्थ" नहीं होगी:
> (क) **सूत्र क्या विधान करता है, कब लगता है, कब नहीं लगता, और वृत्ति के उदाहरणों पर कैसे लगता है** — कदम-दर-कदम **सिद्धि-प्रक्रिया** के साथ; और
> (ख) **इसे अपने अध्ययन, लेखन और अभ्यास में कैसे बरतें** — कितने रूप, किस क्रम से, किस भूल से बचकर — हर बिन्दु पर **दृष्टान्त**।

| the reader asked for | where it lives |
|---|---|
| सूत्र + वृत्ति का मूल, उसका हिन्दी अनुवाद | part 6 — Sanskrit (printed, by tag) with its Hindi (yours) |
| सूत्र की विस्तृत व्याख्या (पदच्छेद, अर्थ, अनुवृत्ति, प्रवृत्ति, पूर्वापर-सम्बन्ध) | part 7 |
| **सूत्र का प्रयोजन एवं सिद्धि-प्रक्रिया** — हर उदाहरण पर सूत्र कैसे लगता है, `इति किम्`/`किमर्थम्` का उत्तर, दोष-निवारण | **part 7-क** |
| **practical** — रूप साधने के अभ्यास, कितनी बार, कैसे परखें, **दृष्टान्त सहित** | **part 9-क** |

# The thing this book must get right — fidelity
The Hindi in part 6 **must not say anything the Sanskrit does not say**, and must not leave out anything it does. Method:

1. **You never retype the Sanskrit.** Write one Hindi line per `(Tn)` tag, **all tags, in order**:
   ```
   ## 6. टीका का हिन्दी अनुवाद
   (T1) <Hindi for T1>
   ```
   For `(T1)` = the सूत्र: give its **सूत्रार्थ** (not a word-list): e.g. `सिद्धो वर्णसमाम्नायः ॥१॥` → «वर्णों का समाम्नाय (पाठ-क्रम) सिद्ध है।» A segment that defeats you:
   still write its line, marked `[इस खण्ड का अर्थ सन्दिग्ध है: …]`. Never leave a hole.
2. **A सूत्र is terse; its words are in सूत्र-रीति.** Split every समास and say the relation (तत्पुरुष / कर्मधारय / बहुव्रीहि / द्वन्द्व …) and the vibhakti of each पद: the सूत्र's meaning is
   fixed by it (`स्वरेऽवर्णवर्जो नामी` ≠ `स्वरोऽवर्णवर्जो नामी`). Say what must be **supplied from earlier सूत्र** (अनुवृत्ति) and which earlier सूत्र it comes from — only if the earlier सूत्र is
   readable in the files you read (neighbouring `src/` files); otherwise say `पूर्व-सूत्र से अनुवृत्ति (उपलब्ध पाठ में स्पष्ट नहीं)`.
3. **Examples are the proof.** The वृत्ति's example forms (`पित्रर्थः`, `नदीश्रद्धाभ्यः` …) are exactly as printed: translate/gloss them (the word meaning and the form in the wording of the वृत्ति, e.g. «पितृ + अर्थः → पित्रर्थः = पिता के लिए»);
   never "correct" a form silently. If a printed form looks wrong for the rule, keep it and say so in part 10 (`पाठ सन्दिग्ध — सम्भवतः …`).
4. **Particles carry the argument:** `किम्`, `इति किम्`, `नन्वेवम्`, `अथ`, `यथा`, `तथा`, `च`, `वा`, `एव`, `अपि`, `इति`, `तेन`, `तस्मात्`. `इति किम्` + counter-examples = "why the word is in the सूत्र"; render it as such, and give the exclusion.
5. **Quoted verses / कारिका in the वृत्ति** ("…॥"): render completely, say they are quoted.
6. **Technical terms**: give the Hindi on first use with the Sanskrit in brackets (`स्वर`, `समान`, `सवर्ण`, `नामी`, `सन्ध्यक्षर`, `लोप`, `आगम`, `विकार`, `प्रत्यय`, `विभक्ति`, `धुट्`, `घोष`, `अघोष`, `संज्ञा`), then keep it **consistent** across §.
7. **The sense test is grammatical:** a rendering under which the rule would not produce the very examples the वृत्ति gives is wrong however well it parses. Test your reading of the सूत्र against its own examples.
8. **A suspect letter:** the scan was blurred; pass 1 marks illegible letters `[अस्पष्ट]` — translate only what is there and mark `[अस्पष्ट पाठ के कारण यहाँ अनुवाद अपूर्ण]`; never fill it from your memory of the गणपाठ/other editions. Suspect fount confusions: `क्ष`↔`च`, `त्व`↔`ल्व`, `श्च`↔`स्व`, `ष`↔`प`, `ण`↔`न`.
9. **Missing text.** The scan has lost whole pages elsewhere; a § keyed `(अंशतः उपलब्ध)` or a segment `[स्कैन में … अनुपलब्ध]` means exactly that: never reconstruct what is missing; translate what is there and say so. In this volume **adhyāya 3 lost about 40 printed pages** (many § begin or end with such a marker; a § whose beginning is missing is `(अंशतः उपलब्ध)`), and 4.3.19–21 (printed page 347) are lost. Where a § is only a **tail** (its सूत्र is not on the page), do not guess the सूत्र: say that only the latter part of the वृत्ति survives. Printed pages 405–406 (§360250–§360320) are physically scrambled and carry many `[अस्पष्ट]`: translate only what is readable. Never invent, in any part (7, 7-क, 8, 9, 9-क), content for missing text.

# The other parts

### 7. सूत्र की विस्तृत व्याख्या
3–6 bullets, each 60–180 words, each with a **bold** sub-heading, in this spirit: **पदच्छेद एवं समास-विग्रह** (every पद: विभक्ति, relation); **सूत्रार्थ** (in your own clear Hindi);
**अनुवृत्ति** (what is carried in and from where); **प्रवृत्ति** (conditions: what must stand where — e.g. «स्वर परे हो तो…»); **वृत्ति का आशय** (what Durgasimha adds: the purpose clauses `किमर्थम्`, examples, the reason a word is in the सूत्र);
**पूर्वापर-सम्बन्ध** (which earlier/later सूत्र of the book it limits, extends or is an exception to — cite `का° A.P.N` **only** for सूत्र you have read in `src/`); **तुलना** with Pāṇini only where you are sure of the सूत्र (give the number and hedge: `लगभग`, `सम्भवतः`) — silence is better than a wrong number.
If the § is a heading, a मङ्गल verse or a colophon-only passage: say what it is and why it stands there; 1–3 bullets are enough.

### 7-क. सूत्र का प्रयोजन एवं सिद्धि-प्रक्रिया
Heading exactly: `## 7-क. सूत्र का प्रयोजन एवं सिद्धि-प्रक्रिया (प्रयोजन, उदाहरण-सिद्धि एवं दोष-निवृत्ति)`.

**Every example group, every `इति किम्`/`किमर्थम्` clause and every exclusion the वृत्ति states gets one bullet**, in this shape:

`- **<उदाहरण / पद / प्रश्न>** — *प्रयोजन:* what this rule (or this word of the सूत्र) is **for** — what wrong form it prevents or right form it makes. *सिद्धि:* the step-by-step derivation in the order of the वृत्ति (e.g. `पितृ + अर्थः → (ऋ का असवर्ण स्वर परे होने पर र्) → पित्र् + अर्थः → पित्रर्थः`), naming the सूत्र that does each step (`का° A.P.N`, only if readable in `src/`; else `(सूत्र उपलब्ध पाठ में नहीं)`). *निवृत्ति:* the wrong form / over-application it blocks (`इति किम्` answer). *दृष्टान्त:* one more concrete form (नया शब्द) that works the same way — marked `(व्याख्याकार का दृष्टान्त)`.`

- Take the *प्रयोजन* from the वृत्ति where it states one and say `ग्रन्थ के अनुसार`; where it is your own reasoning, say `व्याख्याकार का तर्क`. **Never present your reasoning as Durgasimha's.**
- A derivation must be a real derivation, not a restatement; every step must follow from a rule you can name. If you cannot complete a derivation honestly, give as far as you can and say `शेष प्रक्रिया उपलब्ध सूत्रों से स्पष्ट नहीं`.
- If the passage is a heading/मङ्गल/colophon: give the purpose of that (why a मङ्गल; where the पाद ends) — never blank. If truly nothing applies: `इस अनुच्छेद में कोई पृथक् सिद्धि-प्रक्रिया नहीं; उसका प्रयोजन भाग 7 में आ चुका है।`

### 8. उदाहरण एवं प्रयोग
2–3 **additional** forms or phrases (not the वृत्ति's own) showing the rule at work, in Sanskrit with Hindi meaning, marked `(व्याख्याकार का दृष्टान्त)`; a sentence of everyday use where natural. If the § is a heading/मङ्गल: `इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।`

### 9. तुलनात्मक तालिका / चार्ट
One markdown table, 3–8 rows where it helps: (वर्ण-वर्ग ↔ संज्ञा; विभक्ति ↔ प्रत्यय ↔ रूप; मूल रूप ↔ सन्धि ↔ फल; विधि ↔ निषेध ↔ उदाहरण). If none helps: `इस अनुच्छेद हेतु तालिका आवश्यक नहीं।`

### 9-क. प्रयोग-विधि एवं अभ्यास (व्याकरण-अध्ययन में उतारने के सूत्र)
Heading exactly: `## 9-क. प्रयोग-विधि एवं अभ्यास (व्याकरण-अध्ययन में उतारने के सूत्र)`.

**Write for a विद्यार्थी who wants to *form* words this way, not merely understand the rule.** 3–5 bullets, each 40–100 words, each opening with a bold tag:
- **चिन्तन.** the question to ask before applying the rule (`यहाँ परे स्वर असवर्ण है या सवर्ण?`).
- **अभ्यास.** a concrete drill with steps and **how many times** (`प्रतिदिन पाँच रूप तोड़कर जोड़ें; सात दिन`).
- **चर्चा.** a question for a गुरु / सहपाठी and what a good answer looks like.
- **परीक्षण.** how you know the rule is taking root; the usual slip.
- **दृष्टान्त.** every bullet ends with a worked mini-example (a new word, derived step by step).

Rules: (1) tag every bullet **`[ग्रन्थ-सम्मत]`** (the text itself prescribes it) or **`[सुझाव]`** (the व्याख्याकार's suggestion). A count, duration or order is `[सुझाव]`. Never both tags on one bullet. (2) Nothing against the text; no new rules. (3) Every drill and example must be **grammatically sound** — derive it with the rules you actually have; do not use a form you cannot derive. (4) If nothing applies (heading/colophon): `इस अनुच्छेद से कोई पृथक् अभ्यास-सूत्र नहीं निकलता।`

### 10. सन्दर्भ एवं पाद-टिप्पणी
**1–3 one-line bullets, no blank line between them.** The उद्धरण-सूत्र of this § in the form `का° A.P.N`; one line where a printed form or letter is doubtful and how you read it; any Pāṇini parallel you are *sure* of (hedged). Otherwise: `मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।`

---

## Lessons from the audits of the sister books — avoid these faults
1. **Mark the source of every reason.** `ग्रन्थ के अनुसार` only for what the वृत्ति states; **every added reason or derivation step is yours** and carries `(व्याख्याकार का तर्क)`.
2. **9-क tags are exactly `[ग्रन्थ-सम्मत]` or `[सुझाव]`** — never combined; every bullet carries one.
3. **Every drill and every दृष्टान्त must be sound:** a "test" must not itself break the rule it teaches; a derivation must follow the cited sūtras; do not use an example from a different rule.
4. **Cross-references are exact.** Cite `का° A.P.N` only for सूत्र you have read in `src/` that say what you claim. The राजादि-वृत्ति gaṇa sub-sūtras are not in this volume.
5. **Counts and lists:** if the text lists items (the 14 स्वर, the 10 समान …), list them all; do not say "four" and name three.
6. **Open questions the text does not settle are said to be open** — do not resolve them; do not state another grammarian's view as Durgasimha's.
7. **Variant readings `[ ]`/`( )` printed in the Sanskrit are the edition's:** translate the main reading; note a meaning-changing variant in part 10.

## Before writing a §, read
the § in `src/` (every `(Tn)`), the §§ before and after (the rules lean on each other), and for the first § of a pāda the last § of the previous one.

## Context
**कातन्त्र** (शर्ववर्मा) with the **वृत्ति of श्री दुर्गसिंह** — a Sanskrit grammar in the sūtra style, arranged in **अध्याय** (1 सन्धि: 5 pādas; 2 नाम: 6 pādas incl. the तद्धित and the राजादि-वृत्ति of रत्नेश्वरचक्रवर्ती) and **पाद**. This volume covers **अध्याय 3 (आख्यात — the verb: 8 pādas; closes with `इत्याख्यातं समाप्तम्`)** and **अध्याय 4 (कृत् — primary suffixes, opens `अथ कृतः`; 6 pādas)**. Adhyāya 1–2 (सन्धि, नाम, तद्धित) are a separate volume: you may cite `का° 1.x.y` / `का° 2.x.y` only where the rule is quoted in the वृत्ति you read, else write `(पूर्व अध्यायों का सूत्र; यहाँ पाठ उपलब्ध नहीं)`. Reference model for depth and tone: `../katantra-vyakarana/addenda/s20.md`. A सूत्र reference is `का° अध्याय.पाद.सूत्र`.
The text was set from manuscripts; pass 1 read a blurred scan. Several forms are flagged. Do not assert more than a § says. Related texts: पाणिनि-अष्टाध्यायी (for comparison only, hedged), कातन्त्र-वृत्तिकार त्रिलोचनदास/चैत्र (not in the files — do not cite).

## Style — binding
- शास्त्रीय, clear हिन्दी. English digits in your prose; Devanagari digits only inside quoted Sanskrit.
- **Never write any sect name** anywhere.
- **Jain/other authorities named with respect:** `श्री दुर्गसिंह`, `श्री शर्ववर्मा`, `श्री रत्नेश्वरचक्रवर्ती`; non-Jain grammarians plain (`पाणिनि`, `कात्यायन`, `पतञ्जलि`) — use bare names only for them.
- **No working-process language** (बैच, सत्र, file names, scan pages, उपयोगकर्ता, other agents).
- **Never fabricate** a citation, a sūtra number or a form. "लगभग"/"सम्भवतः" where unsure; silence where you do not know.

## Writing the files
One § at a time, immediately: `addenda/s30.md`. Heading order: `## 6. टीका का हिन्दी अनुवाद` · `## 7.` · `## 7-क.` · `## 8.` · `## 9.` · `## 9-क.` · `## 10.` (no parts 3, 4).

## Report back (under 250 words)
§ keys completed; every `(Tn)` you could not construe (named); every printed form that does not fit its rule; every derivation you could not complete; every citation you wanted but could not verify; every 7-क/9-क point you were unsure of; and confirmation that every § has a file and every `(Tn)` has a Hindi line.
