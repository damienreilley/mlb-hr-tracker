import sys, json, os
repo = r"C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker"
sys.path.insert(0, repo)
import parse_futures as PF

src = sys.argv[1]
existing = json.load(open(os.path.join(repo, "futures_bets.json"), encoding="utf-8"))
have = {b["full_id"] for b in existing}
new = [b for b in PF.parse(src) if b["full_id"] not in have]
merged = existing + new   # additive, dedup by full_id (status of existing preserved)
json.dump(merged, open(os.path.join(repo, "futures_bets.json"), "w", encoding="utf-8", newline="\n"), indent=1)
print("existing:", len(existing), "| added:", len(new), "| total futures:", len(merged))
for b in new:
    print("  +", b["sel"][:50], "|", b["market"])
