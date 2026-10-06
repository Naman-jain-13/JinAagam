# Pass 3 — Sanskrit↔Hindi audit spec (परमात्मप्रकाश एवं योगसार)

*Working document. Nothing here goes into the book.*

## What you are doing, and why it exists

Another agent has rendered **श्री ब्रह्मदेव's संस्कृत टीका** into Hindi, segment by segment. You are
reading the Sanskrit and that Hindi side by side and reporting **every place the Hindi says something the
Sanskrit does not, or fails to say something it does.**

The reader of this book has seen a previous व्याख्या where the Hindi misrendered the Sanskrit, and asked
for this to be checked properly. You are that check. Nothing in this pipeline self-certifies: you did not
write the Hindi you are auditing, you have not seen the reasoning behind it, and you should not assume it
is right.

**You report. You do not edit any file in `parts/` or `addenda/`.** Your findings are applied afterwards,
deliberately, so there is a record of what changed and why.

## What to read

For each § key in your range:

- `parts/<batch>.md` — the § block: the **अपभ्रंश दोहा**, the **मुद्रित संस्कृत छाया**, the **printed
  हिन्दी अनुवाद** (part 5), and **part 6's Sanskrit टीका in `(T1)`, `(T2)`… segments**;
- `addenda/s<key>.md` — the same agent's **part 6 Hindi**, against the same tags, plus parts 3, 4, 7–10.

Read the Sanskrit **first**, and construe it yourself, before you look at the Hindi. If you read the Hindi
first you will find yourself agreeing with it. Form your own reading, then compare.

## Settle the pass-1 flags in your range too

`verify/pass1_flags.md` lists every reading the extraction agents could not settle, by § key, together with
the ones already resolved (so you do not re-open them). **If a § in your range appears there, settle its
flag as part of your audit** and record the outcome in your report as `RESOLVED → <reading>` with the
evidence, or `STANDS AS PRINTED`.

The order of attack that has actually worked on this edition, cheapest first:

1. **Read the edition's own हिन्दी for that दोहा.** It glosses the टीका's terms, with the Sanskrit lemma in
   square brackets, and settles most doubts outright with no magnification at all. It is the same editor
   rendering the same sentence.
2. **Rejoin any word split across a line end** before reading it. `…द्वेषाद्रा-` / `गाच्च…` read as one unit
   gives the non-word `रोह`; rejoined it is `रागात् च`.
3. **If it is a quoted verse, recall the received text** of the ग्रन्थ it comes from. The टीका quotes
   constantly, and a received text settles a reading independently of the scan.
4. **Test the word lexically.** A sequence that is not a word of the language is a misreading, not the
   edition. In this fount `प्र` prints as a plain `म` (so `मतिपक्ष` is `प्रतिपक्ष`, `मत्यय` is `प्रत्यय`) and
   `ल` can stand for the suffix `त्व`. Both are in the flags file with worked examples.
5. Only then magnify.

## What pass 2 already did, so you do not re-do it

The व्याख्या agents worked to a detailed spec and reported honestly. Before auditing, know what is already
settled, so your effort goes where it is needed.

**Already handled, and not findings:**
- **Divergences from the edition's printed हिन्दी.** Over a hundred are recorded. The rule was: render the
  **Sanskrit** in part 6, leave part 5 exactly as printed, note the difference in part 10. Confirm the note
  exists and the Sanskrit was read right; do not report the divergence itself as an error.
- **The टीका against the printed छाया.** Part 6 follows the **टीका** (the छाया is the edition's rendering of
  the दोहा; the टीका is श्री ब्रह्मदेव's own gloss). Where that puts part 6 at odds with part 2 on the same
  page, **that is correct**, not a fault.
- **The edition's own `(?)` marks** are kept verbatim everywhere. They are the editor's uncertainty and are
  evidence. Never report their presence as a defect.
- **Internal inconsistencies left unharmonised** — `संपितं` for `संपादितं`, three spellings of `पडियारि`,
  शुद्ध- against अशुद्धनिश्चयनय in adjacent segments. Reproducing them is the standing rule.
- **Grammatical vocabulary read as grammatical** — `कर्मता`, `कर्तृत्व`, `कर्तृभूत`, `करणभूत`, `अभिधेय`,
  `वाच्य`. If part 6 renders one of these as a doctrinal claim, *that* is a finding.

**Known printing faults already corrected in `parts/`** — do not re-flag them, but do check the Hindi used the
corrected reading: `प्र` printing as a plain `म` (about seventy instances), `ल` for `त्व`, `श्च` for `ञ्च`,
`छ` for `ह`, `ङ्ग` for `ज्ञ`, `द्वि` for `दि`, and word-initial `अ` lost in sandhi. `verify/pass1_flags.md`
lists every one with its evidence.

## The four methods that actually settled hard passages

Use these before proposing an emendation. Each has resolved a real case here, and two of them **stopped**
an unnecessary one.

1. **Look for the same construction elsewhere in the same §.** §21900's `रहितान्` looked impossible until T8
   of the same § turned out to run the identical frame in the ablative — so it was `रहितात्`, agreeing with
   `शुद्धात्मद्रव्यात्`. §20250's missing `न` was proved genuinely lost the same way, by T1 and T8.
2. **Ask whether some other feature already carries the force you think is missing.** §10870 seemed to need
   a `न`; it did not — the contrast was in the case (locative `स्वात्मनि` against instrumental
   `स्वशुद्धात्मस्वरूपेण`). The verb was not negated, it was redirected.
3. **Look for the fault's own fingerprints nearby.** §21140's `अग्निर्ज्ञानिलोक…` was settled because the
   initial `अ` of `अग्निः` is demonstrably missing *earlier in the same line* — so a second loss needed no
   separate argument.
4. **Grep `parts/` before emending.** This टीका reuses a small stock of formulas. `कं कर्मतापत्वम्` was
   settled by finding `किं कर्मतापन्नम्` dozens of times. **It cuts both ways:** `पञ्चकलेन` was twice
   proposed for emendation before a grep showed `कल` is the edition's *own* term for a verse-group —
   `त्रिकलम्`, `षट्कलेन`, and the अपभ्रंश `तिघलं`. A word must be real *in this text*, not merely in
   classical Sanskrit.

## Do not convict the edition of an error it did not make

Finding divergences is the job. **Inventing one is worse than missing one**, because a printed charge
carries authority a reader cannot check.

One was caught and removed: a note claimed योगसार दोहा 36's अर्थ — *"चेतन तो केवल एक जीव ही है"* — denies
other जीव their consciousness. It does not. **`एक` there is "alone", not the numeral.** The sound point in
the same place was grammatical: the छाया's `जीव` is a vocative while the अर्थ makes it the subject.

**Idiom is not error. A free भावार्थ is not error. An expansion the Sanskrit supports is not error.**

## If your range is योगसार (keys 30000+)

योगसार has **no टीका**, so there is **no part 6 to audit**. Its § carry parts 3, 4, 7, 8, 9, 10 only, and the
part-6 slot holds the edition's **पाठान्तर**, reproduced verbatim. Audit the अन्वय and अन्वयार्थ against the
**छाया**, and check part 10 explains the variants honestly — what each changes, whether it touches the
sense, and that no variant is presented as the text.

## What counts as a finding

| प्रकार | meaning |
|---|---|
| **त्रुटि** | The Hindi states something the Sanskrit does not, or contradicts it. A compound split wrongly; a `कथंभूत` question attached to the wrong noun; a case or verb misread; a negation or particle dropped so the force changes. |
| **लोप** | A word, qualifier or clause of the Sanskrit has no counterpart in the Hindi. Terse Sanskrit loses qualifiers easily. |
| **वर्धन** | The Hindi adds matter not in that Sanskrit segment. Supplying context is legitimate in part 7; in part 6 it is not, because part 6 claims to be the टीका. |
| **सन्देह** | The Hindi is defensible but another reading is at least as good, and a reader would be served by knowing. |

Check especially the things that go wrong in this commentary:

1. **`कथंभूतः / कथंभूता / कथंभूतम्`** — the gender and number tell you which noun is being asked about.
   Verify the Hindi attached the description to *that* noun. This is the commonest real error.
2. **Quoted अपभ्रंश vs its Sanskrit gloss.** `कम्मु पुराकिउ कर्म पुराकृतं` is the दोहा's words followed by
   their gloss, not a Sanskrit clause. Check the Hindi did not read it as one.
3. **समास splits.** Re-split every long compound yourself and check the relation between members, not just
   the members. `वीतरागस्वसंवेदनतत्त्वज्ञानी` has a specific internal structure and a wrong split changes
   the doctrine.
4. **Particles** — `एव`, `अपि`, `तु`, `हि`, `च`, `किल`. A dropped `एव` turns "only this" into "this".
5. **Case of the final member** of a compound, which governs its role in the sentence.
6. **The answer-to-question pairing** across the whole segment chain: every `किं कृत्वा ।` should have a
   क्त्वान्त answer, every `कस्मात् ।` a reason, and so on.
7. **Whether any `(Tn)` tag from `parts/` has no Hindi line at all** in `addenda/`. Report each as **लोप**.

**8. Ask whether the Hindi could be true of its subject.** This is the sharpest test available and it is
not grammatical. From दोहा 2 of this ग्रन्थ: `तान् सिद्धगणान् कर्मतापन्नान् अहं वन्दे ।` — `कर्मतापन्नान्`
is **कर्मता + आपन्नान्**, "which have become the grammatical object" of `वन्दे`. Split instead as
**कर्म + तापन्नान्**, "afflicted by karma", it gives fluent Hindi that says the सिद्ध — free of all karma by
definition — are afflicted by it, flatly contradicting the verse being explained. A reading that cannot be
true of its subject is wrong however well it parses. Flag such cases **त्रुटि**, not सन्देह.

Watch for the same trap in reverse: `कर्मता`, `कर्तृत्व`, `कर्मत्व`, `अभिधेय`, `वाच्य` are often
**grammatical** terms in this commentary, describing how the verse's words function — not doctrinal terms
about the soul. A Hindi rendering that turns a grammatical note into a doctrinal claim is a त्रुटि.

**9. Sanskrit that does not construe at all is a suspected transcription error — report it.** The
extraction pass is told to transcribe exactly and flag rather than emend, so a segment may reach you with
a word that parses to nothing. Say so as **सन्देह**, name the segment, and give the reading you think the
page actually has and why. One such case was `अत्राहृगुणस्वरूप…`, which the page in fact has as
`अत्रार्हद्गुणस्वरूप…` — a रेफ lost above the following consonant. You are the last check before the Hindi
is believed; a translator who silently invented sense for an impossible word is a त्रुटि, not a सन्देह.

## What is NOT a finding

- A different but equally faithful Hindi wording. You are auditing sense, not style.
- The Hindi being fuller than the Sanskrit **in parts 7–10** — those are the व्याख्या's own and are meant
  to go beyond the टीका.
- A divergence between the Sanskrit and the edition's **printed** हिन्दी (part 5) that the writer already
  recorded in part 10. That is the intended handling; confirm the note exists and move on.
- The टीका itself being terse, odd or ungrammatical. Your job is whether the Hindi reflects it, not
  whether श्री ब्रह्मदेव wrote well.

## Output

One file per range: `verify/v<first-key>-<last-key>.md`.

```markdown
# संस्कृत↔हिन्दी परीक्षण — §<first> से §<last>

## निष्कर्ष
- परीक्षित §: 14 | परीक्षित खण्ड (Tn): 96
- त्रुटि: 2 | लोप: 3 | वर्धन: 0 | सन्देह: 4

## निष्कर्ष-विवरण

### §20390 (T2) — त्रुटि
- **संस्कृत:** पुनरपि किं करोति । अहिणव पेसु ण देइ अभिनवं कर्म प्रवेशं न ददाति ।
- **लिखित हिन्दी:** <quote the Hindi exactly as written>
- **दोष:** <what is wrong, in one or two sentences, with the grammatical reason>
- **सुझाया हिन्दी:** <a corrected line, complete and ready to substitute>
```

Give **`सुझाया हिन्दी` for every त्रुटि and लोप** — a complete replacement line, not a description of what
should change. For **सन्देह**, give the alternative reading instead and say which you would prefer.

If a § is clean, say nothing about it. The report lists problems, not confirmations.

End the file with the counts repeated, so they can be read mechanically.

## Rules

- Audit **only** the § keys in your assigned range.
- Quote the Sanskrit and the Hindi exactly as the files have them — your quotations are what the fix is
  applied against.
- Where you are unsure whether something is an error, say **सन्देह** and give your reasoning. A verifier
  who overcalls wastes a little time; one who undercalls defeats the purpose.
- If a whole § looks sound, that is a real and useful result. Do not invent findings to seem thorough.
- Write the file incrementally — after the first few §, then append — so a long range is never lost.

## Report back (under 200 words)

The § range audited; the four counts; the single most serious finding in your range stated in one
sentence; and whether any `(Tn)` tag was missing its Hindi entirely.
