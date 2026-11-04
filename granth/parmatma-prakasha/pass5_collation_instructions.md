# Pass 5 — collation of our transcription against the printed page

*Working document. Nothing here goes into the book.*

## Why this pass exists

An audit of the printed Hindi (pass 4, reports `verify/h*.md`) checked our files against the scans and found
that **our own transcription is not faithful to the print** in many places:

- in ~74 § of परमात्मप्रकाश, part 5 lacks the printed opening sentence (the पातनिका, `आगे … कहते हैं–`);
- whole printed passages are missing or misplaced in part 5 — all of printed p. 102 (§11090), p. 104 (§11110),
  p. 139 (§20230), p. 246 (§21300), ~14 lines of p. 276 (§21630); the अर्थ of §10140; the end of §10760's
  भावार्थ; a sentence in §21630 that is **not in print at all**;
- in part 6 (the संस्कृत टीका) words are miscopied, some reversing the sense: §10010 T17 `पुनः शुद्ध…` where the
  print has `पुनरशुद्धनिश्चयनयेनेति`; §20360 `तदधस्तान्निषेधकम्` for printed `तन्नाधस्तान्निषेधकम्` (a lost `न`);
  §21114 T6 `परमधर्मरहितैः` for printed `परमधर्मरतैः`; §20250 T4 a lost `न`; whole sentences missing at §10740,
  §10960, §20440, §21080.

**Your job: make parts 1, 2, 5 and 6 of your batch files say exactly what the printed page says.** You are a
copyist checking a copy against its original, line by line. You are not an editor.

## Your files

You own the `parts/` batch files named in your assignment, and only those — other agents are editing the
others at the same time. **Do not touch `addenda/`, `backmatter/`, `frontmatter/`, or any other batch file.**

Each batch file's name gives its scan range (`batch05_p0198-0206.md` = scans 198–206). Render pages with:

```python
import fitz                                    # pymupdf
d = fitz.open('mool/Parmatmaprakash_and_Yogsara_001876.pdf')
p = d[scan - 1]; r = p.rect
# whole page at 150 dpi to orient, then the Sanskrit block and the Hindi block separately at 250–300 dpi:
p.get_pixmap(dpi=280, clip=fitz.Rect(0, 0, r.width, r.height * 0.55)).save(r'<scratch>\s.png')
```

Printed page = scan − 161 (the `(पृष्ठ N)` markers in the files). Work page by page through **every** scan in
your range — do not sample. Write images only to your scratch directory.

## What to compare

For every § in your files:

| part | compare with |
|---|---|
| `## 1.` मूल पाठ | the bold अपभ्रंश दोहा, including `॥ N ॥` |
| `## 2.` संस्कृत छाया | the छाया lines under the दोहा |
| `## 5.` हिन्दी अनुवाद | **everything below the rule** for that दोहा: the पातनिका (`आगे …`), the अर्थ with its `[bracketed]` lemmas, and `**भावार्थ:**` |
| `## 6.` टीका | the dense Sanskrit above the rule, word by word |

Read the scan; read our text; fix every difference **in favour of the print**.

**Hindi spelling is the print's.** This edition writes `आत्माको`, `उनकर`, `सो`, `होवे`, `तिनकर`, `जावे`, joined
postpositions, `हुये`. Reproduce it. Do not modernise, do not "correct" grammar.

## What you must NOT change

1. **Documented corrections of the fount.** `verify/pass1_flags.md` lists readings where the printed glyph was
   deliberately read as something else — above all **`प्र` printing as a plain `म`** (`मतिपक्ष` → `प्रतिपक्ष`,
   `मत्यय` → `प्रत्यय`, `सर्वमकारेण` → `सर्वप्रकारेण`), `ल` for `त्व`, `श्च` for `ञ्च`, a lost रेफ. Read its
   "Already resolved" table and every `RESOLVED →` entry for your § before you start. **Those stay as they are.**
   If you meet a new instance of the same glyph pattern, apply the same convention and log it.
2. **The edition's own errors.** If the print itself is wrong (a misprint, a dropped `न`, a wrong word in the
   Hindi), **reproduce the print**. Pass 4 has listed the edition's errors for a separate परिशिष्ट; the copy must
   show what the edition actually printed. Example: §21660's printed `परमोपदेश` (for परमोपशम) — our copy had
   silently "corrected" it; restore `परमोपदेश`.
3. **`(?)` marks** printed by the editor — keep them.
4. **Structure.** The `§NNNNN — title (…)` line, the `## N.` headings, the `(पृष्ठ N)` markers, the `---`
   separators. Do not change titles.
5. **The `(Tn)` segment tags.** Never renumber, merge, split or delete a tag — `addenda/` is aligned to them.
   - Missing टीका text goes **into the segment where it belongs in sequence** (the end of the preceding segment, or
     the start of the following one, whichever keeps a question with its answer).
   - Text that belongs to a different § (§21190's part 5 holds a compound that belongs to §21200 T4): move it
     to its right place — **only if both § are in your files**; otherwise log it for the compiler.

## Leads

Every `verify/h*.md` report ends with a **प्रतिलिपि-दोष** section, and many also list part-6 copying errors in
an uncounted section, each with the exact printed reading. Read the entries for your § first — they are leads,
not authority: **confirm each on the scan** before applying it. Then do the full page-by-page comparison: the
audit looked at part 6 only incidentally, so most part-6 errors are still unfound.

## Log every change

Write `verify/c<your batch numbers>.md` (e.g. `verify/c05-06.md`), incrementally as you go:

(The rows below only illustrate the format; their content is invented.)

```markdown
# प्रति-मिलान — batch05, batch06 (scan 198–215)

| § | भाग | Tn | हमारी प्रति (पहले) | मुद्रित (अब) | scan | अर्थ-प्रभाव |
|---|---|---|---|---|---|---|
| 10370 | 6 | T3 | `…स्फुटं निश्चितम्…` | `…स्फुटं निश्चितं…` | 199 | नहीं |
| 10420 | 5 | — | (पातनिका नहीं थी) | `आगे … कहते हैं–` | 203 | नहीं |
| 10440 | 6 | T4 | `…तदधस्तान्निषेधकम्…` | `…तन्नाधस्तान्निषेधकम्…` | 205 | **हाँ** — निषेध लौटता है |
```

**अर्थ-प्रभाव = हाँ** whenever the change could alter what our own Hindi of that segment (in `addenda/`, part 6)
or a part-10 note should say: a word with different meaning, a restored `न`, a restored clause or sentence,
a changed case. Spelling, punctuation, sandhi spacing and restored पातनिका are **नहीं**. Be generous with हाँ —
an Opus pass will rework every हाँ row and nothing else.

For very long restorations (a whole page of Hindi) put `(पूरा अनुच्छेद पुनर्स्थापित, N पंक्तियाँ)` in the table
instead of quoting it.

End the log with: `पृष्ठ जाँचे: <list of scans> | परिवर्तन: N | अर्थ-प्रभाव हाँ: M` and a short list of anything
you could not settle (`अनिर्णीत`), with the reason.

## Rules

- Run python with `PYTHONIOENCODING=utf-8`. Write files UTF-8.
- Never write बीसपंथ/तेरापंथ.
- If a reading is genuinely illegible even at 300 dpi, leave our text, and list it as अनिर्णीत.
- Before finishing, re-read your files' structure: every § still has its `## 1.`, `## 2.`, `## 5.`, `## 6.` and its
  `(Tn)` tags in unbroken order 1…n.
