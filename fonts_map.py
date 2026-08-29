# -*- coding: utf-8 -*-
"""ISO 15924 code -> Noto font family.

199 of the 218 codes resolve automatically from the registry's Unicode property
value alias (PVA): NotoSans<PVA with underscores stripped>. The rest are listed
here because the family name does not follow the PVA, because the script lives
in a shared font, or because Noto has not shipped it.
"""

NOTO_REPO = ("https://raw.githubusercontent.com/notofonts/notofonts.github.io/"
             "main/fonts/{fam}/hinted/ttf/{fam}-Regular.ttf")

# Scripts whose glyphs live in a font not named after them.
MANUAL = {
    "Latn": "NotoSans",
    "Grek": "NotoSans",
    "Cyrl": "NotoSans",
    "Cyrs": "NotoSans",
    "Latf": "NotoSans",          # Fraktur has no Noto face; Latin body stands in
    "Latg": "NotoSans",          # same, Gaelic type has no Noto face
    "Brai": "NotoSansSymbols2",
    "Nkoo": "NotoSansNKo",
    "Mero": "NotoSansMeroitic",
    "Merc": "NotoSansMeroitic",
    "Hmnp": "NotoSerifNPHmong",
    "Syre": "NotoSansSyriac",
    "Syrj": "NotoSansSyriacWestern",
    "Syrn": "NotoSansSyriacEastern",
    "Aran": "NotoNastaliqUrdu",
    "Kits": "NotoSerifKhitanSmallScript",
    "Nshu": "NotoSansNushu",
    "Mtei": "NotoSansMeeteiMayek",
    "Egyh": "NotoSansEgyptianHieroglyphs",   # hieratic is unified with hieroglyphs
}

# CJK and Korean live in a separate repo with very large files. Pull a subset
# containing only the specimen characters through the Google Fonts text= API.
GF_SUBSET = {
    "Hani": "Noto Sans SC",
    "Hans": "Noto Sans SC",
    "Hant": "Noto Sans TC",
    "Hang": "Noto Sans KR",
    "Jamo": "Noto Sans KR",
    "Hira": "Noto Sans JP",
    "Kana": "Noto Sans JP",
    "Hrkt": "Noto Sans JP",
    "Bopo": "Noto Sans TC",
    "Jpan": "Noto Sans JP",
    "Kore": "Noto Sans KR",
    "Hanb": "Noto Sans TC",
    "Hntl": "Noto Sans SC",
    "Zsye": "Noto Emoji",
}

# Variant and composite codes have no codepoint range of their own in
# Scripts.txt, so the specimen has to be named explicitly and is drawn in the
# face of the script they are a style of. The plate labels them as such.
BORROWS_PARENT_FACE = {"Latf", "Latg", "Cyrs", "Syre", "Syrj", "Syrn", "Aran", "Hant", "Hans"}

# Codes with no Noto face at all. Recorded so the plate can state the gap
# instead of quietly leaving a blank. Reason is printed in the companion CSV.
NO_FONT = {
    # never encoded in Unicode, so no font can exist
    "Afak": "not encoded in Unicode",
    "Berf": "not encoded in Unicode",
    "Blis": "not encoded in Unicode",
    "Chis": "not encoded in Unicode",
    "Cirt": "not encoded in Unicode",
    "Egyd": "not encoded in Unicode",
    "Inds": "not encoded in Unicode",
    "Jurc": "not encoded in Unicode",
    "Kitl": "not encoded in Unicode",
    "Kpel": "not encoded in Unicode",
    "Leke": "not encoded in Unicode",
    "Loma": "not encoded in Unicode",
    "Maya": "not encoded in Unicode",
    "Moon": "not encoded in Unicode",
    "Nkdb": "not encoded in Unicode",
    "Nkgb": "not encoded in Unicode",
    "Pcun": "not encoded in Unicode",
    "Pelm": "not encoded in Unicode",
    "Phlv": "not encoded in Unicode",
    "Piqd": "not encoded in Unicode",
    "Psin": "not encoded in Unicode",
    "Ranj": "not encoded in Unicode",
    "Roro": "not encoded in Unicode",
    "Sara": "not encoded in Unicode",
    "Seal": "not encoded in Unicode",
    "Shui": "not encoded in Unicode",
    "Sidt": "not encoded in Unicode",
    "Tayo": "not encoded in Unicode",
    "Teng": "not encoded in Unicode",
    "Tols": "not encoded in Unicode",
    "Visp": "not encoded in Unicode",
    "Wole": "not encoded in Unicode",
    # encoded, but Noto has not shipped a face yet (all Unicode 16, 2024)
    "Gara": "encoded in Unicode 16, no Noto face released",
    "Gukh": "encoded in Unicode 16, no Noto face released",
    "Krai": "encoded in Unicode 16, no Noto face released",
    "Onao": "encoded in Unicode 16, no Noto face released",
    "Tutg": "encoded in Unicode 16, no Noto face released",
    "Sunu": "encoded in Unicode 16, no Noto face released",
    "Todr": "encoded in Unicode 16, no Noto face released",
}


def family_for(code, pva):
    """Candidate Noto families for an ISO 15924 code, best first."""
    if code in MANUAL:
        return [MANUAL[code]]
    if not pva:
        return []
    stem = pva.replace("_", "")
    return ["NotoSans" + stem, "NotoSerif" + stem, "Noto" + stem]
