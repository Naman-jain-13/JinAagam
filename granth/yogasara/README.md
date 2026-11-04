# योगसार

**श्री योगीन्दुदेव** — 108 अपभ्रंश दोहे, संस्कृत छाया, पं. डॉ. जगदीशचन्द्र शास्त्री का मुद्रित हिन्दी अर्थ, पाठान्तर और व्याख्या।

यह फ़ोल्डर 2026-10-23 को `../parmatma-prakasha` से अलग किया गया। पहले योगसार उसी पुस्तक ("परमात्मप्रकाश एवं योगसार") का अन्तिम खण्ड था; अब यह स्वतन्त्र ग्रन्थ है। § कुंजियाँ वही रखी गई हैं: 30010–31080 (= 30000 + दोहा × 10)।

## इस फ़ोल्डर में क्या है

| | |
|---|---|
| `meta.json` | शीर्षक, आधार-संस्करण, संरचना; `out` = `vyakhya/Yogasara_Vyakhya.docx` |
| `parts/` | batch37–40: मूल, छाया, हिन्दी अर्थ, मुद्रित पाठभेद (दोहा 1–108) |
| `addenda/` | `s30010.md` … : अन्वय, अन्वयार्थ, व्याख्या, उदाहरण, तालिका, सन्दर्भ |
| `groups.json` | एक ही खण्ड-शीर्षक (§30010) |
| `frontmatter/` | भूमिका |
| `backmatter/` | उपसंहार, शुद्धि-सूची, शब्दावली |

## स्रोत

स्कैन: `../parmatma-prakasha/mool/Parmatmaprakash_and_Yogsara_001876.pdf` — स्कैन-पृष्ठ 520–545; मुद्रित पृष्ठ = स्कैन − 161 (मुद्रित पृष्ठ 359–384)।

## Build

```
node ../parmatma-prakasha/build_docx.js .
python postprocess_docx.py vyakhya/Yogasara_Vyakhya.docx
python check_quality.py docx vyakhya/Yogasara_Vyakhya.docx
python finalize_big.py vyakhya/Yogasara_Vyakhya.docx
```

builder §-कुंजी 3xxxx को योगसार मानता है (शीर्षक "योगसार, दोहा N", भाग 6 = पाठान्तर)। अन्वय/अन्वयार्थ addenda में हैं पर builder उन्हें नहीं छापता।
