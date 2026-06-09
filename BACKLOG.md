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
