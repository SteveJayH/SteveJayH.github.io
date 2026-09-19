"""Restore the multi-hue palette; substitute only the former red highlight."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = 'f814dcbf5b1e2140c9b70fa47ad5ae129d541051'
ROUTES = json.loads((ROOT / 'data/routes.json').read_text())
before = {name: (ROOT / (name + '.html')).read_bytes() for name in ROUTES}
report = {'baseline': BASE, 'replacement': {'#982b34': '#004890'}, 'styles': {}}
for name in ['assets/site.css', 'assets/lab.css']:
    original = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=ROOT, text=True)
    revised, count = re.subn(r'#982b34\b', '#004890', original, flags=re.I)
    assert count > 0, name
    (ROOT / name).write_text(revised)
    report['styles'][name] = {'red_substitutions': count,
        'all_other_css_unchanged_from_baseline': True,
        'sha256': hashlib.sha256(revised.encode()).hexdigest()}

doc = ROOT / 'LAB-SITE.md'
text = doc.read_text().split('## Blue palette')[0].rstrip()
text += '''

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
'''
doc.write_text(text)
subprocess.run([sys.executable, str(ROOT / 'tools/build_preview.py')], cwd=ROOT, check=True)
assert all((ROOT / (n + '.html')).read_bytes() == b for n, b in before.items())
report['static_pages_unchanged'] = len(before)
(ROOT / 'previews').mkdir(exist_ok=True)
(ROOT / 'previews/palette-source-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
