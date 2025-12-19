// Paper filtering functions
function author() {
    const author1_checked = document.getElementById("author1").checked;
    const author2_checked = document.getElementById("author2").checked;

    if (author1_checked && !(author2_checked)) {
        document.getElementById("RLP").style.display = "none";
        document.getElementById("WHOLEEXM").style.display = "none";
        document.getElementById("HAPTIC").style.display = "none";
        document.getElementById("impasto").style.display = "none";
        document.getElementById("jove").style.display = "none";
        document.getElementById("multiscale-jinvariant").style.display = "";
        document.getElementById("neuromorphic-analog").style.display = "";
    }
    else if (!(author1_checked) && author2_checked) {
        document.getElementById("apr").style.display = "none";
        document.getElementById("support").style.display = "none";
        document.getElementById("reals").style.display = "none";
        document.getElementById("3DM").style.display = "none";
        document.getElementById("BEAR").style.display = "none";
        document.getElementById("LTE").style.display = "none";
        document.getElementById("multiscale-jinvariant").style.display = "none";
        document.getElementById("neuromorphic-analog").style.display = "none";
    }
    else {
        document.getElementById("apr").style.display = "";
        document.getElementById("jove").style.display = "";
        document.getElementById("impasto").style.display = "";
        document.getElementById("support").style.display = "";
        document.getElementById("reals").style.display = "";
        document.getElementById("3DM").style.display = "";
        document.getElementById("BEAR").style.display = "";
        document.getElementById("LTE").style.display = "";
        document.getElementById("RLP").style.display = "";
        document.getElementById("WHOLEEXM").style.display = "";
        document.getElementById("HAPTIC").style.display = "";
        document.getElementById("multiscale-jinvariant").style.display = "";
        document.getElementById("neuromorphic-analog").style.display = "";
    }
}

function journal() {
    const journal1_checked = document.getElementById("journal1").checked;
    const journal2_checked = document.getElementById("journal2").checked;

    if (journal1_checked && !(journal2_checked)) {
        document.getElementById("reals").style.display = "none";
        document.getElementById("BEAR").style.display = "none";
        document.getElementById("LTE").style.display = "none";
        document.getElementById("HAPTIC").style.display = "none";
        document.getElementById("multiscale-jinvariant").style.display = "none";
        document.getElementById("neuromorphic-analog").style.display = "";
    }
    else if (!(journal1_checked) && journal2_checked) {
        document.getElementById("apr").style.display = "none";
        document.getElementById("jove").style.display = "none";
        document.getElementById("impasto").style.display = "none";
        document.getElementById("support").style.display = "none";
        document.getElementById("RLP").style.display = "none";
        document.getElementById("WHOLEEXM").style.display = "none";
        document.getElementById("3DM").style.display = "none";
        document.getElementById("multiscale-jinvariant").style.display = "";
        document.getElementById("neuromorphic-analog").style.display = "none";
    }
    else {
        document.getElementById("apr").style.display = "";
        document.getElementById("jove").style.display = "";
        document.getElementById("impasto").style.display = "";
        document.getElementById("support").style.display = "";
        document.getElementById("reals").style.display = "";
        document.getElementById("3DM").style.display = "";
        document.getElementById("BEAR").style.display = "";
        document.getElementById("LTE").style.display = "";
        document.getElementById("RLP").style.display = "";
        document.getElementById("WHOLEEXM").style.display = "";
        document.getElementById("HAPTIC").style.display = "";
        document.getElementById("multiscale-jinvariant").style.display = "";
        document.getElementById("neuromorphic-analog").style.display = "";
    }
}

// Carousel functionality
let currentCarouselSlide = 0;
let carouselSlides;
let dots;

function moveCarousel(direction) {
    carouselSlides = document.querySelectorAll('.carousel-slide');
    dots = document.querySelectorAll('.dot');

    carouselSlides[currentCarouselSlide].classList.remove('active');
    dots[currentCarouselSlide].classList.remove('active');

    currentCarouselSlide += direction;

    if (currentCarouselSlide >= carouselSlides.length) {
        currentCarouselSlide = 0;
    } else if (currentCarouselSlide < 0) {
        currentCarouselSlide = carouselSlides.length - 1;
    }

    carouselSlides[currentCarouselSlide].classList.add('active');
    dots[currentCarouselSlide].classList.add('active');
}

function currentSlide(n) {
    carouselSlides = document.querySelectorAll('.carousel-slide');
    dots = document.querySelectorAll('.dot');

    carouselSlides[currentCarouselSlide].classList.remove('active');
    dots[currentCarouselSlide].classList.remove('active');

    currentCarouselSlide = n - 1;

    carouselSlides[currentCarouselSlide].classList.add('active');
    dots[currentCarouselSlide].classList.add('active');
}

// Profile carousel functionality
let currentProfileSlide = 0;
let profileSlides;
let profileDots;

function moveProfileCarousel(direction) {
    profileSlides = document.querySelectorAll('.profile-carousel-slide');
    profileDots = document.querySelectorAll('.profile-dot');

    profileSlides[currentProfileSlide].classList.remove('active');
    profileDots[currentProfileSlide].classList.remove('active');

    currentProfileSlide += direction;

    if (currentProfileSlide >= profileSlides.length) {
        currentProfileSlide = 0;
    } else if (currentProfileSlide < 0) {
        currentProfileSlide = profileSlides.length - 1;
    }

    profileSlides[currentProfileSlide].classList.add('active');
    profileDots[currentProfileSlide].classList.add('active');
}

function setCurrentProfileSlide(n) {
    profileSlides = document.querySelectorAll('.profile-carousel-slide');
    profileDots = document.querySelectorAll('.profile-dot');

    profileSlides[currentProfileSlide].classList.remove('active');
    profileDots[currentProfileSlide].classList.remove('active');

    currentProfileSlide = n - 1;

    profileSlides[currentProfileSlide].classList.add('active');
    profileDots[currentProfileSlide].classList.add('active');
}

// Function to add a paper card easily
// Usage example:
// addPaperCard({
//   id: "newpaper",
//   imageSrc: "images/paper.png",
//   imageAlt: "paper",
//   title: "Paper Title",
//   titleLink: "https://example.com/paper",
//   keywords: [
//     { text: "Keyword1", color: "#e63946" },
//     { text: "Keyword2", color: "#495057" }
//   ],
//   authors: [
//     { name: "Author1", link: "https://example.com/author1", isFirst: true },
//     { name: "Seungjae Han", isStrong: true },
//     { name: "Author3", link: "https://example.com/author3" }
//   ],
//   venue: { name: "Nature", year: 2024 },
//   links: [
//     { type: "paper", url: "https://example.com/paper" },
//     { type: "code", url: "https://github.com/example" }
//   ],
//   description: "Paper description here",
//   highlighted: false
// });
function addPaperCard(config) {
    const papersGrid = document.querySelector('.papers-grid');
    if (!papersGrid) {
        console.error('Papers grid not found in addPaperCard!');
        return;
    }

    // Create paper card container
    const card = document.createElement('div');
    card.className = 'paper-card' + (config.highlighted ? ' highlighted' : '');
    card.id = config.id;

    // Create image section
    const imageDiv = document.createElement('div');
    imageDiv.className = 'paper-image';
    const img = document.createElement('img');
    img.src = config.imageSrc || '';
    img.alt = config.imageAlt || '';
    imageDiv.appendChild(img);
    card.appendChild(imageDiv);

    // Create content section
    const contentDiv = document.createElement('div');
    contentDiv.className = 'paper-content';

    // Add keywords if provided
    if (config.keywords && config.keywords.length > 0) {
        const keywordsDiv = document.createElement('div');
        keywordsDiv.className = 'paper-keywords';
        config.keywords.forEach(kw => {
            const keywordSpan = document.createElement('span');
            keywordSpan.className = 'keyword';
            keywordSpan.style.backgroundColor = kw.color || '#495057';
            keywordSpan.textContent = kw.text;
            keywordsDiv.appendChild(keywordSpan);
        });
        contentDiv.appendChild(keywordsDiv);
    }

    // Add title
    const titleLink = document.createElement('a');
    titleLink.href = config.titleLink || '#';
    if (config.titleLink) titleLink.target = '_blank';
    const titleDiv = document.createElement('div');
    titleDiv.className = 'paper-title';
    titleDiv.textContent = config.title || '';
    titleLink.appendChild(titleDiv);
    contentDiv.appendChild(titleLink);

    // Add authors
    if (config.authors && config.authors.length > 0) {
        const authorsDiv = document.createElement('div');
        authorsDiv.className = 'paper-authors';
        config.authors.forEach((author, index) => {
            if (index > 0) authorsDiv.appendChild(document.createTextNode(', '));

            if (author.link) {
                const authorLink = document.createElement('a');
                authorLink.href = author.link;
                authorLink.target = '_blank';
                authorLink.textContent = author.name;
                authorsDiv.appendChild(authorLink);
            } else if (author.isStrong) {
                const strong = document.createElement('strong');
                strong.textContent = author.name;
                authorsDiv.appendChild(strong);
            } else {
                authorsDiv.appendChild(document.createTextNode(author.name));
            }

            if (author.isFirst) authorsDiv.appendChild(document.createTextNode('*'));
            if (author.isCorresponding) authorsDiv.appendChild(document.createTextNode('**'));
        });
        contentDiv.appendChild(authorsDiv);
    }

    // Add venue
    if (config.venue) {
        const venueDiv = document.createElement('div');
        venueDiv.className = 'paper-venue';
        const venueHTML = `<em>${config.venue.name}</em>, ${config.venue.year}`;
        if (config.venue.extras) {
            venueDiv.innerHTML = venueHTML + ' ' + config.venue.extras;
        } else {
            venueDiv.innerHTML = venueHTML;
        }
        contentDiv.appendChild(venueDiv);
    }

    // Add links
    if (config.links && config.links.length > 0) {
        const linksDiv = document.createElement('div');
        linksDiv.className = 'paper-links';
        config.links.forEach((link, index) => {
            if (index > 0) linksDiv.appendChild(document.createTextNode(' / '));
            const linkEl = document.createElement('a');
            linkEl.href = link.url;
            linkEl.target = '_blank';
            linkEl.textContent = link.type;
            linksDiv.appendChild(linkEl);
        });
        contentDiv.appendChild(linksDiv);
    }

    // Add description
    if (config.description) {
        const descDiv = document.createElement('div');
        descDiv.className = 'paper-description';
        descDiv.textContent = config.description;
        contentDiv.appendChild(descDiv);
    }

    card.appendChild(contentDiv);

    // Insert at the beginning of the papers grid
    papersGrid.insertBefore(card, papersGrid.firstChild);
}

// Initialize all papers when DOM is ready
function initializePapers() {
    console.log('initializePapers called');
    const papersGrid = document.querySelector('.papers-grid');
    if (!papersGrid) {
        console.error('Papers grid not found!');
        return;
    }
    console.log('Papers grid found, adding papers...');

    // Initialize all papers using addPaperCard function
    // Papers are added in reverse order since addPaperCard inserts at the beginning

    // HAPTIC Paper
    addPaperCard({
        id: "HAPTIC",
        imageSrc: "images/haptic.png",
        imageAlt: "haptic",
        title: "Observation of Human Trajectory in Response to Haptic Feedback from Mobile Robot",
        titleLink: "https://ieeexplore.ieee.org/document/8571937",
        keywords: [
            { text: "Haptic", color: "#495057" },
            { text: "Human-Robot Interaction", color: "#495057" }
        ],
        authors: [
            { name: "Hee-Seung Moon", link: "https://hsmoon121.github.io/" },
            { name: "Woohyun Kim", link: "http://www.gnss.kr/woohyunkim" },
            { name: "Seungjae Han", isStrong: true },
            { name: "Jiwon Seo", link: "https://www.jwseo.com/" }
        ],
        venue: { name: "ICCAS", year: 2018 },
        links: [
            { type: "paper", url: "https://ieeexplore.ieee.org/document/8571937" }
        ],
        description: "Analyze the walking trajectory of a blindfolded participant receiving haptic feedback from a mobile robot. Developed a mobile robot system with a haptic device and algorithm for appropriate haptic feedback.",
        highlighted: false
    });

    // LTE Paper
    addPaperCard({
        id: "LTE",
        imageSrc: "images/lteapp_square.png",
        imageAlt: "lte",
        title: "Smartphone Application to Estimate Distances from LTE Base Stations Based on Received Signal Strength Measurements",
        titleLink: "https://ieeexplore.ieee.org/document/8793365",
        keywords: [
            { text: "LTE RSS", color: "#495057" },
            { text: "Positioning", color: "#495057" }
        ],
        authors: [
            { name: "Seungjae Han", isStrong: true },
            { name: "Taewon Kang", link: "http://www.gnss.kr/taewon" },
            { name: "Jiwon Seo", link: "https://www.jwseo.com/" }
        ],
        venue: {
            name: "ITC-CSCC",
            year: 2019,
            extras: '(<span style="color: #FD3029;"><strong>Oral presentation</strong></span>)'
        },
        links: [
            { type: "paper", url: "https://ieeexplore.ieee.org/document/8793365" }
        ],
        description: "Smartphone application that calculates predicted distances to near base stations based on received signal strength. Research for LTE-based positioning where GPS signal is unavailable.",
        highlighted: false
    });

    // BEAR Paper
    addPaperCard({
        id: "BEAR",
        imageSrc: "images/BEAR_hall_image.png",
        imageAlt: "bear",
        title: "Efficient Neural Network Approximation of Robust PCA for Automated Analysis of Calcium Imaging Data",
        titleLink: "https://link.springer.com/chapter/10.1007%2F978-3-030-87234-2_56/",
        keywords: [
            { text: "Robust PCA", color: "#bb3e03" }
        ],
        authors: [
            { name: "Seungjae Han", isStrong: true },
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main" },
            { name: "Inkyu Park", link: "https://github.com/yunik1004" },
            { name: "Kijung Shin", link: "https://kijungs.github.io/" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: { name: "MICCAI", year: 2021 },
        links: [
            { type: "paper", url: "https://link.springer.com/chapter/10.1007%2F978-3-030-87234-2_56" },
            { type: "code", url: "https://github.com/NICALab/BEAR" },
            { type: "poster", url: "/images/MICCAI_BEAR_poster_v2.pdf" },
            { type: "wallpaper", url: "images/black_zebrafish.png" }
        ],
        description: "Fast and scalable gradient descent based Robust PCA algorithm. Achieves an order of magnitude speed improvement, demonstrated with calcium imaging dataset as large as tens of gigabytes.",
        highlighted: true
    });

    // 3DM Paper
    addPaperCard({
        id: "3DM",
        imageSrc: "images/3DM_before_250.png",
        imageAlt: "3dm",
        title: "3DM: Deep decomposition and deconvolution microscopy for rapid neural activity imaging",
        titleLink: "https://www.osapublishing.org/oe/fulltext.cfm?uri=oe-29-20-32700&id=459843",
        keywords: [
            { text: "Computational Imaging", color: "#2d6a4f" },
            { text: "Robust PCA", color: "#bb3e03" }
        ],
        authors: [
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main", isFirst: true },
            { name: "Seungjae Han", isStrong: true, isFirst: true },
            { name: "Kang-Han Lee", link: "https://www.researchgate.net/scientific-contributions/Kang-Han-Lee-2107619192" },
            { name: "Cheol-Hee Kim", link: "https://scholar.google.com/citations?user=0G8geQsAAAAJ&hl=en" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: {
            name: "Optics Express",
            year: 2021,
            extras: '<strong>(<a href="images/3DM_editors_pick_highlight.png" target="_blank" style="color: #FD3029; text-decoration: underline;">Editor\'s pick (5.8% = 8/138)</a>, <a href="images/3DM_image_of_the_week_highlight.png" target="_blank" style="color: #FD3029; text-decoration: underline;">Image of the Week</a>)</strong>'
        },
        links: [
            { type: "paper", url: "https://opg.optica.org/oe/fulltext.cfm?uri=oe-29-20-32700&id=459843" },
            { type: "code", url: "https://github.com/NICALab/3DM" }
        ],
        description: "Fast computational microscopy for the volumetric imaging of neural activity, using two neural networks which perform sparse decomposition and deconvolution.",
        highlighted: false
    });


    // RLP Paper
    addPaperCard({
        id: "RLP",
        imageSrc: "images/rlp-net_thumbnail_before.png",
        imageAlt: "rlp",
        title: "Three-dimensional fluorescence microscopy through virtual refocusing using a recursive light propagation network",
        titleLink: "https://www.sciencedirect.com/science/article/pii/S1361841522002328?via%3Dihub",
        keywords: [
            { text: "Computational Imaging", color: "#2d6a4f" }
        ],
        authors: [
            { name: "Changyeop Shin", link: "https://nica.kaist.ac.kr/people", isFirst: true },
            { name: "Hyun Ryu", link: "https://nica.kaist.ac.kr/people", isFirst: true },
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main" },
            { name: "Seungjae Han", isStrong: true },
            { name: "Kang-Han Lee", link: "https://www.researchgate.net/scientific-contributions/Kang-Han-Lee-2107619192" },
            { name: "Cheol-Hee Kim", link: "https://scholar.google.com/citations?user=0G8geQsAAAAJ&hl=en" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: { name: "Medical Image Analysis", year: 2022 },
        links: [
            { type: "paper", url: "https://www.sciencedirect.com/science/article/pii/S1361841522002328?via%3Dihub" },
            { type: "code", url: "https://github.com/NICALab/rlpnet" }
        ],
        description: "Neural network that models the light propagation law can reconstruct a volume using two adjacent images.",
        highlighted: false
    });

    // IMPASTO Paper
    addPaperCard({
        id: "impasto",
        imageSrc: "images/impasto_before.png",
        imageAlt: "impasto",
        title: "IMPASTO: Multiplexed cyclic imaging without signal removal via self-supervised neural unmixing",
        titleLink: "https://www.biorxiv.org/content/10.1101/2022.11.22.517463v1",
        keywords: [
            { text: "Denoising", color: "#e63946" },
            { text: "Voltage Imaging", color: "#495057" }
        ],
        authors: [
            { name: "Hyunwoo Kim", link: "https://scholar.google.com/citations?user=YAywWWMAAAAJ&hl=ko&oi=sra", isFirst: true },
            { name: "Seoungbin Bae", link: "https://nica.kaist.ac.kr/people", isFirst: true },
            { name: "Junmo Cho", link: "https://nica.kaist.ac.kr/people" },
            { name: "Hoyeon Nam", link: "https://www.researchgate.net/scientific-contributions/Hoyeon-Nam-2220743474" },
            { name: "Junyoung Seo", link: "https://www.researchgate.net/scientific-contributions/Junyoung-Seo-2185428786" },
            { name: "Seungjae Han", isStrong: true },
            { name: "Euiin Yi", link: "https://nica.kaist.ac.kr/people" },
            { name: "Eunsu Kim", link: "https://nica.kaist.ac.kr/people" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people", isCorresponding: true },
            { name: "Jae-Byum Chang", link: "https://sites.google.com/site/jbchang03/pi?pli=1", isCorresponding: true }
        ],
        venue: { name: "bioRxiv", year: 2022 },
        links: [
            { type: "paper", url: "https://www.biorxiv.org/content/10.1101/2022.11.22.517463v1" }
        ],
        description: "Erasureless cyclic imaging method with self-supervised spectral unmixing.",
        highlighted: false
    });

    // REALS Paper
    addPaperCard({
        id: "reals",
        imageSrc: "images/reals_thumbnail_before.png",
        imageAlt: "reals",
        title: "Robust and Efficient Alignment of Calcium Imaging Data through Simultaneous Low Rank and Sparse Decomposition",
        titleLink: "https://openaccess.thecvf.com/content/WACV2023/html/Cho_Robust_and_Efficient_Alignment_of_Calcium_Imaging_Data_Through_Simultaneous_WACV_2023_paper.html",
        keywords: [
            { text: "Registration", color: "#0a9396" },
            { text: "Robust PCA", color: "#bb3e03" }
        ],
        authors: [
            { name: "Junmo Cho", link: "https://nica.kaist.ac.kr/people", isFirst: true },
            { name: "Seungjae Han", isStrong: true, isFirst: true },
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main" },
            { name: "Kijung Shin", link: "https://kijungs.github.io/" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: { name: "WACV", year: 2023 },
        links: [
            { type: "paper", url: "https://openaccess.thecvf.com/content/WACV2023/html/Cho_Robust_and_Efficient_Alignment_of_Calcium_Imaging_Data_Through_Simultaneous_WACV_2023_paper.html" },
            { type: "code", url: "https://github.com/NICALab/REALS" }
        ],
        description: "REALS can align multiple images very fast and accurately, even if there are lots of contaminations.",
        highlighted: false
    });

    // JoVE Paper
    addPaperCard({
        id: "jove",
        imageSrc: "images/jove.jpg",
        imageAlt: "jove",
        title: "In vivo whole-brain imaging of zebrafish larvae using three-dimensional fluorescence microscopy",
        titleLink: "https://www.jove.com/kr/t/65218/in-vivo-whole-brain-imaging-zebrafish-larvae-using-three-dimensional",
        authors: [
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main" },
            { name: "Seungjae Han", isStrong: true },
            { name: "Gyuri Kim", link: "https://nica.kaist.ac.kr/people" },
            { name: "Minho Eom", link: "https://www.minhoeom.com/" },
            { name: "Kang-Han Lee", link: "https://www.researchgate.net/scientific-contributions/Kang-Han-Lee-2107619192" },
            { name: "Cheol-Hee Kim", link: "https://scholar.google.com/citations?user=0G8geQsAAAAJ&hl=ent" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: { name: "Journal of Visualized Experiments", year: 2023 },
        links: [
            { type: "paper", url: "https://www.jove.com/kr/t/65218/in-vivo-whole-brain-imaging-zebrafish-larvae-using-three-dimensional" },
            { type: "code", url: "https://github.com/NICALab/Zebrafish-brain-visualization" }
        ],
        description: "Effective and reproducible protocol for whole-brain imaging of larval zebrafish using three-dimensional fluorescence microscopy.",
        highlighted: false
    });

    // SUPPORT Paper
    addPaperCard({
        id: "support",
        imageSrc: "images/support_cover.png",
        imageAlt: "support",
        title: "Statistically unbiased prediction enables accurate denoising of voltage imaging data",
        titleLink: "https://www.nature.com/articles/s41592-023-02005-8",
        keywords: [
            { text: "Denoising", color: "#e63946" },
            { text: "Voltage Imaging", color: "#495057" }
        ],
        authors: [
            { name: "Minho Eom", link: "https://www.minhoeom.com/", isFirst: true },
            { name: "Seungjae Han", isStrong: true, isFirst: true },
            { name: "Pojeong Park", link: "https://scholar.google.com/citations?user=MplXTg5UAJsC&hl=en", isFirst: true },
            { name: "Gyuri Kim", link: "https://scholar.google.com/citations?user=BkPHqf4AAAAJ&hl=en&oi=sra" },
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main" },
            { name: "Jueun Sim", link: "https://sites.google.com/site/jbchang03/members" },
            { name: "Kang-Han Lee", link: "https://www.researchgate.net/scientific-contributions/Kang-Han-Lee-2107619192" },
            { name: "Seonghoon Kim", link: "https://scholar.google.co.kr/citations?user=pTIzmbkAAAAJ&hl=en" },
            { name: "He Tian", link: "https://scholar.google.com/citations?user=5xDaLqMAAAAJ&hl=en" },
            { name: "Urs L. Böhm", link: "https://scholar.google.com/citations?user=HqLH9kUAAAAJ&hl=en" },
            { name: "Eric Lowet", link: "https://scholar.google.com/citations?user=kXXeLoEAAAAJ&hl=en" },
            { name: "Hua-an Tseng", link: "https://scholar.google.com/citations?user=pLNtyEsAAAAJ&hl=en" },
            { name: "Jieun Choi", link: "https://kr.linkedin.com/in/jieun-choi-b64522151" },
            { name: "Stephani Edwina Lucia", link: "https://www.linkedin.com/in/stephani-edwina-lucia/?originalSubdomain=kr" },
            { name: "Seung Hyun Ryu", link: "https://seunghyunryu.info/" },
            { name: "Márton Rózsa", link: "https://scholar.google.com/citations?user=bJ-2MhwAAAAJ&hl=en" },
            { name: "Sunghoe Chang", link: "https://www.nfisnu.com/" },
            { name: "Pilhan Kim", link: "http://ivmvl.kaist.ac.kr/" },
            { name: "Xue Han", link: "https://www.bu.edu/hanlab/" },
            { name: "Kiryl D. Piatkevich", link: "https://www.piatkevich-lab.com/" },
            { name: "Myunghwan Choi", link: "https://biosci.snu.ac.kr/neurophoton/en/professor" },
            { name: "Cheol-Hee Kim", link: "https://scholar.google.com/citations?user=0G8geQsAAAAJ&hl=ent" },
            { name: "Adam Cohen", link: "http://cohenweb.rc.fas.harvard.edu/People/people.html" },
            { name: "Jae-Byum Chang", link: "https://sites.google.com/site/jbchang03/pi?pli=1" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: {
            name: "Nature Methods",
            year: 2023,
            extras: '<strong>(<a href="https://www.nature.com/nmeth/volumes/20/issues/10" target="_blank" style="color: #FD3029; text-decoration: underline;">Selected as the cover</a>, <a href="https://breakthroughs.kaist.ac.kr/sub02/view/id/497" target="_blank" style="color: #FD3029; text-decoration: underline;">KAIST Breakthrough</a>, <a href="https://news.kaist.ac.kr/news/html/news/?mode=V&mng_no=31550" target="_blank" style="color: #FD3029; text-decoration: underline;">KAIST News</a>)</strong>'
        },
        links: [
            { type: "paper", url: "https://www.biorxiv.org/content/10.1101/2022.11.17.516709v1" },
            { type: "code", url: "https://github.com/NICALab/SUPPORT" },
            { type: "data", url: "https://zenodo.org/record/7330257#.Y3mv_HZByp0" }
        ],
        description: "Self-supervised learning method for removing Poisson-Gaussian noise in voltage imaging data as well as a wide range of microscopy images.",
        highlighted: true
    });

    // APR Paper
    addPaperCard({
        id: "apr",
        imageSrc: "images/apr.png",
        imageAlt: "apr",
        title: "From Pixels to Information: Artificial Intelligence in Fluorescence Microscopy",
        titleLink: "https://onlinelibrary.wiley.com/doi/full/10.1002/adpr.202300308",
        authors: [
            { name: "Seungjae Han", isStrong: true },
            { name: "Joshua Yedam You", link: "https://nica.kaist.ac.kr/people" },
            { name: "Minho Eom", link: "https://www.minhoeom.com/" },
            { name: "Sungjin Ahn", link: "https://nica.kaist.ac.kr/people" },
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: { name: "Advanced Photonics Research", year: 2024 },
        links: [
            { type: "paper", url: "https://onlinelibrary.wiley.com/doi/full/10.1002/adpr.202300308" }
        ],
        description: "Review article providing an overview of how artificial intelligence is transforming fluorescence microscopy.",
        highlighted: false
    });

    // WHOLEEXM Paper
    addPaperCard({
        id: "WHOLEEXM",
        imageSrc: "images/wholebody_exm_before.png",
        imageAlt: "wholeexm",
        title: "Nanoscale resolution imaging of whole mouse embryos using expansion microscopy",
        titleLink: "",
        keywords: [
            { text: "Expansion Microscopy", color: "#355070" }
        ],
        authors: [
            { name: "Jueun Sim", link: "https://sites.google.com/site/jbchang03/members", isFirst: true },
            { name: "Chan E Park", link: "https://sites.google.com/site/jbchang03/members", isFirst: true },
            { name: "In Cho", link: "https://scholar.google.com/citations?user=SjY3zXoAAAAJ&hl=en&oi=sra", isFirst: true },
            { name: "Kyeongbae Min", link: "https://www.researchgate.net/profile/Kyeongbae-Min" },
            { name: "Minho Eom", link: "https://www.minhoeom.com/" },
            { name: "Seungjae Han", isStrong: true },
            { name: "Hyungju Jeon", link: "https://bsi.kist.re.kr/dt_team/hyungjujeon/" },
            { name: "Hyun-Ju Cho", link: "https://oak.kribb.re.kr/researcher-profile?ep=447" },
            { name: "Eun-Seo Cho", link: "https://sites.google.com/view/eunseocho/main" },
            { name: "Ajeet Kumar", link: "https://scholar.google.com/citations?user=oqrOpGgAAAAJ&hl=en" },
            { name: "Yosep Chong", link: "https://www.cmcujb.or.kr/page/en/doctor/53/D0001275" },
            { name: "Jeong Seuk Kang", link: "https://www.media.mit.edu/people/jskang/overview/" },
            { name: "Kiryl D. Piatkevich", link: "https://www.piatkevich-lab.com/people" },
            { name: "Erica E. Jung", link: "https://jung.lab.uic.edu/profiles/jung-erica/" },
            { name: "Du-Seock Kang", link: "https://gsmse.kaist.ac.kr/boards/lists/professor_04" },
            { name: "Seok-Kyu Kwon", link: "https://kwonlab.wixsite.com/mysite/members" },
            { name: "Jinhyun Kim", link: "https://bsi.kist.re.kr/dt_team/jinhyun-kim-director-general/" },
            { name: "Ki-Jun Yoon", link: "https://www.yoonlab.info/pi" },
            { name: "Jeong-Soo Lee", link: "https://oak.kribb.re.kr/researcher-profile?ep=360&type=article" },
            { name: "Edward S. Boyden", link: "http://syntheticneurobiology.org/people/display/71/11" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people", isCorresponding: true },
            { name: "Jae-Byum Chang", link: "https://sites.google.com/site/jbchang03/pi?pli=1", isCorresponding: true }
        ],
        venue: { name: "ACS Nano", year: 2025 },
        links: [],
        description: "Expansion microscopy (ExM) for whole vertebrates. Demonstrated nanoscale resolution imaging of whole zebrafish larvae and mouse embryos by expanding them fourfold.",
        highlighted: false
    });

    // Multi-scale J-invariant Paper
    addPaperCard({
        id: "multiscale-jinvariant",
        imageSrc: "images/wacv2025.png",
        imageAlt: "multiscale-jinvariant",
        title: "Design principles of multi-scale J-invariant networks for self-supervised image denoising",
        titleLink: "",
        keywords: [
            { text: "Denoising", color: "#e63946" },
            { text: "Self-supervised Learning", color: "#495057" }
        ],
        authors: [
            { name: "Hayeong Yu", isFirst: true, link: "https://nica.kaist.ac.kr/people" },
            { name: "Seungjae Han", isStrong: true, isFirst: true },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people" }
        ],
        venue: {
            name: "WACV",
            year: 2025,
            extras: '<strong>(<span style="color: #FD3029;">Selected for oral presentation</span>)</strong>'
        },
        links: [],
        description: "We report the theoretical design principles of self-supervised denoising networks and demonstrate that a U-Net-shaped blind spot network achieves superior denoising performance at low computational cost.",
        highlighted: false
    });

    // Neuromorphic Analog Computing Paper
    addPaperCard({
        id: "neuromorphic-analog",
        imageSrc: "images/natelect2025.png",
        imageAlt: "neuromorphic-analog",
        title: "Self-supervised video processing with self-calibration on an analogue computing platform based on a selector-less memristor array",
        titleLink: "",
        keywords: [
            { text: "Neuromorphic AI", color: "#355070" },
            { text: "Memristor", color: "#495057" }
        ],
        authors: [
            { name: "Hakcheon Jeong", isFirst: true },
            { name: "Seungjae Han", isStrong: true, isFirst: true },
            { name: "See-On Park" },
            { name: "Tae Ryong Kim" },
            { name: "Jongmin Bae" },
            { name: "Taehwan Jang" },
            { name: "Yoonho Cho" },
            { name: "Seokho Seo" },
            { name: "Hyun-Jun Jeong" },
            { name: "Seungwoo Park" },
            { name: "Taehoon Park" },
            { name: "Juyoung Oh" },
            { name: "Jeongwoo Park" },
            { name: "Kwangwon Koh" },
            { name: "Kang-Ho Kim" },
            { name: "Dongsuk Jeon" },
            { name: "Inyong Kwon" },
            { name: "Young-Gyu Yoon", link: "https://nica.kaist.ac.kr/people", isCorresponding: true },
            { name: "Shinhyun Choi", isCorresponding: true }
        ],
        venue: {
            name: "Nature Electronics",
            year: 2025,
            extras: '<strong>(<a href="https://breakthroughs.kaist.ac.kr/sub02/view/id/4062" target="_blank" style="color: #FD3029; text-decoration: underline;">KAIST Breakthrough</a>, <a href="https://news.kaist.ac.kr/news/html/news/?mode=V&mng_no=43590" target="_blank" style="color: #FD3029; text-decoration: underline;">KAIST News</a>, <a href="https://www.nature.com/articles/s41928-025-01341-1" target="_blank" style="color: #FD3029; text-decoration: underline;">Nature Electronics News & Views</a>, <a href="https://www.nature.com/articles/s41928-025-01361-x" target="_blank" style="color: #FD3029; text-decoration: underline;">Nature Electronics Editorials</a>)</strong>'
        },
        links: [],
        description: "We report a neuromorphic analog computing platform with self-calibration that can perform self-supervised video processing in real time.",
        highlighted: true
    });
}

// Run initialization when DOM is ready
console.log('papers.js loaded, document.readyState:', document.readyState);

function runInitialization() {
    console.log('runInitialization called, checking for papers-grid...');
    const papersGrid = document.querySelector('.papers-grid');
    if (papersGrid) {
        console.log('papers-grid found, initializing...');
        initializePapers();
    } else {
        console.log('papers-grid not found yet, retrying...');
        setTimeout(runInitialization, 100);
    }
}

if (document.readyState === 'loading') {
    console.log('Waiting for DOMContentLoaded...');
    document.addEventListener('DOMContentLoaded', function () {
        console.log('DOMContentLoaded fired');
        runInitialization();
    });
} else {
    // DOM is already loaded, run immediately but check if element exists
    console.log('DOM already loaded, running runInitialization');
    runInitialization();
}

