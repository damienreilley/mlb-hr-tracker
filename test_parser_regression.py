#!/usr/bin/env python3
"""Golden-baseline regression test over the LOCAL paste corpus (Backlog #27).

Replaces the ad-hoc old-vs-new diff scripts that were written and thrown away on
each parser change. Run before AND after any parser edit:

    python test_parser_regression.py            # assert current parser == baseline
    python test_parser_regression.py --update   # regenerate baseline (REVIEW the diff first)

The baseline stores per-file counts plus a SHA1 of each bet's canonical JSON - no raw
bet text - so it is safe to commit to this PUBLIC repo. The _paste_*.txt corpus itself
is NOT tracked in git; if no pastes are present this SKIPS with exit 0, so the test is
harmless in CI while still protecting the local workflow.
"""
import sys, os, glob, json, hashlib
import parse_fanduel as P

BASE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(BASE, "parser_baseline.json")


def snapshot():
    """Parse every corpus paste and reduce it to a comparable fingerprint."""
    out = {}
    for path in sorted(glob.glob(os.path.join(BASE, "_paste_*.txt"))):
        name = os.path.basename(path)
        raw = open(path, encoding="utf-8", errors="replace").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        blocks, dropped = P.split_blocks_checked(lines)
        bets, flags = [], []
        for blk in blocks:
            bet, fl = P.parse_bet(blk)
            if bet:
                bets.append(bet)
            flags += fl
        hashes = {}
        for b in bets:
            canon = json.dumps(b, sort_keys=True, separators=(",", ":"))
            hashes[b["id"]] = hashlib.sha1(canon.encode("utf-8")).hexdigest()[:12]
        out[name] = {
            "bets": len(bets),
            "legs": sum(len(b["legs"]) for b in bets),
            "flags": len(flags),
            "dropped": len(dropped),
            "hashes": hashes,
        }
    return out


def compare(base, cur):
    """Return a list of human-readable regressions. Empty list == clean."""
    problems = []
    for name in sorted(set(base) | set(cur)):
        b, c = base.get(name), cur.get(name)
        if b is None:
            continue  # new corpus file - not a regression, picked up on --update
        if c is None:
            problems.append("%s: MISSING from corpus (baseline had %d bets)" % (name, b["bets"]))
            continue
        for k in ("bets", "legs", "flags", "dropped"):
            if b[k] != c[k]:
                problems.append("%s: %s %d -> %d" % (name, k, b[k], c[k]))
        bh, ch = b.get("hashes", {}), c.get("hashes", {})
        lost = sorted(set(bh) - set(ch))
        gained = sorted(set(ch) - set(bh))
        changed = sorted(i for i in bh if i in ch and bh[i] != ch[i])
        if lost:
            problems.append("%s: BETS LOST %s" % (name, lost[:8]))
        if gained:
            problems.append("%s: bets gained %s" % (name, gained[:8]))
        if changed:
            problems.append("%s: BETS CHANGED %s" % (name, changed[:8]))
    return problems


def main():
    update = "--update" in sys.argv
    cur = snapshot()
    if not cur:
        print("SKIP: no _paste_*.txt corpus present (not tracked in git) - nothing to check.")
        return 0
    if update or not os.path.exists(BASELINE):
        with open(BASELINE, "w", encoding="utf-8", newline="\n") as f:
            json.dump(cur, f, indent=1, sort_keys=True)
        tot = sum(v["bets"] for v in cur.values())
        print("BASELINE WRITTEN: %d files, %d bets -> %s" % (len(cur), tot, os.path.basename(BASELINE)))
        return 0
    base = json.load(open(BASELINE, encoding="utf-8"))
    problems = compare(base, cur)
    if problems:
        print("REGRESSION DETECTED (%d):" % len(problems))
        for p in problems:
            print("   ", p)
        print("\nIf these changes are INTENTIONAL, re-run with --update after reviewing.")
        return 1
    tot = sum(v["bets"] for v in cur.values())
    print("PARSER REGRESSION: PASS - %d files, %d bets identical to baseline" % (len(cur), tot))
    return 0


if __name__ == "__main__":
    sys.exit(main())
