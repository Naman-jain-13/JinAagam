# Translation fidelity — when the व्याख्या renders Sanskrit (or Prakrit/Apabhraṃśa) into Hindi

Use this when the book's value depends on a translation being right: a संस्कृत टीका rendered into Hindi,
an अपभ्रंश मूल with a Sanskrit छाया, a प्राकृत गाथा with अन्वयार्थ. It is the reference behind pass 3 in
`SKILL.md`.

The occasion for it: a reader of a finished book reported Hindi that said things its Sanskrit टीका did
not. The errors were not carelessness — they were specific, recurring, grammatically-caused, and
invisible to anyone who read only the Hindi.

## The failure modes, named

Put these in the translation spec *and* in the audit spec, so the writer guards against them and the
auditor looks for them.

**1. The कथंभूत question attached to the wrong noun.**
Sanskrit commentary runs on one-word questions — `किं कृत्वा ।` `कथंभूतः ।` `कस्मात् ।` `कः ।` `कान् ।`
`किं करोति ।` — each followed by its answer. Each governs a grammatical form:

| question | asks | answer form |
|---|---|---|
| `किं कृत्वा` | having done what? | क्त्वान्त / ल्यबन्त |
| `कथंभूतः / कथंभूता / कथंभूतम्` | of what kind? | adjective agreeing with the subject |
| `कस्मात्` | why? from what? | ablative, or `-त्वात्` clause |
| `कः / के` | who? | nominative |
| `कम् / कान्` | whom? | accusative |
| `किं करोति` | does what? | finite verb |

**The gender and number of `कथंभूतः` tell you which noun it asks about** — the most useful single signal
in such a commentary, and the one most often ignored. Attach the description to the wrong noun and the
doctrine changes while the Hindi still reads smoothly.

**2. A quoted मूल word mistaken for Sanskrit.** Commentaries quote the verse's own words (often set in
bold) and gloss each immediately: `कम्मु पुराकिउ कर्म पुराकृतं` is अपभ्रंश followed by its gloss, not a
Sanskrit clause. Read as one clause it yields plausible nonsense.

**3. A समास split wrongly.** A compound is its members *plus a relation*. `वीतरागस्वसंवेदनतत्त्वज्ञानी`
is "knower of the truth which is dispassionate self-experience", not "a dispassionate knower of
self-experience and truth". Require the spec to **show the split** in the Hindi wherever it is not obvious,
and to record a defensible alternative in the references part.

**4. A particle dropped.** `एव` (ही), `अपि` (भी), `तु`, `हि`, `च`, `किल`. Losing `एव` turns an exclusive
claim into a loose one — a change of doctrine, not of style.

**5. The case of a compound's final member ignored**, so the compound's role in the sentence is misread —
subject taken for object, or a qualifier floated free.

**6. A qualifier quietly lost.** Sanskrit is terse; it is easy to render a sentence's shape and drop a
word. The testable property is that **every word of the source is represented somewhere in the Hindi.**

## Structural choices that make fidelity checkable

- **Transcribe the source once, in the extraction pass, and tag it in segments** `(T1)`, `(T2)` … The
  translating pass writes against the same tags; the builder pairs them. Never let the translating agent
  retype the source — that is where errors enter, and a retyped source cannot be audited against anything.
- **Print source and translation adjacently** in the finished book. A reader who knows the source checks
  you line by line, which is worth more than any claim of accuracy in a preface.
- **Keep a question with its answer inside one segment.** Splitting `कथंभूतः ।` from its answer leaves the
  translator a question with nothing to answer it.
- **Where the edition's own printed translation diverges from the source**, render the *source*, leave the
  printed translation exactly as printed, and note the divergence in one line. Never harmonise silently.

## The audit

A **different** agent, which has not seen the writing, reads source and translation side by side and
classifies each finding:

| | |
|---|---|
| **त्रुटि** | the translation states what the source does not, or contradicts it |
| **लोप** | a word or clause of the source has no counterpart |
| **वर्धन** | the translation adds matter not in the source |
| **सन्देह** | defensible, but another reading is as good |

It gives a **complete replacement line** for every त्रुटि and लोप — not a description of what should
change — and it **reports without editing**, so findings are applied deliberately and leave a record.

Tell the auditor to **construe the source itself before reading the translation**. An auditor who reads
the translation first will agree with it.

Tell it also what is *not* a finding: different but equally faithful wording; the explanatory parts
legitimately going beyond the source; a divergence the writer already recorded; the source itself being
terse or ungrammatical.
