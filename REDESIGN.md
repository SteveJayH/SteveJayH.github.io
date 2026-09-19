# Seungjae Han homepage — revised layout

The profile page follows the rendered layout of https://www.rajanlab.com/kanaka-rajan rather than the previous Seungjae Han website.

The reference was inspected at desktop and mobile widths. The revision uses its red upper background (#982b34), white profile heading, Manrope typography, overlapping square portrait, plain contact links, light-gray CV section (#f0f0f0), square accordion controls, and purple footer (#420d5d). The earlier cream/teal palette, serif headings, numbered section labels, research cards, badges, counters, and promotional subtitles have been removed.

The Rajan Lab name, logo, photograph, institutional affiliations, and biographical text are not reused. Seungjae Han's profile photograph, CV, contact information, education, appointments, fellowships, awards, service record, news, and 16 publication records are retained from the existing site. The short biography is rewritten around those records. Publication status has not been independently refreshed in this visual revision.

## Files

- `index.html`: profile and seven native expandable CV sections.
- `publications.html`: full publication list, with year links.
- `assets/site.css`: shared layout, external font definition, responsive rules and print styles.
- `assets/site.js`: menu dismissal, section deep links and print expansion.
- `photo.jpeg`, `CV_SeungjaeHan_0707.pdf`: unchanged originals.

Open `index.html` directly, or serve the directory as a static site. No build step is required. The primary Manrope variable font is loaded from the exact public CDN asset used by the reference page. Google Fonts Manrope remains an external fallback, followed by Arial. No font files are stored in the repository or distributed in the ZIP. An internet connection is needed to load webfonts. The CV sections and navigation menu use native HTML details elements and work without JavaScript.

The existing page paths remain unchanged. The publication page is intentionally a plain list rather than the previous filter dashboard. Direct publisher links are retained where available; other links are explicitly labelled Google Scholar.

## Typography revision

The original 42px tablet title was not the reference size. It is now 48px at 768–991px and 50px above 991px, with 300 weight and 1.2 line height. The tablet image column is narrowed slightly so the larger name and 18px affiliation text fit without clipping the red band. Mobile titles stay 32px. Browser-synthesized weights are disabled and macOS font smoothing matches the reference. The desktop layout, colors, text, links and photograph are otherwise unchanged.

## Checks

`tests/website_preview.py` checks both pages at 320, 390, 560, 768, 1024 and 1440 px, native CV accordions, desktop/mobile navigation, section links, all 16 publication records, local asset paths, and JavaScript-disabled use. The pull-request workflow captures desktop/mobile screenshots after the primary webfont loads.

`tests/font_check.py` checks the actual browser-rendered face, compares headline/body/section-label glyphs with the reference, checks reference title sizes at mobile/tablet/desktop widths, and checks WebKit font loading. A missing primary webfont fails the test rather than silently accepting Arial. Its report also records whether the previous Google Fonts headline raster is the same; different font URLs alone are not evidence of different glyphs.

Changes are on the existing review branch. The public `main` branch is not changed or deployed by the preview workflow.
