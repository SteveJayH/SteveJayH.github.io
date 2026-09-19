"""Check all pages, local links, native navigation, and single-file preview routes."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from playwright.sync_api import sync_playwright
import json,traceback
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews';OUT.mkdir(exist_ok=True)
BASE='http://localhost:8000/'
PAGES=['index','vision','research','profile','publications','resources','news','contact']
report={'layouts':[],'routes':[],'local_links':[],'errors':[]}
try:
    with sync_playwright() as p:
        browser=p.chromium.launch()
        page=browser.new_page(viewport={'width':1440,'height':1000})
        page.on('pageerror',lambda e:report['errors'].append(str(e)))
        checked=set()
        for name in PAGES:
            page.goto(BASE+name+'.html',wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
            assert page.locator('main h1').count()==1,name
            assert page.locator('a[href="#"]').count()==0,name
            for href in page.locator('a[href]').evaluate_all('es=>es.map(e=>e.getAttribute("href"))'):
                u=urlsplit(href)
                if u.scheme or u.netloc:continue
                target=(ROOT/u.path) if u.path else ROOT/(name+'.html')
                assert target.is_file(),(name,href)
                if u.path and u.path not in checked:
                    assert page.request.get(BASE+u.path).ok,href
                    checked.add(u.path)
                if u.fragment:assert f'id="{unquote(u.fragment)}"' in target.read_text(),(name,href)
            for width in [320,390,560,768,820,991,1024,1440]:
                page.set_viewport_size({'width':width,'height':1000})
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(name,width)
                report['layouts'].append([name,width,'pass'])
            page.set_viewport_size({'width':1440,'height':1000})
            for img in page.locator('main img').all():
                img.scroll_into_view_if_needed();img.evaluate('(img)=>img.decode()')
            page.evaluate('window.scrollTo({top:0,behavior:"instant"})')
            page.screenshot(path=str(OUT/(name+'-desktop.png')),full_page=True)
            if name in ['index','profile','research']:
                page.screenshot(path=str(OUT/(name+'-first-screen.png')))
                page.set_viewport_size({'width':390,'height':844})
                page.screenshot(path=str(OUT/(name+'-mobile.png')),full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        for name in PAGES:
            page.goto(BASE+'index.html');page.locator('.menu-toggle').click()
            if name=='index':page.screenshot(path=str(OUT/'menu-desktop.png'))
            page.locator(f'.menu-panel a[href="{name}.html"]').first.click()
            page.wait_for_url('**/'+name+'.html')
            assert page.locator('main h1').is_visible()
            report['routes'].append(['native',name,'pass'])
        page.goto(BASE+'profile.html')
        assert page.locator('.resume-section').count()==7
        for summary in page.locator('.resume-section > summary').all():
            summary.click();assert summary.locator('..').get_attribute('open') is not None;summary.click()
        page.goto(BASE+'profile.html#education');assert page.locator('#education').get_attribute('open') is not None
        page.goto(BASE+'publications.html');assert page.locator('.publication').count()==16
        page.locator('#paper-year').select_option('2025');assert page.locator('.publication:visible').count()==3
        page.locator('#paper-year').select_option('all');assert page.locator('.publication:visible').count()==16
        page.goto(BASE+'research.html')
        for target in ['denoising','calcium','learning']:
            page.locator(f'.question[href="research.html#{target}"]').click();assert page.locator('#'+target).is_visible()
        page.goto(BASE+'preview.html')
        for name in PAGES:
            page.locator('.menu-toggle').click()
            page.locator(f'.menu-panel a[href="#/{name}"]').first.click()
            page.wait_for_function('(name)=>document.body.dataset.page===name',arg=name)
            assert page.locator('main h1').is_visible()
            assert page.locator('a[href$=".html"]').count()==0
            report['routes'].append(['preview',name,'pass'])
        page.go_back();page.wait_for_function('document.body.dataset.page==="news"')
        page.goto(BASE+'preview.html#/profile/education');assert page.locator('#education').get_attribute('open') is not None
        page.goto(BASE+'preview.html#/publications')
        page.locator('#paper-year').select_option('2025');assert page.locator('.publication:visible').count()==3
        page.goto(BASE+'preview.html#/publications/support');assert page.locator('#support').is_visible()
        page.locator('.menu-toggle').click();page.keyboard.press('Escape');assert page.locator('.navigation').get_attribute('open') is None
        ctx=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        q=ctx.new_page();q.goto(BASE+'index.html');q.locator('.menu-toggle').click()
        q.locator('.menu-panel a[href="research.html"]').click();assert q.locator('main h1').is_visible()
        q.goto(BASE+'profile.html');q.locator('#education summary').click();assert q.locator('#education .resume-content').is_visible()
        q.goto(BASE+'publications.html');assert q.locator('.publication:visible').count()==16
        report['local_links']=sorted(checked)
        assert not report['errors'],report['errors']
        browser.close()
    report['status']='passed'
except Exception:
    report['status']='failed';report['failure']=traceback.format_exc()
    raise
finally:(OUT/'test-report.json').write_text(json.dumps(report,indent=2))
print('Passed',len(report['layouts']),'layout cases and',len(report['routes']),'page transitions.')
