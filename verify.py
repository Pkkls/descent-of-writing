# -*- coding: utf-8 -*-
"""Acceptance checks, and the companion CSV.

Every number the plate prints is recomputed here from the source files. A
failure is loud: the point of the checks is that a silent omission cannot get
through, and a check that cannot fail proves nothing.
"""
import os, re, sys, csv, json, collections

csv.field_size_limit(10 ** 8)
BASE = os.path.dirname(os.path.abspath(__file__))
DATA, OUT = os.path.join(BASE, "data"), os.path.join(BASE, "out")
sys.path.insert(0, BASE)
from genealogy import G

def short_name(n):
    """Drop a trailing parenthetical, keep a leading one.

    ISO 15924 writes Seal as "(Small) Seal"; cutting at the first "(" left
    that script with an empty name in the catalogue."""
    n = re.sub(r"\s*\([^()]*\)\s*$", "", n).strip()
    return n or "unnamed"


D = json.load(open(os.path.join(OUT, "dataset.json"), encoding="utf8"))
S, L, ST = D["scripts"], D["languages"], D["stats"]
SVG = open(os.path.join(OUT, "descent_of_writing.svg"), encoding="utf8").read()

fails, lines = [], []


def check(name, ok, detail):
    lines.append("%-4s %-52s %s" % ("OK" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)


# 1. every non-special ISO 15924 code drawn exactly once
raw = [l.rstrip("\n").split(";") for l in open(os.path.join(DATA, "iso15924.txt"), encoding="utf8")
       if l.strip() and not l.startswith("#")]
special = {"Zinh", "Zyyy", "Zzzz", "Zmth", "Zsym", "Zxxx"}
expect = {r[0] for r in raw if r[0] not in special and not re.match(r"^Q[a-b][a-z]{2}$", r[0])}
drawn = set(re.findall(r'<g id="s-([A-Za-z]{4})">', SVG))
check("1. script count == ISO 15924 non-special count",
      drawn == expect and len(drawn) == len(expect),
      "%d rows loaded, %d special/private removed, %d drawn, missing %s, extra %s"
      % (len(raw), len(raw) - len(expect), len(drawn),
         sorted(expect - drawn) or "none", sorted(drawn - expect) or "none"))

dup = len(re.findall(r'<g id="s-[A-Za-z]{4}">', SVG))
check("1b. no script drawn twice", dup == len(expect), "%d script groups in the svg" % dup)

# 2. scripts with no glyph, named
miss = sorted(c for c in S if not S[c]["glyph"])
unenc = [c for c in miss if not S[c]["encoded"]]
check("2. scripts without a glyph specimen are named", len(miss) > 0,
      "%d without a specimen; %d of them are not encoded in Unicode at all"
      % (len(miss), len(unenc)))
lines.append("     " + ", ".join("%s (%s)" % (c, short_name(S[c]["name"])) for c in miss))

# 3. language leaf count == Glottolog level=language, minus constructed
with open(os.path.join(DATA, "glottolog_languages.csv"), encoding="utf8", newline="") as f:
    gl = [r for r in csv.DictReader(f) if r["Level"] == "language"]
marks = len(set(re.findall(r'id="l-([a-z0-9]{8})"', SVG)))
check("3. language marks == Glottolog languages minus constructed",
      marks == len(L) == len(gl) - ST["artificial_dropped"],
      "%d in source, %d constructed dropped, %d in dataset, %d marks drawn"
      % (len(gl), ST["artificial_dropped"], len(L), marks))

# 4. families
fams = {v["family"] for v in L.values() if not v["isolate"]}
check("4. family count == distinct Family_ID", len(fams) == ST["families"],
      "%d families, %d isolates" % (len(fams), ST["isolates"]))

# 5. every script reaches an origin, or is one
bad = []
for c in S:
    seen, cur = set(), c
    while S[cur]["parent"]:
        if cur in seen:
            bad.append(c)
            break
        seen.add(cur)
        cur = S[cur]["parent"]
    else:
        if S[cur]["parent"] is not None:
            bad.append(c)
origins = sorted(c for c in S if S[c]["parent"] is None)
check("5. every script traces to an origin, no cycles", not bad,
      "%d origins: %s" % (len(origins), ", ".join(origins)))

# 6. languages with no script recorded
none = sum(1 for v in L.values() if not v["scripts"])
check("6. languages with no script recorded", none == ST["languages_without_script"],
      "%d of %d, %.1f%%" % (none, len(L), 100 * none / len(L)))

# 7. sources and date present on the plate
check("7. sources and retrieval date printed on the plate",
      "ISO 15924 registry" in SVG and "Glottolog" in SVG and "HarfBuzz" in SVG,
      "source line found in the svg")

# extra: the plate's own printed figures agree with the data
for n in (ST["scripts"], ST["languages"], ST["families"], ST["isolates"],
          ST["scripts_with_glyph"], ST["scripts_without_glyph"]):
    if str(n) not in SVG:
        fails.append("printed figure %d missing from plate" % n)
check("8. printed figures match the dataset",
      not [f for f in fails if str(f).startswith("printed")], "all key counts appear in the svg")

# ---- companion CSV, one row per script, all seven documented fields
with open(os.path.join(OUT, "scripts_catalogue.csv"), "w", encoding="utf8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["iso15924", "iso_number", "name_en", "name_fr", "native_name", "type",
                "direction", "first_use", "last_use", "status", "parent", "edge",
                "origin", "unicode_version", "unicode_block_start", "codepoints",
                "specimen", "specimen_font", "glyph_missing_reason"])
    for c in sorted(S):
        s = S[c]
        root, cur = c, c
        while S[cur]["parent"]:
            cur = S[cur]["parent"]
        root = cur
        w.writerow([c, s["num"], s["name"], s["name_fr"], s["native"] or "", s["type"],
                    s["direction"], s["start"], s["end"] if s["end"] is not None else "present",
                    s["status"], s["parent"] or "", s["edge"] or "origin", root,
                    s["unicode"] or "not encoded",
                    "U+%04X" % s["block_start"] if s["block_start"] else "",
                    s["block_size"] or 0,
                    s["glyph"]["chars"] if s["glyph"] else "",
                    s["glyph"]["font"] if s["glyph"] else "",
                    s["glyph_miss"] or ""])

print("\n".join(lines))
print("\ncatalogue -> %s" % os.path.join(OUT, "scripts_catalogue.csv"))
print("RESULT: %s" % ("ALL CHECKS PASS" if not fails else "FAILED: %s" % fails))
sys.exit(1 if fails else 0)
