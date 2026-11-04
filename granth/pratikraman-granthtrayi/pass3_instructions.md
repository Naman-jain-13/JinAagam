# Pass 3 — independent audit spec (प्रतिक्रमण-ग्रन्थत्रयी, v2)

*Working document. Nothing here goes into the book.*

Another agent rendered **श्री प्रभाचन्द्राचार्य's संस्कृत टीका** into Hindi, segment by segment, and wrote the व्याख्या parts. You never saw that
work. **Report every place the Hindi says something the Sanskrit does not, or fails to say something it does** — and check the two practical parts
(7-क, 9-क) for honesty. **You report; you do not edit `parts/` or `addenda/`.**

For each § key in your range read: the source `src\s<key>.md` (the **प्राकृत सूत्र** from the परिशिष्ट, **the Sanskrit टीका in `(Tn)` segments**, and the
printed variant footnotes) and `addenda/s<key>.md` (`शीर्षक:` and `सन्दर्भ-संकेत:` lines; part 5 = the Hindi of the सूत्र; part 6 = the Hindi of the टीका
against the same tags; plus parts 2, 3, 4, 7, 7-क, 8, 9, 9-क, 10). **Those are your only sources.** This book is deliberately an *independent* Hindi
rendering: **do not open `parts/`, `mool/`, `img/`, `_v1/` or any file that might carry another Hindi translation of this text, and do not bring one
from memory** — if a Sanskrit reading looks worn or doubtful, report it as सन्देह with the reading you think likely; do not go looking for a published
translation to settle it.

**Read the Sanskrit first and construe it yourself, before reading the Hindi.** If you read the Hindi first you will agree with it.

## A. Part 6 — Sanskrit ↔ Hindi (the main job)

Finding types: **त्रुटि** (the Hindi states what the Sanskrit does not / contradicts it: wrong compound split, a question attached to the wrong noun,
wrong case/verb, dropped negation or particle) · **लोप** (a word/qualifier/clause with no Hindi counterpart; any `(Tn)` with no Hindi line) · **वर्धन**
(Hindi adds matter not in that segment — legitimate in part 7, not in part 6) · **सन्देह** (defensible, another reading at least as good).

Check especially: the quoted प्राकृत सूत्र-पद (bold) + its Sanskrit gloss rendered as a gloss, not as Sanskrit prose; every question (`किं कर्तुम्?`,
`कथम्भूतम्?`, `किंविशिष्टम्?`, `क्व?`) paired with its own answer and attached to the noun it agrees with; every समास re-split by you; particles
`एव अपि तु हि च वा इति`; the case of a compound's final member; **enumerations complete** (the प्रतिक्रमण is made of counted sets — count the items in
Sanskrit and Hindi); quoted verses rendered completely; the टीका's definitions (अतिक्रम / व्यतिक्रम / अतिचार / अनाचार; आभोग / अनाभोग; the 25 क्रिया;
the 22 परीषह …) kept exactly as the टीका gives them; and **whether the Hindi could be true of its subject** — a reading that contradicts the सूत्र it explains
is wrong however well it parses.

**Not findings:** a different but equally faithful wording; the टीका being terse or odd. **Never invent a finding** — idiom, free expansion and an
explanation the Sanskrit supports are not errors.

Sanskrit that does not construe is a suspected transcription error: report as **सन्देह** with the reading you think the page has (confusions in this
print: `प्र`↔`म`, `त्व`↔`ल`, `ञ्च`↔`श्च`, `ष`↔`प`, `ण`↔`न`, `ध`↔`घ`, `द्व`↔`दव`, a dropped `अ` after a hyphen at a line break, a lost रेफ). Do not settle it
from any outside translation.

## B. Parts 7-क and 9-क — the reader's two special requirements

7-क (क्रिया का युक्तिसंगत उद्देश्य) and 9-क (आचरण-विधि एवं अभ्यास) were requested for their practical value to a साधु. They are also where an agent is most
tempted to over-reach. Check, and report as **सन्देह / त्रुटि**:

1. **Every क्रिया / दोष-निवृत्ति the सूत्र names has a bullet in 7-क** (grouped as the सूत्र groups them, none left out), with उद्देश्य, युक्ति and निवृत्ति;
   the युक्ति is a real argument, not a restatement; the targeted कषाय/दोष is plausible and the *mechanism* is stated.
2. **Source honesty.** Things the टीका states are marked `टीका के अनुसार` and really are in the टीका; the writer's own reasoning is marked
   `व्याख्याकार का तर्क`. Report any place the writer's reasoning is presented as the टीका's or the आगम's.
3. **9-क tags.** Every item carries `[आगम-सम्मत]` or `[सुझाव]`; every `[आगम-सम्मत]` really is in the टीका/आगम (check against the Sanskrit); **no suggested
   frequency, count, duration or hour is presented as आगम-विधान.**
4. **Nothing against the आगम; no new vow, no new प्रायश्चित्त, no softened rule.** A technique must serve the very क्रिया the सूत्र prescribes. Flag any
   that invents a rule or relaxes one (illness, travel, a missed प्रतिक्रमण and the choice of प्रायश्चित्त go to the गुरु, not resolved). दैवसिक = the day,
   रात्रिक = the night: flag any mix-up.
5. **Fabricated authority.** Every citation (ग्रन्थ + number) in parts 7, 7-क, 9-क, 10 and the `सन्दर्भ-संकेत:` line: is it certain? A wrong number is a
   **त्रुटि**; an unverifiable one should be `लगभग`/`सम्भवतः` or dropped. Report each you believe is wrong or cannot confirm.
6. **तत्त्वार्थसूत्र in the सर्वार्थसिद्धि recension** (7.13 प्रमत्तयोगात्प्राणव्यपरोपणं हिंसा; 9.2 स गुप्तिसमितिधर्मानुप्रेक्षापरीषहजयचारित्रैः;
   9.5 ईर्याभाषैषणादाननिक्षेपोत्सर्गाः समितयः).

## C. Parts 2–5, 8–10 and the two top lines

- **Part 5 (सूत्र का हिन्दी अनुवाद):** renders exactly what the सूत्र says — nothing added from the टीका, every पद represented, particles kept, reads as
  natural Hindi.
- Part 2 (छाया): faithful to the टीका's glosses, the सूत्र's breaks kept, correct sandhi; **no "व्याख्याकार-कृत" note in the §** (it is said once in the
  भूमिका); absent when part 1 is Sanskrit or absent.
- Parts 3–4: the अन्वय uses only the सूत्र's own प्राकृत words; every पद accounted for in the अन्वयार्थ.
- Part 8: the दृष्टान्त↔दार्ष्टान्तिक mapping holds and its limit is stated; a कथा from the टीका is told as the टीका tells it. Part 9: the table is accurate.
- Part 10: 1–3 bullets only; no process language; no sect names; no bare आचार्य names in prose; **no translator / editor / मुनि / माताजी name anywhere**.
- **`शीर्षक:`** says accurately what the § establishes, from the Sanskrit alone. **`सन्दर्भ-संकेत:`** gives the right ग्रन्थ, page and दण्डक.

## Output

One file per range: `verify/v<first-key>-<last-key>.md`.

```markdown
# परीक्षण — §<first> से §<last>

## निष्कर्ष
- परीक्षित §: N | परीक्षित खण्ड (Tn): M
- त्रुटि: a | लोप: b | वर्धन: c | सन्देह: d

## निष्कर्ष-विवरण
### §<key> (T<n> | भाग 7-क | भाग 9-क …) — त्रुटि
- **संस्कृत / आधार:** <quote exactly>
- **लिखित हिन्दी:** <quote exactly as in addenda/>
- **दोष:** <1–2 sentences with the grammatical or doctrinal reason>
- **सुझाया हिन्दी:** <a complete replacement line, ready to substitute>
```

A `सुझाया हिन्दी` (complete replacement) for every त्रुटि and लोप; for सन्देह, the alternative reading and which you prefer. A clean § gets no entry. End
the file with the counts repeated. Write incrementally (after the first few §, then append). Quote Sanskrit and Hindi **exactly as the files have them** —
the fix is applied against your quotation. If a § is sound, that is a real result — do not invent findings to seem thorough.

## Scan-reading rule for this audit (binding)
This book prints the Sanskrit टीका and the Hindi translation on **separate pages**: in the टीका section (pdf 21–220) the **odd pdf pages carry the
Sanskrit** and the even pages carry the Hindi; the परिशिष्ट (pdf 221–233) carries only the मूल पाठ. **pdf page = मुद्रित पृष्ठ + 19.** You may check a
doubtful Sanskrit/Prakrit reading on the scan **only on an odd pdf page in 21–219 or a page in 221–233**, rendered from the PDF as a zoomed crop:

```
python -c "import pymupdf; d=pymupdf.open(r'mool/Pratikraman_Granthtriyi.pdf'); d[PDF-1].get_pixmap(dpi=450, clip=pymupdf.Rect(x0,y0,x1,y1)).save(r'<your scratch>/z.png')"
```
(page box 792×612 pt, landscape.) Exceptions seen in the scan: pdf 116 (even) carries the टीकाकार's closing verse and the colophon of ग्रन्थ 1 (Sanskrit) together with a modern
translator's line — crop to the Sanskrit lines only; pdf 117 (odd) is the बृहत्प्रतिक्रमण title page. **Never open any other even pdf page in 22–220 and never open `img/`** — those show the printed Hindi, which this book must not
be influenced by. If a page you open turns out to carry Hindi, close it and use none of it.
