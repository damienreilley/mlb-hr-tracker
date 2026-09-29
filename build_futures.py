import json, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
BETS = json.load(open(os.path.join(HERE, "futures_bets.json"), encoding="utf-8"))

# market display order (cleaner-to-grade groups first, awards after)
ORDER = ["World Series Winner","World Series \u2014 Exact Result","Pennant \u2014 Exact Result",
         "World Series \u2014 Finalists","World Series \u2014 First-Time Winner","League Winners",
         "World Series MVP","NL MVP","AL MVP","NL Cy Young","AL Cy Young",
         "NL Rookie of the Year","AL Rookie of the Year","Award Parlays","Other Futures"]
def okey(m): return ORDER.index(m) if m in ORDER else len(ORDER)

tot = len(BETS)
wag = sum((b["wager"] or 0) for b in BETS)
pot = sum((b["payout"] or 0) for b in BETS)
build = time.strftime("%m/%d %H:%M", time.localtime())

TPL = open(os.path.join(HERE, "_futures_template.html"), encoding="utf-8").read()
html = (TPL
        .replace("__BETS__", json.dumps(BETS, separators=(",", ":")))
        .replace("__TOT__", str(tot))
        .replace("__WAG__", "%.2f" % wag)
        .replace("__POT__", "%.2f" % pot)
        .replace("__BUILD__", build))
open(os.path.join(HERE, "futures.html"), "w", encoding="utf-8", newline="\n").write(html)
print("wrote futures.html | bets=%d wager=$%.2f potential=$%.2f" % (tot, wag, pot))
