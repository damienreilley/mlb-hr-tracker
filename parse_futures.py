import re, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import parse_fanduel as P

# A block is a FUTURE if any line carries one of these season-long market signatures.
FUT = re.compile(r"(world series|american league 20\d\d|national league 20\d\d|"
                 r"league mvp|league rookie of the year|league cy young|"
                 r"award parlays|name the finalists|first-time winner)", re.I)

NOISE = {"total wager","total payout","reuse selection","reuse selections","share bet",
         "box score","play-by-play","go to event","ab:","p:","b","s","o","t","cash out"}

def is_noise(s):
    t = s.strip().lower()
    if not t or t.startswith("$") or t.startswith("bet id:") or t.startswith("placed:"): return True
    if t in NOISE or t.startswith("cash out"): return True
    if re.fullmatch(r"[+-]?\d+", t): return True
    if t.startswith("same game parlay"): return True
    if re.match(r"^(top|bot) \d", t): return True
    return False

def market_group(u):
    u = u.upper()
    if "AWARD PARLAYS" in u or "MVP & CY YOUNG" in u: return "Award Parlays"
    if "WORLD SERIES MVP" in u: return "World Series MVP"
    if "NAME THE FINALISTS" in u: return "World Series \u2014 Finalists"
    if "FIRST-TIME WINNER" in u: return "World Series \u2014 First-Time Winner"
    if "WORLD SERIES" in u and "EXACT RESULT" in u: return "World Series \u2014 Exact Result"
    if "WORLD SERIES" in u and "WINNER" in u: return "World Series Winner"
    if ("AMERICAN LEAGUE" in u or "NATIONAL LEAGUE" in u) and "EXACT RESULT" in u: return "Pennant \u2014 Exact Result"
    if "MVP" in u: return "AL MVP" if "AMERICAN" in u else "NL MVP"
    if "ROOKIE OF THE YEAR" in u: return "AL Rookie of the Year" if "AMERICAN" in u else "NL Rookie of the Year"
    if "CY YOUNG" in u: return "AL Cy Young" if "AMERICAN" in u else "NL Cy Young"
    if "LEAGUE" in u and "WINNER" in u: return "League Winners"
    return "Other Futures"

def parse(path):
    raw = open(path, encoding="utf-8").read().splitlines()
    lines = [l.strip() for l in raw if l.strip() != ""]
    blocks, cur = [], []
    for ln in lines:
        cur.append(ln)
        if ln.startswith("PLACED:"): blocks.append(cur); cur = []
    out = []
    for b in blocks:
        b = P.trim_preamble(b)
        label = next((l for l in b if FUT.search(l)), None)
        if not label: continue                       # not a future -> skip (game bet)
        bid = next((l.split("BET ID:",1)[1].strip() for l in b if l.startswith("BET ID:")), None)
        placed = next((l.split("PLACED:",1)[1].strip() for l in b if l.startswith("PLACED:")), "")
        sel = next((l for l in b if not is_noise(l) and l != label and not FUT.search(l)), None)
        if sel is None or re.match(r"^\d+ leg ", sel.lower()) or sel.lower().startswith("same game parlay"):
            sel = label   # parlay: the leg-summary line (the matched label) is the most descriptive pick
        mo = re.search(r"(?<![\d])[+-]\d{2,}(?!\d)", " ".join(b))
        odds = mo.group(0) if mo else ""
        out.append({
            "id": "#"+bid[-6:] if bid else "?", "full_id": bid,
            "market": market_group(label), "market_raw": label.strip(),
            "sel": sel.strip(), "odds": odds,
            "wager": P.money_before(b, "TOTAL WAGER"),
            "payout": P.money_before(b, "TOTAL PAYOUT"),
            "placed": placed, "status": "alive",
        })
    return out

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "_paste_0929_6pm_ALL.txt")
    bets = parse(src)
    outp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "futures_bets.json")
    json.dump(bets, open(outp, "w", encoding="utf-8", newline="\n"), indent=1)
    from collections import Counter
    print("FUTURES parsed:", len(bets))
    print("total wager: $%.2f" % sum((x["wager"] or 0) for x in bets))
    ids = [x["full_id"] for x in bets]
    print("unique ids:", len(set(ids)), "| dups:", [k for k,v in Counter(ids).items() if v>1])
    print("by market:")
    for m, c in sorted(Counter(x["market"] for x in bets).items(), key=lambda kv: -kv[1]):
        print("   %-32s %d" % (m, c))
    print("wrote", outp)
