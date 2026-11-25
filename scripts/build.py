#!/usr/bin/env python3
"""Rebuild The Pit Report's generated files from editions.json.

Run from the repo root after writing today's YYYY-MM-DD.html and adding its
entry to the top of editions.json:

    python3 scripts/build.py

It does four things, and nothing else:
  1. index.html   <- exact copy of the newest edition's file
  2. archive.html <- regenerated from editions.json (newest first, by month)
  3. feed.xml     <- regenerated from editions.json (newest first)
  4. previous edition: its disabled forward arrow becomes a live link to today

It also fails loudly if any edition HTML contains an em dash.
"""
import html
import json
import re
import shutil
import sys
from datetime import date, datetime
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
CENTRAL = ZoneInfo("America/Chicago")
FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800"
         "&family=Archivo:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600"
         "&family=Kaushan+Script&display=swap")

THEME_SCRIPT = """<script>
  (function () {
    var btn = document.getElementById('modeToggle');
    function apply(dark) {
      document.body.classList.toggle('dark-mode', dark);
      btn.textContent = dark ? '☀️' : '\U0001F319';
    }
    var saved = null;
    try { saved = localStorage.getItem('pit-theme'); } catch (e) {}
    apply(saved === 'dark');
    btn.addEventListener('click', function () {
      var dark = !document.body.classList.contains('dark-mode');
      apply(dark);
      try { localStorage.setItem('pit-theme', dark ? 'dark' : 'light'); } catch (e) {}
    });
  })();
</script>"""

SEARCH_SCRIPT = """<script>
  (function () {
    var input = document.getElementById('archiveSearch');
    input.addEventListener('input', function () {
      var q = input.value.toLowerCase().trim();
      document.querySelectorAll('.archive-entry').forEach(function (entry) {
        var text = entry.getAttribute('data-search') || '';
        entry.style.display = (!q || text.indexOf(q) !== -1) ? '' : 'none';
      });
      document.querySelectorAll('.archive-month').forEach(function (month) {
        var el = month.nextElementSibling, any = false;
        while (el && !el.classList.contains('archive-month')) {
          if (el.style.display !== 'none') { any = true; }
          el = el.nextElementSibling;
        }
        month.style.display = any ? '' : 'none';
      });
    });
  })();
</script>"""


def short_date(d: date) -> str:
    return f"{d.strftime('%b')} {d.day}"


def long_date(d: date) -> str:
    return f"{d.strftime('%A')}, {d.strftime('%B')} {d.day}, {d.year}"


def build_archive(data: dict) -> str:
    e = html.escape
    parts = []
    current_month = None
    for i, ed in enumerate(data["editions"]):
        d = date.fromisoformat(ed["date"])
        month = d.strftime("%B %Y")
        if month != current_month:
            parts.append(f'  <div class="archive-month">{month}</div>')
            current_month = month
        search = " ".join([ed["date"], ed["day_of_week"], ed["headline"], ed["teaser"]]).lower()
        badge = '\n      <span class="badge-latest">Latest</span>' if i == 0 else ""
        parts.append(f"""  <div class="archive-entry" data-search="{e(search)}">
    <div class="ae-meta">
      <span class="ae-num">No. {ed['edition']}</span>
      <span class="ae-date">{long_date(d)}</span>{badge}
    </div>
    <a class="ae-headline" href="{e(ed['filename'])}">{e(ed['headline'])}</a>
    <p class="ae-teaser">{e(ed['teaser'])}</p>
  </div>""")
    entries = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Pit Report · Archive</title>
  <meta name="theme-color" content="#f2f3f7">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <link rel="alternate" type="application/rss+xml" title="The Pit Report RSS Feed" href="feed.xml">
</head>
<body>

<nav class="edition-nav">
  <a href="index.html">← Latest Edition</a>
  <span class="nav-right">
    <span class="nav-archive-label">📁 Archive</span>
    <button class="mode-toggle" id="modeToggle" aria-label="Toggle light and dark mode">🌙</button>
  </span>
</nav>

<header class="masthead">
  <div class="masthead-vol">Vol. I · Est. November 2026 · Bone Daddy Crew</div>
  <h1 class="masthead-title">The Pit Report</h1>
  <div><span class="masthead-diamond">◆</span><span class="masthead-tagline">Every edition. Every wipeout. Forever.</span><span class="masthead-diamond">◆</span></div>
  <hr class="masthead-rule">
  <div class="masthead-dateline">Archive · All Editions</div>
</header>

<div class="archive-wrap">
  <div class="archive-search-bar">
    <input type="text" id="archiveSearch" placeholder="Search by date, trader, or headline…" autocomplete="off" aria-label="Search editions">
  </div>

{entries}
</div>

<footer class="page-footer">
  <p>The Pit Report · Vol. I · Archive</p>
  <p>A Bone Daddy crew column. All money simulated. Not affiliated with PitViper.</p>
  <p><a href="index.html">← Latest Edition</a> · <a href="feed.xml">RSS Feed</a></p>
</footer>

{SEARCH_SCRIPT}

{THEME_SCRIPT}
</body>
</html>
"""


def build_feed(data: dict) -> str:
    base = data["site_url"]
    items = []
    for ed in data["editions"]:
        d = date.fromisoformat(ed["date"])
        pub = format_datetime(datetime(d.year, d.month, d.day, 6, 42, tzinfo=CENTRAL))
        url = base + ed["filename"]
        items.append(f"""    <item>
      <title>No. {ed['edition']}: {html.escape(ed['headline'])}</title>
      <link>{url}</link>
      <pubDate>{pub}</pubDate>
      <description><![CDATA[{ed['teaser']}]]></description>
      <guid>{url}</guid>
    </item>""")
    now = format_datetime(datetime.now(CENTRAL).replace(microsecond=0))
    body = "\n\n".join(items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>The Pit Report</title>
    <link>{base}</link>
    <description>Daily roast-booth recap of the Bone Daddy crew's PitViper sim trading competitions. All money simulated.</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>

{body}
  </channel>
</rss>
"""


def patch_previous(data: dict) -> str | None:
    eds = data["editions"]
    if len(eds) < 2:
        return None
    today, prev = eds[0], eds[1]
    path = ROOT / prev["filename"]
    text = path.read_text(encoding="utf-8")
    label = short_date(date.fromisoformat(today["date"]))
    link = f'<a href="{today["filename"]}">{label} →</a>'
    if link in text:
        return f"{prev['filename']} already links to {today['filename']}"
    new, n = re.subn(r'<span class="nav-disabled">[^<]*→</span>', link, text, count=1)
    if n != 1:
        sys.exit(f"ERROR: no disabled forward arrow found in {prev['filename']}")
    path.write_text(new, encoding="utf-8")
    return f"patched {prev['filename']} forward arrow -> {today['filename']}"


def check_no_em_dashes(data: dict) -> None:
    bad = []
    for ed in data["editions"]:
        if "—" in (ROOT / ed["filename"]).read_text(encoding="utf-8"):
            bad.append(ed["filename"])
        if "—" in ed["headline"] + ed["teaser"]:
            bad.append(f"editions.json entry {ed['edition']}")
    if bad:
        sys.exit("ERROR: em dash found in: " + ", ".join(bad))


def main() -> None:
    data = json.loads((ROOT / "editions.json").read_text(encoding="utf-8"))
    eds = data["editions"]
    eds.sort(key=lambda x: x["date"], reverse=True)
    if data.get("latest_edition") != eds[0]["edition"]:
        sys.exit(f"ERROR: latest_edition={data.get('latest_edition')} but newest entry is No. {eds[0]['edition']}")
    for ed in eds:
        if not (ROOT / ed["filename"]).exists():
            sys.exit(f"ERROR: missing {ed['filename']}")
    check_no_em_dashes(data)

    msg = patch_previous(data)
    shutil.copyfile(ROOT / eds[0]["filename"], ROOT / "index.html")
    (ROOT / "archive.html").write_text(build_archive(data), encoding="utf-8")
    (ROOT / "feed.xml").write_text(build_feed(data), encoding="utf-8")

    print(f"index.html   <- {eds[0]['filename']} (No. {eds[0]['edition']})")
    print(f"archive.html <- {len(eds)} edition(s)")
    print(f"feed.xml     <- {len(eds)} item(s)")
    if msg:
        print(msg)


if __name__ == "__main__":
    main()
