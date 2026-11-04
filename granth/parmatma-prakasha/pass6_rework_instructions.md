# Pass 6 — rework our व्याख्या where the corrected transcription changes it

*Working document. Nothing here goes into the book.*

## Background

Pass 5 collated `parts/` against the printed page and corrected our transcription. Each change is logged in
`verify/c*.md`, with a column **अर्थ-प्रभाव**. Separately, the pass-4 reports `verify/h*.md` list **part-10
notes that are wrong** because they rested on our copying errors (they blame the edition for a difference that
was really ours), and a few of our own part-6/7 readings and § titles that the print contradicts.

`addenda/s<key>.md` holds our own व्याख्या for each §: parts 3, 4 (अन्वय, अन्वयार्थ), **6 (हिन्दी of the टीका,
segment by segment, tagged `(T1)`, `(T2)`… to match `parts/`)**, 7–10. Part 10 records पाठ-टिप्पणी, including
where the edition's printed Hindi differs from the टीका.

**Your job: make our व्याख्या agree with the corrected text, for the § keys in your range — nothing more.**

## What to do, per § in your range

Collect the work items:
1. every row in `verify/c*.md` for this § with **अर्थ-प्रभाव = हाँ**, **and every row in भाग 1 or 2 whatever its
   अर्थ-प्रभाव** — a changed मूल or छाया word must be carried into part 3 (अन्वय) and part 4 (अन्वयार्थ), which
   quote them word by word (and into any part-7 quotation of that word);
2. every entry in `verify/h*.md` for this § that says a **part-10 note is wrong / stale / rests on our copying
   error / overstated**, or that our part 6/7 reading or § title is contradicted by the print;
3. restored part-5 text (a पातनिका, a whole restored अर्थ/भावार्थ paragraph) **only** where a part-10 note claimed
   the printed Hindi lacked something that it in fact has (e.g. §21780: "the printed Hindi gives no अर्थ for
   178" — it does).

For each item:
- **Part 6 Hindi:** re-render the affected `(Tn)` line from the **corrected** Sanskrit in `parts/`. Read the
  Sanskrit first and construe it yourself. Change only what the correction requires; keep the line's style and
  the tag. If a restored sentence was appended into a segment, the Hindi of that segment must now cover it.
- **Part 10 notes:** delete a note whose basis has gone (it charged the edition with our error). Rewrite a note
  that was partly right. If the corrected text now *creates* a genuine difference worth noting, add a short note.
  Never leave a note asserting a reading the corrected `parts/` no longer has.
- **Parts 3, 4, 7, 8, 9:** fix only a statement that now contradicts the corrected text (e.g. an अन्वयार्थ built on a
  miscopied मूल word, or a part-7 bullet quoting the miscopied phrase). Do not polish.
- **§ title** (the `§NNNNN — …` line in `parts/` — the one place in `parts/` you may edit): only if an h-report
  says the print contradicts it, and only the wording after `— ` up to `(`.

Use `check_stale_notes.py` (read it first) on your range when done, if it applies.

## Rules

- Edit only `addenda/s<key>.md` for keys in your range (and § title lines as above). Do not touch `backmatter/`.
- Do not re-audit the whole व्याख्या; touch only what an item requires. Record nothing about the process in
  the book text — no "pass", "audit", "प्रतिलिपि", "स्कैन" in addenda.
- Jain आचार्य names with honorifics; no sect names; English numerals outside quoted मूल/संस्कृत.
- Log what you changed in `verify/r<first>-<last>.md`: `§ | भाग | Tn/टिप्पणी | क्या बदला | क्यों`.
  End with `संशोधित §: N | परिवर्तन: M`.
