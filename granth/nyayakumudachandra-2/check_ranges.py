# हर batch फ़ाइल की परास (फ़ाइल-नाम से) उसके भीतर के वास्तविक अन्तिम मुद्रित-पृष्ठ-चिह्न से मिलाता है।
# अन्तर बड़ा हो तो वह बैच अपनी सौंपी गई परास पूरी किए बिना रुक गया — असली छूट का संकेत।
import re,glob,sys
sys.stdout.reconfigure(encoding='utf-8')
for f in sorted(glob.glob('parts/batch*.md'), key=lambda x: int(re.search(r'batch(\d+)',x).group(1))):
    m=re.search(r'batch\d+_p(\d+)-(\d+)', f)
    if not m: continue
    scan_s, scan_e = int(m.group(1)), int(m.group(2))
    expected_end = scan_e + 294  # मुद्रित ≈ स्कैन + 294 (अनुमानित, ±1-2 बहाव सम्भव)
    t=open(f,encoding='utf-8').read()
    pages=[int(x) for x in re.findall(r'मुद्रित पृष्ठ\s*(\d+)', t)] + \
          [int(x) for x in re.findall(r'\(पृष्ठ\s*(\d+)', t)]
    actual_end = max(pages) if pages else 0
    gap = expected_end - actual_end
    flag = f'  *** {gap} पृष्ठ शेष रह गए (सम्भव, बहाव जाँचें) ***' if gap > 2 else ''
    print(f'{f}: सौंपा गया अन्त मु.पृ.~{expected_end} | वास्तविक अन्त मु.पृ.{actual_end}{flag}')
