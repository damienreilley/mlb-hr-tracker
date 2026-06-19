# Daily Rollover Runbook - MLB HR Tracker

Purpose: roll the live board from the prior day to a new day. This is the ONE
irreversible, stateful step in the daily flow - archive the prior day, then start
a fresh empty board for today. It happens once per day, before any of today's bets
go on. Currently brain-owned (delicate, once/day); documented here so it is
repeatable by any chat that follows it exactly. Verified against the 2026-06-17 ->
2026-06-18 rollover.

Preconditions:
- Desktop Commander available (Windows desktop). This needs python + git, so it
  CANNOT run from the phone today (see PHONE-ADD-BET-DESIGN.md for the phone path).
- In the repo: C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker
- Tools: python C:\Users\damie\AppData\Local\Programs\Python\Python314\python.exe ;
  git "C:\Program Files\Git\cmd\git.exe" ; gh "C:\Program Files\GitHub CLI\gh.exe"

Definitions:
- PRIOR = the day currently on the board (staging.json "date"), e.g. 2026-06-17
- TODAY = the new day, from a tool (Get-Date), ET, e.g. 2026-06-18

## STEP 1 - Verify state + sync (never assume)
- Get TODAY from a tool: (Get-Date).ToString('yyyy-MM-dd'). Display ET.
- git fetch ; git pull --no-edit origin main   (pull any Action [skip ci] rebuild
  so you archive the LATEST prior-day index.html).
- Read staging.json "date" = PRIOR. Confirm PRIOR != TODAY. If they are EQUAL this
  is NOT a rollover - it is a same-day add; STOP, do not archive.

## STEP 2 - ARCHIVE GUARD
- Check archive/<PRIOR>.html.
  - EXISTS  -> prior day already archived; skip STEP 3, go to STEP 4.
  - MISSING -> proceed to STEP 3. NEVER overwrite staging.json with TODAY until the
    prior day is archived (a missed archive loses that day - it has happened before).

## STEP 3 - Archive the prior day (archive/ is NOT in the build trigger path -> no rebuild)
- Copy index.html -> archive/<PRIOR>.html
- Copy staging.json -> archive/<PRIOR>.json  (raw bet DATA as clean JSON; analysis + belt-and-suspenders; added 2026-06-19. Verify it is valid JSON with "date":"<PRIOR>".)
- Sanity-check the copy: it contains <PRIOR> and the engine marker (function _lpk),
  and its byte size is close to the live index.html.
- git add archive/<PRIOR>.html archive/<PRIOR>.json ; git commit -m "archive <PRIOR> board + data" ; git push
  (no Action triggers from this, so origin does not move on its own).

## STEP 4 - Flip to a fresh empty TODAY board
- Write staging.json = {"date":"<TODAY>","bets":[]}
- Build locally to verify: python build.py staging.json index.html
  -> expect bets=0 games=0 players=0 pitchers=0 date=<TODAY>; index.html contains
  <TODAY> and function _lpk.
- git add staging.json index.html ; git commit -m "roll over to <TODAY> (fresh empty board)"
- git fetch ; confirm behind==0 (else pull) ; git push
  (staging.json changed -> the Action rebuilds and Pages deploys the empty board).

## STEP 5 - Verify live
- gh run list --limit 3 -> "Build and Deploy Tracker" success + pages deploy success.
- Fetch https://damienreilley.github.io/mlb-hr-tracker/ ->
  HTTP 200 ; shows <TODAY> ; does NOT show <PRIOR> ; contains function _lpk ; 0 bets.

DONE. The board is a clean empty TODAY on the current engine. Today's bets go on
next via the normal intake (parser -> THE GATE -> same-day APPEND), which can be a
helper chat. The rollover itself adds no bets.

## NOTES
- Archiving never triggers a rebuild (archive/ is not in build.yml triggers).
- Always pull before a push that could be behind an Action [skip ci] commit.
- The empty board is intended and brief; today's first bet append fills it.
- An archived page self-grades when opened (its DATE is baked in; it fetches that
  date's now-final feeds), so snapshot timing does not change archived results.
- Same-day ADD is the opposite of a rollover: never archive, never re-date, never
  rebuild staging from only the new bets - READ staging.json, APPEND, dedup by id,
  keep the date, push. See the helper handoff (SAME-DAY ADD vs NEW-DAY ROLLOVER).
