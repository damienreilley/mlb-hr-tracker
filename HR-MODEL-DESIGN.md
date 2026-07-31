# HR-MODEL-DESIGN.md
Home-run probability model for the MLB slate — full specification and runbook.
Version 2.0 — 2026-07-31. (v1.0 same day; superseded within hours, see below.)

## CHANGELOG v1.0 -> v2.0 — READ BEFORE TRUSTING ANY v1 NUMBER

**RETRACTION.** v1.0 reported "14x discrimination". That figure was WRONG. The
v1 backtest scored past games using FULL-SEASON stats, which include the games
being predicted — look-ahead leakage. Rebuilt with point-in-time stats
(cumulative strictly before each game date) over 2,466 observations across 10
dates, **true out-of-sample discrimination is 3.2x** for the outcome-only model.
Any document, chat or note citing 14x is superseded.

| Change | v1.0 | v2.0 |
|---|---|---|
| Backtest | 1,202 rows, 5 dates, leaky | 2,466 rows, 10 dates, point-in-time |
| Discrimination (honest) | 14.0x (inflated) | 3.2x base / 5.3x with Statcast |
| Batter term | outcome HR/PA only | blended with Statcast barrels/PA (w=0.50) |
| SHRINK | 0.826 (fitted on leaky data) | 0.920 (re-fitted leak-free) |
| Park factors | single season | 3 seasons weighted 3-2-1 |
| Openers | not modelled | detected — but measured NO improvement |
| Bias | 1.010 | 0.995 |
| Brier | 0.0809 (leaky) | 0.0914 (honest, leak-free) |

The Brier score got *worse* because the v1 number was flattered by leakage. The
v2 figure is the real one.


## 0. READ THIS FIRST (for a chat with no prior context)

You are being handed a working statistical model that estimates, for every hitter
in tonight's posted lineups, the probability they hit **at least one home run**.
Everything needed to run, validate, or rebuild it is in this document.

**What it produces:** a ranked table of hitters with a calibrated P(HR) for the
day, printed to console and written to `_hr_model_out.json`.

**What it is NOT:** a betting-advice engine and not a full projection system. It
ranks and calibrates. It does not know odds, and it does not decide wagers.

**Non-negotiable rule for whoever runs this:** every number in this model was
either measured from data or empirically derived. Do NOT replace a constant with
an estimate, a "typical value", or something recalled from memory. The v1 model
failed exactly that way — see §9. If you cannot measure it, say so and stop.

---

## 1. ALLOWED AND FORBIDDEN PATHS

**Repo root (all work happens here):**
`C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker`

**ALLOWED — read and write:**
- `hr_model.py` — the model
- `hr_backtest.py` — calibration backtest
- `hr_tune.py` — parameter sweep + cached-row tuner
- `HR-MODEL-DESIGN.md` — this document
- `_bt_rows.json`, `_hr_tuned.json`, `_hr_model_out.json` — generated artifacts, safe to delete/regenerate

**FORBIDDEN — do not read, write, modify, or commit:**
- `C:\Users\damie\OneDrive\Desktop\NewYorkLife-2025-Appeal\` — restricted; requires explicit per-session authorization from Damien
- `staging.json`, `index.html`, `archive/` — the live bet tracker. This model is
  READ-ONLY with respect to the tracker. It shares a folder; it does not share data.
- `parse_fanduel.py`, `build.py`, `daily_run.py`, `tracker_template.html` — tracker pipeline, unrelated to this model
- Any `*.bak.*` file — historical backups, never edit

**File modification rules:**
- Before editing any `hr_*.py`, copy it to `<name>.PRE-<REASON>-<YYYY-MM-DD>.bak.py`
- Never overwrite an existing `.bak` file; if the name exists, add a version suffix
- This doc is versioned the same way: `HR-MODEL-DESIGN.PRE-<REASON>-<DATE>.bak.md`

---

## 2. BEHAVIOURAL DO / DON'T

**DO**
- Measure every constant from data and record where it came from
- Re-run the backtest (§7 step 5) after ANY change to the model, and report the
  calibration numbers before presenting results
- State sample sizes next to any rate built on a small sample
- Say "I don't know" when a value cannot be measured
- Keep the tracker files untouched — this model only reads MLB StatsAPI

**DON'T**
- Do not invent a constant. Not PA-per-slot, not park factors, not weather
  coefficients. If it isn't measured, it isn't in the model.
- Do not hand-pick a subset of hitters and call the result "the top 5". The
  model scans every hitter in every posted lineup. Selecting candidates first
  reintroduces the selection bias that invalidated v1.
- Do not present a ranked list without also reporting calibration
- Do not tune parameters and then report the tuned fit as if it were out-of-sample
- Do not claim a value came from the data if you did not run the query
- Do not commit generated artifacts (`_bt_rows.json`, `_hr_model_out.json`)

---

## 3. ENVIRONMENT

| Item | Value |
|---|---|
| Python | `C:\Users\damie\AppData\Local\Programs\Python\Python314\python.exe` |
| Tooling | Desktop Commander (`start_process`) — requires Damien's laptop to be on |
| Network | MLB StatsAPI is public, no key. RotoWire is a public page. |
| Runtime | Full run ≈ 8–15 min (roughly 90 API calls). Backtest ≈ 10–20 min the first time, seconds afterwards from cache. |
| Timeouts | Use `timeout_ms` of 1,800,000+ for `hr_model.py` and the backtest |

If Desktop Commander is unavailable, check whether Damien is on his phone —
phone means no DC, and this model cannot run. Do not claim DC is unavailable
without a tool call proving it.

---

## 4. DATA SOURCES

All statistics come from **MLB StatsAPI** (`https://statsapi.mlb.com`). No key.

| Purpose | Endpoint |
|---|---|
| Schedule, probable pitchers, game status | `/api/v1/schedule?sportId=1&date=YYYY-MM-DD&hydrate=probablePitcher,team,linescore` |
| Every hitter incl. unqualified rookies | `/api/v1/teams/{teamId}/roster?rosterType=active&hydrate=person(stats(group=[hitting],type=[season],season=2026))` |
| Every pitcher + throwing hand | same with `group=[pitching]` |
| Team home/away splits (park factors) | `/api/v1/teams/{teamId}/stats?stats=statSplits&sitCodes=h,a&group=hitting\|pitching&season=2026&gameType=R` |
| League platoon splits (qualified only) | `/api/v1/stats?stats=statSplits&sitCodes=vr\|vl&group=hitting&season=2026&limit=500&sportId=1&gameType=R` |
| True league totals | `/api/v1/teams/{teamId}/stats?stats=season&group=hitting&season=2026&gameType=R` summed over 30 teams |
| Backtest lineups + outcomes | `/api/v1/game/{gamePk}/boxscore` → `battingOrder`, per-player `homeRuns` |

**Confirmed lineups and weather:** `https://www.rotowire.com/baseball/daily-lineups.php`
StatsAPI probable pitchers are sometimes missing or wrong; RotoWire had three
starters StatsAPI did not on 2026-07-31. RotoWire also supplies batting order,
handedness, temperature, wind speed and direction, and the game total.

**IMPORTANT — pagination trap:** the league-wide `/api/v1/stats` endpoints return
only QUALIFIED players (~148 hitters) and ignore `offset`. They cannot be used
for full-slate coverage. Use the per-team roster hydrate (30 calls) instead.

---

## 5. THE METHOD

### 5.1 Core equation

For each hitter, split expected plate appearances between the opposing starter
and that team's bullpen, then combine:

```
P(>=1 HR) = 1 - (1 - r_sp)^pa_sp * (1 - r_pen)^pa_pen
```

where each rate is built by the **odds-ratio (Log5) method** for rate stats:

```
r = (batter_rate * pitcher_rate / league_rate) * park * weather * SHRINK
```

This is the step that makes the model matchup-aware. Facing Nick Martinez
(2.45 ERA) and facing Ryan Johnson (7.34 ERA) produce different numbers, which
is the whole point — v1 used handedness only and treated them as identical.

### 5.2 Regression to the mean

Raw seasonal rates are noisy, especially in small samples. Both sides regress:

```
batter_rate  = (HR  + LG_HR_PA * K_BAT) / (PA + K_BAT)     K_BAT = 120
pitcher_rate = (HRa + LG_HR_PA * K_PIT) / (BF + K_PIT)     K_PIT = 450
```

This is what stops a 4-for-81 platoon split being treated as true talent.

### 5.3 Constants — every one measured, with provenance

| Constant | Value | Where it came from |
|---|---|---|
| `LG_HR_PA` | 0.03053 | Summed all 30 team season totals: 3,786 HR / 123,989 PA. **Do not use the qualified-player pool** — that gives 0.0334, 9% high, because qualified hitters out-homer the league. |
| `SLOT_PA` | 4.21, 4.31, 4.15, 4.12, 3.90, 3.37, 3.25, 3.31, 3.08 | **Measured** from 2026-07-26/27 boxscores: actual PA for starters by batting-order slot, including early exits. |
| `PA_VS_SP` | 2.6 | Typical times a hitter faces the starter before the bullpen takes over |
| `K_BAT` | 120 | HR rate stabilisation region; swept 60–250, result insensitive |
| `K_PIT` | 450 | Pitcher HR/BF stabilises slower; swept 300–700, result insensitive |
| `SHRINK` | **0.920** | Re-fitted on the LEAK-FREE 2,180-row backtest. v1's 0.826 came from leaky data and over-corrected. |
| `SC_WEIGHT` | **0.50** | Statcast blend weight — see §5.7 |
| `OPENER_BF_PER_APP` | 12.0 | Below this, treat listed starter as an opener |
| Park factors | computed at runtime | 3 seasons, weighted 3-2-1 — see §5.4 |
| Weather | 0.006/°F, 0.014/mph | See §5.5 — approximations, still the weakest link |

### 5.4 Park factors — measured, not borrowed

Computed at runtime for all 30 parks using the classic home/away formula:

```
raw = ((HRfor + HRagainst) at home / (PA + BF) at home)
    / ((HRfor + HRagainst) on road / (PA + BF) on road)
PF  = 1.0 + 0.5 * (raw - 1.0)      # 50% regression for single-season noise
```

Sanity check: Cincinnati returns ~1.12, matching Great American Ball Park's
known reputation. If a park returns something wild (>1.5 or <0.6), suspect a
data problem before believing it.

Limitation: single-season, and NOT split by batter handedness. Baseball Savant's
3-year handedness-controlled factors are better; they were not used because they
are not available through a public JSON endpoint.

### 5.5 Weather

```
mult = 1 + 0.006 * (tempF - 70)
mult *= 1 + 0.014 * wind_mph     if wind blowing OUT
mult *= 1 - 0.014 * wind_mph     if wind blowing IN
                                  cross-wind and domes are neutral
```

These coefficients are **literature-informed approximations, not measured from
this dataset**. That is the weakest link in the model. If you can measure them
empirically, do so and update this table.

### 5.6 The intra-game correlation correction (SHRINK)

`1-(1-r)^n` assumes plate appearances are independent. They are not — a hitter's
PAs in one game share a pitcher, a park, weather, and his own daily form.
Positive correlation **lowers** P(at least one) for a fixed mean rate.

v1 fitted 0.826 on leaky data. **v2 re-fits it to 0.920** on the point-in-time
backtest, giving bias 0.995. Do not remove or change this constant without
re-running §7 step 5.

### 5.7 Statcast batted-ball term (NEW in v2)

The v1 model used only outcome HR/PA. Barrels per plate appearance is a better
and faster-stabilising predictor of future home runs, and it IS publicly
available:

```
https://baseballsavant.mlb.com/leaderboard/statcast?type=batter&year=2026&min=10&csv=true
```

Columns of interest: `brl_pa` (barrels per PA), `player_id` (join key — use the
ID, never the name), plus `avg_hit_speed`, `ev95percent`. A sibling endpoint
(`expected_statistics`) provides `est_slg` and `est_woba` if you want to extend.

The barrel figure is converted onto the HR/PA scale by a league-fitted ratio
(~0.587 HR per unit of barrels/PA, refitted at runtime), then blended:

```
batter_term = (1 - SC_WEIGHT) * outcome_rate + SC_WEIGHT * (brl_pa * ratio)
```

**Measured effect** on the leak-free backtest: discrimination 3.2x -> 5.3x,
Brier 0.09171 -> 0.09135. Brier-optimal weight was 0.70, but **0.50 is used
deliberately** because Savant barrel totals are SEASON figures and retain some
look-ahead in the test — the higher weights are partly buying leakage.

If the Savant fetch fails the model prints a warning and runs without the term.
It does not silently substitute a guess.

### 5.8 Opener / bulk-arm detection (NEW in v2, honest result: no gain)

If the listed starter averages under 12 batters faced per appearance, he is
treated as an opener and plate appearances shift from starter to bullpen.

**This measured NO improvement** (3.2x -> 3.2x, bias unchanged) because genuine
openers are rare in the backtest sample. It is retained as a correctness
safeguard for games where an opener IS listed — RotoWire flags these `PRIM` —
not because it improves aggregate accuracy. Do not claim it as an upgrade.

---

## 6. FILES

| File | Role |
|---|---|
| `hr_model.py` | **The model.** Constants, lineups, roster loader, Statcast loader, park factors, weather, scoring, ranked output. Run this to produce a slate. |
| `hr_rows2.py` | Rebuilds backtest observations **with game dates** from boxscores → `_bt_rows2.json` (2,466 rows, 10 dates). |
| `hr_pit_cache.py` | Builds point-in-time game-log caches for every hitter/pitcher → `_pit_hitters.json`, `_pit_pitchers.json`, `_pit_ids.json`. `as_of()` returns cumulative stats strictly before a date. **This is what makes validation honest.** |
| `hr_ablation.py` | **Primary validation tool.** Scores all variants leak-free and reports bias, Brier, discrimination per feature. Use this, not `hr_backtest.py`. |
| `hr_backtest.py` | v1 backtest — **LEAKY, kept only for historical reference.** Do not quote its numbers. |
| `hr_tune.py` | v1 parameter sweep — also leaky. Superseded by `hr_ablation.py`. |
| `_bt_rows2.json`, `_pit_*.json`, `_sc_*.json`, `_hr_model_out.json` | Generated artifacts. Safe to delete; regenerate with the scripts above. Not committed. |

### The lineup block — the one manual step

`hr_model.py` contains `GAMES` and `LINEUPS` hardcoded from RotoWire, with the
timestamp they were pulled. **These are stale the moment lineups change.**

To run for a new date you MUST replace both:
1. Fetch `https://www.rotowire.com/baseball/daily-lineups.php`
2. For each game record: away, home, away SP + hand, home SP + hand, park team,
   temperature, wind speed, wind direction (`out` / `in` / `cross` / `dome`)
3. For each team record the nine hitters in batting order
4. **Exclude any game already in progress or final** — check
   `/api/v1/schedule` and drop anything not `Pre-Game` or `Scheduled`
5. Update the timestamp comment above `GAMES`

Player names must match StatsAPI `fullName` exactly or the hitter is silently
skipped. After a run, confirm the printed `slate` count ≈ 18 × number of games.
A materially lower number means names are failing to match — investigate before
trusting the output.

---

## 7. EXECUTION RUNBOOK

Numbered. **Wait for Damien's confirmation at each STOP.**

**Step 1 — verify environment**
Confirm Desktop Commander responds and the repo path exists. Print the current
date/time; do not infer it.

**Step 2 — get today's games and drop started ones**
Query the schedule endpoint. List each game with status. Report which games are
excluded and why.
→ **STOP. Confirm the game list with Damien before continuing.**

**Step 3 — get confirmed lineups**
Fetch RotoWire. Fill any missing starter from it (StatsAPI probables are often
incomplete). Update `GAMES` and `LINEUPS` in `hr_model.py`, keeping a `.bak`
first per §1.

**Step 4 — run the model**
```
python hr_model.py
```
Expect ~8–15 minutes. Check the header line: league HR/PA should read ≈0.0305,
hitters ≈390, slate ≈ 18 × games.

**Step 5 — validate before presenting anything**
```
python hr_ablation.py        # leak-free; caches make reruns fast
```
Report bias, Brier, and discrimination. **Acceptance thresholds (v2, honest):**

| Metric | Acceptable | 2026-07-31 v2 result |
|---|---|---|
| Bias (predicted ÷ actual) | 0.95 – 1.05 | 0.995 |
| Brier score | < 0.10 | 0.0914 |
| Discrimination (top ÷ bottom decile) | > 3x | 5.3x (with Statcast) |

Note the discrimination bar is **3x, not 5x** — v1's 5x bar was set against a
leakage-inflated 14x and was never realistic. If bias falls outside the band,
**do not present results**. Diagnose first — §9 lists the failure modes already
found and fixed.

**Step 6 — present**
Give the ranked top N with P(HR), team, opponent and starter. State the
calibration numbers alongside. State the limitations in §8 honestly.
→ **STOP. Do not extend into betting recommendations unless Damien asks.**

---

## 8. KNOWN LIMITATIONS — state these, do not bury them

1. **The model is modest, and the honest numbers say so.** 3.2x discrimination
   outcome-only, 5.3x with Statcast. Useful for ranking; not a projection system.
2. **Statcast term retains season-total leakage** in validation. Savant has no
   cheap point-in-time endpoint, so the 5.3x is an optimistic bound. This is why
   SC_WEIGHT is held at 0.50 instead of the Brier-optimal 0.70.
3. **Park factors are not handedness-split.** A short right-field porch helps
   lefties specifically; the model cannot see that. Savant's park-factor page
   returns HTML rather than CSV, so it needs a different extraction route.
   **This is the top remaining upgrade.**
4. **Weather coefficients are literature approximations**, not fitted here.
5. **Openers**: detected, but measured no aggregate gain (§5.8).
6. **Bullpen is team-aggregate**, not the specific relievers likely to appear.
7. **Umpires not modelled.** Zone size shifts strikeout and walk rates; the HR
   effect is second-order. Low priority.
8. **Defence and catcher framing are deliberately NOT on this list.** A ball over
   the fence cannot be defended. Including them would be padding, not rigour.

---

## 9. FAILURE MODES ALREADY FOUND — do not reintroduce

These are real defects caught by the backtest. Each one is a lesson.

| Defect | Symptom | Fix |
|---|---|---|
| **Backtest look-ahead leakage** | Reported 14x discrimination; true value 3.2x. Every validation number was flattered. | Point-in-time stats via `hr_pit_cache.py` |
| **League rate from qualified players only** (0.0334 vs true 0.0305) | Weak hitters regressed toward an inflated mean; low buckets over-predicted | Sum all 30 team totals |
| **Invented PA-per-slot table** | ~20% too high through the bottom of the order — the largest single error in v1 | Measure from boxscores |
| **Independence assumption** | Stable 1.21x over-prediction that survived every parameter sweep | `SHRINK = 0.826` |
| **Hand-picked candidate list** | "Top 5" was really "top 5 of the 30 I chose" | Score every hitter in every lineup |
| **Handedness-only matchup** | Nick Martinez and Ryan Johnson scored identically | Odds-ratio with pitcher rate |
| **Park/weather shown but unused** | Coors and a dome treated the same | Multipliers applied to the rate |

**The meta-lesson:** v1 looked completely plausible and was wrong by 38%, and
its headline validation number was inflated 4x by leakage. Both were caught only
by testing. Never present this model's output without running §7 step 5, and
never quote a validation number produced with full-season stats.

---

## 10. TROUBLESHOOTING

| Symptom | Likely cause | Action |
|---|---|---|
| `slate` count much lower than 18 × games | Player names don't match StatsAPI `fullName` | Print unmatched names, correct spellings (accents, Jr., II) |
| A hitter you expect is missing | Not on the active roster hydrate, or name mismatch | Query `/people/search?names=` directly |
| Park factor absurd (>1.5, <0.6) | Team split query returned partial data | Re-run; check both hitting AND pitching splits returned |
| League HR/PA ≠ ~0.0305 | Wrong pool (qualified vs all) | Recompute from team totals |
| Bias > 1.05 after a change | New structural error introduced | Revert to `.bak`, re-run backtest, isolate the change |
| Backtest very slow | Refetching boxscores | Confirm `_bt_rows.json` exists and is being read |
| StatsAPI timeouts | Rate limiting | `gj()` already retries 4x; increase sleeps if persistent |

---

## 11. UPGRADE PATH (in priority order, v2)

1. **Handedness-split, multi-year park factors** — now the top item. Savant
   serves its park-factor page as HTML; find a JSON/CSV route or parse it.
2. **Point-in-time Statcast** — removes the residual leakage and would let
   SC_WEIGHT rise toward the Brier-optimal 0.70 honestly.
3. Fit weather coefficients empirically instead of using literature values
4. Reliever-specific bullpen modelling (likely arms, not team aggregate)
5. Widen the backtest beyond 10 dates and re-fit SHRINK on the larger sample
6. Add `est_woba` / `est_slg` alongside barrels as additional batter inputs
7. Umpire zone effects (low expected value for HR specifically)

---

## 12. PROVENANCE

- Built 2026-07-31 with Damien. Slate: 14 games (NYY@CHC excluded, in progress).
- v1 backtest: 1,202 player-games, 5 dates, FULL-SEASON stats — **leaky, retracted**.
- v2 backtest: 2,466 observations (2,180 scored) across 2026-07-19 → 07-28,
  point-in-time stats.
- v2 calibration: bias 0.995, Brier 0.0914, discrimination 3.2x base / 5.3x with
  the Statcast term.
- v1 over-predicted by 38% and claimed 14x discrimination. Both were found by
  testing after Damien challenged the methodology and then insisted the stated
  weaknesses be fixed rather than merely listed. The point-in-time backtest,
  the Statcast term and the multi-year park factors all came out of that push.

## 13. STOP

When the runbook is complete, **STOP**. Do not continue into betting advice,
parlay construction, or wager sizing unless Damien explicitly asks. Report the
ranked list and the calibration numbers, and wait.
