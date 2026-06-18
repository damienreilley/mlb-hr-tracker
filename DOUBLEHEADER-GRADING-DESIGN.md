# Doubleheader / Same-Matchup Grading Fix - Design Spec

Status: Phase 1 in build. Date: 2026-06-18.

## Problem
Two games with the SAME matchup on one date collide on the grading key
"AWY@HOM". This happens for (a) a true doubleheader, or (b) a suspended game
resumed today + today's regular game. Every leg for that matchup grades
against ONE of the two games; the other game's legs grade against the wrong
box score and are wrongly marked dead.

Observed 2026-06-17, SF@ATL had two games:
  pk 824912  SP Houser/Holmes      2:00pm ET   (the 6/16 game, resumed today)
  pk 824913  SP Whisenhunt/Ritchie ~7:15pm ET  (today's regular game)
BOTH were gameNumber=1, doubleHeader="N" -- the resume case does NOT set the
DH flags. All game-2 (Whisenhunt) legs graded vs game-1's final box -> dead.

## Root cause (verified in code)
engine refresh(): keyToGame[key] = allGames.find(teams match) -> returns the
FIRST schedule game for the matchup. GS keyed by matchup; STATS keyed by
player NAME. No gamePk-level or doubleheader handling anywhere.

## Disambiguation signal
gameNumber/doubleHeader are unreliable (both games were gn=1/dh=N in the
resume case). The reliable distinguishers, BOTH present in the FanDuel paste's
matchup line "...(C Whisenhunt) @ ...(J Ritchie)":
  - STARTING PITCHER: always shown (pre-game AND live box-form); differs per game.
  - START TIME: shown pre-game only; scratch-proof; differs per game.
Match against the MLB feed: probablePitcher for not-started games; the ACTUAL
boxscore starter (boxscore.teams[side].pitchers[0]) for live/final games
(ground truth, reflects scratches). Last-name match: FanDuel "C Whisenhunt"
-> MLB "Carson Whisenhunt".

## Matching cascade (only when a matchup has >1 schedule game)
  1. Start time, if the leg carried one (scratch-proof).
  2. Starting pitcher, last-name, EITHER side matches (a one-side scratch
     still resolves; the other game matches neither side).
  3. First-found (today's behavior) as last resort.
Scratch handling falls out of the cascade: the pre-game scratch window is
exactly when a start time IS present (use #1); a live paste already shows the
post-scratch pitcher (use #2 vs the actual starter).

SAFETY PROPERTY: for a matchup with ONE schedule game the cascade returns that
game -- identical to today's find(). Non-doubleheader days are unaffected.

## Phase 1 (build now)  vs  Phase 2 (deferred, flagged)
Phase 1 -- bets on a matchup all belong to the SAME game (the common case,
incl the SF@ATL bug). Map that one key to the correct gamePk via the cascade.
NO change to STATS/GS structure. Low blast radius.
Phase 2 -- bets on BOTH games of one matchup the same day. Needs distinct keys
+ per-game stat attribution (STATS keyed by gamePk) so a game-1 homer cannot
bleed into a game-2 leg. NOT built speculatively. The pipeline MUST DETECT this
case (two distinct pitcher-sets for one matchup in staging) and FLAG it loudly
so it can never be silently mis-graded.

## Per-layer changes (Phase 1)
parse_fanduel.py: capture away/home starter last-name from the matchup paren
  (today discarded by strip_paren). Attach asp/hsp to each leg. PURELY ADDITIVE
  -- no existing field changes. New helper paren_last(); at_game returns
  (g,asp,hsp); box-form path captures both lines; leg-assembly carries cur_ap/hp.
build.py: carry asp/hsp per game into GAMES[key]. Detect two distinct
  pitcher-sets for one matchup -> Phase 2 flag.
tracker_template.html refresh(): add probablePitcher to the SCHED hydrate;
  replace the keyToGame find() with the cascade (time -> pitcher vs
  actual-starter/probable -> first-found).

## Validation
Parser: re-parse morning 32; strip asp/hsp; assert byte-equal to ground truth
  (_staging_june17_draft.json) => additive only. Spot-check asp/hsp populated.
build.py: rebuild; assert index.html identical except GAMES carries asp/hsp.
engine: against live 2026-06-17 SF@ATL, assert the Whisenhunt key resolves to
  pk 824913 (NOT 824912). node --check. Deploy, verify on live URL.
Re-ingest: existing SF@ATL legs were parsed pre-fix (no asp/hsp) -- re-parse
  the affected bets so they carry pitchers and re-grade correctly.

## Files
parse_fanduel.py, build.py, tracker_template.html.
Regression: _diff_parse.py, _staging_june17_draft.json (ground truth).
