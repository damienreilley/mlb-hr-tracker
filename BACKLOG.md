# MLB Bet Tracker - Backlog

Items to explore / build. Not yet implemented. (Started 2026-06-05.)

## 1. Alt-strikeout detection (auto-grade pitcher K-total legs)
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
