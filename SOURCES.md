# मूल स्रोत-ग्रन्थ — Source Scans

इस परियोजना की सब व्याख्याएँ नीचे दिए स्कैन किए गए मुद्रित ग्रन्थों पर आधारित हैं।
**ये फ़ाइलें repo में नहीं हैं** (कुल ~357 MB) — ये पुस्तकालयों द्वारा डिजिटाइज़ की गई हैं और
jainelibrary.org तथा अन्य जैन डिजिटल पुस्तकालयों पर उपलब्ध हैं।

नया कंप्यूटर सेट करते समय इन्हें दोबारा डाउनलोड करके `E:\Projects\JinAagam\` (या जहाँ repo clone किया हो)
में रख दीजिए — नाम वही रखिए, क्योंकि `progress.md` और `meta.json` में इन्हीं नामों से सन्दर्भ हैं।

## जिन ग्रन्थों पर काम हो चुका / हो रहा है

| स्रोत फ़ाइल | आकार | किस काम के लिए | स्थिति |
|---|---|---|---|
| `Ashtasahasri.pdf` | 31 MB | `ashtasahasri_work/` | पूर्ण (574 §) |
| `Nyaay Kumud Chandra-001-Pt. Mahendrakumar Shastri.pdf` | 54 MB | `nyayakumud_work/` | चल रहा है (573 §) |
| `Nyaay Kumud Chandra-002-Pt. Mahendrakumar Shastri.pdf` | 64 MB | `nyayakumud_work/` (द्वितीय भाग) | चल रहा है |
| `02611 Abhishek Path - Sangrah, Soni, Pannalal.pdf` | 13 MB | `abhishek_work/` | पूर्ण (349 अनुच्छेद) |
| `Bruhat Sarvagya Siddhi [Acharya Anantkeertiji Vicharit]-Pt. Kallappa Nitave.pdf` | 5.7 MB | `bruhat_sarvagya_work/` | पूर्ण (80 §) |
| `Laghu Sarvagya Siddhi [Acharya Anantkeertiji Vicharit]-Pt. Kallappa Nitave.pdf` | 1.6 MB | `sarvagya_siddhi_work/` | पूर्ण (75 §) |
| `Nayachakko [Naya Chakra] [Shree Maailladhaval].pdf` | 32 MB | `nayachakra_work/` | आरम्भ |
| `Aapt_pariksha_001613.pdf` | 11 MB | `aapta_pariksha_work/` | आरम्भ |
| `Shantusagar jee.pdf` | 1.9 MB | `shantisagar_work/` (अंग्रेज़ी अनुवाद) | पूर्ण |
| `Gagar Saar.pdf` · `GAGAR MEN SAGAR - Book.pdf` · `Gagar Me Sagar 23-9-2025.pdf` | 3.5 + 41 + 6.3 MB | `gagar_saar_work/` (अंग्रेज़ी अनुवाद) | पूर्ण |
| `praman_pariksha_last_chapter_67_pages.pdf` | 3.8 MB | प्रमाण-परीक्षा का अन्तिम अध्याय | पूर्ण |

> **प्रमाण-परीक्षा** का पूरा स्कैन अब पास नहीं है; उसका markdown स्रोत भी नहीं बचा।
> कोश में वह तैयार `.docx` से पढ़ा जाता है (देखिए `encyclopedia/build_index.py` का `parse_docx`)।
> उसकी किताब Releases में सुरक्षित है।

## जिन ग्रन्थों पर काम अभी शुरू नहीं हुआ

| स्रोत फ़ाइल | आकार |
|---|---|
| `Savrutti Siddhi Vinischayasya [Bhattaarak Akalankdev Krut] [Anantveerya Teeka Sahit]-001-Dr. Mahendrakumar Jain.pdf` | 32 MB |
| `Siddhi Vinishchay Teeka (Acharya Anantveerya Virachit] [Dr. Mahendrakumar Sankalit Tippan Sahit]-002-Dr. Mahendrakumar Jain.pdf` | 25 MB |
| `Naya_Vinishchay_Vivranam_1_090296.pdf` | 19 MB |
| `Nyayvinishchaya_Vivarnam_2_090313.pdf` | 13 MB |

## स्कैन के पन्ने दोबारा कैसे बनाएँ

`*/img/` फ़ोल्डर (कुल ~1.65 GB) भी repo में नहीं हैं। जिस ग्रन्थ पर काम करना हो, केवल उसी के पन्ने बनाइए:

```python
import pymupdf, pathlib
src = "Ashtasahasri.pdf"                      # जो ग्रन्थ चाहिए
out = pathlib.Path("ashtasahasri_work/img"); out.mkdir(parents=True, exist_ok=True)
for i, page in enumerate(pymupdf.open(src)):
    page.get_pixmap(dpi=300).save(out / f"p{i+1:03d}.png")
```

(छोटे ग्रन्थों के लिए 110–150 dpi भी पर्याप्त रहता है; अष्टसहस्री जैसे सघन पाठ के लिए 300 dpi।)

## अधिकार

मूल ग्रन्थ अपनी प्रकाशन-तिथि (1915, 1926 आदि) के कारण सार्वजनिक क्षेत्र में हैं।
स्कैन डिजिटाइज़ करने वाले पुस्तकालयों के हैं — इसीलिए वे यहाँ पुनः-प्रकाशित नहीं किए गए,
केवल सूचीबद्ध हैं।
