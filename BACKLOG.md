# MLB Bet Tracker - Backlog

Items to explore / build. Not yet implemented. (Started 2026-06-05.)

## 1. Alt-strikeout detection (auto-grade pitcher K-total legs) - DONE (shipped 2026-06-08)
- Now: pitcher "alt strikeout" legs (e.g. Yesavage 6+ K inside SGP #5xk3) are flagged NA/manual and do NOT auto-settle.
- Goal: auto-grade by reading the pitcher's total strikeouts from the live boxscore (statsapi pitching.strikeOuts), mark the leg hit when total >= threshold.
- Notes: strikeout totals are a standard, widely-available box-score stat - no reason it can't be tracked. Needs a new prop code (e.g. ALTK with a threshold field) + capture pitcher total K into the stats map. Build as its own proper step, not crammed into a daily slate roll.

## 2. Moneyline detection (team-wins legs)
- Now: moneyline legs (e.g. Astros ML, Dodgers ML in #k46d / #04vk) are flagged manual.
- Goal: at Final, compare the two teams' scores and grade the selected team's leg win/loss.
- Notes: these particular ones were placeholder fillers (lower priority), but the mechanic is easy (final score from linescore). New non-player leg type - needs render handling for a leg with no player.

## 3. Total-runs-over detection
- Now: "Over 9.0 Total Runs" legs (in #k46d / #04vk) are flagged manual.
- Goal: grade total game runs vs the line from the linescore at Final (push handling if exactly on the line).

## 4. Futures handling (season-long award bets)
- Now: futures legs (Cy Young / ROY / MVP - e.g. bets #trfbj #avfc1 #q11x4 #az4k0) are flagged NA/manual; they show but never auto-settle.
- They can't be graded by the live game engine - no per-game stat decides a season award, and they settle at season end (~late Sept).
- Goal: design a sensible way to handle/display futures distinctly from live game bets. Options to explore: a separate Futures section/tab, no live grading, a manual settle toggle, or just a clear season-end note. Don't track them like live bets.
- 2026-06-08: futures are now HIDDEN from the live display (filtered out at render; all 4 bets retained in the data file). Re-enable / build proper treatment when this item is picked up.

## 5. Search by player name (nice-to-have)
- Goal: a search / filter box on the Bets tab - type a player or pitcher name and show only the bets containing that person.
- Gets more useful as the bet list grows; quickly pull up every bet riding on a given guy.
- Priority: nice-to-have, not urgent.

## 6. Revise Hitters-tab result badge (the field to the right of each player's name)
- Now: one badge per player by priority HR > 4+ TB > (has-hit-prop AND >=1 hit) > muted hit count > odds/hyphen.
- PROBLEM (surfaced by the 6/8 settled-bet review): the green check badges fire on RAW live stats, not on the player's actual bet line. A player who needed 2+/3+/4+ hits but has 1 still shows a positive "check 1 H" even though that bet LOST - e.g. Alec Bohm went 1-of-4 hits on 6/8 and the SGP settled $0.00, but the Hitters row reads like a win. It conflates "got a hit" with "bet won."
- Also: TB badge is hardcoded at >=4 regardless of the real line (2+/3+/5+); SB / RBI / runs / doubles / triples props are not surfaced at all; only one prop is shown even when a player rides several different bets.
- GOAL: tie the badge to actual leg/bet status (hit/miss/pending) and/or show the player's real threshold, so the Hitters tab reflects true outcomes instead of a raw-stat heuristic. Needs a rethink of what this tab is for.

## 7. Cloud build + auto-deploy (GitHub Actions) - FOUNDATION for phone deploys
- Now: every deploy runs through Desktop Commander on the Windows desktop (edit staging -> python build -> git push). Phone cannot run DC, so no deploys from phone.
- Goal: a GitHub Actions workflow that runs the existing python build whenever the staging file changes, then publishes. Then "deploy a bet" = "update the staging file in the repo" - no desktop, no DC.
- Verified preconditions (2026-06-11): build is stdlib-only (json, datetime), no build-time network -> CI-friendly; repo is PUBLIC -> Actions free + unlimited; Pages serves from main branch (legacy).
- Token note: current gh token scopes are repo/gist/read:org - MISSING 'workflow' scope. Adding/modifying .github/workflows/*.yml is REJECTED until 'gh auth refresh -s workflow' is run (or the file is created via GitHub web).
- Refactor included: consolidate per-day buildjN.py + gen_bets.py into ONE parameterized build that reads the staging file (date + games derivable) so no per-day hand-editing. Staging file becomes single source of truth.

## 8. Phone bet entry: screenshot -> live (depends on #7)
- Goal: from iPhone, screenshot a FanDuel bet -> it goes live. Once #7 exists, the only remaining step is "write the bet into the staging file from the phone."
- Paths to write staging from phone (ranked):
  - (a) Claude mobile + GitHub connector commits staging directly. Simplest IF the connector can WRITE - UNVERIFIED, must test.
  - (b) Claude mobile + Google Drive connector (write VERIFIED via create_file) writes bet to a Google Sheet/Drive file -> free Google Apps Script bridge (time trigger) commits to GitHub / fires repository_dispatch -> Action builds. More setup, write step proven.
  - (c) Claude mobile extracts bet -> Damien pastes JSON into staging via GitHub mobile web -> Action builds. Works day one, no connector dependency, 2 taps.
- Safety: always echo parsed bet back for confirm-before-publish; a misread ID/odds must not go live silently.

## 9. iOS Shortcut one-tap deploy (needs Anthropic API key) - future, optional
- Goal: Share-sheet Shortcut: screenshot -> Claude API extracts bet JSON -> GitHub API commits staging -> Action builds+deploys. One tap from FanDuel, no chat app.
- Cost: pay-per-use Claude API (~a cent or two per bet) + Anthropic API key with credits. GitHub API free.
- Most automated; most setup. Park until #7 + a chosen #8 path work.

## 10. ACTION ITEM: Verify GitHub connector WRITE capability (blocks #8 path a)
- Question: can Claude's GitHub connector create/update files (commit) in damienreilley/mlb-hr-tracker, or is it read-only?
- How to verify: TC-1 - in Claude MOBILE (GitHub connector enabled), ask Claude to create a test file in the repo. Pass = file appears in repo; Fail = connector cannot write.
- If PASS: path 8(a) viable - "upload screenshot, Claude commits staging" works with NO bridge needed.
- If FAIL: use path 8(b) Google Drive connector (write verified via create_file) + Apps Script bridge, or 8(c) manual paste.
- Status: TC-1 run on phone 2026-06-11; result pending.

## 11. ACTION ITEM: Vercel vs GitHub Pages - level-of-effort vs benefit assessment
- Question: move hosting to Vercel now, or stay on GitHub Pages + Actions?
- Findings: Vercel account active (damienreilley@gmail.com), used for March 2026 Master Bet Tracker (fanduel-bet-tracker repo, auto-deploys on push). Verified via Gmail + past-chat history 2026-06-11.
- Tradeoff: GitHub Pages+Actions = simplest/free/already-hosted, but CANNOT host an API endpoint. Vercel = one platform for site + serverless processing (the future screenshot->bet API) + fancier-app features (functions, KV/Postgres, auth); more setup.
- Damien WILL want a fancier app -> Vercel is the stronger LONG-TERM foundation; keep close.
- Decision rule (Damien): if LOE to move is more than "pretty simple," TABLE to short-future. Do GitHub Actions now as the stepping stone; the refactored single build script carries over to Vercel later (no wasted work).

## TC-1 RESULT (2026-06-11) - GitHub connector is READ-ONLY (path 8a DEAD)
- Tested on phone (Claude mobile) AND web. Both confirm: the "GitHub Integration" connector is Anthropic's
  NATIVE connector (chat file-attach, Projects sync, Claude Code). It does NOT expose a write/commit MCP tool.
  tool_search found no GitHub write tool in either session.
- Phone: GitHub connector not present in the mobile connector list (only Gmail, Google Drive, Spotify,
  StubHub, Uber, Canva, Vercel). Google Drive IS present on phone - good for path 8b.
- Web: same result; web chat also offered to search the registry for a GitHub MCP server (a THIRD-PARTY
  GitHub MCP, distinct from the native connector, MIGHT expose write tools - but likely not on mobile;
  added dependency; does not solve phone-first). Noted, not pursued.
- CONCLUSION: path 8(a) "Claude commits staging via GitHub connector in chat" is NOT viable. Removed.
- Live phone-write options now:
   #9  iOS Shortcut (Claude API + GitHub API) - sidesteps connectors entirely; STRONGEST automated path
       (Damien has API credit). Tokens stored on-device.
   8(c) manual paste into staging via GitHub mobile web - zero build, works once #7 exists; 2 taps.
   8(b) Drive connector + Apps Script bridge - needs TC-2 (confirm Drive WRITE works on phone); more moving parts.
   future: Vercel /api/add-bet serverless endpoint.
- SECURITY NOTE: do NOT put a GitHub token inside a web artifact (client-side JS). Token-bearing writes
  belong in Desktop Commander, an on-device iOS Shortcut, or a server-side function.
- FOUNDATION (#7 GitHub Actions cloud build) is required by ALL remaining paths and depends on no connector.
