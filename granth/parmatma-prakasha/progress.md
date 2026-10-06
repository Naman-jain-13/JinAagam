# परमात्मप्रकाश एवं योगसार — व्याख्या progress log

*Working notes only. Nothing from this file goes into the book.*

## Source — and why this edition

Two scans were in `mool/`. **Use `Parmatmaprakash_and_Yogsara_001876.pdf` (550 pp).** The other,
`06575 Parmatma Prakasha, Yogendo.pdf` (332 pp), is set in an old fount with systematic glyph
substitutions — **अ prints as a ग्र-like glyph** (`ग्रहं` = अहं, `ग्रथ` = अथ) and **ण as a रा-like one**
(`परिरगामो` = परिणामो). Transcribing from it would seed errors into every downstream Hindi rendering.
Confirmed at 500 dpi. Do not use it, not even for collation, without allowing for the fount.

The chosen edition is A. N. Upadhye's, Paramaśruta Prabhāvaka Maṇḍala / Rajchandra Jain Śāstramālā:
clean modern fount, no text layer (the embedded text is only the library watermark).

## What each printed page carries — verbatim for agent prompts

Above a horizontal rule:
1. the **अपभ्रंश दोहा** in bold, ending `॥ ३९ ॥`;
2. its **संस्कृत छाया**, two lines, smaller type — *already printed in this edition*, so it is transcribed,
   never reconstructed;
3. **श्री ब्रह्मदेव's संस्कृत टीका**, dense, with the दोहा's own अपभ्रंश words set in bold and glossed inline.
   It runs in the **कथंभूत catechetical style**: a statement, then `किं कृत्वा ।` / `कथंभूतः ।` / `कस्मात् ।` /
   `कः ।` / `कान् ।` and the answer to each.

Below the rule:
4. the **हिन्दी अनुवाद**, which prints the Sanskrit lemma in **square brackets** before each rendering —
   `[पुराकृतं कर्म] पूर्व उपार्जित कर्मोंको [क्षपयति] क्षय करता है` — an explicit Sanskrit↔Hindi alignment;
5. **भावार्थ**.

Running header: `–दोहा १९० ]  परमात्मप्रकाशः  २९५` or `योगीन्दुदेवविरचितः  [ अ० २, दोहा ३९–`.

## Scan map (established from a header contact sheet; offset is 161 throughout)

| section | scan | printed | in this book |
|---|---|---|---|
| English introduction (Upadhye) | 1–161 | — | **no** |
| **परमात्मप्रकाश, अधिकार 1** | 162–~275 | 1–~114 | yes |
| **परमात्मप्रकाश, अधिकार 2** | ~276–478 | ~115–317 | yes |
| परमप्प-पयासु — critical अपभ्रंश text with ms. variants | 481–~513 | 320–~352 | no (verification witness only) |
| परमात्मप्रकाशदोहादीनां वर्णानुक्रमसूची | ~514–520 | ~353–359 | no (verification witness only) |
| **योगसार** | 521–~546 | 360–~385 | yes |
| publisher's back matter | 547–550 | — | no |

Images rendered at 300 dpi for the two content ranges only: `img/p0162.png`–`p0479.png` and
`img/p0521.png`–`p0547.png` (345 files).

**Two witnesses the volume gives us for free**, both outside the book but valuable for checking:
the critical अपभ्रंश text with manuscript variants (scan 481+) and the alphabetical दोहा index (scan 514+).
Render them when a reading needs settling.

## The three passes

The reader's standing instruction on this ग्रन्थ is that **the Hindi must not say anything the Sanskrit
टीका does not**. The failure they saw before was Sanskrit mistranslated — wrong sense, a समास split
wrongly, or a `कथंभूत` question attached to the wrong phrase. The passes are built around that.

| pass | model | writes | into |
|---|---|---|---|
| 1 — extraction | **Sonnet 5** | अपभ्रंश दोहा · मुद्रित संस्कृत छाया · ब्रह्मदेव टीका · मुद्रित हिन्दी · भावार्थ — all verbatim | `parts/` |
| 2 — व्याख्या | **Opus 5** | अन्वय · अन्वयार्थ · **टीका का खण्डशः हिन्दी अनुवाद** · विस्तृत व्याख्या · उदाहरण · तालिका · सन्दर्भ | `addenda/` |
| 3 — **verification** | **Opus 5** | an independent Sanskrit↔Hindi audit of every § written by pass 2 | `verify/` |

Pass 3 is new to this project and is the whole point. A *different* agent from the one that wrote the
Hindi reads the Sanskrit टीका and the Hindi side by side, clause by clause, and reports every place the
Hindi adds, drops or alters sense. Nothing self-certifies.

## Lessons

(appended as they happen)
