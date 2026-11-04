# मूलाचार अधिकार 5 (पंचाचार, गाथा 198–419) — progress / HOW TO RESUME

Scan: `mool/Mulachar_Purvardh_Aryika_Jnanmati.pdf`, अधिकार 5 = scan p0219–p0387 (printed = scan − 58). Same independent pipeline as
अधिकार 1–4 (see memory note mulachar-project): pass 1 Sanskrit+Prakrit only → `make_src.py` → pass 2 from `src/` only → pass 3 audit
(scans allowed, above the rule only; `crop_above_rule.py`) → fixers → `apply_titles.py` → build.

## Status (2026-10-24)
- **Pass 1 DONE**: 16 batches in `parts/`, 221 § (§1980–§4190), गाथा 198–419 continuous (§2540 = गाथा 254+255 merged on purpose).
  Seam fixes applied (§2570 पातनिका inserted; duplicate §3820 removed from batch13). Known pass-1 normalisations to UNDO in pass 3:
  `verify_flags.md`.
- `src/` built (221 files) by `python make_src.py`.
- **Pass 2 IN PROGRESS**: batch list `pass2_batches.txt` (16 lines × ~14 §). **Run `python resume_status.py`** — it prints which
  lines are DONE and which § are missing. A line agent that was cut off leaves its finished § files; relaunch only the missing keys.
- Pass-2 agent prompt (Opus): "Work dir …\adhikar-5\. Read pass2_instructions.md fully and follow it exactly. Source folder is src\
  (never open parts\, img\, mool\, verify\ or scans). Form model addenda\s2120.md. Your § keys: <list> — write ONLY those keys.
  Write addenda\s<key>.md one § at a time, first line `शीर्षक: …`."

## Next after pass 2
1. pass 3 audit (copy shape from `../adhikar-4/verify/`, spec `pass3_instructions.md`, include `verify_flags.md` items);
2. fixers → `python apply_titles.py`; 3. `groups.json` banners (one per आचार: दर्शन, ज्ञान, चारित्र, तप, वीर्य — and enough
   that every finalize chunk starts with a Heading 1); 4. `node build_docx.js .` → `postprocess_docx.py` → `finalize_big.py`
   (MAX_CHILDREN 190); 5. gates: grep PDF for "Error!" (must be 0) and count `संस्कृत आचारवृत्ति —` (must = 221).
- 2026-10-25: **Pass 2 DONE (221/221).** Pass 3 audit: 8 audits × 2 batch-lines → `verify/v<first>-<last>.md` (lines 1-2 →
  v1980-2250, 3-4 → v2260-2530 launched; 5-6, 7-8, 9-10, 11-12, 13-14, 15-16 to launch). Spec repointed to `src\s<key>.md`;
  auditors also check every item in `verify_flags.md`. Next: fixers (one per audit file, log `verify/x_applied_*.md`) → `apply_titles.py`
  → `../purvardh/join.py`.
- 2026-10-25: audits 1-7 DONE, 8 (v3950-4190) running. Fixers applied for 1980–3660 (logs verify/x_applied_*.md; src==parts verified by regenerating src); fixer 3670-3940 running. Coordinator closed §2090 (print 'वय'), §3240 (* has no footnote), §3720 (no footnote). Next: fixer 3950-4190 → `python apply_titles.py` → join.
- 2026-10-25: **अधिकार 5 TEXT COMPLETE.** Pass 3: 8 audits + 8 fixers done (verify/x_applied_*.md). apply_titles 221/221; src==parts; no sect/translator names. groups.json: 5 आचार banners. Ready for `../purvardh/join.py`.
