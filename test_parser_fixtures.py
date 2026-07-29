#!/usr/bin/env python3
"""Synthetic fixture tests for parse_fanduel (Backlog #27).

WHY THIS EXISTS: the real _paste_*.txt corpus is NOT tracked in git (it is personal
betting history and this repo is PUBLIC), so CI had no way to exercise the parser.
These fixtures are FABRICATED betslips - no real bet IDs, no personal data - that
pin the behaviour of every bug class we have hit:

    #23 straight singles silently dropped
    #24 Correct Score dropped + unknown bet types vanishing (drop detector)
    #25 settled bets ("RETURNED") parsed as still-open
    #26 first-plate-appearance HR prop unmapped
    plus pitcher specials and the leg-count mismatch flag

Run:  python test_parser_fixtures.py     (exit 0 = pass, 1 = fail)
"""
import sys
import parse_fanduel as P

FAILS = []


def parse_one(text):
    """Parse a single fixture betslip -> (bet, flags, dropped)."""
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    blocks, dropped = P.split_blocks_checked(lines)
    if not blocks:
        return None, [], dropped
    bet, flags = P.parse_bet(blocks[0])
    return bet, flags, dropped


def check(name, cond, detail=""):
    if cond:
        print("  PASS  %s" % name)
    else:
        print("  FAIL  %s   %s" % (name, detail))
        FAILS.append(name)


SINGLE = """
Kyle Schwarber
+200
TO HIT A HOME RUN
New York Mets (S Manaea) @ Philadelphia Phillies (J Luzardo)
3:06pm ET
$0.12
TOTAL WAGER
$0.36
TOTAL PAYOUT
Reuse selection
Share bet
BET ID: us-pa:01fixture00000000000singla
PLACED: 7/29/2026 1:57PM ET
"""

FPA_PARLAY = """
2 leg parlay
+1000
Jose Ramirez To Hit A Home Run, Yordan Alvarez Player to Hit a Home Run in First Plate Appearance

Jose Ramirez
+255
To Hit A Home Run
Cleveland Guardians (J Cantillo) @ Cincinnati Reds (B Singer)
7:11pm ET

Yordan Alvarez
+750
Player to Hit a Home Run in First Plate Appearance
Houston Astros (H Wesneski) @ Los Angeles Angels (G Rodriguez)
9:39pm ET
$0.10
TOTAL WAGER
$1.10
TOTAL PAYOUT
BET ID: us-pa:01fixture0000000000000fpa1
PLACED: 7/29/2026 1:24PM ET
"""

CORRECT_SCORE = """
Toronto Blue Jays 8-3
+3500
CORRECT SCORE
Tampa Bay Rays (I Seymour) @ Toronto Blue Jays (S Bieber)
3:08pm ET
$0.10
TOTAL WAGER
$3.60
TOTAL PAYOUT
BET ID: us-pa:01fixture00000000000csbet1
PLACED: 7/29/2026 1:51AM ET
"""

SETTLED_LOST = """
Jose Ramirez
+255
To Hit A Home Run
Cleveland Guardians (J Cantillo) @ Cincinnati Reds (B Singer)
7:11pm ET
$0.20
TOTAL WAGER
$0.00
RETURNED
BET ID: us-pa:01fixture000000000settled1
PLACED: 7/29/2026 1:00PM ET
"""

UNKNOWN_TYPE = """
Some Brand New Market
+700
TOTALLY UNKNOWN MARKET LABEL
Tampa Bay Rays (I Seymour) @ Toronto Blue Jays (S Bieber)
3:08pm ET
$0.10
TOTAL WAGER
$0.80
TOTAL PAYOUT
BET ID: us-pa:01fixture0000000000dropme1
PLACED: 7/29/2026 1:51AM ET
"""

PITCHER_SPECIAL = """
Tarik Skubal to Throw a No-Hitter Through 5 Innings (Min. 15 Outs)
+1700
TARIK SKUBAL PITCHING SPECIALS
Detroit Tigers (T Skubal) @ Los Angeles Angels (G Rodriguez)
10:08pm ET
$0.10
TOTAL WAGER
$1.80
TOTAL PAYOUT
BET ID: us-pa:01fixture00000000000pitch1
PLACED: 7/29/2026 1:52PM ET
"""

LEG_MISMATCH = """
3 leg parlay
+5000
Jose Ramirez To Hit A Home Run, Someone Else Unknown Market Thing

Jose Ramirez
+255
To Hit A Home Run
Cleveland Guardians (J Cantillo) @ Cincinnati Reds (B Singer)
7:11pm ET

Someone Else
+300
Totally Unknown Market Thing
Boston Red Sox (P Sandoval) @ Athletics (J Lopez)
9:41pm ET
$0.10
TOTAL WAGER
$5.10
TOTAL PAYOUT
BET ID: us-pa:01fixture000000000mismatch
PLACED: 7/29/2026 1:30PM ET
"""


def main():
    print("=== #23 straight single must NOT be dropped ===")
    bet, flags, dropped = parse_one(SINGLE)
    check("single parses", bet is not None, str(dropped))
    if bet:
        check("single kind=Single", bet["kind"] == "Single", bet["kind"])
        check("single 1 leg prop HR",
              len(bet["legs"]) == 1 and bet["legs"][0]["prop"] == "HR", str(bet["legs"]))
        check("single no flags", not flags, str(flags))

    print("=== #26 first-plate-appearance HR maps to FPA ===")
    bet, flags, dropped = parse_one(FPA_PARLAY)
    check("fpa parlay parses", bet is not None, str(dropped))
    if bet:
        props = [l["prop"] for l in bet["legs"]]
        check("fpa parlay 2 legs [HR, FPA]", props == ["HR", "FPA"], str(props))
        check("fpa parlay no flags (leg count matches)", not flags, str(flags))

    print("=== #24 Correct Score parses and orients off the label ===")
    bet, flags, dropped = parse_one(CORRECT_SCORE)
    check("cs parses", bet is not None, str(dropped))
    if bet and bet["legs"]:
        l = bet["legs"][0]
        check("cs prop=CS", l["prop"] == "CS", str(l))
        check("cs named team runs first -> home 8 / away 3",
              l.get("hs") == 8 and l.get("as") == 3, str(l))
        check("cs side=home", l.get("side") == "home", str(l.get("side")))

    print("=== #25 RETURNED means SETTLED, not open ===")
    bet, flags, dropped = parse_one(SETTLED_LOST)
    check("settled parses", bet is not None, str(dropped))
    if bet:
        check("settled flag set", bet.get("settled") is True, str(bet.get("settled")))
        check("settled result=lost", bet.get("result") == "lost", str(bet.get("result")))
        check("settled payout=0.0", bet.get("payout") == 0.0, str(bet.get("payout")))
        check("settled status not open", bet.get("status") != "open", str(bet.get("status")))
        check("settled emits a flag", any("SETTLED" in f[0] for f in flags), str(flags))

    print("=== #24 unknown bet type is DETECTED, never silently dropped ===")
    bet, flags, dropped = parse_one(UNKNOWN_TYPE)
    check("unknown type reported in dropped", len(dropped) == 1, str(dropped))

    print("=== pitcher specials still parse ===")
    bet, flags, dropped = parse_one(PITCHER_SPECIAL)
    check("pitcher special parses", bet is not None, str(dropped))
    if bet:
        check("pitcher kind", bet["kind"] == "Pitcher Special", bet["kind"])
        check("pitcher prop NH5",
              bet["legs"] and bet["legs"][0]["prop"] == "NH5", str(bet["legs"]))

    print("=== leg-count mismatch must FLAG (gate hold) ===")
    bet, flags, dropped = parse_one(LEG_MISMATCH)
    check("mismatch flags", any("LEG COUNT MISMATCH" in f[0] for f in flags), str(flags))

    print()
    if FAILS:
        print("FIXTURE TESTS: %d FAILED -> %s" % (len(FAILS), FAILS))
        return 1
    print("FIXTURE TESTS: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
