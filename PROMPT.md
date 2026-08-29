# The prompt

This is the brief that produced [the plate](out/descent_of_writing.svg). It is
written to be handed to any coding agent that can run code and reach the
network, and to be argued with.

Copy everything inside the block. The block is self-contained: the source URLs
are the ones that actually resolve, the counts are what the sources really
return, and the traps section is the list of things that went wrong the first
time. Skipping the traps costs about a day.

**What it needs.** Python 3.10+, network access, roughly 90 MB of downloads,
and an agent allowed to install `fonttools`, `uharfbuzz` and `brotli`. A cold
run takes 15 to 20 minutes, most of it waiting on the Wikidata query service.

**What it is not.** This is not a prompt for an image model. No text-to-image
system can write 7,000 correct language names or draw Linear A from memory. It
asks for code that renders real data, which is the only way "every script" can
mean anything.

---

```text
GOAL
One poster-scale reference plate, in two joined zones:

  ZONE A (upper): the descent of human WRITING. Every script in the ISO 15924
    registry, documented, with real glyph specimens, arranged as a tree from
    the origins of writing. Multiple independent origins, not one apex.

  ZONE B (lower): every human language, one mark each, hung under the script
    that writes it, with a separate register for those no source records a
    script for.

  ZONE C: a catalogue keyed by ISO 15924 code, so nothing the plate asserts
    is missing a row.

The zones share one frame and one edge system. Nothing sampled, nothing
elided, no "..." placeholders, no representative subsets.

You are writing code that fetches real data and renders it. Do not draw
anything from memory. If a fact is not in a source file, it does not go on
the plate.


DATA: the script inventory
- ISO 15924 registry: https://www.unicode.org/iso15924/iso15924.txt
  Semicolon-separated: Code;Number;English;French;PVA;UnicodeVersion;Date
  This is the closed, authoritative list and the guarantee of completeness.
  Load every row. Remove only the six special codes Zinh Zyyy Zzzz Zmth Zsym
  Zxxx and the private-use range markers Qaaa and Qabx. That currently leaves
  218 scripts out of 226 rows. Compute the real numbers, do not hardcode mine.
  An empty UnicodeVersion field means the script is not encoded at all.
- Unicode Character Database, latest:
  https://www.unicode.org/Public/UCD/latest/ucd/Scripts.txt
  https://www.unicode.org/Public/UCD/latest/ucd/Blocks.txt
  https://www.unicode.org/Public/UCD/latest/ucd/extracted/DerivedGeneralCategory.txt
  Use DerivedGeneralCategory to pick letters for the specimens. Do not use the
  language runtime's own Unicode tables: they lag the UCD by several versions
  and return "unassigned" for every recently added script.
- Wikidata, for native names and a cross-check only:
  P506 (ISO 15924 code), P1705 (native label), P571 (inception), P144 (based on).

DATA: the languages
- Glottolog 5 CLDF. The repository is glottolog/glottolog-cldf, branch master.
  (glottolog-cldr does not exist. This costs a 404 if you guess.)
  https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/languages.csv
  https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/values.csv
  languages.csv carries Level, Family_ID, Is_Isolate, Macroarea, ISO639P3code.
  values.csv (21 MB) carries Parameter_ID "aes" for endangerment and
  "category" for Sign_Language, Pidgin, Artificial_Language and the rest.
- Wikidata via https://query.wikidata.org/sparql, joined on ISO 639-3 (P220):
  P282 (writing system) and P1098 (number of speakers).
- Unicode CLDR supplementalData.xml languageData, as an independent second
  opinion on which script a language uses. It is keyed by BCP47, so bridge it
  with the SIL ISO 639-3 tables (iso-639-3.tab has a Part1 column).

SCOPE, exact
- Scripts: all 218. Keep the variant codes (Latf, Cyrs, Aran, the Syriac
  three) and the composite registry codes (Jpan, Kore, Hanb, Hrkt, Hntl).
  They are written forms and registry facts; mark what they are rather than
  dropping them.
- Zsye (Emoji) is not one of the six special codes, so it stays. Draw it,
  type it as a symbol set, and do not present it as a writing system.
- Languages: Glottolog Level == "language" only. Drop Level == "dialect".
  Exclude category Artificial_Language: constructed languages are not part of
  human descent. Include sign languages, pidgins, extinct and ancient.
  Expect roughly 8,600 languages, 245 families, 183 isolates. Compute them.

ZONE A: what "documented" means, per script, non-negotiable
Every script node carries, legible at full zoom:
  1. Name, plus the native name where a source has one
  2. ISO 15924 four-letter code and numeric code
  3. Type: logographic, syllabary, abjad, alphabet, abugida, featural,
     semasiographic, undeciphered, or a marked non-script
  4. Direction: ltr, rtl, ttb, boustrophedon, varies
  5. Span of use, first attestation to last, as absolute dates
  6. Status: living, historical, revived, undeciphered, constructed, fictional
  7. A REAL GLYPH SPECIMEN, at least six characters, outlines pulled from a
     font and shaped. Never drawn by hand, never approximated, never a
     lookalike from another script.

ZONE A: the glyph specimens
- Fonts: the Noto project, SIL OFL. Direct file URL pattern:
  https://raw.githubusercontent.com/notofonts/notofonts.github.io/main/fonts/{Family}/hinted/ttf/{Family}-Regular.ttf
  Family resolves from the registry's PVA field: "NotoSans" + PVA with
  underscores stripped. That works for about 199 of the 218. Fall back to
  "NotoSerif" + stem, then "Noto" + stem. The rest need a hand-written map:
  Latin, Greek and Cyrillic live in NotoSans; Braille in NotoSansSymbols2;
  N'Ko is NotoSansNKo; both Meroitic codes share NotoSansMeroitic;
  Nastaliq is NotoNastaliqUrdu; hieratic is unified with NotoSansEgyptianHieroglyphs.
- CJK, Hangul and kana are in a different repository and the files are huge.
  Get a tiny subset instead, through the Google Fonts CSS API with a text
  parameter: https://fonts.googleapis.com/css2?family=Noto+Sans+SC&text=...
  It returns exactly the requested characters. Key any cache on the requested
  text, or a subset fetched for other characters will be reused and every
  glyph will silently miss.
- SHAPE THE TEXT. Use HarfBuzz (uharfbuzz), not the cmap. Arabic and every
  Brahmic script build their real letterforms through GSUB, and Nastaliq's
  base glyphs are empty outlines: reading the cmap gives disconnected stubs,
  or nothing at all. Shape, then convert the positioned glyphs to SVG paths.
- Variant and composite codes own no codepoint range in Scripts.txt, so name
  their specimen characters explicitly and draw them in the face of the script
  they are a style of. Label them as borrowing that face.
- A script with no font gets a marked gap, never a substitute. Currently 39
  scripts have no specimen; 32 of those are not encoded in Unicode at all, so
  no font for them can exist. Name every one of them on the plate.

ZONE A: descent
- CURATE THE GENEALOGY BY HAND. Do not scrape it. Wikidata P144 covers about
  half the registry and contradicts itself on the Semitic chain. Write one
  readable table: code -> (parent, edge strength, type, direction, start, end,
  status), sourced against standard palaeography (Daniels and Bright, The
  World's Writing Systems; Coulmas, Blackwell Encyclopedia of Writing Systems;
  the Unicode proposals for recent additions).
- Edge strength is part of the data, not decoration:
    attested   direct graphical descent, uncontroversial
    contested  descent claimed but disputed in the literature
    stimulus   the idea of writing borrowed, the letters invented fresh
    variant    the same script in another style or tradition
    composite  a registry code bundling several scripts, not a script
  Give each a distinct stroke and put all five in the legend.
- Origins: writing was invented independently more than once. Sumerian
  proto-cuneiform, Chinese oracle bone and Mesoamerican are treated as
  independent. Mark as contested, do not resolve: Egyptian hieroglyphs
  (stimulus diffusion from Sumer is a live argument) and the Indus script
  (whether it encodes language at all is unsettled). The registry already
  contains the ancestral nodes you need: Pcun, Psin, Pelm, Egyp, Xsux, Inds,
  Roro, Maya, Lina, Hluw.
- Run the chain to full depth. The Proto-Sinaitic line is the deepest:
  Egyp > Psin > Phnx > {Grek > {Ital > Latn, Cyrl, Copt, Goth},
  Armi > {Hebr, Syrc, Nbat > Arab, Brah > all Indic and Southeast Asian}}.
  Do not shortcut it. Every intermediate node is a documented script.
- Assert: every script reaches an origin or is one, and no cycles.

ZONE B: the languages
- Hang each language under the script a source assigns it, ordered by family
  inside each field so genealogy reads as contiguous runs.
- Mark area is speaker count on a log scale, with one cell size shared across
  the whole zone so marks compare between fields. Sizing marks against each
  field's own cell makes a script with one language draw fatter dots than a
  script with ninety-one, which inverts the only thing size is meant to say.
- Fading runs from safe through threatened to moribund. A hollow ring is an
  extinct language.
- Languages with no recorded script get their own register, full width, its
  HEIGHT in proportion to how many it holds, packed at the same density, so
  the areas compare directly.

ZONE B: the honesty requirement, do not skip this
Open data cannot tell you a language is unwritten. It can only tell you no
source records a script for it. Wikidata plus CLDR currently cover about 1,500
of 8,600 languages, so about 82% land in the unrecorded register. The figure
usually quoted for genuinely unwritten languages is nearer 40%. Both numbers
are on the plate only if you label them for what they are. Print the measured
count, state in plain words that it is a gap in the record and not a finding
about the languages, and never let the caption imply otherwise.

LAYOUT
- A tidy tree: leaves take sequential columns in tree order, each parent sits
  over the MIDDLE OF ITS LEAF SPAN, then separate each depth band so no two
  cards collide, moving nodes as little as possible.
- Do not centre each band on the canvas. It gives a cleaner silhouette and
  destroys the plate: a node's position stops relating to its parent's and the
  descent lines become long horizontal sweeps nobody can trace.
- Do not average the children's positions either. A parent with one huge
  subtree and two small late children gets dragged onto the margin, and the
  error compounds at every level.
- The widest band sets the canvas width. Size the canvas from it rather than
  from a global column pitch, which wastes most of the width on sparse bands.

STYLE
A scientific plate or a museum wall chart, not an infographic. Flat. No glow,
no gradients, no drop shadows, no 3D. Typography does the work. One palette,
dark ink on warm paper or the inverse. Reserve hue for the origin a script
descends from, and neutral grey for unwritten and unknown.

OUTPUT
- SVG, at least 16000 wide, every node carrying its ISO 15924 code or
  Glottocode as an element id so the file is inspectable and zoomable to a
  single record.
- A PNG render for preview.
- A companion CSV, one row per script, with all seven documentation fields, so
  the plate is auditable against its own data.

ACCEPTANCE. Compute each of these, print them on the plate, and assert them in
code against the finished SVG. A check that cannot fail proves nothing: after
they pass, delete one script from the output and confirm the checks go red.
  1. Scripts drawn == non-special ISO 15924 count, each exactly once, none
     missing and none extra.
  2. The scripts with no glyph specimen, listed by name, with the reason.
  3. Language marks drawn == Glottolog level=language count, minus constructed.
  4. Families drawn == distinct Family_ID count.
  5. Every script traces to an origin or is one. No cycles.
  6. Count and percentage of languages with no script recorded.
  7. Source versions and retrieval date.


KNOWN TRAPS
Each of these produces a plate that looks right and is wrong.

- HarfBuzz cannot open a woff2 blob. It builds an empty face, every glyph
  resolves to glyph id 0, and .notdef in most Noto faces is a drawn box with
  real bounds, so it passes a "does this glyph have an outline" check. You get
  neat grids of tofu presented as Chinese. Decompress to sfnt before shaping,
  and refuse glyph id 0 outright. In fontTools, save() keeps the woff2 flavor
  unless you clear it first.
- The Wikidata query service rate-limits hard during outages, currently one
  request per minute. Back off past 70 seconds or every query fails at once.
- Absence of a Wikidata P282 link is not evidence a language is unwritten. See
  the honesty requirement.
- ISO 15924 names are not all clean. "(Small) Seal" starts with a parenthesis,
  so cutting a name at the first "(" empties it. Strip trailing parentheticals
  only.
- cairosvg needs a libcairo shared library that is not present on Windows. If
  a rasterizer is missing, drive the Chrome or Edge already installed in
  headless screenshot mode rather than downloading a renderer.
- Do not let the pyramid in your head beat the data. The shape that comes out
  is narrow at the origins, widest where the Brahmic and Latin families bloom,
  narrow again at the tips. That is what the descent looks like.
```

---

## Variations worth asking for

The brief above makes some choices. Any of them can be swapped, and each
changes the plate rather than decorating it.

**Colour by endangerment or by macroarea** instead of by origin. Hue can only
carry one variable. Origin makes the plate about history; endangerment makes it
about loss.

**Both recursions at equal weight.** Right now language genealogy is reduced to
a sort order inside each script field. Drawing the script tree and the language
family tree facing each other, linked by chords, is denser and more honest
about the fact that script and descent are orthogonal.

**Non-glyphic recording systems.** Andean quipu, wampum, Australian message
sticks. They are outside ISO 15924 and outside this plate, which is a
defensible line, not an obvious one.

**Fictional scripts.** Tengwar, Cirth, Klingon and Sarati are in the registry
and on the plate, marked as fictional. Dropping them is reasonable. Dropping
them silently is not.

**Dialects.** Glottolog has 13,706 of them under the 8,600 languages. Including
them triples the plate and changes what "a language" means on it.

## Provenance

Everything above was written after building it, not before. The traps section
exists because each of those items broke the first attempt. The original
sketch that started this was a hand-drawn pyramid with three labels on it; the
argument that turned it into this spec is worth more than the spec.
