# granth-vyakhya — Claude Code skill (setup guide for humans)

This folder teaches Claude Code the exact workflow that produced *Pramana_Pariksha_Sampurna_Vyakhya.pdf*,
*Laghu/Bruhat_Sarvagya_Siddhi_Vyakhya.pdf*, *Abhishek_Path_Sangrah_Vyakhya.pdf* and *Gagar_Saar_English.pdf*:
scanned book → page images → Claude reads them → मूल पाठ, हिन्दी अनुवाद, व्याख्या, उदाहरण, तालिका, सन्दर्भ
per paragraph → Word + PDF with a real विषय-सूची (page numbers), footers, back matter.

## Install (one time)

1. Copy the whole `granth-vyakhya/` folder to **one** of:
   - `C:\Users\<you>\.claude\skills\granth-vyakhya\`   ← available in every project (recommended)
   - `<your project>\.claude\skills\granth-vyakhya\`   ← only that project
2. Install the tools the scripts need (PowerShell):
   ```powershell
   pip install pymupdf python-docx
   cd C:\Users\<you>\.claude\skills\granth-vyakhya\scripts ; npm install
   ```
   Microsoft Word must be installed — it is what fills in the TOC page numbers and exports the PDF
   (LibreOffice cannot do this step).
3. Start Claude Code in the folder that contains your PDF. Check the skill is seen: type `/granth-vyakhya`
   or just ask as below.

## Use

Put the scanned PDF in a folder and say, for example:

> `E:\Books\Nyaya_Dipika.pdf` — इस ग्रन्थ की पूरी व्याख्या बनाओ, Pramana Pariksha वाले format में
> (मूल पाठ, हिन्दी अनुवाद, व्याख्या, उदाहरण, तालिका, सन्दर्भ; TOC और page numbers के साथ)।

or, for a booklet you just want translated with the same layout:

> `E:\Books\Prashnottari.pdf` — translate this to English keeping the format as it is.

Claude will: render pages → read the first few to learn the layout → launch parallel agents per page
range → stitch and check the seams → write the extra parts and back matter → build the .docx → run Word to
finalize → verify → give you the .docx and .pdf. A 30-page booklet is one sitting; a 400-page book is
several — it keeps a `progress.md` in `<book>_work/` so a later session continues where it stopped.

## What you can ask for afterwards

- "page 2 पर एक disclaimer bullet जोड़ो" / "सन्दर्भ वाला font छोटा करो" / "margins कम करो, blank space हटाओ"
- "heading अकेली page के नीचे न रहे" (keep-with-next) — already built in, but re-check with
  `python scripts/check_quality.py pdf <book.pdf>`
- "इसी को English में बनाओ" — same parts/, new agents for translation, `build_simple_docx.py`

## Folder map

```
granth-vyakhya/
  SKILL.md                    what Claude follows (modes, passes, build, hard rules)
  references/
    format-standard.md        the exact document shape and style rules
    agent-prompts.md          copy-paste prompts for the parallel agents (transcribe/translate, addenda, back matter, Q&A)
    pitfalls.md               everything that went wrong across ~1,100 scan pages, and the fix
    sample-section.md         one real § at the expected depth
  scripts/
    render_pages.py           PDF → PNG pages
    build_docx.js             markdown parts → .docx (6-part § format, TOC, footer)      [node]
    build_simple_docx.py      markdown → .docx for translation-only / Q&A booklets          [python]
    postprocess_docx.py       श्री … स्वामी honorifics for आचार्य names + part-6 at 7 pt (run before Word) [python]
    finalize_word.ps1         Word COM: update TOC page numbers, export PDF                 [powershell]
    check_quality.py          gate: numbering, duplicates, forbidden words, orphaned headings
  assets/
    meta.example.json, groups.example.json, meta.simple.example.json
```

## Rules the original reader insisted on (Claude already knows; you should too)

- The book never names Jain sub-sects (बीसपंथ/तेरापंथ). Variants are described neutrally.
- Nothing about the working process (batches, sessions, file names) appears in the book.
- Every आचार्य is named with respect — श्री विद्यानन्द स्वामी, श्री अकलंकदेव — never a bare name.
- सन्दर्भ एवं पाद-टिप्पणी is printed dictionary-size (7 pt, single-spaced, ZERO gap between bullets) and its content is kept very short (1–3 tiny bullets) so references take minimal space.
