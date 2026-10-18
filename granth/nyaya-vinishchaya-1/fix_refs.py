# -*- coding: utf-8 -*-
import glob, io, re, os
files = sorted(glob.glob("parts/batch*.md"))
byNN = {}
TITLE = re.compile(r"^§\s*(\d+)\s*—", re.M)
for f in files:
    nn = int(re.search(r"batch(\d+)_", f).group(1))
    byNN[nn] = [int(m.group(1)) for m in TITLE.finditer(io.open(f, encoding="utf-8").read())]
pat = re.compile(r"(§+\s*(\d+)\s*[–\-—]\s*)(\d+)")
fixed = 0
for f in files:
    t = io.open(f, encoding="utf-8").read()
    def sub(m):
        global fixed
        a, b = int(m.group(2)), int(m.group(3))
        if b < a or b - a > 60:
            nn, k = divmod(b, 100)
            if nn in byNN and 1 <= k <= len(byNN[nn]):
                new = byNN[nn][k - 1]
                fixed += 1
                print(os.path.basename(f), m.group(0), "->", m.group(1) + str(new))
                return m.group(1) + str(new)
        return m.group(0)
    t2 = pat.sub(sub, t)
    if t2 != t:
        io.open(f, "w", encoding="utf-8", newline="").write(t2)
print("fixed", fixed)
