# The Pit Report · Page Structure Reference

The newest `YYYY-MM-DD.html` in the repo is the canonical template. Copy it and
change content only. This file documents each block so you know what goes where.

Design follows the PitViper app's tokens (all in `style.css`): light "paper"
default, cobalt `#0a21c0`, green `#1f7a4d` up, red `#b3202c` down, obsidian
`#07080f` dark mode. Fonts: Kaushan Script (wordmark, sign-off), Bricolage
Grotesque (headlines), Archivo (body), IBM Plex Mono (numbers, meta lines).

## `<head>` (copy verbatim, change title and description)

```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Pit Report · No. [N] · [Month D, YYYY]</title>
<meta name="description" content="[one-line teaser]">
<meta name="theme-color" content="#f2f3f7">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Kaushan+Script&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="alternate" type="application/rss+xml" title="The Pit Report RSS Feed" href="feed.xml">
```

## Nav

```html
<nav class="edition-nav">
  <a href="[prev-date].html">← [Prev Mon D]</a>
  <span class="nav-right">
    <a href="archive.html" class="nav-archive">📁 Archive</a>
    <span class="nav-disabled">[Next Mon D] →</span>
    <button class="mode-toggle" id="modeToggle" aria-label="Toggle light and dark mode">🌙</button>
  </span>
</nav>
```

## Ticker

```html
<div class="ticker-wrap" aria-hidden="true">
  <div class="ticker-track">
    <span>[ALL CAPS ITEM]</span><span class="ticker-dot">◆</span>
    <!-- 6 to 9 items, then the SAME items again for a seamless loop -->
  </div>
</div>
```

## Masthead

```html
<header class="masthead">
  <div class="masthead-vol">Vol. I · No. [N] · Est. November 2026 · Bone Daddy Crew</div>
  <h1 class="masthead-title">The Pit Report</h1>
  <div>
    <span class="masthead-diamond">◆</span>
    <span class="masthead-tagline">[Daily tagline, fresh each day]</span>
    <span class="masthead-diamond">◆</span>
  </div>
  <hr class="masthead-rule">
  <div class="masthead-dateline">From the PitViper Trenches · [Weekday], [Month D, YYYY]</div>
  <div class="masthead-url">unclejim7.github.io/The-Pit-Report</div>
</header>
```

## Scoreboard (4 tiles)

```html
<div class="scoreboard">
  <div class="scoreboard-inner">
    <div class="sb-item">
      <div class="sb-label">Yesterday's Winner</div>
      <div class="sb-value">[Trader]</div>
      <div class="sb-sub">+$X,XXX.XX final</div>
    </div>
    <!-- Active Streak · Crew Comps Finished · Bitcoin -->
  </div>
</div>
```

## Body wrapper

Everything from the lead story to the sign-off sits in `<div class="pit-body">`.

### Lead story

```html
<section class="lead-story">
  <div class="lead-kicker">Headline · [Comp] · [Angle]</div>
  <h2 class="lead-headline">[Headline]</h2>
  <div class="lead-body">
    <p>...</p>
    <p>...</p>
  </div>
</section>
```

### Section heading + subline

```html
<h3 class="section-head">Yesterday's Final: Crypto Daily, [Day Mon D]</h3>
<p class="section-sub">Finalized at midnight. [One-line roast.]</p>
```

### Standings table

```html
<div class="table-wrap">
  <table class="pit-table">
    <thead><tr><th>#</th><th>Trader</th><th>Equity</th><th>P&amp;L</th><th>Booth says</th></tr></thead>
    <tbody>
      <tr class="leader"><td class="rank">1</td><td class="who">[Trader]</td><td class="num">$16,068.13</td><td class="num chg-up">+$6,068.13</td><td class="booth">[roast]</td></tr>
      <tr class="wiped"><td class="rank">5</td><td class="who">[Trader]</td><td class="num">$0.00</td><td class="num chg-dn">−$10,000.00</td><td class="booth">[roast]</td></tr>
    </tbody>
  </table>
</div>
```

Hall of Fame table uses the same markup with columns
`Member · Entered · Won · Comp profit · Scouting report` (no rank column).

### Cards and quote

```html
<article class="story-card gold">   <!-- streaks / trophies -->
  <h4 class="card-head">[Title]</h4>
  <p>...</p>
</article>
<article class="story-card hot">    <!-- wipeouts / jab wars -->
  ...
</article>
<blockquote class="pull-quote">
  "[Jab text, quoted exactly]"
  <cite>[Who, context]</cite>
</blockquote>
```

### Lists

```html
<ul class="pit-list">
  <li><strong>[Name]</strong> is #1 all-time at <span class="chg-up">+$19,130.23</span>. [roast]</li>
</ul>
```

### Prediction and sign-off

```html
<div class="prediction"><p>[Prediction]</p></div>
<div class="sign-off">That's the Pit Report. Trade responsibly. Jab irresponsibly.</div>
```

## Footer

```html
<footer class="page-footer">
  <p>The Pit Report · Vol. I, No. [N] · [Month D, YYYY]</p>
  <p>A Bone Daddy crew column. All money simulated. Not affiliated with PitViper. Roasts are friendly fire.</p>
  <p><a href="archive.html">📁 Archive</a> · <a href="feed.xml">RSS Feed</a></p>
</footer>
```

## Theme script

Copy the `<script>` block before `</body>` from the previous edition exactly. It
toggles `body.dark-mode` and remembers the choice in localStorage (key `pit-theme`).
