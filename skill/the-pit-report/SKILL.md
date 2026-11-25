---
name: the-pit-report
description: Produce a new edition of The Pit Report, a ruthless ESPN-booth-style daily roast column on the Bone Daddy crew's PitViper sim trading competitions, published to GitHub Pages at unclejim7/The-Pit-Report (unclejim7.github.io/The-Pit-Report). Use whenever the user types "run tpr", "run the pit report", "new pit report", or the Daily Pit Report scheduled task fires. Governs the full sequence: read PitViper (read-only), write the edition HTML, update editions.json, run the build script, and push.
---

# The Pit Report · Production Skill

A daily roast-comic recap of J's PitViper sim trading competitions. J trades as
**Uncle_Jim** in the crew **Bone Daddy**. All money is simulated.

**Live site:** unclejim7.github.io/The-Pit-Report
**Repo:** github.com/unclejim7/The-Pit-Report (publishes from `main`, repo root)

---

## Files Per Run

You hand-write TWO things. The build script writes the rest.

| File | Who writes it |
|---|---|
| `YYYY-MM-DD.html` | You. Today's edition. |
| `editions.json` | You. Prepend today's entry, bump `latest_edition`. |
| `index.html` | `scripts/build.py` (copy of today's file) |
| `archive.html` | `scripts/build.py` (from editions.json) |
| `feed.xml` | `scripts/build.py` (from editions.json) |
| `[prev-date].html` | `scripts/build.py` (forward arrow becomes a live link) |
| `style.css` | Nobody, unless the design changes. Shared by every page. |

Never hand-edit `index.html`, `archive.html` or `feed.xml`.

---

## Step 1 · Orient

1. Get today's date in America/Chicago.
2. Get the repo: use the local clone if there is one (`git pull` first), otherwise
   read files from GitHub.
3. From `editions.json`: `latest_edition` + 1 is today's number. The top entry is
   the previous edition (its `filename` and `date`). Read that previous edition's
   HTML: it is your template AND your memory of running storylines and jokes
   already used.

---

## Step 2 · Gather Data (PitViper MCP, READ-ONLY)

NEVER place bets, click trade buttons, or send jabs. Read only.

1. `pitviper_status`: confirm signed in, list current competitions.
2. `pitviper_open /groups/369a398b-7825-4c43-b736-52022e8c8b46`: Bone Daddy crew
   page (past results, streaks, competition record table, crew leaderboard).
3. `pitviper_open /competitions/<id>`: YESTERDAY's finalized Crypto Daily (it
   finalizes at midnight) and TODAY's live one (field, equity, P&L, open
   positions, jabs).
4. `pitviper_open /leaderboard`: global all-time board.
5. Discover page: upcoming comps and BTC price.

Every number in the edition comes from these pages. Compute differences
exactly. If a page fails to load, say so in the edition rather than guessing.

---

## Step 3 · Write `YYYY-MM-DD.html`

Start from the previous edition's file and keep its exact structure, class
names, `<head>`, fonts and theme script. Read `references/page-structure.md`
for each block's markup.

Update:
- `<title>`: `The Pit Report · No. [N] · [Month D, YYYY]`
- Nav: `← [Prev Mon D]` links to the previous file; forward arrow is
  `<span class="nav-disabled">[Next Mon D] →</span>` (build.py turns it live
  tomorrow).
- Ticker: 6 to 9 ALL CAPS items, then the exact same items again (seamless loop).
- Masthead vol line: `Vol. I · No. [N] · Est. November 2026 · Bone Daddy Crew`;
  dateline: `From the PitViper Trenches · [Weekday], [Month D, YYYY]`.
- Scoreboard: 4 tiles (yesterday's winner, active streak, crew comps
  finished, BTC). Mono subline under each.
- Footer: `The Pit Report · Vol. I, No. [N] · [Month D, YYYY]`.

Sections, in order (this is the morning-recap format J chose):
1. **Headline story** (`.lead-story`): yesterday's FINAL result is the main story.
2. **Yesterday's Final**: winner crowned, full final table (`.pit-table`).
3. **Today's Live Standings**: table with a one-line "Booth says" roast per trader.
4. **Streak Watch**: streaks and the jab war. Quote jabs and dunk on them.
   Use `.story-card`, `.story-card.gold` (streaks) and `.story-card.hot` (wipeouts,
   jab wars), plus an optional `.pull-quote`.
5. **Crew Hall of Fame (and Mostly Shame)**: record table with brutal scouting reports.
6. **Global Board Check-In** (`.pit-list`).
7. **On Deck** (`.pit-list`) plus BTC line.
8. **The Booth's Prediction** (`.prediction`).
9. Sign-off (`.sign-off`): `That's the Pit Report. Trade responsibly. Jab irresponsibly.`

Table conventions: money cells get `class="num"`, plus `chg-up` / `chg-dn`.
Leader row gets `class="leader"`; a trader at $0.00 gets `class="wiped"`.
Negative money uses the true minus sign `−` (U+2212), e.g. `−$2,614.46`.

---

## Step 4 · Style Rules (non-negotiable)

- RUTHLESS roast-comic energy. Everyone gets roasted, Uncle_Jim included (he's an
  accountant, use it).
- Absurd comparisons. Call out all-in bets, tiny profit on huge risk, wipeouts,
  choking, no-shows, hypocritical jabs.
- ALL CAPS for emphasis. Fresh jokes daily: check the previous edition and do not
  recycle lines.
- Build running storylines across days (streaks, rivalries, grudges). Reference
  what the Booth predicted yesterday and whether it came true.
- Friendly fire only: roast trading, handles, results, comp behavior. Nothing
  about real life, looks, identity, nothing hateful.
- **NO EM DASHES. Ever.** (build.py refuses to run if it finds one.)

---

## Step 5 · Update `editions.json`

Prepend (newest first) and set `latest_edition` to N:

```json
{
  "edition": 2,
  "date": "2026-11-26",
  "day_of_week": "Thursday",
  "filename": "2026-11-26.html",
  "headline": "[Lead headline]",
  "teaser": "[2 to 3 sentence roast teaser]",
  "stats": {
    "btc": 59115,
    "winner": "[yesterday's winner]",
    "winner_pnl": 6068.13,
    "leader": "[today's live leader]",
    "uncle_jim_pnl": 1284.39,
    "uncle_jim_rank": 3,
    "streak": "Uncle_Jim W4",
    "crew_comps_finished": 29
  }
}
```

Include whatever stats you gathered; omit any you could not get.

---

## Step 6 · Build

From the repo root:

```bash
python3 scripts/build.py
```

It copies today's file to `index.html`, regenerates `archive.html` and
`feed.xml`, patches the previous edition's forward arrow, and checks for em
dashes and missing files. Fix anything it reports and re-run.

---

## Step 7 · Publish

Commit everything to `main` in one commit, message
`The Pit Report No. [N]: [Month D, YYYY]`, and push (local `git push`, or the
GitHub tools' multi-file push if there is no clone). GitHub Pages redeploys in
about a minute.

Finish with a short production note: edition number, lead headline, yesterday's
winner, the live link (`https://unclejim7.github.io/The-Pit-Report/YYYY-MM-DD.html`),
and any data gaps.
