"""Run browser checks against the local static site; write review screenshots."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect

out = Path('previews')
out.mkdir(exist_ok=True)
report = {'layouts': [], 'checks': [], 'errors': []}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.on('pageerror', lambda error: report['errors'].append(str(error)))
    for name in ['index.html', 'publications.html']:
        for width in [320, 390, 560, 768, 1024, 1440]:
            page.set_viewport_size({'width': width, 'height': 1000})
            page.goto('http://localhost:8000/' + name)
            page.evaluate('document.fonts.ready')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (name, width)
            for image in page.locator('img').all():
                assert image.evaluate('(image) => image.complete && image.naturalWidth > 0')
            report['layouts'].append([name, width, 'pass'])
        for width, label in [(1440, 'desktop'), (390, 'mobile')]:
            page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
            page.goto('http://localhost:8000/' + name)
            page.evaluate('document.fonts.ready')
            page.screenshot(path=str(out / f'{name[:-5]}-{label}.png'), full_page=True)
            if name == 'index.html' and width == 1440:
                page.screenshot(path=str(out / 'home-first-screen.png'))
                report['primary_font_loaded'] = page.evaluate('''() => [...document.fonts].some(f => f.family.includes('Manrope Reference') && f.status === 'loaded')''')
                assert report['primary_font_loaded'], 'Primary webfont did not load'
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.goto('http://localhost:8000/index.html')
    expect(page.locator('.resume-section')).to_have_count(7)
    expect(page.locator('.resume-section[open]')).to_have_count(0)
    for section in page.locator('.resume-section').all():
        section.locator('summary').click()
        expect(section.locator('.resume-content')).to_be_visible()
        section.locator('summary').click()
        expect(section.locator('.resume-content')).not_to_be_visible()
    report['checks'].append('All seven CV accordions open and close')
    page.locator('.menu-toggle').click()
    expect(page.locator('.menu-panel')).to_be_visible()
    page.screenshot(path=str(out / 'menu-desktop.png'))
    page.keyboard.press('Escape')
    expect(page.locator('.menu-panel')).not_to_be_visible()
    page.locator('.menu-toggle').click()
    page.locator('.menu-panel a[href="index.html#education"]').click()
    expect(page.locator('#education .resume-content')).to_be_visible()
    expect(page.locator('.menu-panel')).not_to_be_visible()
    report['checks'].append('Menu, Escape key, and section deep links')
    page.goto('http://localhost:8000/index.html')
    for section in page.locator('.resume-section').all():
        section.evaluate('(section) => { section.open = true; }')
    page.screenshot(path=str(out / 'home-expanded-desktop.png'), full_page=True)
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('.menu-toggle').click()
    expect(page.locator('.menu-panel')).to_be_visible()
    page.keyboard.press('Escape')
    expect(page.locator('.menu-panel')).not_to_be_visible()
    page.goto('http://localhost:8000/publications.html')
    expect(page.locator('.publication')).to_have_count(16)
    report['checks'].append('16 publications retained')
    for name in ['index.html', 'publications.html']:
        page.goto('http://localhost:8000/' + name)
        for href in page.locator('a[href]').evaluate_all('(links) => links.map(a => a.getAttribute("href"))'):
            if href.startswith(('http:', 'https:', 'mailto:', '#')):
                continue
            assert Path(href.split('#')[0]).is_file(), (name, href)
    report['checks'].append('All local file links resolve')
    nojs = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
    q = nojs.new_page()
    q.goto('http://localhost:8000/index.html')
    q.locator('#education summary').click()
    expect(q.locator('#education .resume-content')).to_be_visible()
    q.locator('.menu-toggle').click()
    expect(q.locator('.menu-panel')).to_be_visible()
    q.goto('http://localhost:8000/publications.html')
    expect(q.locator('.publication')).to_have_count(16)
    report['checks'].append('Menu, CV and publications remain usable without JavaScript')
    browser.close()
assert not report['errors'], report['errors']
(out / 'test-report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
