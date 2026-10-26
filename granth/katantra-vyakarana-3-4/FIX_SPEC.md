# Pass-3 fixer spec (कातन्त्र, अध्याय 3–4)
*Working document.*

You apply ONE audit report `verify/v_<tag>.md` to:
- `parts/batch*.md` — the Sanskrit (part 6 `(Tn)` lines, § titles);
- `addenda/s<key>.md` — the Hindi parts (6, 7, 7-क, 8, 9, 9-क, 10).

For every finding:
- **A. पाठ-सुधार (Sanskrit vs scan)** → correct `parts/` **letter for letter as the auditor reads the print**. A correction marked `सम्भावित` (not `स्पष्ट`) is applied only if the auditor's description of the crop is unambiguous; otherwise keep the old text and add a part-10 line `सम्भावित पाठ …`. After correcting a printed form, fix **every** Hindi line, bullet, table row, derivation and drill in the addendum that rested on the old reading (parts 6, 7, 7-क, 8, 9, 9-क, 10), and DELETE every note that blamed the print for our slip.
- **`[अस्पष्ट]` the auditor could read on the scan** → fill it in `parts/` only where the auditor marks the reading `स्पष्ट`; translate the recovered words; otherwise keep `[अस्पष्ट]` and add a part-10 line "सम्भावित पाठ …".
- **B. त्रुटि / लोप / वर्धन** in Hindi → apply the auditor's replacement (or an equally faithful wording) after reading the Sanskrit yourself; if you disagree, do not apply, and log why.
- **सन्देह** → apply when the auditor's reading is at least as good and the replacement is ready; otherwise add a one-line part-10 note.
- **Derivations/drills** reported unsound → replace by a sound one (derive only with rules that exist in the book or mark `(सूत्र उपलब्ध पाठ में नहीं)`), never by an invented sūtra number.
- **Titles** reported wrong → rewrite the § title line in `parts/` (keep the parenthesis `(कातन्त्र, अध्याय A, पाद P, सूत्र N, मुद्रित पृष्ठ M)` intact; **never put parentheses inside it**).
- **Citations** reported wrong → correct or hedge (`लगभग`/`सम्भवतः`) or drop.
- **9-क tags**: suggestions never under `[ग्रन्थ-सम्मत]`; exactly one tag per bullet.
- Printed misprints that the auditor says are *as printed* stay as printed in `parts/` (noted in part 10), the Hindi follows the rule's sense and says so.

Rules: never name a sect; no working-process words in book files; never rename or renumber a § key; small Edit calls, re-read the file before each Edit; touch only the § of your report. Do not edit `src/` by hand: run `python make_src.py` ONCE at the very end of your work (it rebuilds all `src/` from `parts/`).

Log every change (and every rejected suggestion with reason) to `verify/x_applied_<tag>.md`: `- §key · part · before → after · basis`.

Report (under 200 words): counts applied / rejected, and anything unresolved.

**Vol 2 additions:** the title's `मुद्रित पृष्ठ` and अध्याय/पाद/सूत्र numbers are corrected exactly as the auditor reads them from the running head. Never fill text the scan lost (`[स्कैन में … अनुपलब्ध]`, tail-only §); the Hindi must say what survives. A finding that depends on a page you cannot verify: apply only if marked `स्पष्ट`. Do NOT run make_src.py (the lead rebuilds `src/` once at the end). Fixers run concurrently: touch only the keys in your report.
