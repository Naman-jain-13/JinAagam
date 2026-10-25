# मूलाचार अधिकार 6 (पिण्डशुद्धि, गाथा 420–501) — progress / HOW TO RESUME
Scan p0388–p0441 (printed = scan − 58); boundaries in `../mulachar-5/verify/boundaries_6_7.md`. Specs adapted from mulachar-5.
Pipeline: pass 1 (Sonnet, `pass1_instructions.md`) → `python make_src.py` → pass 2 (Opus, from src/ only; make `pass2_batches.txt`
like mulachar-5; `python resume_status.py`) → pass 3 audit → fixers → `python apply_titles.py` → then `../mulachar-purvardh/join.py`.
## Status 2026-10-25
- Pass 1 DONE (81 §, गाथा 420–501; §4220 = 422+423 merged). src/ built. Pass 2: pass2_batches.txt (6 lines) — run resume_status.py.
  with the same range (prompt shape: see mulachar-5 progress). After all 5: continuity check (गाथा 420–501, no gaps/dups), seam
  पातनिका check, then make_src.
- 2026-10-25: **Pass 2 DONE (81/81).** Pass 3: audits lines 1-2 → verify/v4200-4480.md, 3-4 → v4490-4760.md launched; 5-6 → v4770-5010.md to launch. Then fixers (copy `../mulachar-5/FIX_SPEC.md`, change chapter) → apply_titles.py → join.
- Pass 3 audits v4200-4480, v4490-4760 done; fixers launched (FIX_SPEC.md). v4770-5010 audit pending fixer. §4740 footnote text missing (marker only).
- 2026-10-25: pass 3 COMPLETE (3 audits + 3 fixers), apply_titles 81/81, src==parts verified, groups.json (7 banners). अधिकार 6 READY for join.
