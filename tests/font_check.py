"""Verify actual rendered Manrope and match the reference's typography."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import hashlib,json,traceback
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'previews';OUT.mkdir(exist_ok=True)
BASE='http://localhost:8000/'
REFERENCE='https://www.rajanlab.com/kanaka-rajan'
STYLE='''el=>{const s=getComputedStyle(el);return Object.fromEntries(['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing'].map(k=>[k,s[k]]))}'''
PAINT='''([f,w,s,t])=>{const c=document.createElement('canvas');c.width=1400;c.height=120;const x=c.getContext('2d');x.font=`${w} ${s} ${f}`;x.fillText(t,10,85);return c.toDataURL()}'''
def fonts(page,selector):
    c=page.context.new_cdp_session(page)
    try:
        c.send('DOM.enable');c.send('CSS.enable');root=c.send('DOM.getDocument')['root']['nodeId']
        node=c.send('DOM.querySelector',{'nodeId':root,'selector':selector})['nodeId']
        fs=c.send('CSS.getPlatformFontsForNode',{'nodeId':node})['fonts']
        assert fs and all(f['isCustomFont'] and 'manrope' in f['familyName'].lower() for f in fs),fs
        return fs
    finally:c.detach()
report={'source':REFERENCE,'matches':[],'rendered_fonts':{}}
try:
    with sync_playwright() as p:
        browser=p.chromium.launch()
        ref=browser.new_page(viewport={'width':1440,'height':1000})
        ref.goto(REFERENCE,wait_until='domcontentloaded');ref.evaluate('document.fonts.ready')
        page=browser.new_page(viewport={'width':1440,'height':1000})
        page.goto(BASE+'profile.html');page.evaluate('document.fonts.ready')
        report['reference_fonts']=fonts(ref,'h1')
        for before,after,text in [('h1','h1','Seungjae Han, PhD'),('.wrap-kanaka-title .text-size-medium','.affiliation','School of Electrical Engineering, KAIST'),('.member-content .w-richtext p','.profile-description > p','Computational neuroscience and fluorescence microscopy.'),('h3.text-accordion','.resume-section h2','Professional appointments')]:
            a=ref.locator(before).first.evaluate(STYLE);b=page.locator(after).first.evaluate(STYLE)
            assert all(a[k]==b[k] for k in ['fontSize','fontWeight','lineHeight','letterSpacing']),(before,a,b)
            aa=ref.evaluate(PAINT,[a['fontFamily'],a['fontWeight'],a['fontSize'],text]);bb=page.evaluate(PAINT,[b['fontFamily'],b['fontWeight'],b['fontSize'],text])
            assert aa==bb,('Glyphs differ',before)
            report['matches'].append({'element':after,'style':b,'glyphs_match':True,'sha256':hashlib.sha256(bb.encode()).hexdigest()})
        for name in ['index','vision','research','profile','publications','resources','news','contact','preview']:
            page.goto(BASE+name+'.html');page.evaluate('document.fonts.ready')
            report['rendered_fonts'][name]=fonts(page,'h1')
            page.wait_for_function('document.documentElement.dataset.fontStatus==="loaded"')
        for width in [390,768,820,991,1024,1440]:
            page.goto(BASE+'profile.html');page.set_viewport_size({'width':width,'height':1000});ref.set_viewport_size({'width':width,'height':1000})
            a=ref.locator('h1').evaluate(STYLE);b=page.locator('h1').evaluate(STYLE)
            assert all(a[k]==b[k] for k in ['fontSize','fontWeight','lineHeight','letterSpacing']),(width,a,b)
        sample=browser.new_page(viewport={'width':820,'height':242},device_scale_factor=1)
        sample.set_content('<link rel="stylesheet" href="'+BASE+'assets/site.css"><style>body{margin:0}section{background:#982b34;color:white;height:208px;padding:28px 0 0 80px}h1{font:300 50px/60px Manrope}p{margin:24px 0 0;font:400 18px/27px Manrope}</style><section><h1>Kanaka Rajan, PhD</h1><p>Associate Professor of Neurobiology<br>Founding Faculty, Kempner Institute for the Study of Natural and Artificial Intelligence<br>Harvard Medical School, Harvard University</p></section>')
        sample.evaluate('document.fonts.ready');fonts(sample,'h1');sample.screenshot(path=str(OUT/'manrope-sample.png'))
        blocked=browser.new_context();blocked.route('**/*.ttf',lambda route:route.abort())
        b=blocked.new_page();b.goto(BASE+'preview.html');b.wait_for_function('document.documentElement.dataset.fontStatus==="fallback"')
        assert b.locator('#preview-font-warning').is_visible()
        report['fallback_disclosed']=True;browser.close()
    report['status']='passed'
except Exception:
    report['status']='failed';report['failure']=traceback.format_exc();raise
finally:(OUT/'font-report.json').write_text(json.dumps(report,indent=2))
print('Actual Manrope verified on eight pages and the multipage preview.')
