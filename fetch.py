"""Download every raw source. Nothing derived here, only bytes to disk."""
import os, sys, json, urllib.request, ssl, time

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
CTX = ssl.create_default_context()
UA = {"User-Agent": "writing-genealogy/1.0 (research plate; contact via local)"}

SOURCES = {
    "iso15924.txt":  "https://www.unicode.org/iso15924/iso15924.txt",
    "Scripts.txt":   "https://www.unicode.org/Public/UCD/latest/ucd/Scripts.txt",
    "Blocks.txt":    "https://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt",
    "PropertyValueAliases.txt": "https://www.unicode.org/Public/UCD/latest/ucd/PropertyValueAliases.txt",
    "DerivedAge.txt": "https://www.unicode.org/Public/UCD/latest/ucd/DerivedAge.txt",
    "DerivedGeneralCategory.txt": "https://www.unicode.org/Public/UCD/latest/ucd/extracted/DerivedGeneralCategory.txt",
    "ReadMe.txt":    "https://www.unicode.org/Public/UCD/latest/ucd/ReadMe.txt",
    "glottolog_languages.csv":  "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/languages.csv",
    "glottolog_values.csv":     "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/values.csv",
    "glottolog_parameters.csv": "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/parameters.csv",
    "glottolog_codes.csv":      "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/codes.csv",
    "glottolog_metadata.json":  "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/cldf-metadata.json",
    # second opinion on which script a language is written in, and the 639-1 to
    # 639-3 bridge CLDR needs to be joined to Glottolog
    "cldr_supplemental.xml":    "https://raw.githubusercontent.com/unicode-org/cldr/main/common/supplemental/supplementalData.xml",
    "iso-639-3.tab":            "https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3.tab",
}


def get(url, dest, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90, context=CTX) as r:
                body = r.read()
            with open(dest, "wb") as f:
                f.write(body)
            return len(body)
        except Exception as e:
            if i == tries - 1:
                return "FAIL: %s" % e
            time.sleep(2 + 3 * i)


if __name__ == "__main__":
    for name, url in SOURCES.items():
        dest = os.path.join(DATA, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            print("%-30s cached %d b" % (name, os.path.getsize(dest)))
            continue
        r = get(url, dest)
        print("%-30s %s" % (name, r))
