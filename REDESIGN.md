# Seungjae Han website

## Pages

`index.html` is the homepage, with Vision, Research, and Impact sections. The full site also contains `vision.html`, `research.html`, `profile.html`, `publications.html`, `resources.html`, `news.html`, and `contact.html`. Every page has the same working menu and footer. Existing profile information, photograph, CV and all 16 publication records have been retained.

The static pages require no build step. Open `index.html` with its adjacent files intact. `preview.html` is a separate single-file review version containing all eight pages; it uses hash routes so links work without adjacent HTML files. Browser back/forward, publication year selection, CV links, and profile accordions are supported. The single-file preview requires JavaScript; the static pages retain their core navigation/content without JavaScript.

## Reference and writing

Reference: https://www.rajanlab.com/ and https://www.rajanlab.com/kanaka-rajan, including Research, Publications, Resources, and menu layouts. This version follows the reference's red introductory sections, white/purple/gray content bands, rectangular linked blocks, four-column menu and charcoal footer. It does not reuse the lab's identity, biography, people, affiliations, or research claims.

**Vision and research-direction prose is a draft based on the research described on the existing personal website and papers. It is not a supplied or approved personal mission statement.**

Research sources:
- SUPPORT: https://www.nature.com/articles/s41592-023-02005-8
- Analogue computing: https://www.nature.com/articles/s41928-024-01318-6
- U-BSN: https://doi.org/10.1109/WACV61041.2025.00135
- REALS: https://doi.org/10.1109/WACV56688.2023.00198
- SUPPORT code: https://github.com/NICALab/SUPPORT
- SUPPORT data: https://zenodo.org/records/8176722

SUPPORT Figure 1 is loaded from the publisher and attributed in each caption to Eom, Han, Park et al., Nature Methods (2023), under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. The existing journal cover image and portrait are preserved.

## Typography

The reference uses Manrope variable font. `assets/site.css` references the same public CDN source. No font binaries are included in the repository, ZIP or HTML preview. Normal internet access to that CDN is required. If it fails in the single-file preview, a visible message identifies the fallback instead of silently describing it as Manrope.

Desktop profile name: 50px, weight 300, line-height 60px. Affiliation: 18px/27px, weight 400. Body: 16px/24px, weight 400. Tablet and mobile title sizes follow the reference breakpoints. Browser/OS rasterization and preview zoom can still differ.

`tests/font_check.py` compares CSS metrics and the rendering of identical strings against the reference in the same Chromium session, verifies actual custom-font use via CDP, and tests the font-failure warning. `tests/website_preview.py` checks eight pages at eight widths, local links, all native and preview routes, browser history, internal anchors, year selection and no-JavaScript behavior. Reports and screenshots are generated under `previews/`.

To regenerate the single-file preview only: `pip install beautifulsoup4` then `python tools/build_preview.py`. To edit the deployed site, edit the corresponding static HTML and shared CSS/JavaScript.
