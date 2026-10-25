# मूलाचार पूर्वार्ध (अधिकार 1–7) — ONE joined book (like mulachar-uttarardh)

User (2026-10-25): don't publish अधिकार 1, 2, 3 … separately — join them into one ग्रन्थ, as was done for the उत्तरार्ध.
This folder holds only the JOIN + build. The per-chapter work stays in `../mulachar` (अ.1), `../mulachar-2` … `../mulachar-7`.
`python join.py` copies parts/addenda/groups from every chapter folder that exists (re-runnable).
Infra copied from `../mulachar-uttarardh` (grey footer, finalize_big MAX_CHILDREN 20 — Word crashed on dense regions at higher values).

## Status
- अ.1–4 DONE (built separately earlier). अ.5: pass 1 done, pass 2 running (see ../mulachar-5/progress.md). अ.6 पिण्डशुद्धि and
  अ.7 षडावश्यक: NOT started — boundaries being mapped (`../mulachar-5/verify/boundaries_6_7.md`); then folders mulachar-6/-7 with the
  same 3-pass pipeline (copy pass1/2/3 specs from mulachar-5, change range).

## Build (when all 7 chapters have pass 3 + apply_titles done)
1. `python join.py`  2. meta.json (title "मूलाचार — पूर्वार्ध : अधिकार 1–7"; copy fields from ../mulachar-uttarardh/meta.json)
3. frontmatter: ONE combined भूमिका (merge chapters' 01_bhumika.md; छाया-note once); backmatter: combined उपसंहार + शब्दावली
4. `node build_docx.js .` → `python postprocess_docx.py vyakhya/<docx>` → `python finalize_big.py vyakhya/<docx>`
5. gates: 0 "Error!" pages; count of `संस्कृत आचारवृत्ति —` = § count; A4; no माताजी/translator name.
- Numbering overlap (for भूमिका of BOTH books): पूर्वार्ध print ends अधिकार 7 at गाथा 692; उत्तरार्ध print begins अधिकार 8 at 683 and jumps ॥६८९॥→॥७००॥. The two volumes number independently; keep each as printed and say so in one line in each भूमिका. Do not renumber.
