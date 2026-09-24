# Pass 2 — व्याख्या spec (नयचक्र)

*Working document. Nothing in this file goes into the book.*

Pass 1 transcribed the whole ग्रन्थ: every § in `parts/` already carries **part 1** (the मूल प्राकृत गाथा with
its Sanskrit उत्थानिका, exactly as printed) and **part 5** (the editor's printed हिन्दी अनुवाद and विशेषार्थ).
Those two are finished and **must not be rewritten**.

You write the other seven parts into `addenda/sNNN.md`. This is the substance of the book — the reason it
exists. The reader is a मुनि or a विद्वान् श्रावक who finds नयचक्र hard and wants it opened up.

## What you write, per §

One file per §, named for its § number zero-padded to three digits: `addenda/s004.md`, `addenda/s123.md`.
A § covering several गाथा (its title says `गाथा 234–236`) gets **one** file, `s234.md`, treating the group
as one unit throughout.

Reproduce these headings **verbatim** — a builder keys on these words and will drop anything else.

```
## 2. संस्कृत छाया
## 3. अन्वय
## 4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ)
## 6. जैनागम के अनुसार विस्तृत व्याख्या
## 7. सरल उदाहरण
## 8. तुलनात्मक तालिका / चार्ट
## 9. सन्दर्भ एवं पाद-टिप्पणी
```

No `## 1.` and no `## 5.` — those exist already and yours would collide.

---

### 2. संस्कृत छाया

A **literal Sanskrit correspondence** of the प्राकृत गाथा, word for word, in the gatha's own order, laid out
in the same number of lines, ending with the same `॥४॥`.

This is phonology and morphology, **not paraphrase**. Keep the gatha's own case-endings, its own verb
forms, its own word order even where Sanskrit would prefer another. Standard correspondences in this text:

| प्राकृत | संस्कृत | | प्राकृत | संस्कृत |
|---|---|---|---|---|
| दव्व | द्रव्य | | सहाव | स्वभाव |
| णय | नय | | पज्जय | पर्याय |
| जेण / जम्हा | येन / यस्मात् | | तम्हा | तस्मात् |
| हुंति / होइ | भवन्ति / भवति | | णाण | ज्ञान |
| सामण्ण | सामान्य | | विसेस | विशेष |
| अत्थि | अस्ति | | णत्थि | नास्ति |
| सव्व | सर्व | | अप्पा | आत्मा |
| मोक्ख | मोक्ष | | णिच्छय | निश्चय |
| ववहार | व्यवहार | | लद्ध | लब्ध |
| सुद्ध | शुद्ध | | किरिया | क्रिया |

Where a प्राकृत form is genuinely ambiguous between two Sanskrit forms, give the one the printed हिन्दी
supports and note the alternative in part 9. Where part 1 carries `[अस्पष्ट]`, carry `[अस्पष्ट]` through into
the छाया too — never invent Sanskrit for text nobody could read.

### 3. अन्वय

The words **of the प्राकृत गाथा itself**, as printed, rearranged into straight prose order so the reader can
see how the verse parses: कर्ता → कर्म / विशेषण → क्रिया, with subordinate clauses placed where prose puts
them. One flowing line, or two for a long गाथा.

Do not substitute Sanskrit here, and do not add words the गाथा does not contain. A genuinely implied word
goes in `( )`.

### 4. अन्वयार्थ (पदच्छेद-सहित शब्दार्थ)

Every पद of your अन्वय, **in the अन्वय's order**, one per line, in exactly this shape:

```
- **जेण** (येन, तृतीया) = जिस कारण से
- **दव्वसहावं** (द्रव्यस्वभावम्, द्वितीया) = द्रव्य-स्वभाव को — दव्व = द्रव्य + सहाव = स्वभाव
- **हुंति** (भवन्ति, वर्तमान, प्र.पु.ब.व.) = होते हैं
- **॥४॥** = गाथा-क्रमांक
```

Split every compound with `+` and gloss each member. Give the grammatical form in `( )` after the Sanskrit
**wherever it decides the sense** — विभक्ति for nouns, tense/person/number for verbs, क्त्वान्त / तुमुन् /
कृदन्त for participles. This part is what lets a reader who knows Sanskrit but not Prakrit work through the
गाथा unaided; it is worth doing slowly.

### 6. जैनागम के अनुसार विस्तृत व्याख्या

**The heart of the book.** 4–8 bullets, each 120–220 words, each opening with a bold sub-heading:

- **the step in the argument** — what this गाथा establishes and why it comes *here*, after the previous one;
- **the doctrine behind it**, named and grounded — the सूत्र or ग्रन्थ it rests on (तत्त्वार्थसूत्र, पञ्चास्तिकाय,
  प्रवचनसार, समयसार, द्रव्यसंग्रह, नियमसार, गोम्मटसार, आप्तमीमांसा, सर्वार्थसिद्धि, धवला), cited only when
  you can stand behind it;
- **the opponent's actual position**, stated fairly before it is answered — बौद्ध क्षणिकवाद, सांख्य
  परिणामवाद, नैयायिक समवाय, वेदान्त अद्वैत, मीमांसक, चार्वाक. Do not caricature; the ग्रन्थ does not;
- **cross-links** — "देखें § 42", "इसी का विस्तार § 173 में", "पूर्वोक्त § 8 के बारह अधिकारों में से यह तीसरा है";
- **an honest limit** where the argument has one, or where the text is compressed and the reasoning has to
  be supplied.

The reader called this ग्रन्थ difficult. Where a गाथा is dense — the नय material especially — **expand**.
Explain the technical vocabulary on first use in the §. Say plainly what a निक्षेप or an उपनय *is* before
using it. A § whose गाथा is one line may still deserve six bullets.

Never pad. If a गाथा genuinely says one simple thing, four good bullets beat eight thin ones.

### 7. सरल उदाहरण

2–3 everyday analogies a श्रावक can follow — the potter and the pot, gold and its ornaments, the ocean and
its waves, milk and curd, the lamp lighting itself and the room, a coin's two faces. Draw on the ones the
जैन tradition itself uses where they fit; the ग्रन्थ's own विशेषार्थ often supplies one, and building on it
is better than inventing a new one.

State the दृष्टान्त, then the दार्ष्टान्तिक — what maps to what, and **where the analogy stops**. An analogy
whose limits are not marked misleads.

If the गाथा is purely enumerative (a list of भेद), write: `इस अनुच्छेद हेतु पृथक् उदाहरण आवश्यक नहीं।`

### 8. तुलनात्मक तालिका / चार्ट

One markdown table, 3–7 rows, of whichever kind the § actually calls for:

- भेद-प्रभेद (the नय's divisions, the निक्षेप's four, the स्वभाव's twenty-one);
- पक्ष / प्रतिपक्ष (जैन position against the एकान्तवादी one, with the दोष each incurs);
- निश्चय / व्यवहार on the same object;
- दृष्टान्त ↔ दार्ष्टान्तिक;
- a comparison across दर्शन.

Header row must be meaningful. If no table helps, write `इस अनुच्छेद हेतु तालिका आवश्यक नहीं।` — an empty
table is worse than none.

### 9. सन्दर्भ एवं पाद-टिप्पणी

**Very short — 1 to 3 one-line bullets, no blank line between them.** This part is printed at dictionary
size and the reader has asked repeatedly that it stay small. Put here only:

- the source of a verse quoted in the गाथा or its विशेषार्थ, with ग्रन्थ and number (`पञ्चास्तिकाय, गाथा 30`);
  `लगभग` or `सम्भवतः` when you are not certain, and nothing at all rather than a guess;
- a one-line पाठ-टिप्पणी where part 1 carries `[अस्पष्ट]`, a bracketed restitution, or a printed oddity;
- a parallel in another ग्रन्थ, one line.

The printed पाठान्तर for this § are already transcribed in `footnotes/bNN_*.md` — read them, and compress
what matters into a single bullet. Do not copy the whole apparatus across.

If there is nothing: `मूल पुस्तक में इस अनुच्छेद हेतु कोई पाद-टिप्पणी नहीं।`

---

## Before you write a §, read

1. **the § itself** in `parts/` — both part 1 and part 5. The printed हिन्दी is your primary guide to what
   the गाथा means; your व्याख्या explains and grounds it, it does not contradict it;
2. **its footnotes** in `footnotes/` — the printed पाठान्तर and citations for that गाथा;
3. **the §§ immediately before and after**, so your cross-links and your "why here" are real;
4. `index_disagreements.txt` — if a § in your range appears there, the ग्रन्थ's own गाथा index disagrees with
   the transcription about that verse's opening. Most entries are noise in the index, but say in part 9 when
   one looks substantive.

## Where the ग्रन्थ stands — context for every §

*द्रव्यस्वभावप्रकाशक नयचक्र*, प्राकृत, 425 गाथा, by **श्री माइल्लधवल**, drawing on **श्री देवसेन स्वामी**'s
नयचक्र and on **श्री कुन्दकुन्दाचार्य**'s शास्त्र (गाथा 1's उत्थानिका says so). गाथा 8–9 announce **twelve
अधिकार**, and the book keeps to them:

| अधिकार | गाथा | | अधिकार | गाथा |
|---|---|---|---|---|
| पीठिका | 1–7 | | निक्षेप | 270–283 |
| गुण | 8–16 | | उपचार | 284– |
| पर्याय | 17–34 | | दर्शन | –324 |
| द्रव्य | 35–146 | | ज्ञान | 325–328 |
| पञ्चास्तिकाय | 147–148 | | सरागचारित्र | –341 |
| तत्त्व + पदार्थ | 149–164 | | वीतरागचारित्र | –357 |
| प्रमाण | 165–172 | | निश्चयचारित्र | –417 |
| **नय** | **173–269** | | उपसंहार | 418–425 |

The नयाधिकार is 97 गाथा, nearly a quarter of the book, and is where the ग्रन्थ earns its name. Anything you
write in §§ 173–269 is the most load-bearing prose in the project.

**The colophon contradicts itself** and the व्याख्या should say so where it is relevant (§§ 423–425): गाथा 424
credits श्री माइल्लधवल with setting the दोहा-composed द्रव्यस्वभावप्रकाश into गाथा form, while गाथा 425 says
श्री देवसेन स्वामी re-composed the नयचक्र. Lay the tangle out; do not resolve it silently.

## Style — non-negotiable

- शास्त्रीय, clear हिन्दी. English digits in your prose (§ 42, गाथा 173, तत्त्वार्थसूत्र 5.29) — Devanagari
  digits **only** inside quoted मूल / संस्कृत / प्राकृत text, where `॥१७॥` stays as printed.
- **Never write any sect name** (बीसपंथ / तेरापंथ or any sub-sect label) anywhere, in any part, for any
  reason. Describe ritual or doctrinal variants neutrally: "कुछ परम्पराओं में…".
- **Jain आचार्य are never named bare.** `श्री कुन्दकुन्दाचार्य`, `श्री देवसेन स्वामी`, `श्री अमृतचन्द्र स्वामी`,
  `आचार्य श्री समन्तभद्र`, `श्री पूज्यपाद स्वामी`, `श्री अकलंकदेव`, `श्री विद्यानन्द स्वामी`, `श्री माइल्लधवल`.
  Non-Jain opponents — कुमारिल, धर्मकीर्ति, उदयन, शंकर — are written plainly. The मूल पाठ is never altered.
- **No working-process language anywhere**: no "बैच", "इस सत्र", "अगले भाग में", file names, scan pages,
  "उपयोगकर्ता", no mention of other agents or of how the book was made. Cross-refer only as "§ 42",
  "पूर्व-वर्णित गाथा", "आगामी अधिकार में".
- **तत्त्वार्थसूत्र numbering: use the दिगम्बर (सर्वार्थसिद्धि) recension, not the श्वेताम्बर one.** They
  diverge in अध्याय 5 and the wrong one is easy to reach for, because the श्वेताम्बर numbering is commoner
  in print. This ग्रन्थ is दिगम्बर and its own footnotes cite सर्वार्थसिद्धि, so:
  `सद्द्रव्यलक्षणम्` = **5.29** · `उत्पादव्ययध्रौव्ययुक्तं सत्` = **5.30** · `तद्भावाव्ययं नित्यम्` = **5.31** ·
  `गुणपर्यायवद् द्रव्यम्` = **5.38**.
  (In the श्वेताम्बर numbering those last two are 5.30 and 5.37 — if you find yourself writing 5.29 for
  उत्पाद-व्यय-ध्रौव्य *and* 5.38 for गुण-पर्याय, you have mixed the two systems. Four files in the first wave
  did exactly that and were corrected.) When you are not certain of a सूत्र number, cite the सूत्र text and
  the अध्याय alone — that is always safe and always useful.

- **Never fabricate.** Not a citation, not a verse number, not a doctrine. "लगभग" / "सम्भवतः" where unsure;
  silence where you do not know. A व्याख्या that invents a सूत्र number is worse than one that omits it —
  this book will be cited.

## Writing the files

**Write each § as its own file, immediately, one at a time.** Do not accumulate several § and write at the
end: a response is capped at 64,000 output tokens and an agent that batched its work has already lost
everything once on this project. Finish `s042.md`, write it, move to `s043.md`.

## Report back (under 250 words)

The § numbers you completed; any § where the printed हिन्दी and the गाथा seemed to disagree; any citation you
wanted to give but could not verify; any § you judged genuinely resistant and would flag for a human reader;
and confirmation that every § in your assigned range has a file.
