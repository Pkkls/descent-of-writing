# Notice

The MIT licence in [LICENSE](LICENSE) covers the code in this repository. The
outputs and the data they are built from carry their own terms.

## Outputs

`out/descent_of_writing.svg`, `out/descent_of_writing.png` and
`out/scripts_catalogue.csv` are released under
[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/), because they
incorporate Glottolog data published under that licence.

Attribution for reuse:

> Glottolog 5, Hammarström, Forkel, Haspelmath and Bank, CC-BY-4.0.

## Glyph specimens

The SVG embeds glyph outlines extracted from Noto fonts and shaped with
HarfBuzz. Noto is published under the
[SIL Open Font License 1.1](https://openfontlicense.org/). The font files
themselves are not redistributed here: `fonts.py` downloads them at build
time from https://github.com/notofonts and the extracted outlines are a
derivative work under the OFL.

## Source data

| Source | Terms |
|---|---|
| ISO 15924 registry | [Unicode Terms of Use](https://www.unicode.org/copyright.html) |
| Unicode Character Database | Unicode Terms of Use |
| Unicode CLDR | Unicode Terms of Use |
| Glottolog 5 CLDF | CC-BY-4.0 |
| Wikidata | CC0 |
| SIL ISO 639-3 code tables | [SIL terms of use](https://iso639-3.sil.org/code_tables/download_tables) |

None of these sources are redistributed in this repository. `fetch.py` and
`fetch_wikidata.py` retrieve them at build time. What is committed under
`out/` is the derived result.
