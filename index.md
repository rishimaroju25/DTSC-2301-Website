<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Rishi Maroju — Data Science</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --paper: #0a0c10;
    --paper-alt: #11141a;
    --ink: #eceef1;
    --slate: #9aa1ab;
    --line: #262a32;
    --teal: #7ea2d1;
    --teal-dim: #1c2836;
    --amber: #a9c1e4;
    --max: 700px;
  }

  *{ box-sizing: border-box; }

  html{ scroll-behavior: smooth; }

  body{
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: 'IBM Plex Sans', -apple-system, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }

  a{ color: var(--teal); text-decoration-thickness: 1px; text-underline-offset: 3px; }
  a:hover{ color: var(--amber); }
  a:focus-visible, button:focus-visible{ outline: 2px solid var(--teal); outline-offset: 3px; }

  .wrap{
    max-width: var(--max);
    margin: 0 auto;
    padding: 5rem 1.5rem 6rem;
  }

  /* ---------- Masthead ---------- */

  header.masthead{
    margin-bottom: 3.5rem;
    opacity: 0;
    animation: rise .7s ease-out forwards;
  }
  @keyframes rise{
    from{ opacity: 0; transform: translateY(8px); }
    to{ opacity: 1; transform: translateY(0); }
  }
  @media (prefers-reduced-motion: reduce){
    header.masthead{ animation: none; opacity: 1; }
  }

  .spark{
    display:block;
    margin-bottom: 1.4rem;
  }
  .spark path{
    stroke: var(--teal);
    stroke-width: 2;
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
  }
  .spark circle{ fill: var(--amber); }

  h1.name{
    font-family: 'Newsreader', Georgia, serif;
    font-weight: 600;
    font-size: clamp(2.4rem, 6vw, 3.1rem);
    line-height: 1.05;
    margin: 0 0 0.6rem;
    letter-spacing: -0.01em;
  }

  p.role{
    font-size: 1.05rem;
    color: var(--slate);
    margin: 0 0 1.2rem;
  }
  p.role .dot{ color: var(--line); margin: 0 0.5em; }

  nav.links{
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem 1.4rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.86rem;
  }
  nav.links a{ white-space: nowrap; }

  hr.rule{
    border: 0;
    border-top: 1px solid var(--line);
    margin: 0 0 3rem;
  }

  /* ---------- Sections ---------- */

  section{ margin-bottom: 3.4rem; }

  h2.section-title{
    font-family: 'Newsreader', Georgia, serif;
    font-style: italic;
    font-weight: 500;
    font-size: 1.5rem;
    margin: 0 0 1.1rem;
    color: var(--ink);
  }

  .lede{
    font-size: 1.08rem;
    max-width: 62ch;
  }
  .lede + .lede{ margin-top: 1.1rem; }

  /* ---------- Record (timeline) ---------- */

  ol.record{
    list-style: none;
    margin: 0;
    padding: 0;
    border-left: 1px solid var(--line);
  }

  ol.record li{
    position: relative;
    padding: 0 0 1.9rem 1.7rem;
  }
  ol.record li:last-child{ padding-bottom: 0; }

  ol.record li::before{
    content: "";
    position: absolute;
    left: -4.5px;
    top: 0.35rem;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--paper);
    border: 1.5px solid var(--teal);
  }

  .record .when{
    display: block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: var(--slate);
    margin-bottom: 0.25rem;
  }

  .record .what{
    font-weight: 600;
    margin: 0 0 0.2rem;
  }

  .record .where{
    color: var(--slate);
    font-size: 0.96rem;
  }

  .record .detail{
    margin: 0.5rem 0 0;
    font-size: 0.98rem;
  }

  /* ---------- Elsewhere (index of links) ---------- */

  ul.index{
    list-style: none;
    margin: 0;
    padding: 0;
  }
  ul.index li{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1rem;
    padding: 0.7rem 0;
    border-bottom: 1px dotted var(--line);
  }
  ul.index li:first-child{ border-top: 1px dotted var(--line); }

  ul.index .label{ font-weight: 500; }
  ul.index .note{
    font-size: 0.85rem;
    color: var(--slate);
    font-family: 'IBM Plex Mono', monospace;
    text-align: right;
  }

  footer{
    font-size: 0.85rem;
    color: var(--slate);
    font-family: 'IBM Plex Mono', monospace;
  }

  @media (max-width: 480px){
    .wrap{ padding: 3.2rem 1.25rem 4rem; }
    ul.index li{ flex-direction: column; gap: 0.15rem; }
    ul.index .note{ text-align: left; }
  }
</style>
</head>
<body>
<div class="wrap">

  <header class="masthead">
    <svg class="spark" width="120" height="28" viewBox="0 0 120 28" aria-hidden="true">
      <path d="M2 22 L22 10 L40 18 L60 6 L80 15 L100 8 L118 14" />
      <circle cx="118" cy="14" r="3"></circle>
    </svg>

    <h1 class="name">Rishi Maroju</h1>
    <p class="role">Data Science student, UNC Charlotte<span class="dot">·</span>Data Science &amp; Automation Intern</p>

    <nav class="links">
      <a href="Rishi_Maroju_Resume.pdf">Resume (PDF)</a>
      <a href="#">LinkedIn</a>
      <a href="https://github.com/rishimaroju25">GitHub</a>
      <a href="blog.md">Blog</a>
      <a href="projects.md">Projects</a>
    </nav>
  </header>

  <hr class="rule">

  <section id="about">
    <h2 class="section-title">About</h2>
    <p class="lede">
      I study data science at UNC Charlotte, with minors in artificial intelligence and statistics.
      My coursework runs through database design, predictive analytics, and applied multivariate
      analysis — and I try to pair each of those with something hands-on rather than leave it on paper.
    </p>
    <p class="lede">
      That currently means cleaning and clustering large datasets as a Data Science &amp; Automation
      Intern at Cacheconomy, and separately doing the same kind of work at Advocations. On the research
      side, I'm modeling how artificial neural networks, MC dropout, and Gaussian processes can stand in
      for biological neural network activity. Outside of coursework, I mentor two students through UNC
      Charlotte's Mentor Collective, and I previously ran logistics for a multi-team collegiate dance
      network.
    </p>
  </section>

  <section id="record">
    <h2 class="section-title">Record</h2>
    <ol class="record">
      <li>
        <span class="when">Fall 2026 —</span>
        <p class="what">Research Assistant</p>
        <p class="where">Studying ANNs, MC dropout &amp; Gaussian processes as models of biological neural activity</p>
      </li>
      <li>
        <span class="when">Mar 2026 —</span>
        <p class="what">Data Science &amp; Automation Intern</p>
        <p class="where">Cacheconomy — cleaning and clustering datasets to surface marketing &amp; business trends</p>
      </li>
      <li>
        <span class="when">Mar 2026 —</span>
        <p class="what">Data Science &amp; Automation Intern</p>
        <p class="where">Advocations — career services &amp; disability-focused job placement</p>
      </li>
      <li>
        <span class="when">Ongoing</span>
        <p class="what">Mentor, UNC Charlotte Mentor Collective</p>
        <p class="where">Mentoring two students</p>
      </li>
    </ol>
  </section>

  <section id="elsewhere">
    <h2 class="section-title">Elsewhere</h2>
    <ul class="index">
      <li><span class="label">Blog</span><span class="note">notes &amp; write-ups</span></li>
      <li><span class="label">Projects</span><span class="note">selected work</span></li>
      <li><span class="label">GitHub — rishimaroju25</span><span class="note">source &amp; code</span></li>
      <li><span class="label">Resume</span><span class="note">PDF</span></li>
      <li><span class="label">LinkedIn</span><span class="note">profile</span></li>
    </ul>
  </section>

  <footer>
    Built by Rishi Maroju · hosted on GitHub Pages
  </footer>

</div>
</body>
</html>

