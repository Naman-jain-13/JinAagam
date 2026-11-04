# -*- coding: utf-8 -*-
"""मूलाचार पूर्वार्ध (अधिकार 1–7) — joins the per-अधिकार folders into this one book folder.
Re-runnable: wipes parts/ and addenda/ here and copies fresh from each chapter folder. § keys are गाथा×10 across the
whole ग्रन्थ, so no collisions. groups.json = each chapter's own banners, with the chapter title prefixed on its first one.
Run: python join.py   (then node build_docx.js . → postprocess_docx.py → finalize_big.py)"""
import os, io, json, glob, shutil, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
G = os.path.dirname(HERE)
CH = [  # folder, chapter banner (first key gets it)
('adhikar-1','[ प्रथमोऽधिकारः ]  [ मूलगुणाधिकार (गाथा 1–36) ]'),
 ('adhikar-2', '[ द्वितीयोऽधिकारः ]  [ बृहत्प्रत्याख्यान-संस्तरस्तवाधिकार (गाथा 37–107) ]'),
 ('adhikar-3', '[ तृतीयोऽधिकारः ]  [ संक्षेपप्रत्याख्यानाधिकार (गाथा 108–121) ]'),
 ('adhikar-4', '[ चतुर्थोऽधिकारः ]  [ समाचाराधिकार (गाथा 122–197) ]'),
 ('adhikar-5', '[ पञ्चमोऽधिकारः ]  [ पञ्चाचाराधिकार (गाथा 198–419) ]'),
 ('adhikar-6', '[ षष्ठोऽधिकारः ]  [ पिण्डशुद्ध्यधिकार ]'),
 ('adhikar-7', '[ सप्तमोऽधिकारः ]  [ षडावश्यकाधिकार ]'),
]
for sub in ('parts', 'addenda'):
    d = os.path.join(HERE, sub); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
groups = {}; report = []
for n, (folder, banner) in enumerate(CH, 1):
    src = os.path.join(G, folder)
    if not os.path.isdir(src): report.append('अधिकार %d: folder %s missing — skipped' % (n, folder)); continue
    pf = sorted(glob.glob(os.path.join(src, 'parts', '*.md')))
    for f in pf: shutil.copy(f, os.path.join(HERE, 'parts', 'a%d_%s' % (n, os.path.basename(f))))
    af = glob.glob(os.path.join(src, 'addenda', 's*.md'))
    for f in af: shutil.copy(f, os.path.join(HERE, 'addenda', os.path.basename(f)))
    g = {}
    gp = os.path.join(src, 'groups.json')
    if os.path.exists(gp): g = json.load(io.open(gp, encoding='utf-8'))
    keys = sorted(int(k) for k in g) if g else []
    # first § key of this chapter
    import re
    first = min(int(k) for f in pf for k in re.findall(r'^§\s*(\d+)\s*—', io.open(f, encoding='utf-8').read(), re.M)) if pf else None
    if first is not None:
        if keys and keys[0] == first: g[str(first)] = banner + '  ' + g[str(first)]
        else: g[str(first)] = banner
    groups.update(g)
    report.append('अधिकार %d: %d parts files, %d addenda, %d banners' % (n, len(pf), len(af), len(g)))
io.open(os.path.join(HERE, 'groups.json'), 'w', encoding='utf-8').write(json.dumps(dict(sorted(groups.items(), key=lambda x: int(x[0]))), ensure_ascii=False, indent=1))
print('\n'.join(report))
