# Pitfalls learned across four books (≈1,100 scan pages)

Each of these cost real time once. Read before starting; re-read before the final build.

## Reading the scans
- **No text layer.** Old scans have none; `get_text()` returns "". Render to PNG (250–300 dpi) and *read the
  images*. Never OCR-guess dense Devanagari at low dpi — conjuncts and matras get misread (e.g. मालरापाटन
  for झालरापाटन). If a proper name looks odd, zoom (crop + re-render at 400 dpi) before writing it down.
- **Compare editions before transcribing a word — the fount decides the error rate.** Two scans of
  परमात्मप्रकाश sat in the same folder. One is set in an old fount with systematic glyph substitutions:
  **अ prints as a ग्र-like glyph** (`ग्रहं` = अहं, `ग्रथ` = अथ) and **ण as a रा-like one**
  (`परिरगामो` = परिणामो). Transcribing from it would have seeded errors into every downstream Hindi
  rendering. The other is a clean modern fount — and prints the संस्कृत छाया and bracketed Sanskrit lemmas
  as a bonus. Render one text page from each candidate at 500 dpi and *look* before choosing.
- **A PDF "text layer" is often only the library watermark.** Check that `get_text()` returns actual
  Devanagari, not `Jain Education International / www.jainelibrary.org`, before planning around it.
- **Map a long volume by its running headers, not by reading pages.** Crop the header band from every 14th
  page, stitch the strips into one contact sheet with PIL, and read that single image: it gives section
  boundaries, the printed-page offset and where an appendix begins, in one look instead of thirty.
- **Two printed pages per scan** is common; each printed page may have two columns. Establish the reading
  order on the first content page and put it in every agent prompt.
- **Missing boxed headings.** A booklet's TOC may list a topic whose boxed heading was never printed
  (Gagar Saar topic 4). Trust TOC page numbers + content shift; insert the heading editorially and say so
  in a note.
- **Verse cut at a page top** belongs to the previous batch. Make every agent read one page *before* its
  range and start at the first complete unit.
- **In a bilingual edition the translation is a witness for its own source text — read it before you zoom.**
  This is the single highest-yield trick found on परमात्मप्रकाश and it cost nothing. The edition prints the
  संस्कृत टीका above a rule and a हिन्दी rendering below it that glosses the टीका's own terms, Sanskrit lemma
  in brackets. Two readings that had defeated magnification fell to it at once: a compound that appeared to
  read `कविलवादिलगमकलवाग्मिल` was settled by the Hindi's *"…ये **चार तरहका** शब्द-गौरव"* (four abstracts, so
  `कवित्व-वादित्व-गमकत्व-वाग्मित्व`), and a quoted verse that appeared to read `द्वेषाद्रोहाच्च` by the Hindi's
  *"और **रागभावसे** परस्त्री आदिका चिंतवन करे"* (so `द्वेषाद्रागाच्च`, the ordinary राग/द्वेष pair).
  **Tell extraction agents to consult the facing translation first and magnify second.**
- **Never emend by deleting a printed letter — it is the correction that always looks reasonable and is
  always wrong.** A page printed `मोहो ममलादिविकल्पजालं`. `ममल` is not a word, so the agent dropped one `म`
  and wrote `मलादि`, which *is* a word and is not what the page says. The right move was the fount's own
  confusion table: `ल` renders `त्व` in this type, giving `ममत्वादि` — every printed letter used, standard
  vocabulary, and attested fourteen times elsewhere in the same corpus. **Make the printed letters the
  constraint:** substitute a letter the fount is known to confuse, or flag it, but never discard ink to
  reach a word. A reading that throws letters away is worse than one that admits defeat.
- **Rejoin words broken across a line end before reading them.** `…द्वेषाद्रा-` at one line's end and
  `गाच्च…` at the next line's start was read as a single visual unit and yielded the non-word `रोह`. Whenever
  a doubtful word sits at the very start or very end of a line, find its other half first.
- **A quotation from another ग्रन्थ has a received text — recall it.** Commentaries quote constantly. If a
  reading of a quoted verse differs from how that verse is normally transmitted, the reading is what to
  doubt. The `द्वेषाद्रागाच्च` case is श्री समन्तभद्र स्वामी's रत्नकरण्डश्रावकाचार, where the standard text
  settles it independently of the scan.
- **A systematic fount fault is settled lexically, not optically — sweep the corpus, don't zoom the page.**
  In परमात्मप्रकाश's small टीका fount the `प्र` ligature's lower stroke merges into its bowl and the conjunct
  reads as a plain `म`. Zooming does *not* help: at 1100 dpi the scan has no more information to give. Four
  readers hit it independently before it was named, and 14 instances needed correcting afterwards
  (`सर्वमकारेण` for `सर्वप्रकारेण`, `मतिपक्ष` for `प्रतिपक्ष`, `अभिमायो` for `अभिप्रायो`, `मत्ययः` for `प्रत्ययः`).

  What settled it was the corpus, not a sharper image. **The same words print legibly elsewhere in the same
  volume**: a count gave `प्रतिपक्ष` clean 9 times against 6 degraded, `अभिप्राय` 12 against 1. The decisive
  test is lexical — *if a letter sits where no word of the language can have one, it is the other letter.*
  So: when any glyph confusion recurs, stop zooming and run a whole-corpus grep for the impossible sequences
  it would produce, then fix them all at once. One sweep finds what page-by-page reading never will.

  **Triage the sweep by hand.** The same sequences occur in perfectly good words — `समभाव`, `परमभाव`,
  `माया`, `कर्मणाम्`, `निरुपम`, `समाप्तम्`, `परिणमति` all survived this one. An unreviewed bulk replace
  would have introduced more errors than it removed.
- **Where a page has two text streams, they are not synchronised — never derive unit boundaries from page
  position.** परमात्मप्रकाश prints the संस्कृत टीका above a horizontal rule and the हिन्दी below it, and a
  single page's टीका routinely closes verse 57 and opens 58 while the हिन्दी below is still finishing 57.
  Follow each stream by its own `॥ N ॥` closings. Consequences worth telling agents up front: a page can
  carry **no new verse at all**, which is not a gap; and an agent will often need to read a page or two past
  its range to finish one stream after the other has closed.
- **A transitional lead-in sentence belongs to the unit it introduces, not the one it follows.** Both streams
  do this — the Sanskrit पातनिका sits above its verse, and the Hindi's `इसके बाद … कहते हैं–` sits at the
  *tail of the previous verse's paragraph*. The second is the easy one to mis-attribute.
- **A form that recurs consistently is the edition's, not a misprint.** परमात्मप्रकाश's टीका writes `संपितं`
  for `संपादितं` every time, with the verse's own Prakrit `संपिय` behind it. One odd spelling is a suspect;
  the same odd spelling four times over is the text. Print it and note it — do not regularise.

## Parallel agents
- **Numbering collisions.** Agents cannot see each other; two will both write "§ 4" / "ग्रन्थ-4". Either
  hand each agent its starting number (when you can count units from the TOC) or make them write `§?` and
  renumber at consolidation. Always `grep -n "^§"` across parts/ after every wave.
- **Boundary duplication.** Despite instructions, adjacent agents both wrote the same verse twice on two
  occasions out of 33 seams. Ask each agent to report its exact first/last words; compare; delete the later
  copy with a line-range `sed -i`.
- **Answer/verse split across agents.** The tail of an answer landing at the top of the next agent's range
  arrives as an orphan fragment. Merge it into the previous file's last unit, remove the fragment and the
  duplicated heading from the next file.
- **Agents guess when they lack context.** The final agent of the अभिषेक project invented a "ग्रन्थ-सार"
  table with a wrong author for ग्रन्थ-1 and 6 missing texts. Summary tables that span the whole book are
  written by *you* (or an agent given *all* parts), never by a batch agent that saw 10 pages.
- **Identity by evidence, not assumption.** A running header can be a poetic title while the colophon gives
  the real name (नित्यमहोद्योतम् / अर्हद्दैवमहाभिषेकविधिः). Confirm a text's name/author from its
  colophon or a printed serial number before naming it in a heading.

- **A whole unit can go missing between two adjacent agents, and each report will look fine.** दोहा 12 of
  परमात्मप्रकाश was lost because the agent owning page 18 thought it began on page 19 and the agent owning
  page 19 thought it began on page 18. Both reports were internally consistent and neither was lying. **The
  only thing that catches this is a coverage gate that knows how many units the ग्रन्थ should have** and
  tests contiguity. Get that number from the text itself where you can — परमात्मप्रकाश's own पीठिका declares
  25+24+43+31 = 123 and 30+36+41+107 = 214, and अधिकार 2's opening colophon repeats the 214.
- **Telling agents to check the running header is necessary but not sufficient.** It is a good cheap check —
  the header names the unit each page runs to — but **a unit that opens and closes inside a single page may
  never appear in any header at all.** दोहा 16 of अधिकार 2 sits entirely within the page whose header says
  दोहा 17, and a header-only check would have passed with it missing. So ask agents for *two* checks: every
  unit named in a header has a §, **and** the units they wrote run consecutively with no skipped number.
  The second is the one that catches a swallowed unit.
- **64k output cap per response.** An agent that drafts 8 dense pages and then writes the whole file in one
  Write call dies with "exceeded the 64000 output token maximum" and leaves nothing on disk. Template A now
  tells agents to save every 2–3 § (Write once, then Edit-append). Keep ranges <= 8 pages for dense prose.

## Content rules that were enforced by the reader
- **No sect names** (बीसपंथ/तेरापंथ) anywhere — the reader stopped the work to say so.
  The rule is about **sub-sect labels used as editorial positioning**, and it does not reach a मूल that
  itself makes the distinction its subject. परमात्मप्रकाश दोहा 88 argues that the आत्मा is none of the
  लिंग and names बौद्ध, दिगम्बर and श्वेताम्बर to do it; those words are the ग्रन्थ's own argument, so they
  are transcribed verbatim. The व्याख्या then presents them exactly as the मूल does — as लिंग-भेद the आत्मा
  transcends — and takes no side. If an extraction agent asks whether such a verbatim exception is intended,
  the answer is yes; it is a sign the agent read the rule properly.
- **No working-process language** leaks into the book. 100+ occurrences of "बैच", "अगले बैच में", "batch04"
  had to be scrubbed after the fact. Put the ban in every agent prompt; grep for it before every build
  (`check_quality.py parts`). Cross-refer with § numbers, "पूर्व-वर्णित", "आगामी अंश".
- **All six parts, every §.** A build with only parts 1–3 and no TOC/page numbers was rejected outright.
- **Real page numbers in the TOC.** Only Word can compute them; LibreOffice will not update the field.

- **Honorifics and reference size are a post-build step.** Writing "श्री … स्वामी" at source is not enough —
  110 bare names slipped through in one book. `postprocess_docx.py` runs on the built .docx (before Word)
  and is idempotent; `check_quality.py docx` fails if it was skipped. Watch hyphenated compounds
  ("श्रीमदाचार्य-अनन्तकीर्ति") — an early version doubled the श्री there; the title page is the place to look.

## Regenerate derived files after every repair, and check against the source

Work assignments, section lists and page maps are **derived** from the extracted text. When a repair adds
units to the source, those files do not update themselves, and every agent dispatched from them will report
complete while the new units sit untouched.

On परमात्मप्रकाश the same three verses were lost **twice, by two different mechanisms**: first by a scan map
built from running headers, which could not see that they sat on a *title page* (a title page has no running
header); then by a work-assignment file generated before they were found, so thirty agents were dispatched
from a plan that did not know they existed. Each agent completed its own list correctly both times.

Two habits prevent it:

- **regenerate every derived file immediately after any repair to the source**, and
- **make the completion check compare against the source, never against the plan.** A plan that is wrong
  looks perfectly complete; only `units in source` vs `outputs on disk` exposes it.

## Gates have bugs too, and they are nearly always the same bug

Three times on one book, in three different gates, a check reported a false result because **a regex found
*a* match where the *right* match lay elsewhere**:

- a colophon's count read from the **first** number word, when these colophons nest and name the containing
  division before their own — a स्थल of 8 reported as 41;
- a § assigned from the **first** `दोहा N` in its title, when the authoritative reference is the
  parenthetical at the end — a descriptive prefix ("प्रक्षेपक दोहा 1: …") silently moved three sections to
  दोहा 1, 2 and 3;
- a numeral read as the **shorter of two overlapping** words — `सप्तदशक` (17) contains `दशक` (10), both end
  at the same character, and a "rightmost match" rule made the short one win.

Each fix is different — scope (search inside the parenthetical), position (take the last), length (prefer
the longer on a tie) — and **one does not substitute for another**: sorting a table longest-first stops
helping the moment you start ranking matches by position.

So whenever a field can occur more than once in a string, **say explicitly which occurrence is
authoritative**, and write the reason in the code. A gate that is confidently wrong is worse than no gate,
because its green light is believed.

## Gates, and what they cannot see

Automated gates are necessary and not sufficient. Learned on a 1,514-page book:

- **Three green gates passed a build with 700 literal asterisks in it.** The व्याख्या marks emphasis as
  `*word*`; the generalised `build_docx.js` parses only `**bold**`. One glance at a rendered page found it.
  **Always render title, TOC, two body pages and a back-matter page, and look at them.**
- **Run a coverage gate only after every agent of a wave has REPORTED.** Checking while agents still append
  looks exactly like a seam gap and costs a wasted repair agent. File mtimes are not a substitute.
- **A skipped unit hides behind a complete-looking report.** One batch reported "गाथा 111–121, no gaps" and
  was internally consistent, yet never wrote §109–110. The tell was its own footnote sidecar, which had
  entries for them. **Cross-check sidecars against the main files.**
- **A gate that tests "does a § with exactly this number exist" reports every merged unit as missing.**
  Where several verses share one commentary they become one §; test "is this verse covered by some §".
- **Scope word-list rules to whole words.** `बैठक` (a work session) is a substring of the ordinary verb
  `बैठकर`; it fired 13 times on innocent prose.
- **Keep every tool's notion of "quoted text" identical.** The honorific post-processor, the source-level
  gate and the quality checker must agree on which parts reproduce the मूल, or they contradict each other
  and you end up trusting none of them.

## Honorifics — two traps

- **The post-processor misses a name with a Hindi case-ending attached.** Its regex refuses any following
  Devanagari, so `योगीन्दुदेवने`, `ब्रह्मदेवकी`, `देवसेनके` all slip past — which in Hindi prose is *most*
  occurrences, not an edge case. Let the matcher take an optional विभक्ति (ने|की|का|के|को|से|में|पर) and
  re-attach it after inserting the honorific.
- **Some आचार्य names are also ordinary words.** `अनन्तवीर्य` is a member of the अनन्तचतुष्टय far more
  often than it is an आचार्य; honouring it prints "अनन्तसुख और श्री अनन्तवीर्य स्वामी" mid-sentence.
  Before a run, grep each name in the corpus and check what it actually is in *this* text.

## Citations

- **तत्त्वार्थसूत्र has two recensions and mixing them is easy.** For दिगम्बर texts use सर्वार्थसिद्धि
  numbering: 5.29 सद्द्रव्यलक्षणम् · 5.30 उत्पादव्ययध्रौव्ययुक्तं सत् · 5.31 तद्भावाव्ययं · 5.38
  गुणपर्यायवद् द्रव्यम्. Writing 5.29 for उत्पाद-व्यय *and* 5.38 for गुण-पर्याय means both systems are in
  play at once. Tell agents: when unsure of a number, cite the सूत्र text and अध्याय alone.
- **A bibliography lists what the book actually cites.** Verify each entry by grep; drop anything famous
  you cannot find cited, and add anything cited that your brief forgot.

## Word / DOCX mechanics
- **Footer page numbers "11, 22, 33".** Adding a second section (cover page) and then touching `.footer` on
  *both* linked sections appends two PAGE fields to the shared footer. Set the footer once on section 0 only.
- **Orphaned headings.** A heading sitting alone as the last line of a page was reported on 5 pages. Set
  keep-with-next on every heading style (both builders do). Verify with `check_quality.py pdf`.
- **Blank half-pages.** Forcing a page break before every § wasted space and was reported. Page breaks only
  before Heading 1 (खण्ड / ग्रन्थ); § flow continuously with a thin rule above.
- **Word COM is slow.** 450–500 pages of Devanagari + tables: TOC update + PDF export takes 30–60 minutes.
  Run it in the background; check that `WINWORD` CPU time keeps rising; do not kill it because it "looks
  stuck". Never write to the .docx while Word has it open (EBUSY). If a run is aborted, `Stop-Process WINWORD`
  before retrying.
- **Windows paths in Python.** The Windows Python does not understand `/tmp` or `/c/Users/...`. Use
  `C:/Users/...` paths inside scripts; `PYTHONIOENCODING=utf-8` when printing Devanagari.

## Process
- **Rebuild everything from parts/.** Never hand-edit the .docx — every fix goes into the markdown and the
  book is regenerated; otherwise the next rebuild silently loses it.
- **Preview before merging.** When a reader is unsure about a new page (cover, credits), build a 2-page
  standalone .docx/.pdf for approval first; don't touch the master until they say yes.
- **progress.md** in the work folder: rules, batch table (file → pages → contents), lessons. It is what lets
  a fresh session pick up after a context reset. Keep it out of the book.
- **Token budget.** ~10–14 dense pages per Sonnet agent ≈ 110–150 k tokens each. A 470-page collection took
  33 agents across 6 sittings; a 33-page Q&A booklet took 4 agents in one sitting.
