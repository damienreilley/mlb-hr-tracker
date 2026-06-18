# PHONE-ADD-BET-DESIGN.md
Add a FanDuel bet to the live tracker from your phone via screenshot(s).

Status: APPROVED DESIGN, build in progress. Created 2026-06-18 by the brain chat under Damien's
full delegated authority ("take this as far as you can ... approve anything") while he was at the
Phillies game. Supersedes the phone-pipeline portion of VERCEL-FUTURE-DESIGN.md.

## 0. GOAL (one sentence)
Damien sends one or more screenshots of a placed FanDuel bet to Claude on his phone; the bet flows
all the way to PUBLISHED on the live tracker (https://damienreilley.github.io/mlb-hr-tracker/) with
no manual approval step, while the deterministic parser stays in the loop so nothing is fabricated.

## 1. LOCKED DECISIONS (from Damien, 2026-06-18)
- INPUT = screenshot(s). Multiple screenshots per bet supported (tall / multi-SGP bets scroll).
- NO approval gate. A clean bet publishes straight through. (See safety model, section 3.)
- Deterministic parser stays in the loop. Vision only TRANSCRIBES the image to text; the repo's
  parse_fanduel.py does ALL structuring/grading. No model-authored bet JSON.
- BET ID is required (parser drops any block without "BET ID:"). The phone screenshot must include
  the "BET ID: us-pa:..." line. CONFIRMED present in Damien's placed-bet view (IMG_8524, IMG_8528).
- Compute layer = Vercel (thin: run the parser + write to GitHub). Tracker stays on GitHub Pages.
- Auth = NO-AUTH MVP (delegated decision A). OAuth 2.1 is the documented fast-follow (section 9).

## 2. ARCHITECTURE / DATA FLOW
  phone (Claude mobile app)
   -> Damien sends screenshot(s) of the placed bet
   -> Claude VISION transcribes the shot(s) into FanDuel "open-bets" TEXT (the format
      parse_fanduel.py consumes), applying the normalization rules in section 5
   -> Claude calls the add_bet MCP tool (Vercel-hosted remote MCP connector) with that text
   -> Vercel function:
        1. runs the REPO's parse_fanduel.py on the text (single source of truth)
        2. if the parser raises ANY flag (leg-count mismatch, unknown prop, g=??, missing
           odds/wager/payout) -> RETURN the flags, DO NOT publish
        3. if clean -> load live staging.json (GitHub Contents API), append the bet, dedup by #id
           (skip if already present), keep the staging date, commit staging.json
   -> existing GitHub Action (build.yml) rebuilds index.html -> GitHub Pages -> LIVE
   -> add_bet returns a one-line receipt (id, kind, legs, odds, payout, live URL) to the chat

Nothing downstream of the parser changes: parser, Action, Pages, void/HR2/doubleheader logic are
all REUSED. Vercel is only "run the parser + write to GitHub."

## 3. NO-CONFIRM SAFETY MODEL (how a bad bet can't silently go live)
Because there is no human approval gate, the parser's own FLAGS are the automatic gate:
- CLEAN parse  -> publish (append + build + live) + post a receipt to the chat.
- ANY flag     -> HALT, do not publish, return the flag text so Damien can fix / re-shoot.
Flags that catch transcription damage: LEG COUNT MISMATCH (header "N leg" or summary count != parsed
legs), unknown prop, g=?? (unresolved game), missing odds/wager/payout.
Post-publish receipt = a non-blocking record (NOT an approval) so Damien can eyeball after the fact.
RESIDUAL RISK (accepted): a PLAUSIBLE misread - right-shaped but wrong value (e.g. $37.33 read as
$87.33, or "To Record A Hit" read as "To Record 2+ Hits") - would not trip a flag and would publish.
At $0.09 stakes this is an accepted trade for zero friction; the receipt is the catch.

## 4. DEDUP / IDEMPOTENCY
#id = "#" + last 6 chars of the FanDuel BET ID (lowercase). Re-sending the same screenshot yields the
same #id, so the append step skips it (no double-post). Existing convention; phone path reuses it.

## 5. TRANSCRIPTION SPEC (screenshot -> parser-format text)  [the contract]
Claude transcribes each bet into this exact line structure (one bet = one block):
  Same Game Parlay            (or "N leg Same Game Parlay+", or "N leg parlay", or a pitcher header)
  +<odds>                     (bet-level odds, e.g. +41376)
  <summary line>              (optional; "Player Prop, Player Prop, ..." - used as a leg-count check)
  <Away Team (A Pitcher)> @ <Home Team (H Pitcher)>      (matchup line, one per game)
  <player>                    (then the prop on the next line)
  <prop>                      (FanDuel prop text, e.g. "To Record A Hit")
  ... (repeat player/prop per leg; repeat matchup+legs per game for a multi-game SGP+)
  $<wager>
  TOTAL WAGER
  $<payout>
  TOTAL PAYOUT
  BET ID: us-pa:<...>
  PLACED: M/D/YYYY h:mmPM ET

NORMALIZATION RULES (verified necessary against real screenshots; the parser is now hardened to
tolerate these too, but the transcription should still produce clean text):
  R1 PROPS: on-screen props are ALL-CAPS ("TO RECORD A HIT"); transcribe in canonical FanDuel casing
     ("To Record A Hit"). [parser also matches case-insensitively now]
  R2 MATCHUP TIME: the game time (e.g. "6:41PM ET") renders on the matchup line; put it on its OWN
     line or omit it - do NOT leave it glued to the matchup. [parser also strips a trailing time now]
  R3 TRUNCATED TEAMS: the expanded multi-SGP view truncates team names ("Kansas City Ro...",
     "Philadelphia Phillies (..."); transcribe the FULL team name. [parser also resolves a unique
     team-name prefix now]
  R4 BET ID + TOTALS: always include the BET ID line and the TOTAL WAGER / TOTAL PAYOUT pair.
  R5 VOID legs: if a leg shows a "Void" token where its odds go, keep the "Void" line in place; the
     parser auto-detects it and sets void:true (do not drop the leg).

## 6. MULTI-SCREENSHOT STITCHING + DEDUP
A tall bet (e.g. a 16-leg SGP+ across 3 games) spans several overlapping screenshots. Claude:
  1. Reads ALL provided shots.
  2. Confirms they belong to the SAME bet (identical BET ID at the bottom of each).
  3. Concatenates the leg sections in order, DEDUPING the overlap: a leg is a duplicate iff the same
     (player, prop, game) tuple already appears. (Same player can legitimately appear twice with
     DIFFERENT props - dedup on the full tuple, not the name.)
  4. Produces ONE text block per section 5, then calls add_bet once.
VALIDATION NET: the bet header "N leg ..." gives the expected leg count. If stitching dropped or
double-counted a leg, the parser's LEG COUNT MISMATCH flag fires and the bet HALTS (section 3).
VERIFIED: the real 16-leg / 3-game / 3-screenshot bet (#2w1q5h) parses to exactly 16 legs split
STL@KC:5 / NYM@PHI:7 / CWS@NYY:4 with no flags.

## 7. PARSER HARDENING  [DONE 2026-06-18, commit 53125d2]
parse_fanduel.py hardened so an imperfect transcription still parses (defense in depth), with the
6/17 outputs byte-identical and the 6/18 void work intact (validated):
  - prop_code(): case-insensitive prop matching (PROP_MAP exact first, then lowercased).
  - _clean_side(): strips a trailing game-time, ellipsis, and truncated-open-paren from matchup sides.
  - team_code(): after exact match, resolves a UNIQUE team-name prefix (>=6 chars) for truncated names.
  - summary leg-count regex made case-insensitive.
Backup: parse_fanduel.PRE-HARDEN-2026-06-18.bak.py.

## 8. VERCEL add_bet MCP SERVER  [to build]
Runtime: PYTHON MCP server on Vercel (Hobby tier, free) so it imports/runs the repo's
parse_fanduel.py directly - one parser, no reimplementation. (Proven pattern: sdiehl/mcp-on-vercel.)
Transport: StreamableHTTP. Function timeout 10s (parse + GitHub write is well under). Cold start
~2-3s (fine for an occasional add).
Tool: add_bet(text: str) -> result
  - parse text with parse_fanduel.py
  - if flags: return {ok: false, flags: [...]}   (no write)
  - else: GitHub Contents API -> GET staging.json (current sha), append + dedup, PUT (commit)
  - return {ok: true, id, kind, legs, odds, payout, url}
Secrets (Vercel env vars, NEVER in repo): GITHUB_TOKEN (fine-grained PAT, repo contents:write on
mlb-hr-tracker only).
Files (deploy-ready drafts in add-bet-server/): the api handler, the add_bet core, requirements,
vercel.json. The append/dedup core is LOCALLY TESTED; the MCP/Vercel wrapper is assembled but only
fully testable once deployed.

## 9. AUTH
claude.ai remote connectors do NOT accept a static API key, bearer token, or token-in-URL (per
Anthropic connector docs). Only OAuth 2.1 (DCR/PKCE) or NO auth.
DECISION (delegated): NO-AUTH MVP. Rationale: the endpoint is write-only to a PUBLIC fun tracker,
exposes no data, and any junk bet someone posted would be visible and one-click removable; stakes are
minimal. The unguessable Vercel URL is the only obscurity.
FAST-FOLLOW: add OAuth 2.1 (DCR + PKCE; Vercel mcp-handler or a provider) before this is relied on
daily. Tracked as an open item.

## 10. SAME-DAY APPEND vs NEW-DAY ROLLOVER
add_bet appends to the CURRENT staging.json and keeps its date. It must compare the screenshot's
PLACED date to staging.json's date:
  - same date  -> append + dedup (normal case).
  - placed date NEWER than staging date -> DO NOT cross days silently; return a flag telling Damien a
    rollover is needed first (see DAILY-ROLLOVER-RUNBOOK.md). (A future enhancement could auto-run the
    rollover; for the MVP it halts and reports.)

## 11. STAGED BUILD PLAN
  S1 [DONE] Harden parse_fanduel.py + validate + commit (53125d2).
  S2 [DONE] This design doc.
  S3 [in progress] add-bet-server/ : add_bet core (parse + append + dedup) + LOCAL test; MCP/Vercel
     wrapper + vercel.json + requirements; deploy runbook. Committed for review (not deployed).
  S4 [needs Damien] Generate a fine-grained GitHub PAT (mlb-hr-tracker, Contents: read+write).
  S5 [needs Damien] Deploy add-bet-server/ to Vercel (his account); set GITHUB_TOKEN env var.
  S6 [needs Damien] Add the custom connector (the Vercel MCP URL) on claude.ai (syncs to mobile).
  S7 [together] End-to-end test from the phone with a real screenshot; confirm publish + receipt.
  S8 [fast-follow] OAuth 2.1 hardening.

## 12. WHAT NEEDS DAMIEN (deploy day - cannot be done for him)
  - Create the GitHub fine-grained PAT (it is a secret; Damien creates it, never shares it with me,
    never commits it). Scope: repo mlb-hr-tracker, Contents read+write only.
  - Log into Vercel, import add-bet-server/, set GITHUB_TOKEN as an env var, deploy.
  - On claude.ai: Settings > Connectors > Add custom connector > paste the Vercel MCP URL.
  Detailed steps in add-bet-server/DEPLOY-RUNBOOK.md.

## 13. OPEN ITEMS / FUTURE
  - OAuth 2.1 hardening (section 9).
  - Auto-rollover inside add_bet on a new-day bet (section 10).
  - Fully-void bet status (would show 'alive'; noted in BACKLOG void protocol) - not phone-specific.
  - The home-pitcher (hsp) is often truncated/blank in screenshots; harmless for non-DH games, but a
    doubleheader bet added via screenshot may lack hsp for per-leg game resolution (edge case).

## 14. VERIFIED EVIDENCE (this session)
  - 4-leg single-game SGP (#dks2bg, IMG_8524): clean transcription parses to 4 legs, NYM@PHI,
    odds 41376, wager 0.09, payout 37.33, no flags.
  - 16-leg 3-game SGP+ (#2w1q5h, IMG_8526/27/28): parses to 16 legs, STL@KC:5 / NYM@PHI:7 / CWS@NYY:4,
    no flags.
  - Hardened parser: 4-leg and 16-leg MESSY forms (all-caps props, time-on-matchup, truncated teams)
    now parse clean; 6/17 regression byte-identical; 6/18 voids intact.
