# -*- coding: utf-8 -*-
"""Witness sheet: render the extracted specimens so the shaping can be seen.

Not part of the plate. This exists so a broken extraction shows up as a blank
or mangled row instead of silently reaching the poster.
"""
import os, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
G = json.load(open(os.path.join(BASE, "out", "glyphs.json"), encoding="utf8"))["glyphs"]

# the ones most likely to break: cursive joining, reordering, stacking, RTL
WATCH = ["Arab", "Aran", "Deva", "Beng", "Taml", "Khmr", "Mymr", "Thai", "Tibt",
         "Hebr", "Syrc", "Nkoo", "Adlm", "Thaa", "Ethi", "Hani", "Hang", "Hira",
         "Egyp", "Xsux", "Linb", "Cher", "Grek", "Cyrl", "Latn", "Brai", "Sgnw",
         "Mong", "Yiii", "Cans", "Vaii", "Tfng", "Java", "Sinh", "Zsye", "Jpan"]

ROW, COL, CELL_W, CELL_H = 6, 6, 320, 130
out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
       'viewBox="0 0 %d %d"><rect width="100%%" height="100%%" fill="#fbf9f4"/>'
       % (COL * CELL_W, ROW * CELL_H + 40, COL * CELL_W, ROW * CELL_H + 40)]
out.append('<text x="12" y="26" font-family="monospace" font-size="18" fill="#111">'
           'specimen witness sheet, %d scripts extracted</text>' % len(G))

for i, code in enumerate(WATCH[:ROW * COL]):
    cx, cy = (i % COL) * CELL_W, 40 + (i // COL) * CELL_H
    out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#ddd"/>'
               % (cx, cy, CELL_W, CELL_H))
    out.append('<text x="%d" y="%d" font-family="monospace" font-size="12" fill="#c00">%s</text>'
               % (cx + 8, cy + 18, code))
    g = G.get(code)
    if not g:
        out.append('<text x="%d" y="%d" font-family="monospace" font-size="12" fill="#999">'
                   'MISSING</text>' % (cx + 8, cy + 40))
        continue
    x0, y0, x1, y1 = g["bbox"]
    w, h = max(x1 - x0, 1), max(y1 - y0, 1)
    s = min((CELL_W - 40) / w, (CELL_H - 50) / h)
    # font y grows up, SVG y grows down
    tx = cx + 20 - x0 * s
    ty = cy + 30 + (CELL_H - 50 + h * s) / 2 + y0 * s
    out.append('<g transform="translate(%.2f,%.2f) scale(%.5f,%.5f)">'
               '<path d="%s" fill="#111"/></g>' % (tx, ty, s, -s, g["d"]))
    out.append('<text x="%d" y="%d" font-family="monospace" font-size="9" fill="#777">'
               '%d glyphs</text>' % (cx + 8, cy + CELL_H - 8, g["n"]))

out.append("</svg>")
p = os.path.join(BASE, "out", "specimen_check.svg")
open(p, "w", encoding="utf8").write("".join(out))
print(p)
print("rendered %d / %d watched" % (sum(1 for c in WATCH[:ROW * COL] if c in G), ROW * COL))
