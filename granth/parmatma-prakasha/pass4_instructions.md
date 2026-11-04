# Pass 4 — मुद्रित हिन्दी (अर्थ एवं भावार्थ) का परीक्षण

*Working document. Nothing here goes into the book. Your report feeds a new परिशिष्ट that the compiler writes.*

## What you are doing

Every § of this book carries, as **part 5 (`## 5. हिन्दी अनुवाद`)**, the **Hindi printed in the source edition**,
copied word for word:

- **परमात्मप्रकाश (keys 10010–22140):** the अर्थ (the paragraph that opens part 5, often beginning `आगे …`) and
  the **`**भावार्थ:**`** paragraph — पं. दौलतरामजी's भाषा-वचनिका as printed in A. N. Upadhye's edition.
- **योगसार (keys 30010+):** the `अर्थ—` paragraph — पं. डॉ. जगदीशचन्द्र शास्त्री's Hindi translation.

Part 5 has **never been audited**. The earlier pass 3 checked only *our own* Hindi of the टीका (part 6) and was
told to leave part 5 exactly as printed. Part 5 stays exactly as printed this time too — **you do not edit it**.
Your job is to find where that printed Hindi **misstates, omits or contradicts** what it is translating, so the
reader can be warned in a separate परिशिष्ट at the back of the book.

## What to read, for every § key in your range

- `parts/<batch>.md` — the § block: `## 1.` अपभ्रंश दोहा, `## 2.` संस्कृत छाया, **`## 5.` the printed Hindi
  (अर्थ + भावार्थ)**, and for परमात्मप्रकाश `## 6.` श्री ब्रह्मदेव's संस्कृत टीका in `(T1)`, `(T2)` … segments.
- `addenda/s<key>.md` — our own parts 3, 4 (अन्वय, अन्वयार्थ), 6 (टीका का हिन्दी), 7–10. **Part 10 already
  records many places where the printed Hindi differs from the टीका** (over a hundred across the book).

**Read the Sanskrit/अपभ्रंश first and form your own reading, then read part 5.** If you read the Hindi first you
will find yourself agreeing with it.

What the printed Hindi is answerable to:
- The **अर्थ** renders the दोहा. Check it against the दोहा and its छाया (and, where the छाया and टीका differ,
  the टीका is श्री ब्रह्मदेव's own gloss — note which the अर्थ follows).
- The **भावार्थ** renders/paraphrases the **टीका**. Check its doctrinal statements, its नय-attributions, its
  negations, its हेय/उपादेय conclusions and its quoted verses against the टीका segments.
- **योगसार** has no टीका: check the अर्थ against the दोहा and छाया, and against `## 6. मुद्रित पाठभेद` where a
  variant decides the sense.

## What counts as a finding

| प्रकार | meaning |
|---|---|
| **त्रुटि** | The printed Hindi says something the source does not, or contradicts it: a wrong नय (शुद्ध/अशुद्ध निश्चय, सद्भूत/असद्भूत व्यवहार), a dropped or added negation, हेय and उपादेय swapped, a word or case misread, a quality attached to the wrong noun. |
| **लोप** | A clause, qualifier or point of the source with no counterpart in the Hindi, **where the loss changes or weakens the sense** (not mere brevity). |
| **वर्धन** | The Hindi asserts doctrine not in the source **in a way that could mislead**. Daulatram's वचनिका is a free भाषा-टीका and often expands — expansion that the टीका supports is *not* a finding. |
| **सन्देह** | Defensible, but another reading is at least as good and a reader would be served by knowing. |

**Idiom is not error. Old Hindi spelling and grammar (`कर`, `सो`, `जो`, `तिनकर`, `हैं सो`, joined words like
`आत्माको`) is not error. A free भावार्थ is not error. Brevity is not error.** You are auditing *sense*.

**Do not convict the edition of an error it did not make.** In this book's own history a note once faulted the
edition for rendering `बाहुडि` as "फिरसे" — but `बाहुडि` *means* again. Another wrongly read योगसार 36's `एक`
as the numeral when it is "alone". A printed charge carries authority a reader cannot check. **Inventing one
finding is worse than missing one.** If unsure, call it सन्देह and say why.

**Ask whether the Hindi could be true of its subject.** A rendering that makes the सिद्ध subject to karma, the
परमात्मा dependent on the body, or a हेय thing उपादेय, is wrong however well it reads.

## Before you charge the edition: is it our copying error?

Part 5 was transcribed from scans. A wrong-looking word may be **our** typo, not the edition's. If a finding
turns on one or two words, check the scan:

```python
import fitz                                   # pymupdf
d = fitz.open('mool/Parmatmaprakash_and_Yogsara_001876.pdf')
scan = printed_page + 161                     # 1-based scan number; printed page is the "(पृष्ठ N)" in part 1/2
d[scan - 1].get_pixmap(dpi=200).save(r'<your scratch dir>\p.png')   # then view it; crop with clip= if needed
```

Report a copying error under **प्रतिलिपि-दोष** (see output) with the exact print reading — those get fixed in
the text, not listed as the edition's fault. Do not write images into the project folder.

## Already recorded — include, but do not re-argue

If part 10 of a § already notes that the printed Hindi differs from the टीका, **list it as a finding anyway**
(the परिशिष्ट must be complete in one place), mark it `(भाग 10 में पूर्व-अंकित)`, and check the note is right.
If you think the part-10 note itself is wrong, say so.

## Output

One file: `verify/h<first-key>-<last-key>.md`. Write it incrementally (after the first few §, then append), so a
long range is never lost.

```markdown
# मुद्रित हिन्दी (अर्थ/भावार्थ) परीक्षण — §<first> से §<last>

## निष्कर्ष
- परीक्षित §: 23
- त्रुटि: 2 | लोप: 1 | वर्धन: 0 | सन्देह: 3 | प्रतिलिपि-दोष: 1

## निष्कर्ष-विवरण

### §10360 (दोहा 1.36, पृष्ठ 38) — भावार्थ — त्रुटि
- **स्रोत:** (T3) …परमात्मभावनाविपक्षभूतैः रागद्वेषमोहैः समुपार्जितैः कर्मभिरशुद्धनिश्चयनयेन…   ← exact quote
- **मुद्रित हिन्दी:** …                                                                   ← exact quote from part 5
- **दोष:** one or two sentences, with the grammatical/doctrinal reason.
- **शुद्ध अर्थ:** a complete corrected Hindi sentence a reader can substitute.

## प्रतिलिपि-दोष (हमारी प्रति बनाम मुद्रित पृष्ठ)
- §10450, पृष्ठ 45: हमारी प्रति `…` — मुद्रित `…` (scan 206 पर देखा)

## गणना
त्रुटि: 2 | लोप: 1 | वर्धन: 0 | सन्देह: 3 | प्रतिलिपि-दोष: 1
```

Say **अर्थ** or **भावार्थ** in each heading. Give **शुद्ध अर्थ** for every त्रुटि and लोप; for सन्देह give the
alternative and which you prefer. A clean § gets no entry — the report lists problems, not confirmations.

## Rules

- Audit **only** the § keys in your range. **Do not edit any file in `parts/`, `addenda/`, `backmatter/`.**
- Quote Sanskrit and Hindi exactly as the files have them.
- Never write बीसपंथ/तेरापंथ, and do not use sect names (दिगम्बर/श्वेताम्बर) in your wording.
- Jain आचार्य names with honorifics (श्री योगीन्दुदेव, श्री ब्रह्मदेव); English numerals.
