# आप्त-परीक्षा

**श्री विद्यानन्द स्वामी — स्वोपज्ञ आप्तपरीक्षालङ्कृति-टीका सहित**

**स्थिति — पूर्ण** · दो चरण: पहले मूल संस्कृत निकाला (§ 0–325), फिर केवल उसी से नई व्याख्या (326 §, 1022 पृष्ठ)

## इस फ़ोल्डर में क्या है

| | |
|---|---|
| `mool/` | मूल ग्रन्थ का स्कैन — `Aapt_pariksha_001613.pdf` |
| `mool_book/` | बनी हुई किताब — `Aapta_Pariksha_Mool_Sanskrit.docx`, `Aapta_Pariksha_Mool_Sanskrit.pdf`, `meta.json`, `parts` |
| `vyakhya/` | बनी हुई किताब — `Aapta_Pariksha_Vyakhya.docx`, `Aapta_Pariksha_Vyakhya.pdf` |
| `parts/` | अनुच्छेदशः मूल पाठ + व्याख्या — 33 फ़ाइलें · **यही असली मेहनत है** |
| `frontmatter/` | प्रस्तावना, समर्पण आदि |
| `img/` | स्कैन के रेंडर किए पन्ने — 476 PNG · _git में नहीं, मूल PDF से दोबारा बनते हैं_ |
| `progress.md` | कहाँ तक हुआ, आगे क्या — **काम यहीं से उठाइए** |
| `addenda/` | भाग 6 की विस्तृत पाठभेद-सामग्री (`bhag6_vistrit_*.md`) एवं संक्षिप्त रूप (`condensed/`) |
| `backmatter/` | उपसंहार, परिशिष्ट, सन्दर्भ-सूची, शब्दावली — 4 फ़ाइलें |
| निर्माण-स्क्रिप्ट | मूल: `assemble_mool.py`, `build_mool_docx.py`, `check_mool.py` · व्याख्या: `meta.json` + `groups.json` → skill का `build_docx.js`, फिर `run_finalize.cmd` |

सब रास्ते इसी फ़ोल्डर के सापेक्ष हैं — स्क्रिप्ट यहीं से चलाइए।
