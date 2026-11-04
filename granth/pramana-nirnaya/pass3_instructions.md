# Pass 3 — independent audit spec (प्रमाणनिर्णय)

*Working document. Nothing here goes into the book.*

Another agent rendered **श्री वादिराजसूरि's संस्कृत मूल पाठ** (प्रमाणनिर्णय) into Hindi, segment by segment, and wrote the व्याख्या
parts. You never saw that work. **Report every place the Hindi says something the Sanskrit does not, or fails to
say something it does** — and check the two practical parts (7-क, 9-क) for honesty. **You report; you do not
edit `parts/` or `addenda/`.**

For each § key in your range read: `parts/batch*_*.md` (the § block: Sanskrit मूल in `(Tn)` segments, printed footnotes) and `addenda/s<key>.md` (the part-6 Hindi against the same tags, plus
parts 2, 3, 4, 7, 7-क, 8, 9, 9-क, 10). The scan is `mool/Pramana_Nirnaya.pdf` (printed page = scan − 20; render a crop with pymupdf at 300–450 dpi, IDX = scan − 1). **In this edition every Sanskrit paragraph is followed by the editor's modern Hindi translation. You may look at the scan ONLY to check a Sanskrit reading: crop just the bold Sanskrit paragraph, never read the Hindi paragraphs, and never use them to judge anything** — this book's Hindi must stay independent of that translation.

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

**Not findings:** a different but equally faithful wording; a divergence from the *printed* Hindi that the
writer already logged in part 10 (confirm the note exists); the printed Hindi being fuller than the Sanskrit
(part 5 is verbatim); the वृत्ति being terse or odd. **Never invent a finding** — a charge against the edition
carries authority a reader cannot check; idiom, free expansion and an explanation the Sanskrit supports are
not errors.

Sanskrit that does not construe is a suspected transcription error: report as **सन्देह** with the reading you
think the page has (confusions in this fount: `प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `ष`↔`प`, `ण`↔`न`, `ध`↔`घ`).
The pass-1 doubtful readings are listed in `verify_flags.md`; **settle those in your range by looking at the
page** (`RESOLVED → <reading>` with evidence, or `STANDS AS PRINTED`).

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

## C. Parts 2–4, 8–10

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
- verify_flags: RESOLVED/STANDS list

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

## D. Addendum for this series (न्याय texts)

- **Part 7-क** is *तर्क का युक्तिसंगत उद्देश्य एवं दृष्टान्त*: every हेतु / विकल्प / खण्डन / निग्रहस्थान the passage uses has a bullet with
  उद्देश्य · युक्ति · निवृत्ति · दृष्टान्त. The दृष्टान्त must actually illustrate the move named (and not smuggle in a different one).
  Writer's own reasoning must be marked `व्याख्याकार का तर्क`, never passed off as `ग्रन्थ के अनुसार`.
- **Part 9-क** is *प्रयोग-विधि एवं अभ्यास*; tags are `[ग्रन्थ-सम्मत]` / `[सुझाव]`. Check no suggested count is presented as the text's, every bullet
  ends with a worked **दृष्टान्त**, and the drill does not mis-apply the logic (a "test" that would itself commit the fallacy it names is a त्रुटि).
- **Part 6 in a न्याय text:** check **who is speaking** (पूर्वपक्ष vs उत्तरपक्ष) is right; that five-member / three-mark enumerations are complete;
  that each हेत्वाभास is the right one; and that an `अ-`/`न-` negation binds exactly what the Sanskrit binds it to.
- The printed edition's Hindi is deliberately NOT used: part 6 Hindi is wholly the writer's — judge it against the Sanskrit alone.
- Paragraphs ॥19॥–॥20॥ are absent from the scan (printed page 10 missing): never report them missing; check that §190/§200 say so honestly.
- `[अस्पष्ट]` in the Sanskrit is real illegibility (watermark / clipped page edge). If, on the scan, a letter is in fact readable, report it as a सन्देह with the reading; if the Hindi filled an अस्पष्ट gap from sense, that is a त्रुटि.
- Pass-1 known normalisations (printed letters replaced by a corrected form) must be reported for restoration: e.g. ¶42 printed `सवत्र` written as `सर्वत्र`.
- **¶99–109 (§60010–§60110) were transcribed while image reads were flaky — read those paragraphs against the scan line by line.**
- Check every citation (ग्रन्थ + number) in parts 7/7-क/9-क/10; several were given from memory (परीक्षामुख 1.13, प्रमाणवार्त्तिक 'अभिप्रायनिवेदनात्', मीमांसासूत्र 1.1.4, अष्टाध्यायी 'तौ सत्' 3.2.127). Report any you believe wrong; unverifiable ones should be लगभग/सम्भवतः.
- Titles: each § title (first line in parts/) must state what THAT paragraph says (e.g. §20012's title mentions सन्निकर्ष, its text may not) — report wrong titles with a corrected one.

- The editor's `( )` / `[ ]` inside the Sanskrit are variant readings; the Hindi should follow the main reading and part 10 may note a meaning-changing variant. Do not report that as an omission.
