<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog — Rishi Maroju</title>
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
    --amber: #a9c1e4;
    --max: 700px;
  }
  *{ box-sizing: border-box; }
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
  a:focus-visible{ outline: 2px solid var(--teal); outline-offset: 3px; }
 
  .wrap{ max-width: var(--max); margin: 0 auto; padding: 4rem 1.5rem 6rem; }
 
  a.back{
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: var(--slate);
    margin-bottom: 2.4rem;
  }
  a.back:hover{ color: var(--teal); }
 
  h1{
    font-family: 'Newsreader', Georgia, serif;
    font-weight: 600;
    font-size: clamp(2.1rem, 5vw, 2.7rem);
    margin: 0 0 0.7rem;
    letter-spacing: -0.01em;
  }
 
  p.intro{ color: var(--slate); font-size: 1.05rem; max-width: 60ch; margin: 0 0 3rem; }
 
  hr.rule{ border: 0; border-top: 1px solid var(--line); margin: 0 0 2.6rem; }
 
  ol.posts{ list-style: none; margin: 0; padding: 0; border-left: 1px solid var(--line); }
  ol.posts li{ position: relative; padding: 0 0 1.6rem 1.7rem; }
  ol.posts li:last-child{ padding-bottom: 0; }
  ol.posts li::before{
    content: "";
    position: absolute; left: -4.5px; top: 0.35rem;
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--paper); border: 1.5px solid var(--teal);
  }
  .posts .num{
    display: block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: var(--slate);
    margin-bottom: 0.25rem;
  }
  .posts .title{ font-weight: 600; font-size: 1.05rem; }
 
  footer{ font-size: 0.85rem; color: var(--slate); font-family: 'IBM Plex Mono', monospace; margin-top: 4rem; }
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">&larr; Rishi Maroju</a>
 
  <h1>Blog</h1>
  <p class="intro">Posts about data science topics I'm interested in, written throughout the course.</p>
 
  <hr class="rule">
 
  <ol class="posts">
    <li>
      <span class="num">Blog 1</span>
      <a class="title" href="blog/blog1.md">Read the post</a>
    </li>
  </ol>
 
  <footer>Rishi Maroju</footer>
</div>
</body>
</html>

