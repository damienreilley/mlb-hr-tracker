# Alt-Strikeout Detection - Design (v1)

Status: DESIGN for sign-off. No code written yet. (2026-06-08)

## Goal
Auto-grade pitcher alt-strikeout legs (e.g. "Gavin Williams 9+ K") live, instead of
flagging them manual. Show a running "X+ K - now N" and lock to hit at the threshold.

## Data source decision: play-by-play (reuse the existing loop)
The engine already walks liveData.plays.allPlays and already identifies the pitcher on
every play (pl.matchup.pitcher.fullName -> pitByKey), using it for the no-hitter (NH3/5/7)
and 1st-inning-K (K1) logic. Total strikeouts is a one-line piggyback on that same loop.
- No box-score path, no new data source, no separate name-matching.
- Name matching is accent-safe: norm() does NFD normalize + strips diacritics + lowercases,
  so "Cristopher Sanchez" / "Sanchez" match cleanly.

## Open items - decided (delegated to Claude 2026-06-08)
1. Event strings: count BOTH `strikeout` and `strikeout_double_play`. Inclusive = correct
   for a strikeout total. Safe to code regardless; confirm on first live game.
   (Note: existing K1 logic counts only `strikeout` - optional future tidy-up, low priority.)
2. Miss timing: v1 = miss only at game-Final. Never a false miss; the running count is always
   correct because the counter stops once the starter is pulled (no more plays with him as the
   pitcher of record). Only cost: a doomed leg reads "pending" until the game ends.
   v2 (miss the instant the starter is pulled) -> backlog; needs current-pitcher tracking.

## Leg data model
{ "p": "<pitcher name>", "prop": "ALTK", "k": <threshold int> }
e.g. { "p":"Gavin Williams", "prop":"ALTK", "k":9 }

## Exact change points (gen_bets.py embedded JS)
1. resetStats() pitchers.forEach: add  p.kTot=0;
2. allPlays pitcher branch: add  if(ev==='strikeout'||ev==='strikeout_double_play')ptp.kTot++;
3. PITCHSET: add  ALTK:1
4. legMet: add  if(pr==='ALTK'){if(p.kTot>=leg.k)return 'hit';if(gs.state==='Final')return 'miss';return 'pending';}
5. Pitcher render: dynamic label "<k>+ K" + progress "now <kTot>" (threshold comes from leg.k, not a static label map)

## Verification plan
- Build defensively (count both K event types).
- On the first live game tonight: confirm a pitcher's "now N" climbs and a leg locks to hit at
  the threshold; confirm existing specials/bets are unaffected. Fix live if an event string differs.
- (DC has no outbound network, so any direct feed inspection is via the browser, not DC.)

## Sequence
1. Sign off on this design.
2. Build alt-K engine as its own commit; verify current page still renders + existing bets intact.
3. Roll to June 8 with the alt-K parlays; confirm live grading as games run.
