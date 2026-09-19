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
        check(page, '.section.purple', 'rgb(66, 13, 93)')
        check(page, '.gray', 'rgb(240, 240, 240)')
        check(page, '.feature-link[href*="research"]', 'rgb(27, 20, 100)')
        check(page, '.feature-link[href*="team"]', 'rgb(31, 75, 81)')
        check(page, '.feature-link[href*="publications"]', 'rgb(66, 13, 93)')
        check(page, '.site-footer', 'rgb(52, 58, 64)')
        check(page, 'body', 'rgb(0, 0, 0)', 'color')
        page.locator('.menu-toggle').click()
        check(page, '.menu-panel', 'rgb(66, 13, 93)')
        page.keyboard.press('Escape')
    for name in json.loads((ROOT / 'data/routes.json').read_text()):
        page.goto(BASE + name + '.html')
        selector = '.profile-background' if name == 'profile' else '.page-hero'
        check(page, selector, 'rgb(0, 72, 144)')
        check(page, '.site-footer', 'rgb(52, 58, 64)')
    page.goto(BASE + 'press.html')
    for i, colour in enumerate(['rgb(31, 75, 81)', 'rgb(66, 16, 91)',
                                'rgb(0, 72, 144)', 'rgb(27, 20, 100)', 'rgb(240, 240, 240)']):
        check(page, '.press-thumb.thumb-' + str(i), colour)
    page.locator('[data-press-filter="highlight"]').click()
    expect(page.locator('.press-row:visible')).to_have_count(3)
    check(page, '[data-press-filter="highlight"]', 'rgb(0, 72, 144)', 'color')
    report['checks'].append('Blue replaces red only; secondary and neutral roles remain separate.')
    page.goto(BASE + 'index.html')
    page.evaluate('document.fonts.ready')
    page.locator('.feature-grid').screenshot(path=str(OUT / 'palette-section-cards.png'))
    browser.close()
report['status'] = 'passed'
(OUT / 'palette-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
