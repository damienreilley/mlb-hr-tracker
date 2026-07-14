import json, os
from collections import Counter
repo = r"C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker"
d = open(os.path.join(repo, "_paste_derby.txt"), encoding="utf-8").read()
L = [x.strip() for x in d.replace("\r\n", "\n").split("\n")]

PL = {"Junior Caminero":"caminero","Ben Rice":"rice","Jac Caglianone":"caglianone",
      "Willson Contreras":"contreras","Jordan Walker":"walker","Bryce Harper":"harper",
      "Kyle Schwarber":"schwarber","Munetaka Murakami":"murakami"}

def money(s):
    return float(s.replace("$", "").replace(",", ""))

def wp(i):
    j = next(k for k in range(i, min(i + 16, len(L))) if L[k] == "TOTAL WAGER")
    return money(L[j - 1]), money(L[j + 1])

def bid(i):
    b = next(L[k] for k in range(i, min(i + 24, len(L))) if L[k].startswith("BET ID:"))
    return b.split("BET ID:")[1].strip()

bets = []
errs = []
for i, x in enumerate(L):
    try:
        if x == "HOME RUN DERBY CHAMPION 2026":
            w, p = wp(i)
            bets.append(dict(t="CHAMP", ps=[PL[L[i-2]]], odds=L[i-1], w=w, p=p, id=bid(i)))
        elif x == "2026 HR DERBY - EXACT RESULT":
            w, p = wp(i)
            a, b = [y.strip() for y in L[i-2].split(" over ")]
            bets.append(dict(t="EXACT", ps=[PL[a], PL[b]], odds=L[i-1], w=w, p=p, id=bid(i)))
        elif x == "2026 HR DERBY - NAME THE FINALISTS":
            w, p = wp(i)
            a, b = [y.strip() for y in L[i-2].replace(" vs. ", " vs ").split(" vs ")]
            bets.append(dict(t="FINPAIR", ps=[PL[a], PL[b]], odds=L[i-1], w=w, p=p, id=bid(i)))
        elif x == "2026 HR DERBY - PLAYER TO HIT 12+ HOME RUNS IN THE FIRST ROUND":
            w, p = wp(i)
            bets.append(dict(t="R1_12", ps=[PL[L[i-2]]], odds=L[i-1], w=w, p=p, id=bid(i)))
        elif x == "2026 HR DERBY - PLAYER TO HIT THE LONGEST HOME RUN":
            w, p = wp(i)
            bets.append(dict(t="LONGEST", ps=[PL[L[i-2]]], odds=L[i-1], w=w, p=p, id=bid(i)))
        elif x == "2026 HR DERBY - PLAYER TO HIT THE HOME RUN WITH THE HIGHEST EXIT VELOCITY":
            w, p = wp(i)
            bets.append(dict(t="TOPEV", ps=[PL[L[i-2]]], odds=L[i-1], w=w, p=p, id=bid(i)))
        elif x == "2026 HR DERBY - TOTAL HOME RUNS HIT BY ALL PLAYERS IN THE FIRST ROUND":
            w, p = wp(i)
            sel = L[i-2]                       # "First Round Total Home Runs Under 74.5"
            side = "under" if " Under " in sel else "over"
            line = float(sel.split()[-1])
            bets.append(dict(t="FIELD_R1", ps=[], side=side, line=line, odds=L[i-1], w=w, p=p, id=bid(i)))
        elif x == "2026 HR DERBY - TOTAL HOME RUNS HIT BY ALL PLAYERS":
            w, p = wp(i)
            sel = L[i-2]                       # "Total Home Runs Hit Over 117.5"
            side = "under" if " Under " in sel else "over"
            line = float(sel.split()[-1])
            bets.append(dict(t="FIELD_ALL", ps=[], side=side, line=line, odds=L[i-1], w=w, p=p, id=bid(i)))
        elif "LONGEST HR DISTANCE - 2026 HR DERBY" in x or "HIGHEST HR EXIT VELOCITY (MPH) - 2026 HR DERBY" in x or "FIRST ROUND TOTAL HOME RUNS" in x:
            w, p = wp(i)
            sel = L[i-3]
            line = float(L[i-2])
            side = sel.split()[-1].lower()
            nm = " ".join(sel.split()[:-1])
            if "LONGEST HR DISTANCE" in x:
                typ = "DIST"
            elif "HIGHEST HR EXIT VELOCITY" in x:
                typ = "EV"
            else:
                typ = "R1OU"
            bets.append(dict(t=typ, ps=[PL[nm]], side=side, line=line, odds=L[i-1], w=w, p=p, id=bid(i)))
    except Exception as e:
        errs.append((x, repr(e)))

ids = [b["id"] for b in bets]
file_ids = [l.split("BET ID:")[1].strip() for l in L if l.startswith("BET ID:")]
print("FILE BET IDs :", len(file_ids), "unique", len(set(file_ids)))
print("PARSED       :", len(bets), "unique", len(set(ids)))
print("MISSING      :", [i for i in file_ids if i not in ids])
print("ERRORS       :", errs)
print("TYPES        :", dict(Counter(b["t"] for b in bets)))
print("TOTAL WAGER  : $%.2f" % sum(b["w"] for b in bets))

for b in bets:
    b["id"] = b["id"][-6:]
out = os.path.join(repo, "derby_bets.json")
json.dump(bets, open(out, "w", encoding="utf-8"), indent=1)
print("WROTE", out)
print("JSON:", json.dumps(bets, separators=(",", ":")))
