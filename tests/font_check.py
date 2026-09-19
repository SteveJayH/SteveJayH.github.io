"""Check the rendered webfont, not only CSS font-family declarations."""
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

REFERENCE = 'https://www.rajanlab.com/kanaka-rajan'
FONT_FILE = '667a13fe587f6a3229bc0dd5_Manrope-VariableFont_wght.ttf'
OUT = Path('previews')
OUT.mkdir(exist_ok=True)
STYLE = '''(el) => { const s = getComputedStyle(el); return Object.fromEntries(
  ['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing'].map(k => [k,s[k]])); }'''
PAINT = '''([family, weight, size, text]) => {
  const c = document.createElement('canvas'); c.width = 1800; c.height = 130;
  const x = c.getContext('2d'); x.fillStyle = '#000';
  x.font = `${weight} ${size} ${family}`; x.fillText(text, 12, 90);
  return c.toDataURL('image/png');
}'''

def actual_fonts(page, selector):
    session = page.context.new_cdp_session(page)
    try:
        session.send('DOM.enable')
        session.send('CSS.enable')
        root = session.send('DOM.getDocument')['root']['nodeId']
        node = session.send('DOM.querySelector', {'nodeId': root, 'selector': selector})['nodeId']
        fonts = session.send('CSS.getPlatformFontsForNode', {'nodeId': node})['fonts']
        assert fonts and all(f['isCustomFont'] and 'manrope' in f['familyName'].lower() for f in fonts), fonts
        return fonts
    finally:
        session.detach()

report = {'reference': REFERENCE, 'font_asset': FONT_FILE, 'sizes': [], 'glyphs': []}
with sync_playwright() as p:
    browser = p.chromium.launch()
    ref = browser.new_page(viewport={'width': 1440, 'height': 1000})
    ref.goto(REFERENCE, wait_until='domcontentloaded', timeout=60000)
    ref.evaluate('document.fonts.ready')
    report['reference_fonts'] = actual_fonts(ref, 'h1')
    ref.screenshot(path=str(OUT / 'font-reference-desktop.png'))
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    page.goto('http://localhost:8000/index.html')
    page.evaluate('document.fonts.ready')
    faces = page.evaluate('''() => [...document.fonts].map(f => ({family:f.family, status:f.status, weight:f.weight}))''')
    assert any('Manrope Reference' in f['family'] and f['status'] == 'loaded' for f in faces), faces
    report['site_fonts'] = actual_fonts(page, 'h1')
    requests = page.evaluate('performance.getEntriesByType("resource").map(e => e.name)')
    assert any(FONT_FILE in url for url in requests), requests
    # Affiliation and biography are different paragraphs with different sizes.
    pairs = [('h1', 'h1', 'Seungjae Han, PhD'),
             ('.member-content p.text-size-medium', '.affiliation', 'Postdoctoral Fellow, KAIST'),
             ('.member-content .w-richtext p', '.profile-description > p', 'Computational neuroscience and fluorescence microscopy.'),
             ('h3.text-accordion', '.resume-section > summary h2', 'Professional appointments')]
    for old, new, text in pairs:
        a = ref.locator(old).first.evaluate(STYLE)
        b = page.locator(new).first.evaluate(STYLE)
        for key in ['fontSize','fontWeight','lineHeight','letterSpacing']:
            assert a[key] == b[key], (old, key, a, b)
        before = ref.evaluate(PAINT, [a['fontFamily'],a['fontWeight'],a['fontSize'],text])
        after = page.evaluate(PAINT, [b['fontFamily'],b['fontWeight'],b['fontSize'],text])
        assert before == after, ('different glyph raster', old)
        report['glyphs'].append({'selector':new, 'matched_reference':True, 'style':b,
                                'raster_sha256':hashlib.sha256(after.encode()).hexdigest()})
    # Record whether the previous Google Fonts font actually has different outlines.
    # Do not infer a visual difference merely from two different font URLs.
    page.evaluate('document.fonts.load(\'300 50px "Manrope"\')')
    google = page.evaluate(PAINT, ['"Manrope"', '300', '50px', 'Seungjae Han, PhD'])
    exact = page.evaluate(PAINT, ['"Manrope Reference"', '300', '50px', 'Seungjae Han, PhD'])
    report['previous_google_headline_raster_equal'] = google == exact
    for width in [390, 768, 820, 991, 1024, 1100, 1440]:
        ref.set_viewport_size({'width':width,'height':1000})
        page.set_viewport_size({'width':width,'height':1000})
        a = ref.locator('h1').evaluate(STYLE)
        b = page.locator('h1').evaluate(STYLE)
        assert all(a[k] == b[k] for k in ['fontSize','fontWeight','lineHeight','letterSpacing']), (width,a,b)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
        if width >= 768:
            heading = page.locator('.profile-heading').bounding_box()
            band = page.locator('.profile-background').bounding_box()
            assert heading['y'] + heading['height'] <= band['y'] + band['height'], (width,heading,band)
        report['sizes'].append({'width':width,'title':b})
    for width, name in [(1440,'desktop'),(1024,'tablet'),(390,'mobile')]:
        page.set_viewport_size({'width':width,'height':1000 if width > 390 else 844})
        page.screenshot(path=str(OUT / f'font-{name}.png'))
    page.set_viewport_size({'width':1440,'height':1000})
    page.locator('.profile-heading').screenshot(path=str(OUT / 'font-heading-detail.png'))
    webkit = p.webkit.launch()
    q = webkit.new_page(viewport={'width':390,'height':844})
    q.goto('http://localhost:8000/index.html')
    q.evaluate('document.fonts.ready')
    assert q.evaluate('''() => [...document.fonts].some(f => f.family.includes('Manrope Reference') && f.status === 'loaded')''')
    assert q.evaluate('document.documentElement.scrollWidth <= innerWidth')
    q.screenshot(path=str(OUT / 'font-mobile-webkit.png'))
    report['webkit_font_loaded'] = True
    webkit.close()
    browser.close()
(OUT / 'font-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
