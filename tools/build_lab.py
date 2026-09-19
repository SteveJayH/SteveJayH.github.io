"""Build the complete lab site. Only verified people and source-linked coverage are used.

Han Lab is a provisional site name, not a claim of a current independent appointment.
Font binaries are never copied into the repository or the review bundle.
"""
from pathlib import Path
from html import escape
import json, re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
E = escape
FONT = 'https://cdn.prod.website-files.com/667a10df2ea8d55c5f903748/667a13fe587f6a3229bc0dd5_Manrope-VariableFont_wght.ttf'
SCHOLAR = 'https://scholar.google.com/citations?hl=en&user=AkzytG8AAAAJ'
EMAIL = 'mailto:jay0118@kaist.ac.kr'
SUPPORT = 'https://www.nature.com/articles/s41592-023-02005-8'
MEMRISTOR = 'https://www.nature.com/articles/s41928-024-01318-6'
REALS = 'https://doi.org/10.1109/WACV56688.2023.00198'
UBSN = 'https://doi.org/10.1109/WACV61041.2025.00135'
CODE = 'https://github.com/NICALab/SUPPORT'
ZENODO = 'https://zenodo.org/records/8176722'
BIO = 'https://nica.kaist.ac.kr/people'
FIGURE = 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41592-023-02005-8/MediaObjects/41592_2023_2005_Fig1_HTML.png'

ARROW = '<span class="arrow"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 13 13 3M3 3h10v10"/></svg></span>'
MARK = '<svg class="lab-mark" viewBox="0 0 42 42" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.2"><path d="M5 9h32M5 21h32M5 33h32M9 5v32M21 5v32M33 5v32"/><circle cx="9" cy="9" r="4"/><circle cx="33" cy="9" r="4"/><circle cx="21" cy="21" r="4"/><circle cx="9" cy="33" r="4"/><circle cx="33" cy="33" r="4"/></g></svg>'

def link(text, href, cls='text-link'):
    ext = ' target="_blank" rel="noopener noreferrer"' if href.startswith('http') else ''
    return f'<a class="{cls}" href="{E(href,quote=True)}"{ext}>{text}{ARROW}</a>'

def brand():
    return f'<a class="lab-brand" href="index.html" aria-label="Han Lab home">{MARK}<span><span class="brand-name"><strong>HAN</strong> LAB</span><small>COMPUTATIONAL NEUROSCIENCE &amp; IMAGING</small></span></a>'

GROUPS = [
 ('Research','From imaging data to neural signals.', [('Our Science','research.html'),('Publications','publications.html'),('Funding','funding.html'),('Resources','resources.html'),('GitHub','https://github.com/SteveJayH')]),
 ('People','The people behind the research.', [('Our Team','team.html'),('Seungjae Han, PhD','profile.html')]),
 ('Broader Impacts','Sharing the science and its methods.', [('Press','press.html'),('Comics','comics.html'),('Comp Neuro FAQs','faq.html'),('News','news.html')]),
 ('Work With Us','Research conversations and collaboration.', [('Join Us','join-us.html'),('Contact','contact.html')])]

def header():
    groups = ''.join(f'<div><h2>{h}</h2><p class="menu-description">{d}</p>'+''.join(link(t,u) for t,u in links)+'</div>' for h,d,links in GROUPS)
    return f'''<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="container navigation-bar">{brand()}<details class="navigation"><summary class="menu-toggle" aria-label="Navigation menu" aria-controls="site-navigation"><span class="menu-lines" aria-hidden="true"><i></i><i></i><i></i></span></summary><nav class="menu-panel" id="site-navigation" aria-label="Main navigation"><div class="container menu-grid">{groups}</div></nav></details></div></header>'''

FOOTER_LINKS=[('Our Science','research.html'),('People','team.html'),('Publications','publications.html'),('Press','press.html'),('Resources','resources.html'),('Join Us','join-us.html'),('Funding','funding.html'),('Contact','contact.html'),('Comics','comics.html'),('FAQs','faq.html')]
def footer():
    links=''.join(f'<a href="{u}">{t}</a>' for t,u in FOOTER_LINKS)
    return f'''<footer class="site-footer"><div class="container footer-grid"><div>{brand()}<p>Computational neuroscience<br>Self-supervised learning<br>Fluorescence microscopy</p></div><nav class="footer-pages" aria-label="Footer navigation">{links}</nav><div class="footer-links">{link('Email',EMAIL)}{link('Google Scholar',SCHOLAR)}{link('GitHub','https://github.com/SteveJayH')}<a href="profile.html">Seungjae Han · KAIST</a></div></div></footer>'''

def hero(title, description='', label='', extra='', cls=''):
    label_html=f'<p class="eyebrow">{label}</p>' if label else ''
    desc_html=f'<p class="hero-description">{description}</p>' if description else ''
    return f'<section class="page-hero {cls}"><div class="container"><div class="hero-copy">{label_html}<h1>{title}</h1>{desc_html}{extra}</div></div></section>'

def section(body, cls='', id=''):
    identity=f' id="{id}"' if id else ''
    return f'<section class="section {cls}"{identity}><div class="container">{body}</div></section>'

def cta(title, description, href, text='Learn More', cls='purple'):
    return section(f'<div class="wide-cta"><div><h2>{title}</h2><p>{description}</p></div>{link(text,href,"button-link")}</div>',cls)

def tiles(items):
    return '<div class="feature-grid">'+''.join(f'<a class="feature-link {c}" href="{u}"><h2>{t}</h2><p>{d}</p>{ARROW}</a>' for t,d,u,c in items)+'</div>'

def figure():
    src='assets/support-figure.png' if (ROOT/'assets/support-figure.png').exists() else FIGURE
    return f'<figure class="science-figure"><img src="{src}" width="1200" height="1100" loading="lazy" alt="Published SUPPORT network architecture and denoising examples."><figcaption>Eom, Han, Park et al., <a href="{SUPPORT}" target="_blank" rel="noopener">Nature Methods (2023), Fig. 1</a>. <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">CC BY 4.0</a>. Unmodified.</figcaption></figure>'

def illustration(mode='signals', invert=False):
    """Original vector schematics: decorative, not experimental measurements."""
    if mode=='signals':
        paths=''.join(f'<path d="M30 {y}h48l9 -12 9 24 9 -12h56l8 -9 8 18 8 -9h42l10 -38 8 67 8 -29h72l9 -13 9 26 9 -13h82"/>' for y in [110,160,210,260])
        inner=f'<g stroke="currentColor" stroke-width="1.8" fill="none">{paths}</g><g fill="currentColor"><circle cx="246" cy="72" r="4"/><circle cx="246" cy="122" r="4"/><circle cx="246" cy="172" r="4"/><circle cx="246" cy="222" r="4"/></g><rect x="219" y="55" width="58" height="250" fill="none" stroke="currentColor" stroke-dasharray="3 7"/>'
    elif mode=='pixels':
        squares=''.join(f'<rect x="{70+x*48}" y="{35+y*48}" width="36" height="36" rx="0" fill="currentColor" opacity="{.15+((x*7+y*3)%8)/10}"/>' for y in range(6) for x in range(7) if (x,y)!=(3,3))
        inner=squares+'<rect x="214" y="179" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2"/><path d="M225 197h14m-7-7v14" stroke="currentColor" stroke-width="2"/>'
    elif mode=='motion':
        inner='<g fill="none" stroke="currentColor" stroke-width="2"><rect x="85" y="60" width="210" height="210"/><rect x="115" y="80" width="210" height="210" opacity=".5"/><rect x="145" y="100" width="210" height="210" opacity=".25"/><circle cx="155" cy="145" r="26"/><circle cx="240" cy="210" r="20"/><path d="M335 160h90m-18-18 18 18-18 18"/></g>'
    else:
        inner=''.join(f'<path d="M{90+i*38} 45v270M60 {70+i*38}h350" stroke="currentColor" stroke-width="1.5" opacity=".55"/>' for i in range(7))
        inner+=''.join(f'<rect x="{82+x*38}" y="{62+y*38}" width="16" height="16" fill="currentColor" opacity="{.25+((x+y*2)%4)*.2}"/>' for y in range(7) for x in range(7))
    return f'<div class="science-art {"inverse" if invert else ""}"><svg viewBox="0 0 480 350" role="img" aria-label="Conceptual illustration of {mode}; not experimental data">{inner}</svg></div>'

# Source records are editable separately after the first build.
PRESS = [
 {'date':'2025-02-27','publisher':'KAIST Breakthroughs','type':'highlight','title':'An analog computing chip that corrects its own errors','description':'A research feature on the self-calibrating memristor platform.','url':'https://breakthroughs.kaist.ac.kr/sub02/view/page/1/id/4062','project':'computing.html'},
 {'date':'2025-02-11','publisher':'Nature Electronics','type':'commentary','title':'Video processing on a self-calibrating analogue memristor array','description':'News & Views by Muhammad Umair Khan and Baker Mohammad.','url':'https://www.nature.com/articles/s41928-025-01341-1','project':'computing.html'},
 {'date':'2025-01-23','publisher':'KAIST Electrical Engineering','type':'highlight','title':'A neuromorphic chip that learns and corrects itself','description':'KAIST research news on the joint work of the Choi and Yoon groups.','url':'https://ee.kaist.ac.kr/en/research-achieve/ee-prof-shinhyun-choi-and-young-gyu-yoons-joint-research-team-develops-neuromorphic-semiconductor-chip-that-learns-and-corrects-itself/','project':'computing.html'},
 {'date':'2025-01-21','publisher':'ScienceDaily','type':'coverage','title':'Neuromorphic semiconductor chip that learns and corrects itself?','description':'A ScienceDaily report sourced from the KAIST press release.','url':'https://www.sciencedaily.com/releases/2025/01/250121125920.htm','project':'computing.html'},
 {'date':'2024-02-26','publisher':'KAIST Breakthroughs','type':'highlight','title':'SUPPORT enables accurate optical readout of voltage signals in neurons','description':'A feature on self-supervised denoising of fluorescence recordings.','url':'https://breakthrough.kaist.ac.kr/sub03/view/id/497','project':'imaging.html'}]
if not (DATA/'press.json').exists(): (DATA/'press.json').write_text(json.dumps(PRESS,indent=2),encoding='utf-8')
PRESS=json.loads((DATA/'press.json').read_text())

def press_rows(records):
    out=[]
    for i,item in enumerate(records):
        date=item['date']; y,m,d=date.split('-'); month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m)-1]
        out.append(f'<article class="press-row" data-press-type="{item["type"]}"><div class="press-meta"><span>{E(item["publisher"])}</span><time datetime="{date}">{int(d)} {month} {y}</time></div><div><h2><a href="{E(item["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{E(item["title"])}</a></h2><p>{E(item["description"])}</p><div class="press-actions">{link("Read coverage",item["url"])}{link("Related research",item["project"])}</div></div></article>')
    return ''.join(out)

PAGES={}
PAGES['index']=('Home',
 hero('Understanding neural activity<br class="desktop-break"> through computation and imaging.',
      'Han Lab brings together self-supervised learning, statistical modelling, and fluorescence microscopy. The goal is to recover reliable neural signals from the data an experiment can actually collect.',
      extra=link('Our Science','research.html','button-link'),cls='lab-home-hero')+
 section('<div class="split"><div><p class="eyebrow">Vision</p><h2 class="section-title">Better images are a means to better measurements of the brain.</h2><p class="body-copy">We study how the design of a learning algorithm changes what can be measured in a neural recording. Acquisition, noise, and computation belong in the same conversation.</p>'+link('Our Vision','vision.html','button-link')+'</div>'+illustration('pixels')+'</div>',id='vision')+
 section('<div class="split">'+illustration('signals',True)+'<div><p class="eyebrow">Research</p><h2 class="section-title">Fast neural signals, moving specimens, and imperfect hardware each demand a different computational approach.</h2><p class="body-copy">Our research connects self-supervised denoising, calcium imaging analysis, and learning on analogue computing devices.</p>'+link('Explore the research','research.html','button-link')+'</div></div>','purple',id='research')+
 section('<p class="eyebrow">Impact</p><div class="impact-grid"><article><h2 class="section-title">Keep the biology in the signal.</h2><p>Methods are evaluated on the dynamics they recover, not just how smooth the resulting images look.</p>'+link('Imaging research','imaging.html')+'</article><article><h2 class="section-title">Make the methods usable.</h2><p>Published code, sample recordings, and documentation connect methodological work to experimental practice.</p>'+link('Open resources','resources.html')+'</article></div>','gray')+
 section('<div class="section-top"><div><p class="eyebrow">Broader Impacts</p><h2>In the press</h2></div>'+link('All press','press.html')+'</div>'+press_rows([PRESS[1],PRESS[-1]]))+
 section(tiles([('Our Science','Research themes and the methods behind them.','research.html',''),('People','Meet the researcher behind the programme.','team.html','teal'),('Publications','Articles, conference papers, and preprints.','publications.html','purple')]),'section-compact')+
 cta('Work with us','Explore the research, try the software, or start a scientific conversation.','join-us.html','Join Us'))

PAGES['vision']=('Vision',hero('Reliable measurements<br>of neural activity.','A research programme at the intersection of neuroscience, machine learning, and imaging.','Vision')+
 section('<div class="split"><div><p class="eyebrow">Our direction</p><h2>Start with the measurement.</h2><p class="body-copy">Neural recordings are shaped by the sensor, the preparation, and the signal being measured. Our research asks how those constraints should shape computational methods.</p><p class="body-copy">The programme connects work on voltage imaging, calcium imaging, and self-supervised video processing. The shared problem is recovering useful information when ideal training data or ideal hardware are unavailable.</p>'+link('Our Science','research.html','button-link')+'</div>'+illustration('pixels')+'</div>')+
 section('<div class="editorial-grid"><h2>Questions that guide the work</h2><div><article class="plain-entry"><h3>What information supports a prediction?</h3><p>Use spatial and temporal dependencies deliberately, and check which assumptions the data can support.</p></article><article class="plain-entry"><h3>What does the method preserve?</h3><p>Evaluate signal timing, amplitude, and residuals alongside image quality.</p></article><article class="plain-entry"><h3>Can someone else use the method?</h3><p>Connect the paper to working software, example data, and practical documentation.</p></article></div></div>','gray')+cta('From questions to methods','Explore three connected areas of research.','research.html','Our Science'))

THEMES=[('Self-supervised denoising','How can we recover fast neural signals without clean training images?','SUPPORT and multi-scale blind-spot networks for fluorescence microscopy.','imaging.html','pixels'),('Calcium imaging analysis','How can motion be separated from changes in neural activity?','Alignment, low-rank structure, and sparse signals in neural recordings.','calcium.html','motion'),('Learning and hardware','How can a learning system adapt to imperfect computing devices?','Self-supervised video processing and self-calibration on memristor arrays.','computing.html','hardware')]
PAGES['research']=('Our Science',hero('Our Science','Computational methods that connect how neural signals are recorded with how they are recovered.')+
 section('<div class="editorial-grid"><h2>Three connected<br>research directions</h2><p class="large-copy">Noise, motion, and hardware variation are not separate from the learning problem. They determine what a useful model must learn and what it must leave unchanged.</p></div>')+
 ''.join(section('<div class="split '+('reverse-mobile' if i%2 else '')+'"><div><p class="eyebrow">'+t[0]+'</p><h2>'+t[1]+'</h2><p class="body-copy">'+t[2]+'</p>'+link('Explore this research',t[3],'button-link')+'</div>'+illustration(t[4],bool(i%2))+'</div>','purple' if i%2 else 'gray') for i,t in enumerate(THEMES))+
 cta('The work behind the questions','Read the articles and access the associated tools.','publications.html','Publications'))

PAGES['imaging']=('Self-supervised denoising',hero('Recovering neural signals<br>without clean training images.','Self-supervised methods for voltage imaging and fluorescence microscopy.','Our Science',link('All research','research.html'))+
 section('<div class="editorial-grid"><h2>Learning from the<br>recording itself</h2><div class="prose"><p>SUPPORT estimates each pixel using its spatial and temporal context while keeping that pixel out of the input. This design can recover fast events even when adjacent frames alone do not predict them well.</p><p>The work brings statistical assumptions into network design: which observations carry useful information, and which noise dependencies would bias a prediction?</p><p class="source-line">Published study: Eom, Han, Park et al., Nature Methods (2023).</p>'+link('Read the paper',SUPPORT)+'</div></div>')+
 section('<div class="split">'+figure()+'<div><p class="eyebrow">SUPPORT</p><h2>From method<br>to experiment</h2><p class="body-copy">The publication evaluates the method using simulations and experimental imaging data. Code and datasets are available through the original research project.</p><div class="link-stack">'+link('Code and documentation',CODE)+link('Example datasets',ZENODO)+link('Press coverage','press.html')+'</div></div></div>','gray')+
 section('<div class="editorial-grid"><h2>Multi-scale<br>blind-spot networks</h2><div class="prose"><p>The WACV 2025 paper examines design principles for multi-scale J-invariant networks. It connects the structure of a blind-spot model to the information available for self-supervised denoising.</p>'+link('WACV 2025 paper',UBSN)+link('Publication record','publications.html#ubsn')+'</div></div>')+
 cta('How can a noisy image teach a network?','A short visual explanation of the blind-spot idea.','comics.html#missing-pixel','Read the comic'))

PAGES['calcium']=('Calcium imaging analysis',hero('Separating motion<br>from neural activity.','Alignment and decomposition methods for calcium imaging recordings.','Our Science',link('All research','research.html'))+
 section('<div class="split"><div><h2>The recording changes.<br>So does the specimen.</h2><p class="body-copy">A changing pixel can reflect neural activity, motion, or both. The REALS work considers alignment together with low-rank and sparse decomposition, rather than treating them as unrelated processing steps.</p><p class="source-line">Cho, Han et al., WACV (2023).</p>'+link('Read the REALS paper',REALS,'button-link')+'</div>'+illustration('motion')+'</div>')+
 section('<div class="editorial-grid"><h2>Related work</h2><div><article class="plain-entry"><h3>Efficient neural approximations</h3><p>Earlier work explores neural-network approximations of robust PCA for automated calcium imaging analysis.</p>'+link('MICCAI 2021 publication','publications.html#robust-pca')+'</article><article class="plain-entry"><h3>Acquisition and reconstruction</h3><p>The publication list also includes three-dimensional fluorescence imaging, virtual refocusing, and deep decomposition and deconvolution microscopy.</p>'+link('3DM publication','publications.html#3dm')+'</article></div></div>','gray')+
 cta('Why does motion correction matter?','See the distinction between a moving cell and a changing signal.','comics.html#moving-camera','Read the comic'))

PAGES['computing']=('Learning on analogue hardware',hero('Learning on<br>imperfect hardware.','Self-supervised video processing with on-device self-calibration.','Our Science',link('All research','research.html'))+
 section('<div class="split"><div><h2>Bring learning<br>closer to computation.</h2><p class="body-copy">This collaborative work implements self-supervised video processing on an analogue platform based on a selector-less memristor array. The learning procedure incorporates self-calibration to account for device behaviour.</p><p class="source-line">Jeong, Han et al., Nature Electronics (2025). Joint work with the Choi and Yoon groups at KAIST.</p>'+link('Read the research article',MEMRISTOR,'button-link')+'</div>'+illustration('hardware')+'</div>')+
 section('<div class="editorial-grid"><h2>Beyond an<br>idealised device</h2><div class="prose"><p>Physical devices are not interchangeable mathematical operations. Their variation becomes part of the computational problem.</p><p>The project connects algorithm design with a hardware implementation of video processing, complementing the imaging work on learning directly from observed data.</p>'+link('Publication and authors','publications.html#memristor')+'</div></div>','gray')+
 section('<div class="section-top"><h2>Research in context</h2>'+link('All press','press.html')+'</div>'+press_rows(PRESS[:2]))+
 cta('Discuss a research connection','Questions about algorithms, imaging data, or hardware-aware learning.','contact.html','Contact'))

# Preserve the user's existing publication entries and profile facts.
for name in ['profile','publications','news']:
    file=DATA/(name+'-main.html')
    if not file.exists():
        soup=BeautifulSoup((ROOT/(name+'.html')).read_text(),'html.parser')
        file.write_text(soup.main.decode_contents(),encoding='utf-8')
    body=file.read_text()
    if name=='profile':
        # Keep biography, all seven CV accordions, existing photo, and source CV.
        body=body.replace('>Research<','>Our Science<')
        PAGES[name]=('Seungjae Han, PhD',body)
    elif name=='publications':
        soup=BeautifulSoup(body,'html.parser')
        desc=soup.select_one('.hero-description')
        if desc: desc.string='Articles, conference papers, and preprints by Seungjae Han and collaborators, including work completed before this lab-site concept.'
        PAGES[name]=('Publications',str(soup))
    else:
        PAGES[name]=('News',body)

PAGES['team']=('Our Team',hero('Our Team','People working across computation, neuroscience, and imaging.','People')+
 section('<div class="person-feature"><a class="person-photo" href="profile.html"><img src="photo.jpeg" width="413" height="531" alt="Seungjae Han" loading="lazy"></a><div><p class="eyebrow">Researcher</p><h2>Seungjae Han, PhD</h2><p class="person-role">Postdoctoral Fellow<br>School of Electrical Engineering, KAIST</p><p>Research interests include self-supervised learning, computational imaging, and the analysis of neural recordings.</p><div class="link-stack">'+link('Biography and CV','profile.html')+link('Google Scholar',SCHOLAR)+link('Email',EMAIL)+'</div></div></div>')+
 section('<div class="editorial-grid"><div><p class="eyebrow">Research connections</p><h2>Collaborative work</h2></div><div><article class="plain-entry"><h3>Neuro-Instrumentation and Computational Analysis</h3><p>Young-Gyu Yoon’s NICA group at KAIST. Seungjae Han’s current research affiliation and the home of the SUPPORT project.</p>'+link('NICA Lab','https://nica.kaist.ac.kr/')+'</article><article class="plain-entry"><h3>Electronic devices and analogue computing</h3><p>Joint research with Shinhyun Choi’s group at KAIST on the self-calibrating memristor platform.</p>'+link('Collaborative research','computing.html')+'</article></div></div>','gray')+
 cta('Interested in the research?','Read about ways to start a conversation.','join-us.html','Join Us'))

PAGES['funding']=('Funding',hero('Funding','Fellowships supporting Seungjae Han’s research.','Research')+
 section('<div class="editorial-grid"><div><p class="eyebrow">Fellowships</p><h2>Research support</h2><p class="body-copy">The fellowships below were awarded to Seungjae Han. Project-specific funding acknowledgements are listed in the individual publications.</p></div><div><article class="support-entry"><p class="eyebrow">2026–2031</p><h2>Sejong Science Fellowship</h2><p>National Research Foundation of Korea</p>'+link('Fellowship record','profile.html#fellowships')+'</article><article class="support-entry"><p class="eyebrow">2026</p><h2>Jang Young Sil Fellowship</h2><p>KAIST</p>'+link('Fellowship record','profile.html#fellowships')+'</article></div></div>')+
 section('<div class="editorial-grid"><h2>Project acknowledgements</h2><div class="prose"><p>Research on SUPPORT and the analogue computing platform was conducted with collaborators. Funding acknowledgements belong to the relevant project and are not presented here as independent lab grants.</p>'+link('SUPPORT acknowledgements',SUPPORT+'#Ack1')+link('Analogue computing acknowledgements',MEMRISTOR+'#Ack1')+'</div></div>','gray'))

PAGES['resources']=('Resources',hero('Resources','Code, data, and practical starting points for the published methods.','Research')+
 section('<div class="resource-categories"><span>Software</span><span>Datasets</span><span>Getting started</span></div><div class="resource-list">'+
 '<article id="support"><p class="eyebrow">Software · SUPPORT</p><h2>Self-supervised denoising</h2><p>The original project repository provides the implementation, environment specification, usage examples, and issue tracker. It is maintained under NICALab, not a separate Han Lab software organisation.</p><div class="link-stack">'+link('Code and documentation',CODE)+link('Beginner guide',CODE+'/blob/main/Beginner_guide.md')+link('Report a software issue',CODE+'/issues')+'</div></article>'+
 '<article id="data"><p class="eyebrow">Data · SUPPORT</p><h2>Published example recordings</h2><p>Data associated with the Nature Methods study are available through Zenodo. Use the dataset’s documentation and the paper when interpreting the recordings.</p>'+link('Open the dataset',ZENODO,'button-link')+'</article>'+
 '<article id="reading"><p class="eyebrow">Learning resources</p><h2>Start with the question.</h2><p>Read a short explanation of the methods, then follow the links to the original research.</p><div class="link-stack">'+link('Computational neuroscience FAQs','faq.html')+link('Science comics','comics.html')+link('Publication list','publications.html')+'</div></article></div>')+
 cta('Working with a new imaging dataset?','Send a description of the measurement, the data format, and the question you are trying to answer.','contact.html','Contact'))

def press_tiles(records):
    cards=[]
    for i,item in enumerate(records):
        art=illustration('pixels' if item['project']=='imaging.html' else 'hardware',True)
        if item['project']=='imaging.html':
            art='<img src="nature_methods_cover.png" width="425" height="584" loading="lazy" alt="Nature Methods October 2023 cover">'
        cards.append(f'<article class="press-row press-tile" data-press-type="{item["type"]}"><a class="press-thumb thumb-{i}" href="{E(item["url"],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Read {E(item["title"],quote=True)}">{art}</a><div class="press-meta"><span>{E(item["publisher"])}</span><time datetime="{item["date"]}">{item["date"]}</time></div><h2><a href="{E(item["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{E(item["title"])}</a></h2><p>{E(item["description"])}</p><div class="press-actions">{link('Read coverage',item['url'])}{link('Related research',item['project'])}</div></article>')
    return '<div class="press-grid">'+''.join(cards)+'</div>'

PAGES['press']=('Press',hero('Press','Research coverage, commentary, and publication highlights.','Broader Impacts')+
 section('<div class="section-top"><h2>In the news</h2><div class="press-controls" role="group" aria-label="Filter press coverage"><button type="button" data-press-filter="all" aria-pressed="true">All</button><button type="button" data-press-filter="highlight" aria-pressed="false">Research highlights</button><button type="button" data-press-filter="commentary" aria-pressed="false">Commentary</button><button type="button" data-press-filter="coverage" aria-pressed="false">Media coverage</button></div></div><p class="press-count sr-only" role="status" aria-live="polite"></p>'+press_tiles(PRESS))+
 section('<div class="split cover-highlight"><figure><img src="nature_methods_cover.png" alt="Nature Methods October 2023 cover" width="425" height="584" loading="lazy"><figcaption>Nature Methods · October 2023</figcaption></figure><div><p class="eyebrow">On the cover</p><h2>SUPPORT in<br>Nature Methods</h2><p class="body-copy">The SUPPORT paper was featured on the October 2023 cover. This is a publication highlight, separate from the press coverage listed above.</p>'+link('The research','imaging.html','button-link')+link('KAIST feature','https://breakthrough.kaist.ac.kr/sub03/view/id/497','button-link')+'</div></div>','gray')+
 cta('Media enquiries','For questions about the research or requests for background material.','contact.html#media','Contact'))

# Simple, original science comics. Vector panels illustrate ideas, not measured results.
def pixel_character(expression='smile'):
    mouth='M29 49q12 12 24 0' if expression=='smile' else 'M29 52h24'
    return f'<g transform="translate(22 16)"><rect x="5" y="5" width="74" height="74" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="28" cy="32" r="3" fill="currentColor"/><circle cx="55" cy="32" r="3" fill="currentColor"/><path d="{mouth}" fill="none" stroke="currentColor" stroke-width="2"/><path d="M20 80l-8 20m45-20 8 20" stroke="currentColor" stroke-width="2"/></g>'

def comic_panel(n, bubble, drawing, caption):
    return f'<article class="comic-panel"><span class="panel-number">{n}</span><p class="speech">{bubble}</p><div class="comic-drawing"><svg viewBox="0 0 300 155" role="img" aria-label="{E(caption,quote=True)}">{drawing}</svg></div><p>{caption}</p></article>'

PIXEL_PANELS=[
 ('“I’m a measurement, not the whole story.”',pixel_character('flat')+'<g fill="currentColor" opacity=".5">'+''.join(f'<circle cx="{135+(i*23)%145}" cy="{30+(i*37)%100}" r="2"/>' for i in range(23))+'</g>','A recorded pixel contains a signal of interest and measurement noise.'),
 ('“Can my neighbours help?”','<g fill="none" stroke="currentColor" stroke-width="2">'+''.join(f'<rect x="{75+x*36}" y="{22+y*36}" width="27" height="27"/>' for y in range(3) for x in range(4) if (x,y)!=(1,1))+'<path d="M116 71h18m-9-9v18"/></g>','A blind-spot network excludes the target pixel and looks for information in its context.'),
 ('“Predict me. Don’t copy me.”',pixel_character()+'<path d="M143 65h75m-15-15 15 15-15 15" stroke="currentColor" stroke-width="2" fill="none"/><rect x="238" y="43" width="42" height="42" fill="currentColor" opacity=".45"/>','Training compares the prediction with a held-out noisy observation, under assumptions about signal and noise.'),
 ('“A smoother picture is not the final test.”','<g fill="none" stroke="currentColor" stroke-width="2"><path d="M20 100h60l10-9 10 18 10-9h30l10-60 10 100 10-40h110"/><path d="M20 25v112h265" opacity=".35"/></g>','The recovered timing and dynamics still need to be checked against the scientific question.')]
MOTION_PANELS=[
 ('“Did the neuron change, or did I move?”','<g fill="none" stroke="currentColor" stroke-width="2"><rect x="30" y="30" width="100" height="100"/><circle cx="65" cy="75" r="18"/><rect x="165" y="30" width="100" height="100"/><circle cx="212" cy="85" r="18"/></g>','A specimen’s movement can change pixel values even without a change in activity.'),
 ('“First, agree on where things are.”','<g fill="none" stroke="currentColor" stroke-width="2"><rect x="65" y="20" width="100" height="100"/><rect x="90" y="38" width="100" height="100" opacity=".4"/><path d="M230 72h-55m15-15-15 15 15 15"/></g>','Alignment estimates how frames move relative to a common coordinate system.'),
 ('“And separate what stays from what changes.”','<g fill="none" stroke="currentColor" stroke-width="2"><rect x="25" y="35" width="65" height="65"/><path d="M110 67h20m-10-10v20"/><rect x="150" y="35" width="65" height="65"/><circle cx="182" cy="68" r="8" fill="currentColor"/></g>','Low-rank and sparse components provide a way to model different structures in the recording.'),
 ('“Check the movie, not just the alignment.”','<g fill="none" stroke="currentColor" stroke-width="2"><path d="M30 112h55l12-40 12 40h55l12-65 12 65h65"/><rect x="20" y="20" width="250" height="115"/></g>','The goal is a useful estimate of activity. Visual inspection and quantitative checks remain important.')]
PAGES['comics']=('Comics',hero('Comics','Short visual stories about the ideas behind computational imaging.','Broader Impacts')+
 section('<div class="section-top"><div><p class="eyebrow">Science explained</p><h2>The missing pixel</h2></div>'+link('Related research','imaging.html')+'</div><div class="comic-grid">'+''.join(comic_panel(i+1,*p) for i,p in enumerate(PIXEL_PANELS))+'</div><p class="source-line">Original educational schematic. Based on the blind-spot principle discussed in <a href="'+SUPPORT+'" target="_blank" rel="noopener">SUPPORT, Nature Methods (2023)</a>. Not experimental data.</p>',id='missing-pixel')+
 section('<div class="section-top"><div><p class="eyebrow">Science explained</p><h2>When the camera moves</h2></div>'+link('Related research','calcium.html')+'</div><div class="comic-grid">'+''.join(comic_panel(i+1,*p) for i,p in enumerate(MOTION_PANELS))+'</div><p class="source-line">Original educational schematic. Related work: <a href="'+REALS+'" target="_blank" rel="noopener">REALS, WACV (2023)</a>. Not experimental data.</p>','gray',id='moving-camera')+
 cta('More questions?','Read the computational neuroscience and imaging FAQs.','faq.html','Comp Neuro FAQs'))

FAQ=[
 ('What does computational neuroscience mean here?','The research programme focuses on computational methods for measuring and analysing neural activity. This includes statistical models, learning algorithms, and the relationship between image acquisition and signal reconstruction.','Our Science','research.html'),
 ('Why combine imaging and machine learning?','Imaging measurements can be noisy, incomplete, or affected by motion. A computational model can use structure in the data to estimate signals of interest. Its assumptions and failure modes are part of the scientific method, not an afterthought.','Imaging research','imaging.html'),
 ('What is self-supervised denoising?','It is a way to train a denoising model without a separate set of clean target images. In a blind-spot approach, part of the observation is withheld from the input and used as the prediction target. This relies on assumptions about the signal and the noise.','SUPPORT paper',SUPPORT),
 ('Does a denoised image show the ground truth?','No. It is an estimate produced by a model. A visually clean output can still omit or distort a relevant feature. The raw data, residuals, and the signal of interest should remain part of an evaluation.','The missing pixel comic','comics.html#missing-pixel'),
 ('How is voltage imaging different from calcium imaging?','Voltage imaging follows changes associated with membrane voltage, while calcium imaging follows a different fluorescent indicator signal. Their temporal characteristics and noise make different demands on an analysis method.','SUPPORT paper',SUPPORT),
 ('Why does motion matter in calcium imaging?','Movement shifts structures across pixels. Without accounting for it, changing pixel values can mix changes in position with changes in activity. The REALS work studies alignment and decomposition together.','Calcium imaging research','calcium.html'),
 ('Where are the code and data?','The Resources page links to the original SUPPORT repository, its beginner guide, and the published example datasets. Ownership and licensing remain with the respective projects.','Resources','resources.html'),
 ('Do I need a GPU to run SUPPORT?','The project distinguishes inference from training. Its documentation describes CPU use for the test GUI and GPU requirements for training workflows. Follow the repository’s environment and hardware notes for the workflow you use.','SUPPORT documentation',CODE),
 ('How can I discuss a possible collaboration?','Send a short description of the scientific question, the kind of data or method involved, and the work you would like to discuss. A link to a paper or project is useful context.','Contact','contact.html')]
PAGES['faq']=('Comp Neuro FAQs',hero('Comp Neuro FAQs','Questions about neural recordings, self-supervised learning, and the research methods.','Broader Impacts')+
 section('<div class="faq-layout"><aside><p class="eyebrow">A starting point</p><p>These answers introduce the ideas. Each question links to research or practical documentation.</p>'+link('Science comics','comics.html','button-link')+'</aside><div class="faq-list">'+''.join(f'<details class="faq-item" id="question-{i+1}"><summary><h2>{q}</h2><span aria-hidden="true">+</span></summary><div class="faq-answer"><p>{a}</p>{link(t,u)}</div></details>' for i,(q,a,t,u) in enumerate(FAQ))+'</div></div>'))

PAGES['join-us']=('Join Us',hero('Join Us','A place to start a conversation about research and collaboration.','Work With Us')+
 section('<div class="editorial-grid"><div><p class="eyebrow">Work with us</p><h2>Shared questions.<br>Different approaches.</h2><p class="body-copy">The research connects experimental neuroscience, computational imaging, and learning algorithms.</p></div><div><article class="plain-entry"><h3>Research collaborations</h3><p>For a potential collaboration, describe the scientific question, your approach, and the data or expertise involved.</p>'+link('Discuss a collaboration',EMAIL+'?subject=Research%20collaboration')+'</article><article class="plain-entry"><h3>Students and prospective researchers</h3><p>For an exploratory enquiry, share your research interests and a short CV or project link. Please refer to the specific research direction that interests you.</p>'+link('Send an enquiry',EMAIL+'?subject=Research%20enquiry')+'</article><article class="plain-entry"><h3>Using the methods</h3><p>For software questions, start with the project documentation and issue tracker. Include the software version, the relevant error message, and a small reproducible example where possible.</p>'+link('Code and resources','resources.html')+'</article></div></div>')+
 section('<div class="editorial-grid"><h2>Open positions</h2><div class="prose"><p>No specific funded position is advertised on this page. Research enquiries are not applications to an announced vacancy.</p>'+link('Research background','research.html')+'</div></div>','gray'))

PAGES['contact']=('Contact',hero('Contact','Research conversations, software questions, and media enquiries.','Work With Us')+
 section('<div class="contact-grid"><div><p class="eyebrow">Primary contact</p><h2>Seungjae Han, PhD</h2><p>Postdoctoral Fellow<br>School of Electrical Engineering<br>KAIST, South Korea</p>'+link('jay0118@kaist.ac.kr',EMAIL,'button-link')+'<p class="source-line">Current affiliation: <a href="'+BIO+'" target="_blank" rel="noopener">NICA Lab, KAIST</a>.</p></div><div><p class="eyebrow">Find the research</p>'+link('Our Science','research.html','contact-row')+link('Publications','publications.html','contact-row')+link('Google Scholar',SCHOLAR,'contact-row')+link('Biography and CV','profile.html','contact-row')+link('GitHub','https://github.com/SteveJayH','contact-row')+'</div></div>')+
 section('<div class="editorial-grid"><div><p class="eyebrow">Press and outreach</p><h2>Media enquiries</h2></div><div class="prose"><p>For questions about a study, please include its title or a link and the topic you would like to discuss.</p>'+link('Email about the research',EMAIL+'?subject=Media%20enquiry')+link('Press coverage','press.html')+'</div></div>','gray',id='media'))

# A simple sitemap is also used by the preview router and the automated tests.
for slug,(title,body) in PAGES.items():
    canonical='https://stevejayh.github.io/'+('' if slug=='index' else slug+'.html')
    desc='Han Lab website concept: computational neuroscience, self-supervised learning, and fluorescence microscopy.'
    html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#004890"><title>{E(title)} | Han Lab</title><meta name="description" content="{desc}"><link rel="canonical" href="{canonical}"><link rel="preconnect" href="https://cdn.prod.website-files.com" crossorigin><link rel="preload" href="{FONT}" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="assets/site.css"><link rel="stylesheet" href="assets/lab.css"><script src="assets/site.js" defer></script><script src="assets/lab.js" defer></script></head>
<body data-page="{slug}"><!-- Han Lab is a provisional name for this review build; appointments are stated on the People page. -->{header()}<main id="main" tabindex="-1">{body}</main>{footer()}</body></html>'''
    (ROOT/(slug+'.html')).write_text(html,encoding='utf-8')
(ROOT/'data/routes.json').write_text(json.dumps(list(PAGES),indent=2))
print(f'Built {len(PAGES)} complete pages.')
