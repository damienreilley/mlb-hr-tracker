# VERCEL - Future Design & Build Reference (MLB / FanDuel Bet Trackers)

Last updated: 2026-06-11. Status: REFERENCE / FUTURE - not active.
Do NOT start any Vercel migration or build from this doc without Damien's explicit go-ahead.

## 0. Why this doc exists
Vercel is parked for FUTURE use - the "fancier app" phase and the fully-automated
phone -> live bet pipeline. This captures everything known so the future build starts
from a complete picture, not rediscovery. The current live tracker (mlb-hr-tracker)
stays on GitHub Pages for now. See BACKLOG.md #7 (cloud build) and #11 (Vercel LOE).

## 1. Account & assets (verified 2026-06-11)
- Vercel account: damienreilley@gmail.com (active; Philadelphia sign-ins Mar 21 & Mar 24 2026 per Gmail).
- Prior project: "Master Bet Tracker" (March 2026).
  - GitHub repo: damienreilley/fanduel-bet-tracker (PRIVATE, main branch).
  - Live URL: https://fanduel-bet-tracker.vercel.app (was serving v1).
  - Local folder: C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\FanDuel\
  - Source chat title: "x0 - Master Bet Tracker Design March 2026 -BAD". The "-BAD" marks early
    BUILD-QUALITY problems (v1 wrong colors, missing settled bets, design/build conflation),
    NOT a Vercel/architecture failure. The GitHub+Vercel architecture was marked "CONFIRMED FINAL".
- vercel.json (proven config, at repo root):
    {
      "outputDirectory": "dashboard",
      "buildCommand": "",
      "installCommand": "",
      "framework": null
    }
  Meaning: serve static files from dashboard/; no build step; no framework. Pure static-host config.

## 2. Proven architecture (what already worked in March)
Data flow:
  FanDuel (browser)
   -> Chrome extension intercepts X-Authentication header -> fd-auth.txt (token); manual copy fallback
   -> Python sync script v4 on Damien's machine: fetch new bets, write versioned JSON to data/
   -> git commit + push to GitHub repo
   -> Vercel auto-deploys in ~30s
   -> https://fanduel-bet-tracker.vercel.app (any device)
Key properties:
- No local server, ever. Vercel hosts everything user-facing.
- Auto-deploy on push to main (~30s). Free.
- Single dashboard/index.html (HTML+JS+CSS, no framework). JSON data in same repo (no CORS).
- Data sync was MANUAL (run script -> push). Auto-sync was flagged as "next phase".

## 3. What Vercel gives us that GitHub Pages does NOT
GitHub Pages = static only. Vercel = static + compute. The compute is the whole point:
- Serverless functions (e.g. /api/add-bet): RECEIVE a bet or screenshot, call the Claude API to
  extract it, update data, trigger redeploy - all on ONE platform. Pages cannot host any endpoint.
- This collapses the phone -> live pipeline: phone POSTs a screenshot to /api/add-bet, function does
  the rest. No GitHub Action + connector + bridge juggling.
- Storage: Vercel KV / Postgres for live bet data instead of a flat JSON file (search, history, multi-day).
- Auth, preview deployments, edge config for a real multi-page app.
- Recent Vercel product emails (2026): "Vercel Sandbox" (persistent sandboxes + Docker), "Workflows GA",
  faster builds - relevant to heavier build/processing later.

## 4. Intended FUTURE uses (the "fancier app")
1. Host the bet tracker front-end on Vercel instead of Pages.
2. Add /api/add-bet serverless function: accepts a FanDuel screenshot (or extracted JSON), uses the
   Claude API (Damien has API credit) to parse via the bet-extraction template, writes to storage,
   updates the live site. THIS is the automated phone->live pipeline, one platform.
3. Move bet data from flat JSON to Vercel KV/Postgres -> enables search-by-player (BACKLOG #5),
   full history, cross-day views, proper futures handling (#4).
4. Optional: iOS Shortcut or a simple web form posts directly to /api/add-bet (ties to BACKLOG #9).
5. Optional: auto-pull from FanDuel (March sync-script + token approach) IF token capture is solved -
   bigger effort, parked.

## 5. Migration notes (mlb-hr-tracker -> Vercel, when ready)
- The single parameterized build script (BACKLOG #7: read staging -> emit index.html) runs identically
  on Vercel as a buildCommand. No rework. This is why doing GitHub Actions first wastes nothing.
- Two migration shapes:
  (a) Static parity: point Vercel at the repo, buildCommand runs the Python build, outputDirectory =
      build output. Same behavior as Pages, no new features. LOW effort.
  (b) Dynamic upgrade: add /api/add-bet + storage. HIGHER effort, unlocks automation + fancier app.
- Repo visibility: old fanduel-bet-tracker is PRIVATE; mlb-hr-tracker is PUBLIC. Vercel works with both.
  (Note: GitHub Actions free-unlimited needs PUBLIC; Vercel hobby tier does not care.)
- Python on Vercel: build env can run Python for the build; serverless functions support a Python
  runtime. Confirm current runtime versions at build time.

## 6. Open questions / decisions before building
- LOE vs benefit (BACKLOG #11): if a move is more than "pretty simple," table to short-future.
  Static parity (5a) is simple; dynamic (5b) is not.
- Public vs private repo for the new Vercel project.
- Free hobby tier limits (build minutes, function invocations, bandwidth) vs usage - confirm at build
  time; usage here is tiny.
- Secrets: Claude API key + any GitHub token live as Vercel environment variables (never in the repo).
- Keep or drop the FanDuel auto-sync ambition (token capture was the hard, unsolved part).

## 7. Lessons carried from the March attempt
- Separate DESIGN from BUILD - no code until design is approved.
- Never overwrite files - version (v2, v3...).
- Save a TEST-RESULTS file alongside every deliverable.
- Action Network and Juice Reel were already EVALUATED and REJECTED in March:
  Action Network does NOT support FanDuel; Juice Reel lacked in-game per-leg progress and had poor UI.
  (This answers the re-raised questions in Research-notes-Action-Network_Juice-Reel.txt - no need to
  re-try them for the core game-view need.)
- Unique value no off-the-shelf app provides: click a game -> see EVERY bet on it with per-leg status
  at once. That is the reason to build.

## 8. Related files / pointers
- This project: C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker\ (BACKLOG.md #7-#11).
- Old Vercel project: C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\FanDuel\ (vercel.json, dashboard/, scripts/).
- Old repo: github.com/damienreilley/fanduel-bet-tracker (private). Old URL: fanduel-bet-tracker.vercel.app.

## 9. STOP
Reference doc only. Do not start a Vercel migration/build without Damien's explicit go-ahead
and a completed LOE assessment (BACKLOG #11).
