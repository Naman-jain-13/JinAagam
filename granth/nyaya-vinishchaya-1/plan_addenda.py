# -*- coding: utf-8 -*-
"""addenda के कार्य-खण्ड बनाइए; और जाँचिए कि कौन-से § के addenda अभी बने हैं।

चलाइए:  python plan_addenda.py            # बाक़ी कार्य-खण्ड
        python plan_addenda.py --all      # सब कार्य-खण्ड
"""
import glob, io, re, sys, pathlib
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
HERE = pathlib.Path(__file__).resolve().parent
TITLE = re.compile(r"^§\s*(\d+)\s*—", re.M)
NAME = re.compile(r"batch(\d+)_p(\d+)-(\d+)")
files = sorted(glob.glob(str(HERE/"parts"/"batch*.md")),
               key=lambda f: int(NAME.search(pathlib.Path(f).name).group(2)))
CHUNK = 12
tasks = []
for f in files:
    nums = [int(m.group(1)) for m in TITLE.finditer(io.open(f, encoding="utf-8").read())]
    for i in range(0, len(nums), CHUNK):
        part = nums[i:i+CHUNK]
        tasks.append((pathlib.Path(f).name, part[0], part[-1], part))
done = {int(p.stem[1:]) for p in (HERE/"addenda").glob("s*.md")}
show_all = "--all" in sys.argv
left = 0
for n, (fn, a, b, part) in enumerate(tasks, 1):
    miss = [x for x in part if x not in done]
    left += len(miss)
    if show_all or miss:
        print("T%02d  %s  §%d–§%d  (%d §, बाक़ी %d)" % (n, fn, a, b, len(part), len(miss)))
print("कुल § %d; addenda बने %d; बाक़ी %d; कार्य-खण्ड %d" % (sum(len(t[3]) for t in tasks), len(done), left, len(tasks)))
