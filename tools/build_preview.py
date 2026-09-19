"""Build a single-file preview with working page routes. Font files are never bundled."""
from pathlib import Path
import base64, json, mimetypes
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
NAMES=['index','vision','research','profile','publications','resources','news','contact']
def embed_images(soup):
    for image in soup.select('img[src]'):
        source=image['src']
        if not source.startswith(('https:','http:','data:')):
            path=ROOT/source
            if path.is_file():
                mime=mimetypes.guess_type(source)[0] or 'application/octet-stream'
                image['src']=f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()
doc=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
for el in doc.select('link[rel="canonical"],link[href="assets/site.css"],script[src="assets/site.js"]'):el.decompose()
style=doc.new_tag('style');style.string=(ROOT/'assets/site.css').read_text();doc.head.append(style)
content={}
for name in NAMES:
    page=BeautifulSoup((ROOT/f'{name}.html').read_text(),'html.parser');embed_images(page)
    content[name]={'title':page.title.get_text(),'body':page.main.decode_contents()}
embed_images(doc)
warning=doc.new_tag('div',id='preview-font-warning',attrs={'class':'preview-font-warning','role':'status','hidden':''})
warning.string='웹폰트를 불러오지 못해 대체 글꼴로 표시 중입니다. 함께 제공한 화면 이미지는 Manrope 로딩 후 촬영했습니다.'
doc.body.append(warning);doc.body['data-preview']='true'
data=doc.new_tag('script',id='preview-pages',type='application/json');data.string=json.dumps(content,ensure_ascii=False).replace('</','<\\/');doc.body.append(data)
script=doc.new_tag('script');script.string=(ROOT/'assets/site.js').read_text();doc.body.append(script)
router=r'''
(() => {
  const pages=JSON.parse(document.getElementById('preview-pages').textContent);
  const main=document.getElementById('main');
  const pdf=new Blob([Uint8Array.from(atob('__CV__'),c=>c.charCodeAt(0))],{type:'application/pdf'});
  const pdfURL=URL.createObjectURL(pdf);
  function prepare(){
    document.querySelectorAll('a[href]').forEach(a=>{
      const href=a.getAttribute('href');
      if(href==='CV_SeungjaeHan_0707.pdf'){a.href=pdfURL;a.target='_blank';a.rel='noopener';return;}
      const match=href.match(/^([\w-]+)\.html(?:#(.*))?$/);
      if(match&&pages[match[1]])a.setAttribute('href','#/'+match[1]+(match[2]?'/'+match[2]:''));
    });
  }
  function route(){
    const parts=location.hash.replace(/^#\//,'').split('/');
    const name=pages[parts[0]]?parts[0]:'index';
    main.innerHTML=pages[name].body;document.title=pages[name].title;document.body.dataset.page=name;
    const menu=document.querySelector('.navigation');if(menu)menu.open=false;
    prepare();
    if(parts[1])window.siteReveal(decodeURIComponent(parts.slice(1).join('/')));
    else window.scrollTo({top:0,behavior:'instant'});
  }
  document.addEventListener('click',e=>{
    if(!(e.target instanceof Element))return;
    const a=e.target.closest('a[href^="#/"]');
    if(a&&a.hash===location.hash){e.preventDefault();route();}
  });
  window.addEventListener('hashchange',()=>{if(location.hash.startsWith('#/'))route();});
  prepare();route();
})();
'''.replace('__CV__',base64.b64encode((ROOT/'CV_SeungjaeHan_0707.pdf').read_bytes()).decode())
script=doc.new_tag('script');script.string=router;doc.body.append(script)
(ROOT/'preview.html').write_text(str(doc))
print('Built preview.html with eight page routes; no font binaries embedded.')
