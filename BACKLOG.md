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

- STATUS 2026-06-18 (APPROVED DESIGN + BUILD IN PROGRESS): chosen path is (d) NEW - a Vercel-hosted add_bet MCP remote connector (sidesteps the auth wall that killed path a). Flow: phone screenshot -> Claude vision transcribes -> add_bet tool runs the REPO parse_fanduel.py -> clean parse appends to staging.json (GitHub Contents API) -> Action builds -> live -> receipt. Full design: PHONE-ADD-BET-DESIGN.md. Code: add-bet-server/ (core LOCALLY TESTED 4/4; MCP/Vercel wrapper deploy-ready draft). Deploy steps: add-bet-server/DEPLOY-RUNBOOK.md.
- DECISION UPDATE 2026-06-18: NO confirm-before-publish gate (SUPERSEDES the Safety line above). Damien chose straight-to-published; the parser's own FLAGS are the auto-gate (clean -> publish, any flag -> halt + report) plus a post-publish receipt. Residual risk (a plausible misread) accepted at $0.09 stakes.
- Parser hardened for the screenshot path 2026-06-18 (commit 53125d2): case-insensitive props, strip matchup time/ellipsis/truncation, unique-prefix team match. 6/17 regression byte-identical.

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

### Void-leg protocol (locked 2026-06-14; AUTO-DETECTION added 2026-06-18)
- FanDuel owns all odds/payout computation. We do NOT recompute odds on our side.
- AUTO-DETECT (2026-06-18, Option A): parse_fanduel.py detects FanDuel's "Void" token (shown where a voided leg's odds go, in EITHER position: player/Void/prop OR player/prop/Void) and sets that leg's "void":true automatically. The real player + prop are still captured. No manual step for legs FanDuel has already voided in the open-bets paste. (prev_name/prev_team skip the "Void" token; void_around() flags the leg.)
  - Engine drops void legs from the win condition: betStatus does if(s==='void')continue (void legs excluded from total/hit/miss; surviving legs decide win/loss). build.py mk_leg passes void:true through.
  - Bet-level PAYOUT = FanDuel's TOTAL PAYOUT from the paste (already recalculated post-void) -> correct.
  - Bet-level ODDS may stay FanDuel's displayed ORIGINAL number on a partially-voided bet (FanDuel does not relabel it and we do no odds math). Cosmetic only -- payout and grading are correct. Example: #zyhbkm voided 3 of 4 legs down to a single +520 leg; stored odds stays 34170, payout $0.62 is correct.
- Fully-voided bets (zero surviving legs) are NOT special-cased: betStatus would show 'alive' (act=0). Not seen as of 2026-06-18; revisit if it occurs (would need a 'void'/'push' bet status).
- Why not compute per-leg math: SGP/SGP+ legs are correlated and FanDuel prices them proprietarily, so the adjusted price cannot be reconstructed from per-leg odds. Re-reading FanDuel is the only reliable source (straight parlays and SGPs alike).

### Per-leg odds (decided 2026-06-14)
- NOT stored for now; we keep only bet-level odds/payout as FanDuel gives them.
- Capturing per-leg odds for analysis is a wanted future feature -> see FEATURE LOG #16.


## FEATURE LOG (enhancement requests; continues the backlog numbering)

## 12. Sort bets by number of legs alive  [DONE 2026-06-18 - shipped in Bets-tab sort row: Payout/Time/Legs/Alive/Hit]
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

## 15. Sort bets by FanDuel bet timestamp  [DONE 2026-06-18 - shipped in Bets-tab sort row: Payout/Time/Legs/Alive/Hit]
- Goal: on the Bets tab, add a sort option ordering bets by when they were PLACED on FanDuel (newest-first / oldest-first).
- Already available: each bet stores "placed" (e.g. "6/14 9:21AM") and a derived "ts"; sort keys off ts.
- Pairs with #12 - likely the same sort/order control with multiple modes.
- Priority: requested by Damien 2026-06-16.

## 16. Capture per-leg odds for analysis/tracking
- Now: per-leg American odds (e.g. +320 / +260) are visible in the FanDuel screenshot but NOT stored; only bet-level odds/payout are kept (see LOCKED DECISIONS: per-leg odds not stored).
- Goal: capture each leg's odds into the leg record for future analysis and tracking.
- Note: not needed for void math (FanDuel recomputes; SGP correlation makes per-leg reconstruction unreliable); purely for analysis.
- Priority: nice-to-have; wanted by Damien 2026-06-14.

## 17. Sort bets by number of legs that hit  [DONE 2026-06-18 - shipped in Bets-tab sort row: Payout/Time/Legs/Alive/Hit]
- Goal: on the Bets tab, add a sort option ranking bets by how many legs have already HIT (graded win), highest-first - a "how many cashed / how close did it come" view.
- Distinct from #12 (legs ALIVE = hit + pending): this counts ONLY legs already graded 'hit'.
- Already available: betStatus(b) returns {hit, total}; sort key off hit (tiebreak by hit/total, then alive).
- Pairs with #12 and #15 - same sort/order control, just another mode (Time placed / Legs alive / Legs hit / Odds / Payout). Recommend building ONE sort dropdown rather than three separate toggles.
- Priority: requested by Damien 2026-06-17.

## 18. Wire up TR (total runs Over/Under) in build.py - grader already exists
- Source: Damien test bet 2026-06-17 (us-pa ...g5d2rm leg "Over 9.5 Alternate Total Runs").
- Now: engine legMet HAS a TR grader (tot = as + hs vs leg.line, default 8.5), BUT build.py mk_leg has no TR case, so a TR leg falls to the general "return dict(p,prop)" which DROPS g and line - TR can never grade (no game, line defaults).
- Fix: add to mk_leg -> if l["prop"]=="TR": return dict(prop="TR", g=l["g"], line=l.get("line"), side=l.get("side","over")). Parser emits {prop:"TR", g, line}. Then Over/Under total-runs legs grade end-to-end.
- Priority: small, safe, additive build.py change. Test data on hand.

## 19. Grader: First 5 Innings Result (F5) - PARKED
- Source: Damien test bet 2026-06-17 (O/1924696/0004179 leg "Baltimore Orioles First 5 Innings Result").
- DECISION 2026-06-17: PARKED. Damien rarely bets this. Do NOT build a grader unless it becomes frequent. The parser tags it prop="NA" (recorded on the board, manual / not auto-graded); the bet's other legs grade normally and the NA leg shows un-graded.
- If ever built: needs first-5-innings line score from the box feed (confirm the feed exposes inning-by-inning runs first); new game-prop code F5 + a build.py mk_leg case carrying side.

## 20. Grader: Race To N Runs - PARKED
- Source: Damien test bet 2026-06-17 (us-pa ...g5d2rm leg "Pittsburgh Pirates Race To 5 Runs").
- DECISION 2026-06-17: PARKED (same handling as #19). Rarely bet. Parser tags prop="NA" (recorded, manual). Do NOT build unless frequent.
- If ever built: needs running score by team / play-by-play to know who reached N first; new game-prop code + build.py case (team + N).


## 21. Link to archived day pages from the live tracker
- Source: Damien 2026-06-19. The rollover auto-archives each prior day as archive/<date>.html, but those pages have no navigation - they just accumulate (9 exist as of 6/19: 06-03,04,05,08,09,11,13,16,17, with gaps on un-played/un-archived days). No way to reach a past day from the live board.
- Goal: from the live tracker, open any past day's board.
- RECOMMENDED approach (build chat confirms):
  (1) One-time: add a small "Past days" link in tracker_template.html (header or footer) pointing to archive/index.html - a static link, no per-day edit.
  (2) New tiny generator (e.g. build_archive_index.py): scan archive/*.html, sort newest-first, write archive/index.html as a dated link list styled like the tracker, with a "back to live board" link at top.
  (3) Wire into DAILY-ROLLOVER-RUNBOOK.md: after archiving the prior day's page, regenerate archive/index.html and commit it alongside the archived page.
- Alternatives considered + rejected: a date dropdown in the main header (gets unwieldy / clutters header as days pile up); a footer date list on the main page (grows without bound). An index page keeps the live board clean and scales.
- Keep index generation OUT of build.py's CI trigger path - the archive set only changes at rollover, which runs locally; no need to rescan on every bet build.
- Aside: archive/ also holds legacy gen_bets_*.py (06-03..06-09), pre-consolidation build scripts - unrelated clutter, can be ignored or cleaned separately.
- Priority: requested by Damien 2026-06-19.



## 22. BUG: daily_run.py rollover overwrites staging WITHOUT archiving (data-loss path) - DONE (shipped 2026-07-18)
- SHIPPED: all 3 solution parts below. Tested: rollover w/o --auto-rollover REFUSES + staging untouched;
  --dry-run prints per-file WOULD lines; same-day mode unaffected. Backup: daily_run.PRE-ARCHFIX-2026-07-18.bak.py.
- RUNBOOK NOTE: the standard rollover command is now `python daily_run.py <paste.txt> --auto-rollover`.
- Surfaced: 2026-07-18 rollover (7/16 -> 7/18). daily_run printed "WOULD archive prior day 2026-07-16"
  then OVERWROTE staging.json anyway. archive/2026-07-16.{html,json} were never written - the exact
  missed-archive scenario the DAILY-ROLLOVER-RUNBOOK warns loses a day. 7/16 was recovered by hand
  (index.html was still the 7/16 board; staging came from git HEAD) before commit, so nothing was lost.
- ROOT CAUSE: asymmetric flag gate. The archive copy runs only when --auto-rollover is passed
  (`if a.dry_run or not a.auto_rollover: print("WOULD archive...")`), but the staging WRITE is gated
  only by --dry-run. Without --auto-rollover the script skips the archive, then falls through and
  writes today's staging over the un-archived prior day. The docstring says rollover "needs
  --auto-rollover to write" - the code never enforced it.
- SOLUTION (3 parts):
  (1) REFUSE: in rollover mode, if neither --dry-run nor --auto-rollover -> print refusal, exit 1,
      touch nothing. Matches documented intent.
  (2) Per-file archive guard: check archive/<PRIOR>.html and .json INDIVIDUALLY and copy whichever is
      missing (old guard was an OR - one existing file suppressed archiving the other).
  (3) Belt-and-suspenders: hard assert BOTH archive files exist immediately before the rollover
      staging write. Overwriting an un-archived day becomes impossible.

## 23. BUG: parser silently DROPS straight single bets (no flag, GATE blind) - DONE (shipped 2026-07-18)
- SHIPPED: all 3 solution parts below + server copy synced. Corpus regression vs old parser: ZERO bets
  lost/changed, ZERO new flags - pure additive. Backup: parse_fanduel.PRE-SINGLES-2026-07-18.bak.py.
- HISTORICAL AUDIT (from the corpus diff - the new parser recovers singles old one dropped):
  - 7/16: 11 SB singles recovered from paste - ALL already on the archived board (arrived another route). No loss.
  - 7/01: #4222 Machado HR - already on board. No loss.
  - 6/19: THREE singles MISSING from archive/2026-06-19.json: #gfggy8 Freeman HR $0.09,
    #h42sep Riley HR $0.10 (settled $0.00), #n485gg Cruz HR $0.40 (settled $0.00). FanDuel settled
    them; only the tracker's 6/19 archive is incomplete ($0.59 wagered untracked). OPEN DECISION:
    retro-inject into the archived page (it self-grades from that date's final feeds) or leave as-is.
- Surfaced: 2026-07-18. Kyle Schwarber +200 "TO HIT A HOME RUN" straight single (#v2vtjw) vanished
  from intake - 20 bets in paste, 19 parsed, zero flags. First straight single ever bet; all prior
  bets were parlays/SGP/SGP+/pitcher specials.
- ROOT CAUSE: split_blocks keeps a block only from its first is_header() line; is_header matches only
  "^\d+ leg ", "Same Game Parlay", or pitcher_prop(). A straight single (player / +odds / prop) has no
  such line -> `hi is None` -> block silently discarded BEFORE parse_bet. The GATE reads parser flags,
  and a never-segmented block raises none - structurally invisible failure.
- Proof parse is fine: parse_bet() called directly on the Schwarber block -> clean bet, zero flags,
  prop HR, game NYM@PHI, pitchers resolved. Only segmentation is broken.
- SOLUTION (3 parts):
  (1) split_blocks fallback: when no is_header line exists in a block, anchor a single at index i
      where lines[i+1] matches ^\+\d+$ AND prop_code(lines[i+2]) is not None (player/odds/prop shape);
      emit block[i:]. Parlays/SGPs/pitcher specials keep the existing header path (unchanged).
  (2) parse_bet kind: a block with no SGP token and exactly 1 leg -> kind="Single", expected=1
      (enables the leg-count check; was labeled "1-leg SGP" with expected=None).
  (3) Relabel live #v2vtjw kind "1-leg SGP" -> "Single" in staging for consistency.
- Phone path: Vercel bundles the ROOT parser at build (Install Command `cp ../parse_fanduel.py`), so
  root patch + redeploy fixes add_bet too. Also sync the stale local add-bet-server/parse_fanduel.py copy.


## 24. Correct Score bets: parsed as NA/manual (DONE 2026-07-23) + AUTO-GRADER (open)
- Surfaced 2026-07-23 intake: 4 "Correct Score" singles on TOR (8-3, 8-0, 8-5, 7-2) were SILENTLY
  DROPPED - 18 BET IDs in paste, only 14 parsed, zero flags. Same failure class as #23.
- ROOT CAUSE: block shape is `<Team> H-A` / `+odds` / `CORRECT SCORE` / matchup. No is_header match,
  and the #23 singles anchor required prop_code(b[i+2]) - "CORRECT SCORE" is not in PROP_MAP -> no
  anchor -> block discarded before parse_bet.
- SHIPPED (2026-07-23):
  (1) tokenize: "correct score" line emits an NA/manual leg with txt "Correct score <TEAM> H-A
      (manual/FD)" - same convention as First 5 Innings (#19) / Race To N (#20). Selection is found by
      scanning up to 3 lines back for `^(.+?)\s+(\d+)-(\d+)$`. If NO team+score line is found it emits
      NOTHING (guards against legacy non-MLB "Correct Score" legs, e.g. the 6/19 soccer SGP #4191,
      which must stay byte-identical).
  (2) single_start accepts a SINGLE_MARKETS label ("correct score") in place of a prop code, so the
      block segments.
  (3) DROP DETECTOR - split_blocks_checked() returns (blocks, dropped); any block carrying a BET ID
      that matches no anchor raises flag "UNPARSED BLOCK (unknown bet type...)" -> GATE HOLD. This is
      the STRUCTURAL fix for the whole #23/#24 bug class: an unknown bet type can no longer vanish
      silently, it now halts intake loudly. Wired into parse_fanduel.main().
  (4) ZERO LEGS flag - any bet parsing to 0 legs now flags (can never grade; always a parser miss).
  - Regression: full corpus re-parsed vs backup - ONLY _paste_0723 changed (+4 recovered bets);
    every other paste byte-identical incl. #4191. Corpus + gate suites pass.
    Backup: parse_fanduel.PRE-CORRECTSCORE-2026-07-23.bak.py
- OPEN - AUTO-GRADER for Correct Score (currently NA/manual, tracked on FanDuel):
  - Gradable in principle: final linescore gives both teams' runs; leg needs {team, teamRuns, oppRuns}.
  - Orientation rule to encode: FanDuel lists the NAMED team's runs FIRST ("Toronto Blue Jays 8-3" =
    TOR 8, opponent 3) - NOT home-away order. Must be tested against a settled example before trusting.
  - Work: new prop code CS + build.py mk_leg case carrying g/team/runs + engine legMet case; grade only
    at Final (a 5-3 game in the 7th is pending, not a miss).
  - Sibling of #2 (moneyline) / #3 + #18 (total runs) - all game-level graders off the same linescore.
  - Priority: only worth building if Damien bets these regularly; NA handling is correct meanwhile.
- PHONE PATH: root parser is bundled to Vercel at build, so add_bet gets all of the above on deploy.
