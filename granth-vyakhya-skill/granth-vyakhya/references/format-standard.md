# ग्रन्थ-व्याख्या — Format Standard

This is the exact shape of the deliverable. It was set by `Pramana_Pariksha_Sampurna_Vyakhya.pdf` and later
confirmed on लघु-सर्वज्ञ-सिद्धि, बृहत्-सर्वज्ञ-सिद्धि and अभिषेक-पाठ-संग्रह. A version of लघु-सर्वज्ञ-सिद्धि that
had only parts 1–3, no TOC and no page numbers was **rejected** by the reader ("wants things similar to
Pramana Pariksha") and cost a full extra sitting to rebuild — so the shape below is not optional polish, it is
what "done" means.

## 1. Document skeleton (in this order)

| # | Block | Notes |
|---|---|---|
| 1 | Title block | author line (e.g. `श्रीमदाचार्य-विद्यानन्द-विरचिता`) → **ग्रन्थ name** (large) → subtitle `सम्पूर्ण ग्रन्थ (§1 – §N): अनुच्छेदशः मूल पाठ, हिन्दी अनुवाद, …` |
| 2 | **आधार** paragraph | which scan, how many pages, printed page range, "मूल पाठ स्कैन-छवियों को पढ़कर लिपिबद्ध किया गया है; जहाँ अक्षर अस्पष्ट थे वहाँ [अस्पष्ट] अंकित है … मूल पुस्तक से मिलान अवश्य करें" |
| 3 | **प्रत्येक अनुच्छेद की संरचना** | the six parts, listed |
| 4 | **ग्रन्थ का विषय** | 3–6 lines: what the text argues, against whom; "अनुच्छेद-विभाजन (§) एवं शीर्षक व्याख्याकार के हैं, मूल ग्रन्थ के नहीं" |
| 5 | (optional) credits row / disclaimer | e.g. `संकलन एवं सम्पादन (हिन्दी व्याख्या): <names>` — discreet, one line |
| 6 | **विषय-सूची** | real Word TOC field, headings 1–2, **with page numbers** (filled by `finalize_word.ps1`) |
| 7 | (optional) भूमिका | 1–2 pages: scope, method, how to read, cautions |
| 8 | Body | खण्ड header `[ … ]` as Heading 1 → each `§ N — title` as Heading 2 → six Heading 3 parts |
| 9 | Back matter | ग्रन्थ-सार · परिशिष्ट · सन्दर्भ ग्रन्थ सूची · शब्दावली (each Heading 1) |
| 10 | Footer | centred page number on every page |

For a *collection* of independent texts (like अभिषेक-पाठ-संग्रह with 16 ग्रन्थ), each ग्रन्थ is a Heading 1 that
starts on a new page; अनुच्छेद are Heading 2 and flow continuously (no page break between them).

## 2. The six parts of every §

Every § carries all six headings, always in this order, even when a part has nothing to say — then write
the standard one-liner rather than dropping the heading. Readers navigate by these headings; a missing one
reads as an omission.

```
§ 12 — <व्याख्याकार का शीर्षक: what this passage does in the argument>

## 1. मूल पाठ            (संस्कृत / प्राकृत / हिन्दी as printed; verse numbers in Devanagari as printed;
                          [अस्पष्ट] where the scan cannot be read; (पृष्ठ 14) printed-page marker)
## 2. हिन्दी अनुवाद      (faithful, readable; bracketed glosses (…) for implied words)
## 3. जैनागम के अनुसार विस्तृत व्याख्या
                         (4–8 bullets, each 100–220 words: the argument step, the doctrine behind it,
                          the opponent's actual position, cross-links to other §, honest limits)
## 4. सरल उदाहरण         (2–3 everyday analogies a श्रावक can follow; else
                          "इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।")
## 5. तुलनात्मक तालिका / चार्ट
                         (one markdown table 3–7 rows: पक्ष-विपक्ष, steps, दृष्टान्त↔दार्ष्टान्त,
                          across-दर्शन comparison; else "इस अनुच्छेद हेतु तालिका आवश्यक नहीं।")
## 6. सन्दर्भ एवं पाद-टिप्पणी
                         (source of quoted verses with ग्रन्थ/प्रकरण/number — "लगभग"/"सम्भवतः" when unsure,
                          never invented; पाठ-टिप्पणी on unclear readings & sandhi; parallels in other
                          न्याय texts; else "मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।")
```

Depth target: **≈ 2.5–3 pages per §** in the final PDF. Parts 1–3 are written in the first pass
(transcription batch); parts 4–6 (and a deepening "पूरक व्याख्या") are written in the addenda pass.

## 3. Back matter contents

| File | Heading 1 | Contents |
|---|---|---|
| `01_saar.md` | उपसंहार | ग्रन्थ-सार (the whole argument as a journey, by खण्ड); central doctrine; shared fate of the opponent's objections; relation to sister texts |
| `02_parishisht.md` | परिशिष्ट | 1 ग्रन्थ की संरचना (खण्ड → § → scan pages table) · 2 दृष्टान्त-सूची · 3 पूर्वपक्ष-आपत्ति-सूची (by opponent → answered in §) · 4 प्रयुक्त युक्तियाँ (अन्यथानुपपत्ति, इतरेतराश्रय, सिद्ध-साधन… definition + § example) · 5 उद्धृत श्लोक/गाथा + probable source · 6 पाठ-सम्बन्धी सूचनाएँ (scan↔printed pages, अस्पष्ट spots, पुष्पिका, author's date) · 7 अध्ययन-क्रम सुझाव |
| `03_sandarbh.md` | सन्दर्भ ग्रन्थ सूची | by परम्परा: (क) मूल ग्रन्थ/ग्रन्थकार (ख) जैन आगम-सिद्धान्त (ग) जैन न्याय (घ) मीमांसा (ङ) बौद्ध (च) न्याय-वैशेषिक/सांख्य/वेदान्त (छ) अन्य — each: ग्रन्थ, कर्ता, लगभग काल, where used in this व्याख्या |
| `04_shabdavali.md` | शब्दावली | 30–60 पारिभाषिक terms grouped by theme; one-line definition + § of first/main use |

## 4. Style rules (apply to every word the reader sees)

- **Language:** शास्त्रीय, clear हिन्दी. Sanskrit technical terms kept, glossed in (…) on first use in a §.
- **Numerals:** English digits everywhere (§ 58, तत्त्वार्थसूत्र 1.4, पृष्ठ 51) **except inside quoted
  मूल verses** where `॥१२॥` stays as printed. (`meta.json → "numerals": "en"`; the builder converts
  automatically outside मूल text.) Older projects used Devanagari throughout — either is acceptable if
  consistent; `"dev"` keeps them.
- **Accuracy over completeness:** write only what the मूल text, the translation, or established जैन-दर्शन
  supports. Unsure verse number → "लगभग"/"सम्भवतः". Never fabricate a citation.
- **Sect names:** never write बीसपंथ / तेरापंथ (or any sub-sect label) anywhere — not in tables, not in
  comparisons. Describe ritual variants neutrally ("कुछ परम्पराओं में…"). The reader explicitly forbade this.
- **Honorifics for the guru-paramparā:** a Jain आचार्य is never a bare name. Write "श्री विद्यानन्द स्वामी",
  "श्री अकलंक स्वामी", "श्री अकलंकदेव", "आचार्य श्री समन्तभद्र", "श्री पूज्यपाद स्वामी". Rule of thumb: bare
  name → `श्री <name> स्वामी`; name already ending in देव/सूरि/स्वामी, or preceded by आचार्य/भट्टारक/मुनि/पं.,
  or used as a compound ("जिनसेन-कृत") → `श्री <name>`. Non-Jain opponents (कुमारिल, धर्मकीर्ति, उदयन…)
  stay as they are. Never touch the मूल पाठ or the TOC. `scripts/postprocess_docx.py` applies this to the
  whole book after the build — but write it correctly at source too.
- **Part 6 at dictionary size:** सन्दर्भ एवं पाद-टिप्पणी body 7 pt, single spacing, heading 9 pt, and **zero
  space between bullets** (one entry runs straight into the next); the content itself is kept very short —
  1–3 tiny bullets (the reader wants references present but taking minimal space). Applied by `postprocess_docx.py` (REF_AFTER = 0).
- **No working-process language** in the document: no "बैच", "सत्र", "अगले बैच में", "progress.md",
  file names, "उपयोगकर्ता", "हमने पिछली बातचीत में", "Q3/Q4", English project nicknames. Cross-refer with
  "§ 14", "पूर्व-वर्णित", "आगामी अंश". This is a book for मुनि/श्रावक, not a work log.
- **Headings never orphaned:** every heading style has keep-with-next so a heading is never the last line
  of a page (readers reported this; the builders already set it — do not remove).
- **Font:** Nirmala UI (Devanagari-complete, ships with Windows). Body 12 pt; tables 10.5 pt.
- **Tables:** header row shaded; 2-column tables 1:2 width. Flow-chart boxes: a fenced ``` block or a
  1-cell shaded table.

## 5. meta.json fields (for `scripts/build_docx.js`)

```json
{
  "title": "लघु-सर्वज्ञ-सिद्धिः",
  "author_line": "श्रीमदाचार्य-अनन्तकीर्ति-विरचिता",
  "subtitle": "सम्पूर्ण ग्रन्थ (§1 – §{N}): अनुच्छेदशः मूल संस्कृत पाठ, हिन्दी अनुवाद, जैनागम-सम्मत विस्तृत व्याख्या, सरल उदाहरण, तुलनात्मक तालिका/चार्ट एवं सन्दर्भ",
  "basis": "उपलब्ध 21-पृष्ठीय स्कैन — \"…\" (मुद्रित पृष्ठ 107–127)। मूल पाठ स्कैन-छवियों को पढ़कर लिपिबद्ध …",
  "subject": "यह कृति केवल तर्क के बल पर सर्वज्ञ की सिद्धि करती है और …",
  "credits": { "label": "संकलन एवं सम्पादन (हिन्दी व्याख्या)", "value": "…" },
  "disclaimer": "यह व्याख्या कृत्रिम बुद्धि की सहायता से, मानव-पर्यवेक्षण सहित तैयार की गई है; प्रामाणिक उद्धरण हेतु मूल ग्रन्थ से मिलान करें।",
  "numerals": "en",
  "font": "Nirmala UI",
  "out": "../Laghu_Sarvagya_Siddhi_Vyakhya.docx"
}
```
`{N}` in subtitle is replaced by the § count. `groups.json` maps the first § of each खण्ड to its bracketed
heading: `{ "1": "[ मङ्गलाचरण एवं मूल अनुमान ]", "5": "[ पूर्वपक्ष: … ]" }`.
