# Pass 2 — व्याख्या spec (परमात्मप्रकाश एवं योगसार)

*Working document. Nothing here goes into the book.*

Pass 1 has transcribed, into `parts/`: the **अपभ्रंश दोहा** (part 1), its **मुद्रित संस्कृत छाया** (part 2),
the **printed हिन्दी अनुवाद and भावार्थ** (part 5), and **श्री ब्रह्मदेव's संस्कृत टीका** in tagged segments
(part 6, under a heading containing "मूल"). Those are finished and **must not be rewritten**.

You write parts **3, 4, 6-Hindi, 7, 8, 9, 10** into `addenda/s<key>.md`.

---

# The thing this project exists to get right

The reader's standing instruction on this ग्रन्थ is: **the Hindi must not say anything the Sanskrit टीका
does not say.** They have seen a previous व्याख्या where it did — wrong sense, a compound split wrongly, a
`कथंभूत` question attached to the wrong phrase. Everything below is built around preventing that.

An independent agent will afterwards read your Hindi against the Sanskrit, clause by clause, and report
every addition, omission and shift of sense. Write as though that audit will happen, because it will.

---

## Part 6 — the Sanskrit टीका rendered into Hindi

This is the heart of your work. **You never retype the Sanskrit.** It is already in `parts/`, tagged
`(T1)`, `(T2)`, … You write a Hindi line against each tag, and the builder prints them interleaved —
Sanskrit, then its Hindi, down the page — so any reader who knows Sanskrit can check you line by line.

```
## 6. टीका का हिन्दी अनुवाद
(T1) <Hindi for segment T1>
(T2) <Hindi for segment T2>
```

Use **exactly the tags pass 1 used**, all of them, in order. If a segment defeats you, still write its
line and say so inside it — a visible `[इस खण्ड का अर्थ सन्दिग्ध है: …]` is honest; a missing tag is a
hole the reader cannot see.

### The method, in the order you should apply it

**1. Separate the quoted अपभ्रंश from the Sanskrit.** श्री ब्रह्मदेव quotes the दोहा's own words (set in
bold in the edition) and glosses each immediately in Sanskrit. `कम्मु पुराकिउ कर्म पुराकृतं` is **not** a
Sanskrit sentence — it is the अपभ्रंश `कम्मु पुराकिउ` followed by its gloss `कर्म पुराकृतं`. Render it as
a gloss: `'कम्मु पुराकिउ' — अर्थात् पूर्वकृत कर्म`. Treating a quoted अपभ्रंश word as Sanskrit, or the
gloss as a separate statement, is a frequent and invisible error.

**2. Render the कथंभूत questions as questions, each joined to its own answer.** These one-word questions
are the skeleton of the commentary, and each governs a specific grammatical form in its answer:

| question | asks | the answer is |
|---|---|---|
| `किं कृत्वा ।` | having done what? | a क्त्वान्त / ल्यबन्त (मुक्त्वा, गत्वा, परिगृह्य) |
| `कथंभूतः ।` / `कथंभूता ।` / `कथंभूतम् ।` | of what kind? | an adjective **agreeing with the subject just named** |
| `कस्मात् ।` | from what? why? | an ablative, or a हेतु clause ending `-त्वात्` |
| `कः ।` / `के ।` | who? | a nominative |
| `कम् ।` / `कान् ।` | whom? what? | an accusative |
| `किं करोति ।` | what does he do? | a finite verb |
| `क्व ।` | where? | a locative |

**The gender and number of `कथंभूतः / कथंभूता / कथंभूतम्` tell you which noun it is asking about.** That
is the single most useful signal in this entire commentary. `कथंभूतः` cannot be asking about a feminine
or neuter noun; find the masculine nominative it agrees with. Getting this wrong attaches a description
to the wrong thing and is exactly the failure the reader reported.

Render it so the structure shows:
`(टीकाकार पूछते हैं:) वह कैसा है? — 'xyz' — अर्थात् …`

**3. Split every समास and say how the members relate.** A compound's meaning is not the sum of its parts;
it is the parts plus a relation. `वीतरागस्वसंवेदनतत्त्वज्ञानी` is वीतराग-स्वसंवेदन-रूप तत्त्व का ज्ञानी —
"one who knows the truth that is dispassionate self-experience" — not "a dispassionate person who knows
self-experience and truth". When the split is not obvious, show it in the Hindi:
`'वीतरागस्वसंवेदनतत्त्वज्ञानी' — वीतराग स्वसंवेदन रूप जो तत्त्व, उसका ज्ञानी`.
Where two splits are both defensible, give the one the printed हिन्दी supports and record the other in
part 10.

### A worked example — why this matters, from दोहा 2 of this very ग्रन्थ

The टीका reads: `तान् सिद्धगणान् कर्मतापन्नान् अहं वन्दे ।`

`कर्मतापन्नान्` splits two ways, and both look like Sanskrit:

| split | yields | verdict |
|---|---|---|
| **कर्मता + आपन्नान्** | "which have become the **grammatical object**" — the commentator noting that `तान् सिद्धगणान्` stands as the कर्म of `वन्दे` | **correct** |
| कर्म + तापन्नान् | "afflicted by karma" | wrong |

The second produces perfectly fluent Hindi — and says that the सिद्ध, who are **by definition free of all
karma**, are afflicted by it. The verse being commented on says they burnt their karma away.

**The test that catches it is not grammatical, it is doctrinal: a reading that contradicts the very verse
it explains is wrong, however well it parses.** Before you commit a rendering, ask whether it could be
true of the subject. An impossible sense is the loudest signal available that a compound was split wrongly
or a question attached to the wrong noun.

Note also that `कर्मता-आपन्न`, `कर्तृत्व`, `कर्मत्व`, `अभिधेय`, `वाच्य` and the like are often **grammatical**
vocabulary in this commentary, describing how the verse's words function, not doctrinal vocabulary
describing the soul. Read them in that register first.

**4. Keep the particles.** `एव` (ही), `अपि` (भी), `तु` (किन्तु), `च` (और), `हि` (क्योंकि), `किल` (कहते हैं),
`नूनम्` (निश्चय ही) each change the force of a sentence. Dropping `एव` turns an exclusive claim into a
loose one — a real change of doctrine, not a stylistic nicety.

**5. Carry the case of the final member.** In a long compound, the case ending on the last member governs
the whole compound's role in the sentence. `-रहितः` nominative describes the subject; `-रहितम्`
accusative describes the object. Read the ending before you decide who is doing what.

**6. Account for every word.** When you have written your Hindi line, read the Sanskrit once more and
check that nothing in it is unrepresented. Sanskrit commentary is terse; it is easy to render the shape
of a sentence and quietly lose a qualifier.

### Where the printed हिन्दी and the Sanskrit disagree

The edition's own हिन्दी (part 5) is a good guide and is usually right. But it is a translation, it
occasionally paraphrases, and it occasionally errs. **Your part 6 renders the Sanskrit, not the printed
Hindi.** Where the two genuinely diverge:

- render the **Sanskrit** in part 6;
- leave part 5 exactly as printed — it is the edition's text, not yours to correct;
- state the divergence in **one line of part 10**, neutrally: what the Sanskrit has, what the printed
  हिन्दी has, and which you followed.

Never silently harmonise them. A reader comparing your book with the original must find the difference
where it actually is.

---

## A स्थल-colophon is structural — render it, do not fold it into the दोहा

Some दोहा carry, as their **last** टीका segment, a sentence of श्री ब्रह्मदेव's that closes a division of the
ग्रन्थ and counts its verses:

> `एवं मोक्षमोक्षफलमोक्षमार्गप्रतिपादकमहाधिकारमध्ये … चतुर्दशसूत्रैः स्थलं समाप्तम् ।`

and some carry the matching opening as `(T1)`. The edition prints a हिन्दी twin of these too
("इस तरह … चौदह दोहे पूर्ण हुए")।

**Translate it in part 6 like any other segment** — it is the टीका and it is the author's own voice. But it
is a statement about the *book*, not about the verse, so:

- do **not** let it into part 3 (अन्वय), part 4 (अन्वयार्थ) or the भावार्थ — those are the दोहा's own sense,
  and the colophon is not part of it;
- in part 7 you may note which division is closing or opening and what it covered, in one sentence, since
  that genuinely helps a reader placing the verse;
- never paraphrase its count. If it says चतुर्दश, the Hindi says चौदह.

## If your range is योगसार, part 6 is not yours

योगसार (keys 30000+) has **no commentary at all** — no श्री ब्रह्मदेव टीका, so there is no टीका to render
into Hindi and **you write no part 6**. The extraction pass has already put the edition's **पाठान्तर**
(manuscript variants, with their sigla) in that slot, and it is reproduced verbatim. Do not touch it, do not
translate it, do not add a `## 6.` heading of your own.

What you write for a योगसार § is parts **3, 4, 7, 8, 9 and 10**. Two things change with the loss of part 6:

- **The छाया carries more weight.** With no टीका to construe, the printed संस्कृत छाया is your main
  evidence for what the अपभ्रंश दोहा means, and the printed `अर्थ—` is the edition's own reading of it.
  Build अन्वय and अन्वयार्थ from the छाया, and check them against the अर्थ.
- **Part 10 now has real work.** Explain the पाठान्तर for the reader: what a siglum is, what the variant
  changes, and whether it affects the sense. Where the edition prints its own `(?)`, say that the editor
  marked the reading uncertain — do not pass over it in silence and do not resolve it for them. Where a
  manuscript's variant would change the meaning, say what the other reading would give. **Never present a
  variant as the text**; the दोहा as printed is the text.

Everything else in this document applies unchanged, including the rule that part 7 is where you may go
beyond what the page says, and parts 1–5 are never embroidered.

## Quoted verses — the edition tells you where most of them come from

श्री ब्रह्मदेव quotes constantly, usually inside `"…"`. **The printed edition indexes those quotations
itself**, in a three-page apparatus at the back listing each quoted verse by its opening words together with
the work it comes from. That apparatus has been attached to the § that actually carry the quotations:

> **`verify/udharan_map.md`** — look up your § keys there before you write part 10.

Where it names a source — `कुन्दकुन्द, पञ्चास्तिकाय २०`, `पूज्यपाद, इष्टोपदेश ४७`, `रामसिंह, दोहापाहुड ८४`,
`अमितगति, योगसार ९-५१` — **cite it in part 10**, in one short line. That is the edition's own attribution,
not a guess, and it is the best citation available for this text.

Where it says **स्रोत संस्करण में नहीं दिया गया**, the edition itself gives no source. Then say only that the
line is a quotation and leave it there. **Do not supply a source the apparatus does not give**, however
familiar the verse looks — about a third of the entries are unattributed in the original and that is a fact
about the edition worth preserving.

Where the entry carries a warning that the apparatus records the verse on a different printed page, the same
verse is probably quoted twice in the book. Check that the words really match your § before citing it.

If a quotation in your range is absent from that file altogether, treat it as unattributed.

## When you split a समास, apply the fount's confusion table too

The extraction pass corrects the systematic misprints it can see, but a compound can hide one from it and
reach you intact. **If a split only works by reading a `म` as something else, stop and try `प्र` first.**

A real case from this ग्रन्थ: `शुद्धात्मतत्त्वभावनामतिकूलेषु` was split as भावना + **अतिकूल**, and
`सुखामृतमतिबन्धकैः` as अमृत + **अतिबन्धक**. Both "work" in the sense that they yield the right general idea.
But **neither अतिकूल nor अतिबन्धक is a Sanskrit word**, while `प्रतिकूल` occurs eight times and
`प्रतिबन्धक` four times elsewhere in this very corpus. And the splits do not even account for the printed
letters: भावना + अतिकूल would give *भावनातिकूल*, with no `म` at all.

Two tests, both cheap:

1. **Is the member you produced actually a word?** `अतिकूल` is not. `प्रतिकूल` is. A split that invents
   vocabulary is wrong however well the sense comes out.
2. **Does your split use every printed letter, and no more?** If a `म` is left unexplained, you have not
   split the compound — you have replaced it.

The sense usually survives a wrong split, which is exactly why this is dangerous: in the case above the
Hindi still said "obstructing", but it had acquired an "अत्यन्त" the Sanskrit never licensed. **A wrong
split leaks small additions into the Hindi**, and those are the hardest errors to see later.

## The other parts

### 3. अन्वय
The words **of the अपभ्रंश दोहा**, as printed, rearranged into straight prose order — कर्ता, then
कर्म/विशेषण, then क्रिया. Do not substitute Sanskrit and do not add words the दोहा lacks; a genuinely
implied word goes in `( )`.

### 4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ)
Every पद of the अन्वय, in the अन्वय's order, one per line:

```
- **कम्मु** (कर्म, द्वितीया ए.व.) = कर्म को
- **मुएविणु** (मुक्त्वा, ल्यबन्त) = छोड़कर
- **संगु** (संगम्, द्वितीया ए.व.) = परिग्रह को — बाह्य एवं आभ्यन्तर दोनों
- **॥३९॥** = दोहा-क्रमांक
```
The Sanskrit in `( )` should be the form the **printed छाया** gives wherever the छाया covers that word —
this edition prints the छाया, so use it rather than inventing a correspondence. Split compounds with `+`.
Give the grammatical form wherever it decides the sense.

### 7. जैनागम के अनुसार विस्तृत व्याख्या
4–8 bullets, each 120–220 words, each with a bold sub-heading: what this दोहा establishes and why it
stands here; the doctrine behind it with the सूत्र or ग्रन्थ it rests on; the opposing position stated
fairly where there is one; cross-links (`देखें परमात्मप्रकाश 1.17`); and an honest limit where the दोहा
is compressed or the टीका supplies what the दोहा does not.

**परमात्मप्रकाश is an अध्यात्म text**, not a न्याय text. Its argument moves through experience —
बहिरात्मा / अन्तरात्मा / परमात्मा, the आत्मा mistaken for the body, शुद्धोपयोग — and its reader is being
pointed at something, not only informed. Let the व्याख्या keep that register without becoming vague.

### 8. सरल उदाहरण
2–3 everyday analogies a श्रावक can follow. State the दृष्टान्त, then the दार्ष्टान्तिक — what maps to
what — and **where the analogy stops**. The टीका and भावार्थ often supply one; build on theirs first.
If the दोहा is purely enumerative: `इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।`

### 9. तुलनात्मक तालिका / चार्ट
One markdown table, 3–7 rows, of whatever kind the दोहा calls for — भेद-प्रभेद, the three आत्मा, निश्चय
against व्यवहार, दृष्टान्त ↔ दार्ष्टान्तिक. If none helps: `इस अनुच्छेद हेतु तालिका आवश्यक नहीं।`

### 10. सन्दर्भ एवं पाद-टिप्पणी
**1 to 3 one-line bullets, no blank line between them.** Printed at dictionary size. Only: the source of
a verse quoted in the टीका (with ग्रन्थ and number, `लगभग`/`सम्भवतः` when unsure, nothing at all rather
than a guess); a one-line note where the Sanskrit and the printed हिन्दी diverge, or where a समास admits
two splits, or where part 1 carries `[अस्पष्ट]`. Otherwise:
`मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।`

---

## Before writing a §, read

1. the § itself in `parts/` — all of it, especially every `(Tn)` segment of the टीका;
2. the §§ immediately before and after, so your cross-links and your "why here" are real;
3. for the first § of your range, the preceding § in full, since श्री ब्रह्मदेव's टीका often carries an
   argument across several दोहा.

## Context — where the ग्रन्थ stands

**परमात्मप्रकाश**, अपभ्रंश दोहा, by **श्री योगीन्दुदेव**, with **श्री ब्रह्मदेव's** संस्कृत टीका. It is
framed as the answer to a question put by **भट्ट प्रभाकर**, and its subject is the three-fold आत्मा:

| | |
|---|---|
| **अधिकार 1** (दोहा 1–123 + extras) | त्रिविध आत्मा — बहिरात्मा, अन्तरात्मा, परमात्मा — and the nature of the शुद्धात्मा |
| **अधिकार 2** (दोहा 1–214 + extras) | मोक्ष, मोक्षमार्ग and मोक्षफल |
| **योगसार** (दोहा 1–108) | the same teaching compressed, by the same आचार्य |

The ग्रन्थ stands in श्री कुन्दकुन्दाचार्य's line and the टीका quotes समयसार, प्रवचनसार, पञ्चास्तिकाय,
तत्त्वार्थसूत्र, इष्टोपदेश, समाधितन्त्र and others.

## Style — binding

- शास्त्रीय, clear हिन्दी. English digits in your prose — Devanagari digits **only** inside quoted
  मूल / छाया / टीका, where `॥ ३९ ॥` stays as printed.
- **Never write any sect name** (बीसपंथ / तेरापंथ or any sub-sect label) anywhere, for any reason.
- **Jain आचार्य are never named bare**: `श्री योगीन्दुदेव`, `श्री ब्रह्मदेव`, `आचार्य श्री कुन्दकुन्द`,
  `श्री अमृतचन्द्र स्वामी`, `श्री पूज्यपाद स्वामी`. Write the honorific **at source**, including when a
  Hindi case-ending follows (`श्री योगीन्दुदेवने`, `श्री ब्रह्मदेवकी`). Non-Jain opponents are plain.
- **No working-process language anywhere**: no "बैच", "इस सत्र", file names, scan pages, "उपयोगकर्ता",
  no mention of other agents or of how the book was made.
- **तत्त्वार्थसूत्र: use the दिगम्बर (सर्वार्थसिद्धि) recension.** 5.29 सद्द्रव्यलक्षणम् · 5.30
  उत्पादव्ययध्रौव्ययुक्तं सत् · 5.31 तद्भावाव्ययं नित्यम् · 5.38 गुणपर्यायवद् द्रव्यम्. If you find
  yourself writing 5.29 for उत्पाद-व्यय *and* 5.38 for गुण-पर्याय you have mixed the two recensions.
  When unsure of a number, cite the सूत्र text and the अध्याय alone — always safe, always useful.
- **Never fabricate** a citation, a verse number or a doctrine. "लगभग" / "सम्भवतः" where unsure; silence
  where you do not know. This book will be cited.

## Writing the files

**Write each § as its own file, immediately, one at a time** — `addenda/s20390.md` for `§20390`. Do not
accumulate several and write at the end; a response is capped at 64,000 output tokens.

## Report back (under 250 words)

The § keys completed; **every place the Sanskrit टीका and the printed हिन्दी diverged, and which you
followed**; every समास you split against the obvious reading and why; any `(Tn)` segment whose Sanskrit
you could not construe, named explicitly; any citation you wanted but could not verify; and confirmation
that every § in your range has a file and every `(Tn)` tag has a Hindi line.
