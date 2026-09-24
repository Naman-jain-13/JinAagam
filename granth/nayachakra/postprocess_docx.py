# -*- coding: utf-8 -*-
"""
Post-processor for the ग्रन्थ-व्याख्या docx files (run AFTER build, BEFORE finalize_word.ps1).

1. "सन्दर्भ एवं पाद-टिप्पणी" (part 6 of every §): shrink to dictionary-size font
   (7 pt body, tighter line spacing); the part heading itself to 9 pt.
2. Jain आचार्य names: add honorific "श्री" (and "स्वामी" after bare names) everywhere
   outside the मूल संस्कृत पाठ blocks and outside the TOC.

Usage:  python postprocess_docx.py [--dry-run] <file.docx> [<file.docx> ...]
        --dry-run : report what would change (paragraph and name counts, sample names) without writing.
Pipeline position:  build_docx.js  ->  postprocess_docx.py  ->  finalize_word.ps1
Works on the raw word/document.xml so Word's namespace declarations stay intact. Idempotent: running it
twice adds nothing (names already preceded by श्री are left alone).
Why: the reader asked (a) that guru-paramparā names be written with respect — श्री … स्वामी — and
(b) that reference/footnote matter take minimal space (dictionary size). Extend NAMES when a new आचार्य appears.
"""
import re, sys, zipfile, shutil, os, io

REF_SIZE = 14        # half-points -> 7 pt
REF_HEAD_SIZE = 18   # 9 pt
REF_LINE = 240       # single spacing
REF_AFTER = 0        # compact part 9: no gap between reference bullets

# Names (longest variants first inside each alternation group). Bare form gets "श्री X स्वामी";
# forms already carrying a title-suffix (देव/सूरि/स्वामी…) only get "श्री ".
NAMES = [
    'विद्यानन्दि', 'विद्यानन्द', 'विद्यानंद',
    'अकलंकदेव', 'अकलङ्कदेव', 'भट्टाकलंक', 'अकलंक', 'अकलङ्क',
    'समन्तभद्र', 'समंतभद्र',
    'कुन्दकुन्द', 'कुंदकुंद',
    'उमास्वामी', 'उमास्वाति',
    'पूज्यपाद', 'देवनन्दि',
    'प्रभाचन्द्र', 'प्रभाचंद्र',
    'माणिक्यनन्दी', 'माणिक्यनन्दि', 'माणिक्यनंदि',
    'अनन्तवीर्य', 'अनंतवीर्य',
    'अनन्तकीर्ति', 'अनंतकीर्ति',
    'वादिराज', 'वादिदेवसूरि', 'वादिदेव',
    'हेमचन्द्र', 'हेमचंद्र', 'अभयदेव', 'सिद्धसेन', 'सिद्धर्षि',
    'अमृतचन्द्र', 'अमृतचंद्र', 'नेमिचन्द्र', 'नेमिचंद्र',
    'वीरसेन', 'जिनसेन', 'गुणभद्र', 'वसुनन्दि', 'देवसेन', 'यशोविजय', 'हरिभद्र',
    'मल्लिषेण', 'शुभचन्द्र', 'सोमदेव', 'जयसेन', 'रविषेण', 'पद्मनन्दि',
    'धरसेन', 'पुष्पदन्त', 'भूतबलि', 'वट्टकेर', 'शिवार्य', 'योगीन्दु', 'अमितगति',
    'आशाधर', 'पात्रकेसरी', 'कुमारनन्दि', 'धर्मभूषण', 'जिनभद्र', 'सुमतिदेव',
    'विद्यासागर', 'ज्ञानसागर', 'शान्तिसागर',
    'माइल्लधवल', 'माइल्ल धवल', 'ब्रह्मदेव', 'श्रुतसागर', 'मल्लवादी', 'अकलंकचन्द्र',
]
SUFFIX_TITLED = ('देव', 'सूरि', 'स्वामी', 'स्वाति')   # name already ends with a title
DEV = 'ऀ-ॿ'
NAME_RE = re.compile(r'(?<![' + DEV + r'])(' + '|'.join(NAMES) + r')(?![' + DEV + r'])')
# already honoured: श्री, श्रीमद्, श्रीमत्पण्डित, श्रीमदाचार्य … — also in hyphenated compounds "श्रीमदाचार्य-अनन्तकीर्ति"
PRE_SKIP = re.compile(r'श्री[' + DEV + r']*[\s\-–]*$')
PRE_TITLE = re.compile(r'(आचार्य|स्वामी|भट्ट|भट्टारक|मुनि|भगवान्|भगवान|महाराज|पण्डित|पंडित|पं\.|कवि|योगीन्द्र|भदन्त)[\s\-–]+$')
POST_TITLE = re.compile(r'^\s*(स्वामी|देव|सूरि|जी|महाराज|स्वामिन्)(?![' + DEV + r'])')
POST_COMPOUND = re.compile(r'^[-–]')                                 # "विद्यानन्द-कृत"

def honor(text, prev, nxt):
    out = []; last = 0
    for m in NAME_RE.finditer(text):
        s, e = m.span(); name = m.group(1)
        pre = (prev if s == 0 else '') + text[:s]
        post = text[e:] + (nxt if e == len(text) else '')
        out.append(text[last:s])
        if PRE_SKIP.search(pre):
            out.append(name)
        elif PRE_TITLE.search(pre) or POST_TITLE.match(post) or POST_COMPOUND.match(post) \
                or name.endswith(SUFFIX_TITLED) or name.startswith('भट्ट'):
            out.append('श्री ' + name)
        else:
            out.append('श्री ' + name + ' स्वामी')
        last = e
    out.append(text[last:])
    return ''.join(out)

P_RE = re.compile(r'<w:p(?=[ >]).*?</w:p>', re.S)
R_RE = re.compile(r'<w:r(?=[ >]).*?</w:r>', re.S)
T_RE = re.compile(r'(<w:t(?: [^>]*)?>)(.*?)(</w:t>)', re.S)

def para_style(p):
    m = re.search(r'<w:pStyle w:val="([^"]+)"', p); return m.group(1) if m else ''
def para_text(p):
    return ''.join(T_RE.findall(p)[i][1] for i in range(len(T_RE.findall(p))))

def set_run_size(run, sz):
    if '<w:rPr>' in run or '<w:rPr/>' in run:
        run = run.replace('<w:rPr/>', '<w:rPr></w:rPr>')
        rpr = re.search(r'<w:rPr>.*?</w:rPr>', run, re.S).group(0)
        new = re.sub(r'<w:sz w:val="\d+"/>', '', rpr); new = re.sub(r'<w:szCs w:val="\d+"/>', '', new)
        new = new.replace('</w:rPr>', f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>')
        return run.replace(rpr, new)
    return run.replace('>', f'><w:rPr><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>', 1)

def set_para_spacing(p):
    if '<w:pPr>' in p:
        ppr = re.search(r'<w:pPr>.*?</w:pPr>', p, re.S).group(0)
        new = re.sub(r'<w:spacing [^/]*/>', '', ppr)
        new = new.replace('</w:pPr>', f'<w:spacing w:after="{REF_AFTER}" w:line="{REF_LINE}" w:lineRule="auto"/></w:pPr>')
        return p.replace(ppr, new)
    return p

def process(xml):
    sec = 'other'; stats = {'ref_paras': 0, 'names': 0, 'samples': []}
    def fix_para(m):
        nonlocal sec
        p = m.group(0); st = para_style(p); txt = para_text(p)
        if st == 'Heading3':
            # part-1 heading may read "मूल संस्कृत पाठ", "मूल पाठ", "मूल प्राकृत गाथा" … ; part-6 "सन्दर्भ एवं पाद-टिप्पणी"
            if 'मूल' in txt: sec = 'mool'
            elif 'सन्दर्भ' in txt and 'टिप्पणी' in txt: sec = 'ref'
            else: sec = 'other'
        elif st in ('Heading1', 'Heading2'):
            sec = 'other'
        is_ref_heading = (st == 'Heading3' and sec == 'ref')
        # --- honorifics (skip mool text and TOC) ---
        if sec != 'mool' and not st.startswith('TOC'):
            runs = R_RE.findall(p)
            texts = [''.join(t[1] for t in T_RE.findall(r)) for r in runs]
            newp = p
            for i, r in enumerate(runs):
                prev = texts[i-1][-40:] if i > 0 else ''
                nxt = texts[i+1][:40] if i+1 < len(runs) else ''
                def rep(t, prev=prev, nxt=nxt):
                    new = honor(t.group(2), prev, nxt)
                    if new != t.group(2):
                        stats['names'] += 1
                        if len(stats['samples']) < 8: stats['samples'].append(new.strip()[:70])
                    return t.group(1) + new + t.group(3)
                nr = T_RE.sub(rep, r)
                if nr != r: newp = newp.replace(r, nr, 1)
            p = newp
        # --- dictionary size for part 6 ---
        if sec == 'ref':
            sz = REF_HEAD_SIZE if is_ref_heading else REF_SIZE
            p = R_RE.sub(lambda r: set_run_size(r.group(0), sz), p)
            if not is_ref_heading: p = set_para_spacing(p)
            stats['ref_paras'] += 1
        return p
    return P_RE.sub(fix_para, xml), stats

def main(path, dry=False):
    z = zipfile.ZipFile(path); items = {n: z.read(n) for n in z.namelist()}; z.close()
    xml = items['word/document.xml'].decode('utf-8')
    new, stats = process(xml)
    samples = stats.pop('samples')
    print(os.path.basename(path), 'DRY-RUN' if dry else '', stats)
    for s in samples: print('   e.g.', s)
    if dry:
        return
    items['word/document.xml'] = new.encode('utf-8')
    bak = path + '.bak'; shutil.copy(path, bak)
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as out:
        for n, b in items.items(): out.writestr(n, b)
    os.remove(bak)

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--dry-run']
    for f in args: main(f, dry='--dry-run' in sys.argv)
