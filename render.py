# -*- coding: utf-8 -*-
"""Draw the plate.

Zone A  the descent of writing: 218 scripts, 10 independent origins, real
        glyph specimens, triangular silhouette per the source sketch.
Zone B  every Glottolog language, hung under the script it is written in,
        with a separate field for those no open source records a script for.
Zone C  the catalogue: all 7 documentation fields for all 218 scripts, keyed
        by ISO 15924 code, so nothing on the plate is asserted without a row.

Layout is computed, not hand-placed. Band widths come from the tree, and the
canvas is widened until no two cards in a band collide.
"""
import os, re, sys, json, math, time, collections

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "out")
DATE = time.strftime('%Y-%m-%d', time.localtime(os.path.getmtime(
    os.path.join(BASE, 'data', 'iso15924.txt'))))
D = json.load(open(os.path.join(OUT, "dataset.json"), encoding="utf8"))
S, L, FAM, ST = D["scripts"], D["languages"], D["family_names"], D["stats"]

W = 20000
PAD = 260
TITLE_H = 620
BAND = 470                     # one depth level of the descent tree
NODE_W, NODE_H = 300, 300
GLYPH_H = 132

INK = "#1a1714"
INK_SOFT = "#6b6155"
INK_FAINT = "#a89d8d"
PAPER = "#f6f1e6"
RULE = "#c9bda9"

# one hue per independent origin, plus a neutral for what has no script
HUE = {
    "Pcun": "#8c3b2e",   # Mesopotamia
    "Egyp": "#a86a1f",   # Egypt and everything out of Proto-Sinaitic
    "Hani": "#2f5d50",   # China
    "Maya": "#6b3f7a",   # Mesoamerica
    "Inds": "#7a6a3a",   # Indus, undeciphered
    "Pelm": "#7a5a3a",   # Proto-Elamite, undeciphered
    "Roro": "#3d5f7a",   # Rongorongo, undeciphered
    "Lina": "#2f6b7a",   # Aegean
    "Hluw": "#8a5a4a",   # Anatolian
    "Nkdb": "#4a6b2f",   # Naxi Dongba
}
NONE_GREY = "#9c9488"

AES_ALPHA = {"not_endangered": 1.0, "threatened": 0.78, "shifting": 0.58,
             "moribund": 0.40, "nearly_extinct": 0.28, "extinct": 0.0,
             "unknown": 0.16}


def short_name(n):
    """Drop a trailing parenthetical, keep a leading one.

    ISO 15924 writes Seal as "(Small) Seal"; cutting at the first "(" left
    that script with an empty name in the catalogue."""
    n = re.sub(r"\s*\([^()]*\)\s*$", "", n).strip()
    return n or "unnamed"


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def yr(v):
    if v is None:
        return "present"
    return "%d BCE" % -v if v < 0 else "%d CE" % v


# ---------------------------------------------------------------- tree ------
children = collections.defaultdict(list)
for c, s in S.items():
    if s["parent"]:
        children[s["parent"]].append(c)

DESC = {}


def n_desc(c):
    if c not in DESC:
        DESC[c] = 1 + sum(n_desc(k) for k in children[c])
    return DESC[c]


for c in S:
    n_desc(c)
for p in children:
    children[p].sort(key=lambda c: (-DESC[c], c))

DEPTH = {}


def depth(c):
    if c not in DEPTH:
        p = S[c]["parent"]
        DEPTH[c] = 0 if not p else depth(p) + 1
    return DEPTH[c]


for c in S:
    depth(c)

ORIGINS = sorted((c for c in S if S[c]["parent"] is None), key=lambda c: -DESC[c])
N_NOGLYPH_UNENCODED = sum(1 for s in S.values() if not s["glyph"] and not s["encoded"])

ROOT_OF = {}


def root_of(c):
    if c not in ROOT_OF:
        p = S[c]["parent"]
        ROOT_OF[c] = c if not p else root_of(p)
    return ROOT_OF[c]


for c in S:
    root_of(c)

# in-order slot assignment: recurse into the first half of the children, take a
# slot for the node itself, then the rest. Parents end up centred over children.
SLOT = {}
_next = [0]


def assign(c):
    ch = children[c]
    half = len(ch) // 2
    for k in ch[:half]:
        assign(k)
    SLOT[c] = _next[0]
    _next[0] += 1
    for k in ch[half:]:
        assign(k)


for r in ORIGINS:
    assign(r)
NSLOT = _next[0]
assert NSLOT == len(S), "slot count %d != script count %d" % (NSLOT, len(S))


GAP = 26
BY_BAND = collections.defaultdict(list)
for c in S:
    BY_BAND[DEPTH[c]].append(c)

# A band only has to fit its own members. Sizing the canvas off the global slot
# pitch instead wastes most of the width on the sparse bands and pushes the
# plate past 70000 px, so each band is separated on its own.
W = max(W, int(max(len(v) for v in BY_BAND.values()) * (NODE_W + GAP) + 2 * PAD + NODE_W))

PITCH = NODE_W + GAP
LO, HI = PAD + NODE_W / 2, W - PAD - NODE_W / 2

# Tidy tree: leaves take sequential columns in tree order, every parent sits
# over the centre of its own children. Centring each band on the canvas
# instead gave a cleaner silhouette but severed a node's x from its parent's,
# and the descent lines came out as long horizontal sweeps you cannot trace.
# A genealogy you can follow beats a tidier outline.
LEAVES = [c for c in sorted(S, key=lambda c: SLOT[c]) if not children[c]]
LEAFPITCH = (HI - LO) / max(len(LEAVES) - 1, 1)
BASE = {c: LO + i * LEAFPITCH for i, c in enumerate(LEAVES)}


def leaf_span(c, memo={}):
    """First and last leaf column under c. A parent sits over the middle of it.

    Averaging the children's positions instead drags a node toward whichever
    small children happen to sort last: Egyptian hieroglyphs, parent of the
    whole Proto-Sinaitic world, ended up parked on the right margin next to
    its two smallest branches.
    """
    if c not in memo:
        if not children[c]:
            memo[c] = (BASE[c], BASE[c])
        else:
            spans = [leaf_span(k) for k in children[c]]
            memo[c] = (min(s[0] for s in spans), max(s[1] for s in spans))
    return memo[c]


def base_x(c):
    if c not in BASE:
        lo, hi = leaf_span(c)
        BASE[c] = (lo + hi) / 2
    return BASE[c]


for c in S:
    base_x(c)

X = {}
for d, codes in BY_BAND.items():
    codes.sort(key=lambda c: (base_x(c), SLOT[c]))
    want = [base_x(c) for c in codes]
    # minimal displacement: push right, then pull back inside the usable range
    for i in range(len(want)):
        want[i] = max(want[i], LO + i * PITCH)
        if i:
            want[i] = max(want[i], want[i - 1] + PITCH)
    for i in range(len(want) - 1, -1, -1):
        want[i] = min(want[i], HI - (len(want) - 1 - i) * PITCH)
        if i < len(want) - 1:
            want[i] = min(want[i], want[i + 1] - PITCH)
    for c, x in zip(codes, want):
        X[c] = x

WORST = min(min((b - a for a, b in zip(sorted(X[c] for c in v),
                                       sorted(X[c] for c in v)[1:])), default=1e9)
            for v in BY_BAND.values())
assert WORST >= PITCH - 1, "band collision: tightest gap %.1f < pitch %d" % (WORST, PITCH)

MAXD = max(DEPTH.values())
ZONE_A_TOP = TITLE_H
ZONE_A_H = (MAXD + 1) * BAND + 120
BASELINE_Y = ZONE_A_TOP + ZONE_A_H
ZONE_B_H = 3200
ZONE_C_TOP = BASELINE_Y + ZONE_B_H + 200


def node_xy(c):
    return X[c], ZONE_A_TOP + 90 + DEPTH[c] * BAND


# ------------------------------------------------------------- zone B -------
# languages grouped by the script they are written in
by_script = collections.defaultdict(list)
unwritten = []
for gid, v in L.items():
    if v["scripts"]:
        by_script[v["scripts"][0]].append(gid)
    else:
        unwritten.append(gid)


def mark_r(v, cell):
    """One cell size for the whole of Zone B, so marks compare across fields.

    Sizing the radius against each field's own cell made a script with one
    language draw fatter dots than a script with ninety-one, which inverts the
    only thing the mark size is supposed to say.
    """
    base = cell * 0.26
    n = v["speakers"]
    if not n:
        return base
    return base + cell * 0.20 * min(1.0, math.log10(n + 1) / 9.0) * 3.0


def mark_fill(v, colour):
    a = AES_ALPHA.get(v["aes"], 0.16)
    return colour, a


# --------------------------------------------------------------- draw -------
o = []
a = o.append
H = ZONE_C_TOP + 110 + math.ceil(len(S) / 9) * 84 + 130 + 58 + 8 * 46 + 260
a('<?xml version="1.0" encoding="UTF-8"?>')
a('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
  % (W, H, W, H))
a('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))
a('<defs><style>'
  'text{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;'
  'fill:%s;} .m{font-family:"Consolas","DejaVu Sans Mono",monospace;}'
  '</style></defs>' % INK)

# ---- title
cx = W / 2
a('<text x="%.0f" y="176" text-anchor="middle" font-size="112" letter-spacing="16">'
  'THE DESCENT OF WRITING</text>' % cx)
a('<text x="%.0f" y="256" text-anchor="middle" font-size="46" fill="%s">'
  'every script humans are known to have written, and every language beneath them</text>'
  % (cx, INK_SOFT))
a('<line x1="%d" y1="300" x2="%d" y2="300" stroke="%s" stroke-width="3"/>' % (PAD, W - PAD, RULE))
a('<text x="%.0f" y="372" text-anchor="middle" font-size="34" fill="%s" class="m">'
  '%d scripts of ISO 15924  &#183;  %d origins invented independently  &#183;  '
  '%d languages of Glottolog  &#183;  %d families  &#183;  %d isolates</text>'
  % (cx, INK_SOFT, ST["scripts"], len(ORIGINS), ST["languages"], ST["families"], ST["isolates"]))

# ---- zone A edges
for c, s in S.items():
    p = s["parent"]
    if not p:
        continue
    x1, y1 = node_xy(p)
    x2, y2 = node_xy(c)
    y1 += NODE_H / 2
    y2 -= NODE_H / 2
    col = HUE[root_of(c)]
    mid = (y1 + y2) / 2
    d = "M%.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" % (x1, y1, x1, mid, x2, mid, x2, y2)
    e = s["edge"]
    dash = {"attested": "", "contested": ' stroke-dasharray="16 14"',
            "stimulus": ' stroke-dasharray="4 18" stroke-linecap="round"',
            "variant": ' stroke-dasharray="30 10"',
            "composite": ' stroke-dasharray="2 12"'}[e]
    wdt = 3.4 if e == "attested" else 2.4
    a('<path d="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="%.2f"%s/>'
      % (d, col, wdt, 0.85 if e == "attested" else 0.6, dash))

# ---- zone A nodes
for c, s in S.items():
    x, y = node_xy(c)
    col = HUE[root_of(c)]
    is_origin = s["parent"] is None
    a('<g id="s-%s">' % c)
    if is_origin:
        a('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="10" fill="%s" opacity="0.10"/>'
          % (x - NODE_W / 2, y - NODE_H / 2, NODE_W, NODE_H, col))
        a('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="10" fill="none" stroke="%s" '
          'stroke-width="4"/>' % (x - NODE_W / 2, y - NODE_H / 2, NODE_W, NODE_H, col))
    g = s["glyph"]
    gy = y - NODE_H / 2 + 20
    if g:
        x0, y0, x1b, y1b = g["bbox"]
        gw, gh = max(x1b - x0, 1), max(y1b - y0, 1)
        sc = min((NODE_W - 44) / gw, GLYPH_H / gh)
        tx = x - (gw * sc) / 2 - x0 * sc
        ty = gy + GLYPH_H / 2 + (gh * sc) / 2 + y0 * sc
        a('<g transform="translate(%.2f,%.2f) scale(%.6f,%.6f)"><path d="%s" fill="%s"/></g>'
          % (tx, ty, sc, -sc, g["d"], INK))
    else:
        a('<rect x="%.1f" y="%.1f" width="%d" height="%d" fill="none" stroke="%s" '
          'stroke-width="2" stroke-dasharray="6 8"/>'
          % (x - 60, gy + 22, 120, 76, INK_FAINT))
        a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="19" fill="%s" class="m">'
          'no glyph</text>' % (x, gy + 68, INK_FAINT))
    ty = gy + GLYPH_H + 42
    a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="30" class="m" fill="%s">%s</text>'
      % (x, ty, col, c))
    name = short_name(s["name"])
    if len(name) > 26:
        name = name[:25] + "…"
    a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="26">%s</text>'
      % (x, ty + 34, esc(name)))
    bits = "%s &#183; %s" % (s["type"][:12], s["direction"])
    a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="20" fill="%s">%s</text>'
      % (x, ty + 62, INK_SOFT, bits))
    a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="20" fill="%s">%s &#8211; %s</text>'
      % (x, ty + 88, INK_SOFT, yr(s["start"]), yr(s["end"])))
    if s["status"] in ("undeciphered", "fictional", "constructed"):
        a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="20" fill="%s" '
          'font-style="italic">%s</text>' % (x, ty + 114, "#9c3b2e", s["status"]))
    a("</g>")

# one caption over the origin row: ten labels at this pitch just collide
_ox = [node_xy(r)[0] for r in ORIGINS]
_oy = node_xy(ORIGINS[0])[1] - NODE_H / 2
a('<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke="%s" stroke-width="2"/>'
  % (min(_ox) - NODE_W / 2, _oy - 34, max(_ox) + NODE_W / 2, _oy - 34, INK_SOFT))
a('<text x="%.0f" y="%.0f" text-anchor="middle" font-size="34" fill="%s" letter-spacing="10">'
  'INVENTED INDEPENDENTLY &#183; %d TIMES, NOT ONCE</text>'
  % (sum(_ox) / len(_ox), _oy - 54, INK_SOFT, len(ORIGINS)))

# ---- the base line of the sketch
a('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5"/>'
  % (PAD, BASELINE_Y, W - PAD, BASELINE_Y, INK))
a('<text x="%d" y="%d" font-size="34" letter-spacing="8" fill="%s">'
  'BELOW THIS LINE, THE LANGUAGES</text>' % (PAD, BASELINE_Y - 26, INK_SOFT))

# ---- zone B
# Two registers, both full width, their HEIGHTS in proportion to how many
# languages they hold. Sharing one row instead put every script field in the
# left fifth and dragged the ties across the whole plate; splitting by height
# keeps the area honest and lets each field hang under its own script.
order = sorted(by_script, key=lambda c: X[c])
total = len(L)
gapx = 22
MINW = 108                                    # a field must stay wide enough to label
n_written = total - len(unwritten)
inner = W - 2 * PAD

top = BASELINE_Y + 120
usable_h = ZONE_B_H - 560
row_a_h = usable_h * n_written / total
row_b_h = usable_h * len(unwritten) / total
row_b_top = top + row_a_h + 210

GLOBAL_CELL = math.sqrt(inner * row_a_h / max(n_written, 1))
script_pool = inner - gapx * (len(order) + 1)
raw = {c: script_pool * len(by_script[c]) / max(n_written, 1) for c in order}
short = sum(MINW - v for v in raw.values() if v < MINW)
spare = sum(v - MINW for v in raw.values() if v > MINW)
for c in raw:                                  # lend width to the slivers
    if raw[c] < MINW:
        raw[c] = MINW
    elif spare > 0:
        raw[c] -= (raw[c] - MINW) * (short / spare)


def draw_field(gids, x0, w, colour, label, sub, top, field_h, label_size=26):
    """Pack the languages to fill their box, whatever its proportions."""
    if w < 4 or not gids:
        return
    n = len(gids)
    # cells as square as the box allows, so a wide field and a narrow one read
    # at the same density instead of one sprawling and the other overflowing
    cols = max(1, min(n, round(w / GLOBAL_CELL)))
    rows = math.ceil(n / cols)
    dx, dy = w / cols, min(field_h / rows, GLOBAL_CELL * 1.35)
    unit = GLOBAL_CELL
    gids = sorted(gids, key=lambda g: (L[g]["family"], -(L[g]["speakers"] or 0)))
    for i, gid in enumerate(gids):
        v = L[gid]
        px = x0 + (i % cols) * dx + dx / 2
        py = top + (i // cols) * dy + dy / 2
        r = min(mark_r(v, unit), dy / 2 - 0.5, dx / 2 - 0.5)
        if r <= 0.3:
            continue
        col, al = mark_fill(v, colour)
        if v["aes"] == "extinct":
            a('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" '
              'stroke-width="1.4" opacity="0.6" id="l-%s"/>' % (px, py, r, col, gid))
        else:
            a('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f" id="l-%s"/>'
              % (px, py, r, col, max(al, 0.14), gid))
    if w >= label_size * 3.2:
        a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" class="m" fill="%s">%s</text>'
          % (x0 + w / 2, top + field_h + label_size + 18, label_size, colour, esc(label)))
        a('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" fill="%s">%s</text>'
          % (x0 + w / 2, top + field_h + label_size * 2 + 26, label_size - 2, INK_SOFT, esc(sub)))
    else:
        a('<text x="%.1f" y="%.1f" font-size="%d" class="m" fill="%s" '
          'transform="rotate(90 %.1f %.1f)">%s %s</text>'
          % (x0 + w / 2 + label_size * 0.36, top + field_h + 16, label_size - 4, colour,
             x0 + w / 2 + label_size * 0.36, top + field_h + 16, esc(label), esc(sub)))


x_cur = PAD
for c in order:
    w = raw[c]
    colour = HUE[root_of(c)]
    draw_field(by_script[c], x_cur, w, colour, c, "%d" % len(by_script[c]), top, row_a_h)
    sx, sy = node_xy(c)
    a('<path d="M%.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" stroke="%s" stroke-width="1.8" '
      'opacity="0.5" fill="none"/>'
      % (sx, sy + NODE_H / 2, sx, BASELINE_Y - 60, x_cur + w / 2, BASELINE_Y + 30,
         x_cur + w / 2, top - 20, colour))
    x_cur += w + gapx

a('<text x="%d" y="%.0f" font-size="34" letter-spacing="6" fill="%s">'
  'WRITTEN: %d languages a source assigns to a script, under the script that writes them</text>'
  % (PAD, top - 46, INK_SOFT, n_written))

draw_field(unwritten, PAD, inner, NONE_GREY,
           "no script recorded in any source used",
           "%d languages, %.0f%% of every language in Glottolog"
           % (len(unwritten), 100 * len(unwritten) / total),
           row_b_top, row_b_h, label_size=34)
a('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s" '
  'stroke-width="2.5" stroke-dasharray="16 12"/>'
  % (PAD - 18, row_b_top - 20, inner + 36, row_b_h + 40, NONE_GREY))
a('<text x="%d" y="%.0f" font-size="34" letter-spacing="6" fill="%s">'
  'UNRECORDED</text>' % (PAD, row_b_top - 44, NONE_GREY))

foot = row_b_top + row_b_h + 118
a('<text x="%d" y="%.0f" font-size="30" fill="%s">'
  'The two registers are the same width; their heights are in proportion to the languages they hold, '
  'and both are packed to the same density, so the areas compare directly. '
  'Mark area is speaker count on a log scale. Fading runs from safe through threatened to moribund; '
  'a hollow ring is an extinct language.</text>' % (PAD, foot, INK_SOFT))
a('<text x="%d" y="%.0f" font-size="30" fill="%s">'
  'The lower register is not proof of unwritten languages. It is what Wikidata and CLDR record no script for, '
  'and their coverage thins fast outside the major languages. The true unwritten share is lower, and unknown.</text>'
  % (PAD, foot + 44, "#9c3b2e"))

# ---- zone C, the catalogue
a('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3"/>'
  % (PAD, ZONE_C_TOP - 70, W - PAD, ZONE_C_TOP - 70, RULE))
a('<text x="%d" y="%d" font-size="46" letter-spacing="10">CATALOGUE OF SCRIPTS</text>'
  % (PAD, ZONE_C_TOP - 16))
a('<text x="%d" y="%d" font-size="26" fill="%s">'
  'All %d, alphabetical by code. Columns: code, name, type, direction, span of use, status, parent.</text>'
  % (PAD + 700, ZONE_C_TOP - 16, INK_SOFT, len(S)))

CAT_COLS = 9
rows_per = math.ceil(len(S) / CAT_COLS)
colw = (W - 2 * PAD) / CAT_COLS
rowh = 84
for i, c in enumerate(sorted(S)):
    s = S[c]
    cx0 = PAD + (i // rows_per) * colw
    cy0 = ZONE_C_TOP + 110 + (i % rows_per) * rowh
    col = HUE[root_of(c)]
    a('<text x="%.0f" y="%.0f" font-size="38" class="m" fill="%s">%s</text>' % (cx0, cy0, col, c))
    nm = short_name(s["name"])
    a('<text x="%.0f" y="%.0f" font-size="38">%s</text>' % (cx0 + 148, cy0, esc(nm[:44])))
    a('<text x="%.0f" y="%.0f" font-size="29" fill="%s">'
      '%s &#183; %s &#183; %s to %s &#183; %s%s%s</text>'
      % (cx0 + 148, cy0 + 40, INK_SOFT, s["type"], s["direction"],
         yr(s["start"]), yr(s["end"]), s["status"],
         "" if s["encoded"] else " &#183; not in Unicode",
         "" if s["glyph"] else " &#183; NO GLYPH"))

# ---- legend and the acceptance figures
LEG_Y = ZONE_C_TOP + 110 + rows_per * rowh + 130
a('<line x1="%d" y1="%.0f" x2="%d" y2="%.0f" stroke="%s" stroke-width="3"/>'
  % (PAD, LEG_Y - 66, W - PAD, LEG_Y - 66, RULE))

lx = PAD
a('<text x="%d" y="%.0f" font-size="40" letter-spacing="8">HOW TO READ IT</text>' % (lx, LEG_Y))
for i, (label, dash, note) in enumerate([
        ("attested descent", "", "direct graphical descent, uncontroversial"),
        ("contested", "16 14", "descent claimed but disputed in the literature"),
        ("stimulus diffusion", "4 18", "the idea of writing borrowed, the letters invented fresh"),
        ("variant", "30 10", "the same script in another style or tradition"),
        ("registry composite", "2 12", "an ISO code bundling several scripts, not a script")]):
    y = LEG_Y + 58 + i * 52
    a('<line x1="%d" y1="%.0f" x2="%d" y2="%.0f" stroke="%s" stroke-width="4"%s/>'
      % (lx, y - 10, lx + 190, y - 10, INK, ' stroke-dasharray="%s"' % dash if dash else ""))
    a('<text x="%d" y="%.0f" font-size="32">%s</text>' % (lx + 220, y, label))
    a('<text x="%d" y="%.0f" font-size="28" fill="%s">%s</text>' % (lx + 700, y, INK_SOFT, note))

lx2 = PAD + 2700
a('<text x="%d" y="%.0f" font-size="40" letter-spacing="8">ORIGINS AND THEIR COLOUR</text>' % (lx2, LEG_Y))
for i, r in enumerate(ORIGINS):
    y = LEG_Y + 58 + i * 52
    cxx = lx2 + (i // 5) * 1250
    yy = LEG_Y + 58 + (i % 5) * 52
    a('<rect x="%d" y="%.0f" width="46" height="30" fill="%s"/>' % (cxx, yy - 26, HUE[r]))
    a('<text x="%d" y="%.0f" font-size="32">%s</text>'
      % (cxx + 68, yy, esc(short_name(S[r]["name"])[:26])))
    a('<text x="%d" y="%.0f" font-size="28" fill="%s">%d scripts</text>'
      % (cxx + 68, yy + 34, INK_FAINT, DESC[r]))

lx3 = PAD + 6600
a('<text x="%d" y="%.0f" font-size="40" letter-spacing="8">WHAT WAS COUNTED</text>' % (lx3, LEG_Y))
checks = [
    "ISO 15924 rows loaded: %d; special and private-use removed: %d; scripts drawn: %d"
    % (ST["iso15924_total_rows"], ST["iso15924_special_removed"], ST["scripts"]),
    "Every non-special ISO 15924 code appears exactly once. Asserted in code, not by eye.",
    "Scripts with a real glyph specimen: %d. Without: %d, each named in the catalogue."
    % (ST["scripts_with_glyph"], ST["scripts_without_glyph"]),
    "Of those %d, %d are not encoded in Unicode at all, so no font for them can exist."
    % (ST["scripts_without_glyph"], N_NOGLYPH_UNENCODED),
    "Languages drawn: %d, every Glottolog languoid at level=language, minus %d constructed."
    % (ST["languages"], ST["artificial_dropped"]),
    "Families: %d. Isolates: %d. Sign languages: %d. Extinct: %d."
    % (ST["families"], ST["isolates"], ST["sign_languages"], ST["extinct"]),
    "Languages with no script recorded: %d, %.1f%% of the total."
    % (ST["languages_without_script"], 100 * ST["languages_without_script"] / ST["languages"]),
    "Deepest chain of descent: %d generations. Every script traces to an origin or is one."
    % MAXD,
]
for i, t in enumerate(checks):
    a('<text x="%d" y="%.0f" font-size="30" fill="%s">%s</text>'
      % (lx3, LEG_Y + 58 + i * 46, INK_SOFT, esc(t)))

a('<text x="%d" y="%.0f" font-size="28" fill="%s" class="m">'
  'Sources: ISO 15924 registry and Unicode Character Database (unicode.org, retrieved %s) '
  '&#183; Glottolog 5 CLDF (CC-BY-4.0) &#183; Wikidata P282 P1098 P1705 '
  '&#183; Unicode CLDR supplementalData &#183; SIL ISO 639-3 tables '
  '&#183; specimens rendered from Noto (SIL OFL), shaped with HarfBuzz.</text>'
  % (PAD, LEG_Y + 58 + 8 * 46 + 60, INK_FAINT, DATE))
a('<text x="%d" y="%.0f" font-size="28" fill="%s" class="m">'
  'Descent is curated against standard palaeography, not scraped: Wikidata P144 covers barely half the '
  'registry and contradicts itself on the Semitic chain. Contested links are drawn as contested.</text>'
  % (PAD, LEG_Y + 58 + 8 * 46 + 100, INK_FAINT))

a("</svg>")

path = os.path.join(OUT, "descent_of_writing.svg")
open(path, "w", encoding="utf8").write("\n".join(o))
print("canvas %d x %d  (%.1f:1)" % (W, H, W / H))
print("tightest gap in a band: %.0f px, card %d px" % (WORST, NODE_W))
print("%s  %.1f MB" % (path, os.path.getsize(path) / 1e6))
