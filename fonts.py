# -*- coding: utf-8 -*-
"""Download a Noto face per script, pick specimen characters, extract outlines.

Output: out/glyphs.json
  { code: {font, chars, upem, glyphs:[{d, adv}], source} }
Paths are real font outlines converted to SVG path data. Nothing is drawn by
hand and nothing is approximated: a script either gets its own glyphs or is
recorded in `misses` with the reason.
"""
import os, re, sys, json, time, hashlib, urllib.request, urllib.parse

BASE = os.path.dirname(os.path.abspath(__file__))
DATA, FONTS, OUT = (os.path.join(BASE, d) for d in ("data", "fonts", "out"))
sys.path.insert(0, BASE)
from fonts_map import NOTO_REPO, GF_SUBSET, NO_FONT, family_for
from genealogy import SPECIMEN_OVERRIDE

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
N_SPECIMEN = 6


def fetch(url, headers=UA, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                return None
            time.sleep(2 + 3 * i)


def load_iso():
    rows = [l.rstrip("\n").split(";") for l in open(os.path.join(DATA, "iso15924.txt"), encoding="utf8")
            if l.strip() and not l.startswith("#")]
    special = {"Zinh", "Zyyy", "Zzzz", "Zmth", "Zsym", "Zxxx"}
    return [r for r in rows if r[0] not in special and not re.match(r"^Q[a-b][a-z]{2}$", r[0])]


def load_scripts_map():
    """PVA script name -> sorted list of codepoints."""
    out = {}
    for line in open(os.path.join(DATA, "Scripts.txt"), encoding="utf8"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        rng, name = [x.strip() for x in line.split(";")]
        if ".." in rng:
            a, b = rng.split("..")
        else:
            a = b = rng
        out.setdefault(name, []).extend(range(int(a, 16), int(b, 16) + 1))
    return {k: sorted(v) for k, v in out.items()}


def load_categories():
    """codepoint -> general category, from the live UCD (Python's own table is older)."""
    cat = {}
    p = os.path.join(DATA, "DerivedGeneralCategory.txt")
    for line in open(p, encoding="utf8"):
        line = line.split("#")[0].strip()
        if not line:
            continue
        rng, gc = [x.strip() for x in line.split(";")]
        if gc[0] != "L":
            continue
        a, _, b = rng.partition("..")
        for cp in range(int(a, 16), int(b or a, 16) + 1):
            cat[cp] = gc
    return cat


def get_font(code, pva, chars):
    """Return (path, source_label) for a usable font file, or (None, reason)."""
    if code in NO_FONT:
        return None, NO_FONT[code]

    if code in GF_SUBSET:
        fam = GF_SUBSET[code]
        # key the cache on the requested text: a subset fetched for different
        # specimen characters does not contain the ones asked for now
        tag = hashlib.sha1(chars.encode("utf8")).hexdigest()[:8]
        dest = os.path.join(FONTS, "%s.%s.gf.ttf" % (code, tag))
        if not os.path.exists(dest):
            css = fetch("https://fonts.googleapis.com/css2?" + urllib.parse.urlencode(
                {"family": fam, "text": chars}), headers=UA)
            if not css:
                return None, "Google Fonts subset request failed"
            # the served URL carries no file extension, only a format() hint
            m = re.search(r"url\((https://[^)]+)\)", css.decode("utf8"))
            if not m:
                return None, "no font url in Google Fonts CSS for %s" % fam
            blob = fetch(m.group(1))
            if not blob:
                return None, "font subset download failed"
            # Google serves woff2. HarfBuzz cannot open a woff2 blob: it builds
            # an empty face and every glyph silently resolves to .notdef, which
            # renders as a tofu box. Decompress to sfnt before shaping.
            from fontTools.ttLib import TTFont
            import io
            tf = TTFont(io.BytesIO(blob), fontNumber=0)
            tf.flavor = None            # save() keeps the woff2 flavor otherwise
            tf.save(dest)
        return dest, fam + " (Google Fonts subset)"

    tried = []
    for fam in family_for(code, pva):
        dest = os.path.join(FONTS, fam + ".ttf")
        if os.path.exists(dest):
            return dest, fam
        blob = fetch(NOTO_REPO.format(fam=fam), tries=1)
        if blob and len(blob) > 2000:
            open(dest, "wb").write(blob)
            return dest, fam
        tried.append(fam)
    return None, "no Noto face published (tried %s)" % ", ".join(tried or ["-"])


def specimen_chars(code, pva, scripts, cats):
    if code in SPECIMEN_OVERRIDE:
        return SPECIMEN_OVERRIDE[code]
    cps = scripts.get(pva, [])
    letters = [c for c in cps if c in cats]
    pool = letters or cps
    return "".join(chr(c) for c in pool[:N_SPECIMEN * 4])


def outlines(path, chars, want=N_SPECIMEN):
    """Shape the specimen with HarfBuzz, return one laid-out SVG path.

    Shaping is not optional. Arabic, Nastaliq, and every Brahmic script build
    their real letterforms through GSUB; drawing the base glyphs straight from
    the cmap gives disconnected stubs, and Nastaliq gives nothing at all.
    """
    import uharfbuzz as hb
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.misc.transform import Transform

    f = TTFont(path, fontNumber=0, lazy=True)
    upem = f["head"].unitsPerEm
    gs = f.getGlyphSet()
    order = f.getGlyphOrder()

    blob = hb.Blob.from_file_path(path)
    hbfont = hb.Font(hb.Face(blob))
    text = chars[:want]
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()      # picks script and direction from the text
    hb.shape(hbfont, buf)

    rec = RecordingPen()
    x = y = 0
    drawn = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        # glyph id 0 is .notdef. In most Noto faces it is a drawn box, so it
        # passes a bounds check and would reach the plate as a fake specimen.
        gn = order[info.codepoint] if 0 < info.codepoint < len(order) else None
        if gn and gn in gs:
            probe = BoundsPen(gs)
            gs[gn].draw(probe)
            if probe.bounds:
                gs[gn].draw(TransformPen(rec, Transform().translate(
                    x + pos.x_offset, y + pos.y_offset)))
                drawn += 1
        x += pos.x_advance
        y += pos.y_advance

    if not drawn:
        f.close()
        return upem, None

    svg = SVGPathPen(gs)
    rec.replay(svg)
    bp = BoundsPen(gs)
    rec.replay(bp)
    f.close()
    return upem, {"d": svg.getCommands(), "adv": x, "bbox": list(bp.bounds),
                  "n": drawn, "chars": text}


if __name__ == "__main__":
    iso = load_iso()
    scripts = load_scripts_map()
    cats = load_categories()
    result, misses = {}, {}
    for i, r in enumerate(iso):
        code, num, en, fr, pva, uv, date = r
        chars = specimen_chars(code, pva, scripts, cats)
        path, src = get_font(code, pva, chars[:N_SPECIMEN])
        if not path:
            misses[code] = src
            continue
        try:
            upem, gl = outlines(path, chars)
        except Exception as e:
            misses[code] = "font parse failed: %s" % str(e)[:60]
            continue
        if not gl:
            misses[code] = "font carries no drawable glyph for the specimen"
            continue
        gl.update({"font": src, "upem": upem})
        result[code] = gl
        print("%-5s %-2d %s" % (code, gl["n"], src), flush=True)

    json.dump({"glyphs": result, "misses": misses},
              open(os.path.join(OUT, "glyphs.json"), "w", encoding="utf8"), ensure_ascii=False)
    print("\nWITH GLYPHS: %d / %d" % (len(result), len(iso)))
    print("WITHOUT (%d):" % len(misses))
    for k, v in sorted(misses.items()):
        print("   %-5s %s" % (k, v))
