# Han Lab — complete lab-site review

## Scope

This revision replaces the personal-homepage structure with a full laboratory website. The reference is https://www.rajanlab.com/ and its complete navigation, not only the PI profile page.

17 pages: Home, Vision, Our Science, three research-detail pages, Publications, Funding, Resources, Our Team, Seungjae Han's profile, Press, Comics, Comp Neuro FAQs, Join Us, News, Contact.

The four navigation groups mirror the reference's information structure: Research, People, Broader Impacts, Work With Us. All internal links lead to complete pages; no placeholder links or non-functional forms are used.

## Content that needs the owner's approval before publication

- **Han Lab is a provisional name for this draft.** The research direction and the lab-level “we” wording are proposed website copy, not evidence of an established independent lab.
- Seungjae Han's verified role remains postdoctoral fellow at KAIST. He is not labelled a professor or principal investigator.
- The People page contains only Seungjae Han. It distinguishes existing research connections from lab membership. No students or alumni were invented.
- Funding lists individual fellowships, not invented lab grants.
- Join Us provides enquiry routes and clearly states that no specific funded vacancy is being advertised.
- Publications include work by Seungjae Han and collaborators predating this draft. Existing entries are preserved; the publication list is not presented as an exhaustive independently re-audited bibliography.

## Editing

Static HTML files work without a build tool. `index.html` is the landing page. `preview.html` contains all routes and local images in one review file, plus an embedded CV. The webfont is still loaded from its original public CDN.

To regenerate after editing source content:

```sh
python -m pip install beautifulsoup4
python tools/build_lab.py
python tools/build_preview.py
```

Page copy and shared navigation are in `tools/build_lab.py`. Existing profile, publications and news content are in `data/*-main.html`. Coverage records can be edited in `data/press.json`. Layout overrides are in `assets/lab.css`. Rebuilding overwrites the generated HTML, so edit these sources rather than both representations.

## Sources and credits

Profile and fellowships: https://stevejayh.github.io/ and https://nica.kaist.ac.kr/people

SUPPORT: Eom, Han, Park et al., Nature Methods (2023), https://www.nature.com/articles/s41592-023-02005-8
The unmodified Figure 1 is reused under CC BY 4.0 with visible credit. Code: https://github.com/NICALab/SUPPORT. Data: https://zenodo.org/records/8176722

Analogue computing: Jeong, Han et al., Nature Electronics (2025), https://www.nature.com/articles/s41928-024-01318-6
REALS: https://doi.org/10.1109/WACV56688.2023.00198
Multi-scale J-invariant networks: https://doi.org/10.1109/WACV61041.2025.00135

Press records (five):
- KAIST Breakthroughs, 2025-02-27: https://breakthroughs.kaist.ac.kr/sub02/view/page/1/id/4062 (headline paraphrased).
- Nature Electronics News & Views, 2025-02-11: https://www.nature.com/articles/s41928-025-01341-1
- KAIST EE research news, 2025-01-23: https://ee.kaist.ac.kr/en/research-achieve/ee-prof-shinhyun-choi-and-young-gyu-yoons-joint-research-team-develops-neuromorphic-semiconductor-chip-that-learns-and-corrects-itself/
- ScienceDaily, 2025-01-21: https://www.sciencedaily.com/releases/2025/01/250121125920.htm (KAIST-sourced report, not an independent interview).
- KAIST Breakthroughs, 2024-02-26: https://breakthrough.kaist.ac.kr/sub03/view/id/497

The Nature Methods cover is an existing user-repository asset. It is identified separately from media coverage. The other graphics, including the two four-panel science comics and press thumbnails, are original conceptual schematics, not experimental measurements or images from the linked coverage.

Manrope uses the same public font URL as the reference. No font files are included in the repository, ZIP or single-file preview. An internet connection is required for that font; offline reading uses a fallback. The font check verifies actual rendered custom fonts with Chromium, not merely the declared CSS family name.

## Validation

`tests/lab_test.py` checks all 17 pages at 320, 390, 768, 1024 and 1440px; local links and section targets; every preview route; menu and browser-back behaviour; press filters; publications; FAQs; profile accordions; and navigation without JavaScript. Screenshot and font-check evidence is written to `previews/`.

Changes belong only to the review branch. There is no automatic merge into main and no production deployment in this revision.

## Colour roles: blue highlight, independent secondary colours

The former red highlight (`#982B34`) is now the owner-supplied `#004890`.
All other CSS is restored to the pre-blue baseline. This is not a monochromatic
blue theme, and it does not recolour research figures or publication covers.

- Main heading bands and formerly red highlights: `#004890`.
- Research sections, menu, and Publications tile: purple `#420D5D`.
- Our Science tile: indigo `#1B1464`.
- People tile: dark teal `#1F4B51`.
- Footer: charcoal `#343A40`.
- Neutral section backgrounds: `#F0F0F0`; body text and borders remain neutral.

The legacy `--red` variable means the primary highlight role. Its value is blue.
The other colour variables retain their independent roles and original values.
`#017CC2` is not used as a second site-wide wash. Typography, content, all 17
page routes and interaction code are unchanged. The portable preview uses the
same styles and retains working navigation.

`tests/palette_roles.py` checks the distinct section, card, menu, footer and
Press colours, including the single-file preview. The standard lab tests cover
all 17 pages and their interactions.
