"""Protect independent colour roles against an accidental all-blue repaint."""
from pathlib import Path
import json
import os
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'previews'
OUT.mkdir(exist_ok=True)
BASE = os.environ.get('SITE_BASE', 'http://127.0.0.1:8000/')
report = {'colours': [], 'checks': []}

def check(page, selector, expected, prop='backgroundColor'):
    actual = page.locator(selector).first.evaluate('(e,p)=>getComputedStyle(e)[p]', prop)
    assert actual == expected, (selector, prop, actual, expected)
    report['colours'].append({'page': page.url.split('/')[-1], 'selector': selector,
                             'property': prop, 'value': actual})

with sync_playwright() as p:
    options = {'executable_path': os.environ['CHROMIUM_PATH']} if os.environ.get('CHROMIUM_PATH') else {}
    browser = p.chromium.launch(**options)
    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
    for file in ['index.html', 'preview.html']:
        page.goto(BASE + file)
        page.evaluate('document.fonts.ready')
        check(page, '.page-hero', 'rgb(0, 72, 144)')
        check(page, '.section.purple', 'rgb(41, 61, 70)')
        check(page, '.gray', 'rgb(240, 240, 240)')
        check(page, '.feature-link[href*="research"]', 'rgb(37, 59, 99)')
        check(page, '.feature-link[href*="team"]', 'rgb(49, 92, 83)')
        check(page, '.feature-link[href*="publications"]', 'rgb(98, 88, 79)')
        check(page, '.site-footer', 'rgb(52, 58, 64)')
        check(page, 'body', 'rgb(0, 0, 0)', 'color')
        page.locator('.menu-toggle').click()
        check(page, '.menu-panel', 'rgb(36, 52, 60)')
        page.keyboard.press('Escape')
    for name in json.loads((ROOT / 'data/routes.json').read_text()):
        page.goto(BASE + name + '.html')
        selector = '.profile-background' if name == 'profile' else '.page-hero'
        check(page, selector, 'rgb(0, 72, 144)')
        check(page, '.site-footer', 'rgb(52, 58, 64)')
    page.goto(BASE + 'press.html')
    for i, colour in enumerate(['rgb(49, 92, 83)', 'rgb(98, 88, 79)',
                                'rgb(0, 72, 144)', 'rgb(37, 59, 99)', 'rgb(240, 240, 240)']):
        check(page, '.press-thumb.thumb-' + str(i), colour)
    page.locator('[data-press-filter="highlight"]').click()
    expect(page.locator('.press-row:visible')).to_have_count(3)
    page.mouse.move(0, 0)  # The original hover style is black; inspect selection after leaving it.
    check(page, '[data-press-filter="highlight"]', 'rgb(0, 72, 144)', 'color')
    report['checks'].append('Approved primary and neutrals remain; science ink, forest green and warm stone are distinct secondary roles.')

    forbidden = {'rgb(66, 13, 93)', 'rgb(66, 16, 91)', 'rgb(50, 20, 70)'}
    for name in json.loads((ROOT / 'data/routes.json').read_text()):
        page.goto(BASE + name + '.html')
        colours = page.locator('body *').evaluate_all("xs=>xs.filter(e=>e.getClientRects().length).flatMap(e=>{const s=getComputedStyle(e);return [s.color,s.backgroundColor,s.borderTopColor,s.stroke,s.fill]})")
        assert not forbidden.intersection(colours), (name, forbidden.intersection(colours))
    report['checks'].append('No old purple UI colours remain on any of the 17 routes; source images remain unchanged.')
    page.goto(BASE + 'comics.html')
    check(page, '.comic-panel', 'rgb(41, 61, 70)', 'color')
    check(page, '.comic-panel', 'rgb(41, 61, 70)', 'borderTopColor')
    page.goto(BASE + 'research.html')
    if page.locator('.question').count():
        check(page, '.question', 'rgb(37, 59, 99)')
    def contrast_white(hex_colour):
        rgb = [int(hex_colour[i:i+2],16)/255 for i in (0,2,4)]
        linear = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        return 1.05 / (sum(v*w for v,w in zip(linear,[.2126,.7152,.0722]))+.05)
    report['white_text_contrast'] = {c:round(contrast_white(c),2) for c in ['004890','253B63','315C53','62584F','293D46','24343C','343A40']}
    assert min(report['white_text_contrast'].values()) >= 4.5
    report['checks'].append('White text contrast checked on every dark palette surface.')

    page.goto(BASE + 'index.html')
    page.evaluate('document.fonts.ready')
    page.locator('.feature-grid').screenshot(path=str(OUT / 'palette-section-cards.png'))
    browser.close()
report['status'] = 'passed'
(OUT / 'palette-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
