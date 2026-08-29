# -*- coding: utf-8 -*-
"""Join every source into out/dataset.json, the single input to the renderer.

Zone A: 218 script records, descent, metadata, glyph specimens.
Zone B: every Glottolog language, its family, endangerment, speakers, and the
script(s) it is written in.
"""
import os, re, sys, csv, json, collections

csv.field_size_limit(10 ** 8)
BASE = os.path.dirname(os.path.abspath(__file__))
DATA, OUT = os.path.join(BASE, "data"), os.path.join(BASE, "out")
sys.path.insert(0, BASE)
from genealogy import G

SPECIAL = {"Zinh", "Zyyy", "Zzzz", "Zmth", "Zsym", "Zxxx"}


def iso15924():
    out = {}
    for line in open(os.path.join(DATA, "iso15924.txt"), encoding="utf8"):
        if not line.strip() or line.startswith("#"):
            continue
        code, num, en, fr, pva, uv, date = line.rstrip("\n").split(";")
        if code in SPECIAL or re.match(r"^Q[a-b][a-z]{2}$", code):
            continue
        out[code] = {"code": code, "num": num, "name": en, "name_fr": fr,
                     "pva": pva, "unicode": uv, "iso_date": date}
    return out


def unicode_blocks(scripts_needed):
    """PVA -> (first codepoint, count) so the plate can state the encoding."""
    span = collections.defaultdict(lambda: [None, 0])
    for line in open(os.path.join(DATA, "Scripts.txt"), encoding="utf8"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        rng, name = [x.strip() for x in line.split(";")]
        a, _, b = rng.partition("..")
        lo, hi = int(a, 16), int(b or a, 16)
        s = span[name]
        s[0] = lo if s[0] is None else min(s[0], lo)
        s[1] += hi - lo + 1
    return {k: tuple(v) for k, v in span.items()}


def wikidata(name):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return []
    return json.load(open(p, encoding="utf8"))["results"]["bindings"]


def build_scripts():
    iso = iso15924()
    blocks = unicode_blocks(set())
    glyphs = json.load(open(os.path.join(OUT, "glyphs.json"), encoding="utf8"))

    # native names from Wikidata, keyed by ISO 15924 code
    native = {}
    for b in wikidata("wd_scripts.json"):
        c = b.get("code", {}).get("value")
        n = b.get("native", {}).get("value")
        if c and n and c not in native:
            native[c] = n

    out = {}
    for code, rec in iso.items():
        if code not in G:
            raise SystemExit("genealogy is missing %s" % code)
        parent, edge, typ, direction, start, end, status = G[code]
        lo, n = blocks.get(rec["pva"], (None, 0))
        out[code] = dict(rec,
                         parent=parent, edge=edge, type=typ, direction=direction,
                         start=start, end=end, status=status,
                         native=native.get(code),
                         block_start=lo, block_size=n,
                         encoded=bool(rec["unicode"]),
                         glyph=glyphs["glyphs"].get(code),
                         glyph_miss=glyphs["misses"].get(code))
    return out


def build_languages():
    langs, meta = {}, {}
    with open(os.path.join(DATA, "glottolog_languages.csv"), encoding="utf8", newline="") as f:
        for r in csv.DictReader(f):
            if r["Level"] != "language":
                continue
            langs[r["ID"]] = {
                "id": r["ID"], "name": r["Name"], "iso": r["ISO639P3code"],
                "macroarea": (r["Macroarea"] or "").split(";")[0],
                "family": r["Family_ID"] or r["ID"],
                "isolate": r["Is_Isolate"] == "true",
            }
    # family display names
    fam_name = {}
    with open(os.path.join(DATA, "glottolog_languages.csv"), encoding="utf8", newline="") as f:
        for r in csv.DictReader(f):
            if r["Level"] == "family":
                fam_name[r["ID"]] = r["Name"]

    # endangerment + category
    aes, cat = {}, {}
    with open(os.path.join(DATA, "glottolog_values.csv"), encoding="utf8", newline="") as f:
        for r in csv.DictReader(f):
            if r["Parameter_ID"] == "aes":
                aes[r["Language_ID"]] = (r["Code_ID"] or "").replace("aes-", "")
            elif r["Parameter_ID"] == "category":
                cat[r["Language_ID"]] = (r["Code_ID"] or "").replace("category-", "")

    by_iso = {v["iso"]: k for k, v in langs.items() if v["iso"]}

    speakers = {}
    for b in wikidata("wd_speakers.json"):
        gid = by_iso.get(b["iso"]["value"])
        if not gid:
            continue
        try:
            n = float(b["n"]["value"])
        except ValueError:
            continue
        speakers[gid] = max(speakers.get(gid, 0), n)

    valid = set(build_scripts())
    lang_scripts = collections.defaultdict(set)
    src_count = collections.Counter()
    for b in wikidata("wd_lang_script.json"):
        gid = by_iso.get(b["iso"]["value"])
        c = b.get("scCode", {}).get("value")
        if gid and c in valid:
            lang_scripts[gid].add(c)
            src_count["wikidata"] += 1

    # CLDR languageData is a second, independently maintained opinion on which
    # script a language uses. It is keyed by BCP47, so bridge 639-1 to 639-3.
    import xml.etree.ElementTree as ET
    part1 = {}
    with open(os.path.join(DATA, "iso-639-3.tab"), encoding="utf8") as f:
        rd = csv.DictReader(f, delimiter="\t")
        for r in rd:
            if r.get("Part1"):
                part1[r["Part1"]] = r["Id"]
    root = ET.parse(os.path.join(DATA, "cldr_supplemental.xml")).getroot()
    for el in root.iter("language"):
        t, sc = el.get("type"), el.get("scripts")
        if not t or not sc:
            continue
        iso3 = part1.get(t, t if len(t) == 3 else None)
        gid = by_iso.get(iso3)
        if not gid:
            continue
        for c in sc.split():
            if c in valid:
                lang_scripts[gid].add(c)
                src_count["cldr"] += 1
    print("script links: %s" % dict(src_count))

    dropped = []
    for gid, v in langs.items():
        v["aes"] = aes.get(gid, "unknown")
        v["category"] = cat.get(gid, "")
        v["speakers"] = speakers.get(gid)
        v["scripts"] = sorted(lang_scripts.get(gid, []))
        if v["category"] == "Artificial_Language":
            dropped.append(gid)
    for gid in dropped:                       # spec excludes constructed languages
        del langs[gid]
    return langs, fam_name, len(dropped)


if __name__ == "__main__":
    scripts = build_scripts()
    langs, fam_name, n_artificial = build_languages()

    fams = collections.Counter(v["family"] for v in langs.values())
    with_script = sum(1 for v in langs.values() if v["scripts"])
    stats = {
        "iso15924_total_rows": 226,
        "iso15924_special_removed": 8,
        "scripts": len(scripts),
        "scripts_with_glyph": sum(1 for s in scripts.values() if s["glyph"]),
        "scripts_without_glyph": sum(1 for s in scripts.values() if not s["glyph"]),
        "scripts_encoded": sum(1 for s in scripts.values() if s["encoded"]),
        "scripts_not_encoded": sum(1 for s in scripts.values() if not s["encoded"]),
        "origins": sorted(k for k, v in scripts.items() if v["parent"] is None),
        "languages": len(langs),
        "artificial_dropped": n_artificial,
        "families": len([f for f in fams if not langs[[g for g in langs if langs[g]['family'] == f][0]]["isolate"]]) if langs else 0,
        "isolates": sum(1 for v in langs.values() if v["isolate"]),
        "languages_with_script": with_script,
        "languages_without_script": len(langs) - with_script,
        "languages_with_speakers": sum(1 for v in langs.values() if v["speakers"]),
        "sign_languages": sum(1 for v in langs.values() if v["category"] == "Sign_Language"),
        "extinct": sum(1 for v in langs.values() if v["aes"] == "extinct"),
        "aes": dict(collections.Counter(v["aes"] for v in langs.values())),
        "macroareas": dict(collections.Counter(v["macroarea"] for v in langs.values())),
    }
    stats["families"] = len({v["family"] for v in langs.values() if not v["isolate"]})

    json.dump({"scripts": scripts, "languages": langs, "family_names": fam_name,
               "stats": stats},
              open(os.path.join(OUT, "dataset.json"), "w", encoding="utf8"), ensure_ascii=False)
    for k, v in stats.items():
        print("%-28s %s" % (k, v if not isinstance(v, list) else "%d %s" % (len(v), v)))
