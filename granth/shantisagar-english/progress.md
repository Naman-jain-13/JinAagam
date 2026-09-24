# Shantisagar Ji — English Edition (progress)
Source: "E:\Projects\JinAagam\Shantusagar jee.pdf" (40 pp, scanned, Hindi). Pages rendered to img/pNN.png (110 dpi) and read visually.
Output: E:\Projects\JinAagam\Shantisagar_Ji_English.docx / .pdf — 55 pages (2026-09-21). Done in the Gagar_Saar_English style (page-by-page faithful translation, structure identical).
Parts: part01 (pp1–4 life-sketch + chaturmas table), part02 (pp5–9 muni/aryika/ailaka/kshullaka tables + sources), part03 (pp10–14 kshullika table + Q1–55), part04 (pp15–18 Q56–106), part05 (pp19–22 Q107–163), part06 (pp23–24 Q164–192), part07 (pp25–28 Shantisagar pooja + 3 arghyas), part08 (pp29–32 Ajitsagar/Shrutsagar arghya + Vardhamansagar pooja), part09 (pp33–35 aarti + chalisa), part10 (pp36–40 barah bhavana).
Verses: Roman transliteration (italic) + English meaning; mantras transliterated.
Build: `python build_docx.py` (handles **bold**, *italic*, pipe tables with width heuristics) → `finalize_word.ps1` with $env:OUT (Word COM; once failed with RPC error when another Word instance was busy — retry worked).
2026-09-21: Book/print format added — `build_book.py` → Shantisagar_Ji_English_Print.docx/.pdf (5.5in×10.5in like "Gagar Me Sagar 23-9-2025.pdf": single column for prose/tables/pooja, quiz in 2 columns with rule, footer "( N )", Cambria 10pt). 55 pages.
