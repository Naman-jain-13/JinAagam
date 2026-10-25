# Pass 3 — independent audit spec (मूलाचार, अधिकार 4)

*Working document. Nothing here goes into the book.*

Another agent rendered **श्री वसुनन्दि's संस्कृत आचारवृत्ति** into Hindi, segment by segment, and wrote the व्याख्या
parts. You never saw that work. **Report every place the Hindi says something the Sanskrit does not, or fails to
say something it does** — and check the two practical parts (7-क, 9-क) for honesty. **You report; you do not
edit `parts/` or `addenda/`.**

For each § key in your range read: the source `C:\Users\naman\AppData\Local\Temp\claude\e--Projects-JinAagam\8833b842-66bd-488c-af18-e032f95ce610\scratchpad\mulachar_src\s<key>.md` (the **प्राकृत गाथा**, **श्री वसुनन्दि's Sanskrit वृत्ति in `(Tn)` segments**, and the
manuscript-variant footnotes) and `addenda/s<key>.md` (part 5 = the Hindi of the गाथा; part 6 = the Hindi of the वृत्ति against the same tags; plus parts 2, 3,
4, 7, 7-क, 8, 9, 9-क, 10). **Those are your only sources.** This book is deliberately an *independent* Hindi rendering: **do not open `parts/`, `img/`, `mool/`,
`_archive_v1/` or any file that might carry another Hindi translation of this text, and do not bring one from memory** — if a Sanskrit reading looks worn or
doubtful, report it as सन्देह with the reading you think likely; do not go looking for a published translation to settle it.

**Read the Sanskrit first and construe it yourself, before reading the Hindi.** If you read the Hindi first you
will agree with it.

## A. Part 6 — Sanskrit ↔ Hindi (the main job)

Finding types: **त्रुटि** (the Hindi states what the Sanskrit does not / contradicts it: wrong compound split, a
question attached to the wrong noun, wrong case/verb, dropped negation or particle) · **लोप** (a word/qualifier/
clause with no Hindi counterpart; any `(Tn)` with no Hindi line) · **वर्धन** (Hindi adds matter not in that
segment — legitimate in part 7, not in part 6) · **सन्देह** (defensible, another reading at least as good).

Check especially: quoted प्राकृत word + `—` + gloss rendered as a gloss, not as Sanskrit prose; every question
paired with its own answer, and `कथंभूतः/ता/तम्` attached to the noun it agrees with; every समास re-split by you;
particles `एव अपि तु हि च वा इति`; the case of a compound's final member; **enumerations complete** (count the
items in Sanskrit and Hindi); quoted verses rendered completely; and **whether the Hindi could be true of its
subject** — a reading that contradicts the गाथा it explains is wrong however well it parses.

**Not findings:** a different but equally faithful wording; 
(part 5 is verbatim); the वृत्ति being terse or odd. **Never invent a finding** — a charge against the edition
carries authority a reader cannot check; idiom, free expansion and an explanation the Sanskrit supports are
not errors.

Sanskrit that does not construe is a suspected transcription error: report as **सन्देह** with the reading you
think the page has (confusions in this fount: `प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `ष`↔`प`, `ण`↔`न`, `ध`↔`घ`).
Doubtful or worn readings in the Sanskrit/Prakrit source: report as **सन्देह** (with the reading you think likely and why); do not settle them from any outside translation.

## B. Parts 7-क and 9-क — the reader's two special requirements

7-क (क्रिया का युक्तिसंगत उद्देश्य) and 9-क (आचरण-विधि एवं अभ्यास) were requested for their practical value to
a साधु. They are also where an agent is most tempted to over-reach. Check, and report as **सन्देह / त्रुटि**:

1. **Every क्रिया the गाथा names has a bullet in 7-क**, with उद्देश्य, युक्ति and निवृत्ति; the युक्ति is a real
   argument, not a restatement; the targeted कषाय/दोष is plausible and the *mechanism* is stated.
2. **Source honesty.** Things the वृत्ति states are marked `वृत्ति के अनुसार` and really are in the वृत्ति; the
   writer's own reasoning is marked `व्याख्याकार का तर्क`. Report any place the writer's reasoning is presented
   as the वृत्ति's or the आगम's.
3. **9-क tags.** Every item carries `[आगम-सम्मत]` or `[सुझाव]`; every `[आगम-सम्मत]` really is in the वृत्ति/आगम
   (check against the Sanskrit); **no suggested frequency, count, duration or hour is presented as आगम-विधान.**
4. **Nothing against the आगम; no new vow, no softened rule.** A technique must serve the very क्रिया the गाथा
   prescribes. Flag any that invents a rule or relaxes one (illness, travel and the like should be sent to the
   गुरु, not resolved).
5. **Fabricated authority.** Every citation (ग्रन्थ + number) in parts 7, 7-क, 9-क, 10: is it certain? A wrong
   verse number is a **त्रुटि**; an unverifiable one should be `लगभग`/`सम्भवतः` or dropped. Report each you
   believe is wrong or cannot confirm.
6. **दिगम्बर recension of तत्त्वार्थसूत्र** (e.g. 7.13 प्रमत्तयोगात्प्राणव्यपरोपणं हिंसा; 5.29 सद्द्रव्यलक्षणम्;
   5.30 उत्पादव्ययध्रौव्ययुक्तं सत्; 5.38 गुणपर्यायवद् द्रव्यम्).

## C. Parts 2–5, 8–10

- **Part 5 (गाथा का हिन्दी अनुवाद):** renders exactly what the गाथा says — nothing added from the वृत्ति, every word of both lines represented, particles kept, reads as natural Hindi.
- Part 2 (छाया, व्याख्याकार-कृत): faithful to the वृत्ति's glosses, two lines, closing `॥N॥`.
- Parts 3–4: the अन्वय uses only the गाथा's own प्राकृत words; every word accounted for in the अन्वयार्थ.
- Part 8: the दृष्टान्त↔दार्ष्टान्तिक mapping holds and its limit is stated. Part 9: the table is accurate.
- Part 10: 1–3 bullets only; no process language; no sect names; no bare आचार्य names in prose.

## Output

One file per range: `verify/v<first-key>-<last-key>.md`.

```markdown
# परीक्षण — §<first> से §<last>

## निष्कर्ष
- परीक्षित §: N | परीक्षित खण्ड (Tn): M
- त्रुटि: a | लोप: b | वर्धन: c | सन्देह: d

## निष्कर्ष-विवरण
### §<key> (T<n> | भाग 7-क | भाग 9-क …) — त्रुटि
- **संस्कृत / आधार:** <quote exactly>
- **लिखित हिन्दी:** <quote exactly as in addenda/>
- **दोष:** <1–2 sentences with the grammatical or doctrinal reason>
- **सुझाया हिन्दी:** <a complete replacement line, ready to substitute>
```

A `सुझाया हिन्दी` (complete replacement) for every त्रुटि and लोप; for सन्देह, the alternative reading and which
you prefer. A clean § gets no entry. End the file with the counts repeated. Write incrementally (after the
first few §, then append). Quote Sanskrit and Hindi **exactly as the files have them** — the fix is applied
against your quotation. If a § is sound, that is a real result — do not invent findings to seem thorough.

- Also audit the **`शीर्षक:` first line** of each addendum: it must say accurately what the गाथा establishes, from the Sanskrit alone.

## Scan-reading rule for this audit (binding)
You may check a doubtful Sanskrit/Prakrit reading on the scan **only through the crop tool**, which returns the area above the horizontal rule and nothing below it:
`python crop_above_rule.py mool/Mulachar_Purvardh_Aryika_Jnanmati.pdf <scan page> <out.png> 220 [x0 y0 x1 y1]` (page box 504×666 pt; the optional box is a zoom region *inside* the above-rule area; printed page = scan page − 58).
**Never** render the page yourself or open `img/p*.png` — those show the printed Hindi below the rule, which this book must not be influenced by. If the tool warns "no rule found", look only at the Sanskrit and ignore any Hindi.
