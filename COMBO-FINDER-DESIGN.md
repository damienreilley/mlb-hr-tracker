# COMBO FINDER - Build Spec

Status: DESIGN SPEC for a brain-chat build. Not yet built. Experimental / educational.
Last updated: 2026-06-22 (brain chat).

## How to use this file
This is a BUILD SPEC, not a run instruction. Building the tool is brain-chat work (the data pipeline, scoring, and gates have to be designed and debugged with Desktop Commander, the way parse_fanduel.py was built). It is NOT a helper run-instruction - there is no tool yet for a helper to execute. Once the tool is built and its rankings pass Damien's eye test, this collapses into a short helper-runnable step.

This tool is experimental and educational. It is NOT a market-edge tool. It explores parlay combinations WITHIN a player pool Damien has already chosen (players already on today's board) and attaches data-grounded reasoning. Output is suggestions only; it never places bets and never writes to the live board.

## 0. How to read this spec (REQUIREMENTS vs. METHOD)
This spec separates two things on purpose:
- HARD REQUIREMENTS (Section 4) are non-negotiable. Every one constrains the INTEGRITY OF THE OUTPUT (no meaningless legs, no fabricated or assumed data, no false precision, no misleading presentation). They are what keep the result from being lazy filler. They do NOT dictate your approach.
- ILLUSTRATIVE / OPEN (Section 5) covers data sources, specific stats, and scoring logic. These are STARTING POINTS, NOT A CEILING. If during the build you find a better source, a stronger driver stat, or a smarter way to score or group, USE IT - you are explicitly encouraged to. The requirements protect the output; they say nothing about your method, and you should improve the method freely. Do not treat my first-guess sources or formulas as the limit of what is allowed.

If a requirement and a better idea ever seem to conflict, the requirement is almost certainly about OUTPUT INTEGRITY (e.g. "cite a real number") and the better idea is about METHOD (e.g. "which number") - those do not actually conflict. If one genuinely does, surface it to Damien rather than silently dropping the requirement.

## 1. Goal
From the players already on today's board, produce a SMALL, RANKED set of suggested parlays Damien does NOT already hold, each carrying a stated reason rooted in real matchup data. Suggestions only - no writing to staging.json, no bet placement.

## 2. Inputs
- The board (staging.json): the two pools - every player with an HR leg, every player with an SB leg - each carried as a (player, prop, game) leg, not a bare name.
- Existing bet signatures: the exact player-sets already held, for exclusion (see R3).
- Per-game matchup context: the external signal that makes a suggestion more than re-sorted odds. WHAT context to pull is open (Section 5).

## 3. Candidate space (settled with Damien)
Both of these are IN:
- Cross-game combos - allowed, but flagged variance-only (see R7).
- Same-game same-player different-prop - allowed (e.g. one player to homer AND steal in one SGP).

This yields FOUR buckets, each scored and presented separately:
1. HR-stack (multiple HR bats, same game)
2. SB-stack (multiple SB threats, same game)
3. Single-player multi-prop (same player, same game, different props)
4. Cross-game / variance (independent legs across games)

## 4. HARD REQUIREMENTS (output integrity - non-negotiable)
- R1 - Leg identity. A leg is a (player, prop, game) triple. Never suggest a bare player; a suggestion must always say which prop in which game.
- R2 - Validity gate (runs BEFORE scoring). Reject any candidate that is not: at least 2 distinct (player, prop, game) legs, no duplicate leg, every leg resolvable to a real game today. Same player twice with the SAME prop is rejected; same player with DIFFERENT props is allowed (Section 3).
- R3 - Exclusion of what Damien holds. Exclude only EXACT player-set matches of bets already held. For partial overlaps, ANNOTATE, do not filter ("overlaps your existing bet #xxxx - player Y in both") and let Damien decide.
- R4 - Numeric-citation gate (the anti-laziness gate). Every suggested combo must cite AT LEAST ONE specific numeric driver tied to its game (an HR/9, a CS%, a park-factor number, etc.). A rationale with no number ("both good hitters in a good spot") is an automatic reject - regenerate or drop it.
- R5 - Insufficient-data path. If the driver data a candidate would need is missing, SET IT ASIDE and report it as "insufficient data" - never score or rank it on partial or assumed numbers. Backfilling with assumptions is the laziness in disguise; do not.
- R6 - Ordinal-within-bucket scoring only. Rank candidates WITHIN each bucket. Never produce a single global leaderboard across buckets (they use different drivers and are not comparable), and never present a score as a win probability.
- R7 - Output is FOUR separate ranked lists. One per bucket, each capped at N. The cross-game list is explicitly marked variance-only; its rationale may cite each leg's individual matchup but is FORBIDDEN from implying the legs reinforce each other.
- R8 - Suggestions only. No placing bets, no writing to staging.json or the live board, no calling the add-bet path.
- R9 - Trust rules inherited (same standards as the rest of this project). Verify data with real tool calls; never fabricate a stat or a player; cite the source of a number; say "I do not know" plainly when data is absent. A made-up driver number is worse than no suggestion.

## 5. ILLUSTRATIVE / OPEN (improve freely - this is NOT a closed list)
Everything here is a STARTING POINT. Treat it as "here is a reasonable first cut" and beat it where you can. Nothing in this section is a restriction.

- Data sources (suggested, not required). The MLB statsapi already used to grade the board has probable pitchers and game logs; park factors are a static lookup. That is a floor, not a ceiling - if you find cleaner endpoints or richer signals, use them. Drivers worth considering (and you may find better) include: opposing starter HR/9 and recent form; catcher caught-stealing % and pop time; pitcher time-to-plate and pickoff tendency; park factor and wind/weather; platoon/handedness matchup; Statcast signals (barrel rate, xSLG for HR; sprint speed for SB); bullpen quality for late-game SB; lineup slot and expected plate appearances; umpire tendencies. Pull what actually moves the read; ignore what does not.
- Scoring logic per bucket (suggested). HR-stack by opposing HR/9 + park; SB-stack by catcher CS-vulnerability + pitcher time-to-plate + game state; single-player multi-prop framed honestly (correlated on OPPORTUNITY - he reaches base / he is active - but power and speed rarely co-fire in one game, so combined probability stays low even when each leg is fair); cross-game by per-leg quality only. Refine any of these if you find better drivers - keep the scoring transparent and ordinal (R6).
- List length N and leg-count ceiling. Run-time parameters, set by Damien when the tool is run (he has intentionally left them open). Sensible default to propose: 2-to-3-leg combos, top 5-8 per bucket. Do not hard-code; make them inputs.

## 6. Output format
Four labeled sections (one per bucket), each a ranked list capped at N. Each line shows: the legs as "player - prop - game"; the one-line rationale WITH its numeric driver(s); for cross-game, the variance tag; for partial-overlap combos, the annotation from R3. Append an "insufficient data - not ranked" list of set-aside candidates with the reason each was set aside (R5), so nothing silently disappears.

## 7. Build sequencing
- This is a BRAIN-CHAT build, not a helper run - there is no tool yet; the data pipeline, scoring, and gates have to be built and debugged, which is design work.
- Build and PROVE ONE BUCKET first against Damien's eye test (SB-stack or HR-stack is the cleanest start), then widen to the other three.
- Once it is built and the rankings pass the eye test, it collapses into a short helper-runnable step ("run the combo finder against today's board, present the four lists"), exactly like the parser became the daily run.
- If this becomes code, keep it OUTPUT-ONLY: it must never import or call anything that writes staging.json or touches the live board.

## 8. Open items to set at build/run time
- N per bucket and the leg-count ceiling (2-only vs. 2-and-3) - run-time params, Damien's call when the tool is built.
- Which single bucket to prove first.

## 9. Provenance
Scoped in a brain chat on 2026-06-22 from a research discussion with Damien. Candidate space (cross-game IN, same-player multi-prop IN) settled by Damien. NOT prototyped - this is a design spec, not tested code. A build chat should verify every assumption against disk and live data before relying on it, and is encouraged to improve on the suggested method (Section 5) freely.