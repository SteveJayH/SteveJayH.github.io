"""Check the full lab site, preview router, menus, content filters and rendered font."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'previews'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:8000/'
ROUTES = json.loads((ROOT/'data/routes.json').read_text())
report = {'routes':ROUTES,'layouts':[],'checks':[],'errors':[]}
for name in ROUTES:
    file=ROOT/(name+'.html')
    doc=BeautifulSoup(file.read_text(),'html.parser')
    assert len(doc.select('h1'))==1, name
    assert len(doc.select('#site-navigation .menu-grid > div'))==4,name
    for a in doc.select('a[href]'):
        url=urlsplit(a['href'])
        if url.scheme or url.netloc: continue
        path=(ROOT/unquote(url.path)) if url.path else file
        assert path.is_file(),(name,a['href'])
        if url.fragment and path.suffix=='.html':
            target=BeautifulSoup(path.read_text(),'html.parser')
            assert target.find(id=unquote(url.fragment)),(name,a['href'])
report['checks'].append('All local file links and fragment targets exist')

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000})
    page.on('pageerror',lambda error: report['errors'].append(str(error)))
    for name in ROUTES:
        page.goto(BASE+name+'.html',wait_until='networkidle')
        page.evaluate('document.fonts.ready')
        page.evaluate('async()=>{await Promise.all([...document.images].map(i=>{i.loading="eager";return i.decode().catch(()=>{});}));}')
        assert page.evaluate('document.fonts.check(\'300 50px "Manrope"\')'),name
        for w in [320,390,768,1024,1440]:
            page.set_viewport_size({'width':w,'height':1000})
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(name,w)
            report['layouts'].append([name,w,'pass'])
        page.screenshot(path=str(OUT/(name+'-desktop.png')),full_page=True)
        page.screenshot(path=str(OUT/(name+'-first.png')))
        page.set_viewport_size({'width':390,'height':844})
        page.screenshot(path=str(OUT/(name+'-mobile.png')),full_page=True)
        assert page.locator('img').evaluate_all('(xs)=>xs.every(i=>i.complete&&i.naturalWidth>0)'),name
    page.set_viewport_size({'width':1440,'height':1000})
    page.goto(BASE+'index.html')
    page.locator('.menu-toggle').click()
    expect(page.locator('#site-navigation')).to_be_visible()
    page.screenshot(path=str(OUT/'menu-desktop.png'))
    page.keyboard.press('Escape')
    expect(page.locator('#site-navigation')).not_to_be_visible()
    page.goto(BASE+'press.html')
    for mode,count in [('highlight',3),('commentary',1),('coverage',1),('all',5)]:
        page.locator('[data-press-filter="'+mode+'"]').click()
        expect(page.locator('.press-row:visible')).to_have_count(count)
    report['checks'].append('Press filters: 5 source-linked records')
    page.goto(BASE+'publications.html')
    expect(page.locator('.publication')).to_have_count(16)
    page.locator('#paper-year').select_option('2025')
    expect(page.locator('.publication:visible')).to_have_count(3)
    page.locator('#paper-year').select_option('all')
    expect(page.locator('.publication:visible')).to_have_count(16)
    page.goto(BASE+'profile.html')
    for i in range(7):
        item=page.locator('.resume-section').nth(i)
        item.locator('summary').click();expect(item).to_have_attribute('open','')
        item.locator('summary').click();expect(item).not_to_have_attribute('open','')
    page.goto(BASE+'faq.html')
    expect(page.locator('.faq-item')).to_have_count(9)
    page.locator('.faq-item summary').first.click()
    expect(page.locator('.faq-answer').first).to_be_visible()
    page.goto(BASE+'comics.html')
    expect(page.locator('.comic-panel')).to_have_count(8)
    report['checks'].append('16 publications, 7 profile accordions, 9 FAQs, 8 comic panels')
    # Confirm the actual rendered font rather than only the CSS declaration.
    page.goto(BASE+'profile.html')
    page.evaluate('document.fonts.ready')
    session=page.context.new_cdp_session(page)
    session.send('DOM.enable');session.send('CSS.enable')
    root=session.send('DOM.getDocument')['root']['nodeId']
    node=session.send('DOM.querySelector',{'nodeId':root,'selector':'h1'})['nodeId']
    fonts=session.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
    assert fonts and all(f['isCustomFont'] and 'manrope' in f['familyName'].lower() for f in fonts),fonts
    report['rendered_font']=fonts
    session.detach()
    ref=browser.new_page(viewport={'width':1440,'height':1000})
    ref.goto('https://www.rajanlab.com/kanaka-rajan',wait_until='networkidle')
    ref.evaluate('document.fonts.ready')
    style='el=>{const s=getComputedStyle(el);return [s.fontFamily,s.fontSize,s.fontWeight,s.lineHeight,s.letterSpacing]}'
    a=ref.locator('h1').evaluate(style);b=page.locator('h1').evaluate(style)
    assert a[1:]==b[1:],(a,b)
    paint='''family=>{const c=document.createElement('canvas');c.width=850;c.height=100;const x=c.getContext('2d');x.font='300 50px '+family;x.fillText('Seungjae Han, PhD',10,70);return c.toDataURL()}'''
    assert ref.evaluate(paint,a[0])==page.evaluate(paint,b[0])
    report['reference_profile_type_match']=True
    ref.close()
    # Single-file preview: use every route, then click real menu links.
    page.goto(BASE+'preview.html')
    for name in ROUTES:
        page.evaluate('(name)=>location.hash="/"+name',name)
        page.wait_for_function('(name)=>document.body.dataset.page===name',arg=name)
        expect(page.locator('h1')).to_have_count(1)
        assert page.locator('main').inner_text().strip(),name
    page.locator('.menu-toggle').click()
    page.locator('#site-navigation').get_by_role('link',name='Our Science',exact=True).click()
    expect(page.locator('h1')).to_have_text('Our Science')
    page.locator('.menu-toggle').click()
    page.locator('#site-navigation').get_by_role('link',name='Press',exact=True).click()
    expect(page.locator('h1')).to_have_text('Press')
    page.go_back();expect(page.locator('h1')).to_have_text('Our Science')
    page.evaluate('location.hash="/profile/education"')
    page.wait_for_function('document.body.dataset.page==="profile"')
    expect(page.locator('#education')).to_have_attribute('open','')
    assert page.get_by_role('link',name='Curriculum vitae',exact=True).first.get_attribute('href').startswith('blob:')
    report['checks'].append('All 17 preview routes, menu clicks, browser back, CV and deep links')
    # The actual static pages remain navigable without JavaScript.
    nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    q=nojs.new_page();q.goto(BASE+'index.html')
    q.locator('.menu-toggle').click()
    q.locator('#site-navigation').get_by_role('link',name='Comp Neuro FAQs').click()
    q.locator('.faq-item summary').first.click()
    expect(q.locator('.faq-answer').first).to_be_visible()
    q.goto(BASE+'publications.html');expect(q.locator('.publication:visible')).to_have_count(16)
    report['checks'].append('Static navigation and reading work without JavaScript')
    nojs.close();browser.close()
assert not report['errors'],report['errors']
report['status']='passed'
(OUT/'lab-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
