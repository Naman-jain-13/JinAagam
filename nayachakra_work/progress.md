# नयचक्र (णयचक्को) व्याख्या — progress log

*Working notes only. Nothing from this file goes into the book.*

## Source

`E:\Projects\JinAagam\Nayachakko [Naya Chakra] [Shree Maailladhaval].pdf` — 315 scan pages, **no text layer**.
भारतीय ज्ञानपीठ, मूर्तिदेवी जैन ग्रन्थमाला, प्राकृत ग्रन्थांक 12, तृतीय संस्करण 2001.
सम्पादन-अनुवाद: सिद्धान्ताचार्य पं. कैलाशचन्द्र शास्त्री. मूल: श्री माइल्लधवल (द्रव्यस्वभावप्रकाशक नयचक्र);
प्रथम रचना दोहा-छन्द में आचार्य श्री देवसेन स्वामी द्वारा (गाथा 424–425 का कथन).

## Scan-page map (established by reading pages 1, 5, 30, 40, 42, 44, 50, 241, 243, 248, 249, 250, 285, 290, 300, 310)

| scan | printed | contents |
|---|---|---|
| 1 | — | title page |
| 2–41 | प्रस्ता० 1–47 | सम्पादकीय प्रस्तावना + its own विषय-सूची — **OUT OF SCOPE (reader's instruction)** |
| **42–248** | **1–207** | **मूल ग्रन्थ, गाथा 1–425 — THIS PROJECT** |
| 249–~284 | 208–~244 | परिशिष्ट 1: आलापपद्धतिः (श्रीदेवसेनविरचिता, हिन्दीटीका-सहिता) — phase 2, not now |
| ~285–~300 | ~245–260 | परिशिष्ट 2: नयविवरणम् — phase 2, not now |
| ~301–309 | — | परिशिष्ट 3 — phase 2 |
| 310–315 | — | परिशिष्ट 4: नयचक्रगत गाथानुक्रमणी (useful for cross-checking gatha first-words) |

Offset is **41** for most of the body (scan = printed + 41) but **40** from about printed 210 on — one
unnumbered leaf intervenes. Never compute it; agents read the printed number off the page.

Images: `img/p0042.png … p0249.png` at 300 dpi (p0249 kept only as the "read one page past" reference
for the last batch).

## Page layout (verbatim for agent prompts)

One PNG = one printed page, single column. Order on a page:

1. running header — one side: gatha-range marker `[ गा० ४०१–` or `–४२५ ]`; centre: `नयचक्र` or
   `द्रव्यस्वभावप्रकाशक`; other side: printed page number in Devanagari.
2. a **block of Prakrit गाथाएँ** at the top, each preceded by a short Sanskrit उत्थानिका/अवतरण sentence
   (e.g. `स्वभावस्य नामान्तरं ब्रूते 'तच्चं' इत्यादि—`), each ending `॥4॥`. Several gathas may stand together
   before any Hindi appears. Superscript digits in the गाथा point to the footnotes (पाठान्तर).
3. a horizontal rule.
4. the **Hindi part**: for each gatha (matched by its `॥n॥`) — अनुवाद paragraph, then `विशेषार्थ—` paragraph(s),
   sometimes `शंका—` / `समाधान—` pairs, sometimes `कहा भी है—` + a quoted verse.
5. **footnotes** at the page bottom in small type: `१. … २. …` — मुद्रित पाठान्तर from the manuscripts
   (अ०, क०, ख०, मु०, ज०, प्रतौ) and source citations (पञ्चास्ति०, सर्वार्थसि०, आ० प० प्र०, जयसेन टीका …).
   These are part 9 material, never prose.
6. `इति <name>अधिकारः ।` marks the end of an अधिकार — **report these**, they become the खण्ड headers.

Two things to ignore completely: the library stamp `मार्गदर्शक :– आचार्य श्री सुविधिसागर जी महाराज` overlaid
mid-page, and the faint bleed-through of the reverse side's text.

## § numbering scheme (collision-free, no renumbering pass)

**§ number = the number of the FIRST गाथा of the unit.** A unit is one gatha, or the group of gathas that
the book explains together (printed `॥5-6॥`). So §5 covers गाथा 5–6 and there is no §6. Gaps in the §
sequence are intentional and are explained in the front matter. Agents never invent § numbers and never
renumber — every agent can therefore work without knowing what the others produced.

## Format — 9 parts per §

1. मूल पाठ (प्राकृत गाथा) · 2. संस्कृत छाया · 3. अन्वय · 4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ) ·
5. हिन्दी अनुवाद · 6. जैनागम के अनुसार विस्तृत व्याख्या · 7. सरल उदाहरण · 8. तुलनात्मक तालिका / चार्ट ·
9. सन्दर्भ एवं पाद-टिप्पणी

Parts 2–4 are this project's addition (the reader asked for them, after अभिषेक-पाठ-संग्रह) because the मूल
is Prakrit. Parts 1–5 = pass 1 (philology, precision). Parts 6–9 = pass 2 (`addenda/sNNN.md`, depth).
Builder: `build_docx.js` in this folder — a copy of the skill's builder patched to a 9-slot renderer
(`kind()` keys on छाया / अन्वय / अन्वयार्थ before मूल / अनुवाद, so heading-word order matters).

## Rules (from the reader; do not relitigate)

- No sect names (बीसपंथ/तेरापंथ) anywhere.
- Jain आचार्य never bare: श्री … स्वामी. `postprocess_docx.py` (local copy — माइल्लधवल, ब्रह्मदेव etc. added
  to NAMES) runs on the built .docx before Word.
- Part 9 at dictionary size (7 pt).
- No working-process language in any parts/ or addenda/ file.
- प्रस्तावना is out of scope.
- The मूल पाठ is never altered; [अस्पष्ट] where unreadable; लगभग/सम्भवतः where unsure; never invent a citation
  or a Prakrit form.

## Batch table

| batch | scan pages | printed | § (गाथा) | model | state |
|---|---|---|---|---|---|
| 01 | 42–49 | 1–8 | | opus | |
| 02 | 50–57 | 9–16 | | opus | |
| 03 | 58–65 | 17–24 | | opus | |
| 04 | 66–73 | 25–32 | | opus | |
| 05–26 | 74–248 | 33–207 | | | queued |

Batch size 8 scan pages × 26 batches. Pass 1 only writes parts 1–5.

## Lessons (append as they happen)
