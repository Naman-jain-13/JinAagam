# Agent prompt templates

Copy, fill the `<…>` fields, and launch as background subagents (`Agent` tool, `model: sonnet`, several in
one message so they run in parallel). Each template is self-contained because a fresh agent knows nothing
about this conversation. Keep the shared blocks (glossary, numbering scheme, style rules) **identical**
across the agents of one wave — inconsistency between agents is the #1 source of consolidation work.

Contents: A. Transcription + translation + व्याख्या batch · B. Addenda (parts 4–6) · C. Back matter ·
D. Translation-only / Q&A booklet · E. Boundary-check snippet

---

## A. Batch: मूल पाठ → हिन्दी अनुवाद → व्याख्या (parts 1–3)

```
You are producing part of a scholarly Hindi व्याख्या of a scanned Jain text, "<ग्रन्थ name>" by <author>,
for readers who are मुनि/विद्वान् श्रावक. Other agents are doing other page ranges in parallel; you own
scan pages <S>–<E> only.

SOURCE: one PNG per scan page at
  <img_dir>\p<SSS>.png … <img_dir>\p<EEE>.png   (read them in order with the Read tool)
Also read the page BEFORE your range (<img_dir>\p<S-1>.png) only to see where the previous agent's
text ends — do not translate it. Your first § begins with the first complete sentence/verse that starts
on page <S>. A verse or sentence that is cut at the top of page <S> belongs to the previous agent.
Symmetrically, YOUR last sentence: if it is cut at the bottom of page <E>, read page <E+1> and finish
that sentence (only up to its end — usually a few words), then stop. The next agent will skip it. This
way no sentence tail is left to nobody.
<Layout note, e.g.: each PNG shows two printed pages side by side, each in two columns; read column 1
top→bottom, then column 2, then columns 3 and 4. Printed page numbers "(14)" appear at the bottom —
use them to keep order, and record them as "(पृष्ठ 14)" markers, but never as prose.>

UNIT OF WORK: split the text into अनुच्छेद (§) of one coherent argument step / one verse + its commentary
(roughly 6–20 lines of मूल). Number them **§<START> onward** in sequence. (<If the count is unknown:
"Number your first § as §? and keep '?' for all; I will renumber at consolidation.">)

FOR EVERY § WRITE EXACTLY THIS (headings verbatim — the builder keys on these words):

§<n> — <a descriptive व्याख्याकार title: what this passage does in the argument>

## 1. मूल पाठ
(पृष्ठ <printed page>)
<transcribe exactly as printed — sandhi, verse numbers ॥१२॥, punctuation. Where a letter is truly
unreadable write [अस्पष्ट]; where you infer a printing slip write the printed form and note it in part 6.
Commentary (टीका) after a verse is transcribed too, marked "टीका —".>

## 2. हिन्दी अनुवाद
<faithful, natural Hindi; implied words in (…); keep technical terms, gloss on first use in this §>

## 3. जैनागम के अनुसार विस्तृत व्याख्या
- **<sub-heading>:** … (4–8 bullets, 100–220 words each: the step of the argument, the जैन doctrine
  behind it with the sūtra/ग्रन्थ it rests on, the opponent's real position stated fairly, cross-links
  "देखें § 7", and an honest note where the argument's reach is limited)

(Parts 4–6 will be added later by another pass — do NOT write them.)

STYLE (non-negotiable):
- शास्त्रीय, clear हिन्दी. English digits everywhere except inside quoted मूल verses.
- Never write sect names (बीसपंथ/तेरापंथ etc.). Describe variants neutrally.
- Jain आचार्य are always named with respect, never bare: "श्री विद्यानन्द स्वामी", "श्री अकलंकदेव",
  "आचार्य श्री समन्तभद्र", "श्री पूज्यपाद स्वामी" (in parts 2–6; the मूल पाठ stays as printed). Opponent
  philosophers (कुमारिल, धर्मकीर्ति, उदयन …) are written plainly.
- No working-process language anywhere in the file: no "बैच", "अगले बैच", "इस सत्र", file names,
  "उपयोगकर्ता". If a § continues on the next agent's pages, end your last § normally and simply say
  in your REPORT (not in the file) where you stopped.
- Do not summarise or skip: every line of मूल in your range must appear in some § part 1.
- Cite only what you can stand behind; "लगभग"/"सम्भवतः" for uncertain numbers; never invent.

OUTPUT: write one file  <work_dir>\parts\batch<NN>_p<SSS>-<EEE>.md
WRITE INCREMENTALLY: create the file with the Write tool after the first 2–3 §, then append each further
2–3 § with the Edit tool (old_string = the file's last line, new_string = that line + the new §). Never emit
more than ~3 § in one response — a single response is capped at 64k output tokens, and 8 dense pages of
§ blow through it (one agent lost all its work this way).
REPORT BACK (under 200 words): § range written; the exact first 6 words of मूल you started with and the
exact last 6 words you ended with (with printed page numbers) so I can check the seams; any [अस्पष्ट]
spots; any place you suspect a misprint.
```

Sizing: 8–14 scan pages per agent for dense commentary; up to 20 for plain verse or Q&A.
Launch 3–5 agents per wave; consolidate (see E) before the next wave so numbering stays clean.

---

## B. Addenda: parts 4–6 for every § (`addenda/sNN.md`)

```
You are completing a scholarly Hindi व्याख्या of "<ग्रन्थ name>". Each § in <work_dir>\parts\*.md already has
parts 1–3 (मूल पाठ, हिन्दी अनुवाद, विस्तृत व्याख्या). The final book needs SIX parts per §. For each § in
<first>–<last>, write one file  <work_dir>\addenda\s<NN>.md  (NN = two-digit § number, e.g. s07.md).

First read <work_dir>\addenda\<a finished sample>.md (or references/sample-section.md) to match depth and tone.
Then read the § itself (and its neighbours, for cross-links) in parts/.

FILE FORMAT — headings verbatim, in this order, first line exactly "## 3. पूरक व्याख्या":

## 3. पूरक व्याख्या
- **<उप-शीर्षक>:** … (3–5 bullets, 120–220 words each — DEEPEN, do not repeat parts 1–3: the न्याय
  technicality, the आगम/सिद्धान्त backing with its sūtra, the opponent school's exact doctrine, links to
  other §, an honest सन्तुलन-टिप्पणी on the argument's limits)

## 4. सरल उदाहरण
- **<उदाहरण-शीर्षक>:** … (2–3 bullets, 80–160 words, from daily life so a सामान्य श्रावक follows the logic)

## 5. तुलनात्मक तालिका / चार्ट
<one intro line>
| … | … | … |
|---|---|---|
| 3–7 rows |
<one concluding line>   (If the part-file already has a table for this §, take a DIFFERENT angle:
argument steps / पक्ष-विपक्ष / दृष्टान्त↔दार्ष्टान्त / other दर्शन.)

## 6. सन्दर्भ एवं पाद-टिप्पणी
- **उद्धरण-स्रोत:** ग्रन्थ, प्रकरण, verse no. of anything quoted ("लगभग"/"सम्भवतः" if unsure; never invent)
- **पाठ-टिप्पणी:** unclear readings, sandhi splits, meaning of पारिभाषिक words
- **समानान्तर:** the same युक्ति in other जैन न्याय texts (अष्टसहस्री, न्यायकुमुदचन्द्र, प्रमेयकमलमार्तण्ड,
  सन्मतितर्क-टीका …) — one-line pointer each, only where it really occurs
(4–7 bullets)

RULES: file ≈ 8–12 KB (≈1000–1500 words). शास्त्रीय हिन्दी; English digits outside quoted verses; no sect
names; आचार्य names always with honorific (श्री … स्वामी / श्री अकलंकदेव / आचार्य श्री …); no working-process language (बैच/सत्र/अगले संस्करण/file names/उपयोगकर्ता/"Laghu"/"Bruhat" in
English → write the ग्रन्थ name in Hindi or "इस ग्रन्थ"). Do NOT edit parts/.
REPORT: list of files written with sizes; one line per any inconsistency you noticed in parts (don't fix it).
```

Sizing: 10–15 § per agent.

---

## C. Back matter (`backmatter/01_saar.md … 04_shabdavali.md`)

```
Write the back matter for the Hindi व्याख्या of "<ग्रन्थ name>" (<N> §, <P> scan pages). Read ALL of
<work_dir>\parts\*.md and <work_dir>\groups.json (खण्ड titles) first; read <sample backmatter dir> for the
level and structure to match — but every fact must come from THIS text.

Builder syntax: "# " Heading 1, "## " Heading 2, "### " Heading 3, "- " bullets, "|" tables, paragraphs.

- backmatter/01_saar.md   → "# उपसंहार" → "## ग्रन्थ-सार: सम्पूर्ण <name> एक दृष्टि में": the argument as a
  journey, खण्ड by खण्ड; the central doctrine; what happens to each opponent objection; relation to sister
  texts (one neutral sub-section). ≈ 12–16 KB.
- backmatter/02_parishisht.md → "# परिशिष्ट": 1 ग्रन्थ की संरचना (खण्ड → § → scan pages, table);
  2 दृष्टान्त-सूची (every analogy in the text, with §); 3 पूर्वपक्ष-आपत्ति-सूची by opponent (objection →
  answered in §); 4 प्रयुक्त युक्तियाँ (definition + § example); 5 उद्धृत श्लोक/गाथा + probable source
  ("सम्भवतः" when unsure); 6 पाठ-सम्बन्धी सूचनाएँ (scan↔printed pages, [अस्पष्ट] spots, पुष्पिका,
  author's probable date); 7 अध्ययन-क्रम का सुझाव. ≈ 25–35 KB.
- backmatter/03_sandarbh.md → "# सन्दर्भ ग्रन्थ सूची" by परम्परा (क) मूल ग्रन्थ/कार (ख) जैन आगम-सिद्धान्त
  (ग) जैन न्याय (घ) मीमांसा (ङ) बौद्ध (च) न्याय-वैशेषिक/सांख्य/वेदान्त (छ) अन्य. Each: ग्रन्थ, कर्ता,
  लगभग काल, where used in this व्याख्या. Only works actually cited in parts/. ≈ 15–20 KB.
- backmatter/04_shabdavali.md → "# शब्दावली": पारिभाषिक terms grouped by theme; one-line definition +
  § of first/main use. ≈ 18–25 KB.

RULES as in the other templates (हिन्दी, English digits, no sect names, आचार्य names with श्री … स्वामी, no process language, don't edit parts/).
REPORT: files + sizes; any inconsistency seen.
```

Optional `frontmatter/01_bhumika.md` → "# भूमिका": scope, method (AI-assisted reading of scan images with
human verification), how to read a §, cautions, आभार. 1–2 pages.

---

## D. Translation-only / question-answer booklet (no व्याख्या)

```
Translate "<booklet>" (Hindi → <target language>) preserving its exact structure. You own scan pages
<S>–<E>. <layout note>. Topics are boxed headings "N. <name>"; inside, numbered प्रश्न/उत्तर pairs.

Use these EXACT topic headings (shared with the other agents, for the TOC): <numbered glossary list>.
Preserve question numbers exactly as printed (keep duplicates/gaps; do not renumber). Continue a topic
that started in the previous range without repeating its heading.

Format:
# 13. Jiva Samasa (Classification of Souls)

**Question 8.** …
Answer: …

Mantras/verses: transliterate, then give the meaning in (…). Technical terms: transliteration + gloss on
first use per topic. No page-break markers, no tables unless printed.
OUTPUT <work_dir>\parts\part<NN>_p<SSS>-<EEE>.md.  REPORT: topics + question counts, printed-page
range covered, exact first/last question, any illegible spot.
```

---

## E. Seam check after a wave (run yourself, before the next wave)

```
grep -n "^§" <work_dir>/parts/*.md                     # numbering: sequence, duplicates, "§?"
grep -c "^§" <work_dir>/parts/*.md
python scripts/check_quality.py parts <work_dir>       # gaps, dups, forbidden words
```
Then compare each agent's reported "last 6 words" with the next agent's "first 6 words": identical text on
both sides → delete the later copy (`sed -i 'START,ENDd'`); a gap → read the page top yourself and patch the
missing words into the previous file's last § (part 1 and part 2). The classic gap is the tail of a sentence
cut at a page bottom — the seam rule above exists because it happened on 4 of 4 seams once. Fix `§?`/collided numbers with targeted edits — each needs the cross-file context only you have.
