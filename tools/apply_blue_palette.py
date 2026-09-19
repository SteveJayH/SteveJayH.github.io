"""Apply the owner's two-blue palette without changing content, links or typography."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOKENS = """:root {
  --brand-primary: #004890;
  --brand-accent: #017cc2;
  --brand-deep: #00366b;
  --brand-secondary: #005b91;
  --brand-footer: #082e50;
  --surface: #eef5fa;
  --border: #cbdce8;
  --ink: #132b40;
  --muted: #4b6275;
  /* Compatibility aliases for the existing section classes. */
  --red: var(--brand-primary);
  --purple: var(--brand-deep);
  --blue: var(--brand-primary);
  --gray: var(--surface);
  --teal: var(--brand-secondary);
  --charcoal: var(--brand-footer);
  --width: 1280px;
}"""
MAPPING = {
    '#982b34': 'var(--brand-primary)',
    '#420d5d': 'var(--brand-deep)',
    '#42105b': 'var(--brand-deep)',
    '#321446': 'var(--brand-deep)',
    '#1b1464': 'var(--brand-accent)',
    '#1f4b51': 'var(--brand-secondary)',
    '#343a40': 'var(--brand-footer)',
    '#4d65ff': 'var(--brand-accent)',
    '#f0f0f0': 'var(--surface)',
    '#e1e1e1': 'var(--border)',
    '#ccc': 'var(--border)',
    '#ddd': 'var(--border)',
    '#585858': 'var(--muted)',
    '#505050': 'var(--muted)',
    '#565656': 'var(--muted)',
    '#484848': 'var(--muted)',
}
EXTRA = """
/* School-blue palette. Layout, copy and Manrope settings are unchanged. */
@media screen {
  .section.purple { background: var(--brand-secondary); }
  .science-art { color: var(--brand-accent); }
  .science-art.inverse { color: #fff; }
  .text-link, .button-link, .article-link { color: var(--brand-primary); }
  .text-link .arrow, .link-arrow { color: var(--brand-accent); }
  .text-link:hover, .button-link:hover, .article-link:hover { color: var(--brand-accent); }
  .gray .text-link:hover, .gray .button-link:hover, .resume a:hover { color: var(--brand-primary); }
  .page-hero a, .purple a, .teal a, .menu-panel a, .site-footer a { color: #fff; }
  .page-hero a:hover, .purple a:hover, .teal a:hover, .menu-panel a:hover, .site-footer a:hover { color: #fff; }
  .page-hero .arrow, .purple .arrow, .teal .arrow, .menu-panel .arrow, .site-footer .arrow { color: #fff; }
  .press-controls button[aria-pressed="true"] { color: var(--brand-primary); border-bottom-color: var(--brand-accent); }
  .press-thumb.thumb-3 { background: var(--brand-accent); }
  .comic-panel { border-color: var(--border); color: var(--brand-deep); }
  .comic-panel:nth-child(2n) { color: var(--brand-primary); }
  .footer-links > a:last-child { color: #cbdce8; }
  :focus-visible { outline: 2px solid var(--brand-accent); outline-offset: 4px; box-shadow: 0 0 0 4px #fff; }
  ::selection { color: #fff; background: var(--brand-primary); }
}
"""
css_path = ROOT/'assets/site.css'
css = css_path.read_text()
css = re.sub(r':root\s*\{[^}]*\}', lambda _: TOKENS, css, count=1)
css = css.replace('  color: #000;\n  font-family:', '  color: var(--ink);\n  font-family:', 1)
pattern = re.compile(r'#[0-9a-fA-F]{3,8}\b')
css = pattern.sub(lambda m: MAPPING.get(m.group().lower(), m.group()), css)
css_path.write_text(css, encoding='utf-8')
lab_path = ROOT/'assets/lab.css'
lab = lab_path.read_text()
lab = pattern.sub(lambda m: MAPPING.get(m.group().lower(), m.group()), lab)
if '/* School-blue palette.' not in lab:
    lab += EXTRA
lab_path.write_text(lab, encoding='utf-8')
source_path = ROOT/'tools/build_lab.py'
source = source_path.read_text().replace('content="#982b34"', 'content="#004890"')
source_path.write_text(source, encoding='utf-8')
notes_path = ROOT/'LAB-SITE.md'
notes = notes_path.read_text()
if '## Blue palette' not in notes:
    notes += '''\n## Blue palette\n\nThe primary colour is the owner-supplied `#004890`; `#017CC2` is the accent.\nMenu: `#00366B`. Research sections: `#005B91`. Footer: `#082E50`.\nLight sections: `#EEF5FA`. Main text: `#132B40`.\nThese are site design choices, not a separately verified institutional identity standard.\n\nChange the semantic colour tokens in `assets/site.css` for later adjustments.\nScreen-specific details are in the final palette block of `assets/lab.css`.\nThe original red/purple class names remain only as compatibility aliases.\nAll publication images, text, routes, typography and interactive behaviour are retained.\nThe single-file `preview.html` is rebuilt from the same blue site sources.\n'''
notes_path.write_text(notes, encoding='utf-8')
print('Applied the owner-supplied blue palette to both shared stylesheets and theme metadata.')
