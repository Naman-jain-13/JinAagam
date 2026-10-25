# मूलाचार उत्तरार्ध (अधिकार 8–12) — progress / HOW TO RESUME

Scan: `mool/Mulachar_Uttarardh_Aryika_Jnanmati.pdf`, 456 pages. Same independent 3-pass pipeline as
`mulachar-5` (see pass1/2/3_instructions.md): pass 1 Sanskrit+Prakrit only → `make_src.py` → pass 2
from `src/` only → pass 3 audit (scans allowed, above the rule only; `crop_above_rule.py`) → fixers →
`apply_titles.py` → build.

Page map (from a dedicated boundary-mapping pass): scan 1–34 front matter/कण्ठहार/भूमिका/TOC (excluded);
scan 35–454 = printed 1–420 = main body (offset 34); scan 455–456 = publisher back matter (excluded).
**पूर्वार्ध has 7 अधिकार (1–7), not 5** — अधिकार 6 (पिण्डशुद्धि) and 7 (षडावश्यक) are not yet done anywhere
in this project; this उत्तरार्ध volume is अधिकार **8–12 only** — द्वादशानुप्रेक्षा (683–768), अनगारभावना
(769–893), समयसार (894–1017), शीलगुण (1018–1043), पर्याप्ति (1044–1249, ends the whole ग्रन्थ).

## Status (2026-10-26) — पास 1 DONE, fully verified
- **40 batches written** (`parts/batch01…batch40.md`), scan 35–425, गाथा 683–1249.
- **Two numbering errors found and fixed** during a full continuity check (this book's scan font has a
  confirmed, recurring ९/६ glyph confusion — cross-check any suspicious digit against known-good
  reference digits on the same page before trusting it, in this pass or any later one):
  - batch16 (scan 181–190): whole batch mislabeled गाथा 870–887 instead of true 970–987 (also fixed 6
    genuine transcription errors found while re-verifying).
  - batch33 (scan 348–357): one गाथा mislabeled 1169 instead of true 1199.
  - batch01 (scan 35–44): its own last 6 गाथा were mislabeled 690–696 (off-by-10 cascade from
    misreading two closing numerals) — true values are 700–706; fixed in place, no content lost.
  - batch26 (scan 278–287): "गाथा 1067–1069" were actually a **genuine printer erratum** — the source
    book itself prints 1097/1098/1099 as 1067/1068/1069 (confirmed: both the Sanskrit mūla AND the
    (ignored) Hindi stream show the same wrong digits; गाथा 1067–1069's real content sits correctly
    elsewhere at पृष्ठ 224–225). Fixed: renumbered to 1097–1099, restored 3 dropped opening पातनिका,
    added part-11 footnotes documenting the print erratum.
- **One genuine, unexplained, confirmed printed gap: गाथा 690–699 (10 गाथा) do not exist in this
  edition** — verified directly against the scan (प.4→5 jumps ॥६८९॥ → ॥७००॥), no footnote explains it
  (unlike the other known jump pattern in this book). **Do not try to "find" or write these — they are
  not in the source.** True गाथा count for this volume: 557 (not 567).
- `src/` built: `python make_src.py` → 538 files (§ keys; several keys cover 2–4 गाथा via merges, so
  538 keys ↔ 557 गाथा).
- Full continuity re-check after fixes: zero gaps (besides the confirmed 690–699), zero duplicates.

## Status (2026-10-25) — BOOK COMPLETE, docx+PDF built
- **पास 2** addenda: all 538 § written independently from `src/` only. शीर्षक line was missing from
  395/538 files due to an ambiguous instruction sentence (fixed in `pass2_instructions.md`); all fixed
  via 10 corrective batches; `apply_titles.py` confirms 538/538 applied.
- **पास 3** audit: 18 parallel batches covered all 538 §, independent Sanskrit↔Hindi cross-check per
  `pass3_instructions.md`. Found and fixed (via 18 parallel fixer batches, applying every त्रुटि/लोप plus
  two systemic sweeps across *all* 538 keys regardless of what each audit batch explicitly logged):
  dropped/reversed negations, wrong compound splits, a fabricated गाथा cross-reference, mis-split
  प्रकृति compounds (अगुरुलघु), γāthā-number typos, table-count errors, and two **systemic** issues
  present book-wide: (a) addenda's part 10 falsely claiming "कोई पाद-टिप्पणी नहीं" when `src/`'s own
  §11 had a real footnote — found in nearly every audited range, not just the ones that logged it; (b)
  9-क bullets (esp. "परिस्थिति-विशेष"/"परीक्षण"/"चर्चा" types) missing their required [सुझाव]/[आगम-सम्मत]
  tag. Both swept and fixed across the whole book, not just flagged instances.
- `groups.json` densification turned out to be unnecessary — `finalize_big.py`'s banner-fallback
  mechanism (nearest preceding Heading 1 substituted into the running header) already handles sparse
  groups.json safely; the 5 अधिकार-level banners were sufficient.
- **Build**: `build_docx.js` → `postprocess_docx.py` ran clean. `finalize_big.py` hit a genuine,
  reproducible Word bug: certain regions (citation-within-citation sub-blocks, 9-क-bullet-dense
  sections) made Word's PDF export hang/crash past a **content-density** threshold that varied by
  region (~151 children in one spot, ~75-76 in another — bisected and confirmed both times, see
  `bisect_chunk.py` pattern in scratchpad if this recurs). Fixed by lowering `MAX_CHILDREN` 190→20
  (539 small chunks, max 48 children, safely under both found thresholds) and shortening the
  per-chunk export watchdog (1200s→150s) so a hang recovers in ~3 min instead of 20. Also cleared a
  stale Word crash-recovery state (`HKCU\...\Word\Resiliency`, stale `.asd`/`.wbk` autorecovery files)
  that was silently showing a "Start in Safe Mode?" dialog on every headless launch, blocking all
  COM automation until cleared.
- **Final output**: `vyakhya/Mulachar_Uttarardh_Adhikar8-12_Vyakhya.docx` (1.8 MB) and
  `vyakhya/Mulachar_Uttarardh_Adhikar8-12_Vyakhya.pdf` (1563 pages, 70.9 MB — front matter+TOC pp.
  1–12, body pp. 13–1563). Visually verified: A4 page size, both header elements (title + अधिकार
  banner) in matching watermark-gray, footer page numbers present, TOC content/page-numbers correct,
  content spot-checked against पास 3 fixes (confirmed present in the rendered PDF).
- **Known minor gap**: TOC entries are not clickable hyperlinks (543 §-entries vs 544 leader-lines
  found during link-mapping → finalize_big.py declined to guess the mapping rather than risk a wrong
  link). Bookmarks/outline navigation still works fine; only the TOC *text* isn't clickable. Not
  investigated further — low priority, book is otherwise complete and correct.

## Follow-up (not started, out of scope for this folder)
अधिकार 6–7 (पिण्डशुद्धि, षडावश्यक — the gap in पूर्वार्ध) remain undone anywhere in the project.
