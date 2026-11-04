# प्रमाणनिर्णय (श्री वादिराजसूरि) — progress

Source: `mool/Pramana_Nirnaya.pdf` (129 scan pp). Text = scan p21–129, printed = scan − 20. Scan p1–20 = editor's Hindi
introduction (skipped). Each Sanskrit paragraph is followed by the editor's Hindi — never transcribed (independent route,
same as the मूलाचार/पत्रपरीक्षा series: 7-क/9-क with दृष्टान्त).

## GAP — printed page 10 missing from the scan
Scan p30 (where text page 10 belongs) is a duplicate of introduction page 10 ("स्थितिकाल"; same as scan p9).
Checked all of scan p1–32: the real text page 10 is not anywhere in the file. Paragraphs **॥19॥ and ॥20॥** are therefore
absent (§190 = ॥18॥ → §200 = ॥21॥). The book must say so in a note at that place and in the भूमिका; never reconstruct them.
Ask the user for another copy/scan of printed page 10.

## Pass 1 (Sonnet, 10 batches of 11 scan pp)
- batch01 p21–31 ✓ (॥1–18, 21–22॥), batch02 p32–42 ✓ (॥23–37॥), batch04 p54–64 ✓ (॥52–65॥), batch05 p65–75 ✓ (॥66–80॥;
  p65 independently re-read → identical), batch03, 06–09 running, batch10 p120–129 pending.

## Scan defects found in pass 1
- Scan p111 (printed 91, ¶126–127): left edge of several lines cut off; scan p113–114 (¶132–133): right edge cut. Letters marked `[अस्पष्ट]`, never guessed.
- Grey watermark `मार्गदर्शक :- आचार्य श्री सुविधिसागर जी महाराज` hides parts of lines on many pages → most `[अस्पष्ट]`.

## Quarantine (written while image reads were failing → re-read by fresh agents that cannot see the drafts)
- batch03 §20010–20050 (scan p43–46) → `quarantine/batch03_s20010-20050_UNREAD.md`; fresh re-read → `parts/batch03a_p043-046.md` (keys §20011…).
- batch06 §50010–50090 (scan p76–83, ¶81–89) → `quarantine/batch06_s50010-50090_UNREAD.md`; fresh re-read → `parts/batch06a_p076-083.md` (keys §50011…).
- batch05 §40010–40020 (p65) was independently re-read: identical → kept.
- batch07 (¶99–109): request-limit notices during reads (agent says images then displayed) → pass-3 auditor must read these paragraphs against the scan line by line.
- batch03a ¶42: printed `सवत्र`, transcriber wrote `सर्वत्र` — restore printed form, note in part 11.
- pass2: §20012 title (from pass-1 re-read) mentions सन्निकर्ष but the § text does not → pass 3 must re-title. Pass-2 batch 3 cited परीक्षामुख 1.13, प्रमाणवार्त्तिक "अभिप्रायनिवेदनात्", मीमांसासूत्र 1.1.4 from memory → pass 3 verify.

## HOW TO RESUME (2026-10-24)
- Pass 1 DONE (166 § incl. re-reads batch03a/06a; ¶19–20 absent from scan).
- **Pass 2 IN PROGRESS**: `pass2_batches.txt` (12 lines). **Run `python resume_status.py`** to see missing § per line; relaunch only
  missing keys with prompt: "Work dir …\pramana-nirnaya\. Read pass2_instructions.md fully and follow it exactly. Form model
  addenda\s150.md. Your § keys: <list> — write ONLY those. Read them in parts\ (+ neighbours). Never open mool\, img\, quarantine\ or
  scans. One file per § addenda\s<key>.md."
- Next: pass 3 audit (`pass3_instructions.md` adapted from प्रमाणसंग्रह — auditors MAY open scans for the Sanskrit only; give them the
  items in this file: batch07 request-limit paragraphs, §20012 title, from-memory citations, printed-form normalisations) → fixers →
  groups.json (4 निर्णय banners + extra so every finalize chunk opens with Heading 1) → meta.json (title प्रमाणनिर्णय, author श्री
  वादिराजसूरि, basis note incl. missing printed p10, no editor/translator name) → build → postprocess → finalize_big.py → gates:
  0 "Error!", Sanskrit-label count = § count.
- 2026-10-25: **pass 2 DONE** (166/166). **Pass 3 audit started**: 6 auditors, 2 batch-lines each → `verify/v_lines01-02.md` … `v_lines11-12.md`
  (01-02, 03-04, 05-06 launched; 07-08, 09-10, 11-12 to launch). Spec `pass3_instructions.md` adapted (scan only for the bold Sanskrit,
  never the editor's Hindi). Next: fixers apply every त्रुटि/लोप + restore printed forms → groups.json/meta.json → build.
- **Systemic pass-1 error (audit lines 05-06):** the fount's `न्न` was transcribed as `त्र` (`तन्न`→`तत्र`), scan-confirmed at §30040, §30160, §40060, §40100, §40140, §40150. Fixers: restore `तन्न` there, delete part-10 notes that blame the print; and EVERY other `तत्र` in parts/ must be checked against the scan (auditors 07-08, 09-10, 11-12 told to do so for their ranges; lines 01-04 need a sweep).
- **Audit 03-04 systemic finding:** pass 1 skipped the editor's Sanskrit footnotes as "glosses", but many name the speaker (सांख्याः, प्रभाकर आह) or settle the meaning; 7+ § falsely say in part 10 "कोई पाद-टिप्पणी नहीं". Fixers: remove every such false claim; where a footnote decides the speaker/meaning, correct parts 6/7 and mention it briefly ("सम्पादक की टिप्पणी के अनुसार …") — do NOT reproduce the modern editor's notes verbatim. Two meaning reversals: §30020 (`…अनिष्पादनात्`, अ dropped in pass 1), §10150 (यतः opens the reply).
- निर्णय label fixed: ¶99–109 (batch07) were 'निर्णय 2' → 'निर्णय 3' (audit 07-08).
- Fixers launched (FIX_SPEC.md) for v_lines01-02 … 09-10 (sweep folded into 01-04). After all fixers: rerun make_src.py so src matches parts.
- Fixers done: 01-02, 05-06, 09-10. OPEN for a final scan-check pass: §30160 T1 (`चेन्न`, `तद्रूपतया`, scan 64), §40110 T1 (`तेनाऽपि … परिच्छेदान्न`, scan 71); [अस्पष्ट] STANDS: §70030 T1, §70160 T8, §80070 T2, §80020 T5, §80030 T1–T6; footnote markers without text (§30040 ³⁴, §70080 ³⁴⁵, §70090 ⁶⁷, §80040 ³) — only add if they quote a source/variant.
- Fixer 03-04 done (51 changes). Open: [अस्पष्ट] §20080 T2, §20110 T8, §10090 T6, §10150 T3; §10090 T5 part-7 'पर से प्रतिपत्ति' bullet may need aligning with 'क्रिया-विधि'.
- Fixer 07-08 done (55 changes). Open for scan-check: [अस्पष्ट] §50011 T4, §50013 T8, §50130, §50160 T4, §60020 T4, §60040 (…मशको); verify §50013 कथमेवं and §60080 gap (filled from ¶107 footnote, not scan). All fixers 01–10 DONE; waiting audit 11-12.
- 2026-10-25: all fixers + scan-check DONE. (src/ is unused in this book — pass 2 read parts/ directly; no make_src.) groups.json, meta.json, bhumika, shabdavali written. Build next.
