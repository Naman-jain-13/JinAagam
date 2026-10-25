# Shows exactly what is left: pass-2 addenda missing per batch line. Run: python resume_status.py
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
lines = io.open(os.path.join(here, 'pass2_batches.txt'), encoding='utf-8').read().split('\n')
have = set(f for f in os.listdir(os.path.join(here, 'addenda')))
for i, l in enumerate(lines, 1):
    ks = re.findall(r'§(\d+)', l)
    if not ks: continue
    miss = [k for k in ks if 's%s.md' % k not in have]
    print('line %2d: %s' % (i, 'DONE' if not miss else 'missing ' + ', '.join(miss)))
