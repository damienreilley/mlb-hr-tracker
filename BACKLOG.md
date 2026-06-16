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


## LOCKED DECISIONS / CONVENTIONS (read before building)

### Bet ID convention (locked 2026-06-14)
- id = "#" + the LAST 6 characters of the FanDuel BET ID, lowercase.
  Example: us-pa:01kv34p6b8fvm8md8sy7wbvhqq  ->  #wbvhqq
- Legacy O/####### bets keep their existing "#<sequence>" form (e.g. #4155); do not rewrite them.
- Why: the tail is a real substring of the FanDuel BET ID, so Damien can copy the id from the tracker and Ctrl+F it inside FanDuel to find the bet. It is deterministic, so re-reading the same bet yields the same id, which lets the dedup guard block double-posts.

### Void-leg protocol (locked 2026-06-14)
- FanDuel owns all odds/payout computation. We do NOT recompute odds on our side.
- When a leg voids: Damien supplies FanDuel's UPDATED bet (manual is fine for now). The build/helper then:
  1) sets the leg's void flag (engine drops it from the win condition; surviving legs decide win/loss), and
  2) overwrites the stored bet-level odds + payout with FanDuel's recalculated numbers.
- Why not compute per-leg math: SGP/SGP+ legs are correlated and FanDuel prices them proprietarily, so the adjusted price cannot be reconstructed from per-leg odds. Re-reading FanDuel is the only reliable source (straight parlays and SGPs alike).

### Per-leg odds (decided 2026-06-14)
- NOT stored for now; we keep only bet-level odds/payout as FanDuel gives them.
- Capturing per-leg odds for analysis is a wanted future feature -> see FEATURE LOG #16.


## FEATURE LOG (enhancement requests; continues the backlog numbering)

## 12. Sort bets by number of legs alive
- Goal: on the Bets tab, add a sort option that ranks bets by how many legs are still alive - surface the bets closest to cashing at the top.
- Definition: "alive" = a leg whose legMet() is neither 'miss' nor 'void' (hit + pending). One missed leg kills the bet, so dead bets sink.
- Open decisions for the build chat:
  - ranking basis: raw alive-leg count vs alive ratio (alive / total) vs "closest to cashing" (hit / total, pending-aware). A 2-of-2-alive small parlay vs a 6-of-8-alive big one rank differently under each.
  - new sort toggle alongside the current order, or replaces it.
- Already available: betStatus(b) returns {st, hit, total}; each bet carries _st (won/dead/alive) and _hit/_tot. Alive-count is a small derivation from existing per-leg legMet() results - no new data needed.
- Priority: nice-to-have. Source: helper chat 2026-06-16 (scoped from code, NOT prototyped; build chat confirms approach).

## 13. Make pitcher-special prop text easy to read (darker + slightly bigger)
- Now: the pitcher-special bet line (e.g. "No-hit thru 5 - 0 hits", "3+ K in 1st - now 0") renders in <span class="lprop">. Current CSS: .lprop{font-family:'Spline Sans Mono';font-size:11px;color:var(--dim);white-space:nowrap}. --dim is #74857b (muted gray-green), faint and small. On pitcher-special cards the leg row is just the marker + this text (pitcher name is in the card header), so .lprop is the main visible line.
- Goal: darker and a little bigger.
  - color -> var(--ink2) (#36443c) or var(--ink) (#172019)
  - size -> 12.5px to 13px (from 11px); optional font-weight:600
- Scope decision for the build chat: .lprop is shared by all legs (hitter legs too).
  - (a) bump .lprop globally - simplest; affects every leg.
  - (b) scope to pitcher specials only: in betCardHTML append a "lprop-ps" modifier class when the leg is a pitcher special, and style .lprop-ps{font-size:13px;color:var(--ink2);font-weight:600}. Recommend (b) unless all legs should match.
- Note: a .pspec/.psd/.pst class set exists in the CSS but is DEAD - not referenced by any render code. The live class is .lprop.
- Priority: nice-to-have; final size/weight/color needs one eyeball pass on the deployed card. Source: helper chat 2026-06-16.

## 14. Display stolen bases on the Hitters tab (parity with HR) - relates to #6
- Now: renderHitters shows a per-player badge by priority HR -> 4+ TB -> hit badge -> hit count -> odds. No SB branch; a steal never appears on the Hitters tab. HR treatment is three-fold: a HR badge on the row, a row marker, and a pill in the top "homered" track.
- Goal: when a player records a stolen base, surface it on the Hitters tab the way a HR is.
- Already available: statOf(name).sb is live from the box score (sb=bt.stolenBases||0) - same path HR uses, no new fetch.
- Open decisions for the build chat:
  - coexistence when a player both homers and steals (HR badge primary + small SB chip, not one-or-the-other).
  - parallel SB pill in the top track (like "homered" pills) or just a row badge.
  - badge style/threshold (SB >= 1; possibly a count if >1).
- Context: a concrete case of #6 (revise Hitters-tab badge), which already notes SB/RBI/runs/doubles/triples are not surfaced. Could be standalone (just SB) or folded into a #6 rethink.
- Priority: Damien asked specifically, likely higher than the rest of #6. Source: helper chat 2026-06-16 (scoped from code, NOT prototyped).

## 15. Sort bets by FanDuel bet timestamp
- Goal: on the Bets tab, add a sort option ordering bets by when they were PLACED on FanDuel (newest-first / oldest-first).
- Already available: each bet stores "placed" (e.g. "6/14 9:21AM") and a derived "ts"; sort keys off ts.
- Pairs with #12 - likely the same sort/order control with multiple modes.
- Priority: requested by Damien 2026-06-16.

## 16. Capture per-leg odds for analysis/tracking
- Now: per-leg American odds (e.g. +320 / +260) are visible in the FanDuel screenshot but NOT stored; only bet-level odds/payout are kept (see LOCKED DECISIONS: per-leg odds not stored).
- Goal: capture each leg's odds into the leg record for future analysis and tracking.
- Note: not needed for void math (FanDuel recomputes; SGP correlation makes per-leg reconstruction unreliable); purely for analysis.
- Priority: nice-to-have; wanted by Damien 2026-06-14.
