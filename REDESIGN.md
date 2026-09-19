# Seungjae Han homepage — revised layout

The profile page now follows the rendered layout of https://www.rajanlab.com/kanaka-rajan rather than the previous Seungjae Han website.

The reference was inspected at 1440 px and 390 px. The revision uses its red upper background (#982b34), white profile heading, Manrope typography, overlapping square portrait, plain contact links, light-gray CV section (#f0f0f0), square accordion controls, and purple footer (#420d5d). The earlier cream/teal palette, serif headings, numbered section labels, research cards, badges, counters, and promotional subtitles have been removed.

The Rajan Lab name, logo, photograph, institutional affiliations, and biographical text are not reused. Seungjae Han's profile photograph, CV, contact information, education, appointments, fellowships, awards, service record, news, and 16 publication records are retained from the existing site. The short biography is rewritten around those records. Publication status has not been independently refreshed in this visual revision.

## Files

- `index.html`: profile and seven native expandable CV sections.
- `publications.html`: full publication list, with year links.
- `assets/site.css`: shared layout, responsive rules and print styles.
- `assets/site.js`: menu dismissal, section deep links and print expansion.
- `photo.jpeg`, `CV_SeungjaeHan_0707.pdf`: unchanged originals.

Open `index.html` directly, or serve the directory as a static site. No build step is required. Manrope is loaded from Google Fonts; no font files are distributed. Arial is the fallback when the external font is unavailable. The CV sections and navigation menu use native HTML details elements and work without JavaScript.

The existing page paths remain unchanged. The publication page is intentionally a plain list rather than the previous filter dashboard. Direct publisher links are retained where available; other links are explicitly labelled Google Scholar.

## Checks

`tests/website_preview.py` checks both pages at 320, 390, 560, 768, 1024 and 1440 px, native CV accordions, desktop/mobile navigation, section links, all 16 publication records, local asset paths, and JavaScript-disabled use. The pull-request workflow also captures desktop/mobile screenshots with the webfont loaded when available.

Changes are on the existing review branch. The public `main` branch is not changed or deployed by the preview workflow.
