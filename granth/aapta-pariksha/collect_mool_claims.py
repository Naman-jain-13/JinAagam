# anuvad_bhed/aNN.md के "## मूल-पाठ सूचना" खण्डों से दावे एकत्र करता है।
# आउटपुट: anuvad_bhed/mool_claims_full.md (दावे सहित — केवल निर्णय हेतु)
#         anuvad_bhed/mool_claims_blind.md (बिना दावा — स्वतन्त्र छवि-सत्यापन हेतु)
import glob, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
full, blind, n = [], [], 0
for f in sorted(glob.glob(os.path.join(HERE, 'anuvad_bhed', 'a[0-9][0-9].md'))):
    parts = io.open(f, encoding='utf-8').read().split('## मूल-पाठ सूचना')
    if len(parts) < 2: continue
    for line in parts[1].splitlines():
        if not line.startswith('- §'): continue
        n += 1
        m_sec = re.match(r'- §\s*(\d+)', line)
        m_pg = re.search(r'मु॰\s*पृ॰\s*([\d–-]+)', line)
        m_ln = re.search(r'पंक्ति\s*([^·]+)', line)
        m_our = re.search(r'हमारा:\s*`([^`]+)`', line)
        cid = 'C%03d' % n
        full.append('%s | %s | %s' % (cid, os.path.basename(f), line[2:].strip()))
        blind.append('- %s · § %s · मुद्रित पृष्ठ %s (छवि `img\\p%03d.png`)%s · हमारा पाठ: `%s`' % (
            cid, m_sec.group(1) if m_sec else '?', m_pg.group(1) if m_pg else '?',
            int(re.split(r'[–-]', m_pg.group(1))[0]) + 113 if m_pg else 0,
            (' · पंक्ति ' + m_ln.group(1).strip()) if m_ln else '',
            m_our.group(1) if m_our else '?'))
io.open(os.path.join(HERE, 'anuvad_bhed', 'mool_claims_full.md'), 'w', encoding='utf-8').write('\n'.join(full) + '\n')
io.open(os.path.join(HERE, 'anuvad_bhed', 'mool_claims_blind.md'), 'w', encoding='utf-8').write('\n'.join(blind) + '\n')
print('claims', n)
