"""Local test for add_bet_core. Run: python add-bet-server/test_add_bet_core.py"""
import os, sys, json, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import add_bet_core as C

FOURLEG = """Same Game Parlay
+41376
Bryce Harper To Hit A Home Run, Juan Soto To Hit A Home Run, Alec Bohm To Record 2+ RBIs, Bryson Stott To Record A Stolen Base
New York Mets (S Manaea) @ Philadelphia Phillies (A Nola)
6:41pm ET
Bryce Harper
To Hit A Home Run
Juan Soto
To Hit A Home Run
Alec Bohm
To Record 2+ RBIs
Bryson Stott
To Record A Stolen Base
$0.09
TOTAL WAGER
$37.33
TOTAL PAYOUT
BET ID: us-pa:01kve96s3keh99ebe88fdks2bg
PLACED: 6/18/2026 5:11PM ET
"""

def base_staging():
    return {"date": "2026-06-18", "bets": [{"id": "#aaa111", "legs": []}, {"id": "#bbb222", "legs": []}]}

results = []

# 1. clean add
s = base_staging()
r = C.process(FOURLEG, s)
ok = r["ok"] and r["added"] == ["#dks2bg"] and len(r["staging"]["bets"]) == 3 and r["receipt"][0]["legs"] == 4 and r["receipt"][0]["payout"] == 37.33
results.append(("clean add publishes", ok, "added=%s legs=%s payout=%s" % (r.get("added"), r["receipt"][0]["legs"] if r.get("ok") else "-", r["receipt"][0]["payout"] if r.get("ok") else "-")))

# 2. dedup on re-add (staging already has it)
r2 = C.process(FOURLEG, r["staging"])
ok = r2["ok"] and r2["added"] == [] and r2["skipped_dup"] == ["#dks2bg"] and len(r2["staging"]["bets"]) == 3
results.append(("re-add dedups (no double-post)", ok, "added=%s skipped=%s total=%d" % (r2.get("added"), r2.get("skipped_dup"), len(r2["staging"]["bets"]))))

# 3. date mismatch -> halt
newday = FOURLEG.replace("6/18/2026", "6/19/2026")
r3 = C.process(newday, base_staging())
ok = (not r3["ok"]) and r3["reason"] == "date_mismatch"
results.append(("new-day bet halts (rollover needed)", ok, "ok=%s reason=%s" % (r3["ok"], r3.get("reason"))))

# 4. flag-gate: drop a leg from the body so parsed(3) != summary(4)
garbled = FOURLEG.replace("Bryson Stott\nTo Record A Stolen Base\n", "")
r4 = C.process(garbled, base_staging())
ok = (not r4["ok"]) and r4["reason"] == "parser_flags" and any("LEG COUNT MISMATCH" in f for f in r4["flags"])
results.append(("flagged parse halts (not published)", ok, "ok=%s reason=%s flags=%s" % (r4["ok"], r4.get("reason"), r4.get("flags"))))

# 5. missing-money gate: strip the money block so wager/payout can't be read
nomoney = FOURLEG.replace("$0.09\nTOTAL WAGER\n$37.33\nTOTAL PAYOUT\n", "")
r5 = C.process(nomoney, base_staging())
ok = (not r5["ok"]) and r5["reason"] == "missing_money" and any("dks2bg" in f for f in r5["flags"])
results.append(("missing money halts (not published)", ok, "ok=%s reason=%s" % (r5["ok"], r5.get("reason"))))

# 6. tolerant layout: amount BELOW the label (phone/screenshot order)
afterlbl = FOURLEG.replace("$0.09\nTOTAL WAGER\n$37.33\nTOTAL PAYOUT\n", "TOTAL WAGER\n$0.09\nTOTAL PAYOUT\n$37.33\n")
r6 = C.process(afterlbl, base_staging())
ok = r6["ok"] and r6["receipt"][0]["wager"] == 0.09 and r6["receipt"][0]["payout"] == 37.33
results.append(("money read when amount trails label", ok, "ok=%s w=%s p=%s" % (r6["ok"], r6["receipt"][0]["wager"] if r6.get("ok") else "-", r6["receipt"][0]["payout"] if r6.get("ok") else "-")))

# 7. tolerant layout: inline "LABEL: $x"
inlinem = FOURLEG.replace("$0.09\nTOTAL WAGER\n$37.33\nTOTAL PAYOUT\n", "TOTAL WAGER: $0.09\nTOTAL PAYOUT: $37.33\n")
r7 = C.process(inlinem, base_staging())
ok = r7["ok"] and r7["receipt"][0]["wager"] == 0.09 and r7["receipt"][0]["payout"] == 37.33
results.append(("money read inline (LABEL: $x)", ok, "ok=%s w=%s p=%s" % (r7["ok"], r7["receipt"][0]["wager"] if r7.get("ok") else "-", r7["receipt"][0]["payout"] if r7.get("ok") else "-")))

print("=" * 70)
allok = True
for name, ok, detail in results:
    print("%-4s %-36s %s" % ("PASS" if ok else "FAIL", name, detail)); allok = allok and ok
print("=" * 70)
print("ALL PASS" if allok else "SOME FAILED")
