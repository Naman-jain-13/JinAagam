# Pass-3 fixer spec (प्रमाणप्रमेयकलिका)
*Working document.*
You apply ONE audit report `verify\v_linesNN-MM.md` (and, for lines 01–04, also `verify\sweep_tatra_lines01-04.md`) to:
- `parts\batch*.md` — the Sanskrit (part 6 `(Tn)` lines, part 11 footnotes, § titles);
- `addenda\s<key>.md` — the Hindi parts.
For every finding:
- **Transcription errors confirmed on the scan** (e.g. printed `तन्न`/`यन्न` written `तत्र`/`यत्र`; a dropped `अ`; `व्यापत्तेः` normalised to `व्याप्तेः`) → correct the Sanskrit in `parts\` letter for letter as printed; then fix every Hindi line/note in the addendum that rested on the wrong reading, and DELETE every bracket/part-10 note that blamed the print for our slip.
- **[अस्पष्ट] the auditor could read on the scan** → fill it in parts only where the auditor marks the reading clear; translate the recovered words. Moderate-confidence readings: fill only if two auditors agree or the scan crop in the report is unambiguous; otherwise keep [अस्पष्ट] and add a part-10 line "सम्भावित पाठ …".
- **त्रुटि / लोप / वर्धन** in Hindi → apply the auditor's replacement (or an equally faithful wording) after reading the Sanskrit yourself; disagreeing → do not apply, log why.
- **Footnotes (systemic gap):** pass 1 skipped the editor's Sanskrit footnotes. Where the auditor reports a footnote that names the speaker or settles a meaning, correct parts 6/7 accordingly and mention it in part 10 in ONE short line of your own ("सम्पादक की पाद-टिप्पणी के अनुसार यहाँ वक्ता …"). Do NOT copy the modern editor's notes verbatim into the book; do not add them to part 11. Remove every false "कोई पाद-टिप्पणी नहीं" and any part-7 sentence the footnotes prove false.
- **Titles** reported wrong → rewrite the § title line in parts (keep the parenthesis `(प्रमाणप्रमेयकलिका, परीक्षा K, अनुच्छेद N, मुद्रित पृष्ठ P)` intact).
- **Citations** reported wrong → correct or hedge (लगभग/सम्भवतः) or drop.
- **9-क tags**: suggestions never under `[ग्रन्थ-सम्मत]`.
Rules: never name a sect; no working-process words in book files; small Edit calls, re-read the file before each Edit; touch only the § of your report.
Log every change (and every rejected suggestion with reason) to `verify\x_applied_linesNN-MM.md`: `- §key · part · before → after · basis`.
Report: counts applied / rejected, and anything unresolved.
