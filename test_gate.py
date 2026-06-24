import sys, os
R=r"C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker"
sys.path.insert(0,R)
import daily_run as D

def mk(id, odds, wager, payout, legs, void=False):
    return {"full_id":id,"id":id,"kind":"x","odds":odds,"wager":wager,"payout":payout,
            "placed":"6/24 1:00PM","status":"open","void":void,
            "legs":[{"p":p,"prop":pr,"g":"AAA@BBB","asp":"x","hsp":"y"} for p,pr in legs]}

# clean bet: $1 at +200 -> payout 3.00
clean = mk("#clean", 200, 1.0, 3.00, [("Real Player","HR")])
# garble: leg player is a bare number
garble = mk("#garble", 200, 1.0, 3.00, [("-145","HR")])
# payout BELOW odds-math, no void  -> should HOLD
low = mk("#low", 200, 1.0, 2.00, [("Real Player","HR")])   # expected 3.00, got 2.00
# boost: payout ABOVE odds-math -> should NOT hold (note only)
boost = mk("#boost", 200, 1.0, 4.50, [("Real Player","HR")])  # +50%
# void bet, payout below odds -> should NOT hold (void carve-out)
voidb = mk("#void", 200, 1.0, 2.00, [("Real Player","HR")], void=True)

bets=[clean,garble,low,boost,voidb]
holds,notes = D.gate(bets, "FLAGS: none\nUNRESOLVED GAMES (g=??): none\nMISSING odds/wager/payout: none\nMANUAL/NA legs: none\nDUP IDS: none")
held_ids={h[0] for h in holds}
print("HELD:", held_ids)
print("expected held: {'#garble','#low'}")
assert held_ids=={"#garble","#low"}, "GATE LOGIC WRONG: "+str(holds)
print("PASS: gate holds garble + payout-below, passes clean/boost/void")

# parser-flag passthrough
holds2,_ = D.gate([clean], "FLAGS (1):\n  - LEG COUNT MISMATCH header=5 parsed=0 | O/1924696/0004200\n")
print("flag-passthrough held:", holds2)
assert any("0004200" in h[0] for h in holds2), "parser flag not passed through"
print("PASS: parser FLAGS block routes to a hold")
print("ALL GATE TESTS PASS")
