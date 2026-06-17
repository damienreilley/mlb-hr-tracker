# FanDuel Paste -> staging.json Parser - DESIGN SPEC
Status: DESIGN (brain-approved for build). Not built yet.
Purpose: kill the daily hand-transcription. Turn Damien's raw FanDuel "Open Bets"
paste into the staging.json bets[] array deterministically, so the daily build
becomes: paste -> run parser -> reconcile FLAGS only -> push. A mechanical task a
Sonnet helper can run fast.

## WHY
Today's bottleneck is a human typing ~32 bets / ~128 legs out of a noisy paste.
The deploy half (staging -> push -> Action -> Pages) is already one push / ~50s.
This spec removes the typing, not the human check.

## REQUIREMENTS (MUST)
- Input: a single text file containing the raw FanDuel paste (exactly as Damien copies it).
- Output 1: bets[] in the REAL schema:
  {full_id, id, kind, odds(int,no +), wager(float), payout(float), placed, status:"open", legs:[{p,prop,g}]}
- Output 2: a FLAG REPORT listing every bet/leg the parser could NOT resolve with certainty.
- Deterministic only. The parser NEVER guesses. Anything uncertain -> leg g:"??" + a flag.
- Preserve exact transcription: odds, wager, payout, player names copied verbatim from the paste.

## NICE-TO-HAVES (not required for v1)
- Auto-detect voids. Per-leg odds capture. Writing staging.json directly (v1 just emits a draft).

## INPUT PARSING RULES
- Split into bets on "BET ID:" boundaries (each bet block ends at its BET ID / PLACED lines).
- id convention: us-pa:* -> "#"+last6(full_id).lower(); legacy O/.../NNNN -> "#"+int(NNNN).
- placed: "6/17/2026 1:08PM ET" -> "6/17 1:08PM".
- kind: from the bet header -> "N-leg SGP+" (Includes 1 SGP + selections), "N-leg parlay"
  (cross-game, no SGP), "N-leg SGP" (single-game Same Game Parlay), "Pitcher Special" (pitcher single).
- odds: the BET-LEVEL odds (the first +NNNNN under the header), not inner SGP odds.

## PROP TEXT -> CODE (exact map; engine BATSET/PSET)
"To Hit A Home Run"->HR ; "To Record A Hit"->HIT ; "To Record 2+ Hits"->HIT2 ;
"To Record 3+ Hits"->HIT3 ; "To Record A Stolen Base"->SB ; "To Record 2+ Stolen Bases"->SB2 ;
"To Record An RBI"->RBI ; "To Record 2+ RBIs"->RBI2 ; "To Record A Run"->RUN ;
"To Record 2+ Runs"->RUN2 ; "No-Hitter Through 5 Innings (Min. 15 Outs)"->NH5 ;
"No-Hitter Through 7 Innings (Min. 21 Outs)"->NH7 ; "3+ Strikeouts in the 1st Inning"->K1.
Any prop text NOT in this map -> FLAG (do not invent a code).

## GAME ATTRIBUTION (the hard part - deterministic)
- A game block appears as two team lines: "<City Nickname> (<Pitcher>)" for AWAY then HOME,
  in either the "AWY @ HOM / time" form OR a live box-score block. AWAY is always listed first.
- Map full team display name -> code (build.py TEAM nicknames + city; "Athletics" has no city -> ATH).
- Per leg: if the leg is immediately followed by its OWN game block, use AWAYcode@HOMEcode.
  If the leg has NO own block, it INHERITS the current SGP game (stated once under the SGP header).
- If a leg's game cannot be resolved to two known team codes -> g:"??" + FLAG (never guess).

## INTEGRITY / EXPANSION CHECK (Damien's intake rule, automated)
- For each bet, compare the stated leg count (the "N leg" label and/or the comma leg-summary)
  to the number of legs actually parsed. Mismatch -> FLAG that bet as possibly unexpanded; do
  not emit it as complete.

## ACCEPTANCE TEST (first run must pass)
- Run against the June 17 paste and diff output vs the verified ground-truth file
  _staging_june17_draft.json (32 bets, 128 legs, $4.25). All unambiguous fields must match
  byte-for-byte; any leg the parser flags must be one of the known cross-game inferences
  (Mullins->TB@LAD, Bichette->NYM@CIN, Wood->KC@WSH, Witt->KC@WSH, Soto/Trout/Yoshida/Goodman).
- Parser is "trusted" only after it reproduces a verified day, with its flags landing exactly
  on the legs a human would also double-check.

## NON-GOALS
- No settling/grading (the live engine does that). No editing leg status. No pushing.
- Output is a DRAFT for human reconcile + sign-off; the existing push/archive flow is unchanged.
