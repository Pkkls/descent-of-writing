# -*- coding: utf-8 -*-
"""Curated descent of every ISO 15924 script.

Wikidata P144 covers barely half the registry and disagrees with itself on the
Semitic chain, so descent is curated here against standard palaeographic
scholarship (Daniels & Bright, The World's Writing Systems; Coulmas, Blackwell
Encyclopedia of Writing Systems; Unicode script proposals for the recent codes).

Row = code: (parent, edge, type, direction, start, end, status)
  parent    ISO 15924 code, or None for an origin node
  edge      attested | contested | stimulus | variant | composite
              attested  = direct graphical descent, uncontroversial
              contested = descent claimed but disputed in the literature
              stimulus  = idea-of-writing borrowed, glyphs invented fresh
              variant   = same script, different style/orthographic tradition
              composite = registry code bundling several scripts, not a script
  type      logographic | syllabary | abjad | alphabet | abugida | featural
            | semasiographic | undeciphered | composite | variant | symbols
  direction ltr | rtl | ttb | boustrophedon | varies
  start     first attestation, year (negative = BCE)
  end       last use, year, or None if still in current use
  status    living | historical | revived | undeciphered | constructed | fictional
"""

G = {}

# ---------------------------------------------------------------- ORIGINS ----
# The independent inventions of writing. No parent by definition.
G["Pcun"] = (None, None, "logographic", "varies", -3300, -2900, "historical")
G["Egyp"] = (None, None, "logographic", "varies", -3250, 400, "historical")
G["Hani"] = (None, None, "logographic", "varies", -1250, None, "living")
G["Maya"] = (None, None, "logographic", "ltr", -300, 1600, "historical")
G["Inds"] = (None, None, "undeciphered", "rtl", -2600, -1900, "undeciphered")
G["Pelm"] = (None, None, "undeciphered", "rtl", -3200, -2900, "undeciphered")
G["Roro"] = (None, None, "undeciphered", "boustrophedon", 1700, 1864, "undeciphered")
G["Lina"] = (None, None, "undeciphered", "ltr", -1800, -1450, "undeciphered")
G["Hluw"] = (None, None, "logographic", "boustrophedon", -1400, -700, "historical")
G["Nkdb"] = (None, None, "semasiographic", "ltr", 1200, None, "living")

# ------------------------------------------------------------- MESOPOTAMIA ---
G["Xsux"] = ("Pcun", "attested", "logographic", "ltr", -2900, 75, "historical")
G["Ugar"] = ("Xsux", "stimulus", "abjad", "ltr", -1400, -1190, "historical")
G["Xpeo"] = ("Xsux", "stimulus", "syllabary", "ltr", -525, -330, "historical")

# ------------------------------------------------------------------ EGYPT ----
G["Egyh"] = ("Egyp", "attested", "logographic", "rtl", -3200, 300, "historical")
G["Egyd"] = ("Egyh", "attested", "logographic", "rtl", -650, 500, "historical")
G["Mero"] = ("Egyp", "attested", "abugida", "rtl", -300, 400, "historical")
G["Merc"] = ("Egyd", "attested", "abugida", "rtl", -300, 400, "historical")
G["Psin"] = ("Egyp", "attested", "abjad", "varies", -1900, -1400, "historical")

# -------------------------------------------------- PROTO-SINAITIC / SEMITIC --
G["Phnx"] = ("Psin", "attested", "abjad", "rtl", -1050, 100, "historical")
G["Samr"] = ("Phnx", "attested", "abjad", "rtl", -600, None, "living")
G["Sarb"] = ("Psin", "attested", "abjad", "boustrophedon", -900, 600, "historical")
G["Narb"] = ("Psin", "attested", "abjad", "varies", -800, 400, "historical")
G["Ethi"] = ("Sarb", "attested", "abugida", "ltr", -100, None, "living")
G["Tfng"] = ("Sarb", "contested", "abjad", "varies", -300, None, "living")

# ----------------------------------------------------------------- ARAMAIC ---
G["Armi"] = ("Phnx", "attested", "abjad", "rtl", -900, -100, "historical")
G["Hebr"] = ("Armi", "attested", "abjad", "rtl", -300, None, "living")
G["Nbat"] = ("Armi", "attested", "abjad", "rtl", -200, 400, "historical")
G["Palm"] = ("Armi", "attested", "abjad", "rtl", -100, 300, "historical")
G["Hatr"] = ("Armi", "attested", "abjad", "rtl", -100, 300, "historical")
G["Syrc"] = ("Armi", "attested", "abjad", "rtl", 100, None, "living")
G["Syre"] = ("Syrc", "variant", "variant", "rtl", 100, None, "living")
G["Syrj"] = ("Syrc", "variant", "variant", "rtl", 400, None, "living")
G["Syrn"] = ("Syrc", "variant", "variant", "rtl", 400, None, "living")
G["Mand"] = ("Armi", "attested", "abjad", "rtl", 200, None, "living")
G["Mani"] = ("Palm", "attested", "abjad", "rtl", 250, 1000, "historical")
G["Elym"] = ("Armi", "attested", "abjad", "rtl", -100, 300, "historical")
G["Chrs"] = ("Armi", "attested", "abjad", "rtl", -100, 800, "historical")
G["Prti"] = ("Armi", "attested", "abjad", "rtl", -250, 250, "historical")
G["Phli"] = ("Armi", "attested", "abjad", "rtl", -100, 900, "historical")
G["Phlp"] = ("Phli", "attested", "abjad", "rtl", 600, 800, "historical")
G["Phlv"] = ("Phli", "attested", "abjad", "rtl", 400, 1100, "historical")
G["Avst"] = ("Phlv", "attested", "alphabet", "rtl", 400, 1000, "historical")
G["Sogo"] = ("Armi", "attested", "abjad", "rtl", -100, 400, "historical")
G["Sogd"] = ("Sogo", "attested", "abjad", "varies", 400, 1000, "historical")
G["Ougr"] = ("Sogd", "attested", "abjad", "ttb", 800, 1800, "historical")
G["Mong"] = ("Ougr", "attested", "abjad", "ttb", 1204, None, "living")
G["Orkh"] = ("Sogd", "contested", "alphabet", "rtl", 700, 1000, "historical")
G["Hung"] = ("Orkh", "contested", "alphabet", "rtl", 900, None, "revived")

# ------------------------------------------------------------------ ARABIC ---
G["Arab"] = ("Nbat", "attested", "abjad", "rtl", 400, None, "living")
G["Aran"] = ("Arab", "variant", "variant", "rtl", 1400, None, "living")
G["Thaa"] = ("Arab", "attested", "abugida", "rtl", 1700, None, "living")
G["Rohg"] = ("Arab", "attested", "alphabet", "rtl", 1983, None, "living")
G["Adlm"] = ("Arab", "stimulus", "alphabet", "rtl", 1989, None, "living")
G["Nkoo"] = ("Arab", "stimulus", "alphabet", "rtl", 1949, None, "living")
G["Yezi"] = ("Syrc", "attested", "alphabet", "rtl", 1400, None, "living")
G["Berf"] = ("Arab", "stimulus", "alphabet", "rtl", 1980, None, "living")

# ------------------------------------------------------------------- GREEK ---
G["Grek"] = ("Phnx", "attested", "alphabet", "ltr", -800, None, "living")
G["Cari"] = ("Grek", "contested", "alphabet", "varies", -700, -300, "historical")
G["Lyci"] = ("Grek", "attested", "alphabet", "ltr", -500, -300, "historical")
G["Lydi"] = ("Grek", "attested", "alphabet", "rtl", -700, -300, "historical")
G["Sidt"] = ("Grek", "attested", "alphabet", "ltr", -500, -300, "historical")
G["Copt"] = ("Grek", "attested", "alphabet", "ltr", 200, None, "living")
G["Goth"] = ("Grek", "attested", "alphabet", "ltr", 350, 900, "historical")
G["Armn"] = ("Grek", "contested", "alphabet", "ltr", 405, None, "living")
G["Aghb"] = ("Armn", "contested", "alphabet", "ltr", 400, 1000, "historical")
G["Geok"] = ("Grek", "contested", "alphabet", "ltr", 430, 1100, "historical")
G["Geor"] = ("Geok", "attested", "alphabet", "ltr", 1000, None, "living")
G["Glag"] = ("Grek", "attested", "alphabet", "ltr", 863, 1900, "historical")
G["Cyrl"] = ("Grek", "attested", "alphabet", "ltr", 900, None, "living")
G["Cyrs"] = ("Cyrl", "variant", "variant", "ltr", 900, None, "living")
G["Perm"] = ("Cyrl", "attested", "alphabet", "ltr", 1372, 1700, "historical")
G["Ital"] = ("Grek", "attested", "alphabet", "varies", -700, -100, "historical")
G["Runr"] = ("Ital", "attested", "alphabet", "boustrophedon", 150, 1500, "historical")

# ------------------------------------------------------------------- LATIN ---
G["Latn"] = ("Ital", "attested", "alphabet", "ltr", -700, None, "living")
G["Latf"] = ("Latn", "variant", "variant", "ltr", 1150, None, "living")
G["Latg"] = ("Latn", "variant", "variant", "ltr", 700, None, "living")
G["Ogam"] = ("Latn", "stimulus", "alphabet", "varies", 350, 600, "historical")
G["Moon"] = ("Latn", "attested", "alphabet", "boustrophedon", 1845, None, "living")
G["Brai"] = ("Latn", "stimulus", "alphabet", "ltr", 1824, None, "living")
G["Dupl"] = ("Latn", "attested", "alphabet", "ltr", 1860, None, "living")
G["Visp"] = ("Latn", "stimulus", "featural", "ltr", 1867, 1900, "historical")
G["Shaw"] = ("Latn", "stimulus", "alphabet", "ltr", 1960, None, "constructed")
G["Dsrt"] = ("Latn", "stimulus", "alphabet", "ltr", 1854, 1877, "constructed")
G["Osge"] = ("Latn", "attested", "alphabet", "ltr", 2006, None, "living")
G["Cher"] = ("Latn", "stimulus", "syllabary", "ltr", 1821, None, "living")
G["Vaii"] = ("Latn", "stimulus", "syllabary", "ltr", 1833, None, "living")
G["Bass"] = ("Latn", "stimulus", "alphabet", "ltr", 1907, None, "living")
G["Mend"] = ("Vaii", "stimulus", "syllabary", "rtl", 1917, None, "living")
G["Kpel"] = ("Vaii", "stimulus", "syllabary", "ltr", 1935, None, "living")
G["Loma"] = ("Vaii", "stimulus", "syllabary", "ltr", 1930, None, "living")
G["Bamu"] = ("Latn", "stimulus", "syllabary", "ltr", 1896, None, "living")
G["Medf"] = ("Latn", "stimulus", "alphabet", "ltr", 1930, None, "living")
G["Gara"] = ("Latn", "stimulus", "alphabet", "rtl", 1961, None, "living")
G["Afak"] = ("Latn", "stimulus", "syllabary", "ltr", 1910, None, "historical")
G["Wole"] = ("Latn", "stimulus", "syllabary", "ltr", 1900, 1950, "historical")
G["Osma"] = ("Latn", "stimulus", "alphabet", "ltr", 1922, None, "living")
G["Olck"] = ("Latn", "stimulus", "alphabet", "ltr", 1925, None, "living")
G["Lisu"] = ("Latn", "attested", "alphabet", "ltr", 1915, None, "living")
G["Plrd"] = ("Latn", "stimulus", "abugida", "ltr", 1904, None, "living")
G["Cans"] = ("Latn", "stimulus", "abugida", "ltr", 1840, None, "living")
G["Hmng"] = ("Latn", "stimulus", "alphabet", "ltr", 1959, None, "living")
G["Hmnp"] = ("Latn", "stimulus", "alphabet", "ltr", 1980, None, "living")
G["Wara"] = ("Latn", "stimulus", "alphabet", "ltr", 1950, None, "living")
G["Mroo"] = ("Latn", "stimulus", "alphabet", "ltr", 1980, None, "living")
G["Toto"] = ("Latn", "stimulus", "abugida", "ltr", 1936, None, "living")
G["Tnsa"] = ("Latn", "stimulus", "alphabet", "ltr", 1990, None, "living")
G["Wcho"] = ("Latn", "stimulus", "alphabet", "ltr", 2001, None, "living")
G["Nagm"] = ("Latn", "stimulus", "alphabet", "ltr", 1949, None, "living")
G["Onao"] = ("Latn", "stimulus", "alphabet", "ltr", 1981, None, "living")
G["Gukh"] = ("Latn", "stimulus", "abugida", "ltr", 1980, None, "living")
G["Krai"] = ("Latn", "stimulus", "abugida", "ltr", 1990, None, "living")
G["Sunu"] = ("Latn", "stimulus", "abugida", "ltr", 1942, None, "living")
G["Tols"] = ("Latn", "stimulus", "alphabet", "ltr", 1980, None, "living")
G["Chis"] = ("Latn", "stimulus", "alphabet", "ltr", 1990, None, "living")
G["Leke"] = ("Mymr", "attested", "abugida", "ltr", 1830, None, "living")
G["Tayo"] = ("Lana", "attested", "abugida", "ltr", 1500, None, "historical")
G["Elba"] = ("Grek", "stimulus", "alphabet", "ltr", 1761, 1800, "historical")
G["Vith"] = ("Grek", "stimulus", "alphabet", "ltr", 1844, 1900, "historical")
G["Todr"] = ("Grek", "stimulus", "alphabet", "ltr", 1700, 1900, "historical")
G["Sgnw"] = ("Latn", "stimulus", "featural", "ttb", 1974, None, "living")
G["Blis"] = ("Hani", "stimulus", "semasiographic", "ltr", 1949, None, "living")

# ------------------------------------------------------------------ AEGEAN ---
G["Linb"] = ("Lina", "attested", "syllabary", "ltr", -1450, -1200, "historical")
G["Cpmn"] = ("Lina", "attested", "undeciphered", "ltr", -1550, -1050, "undeciphered")
G["Cprt"] = ("Cpmn", "attested", "syllabary", "rtl", -1100, -300, "historical")

# ------------------------------------------------------- BRAHMIC: NORTHERN ---
G["Brah"] = ("Armi", "contested", "abugida", "ltr", -300, 500, "historical")
G["Khar"] = ("Armi", "attested", "abugida", "rtl", -400, 300, "historical")
G["Sidd"] = ("Brah", "attested", "abugida", "ltr", 550, 1200, "historical")
G["Deva"] = ("Sidd", "attested", "abugida", "ltr", 700, None, "living")
G["Shrd"] = ("Brah", "attested", "abugida", "ltr", 800, 1900, "historical")
G["Takr"] = ("Shrd", "attested", "abugida", "ltr", 1500, None, "historical")
G["Dogr"] = ("Takr", "attested", "abugida", "ltr", 1860, None, "historical")
G["Guru"] = ("Shrd", "attested", "abugida", "ltr", 1539, None, "living")
G["Khoj"] = ("Shrd", "attested", "abugida", "ltr", 1500, None, "historical")
G["Mult"] = ("Shrd", "attested", "abugida", "ltr", 1750, 1950, "historical")
G["Sind"] = ("Shrd", "attested", "abugida", "ltr", 1550, None, "historical")
G["Mahj"] = ("Deva", "attested", "abugida", "ltr", 1600, 1950, "historical")
G["Kthi"] = ("Deva", "attested", "abugida", "ltr", 1550, 1950, "historical")
G["Modi"] = ("Deva", "attested", "abugida", "ltr", 1200, None, "historical")
G["Nand"] = ("Deva", "attested", "abugida", "ltr", 1100, 1800, "historical")
G["Gujr"] = ("Deva", "attested", "abugida", "ltr", 1592, None, "living")
G["Sylo"] = ("Kthi", "attested", "abugida", "ltr", 1500, None, "living")
G["Gong"] = ("Deva", "stimulus", "abugida", "ltr", 1750, None, "living")
G["Gonm"] = ("Deva", "stimulus", "abugida", "ltr", 1918, None, "living")
G["Beng"] = ("Sidd", "attested", "abugida", "ltr", 1000, None, "living")
G["Tirh"] = ("Beng", "attested", "abugida", "ltr", 1100, None, "historical")
G["Orya"] = ("Sidd", "attested", "abugida", "ltr", 1050, None, "living")
G["Newa"] = ("Sidd", "attested", "abugida", "ltr", 1100, None, "living")
G["Ranj"] = ("Sidd", "attested", "abugida", "ltr", 1100, None, "living")
G["Bhks"] = ("Brah", "attested", "abugida", "ltr", 1000, 1200, "historical")
G["Mtei"] = ("Brah", "contested", "abugida", "ltr", 1100, None, "living")
G["Cakm"] = ("Mymr", "attested", "abugida", "ltr", 1700, None, "living")
G["Sora"] = ("Latn", "stimulus", "alphabet", "ltr", 1936, None, "living")

# ------------------------------------------------------- BRAHMIC: TIBETAN ----
G["Tibt"] = ("Brah", "attested", "abugida", "ltr", 650, None, "living")
G["Marc"] = ("Tibt", "attested", "abugida", "ltr", 1000, None, "historical")
G["Phag"] = ("Tibt", "attested", "abugida", "ttb", 1269, 1400, "historical")
G["Lepc"] = ("Tibt", "attested", "abugida", "ltr", 1700, None, "living")
G["Limb"] = ("Lepc", "attested", "abugida", "ltr", 1700, None, "living")
G["Zanb"] = ("Tibt", "attested", "abugida", "ltr", 1686, 1800, "historical")
G["Soyo"] = ("Ranj", "attested", "abugida", "ltr", 1686, 1800, "historical")

# ------------------------------------------------------- BRAHMIC: SOUTHERN ---
G["Gran"] = ("Brah", "attested", "abugida", "ltr", 500, None, "living")
G["Taml"] = ("Gran", "attested", "abugida", "ltr", 700, None, "living")
G["Mlym"] = ("Gran", "attested", "abugida", "ltr", 830, None, "living")
G["Tutg"] = ("Gran", "attested", "abugida", "ltr", 1000, None, "historical")
G["Saur"] = ("Gran", "attested", "abugida", "ltr", 1880, None, "living")
G["Sinh"] = ("Brah", "attested", "abugida", "ltr", -200, None, "living")
G["Diak"] = ("Sinh", "attested", "abugida", "ltr", 800, 1700, "historical")
G["Knda"] = ("Brah", "attested", "abugida", "ltr", 500, None, "living")
G["Telu"] = ("Brah", "attested", "abugida", "ltr", 600, None, "living")

# --------------------------------------------------- BRAHMIC: SOUTHEAST ASIA -
G["Khmr"] = ("Gran", "attested", "abugida", "ltr", 611, None, "living")
G["Thai"] = ("Khmr", "attested", "abugida", "ltr", 1283, None, "living")
G["Laoo"] = ("Khmr", "attested", "abugida", "ltr", 1350, None, "living")
G["Mymr"] = ("Gran", "attested", "abugida", "ltr", 1000, None, "living")
G["Lana"] = ("Mymr", "attested", "abugida", "ltr", 1300, None, "living")
G["Tavt"] = ("Lana", "attested", "abugida", "ltr", 1500, None, "living")
G["Talu"] = ("Lana", "attested", "abugida", "ltr", 1200, None, "living")
G["Tale"] = ("Mymr", "attested", "abugida", "ltr", 1300, None, "living")
G["Ahom"] = ("Mymr", "attested", "abugida", "ltr", 1300, 1800, "revived")
G["Kali"] = ("Mymr", "attested", "abugida", "ltr", 1962, None, "living")
G["Cham"] = ("Gran", "attested", "abugida", "ltr", 400, None, "living")
G["Kawi"] = ("Gran", "attested", "abugida", "ltr", 750, 1500, "historical")
G["Java"] = ("Kawi", "attested", "abugida", "ltr", 1500, None, "living")
G["Bali"] = ("Kawi", "attested", "abugida", "ltr", 1000, None, "living")
G["Sund"] = ("Kawi", "attested", "abugida", "ltr", 1400, None, "living")
G["Rjng"] = ("Kawi", "attested", "abugida", "ltr", 1700, None, "living")
G["Batk"] = ("Kawi", "attested", "abugida", "ltr", 1300, None, "living")
G["Bugi"] = ("Kawi", "attested", "abugida", "ltr", 1600, None, "living")
G["Maka"] = ("Bugi", "attested", "abugida", "ltr", 1600, 1900, "historical")
G["Tglg"] = ("Kawi", "attested", "abugida", "ltr", 1300, None, "revived")
G["Hano"] = ("Tglg", "attested", "abugida", "ltr", 1300, None, "living")
G["Buhd"] = ("Tglg", "attested", "abugida", "ltr", 1300, None, "living")
G["Tagb"] = ("Tglg", "attested", "abugida", "ltr", 1300, None, "living")
G["Pauc"] = ("Latn", "stimulus", "alphabet", "ltr", 1902, None, "living")

# -------------------------------------------------------------------- HAN ----
G["Seal"] = ("Hani", "variant", "variant", "ttb", -800, None, "living")
G["Hans"] = ("Hani", "variant", "variant", "ltr", 1956, None, "living")
G["Hant"] = ("Hani", "variant", "variant", "varies", -200, None, "living")
G["Hira"] = ("Hani", "attested", "syllabary", "varies", 800, None, "living")
G["Kana"] = ("Hani", "attested", "syllabary", "varies", 800, None, "living")
G["Bopo"] = ("Hani", "attested", "syllabary", "varies", 1913, None, "living")
G["Nshu"] = ("Hani", "attested", "syllabary", "ttb", 1400, None, "historical")
G["Tang"] = ("Hani", "stimulus", "logographic", "ltr", 1036, 1500, "historical")
G["Kitl"] = ("Hani", "stimulus", "logographic", "ttb", 920, 1200, "undeciphered")
G["Kits"] = ("Kitl", "attested", "logographic", "ttb", 925, 1200, "undeciphered")
G["Jurc"] = ("Kitl", "stimulus", "logographic", "ttb", 1119, 1500, "historical")
G["Yiii"] = ("Hani", "contested", "syllabary", "ltr", 1300, None, "living")
G["Nkgb"] = ("Nkdb", "attested", "syllabary", "ltr", 1600, None, "living")
G["Shui"] = ("Hani", "stimulus", "logographic", "rtl", 1400, None, "living")
G["Hang"] = ("Phag", "contested", "featural", "varies", 1443, None, "living")
G["Jamo"] = ("Hang", "variant", "variant", "ltr", 1443, None, "living")

# ------------------------------------------------------ COMPOSITE REGISTRY ---
# Not scripts. Registry conveniences bundling several scripts for locale tagging.
G["Jpan"] = ("Hani", "composite", "composite", "varies", 800, None, "living")
G["Kore"] = ("Hani", "composite", "composite", "varies", 1443, None, "living")
G["Hanb"] = ("Hani", "composite", "composite", "varies", 1913, None, "living")
G["Hrkt"] = ("Hani", "composite", "composite", "varies", 800, None, "living")
G["Hntl"] = ("Hani", "composite", "composite", "varies", 1900, None, "living")

# ------------------------------------------------------------- NOT A SCRIPT --
# Retained because the spec removes only the six named Z codes. Marked so the
# plate does not present an emoji set as a writing system.
G["Zsye"] = ("Latn", "composite", "symbols", "ltr", 1999, None, "living")

# ---------------------------------------------------------------- FICTIONAL --
G["Teng"] = ("Latn", "stimulus", "alphabet", "ltr", 1930, None, "fictional")
G["Cirt"] = ("Runr", "stimulus", "alphabet", "ltr", 1930, None, "fictional")
G["Sara"] = ("Latn", "stimulus", "alphabet", "ltr", 1919, None, "fictional")
G["Piqd"] = ("Latn", "stimulus", "alphabet", "ltr", 1985, None, "fictional")

# Sample codepoints for the glyph specimens, keyed by ISO 15924 code.
# Only needed where the Unicode block start is a poor specimen (combining marks,
# format characters, or a block whose first rows are rarely-drawn variants).
SPECIMEN_OVERRIDE = {
    "Arab": "ابجدهو",
    "Hebr": "אבגדהו",
    "Grek": "ΑΒΓΔΕΖ",
    "Cyrl": "АБВГДЕ",
    "Latn": "ABCDEF",
    "Hani": "中文字書写語",
    "Hans": "汉字简体中文",
    "Hant": "漢字繁體中文",
    "Deva": "अआइकखग",
    "Thai": "กขฃคฅฆ",
    "Hang": "가나다라마바",
    "Hira": "あいうえおか",
    "Kana": "アイウエオカ",
    "Ethi": "ሀለሐመሠረ",
    "Armn": "ԱԲԳԴԵԶ",
    "Geor": "აბგდევ",
    "Taml": "அஆஇகஙச",
    "Beng": "অআইকখগ",
    "Telu": "అఆఇకఖగ",
    "Knda": "ಅಆಇಕಖಗ",
    "Mlym": "അആഇകഖഗ",
    "Guru": "ਅਆਇਕਖਗ",
    "Gujr": "અઆઇકખગ",
    "Orya": "ଅଆଇକଖଗ",
    "Sinh": "අආඇකඛග",
    "Mymr": "ကခဂဃငစ",
    "Khmr": "កខគឃងច",
    "Laoo": "ກຂຄງຈຊ",
    "Tibt": "ཀཁགངཅཆ",
    "Mong": "ᠠᠡᠢᠣᠤᠥ",
    "Syrc": "ܐܒܓܕܖܗ",
    "Thaa": "ހށނރބޅ",
    "Nkoo": "ߊߋߌߍߎߏ",
    "Adlm": "\U0001e900\U0001e901\U0001e902\U0001e903\U0001e904\U0001e905",
    "Cher": "ᎠᎡᎢᎣᎤᎥ",
    "Copt": "ⲀⲂⲄⲆⲈⲊ",
    "Egyp": "\U00013000\U00013001\U00013002\U00013003\U00013004\U00013005",
    "Xsux": "\U00012000\U00012001\U00012002\U00012003\U00012004\U00012005",
    "Egyh": "\U00013009\U0001300a\U0001300b\U0001300c\U0001300d\U0001300e",
    "Brai": "⠁⠃⠉⠙⠑⠋",
    # Variant and composite registry codes own no codepoint range, so the
    # specimen is named here and drawn in the face of the script they style.
    "Latf": "ABCDEF",
    "Latg": "ABCDEF",
    "Cyrs": "АБВГДЕ",
    "Aran": "ابجدهو",
    "Syre": "ܐܒܓܕܗܘ",
    "Syrj": "ܐܒܓܕܗܘ",
    "Syrn": "ܐܒܓܕܗܘ",
    "Jamo": "ᄀᄂᄃᄅᄆᄇ",
    "Hrkt": "あいうカキク",
    "Jpan": "日本語かなカ",
    "Kore": "한국어漢字書",
    "Hanb": "漢字ㄅㄆㄇㄈ",
    "Hntl": "漢字ABCD",
    "Bopo": "ㄅㄆㄇㄈㄉㄊ",
    "Zsye": "☺★☂✈♪⚑",
}
