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

Images: `img/p0042.png … p0249.png` (paths are relative to this folder: `granth/nayachakra/`) at 300 dpi (p0249 kept only as the "read one page past" reference
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

## Two-pass split and model choice (revised 2026-09-24)

The A/B test recorded in the `extraction-model-choice` memory applies here: **Opus silently normalises worn
print toward correct Sanskrit**, which is exactly the wrong failure mode for transcribing a Prakrit गाथा
whose whole value is that it is what the page says. So the passes are split by *kind of work*, not by page:

| pass | model | writes | into |
|---|---|---|---|
| 1 — extraction | **Sonnet 5** | part 1 (संस्कृत उत्थानिका + प्राकृत गाथा, verbatim) and part 5 (the printed हिन्दी अनुवाद + विशेषार्थ / शंका-समाधान) | `parts/batchNN_pSSS-EEE.md` |
| 1b — sidecar | same agent | the page-bottom footnotes verbatim, keyed by § | `footnotes/bNN_pSSS-EEE.md` — **working input only, never built into the book** |
| 2 — reasoning | **Opus 5** | parts 2 (संस्कृत छाया), 3 (अन्वय), 4 (अन्वयार्थ), 6 (विस्तृत व्याख्या), 7 (सरल उदाहरण), 8 (तालिका), 9 (सन्दर्भ) | `addenda/sNNN.md` |

The builder routes a sub-section to its slot by keyword (`kind()`), not by which file it came from, so parts
2–4 living in `addenda/` is fine and needs no builder change.

Sonnet's two known weaknesses go into the pass-1 spec as explicit guards: **magnify every प्रति-संकेत
(अ० क० ख० मु० ज०) before writing it** — one agent on another book wrote 15 `द` against 1 `व` and every one
checked was wrong — and **always rejoin a word broken across a page break**.

Part 9 follows the compact rule: **1–3 one-line bullets, no blank line between them**; `postprocess_docx.py`
here has `REF_AFTER = 0`.

## Batch table

26 batches of 8 scan pages: 42–49, 50–57, 58–65, 66–73, 74–81, … , 234–241, 242–248.

| batch | scan pages | printed | § written | pass 1 | pass 2 |
|---|---|---|---|---|---|
| 01 | 42–49 | 1–8 | §1–§15 (गाथा 1–15) | done | |
| 02 | 50–57 | 9–16 | §16–§31 | done | |
| 03 | 58–65 | 17–24 | §32–§47 | done | |
| 04 | 66–73 | 25–32 | §48–§61 | done | |
| 05 | 74–81 | 33–40 | §62–§73 | done | |
| 06 | 82–89 | 41–48 | §74–§84 | done | |
| 07 | 90–97 | 49–56 | §85–§93 | done | |
| 08 | 98–105 | 57–64 | §94–§108 | done | |
| 08b | 107–108 | 66–67 | §109, §110 — seam repair | done | |
| 09 | 106–113 | 65–72 | §111–§121 | done | |
| 10 | 114–121 | 73–80 | §122–§136 | done | |
| 11 | 122–129 | 81–88 | §137–§155 | done | |
| 12 | 130–137 | 89–96 | §156–§169 | done | |
| 13 | 138–145 | 97–104 | §170–§182 | done | |
| 14 | 146–153 | 105–112 | §183–§208 | done | |
| 15 | 154–161 | 113–120 | §209–§234 | done | |
| 16 | 162–169 | 121–128 | §237–§255 | done | |
| 17 | 170–177 | 129–136 | §258–§270 | done | |
| 18 | 178–185 | 137–144 | §273–§295 | done | |
| 19 | 186–193 | 145–152 | §296–§307 | done | |
| 20 | 194–201 | 153–160 | §308–§321 | done | |
| 21 | 202–209 | 161–168 | §324–§336 | done | |
| 22 | 210–217 | 169–176 | §337–§348 | done | |
| 23 | 218–225 | 177–184 | §349–§367 | done | |
| 24 | 226–233 | 185–192 | §368–§380 | done | |
| 25 | 234–241 | 193–200 | §381–§402 | done | |
| 26 | 242–248 | 201–207 | §403–§425 — **ग्रन्थ closed** | done | |

**Verified through गाथा 93** (batches 01–07, 91 §): no gaps, no duplicates, every § title's gatha number
matching its § number, and the forbidden-word screen clean. Ranges abut exactly at every seam.

§ per batch falls from 16 to 9 as the book goes on, because the विशेषार्थ grows: printed pages 49–51 carry
**no मूल at all** — they are one continuous विशेषार्थ belonging to गाथा 84. Expect 8 scan pages to yield
anywhere from 7 to 16 §. § grouping so far:
§5 = गाथा 5–6, §8 = 8–9, §37 = 37–38, §50 = 50–51; all others one gatha each.

## खण्ड structure — the ग्रन्थ names its own twelve अधिकार

§8 (गाथा 8–9) lists them, so `groups.json` follows the ग्रन्थ rather than an editorial guess:

> गुण · पर्याय · द्रव्य · पञ्चास्तिकाय · सात तत्त्व · नौ पदार्थ · प्रमाण · नय · निक्षेप · उपचार ·
> तथा निश्चय-उपचार के भेद से सम्यग्दर्शन, सम्यग्ज्ञान, सम्यक्चारित्र

**All twelve अधिकार are now accounted for.** Only the उपचार→दर्शन boundary remains unfixed.
Boundaries confirmed from the scans:

| अधिकार | गाथा | evidence |
|---|---|---|
| पीठिका | 1–7 | `इति पीठिकानिर्देशः ।` printed p. 4, echoed in Hindi as "पीठिका समाप्त" |
| गुणाधिकार | 8–16 | गाथा 8–9 announce the twelve; `इति गुणाधिकारः ।` printed p. 9 closes it |
| पर्यायाधिकार | 17–34 | ends with the Hindi line "इस प्रकार पर्यायाधिकार समाप्त हुआ।", printed p. 17 |
| द्रव्याधिकार | 35–146 | `एवं द्रव्याधिकारः समाप्तः ।` printed p. 84 + Hindi echo. **Within it**, `इति द्रव्यसामान्यलक्षणम् ।` at p. 57 (गाथा 94) closes only the सामान्य-लक्षण sub-section — an earlier note that read this as the end of the अधिकार was wrong |
| पञ्चास्तिकायाधिकार | 147–148 | `इति पञ्चास्तिकायाः ।` printed p. 85 + Hindi echo |
| तत्त्व + पदार्थ | 149–164 | no separate `इति` for the आस्रव/बन्ध/संवर material; the two run together and close at `इति पदार्थाधिकारः ।` printed p. 95, echoed as "पदार्थाधिकार सम्पूर्ण।" |
| प्रमाणाधिकार | 165–172 | `इति प्रमाणाधिकारः ।` printed p. 99, echoed as "प्रमाणाधिकार समाप्त हुआ।" p. 100 |
| नयाधिकार | 173–269 | `इति नयाधिकारः ।` printed p. 135 — the ग्रन्थ's longest अधिकार, 97 गाथा. Within it, `असद्भूतव्यवहारः—` is set as a bare heading above गाथा 242 (printed p. 124) with no `इति` line — such headings are division points too and agents now report them |
| निक्षेपाधिकार | 270–283 | `इति निक्षेपाधिकारः ।` printed p. 140, printed **twice** on that page — once after गाथा 283's मूल and again after its अनुवाद |
| उपचाराधिकार | 284–… | begins at गाथा 284; its close not yet seen |
| सरागचारित्राधिकार | …–341 | `इति सरागचारित्राधिकारः ।` printed p. 173 + Hindi echo, at the गाथा 341/342 seam |
| दर्शनाधिकार | …–324 | `इति दर्शनाधिकारः ।` printed p. 162 + Hindi "दर्शनाधिकार समाप्त ।" |
| ज्ञानाधिकार | 325–328 | `इति ज्ञानाधिकारः ।` printed p. 163 + Hindi echo p. 164 |
| चारित्राधिकार | 329–357 | closes at `इति वीतरागचारित्राधिकारः ।` printed p. 180 (after गाथा 357); the Hindi echo on p. 181 is printed **बीतराग** with ब — kept as printed |
| (unnamed) | 358–417 | सामान्य-विशेष / सत्ता and कारणसमय-कार्यसमय material |
| निश्चयचारित्राधिकार | …–417 | `इति निश्चयचारित्राधिकारः ।` printed p. 205 + Hindi echo. A footnote there records that the ज० प्रति reads `वीतरागचारित्राधिकारः` instead — a real variant, kept in the sidecar, not harmonised |
| उपसंहार | 418–425 | closing verses and the ग्रन्थ's own colophon |

Not every boundary is the formal `इति …अधिकारः ।`; some are a plain Hindi sentence in the विशेषार्थ, and
one (`असद्भूतव्यवहारः—`) is a bare heading set above a गाथा.

**Layout warning for the closing अधिकार.** From about printed p. 162 on, the edition prints each new
अधिकार's मूल-block up front and lets the हिन्दी for the *previous* गाथा trail behind it — so गाथा 326's
विशेषार्थ appears *below* गाथा 327–328's मूल, and गाथा 328's below गाथा 329–330's. Match commentary to
मूल by the `॥number॥` only, never by position on the page.
Agents report both. `groups.json` is written once all boundaries are in — do not guess it early.

## The गाथा index as a verification table — what it is and is not worth

`gatha_index.md` transcribes परिशिष्ट 4 (419 rows) and `check_against_index.py` compares each §'s मूल against
the index's आद्य-पद for that गाथा number. It exists because a misread गाथा NUMBER is invisible to
`check_coverage.py` — the § sequence stays contiguous while pointing at the wrong verse — and one batch had
already found a printed number faded to `११२` that the index gave as `३१२`.

**It is a triage list, not a gate, and the first version of it was built wrong.** Comparing the words
literally gave 111 "disagreements" out of 300, nearly all of them noise in the *index* transcription rather
than errors in the body: `तण्णं` for `तच्चं`, `देहामार` for `देहायार`, `पंचाक्खत्था` for `पंचावत्था`, plus
sandhi splits like `अगुरुलहुगा अणंता` against `अगुरुलहुगाणंता`. That should have been predictable — the index
is itself a stamped scan, and one agent read ~420 tiny entries over six dense pages where each batch agent
read eight. **Using the noisier copy to adjudicate the careful one is backwards.** The index's own error rate
shows in its totals: 27 गाथा numbers absent, 19 numbers carrying two different openings — the signature of
misread digits (342 as 242, 326 as 226, 378 as 278).

Rebuilt to compare **consonant skeletons of the first six consonants**, it asks only "is §N the verse the
index calls N?" and ignores spelling entirely. That cut it to 64, and among those it found a real body
error: §123 read `वेहजुदो` where the page plainly says `देहजुदो` (the द/व pair from guard 0), corrected.

The remaining 64 are in `index_disagreements.txt` for the व्याख्या pass to resolve in context — that pass
reads each गाथा whole and is far better placed to judge them than a bulk comparison is. Where the index is
used one word at a time against the *image*, as the batch agents use it, it has been consistently right;
it is the bulk transcription that is noisy.

## PASS 1 COMPLETE — 2026-09-24

All 26 batches in. **360 §, गाथा 1–425, coverage gate green**: no gaps, no duplicates, no forbidden
vocabulary, every § carrying part 1 (मूल प्राकृत गाथा) and part 5 (the editor's printed हिन्दी + विशेषार्थ).
43 § are merged units covering two to four गाथा that share one विशेषार्थ.

Still open for the व्याख्या pass, all recorded in the files themselves as `पाठ-सूचना`:
- the 73 entries in `index_disagreements.txt` (mostly index-side noise; to be judged in context);
- bracketed restitutions at गाथा 91, 263, 368, 419, 424 and `[अस्पष्ट]` at गाथा 179, 220, 293, 353, 364, 382;
- printed inconsistencies kept as printed: `सत्य`/`सत्थ` (275 vs 277), `लक्खणवो`/`लक्खणदो` (399 vs 392),
  `मिच्छेत्तं`/`मिच्छत्तं`, गाथा 370's अनुवाद closing `॥372॥`, `बीतराग` for `वीतराग` (p. 181),
  and the colophon's माइल्लधवल/देवसेन contradiction.

## PASS 2 — the व्याख्या (started 2026-09-24)

Spec: `pass2_instructions.md`. Assignments: `pass2_assignments.json` (27 agents × 14 §, one agent per
entry, each handed an explicit § list because § numbers have gaps). Model: **Opus** — this pass is
reasoning, not extraction, and the A/B test that put Sonnet on transcription put Opus here.

Each agent writes `addenda/sNNN.md` carrying parts **2, 3, 4, 6, 7, 8, 9** — संस्कृत छाया, अन्वय,
अन्वयार्थ, विस्तृत व्याख्या, सरल उदाहरण, तालिका, सन्दर्भ. Parts 1 and 5 already exist in `parts/` and must
not be redefined; the builder merges the two sources by heading keyword.

Gate: `python check_addenda.py` — every § has a file, all seven headings present and ordered, parts 1/5 not
redefined, part 9 compact (1–3 bullets, no blank line between), no forbidden vocabulary, no bare आचार्य
names, and a warning list for thin व्याख्या (part 6 under 400 words or fewer than 4 bullets).

Waves of 5. Run the gate only after every agent of a wave has reported — the same rule as pass 1.

## The coverage gate

`python check_coverage.py` (in this folder) is the gate. It checks duplicates, missing गाथा, §-number vs
title mismatch, **§ that appear in a `footnotes/` sidecar but never got a unit in `parts/`**, missing
part 1 or part 5, and forbidden vocabulary. Exit code 1 on any problem.

Run it **only after every agent of a wave has reported**, never on mtimes alone.

## The ग्रन्थ's colophon contradicts itself — and that belongs in the व्याख्या

गाथा 424 says the द्रव्यस्वभावप्रकाश was found composed in दोहा verses and set into गाथा form by
**श्री माइल्लधवल**; गाथा 425, two verses later, says `सिरिदेवसेणमुणिणा … णयचक्कं पुणो रइयं` — that
**श्री देवसेन स्वामी** re-composed the नयचक्र. Two different names credited with the same act. Both lines
were re-zoomed and the discrepancy is in the printing, not the reading. परिशिष्ट 1 of the same volume is
`श्रीदेवसेनविरचिता आलापपद्धतिः`, so देवसेन is a real and distinct author in this textual family — which is
exactly the tangle the व्याख्या pass should lay out for the reader rather than resolve silently. गाथा 1's
own उत्थानिका already names श्रीकुन्दकुन्दाचार्य's शास्त्र as the source of the सारार्थ, so the ग्रन्थ has a
three-layered ancestry to explain.

There is **no पुष्पिका after गाथा 425**; the आलापपद्धति heading follows directly.

## Lessons

- **2026-09-22:** a first wave of 4 Opus agents was launched for parts 1–5 together and was stopped before any
  of them reached its first incremental write — `parts/` was left empty. Two changes as a result: the passes
  are split by model (see above), and every agent writes its file after the **first** § rather than the
  first two, so an interrupted agent still leaves something on disk.
- **Never run the seam check until the completion notification for every agent in the wave has arrived.**
  On 2026-09-24 the check was run while two agents were still appending their last sections; it showed
  batch01 ending at §13 and batch02 at §29 and looked exactly like the classic two-gatha seam gap. A repair
  agent was launched for गाथा 14–15 and 30–31, and minutes later both original agents reported having
  written through §15 and §31. The repair agent was stopped before it wrote anything, so no duplicates
  landed — but a few minutes' patience would have avoided the whole detour. File mtimes are not a safe
  substitute for the notification: an agent can be mid-`Edit` when the directory is listed.
- The "your range's LAST page is yours" section in `pass1_instructions.md` was added during that false
  alarm. It is still worth keeping — the failure it describes is real on other books in this pipeline — but
  it was not what happened here.
- **A skipped unit can hide behind a complete-looking report.** The batch covering printed 65–72 reported
  "गाथा 111–121 continuously, no gaps" and was internally consistent — but गाथा 109 and 110, printed at the
  top of page 66, never got a §. The tell was its own footnote sidecar, which *did* carry `§109` and `§110`
  entries: the agent read the page, transcribed its footnotes, and never wrote the units. `check_coverage.py`
  now cross-checks sidecar § against `parts/` § for exactly this. Trust the files, not the report.
- **The index is now doing preventive work, not just repair.** Batch 19 used it unprompted to fix
  `सुहेदुं`→`सुहहेदुं` before writing, and caught two places where body and index genuinely disagree
  (`मिच्छेत्तं` in the body at गाथा 302–303 against `मिच्छत्तं` in the index; `असुहं सुहं` against a
  compressed `असुहसुहं`). It transcribed the body and reported the disagreement, which is the rule — the
  printed index has its own typos and is a witness, not an authority.
- **The edition contradicts itself in places, and that is data.** `अरहंतसत्यजाणो` (गाथा 275) against
  `अरहंतसत्थजाणो` (गाथा 277) was verified at 700 dpi as a real difference in the printing, not a
  transcription slip. सत्थ (= शास्त्र) fits both contexts, so गाथा 275 is probably a printer's error — but
  both stand as printed with a पाठ-सूचना explaining it. Never harmonise the ग्रन्थ with itself.
- **The index pays off twice more.** गाथा 239's opening word was buried under the stamp and had been
  supplied as `[भेदु]` from the Hindi with a पाठ-सूचना; the index prints `भेदुवयारं णिच्छय २३९`, so the
  brackets came off and the note now cites the ग्रन्थ's own second witness instead of an inference. The
  index also confirms `सब्भूदमसब्भूदं १८७` and `मइसुद परोक्खणाणं १७०`. **Check the index before writing a
  bracketed reconstruction, not after.**
- **परिशिष्ट 4 (गाथानुक्रमणी) is a second witness and was sitting unused for 13 batches.** It prints every
  गाथा's opening words with its number in different type. It settled `जम्हा` vs `जह्रा` outright
  (`जम्हा णएण विणा १७४`), and independently confirms `तिक्काले` and `सुद्धो`. Now rendered at
  `img/p0310–p0315.png` and written into the spec. Ten `जम्हा` were already correct against five wrong —
  the same glyph had been going both ways across agents, which is exactly the kind of drift a second
  witness removes.
- **द्ध read as ढ्ढ is the worst confusion so far**, because the wrong form still looks like Prakrit. A
  द्रव्यसंग्रह गाथा 8 quotation came back as `वेदणकम्माणादा सुढणया सुढभावाणं`; at 1000 dpi the page reads
  `चेदणकम्माणादा सुद्धणया सुद्धभावाणं`, which is also the received text. गाथा 127's `लद्धा` had likewise
  become `लढ्ढा`. A sweep of every ढ in `parts/` and `footnotes/` found no others — the rest (पुढवी, वड्ढी,
  वुड्ढत्तं, निरूढ, and Hindi बुढ़ापा/बढ़ते) are genuine. `मुरव` in the त्रिलोकसार quotation is also genuine
  (मुरज, a drum — the simile for लोक's shape), not a ख/रव misreading.
- **Doubled conjuncts are a distinct error class.** A footnote quoting द्रव्यसंग्रह गाथा 3 was transcribed
  `तिकाले`; at 1100 dpi the page shows `तिक्काले`, which is also the received reading of that verse. क्क, ट्ठ,
  द्द and प्प all collapse toward their single form at normal zoom. Where a quoted verse has a known text,
  a disagreement with it is a signal to magnify, not licence to emend.
- A too-cautious agent preserves its own misreading. One wrote `रूवाइष्ड` where the page says `रूवाइपिंड`
  at 350 dpi, reasoning that it must not normalise. "Do not normalise" means do not improve a form you have
  read; it does not mean keep a form that is not a word. The spec now says so with this example.
- The project moved to `granth/nayachakra/` in the 2026-09-24 reorganisation; the old `nayachakra_work/`
  path in any older note is dead.
