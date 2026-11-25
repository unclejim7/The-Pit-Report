# The Pit Report

A ruthless, ESPN-booth-style daily roast column on the Bone Daddy crew's
PitViper sim trading competitions. All money is simulated.

**Live:** https://unclejim7.github.io/The-Pit-Report/

## How it's laid out

| File | What it is |
|---|---|
| `index.html` | Today's edition (copy of the newest dated file) |
| `YYYY-MM-DD.html` | Permanent archive copy of each edition |
| `archive.html` | Searchable list of every edition |
| `editions.json` | Edition index: number, date, headline, teaser, stats |
| `feed.xml` | RSS feed |
| `style.css` | Shared styles, matched to the PitViper app's colors and fonts |
| `scripts/build.py` | Regenerates index, archive, feed and the previous edition's forward link |
| `skill/the-pit-report/` | The "run tpr" production skill |

## Daily run

1. Write `YYYY-MM-DD.html` (copy yesterday's, change content).
2. Prepend the new entry to `editions.json` and bump `latest_edition`.
3. `python3 scripts/build.py`
4. Commit to `main` and push. GitHub Pages redeploys in about a minute.

Full instructions: `skill/the-pit-report/SKILL.md`.
