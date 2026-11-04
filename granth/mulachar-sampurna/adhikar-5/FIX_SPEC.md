# Pass-3 fixer spec (मूलाचार अधिकार 5)
*Working document.*

You apply ONE audit report `verify\v<range>.md` to this chapter's files. For every finding:
- **त्रुटि / लोप / वर्धन** → apply the auditor's `सुझाया हिन्दी` (or an equally faithful wording of yours) in `addenda\s<key>.md`.
  Before applying, read the Sanskrit in `src\s<key>.md` yourself; if you disagree with the auditor, do not apply — log why.
- **Transcription errors confirmed on the scan** (printed letters differ from `src`) → correct the Sanskrit in BOTH `src\s<key>.md` AND the
  matching § in `parts\batch*.md` (part 1 / part 6 / part 11 lines), letter for letter as printed. Then remove any note in the addendum that
  blamed the print for what was our slip, and adjust Hindi that rested on the wrong reading.
- **Printed misprints** (the print itself is wrong) → keep the printed form in src/parts; the addendum's part 10 notes the correct form in one line.
- **सन्देह** → apply if the auditor's preferred reading is clearly better on the Sanskrit; otherwise add a short note in part 10.
- **Footnotes**: remove every false "कोई पाद-टिप्पणी नहीं"; mention meaning-relevant printed variants in part 10 (one line each).
- **9-क tags**: split mixed items so a suggestion never sits under `[आगम-सम्मत]`.
Rules: never name a sect; no working-process words in the book files; keep part order/headings; edit with small Edit calls.
Log every change (and every rejected suggestion with reason) to `verify\x_applied_<range>.md`: `- §key · part · before → after · basis`.
Report: counts applied / rejected, and any finding you could not resolve.
