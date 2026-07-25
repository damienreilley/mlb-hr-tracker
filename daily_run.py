#!/usr/bin/env python3
# daily_run.py - ONE-CALL intake gate + writer for the MLB HR tracker.
# Replaces the manual multi-step intake with a single deterministic pass.
# Does NOT push. It writes staging.json (unless --dry-run) and prints a report
# plus the exact git commands to run. The GATE decides publish/hold per bet -
# no human eyeballing of raw text.
#
# Usage:
#   python daily_run.py <paste.txt> [--today YYYY-MM-DD] [--staging PATH]
#                       [--dry-run] [--auto-rollover]
#
# Modes (auto-detected from staging "date" vs today):
#   staging.date  < today  -> NEW-DAY ROLLOVER (needs --auto-rollover to write;
#                             archives prior day, then writes today populated)
#   staging.date == today  -> SAME-DAY ADD (read staging, append, dedup by full_id)
#   staging.date  > today  -> ERROR (refuse)
import sys, os, re, json, subprocess, shutil, datetime, argparse
R = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
sys.path.insert(0, R)
import parse_fanduel as P

def dec(am): return 1 + am/100.0 if am > 0 else 1 + 100.0/abs(am)

def run_parser(paste):
    out = os.path.join(R, "_dr_parsed.json")
    pr = subprocess.run([PY, os.path.join(R, "parse_fanduel.py"), paste, out],
                        capture_output=True, text=True, cwd=R)
    data = json.load(open(out, encoding="utf-8"))
    return data, pr.stdout, pr.stderr

def leg_void(l):  return bool(l.get("void"))
def bet_void(b):  return bool(b.get("void")) or any(leg_void(l) for l in b.get("legs", []))

def gate(bets, parser_stdout):
    """Deterministic gate. Returns (holds, notes). holds = list of (id, reason)."""
    holds, notes = [], []
    # 1) parser's own FLAGS block -> any flag holds that bet
    if "FLAGS:" in parser_stdout and "FLAGS: none" in parser_stdout:
        pass
    else:
        for line in parser_stdout.splitlines():
            line = line.strip()
            if line.startswith("- ") and "|" in line:
                msg, ctx = line[2:].rsplit("|", 1)
                msg = msg.strip()
                # MANUAL/NA legs (First HR, First 5 Innings, Race To N) are intentional
                # "track on FanDuel" legs, not errors -> note, never hold.
                if msg.startswith("MANUAL leg"):
                    notes.append("manual/NA leg (publish OK): %s | %s" % (msg, ctx.strip()))
                elif msg.startswith("SETTLED by FanDuel"):
                    # FanDuel-settled result (RETURNED line). Authoritative, publish as-is.
                    notes.append("settled (publish OK): %s | %s" % (msg, ctx.strip()))
                else:
                    holds.append((ctx.strip(), "parser flag: " + msg))
    # 2) parser summary lines that signal problems
    for key, label in [("UNRESOLVED GAMES (g=??):", "unresolved game"),
                       ("MISSING odds/wager/payout:", "missing odds/wager/payout"),
                       ("MANUAL/NA legs:", "manual/NA leg"),
                       ("DUP IDS:", "duplicate id")]:
        for line in parser_stdout.splitlines():
            if line.startswith(key) and "none" not in line:
                notes.append(label + " -> " + line.split(":", 1)[1].strip())
    # 3) garble: no leg player field is a bare signed number (Error #86)
    bare = re.compile(r"^[+-]?\d+$")
    for b in bets:
        for l in b["legs"]:
            if l.get("p") and bare.fullmatch(str(l["p"]).strip()):
                holds.append((b["id"], "garble: player field is a number (%r)" % l["p"]))
    # 4) payout-vs-odds: hold only if payout is LOWER than odds-math by >2% and
    #    NOT a void bet. Boost (payout higher) is legitimate -> publish (Error #85/#88).
    for b in bets:
        o, w, p = b.get("odds"), b.get("wager"), b.get("payout")
        if None in (o, w, p) or bet_void(b) or b.get("settled"):
            continue  # settled bets carry FanDuel's actual return, not odds-math
        exp = w*dec(o)
        if exp <= 0: continue
        diff = (p-exp)/exp
        if diff < -0.02:
            holds.append((b["id"], "payout %.2f BELOW odds-math %.2f (%.1f%%), no void" % (p, exp, diff*100)))
        elif diff > 0.02:
            notes.append("%s: payout %.2f above odds-math %.2f (+%.1f%%) = profit boost, OK" % (b["id"], p, exp, diff*100))
    # de-dup holds by (id,reason)
    seen=set(); H=[]
    for h in holds:
        if h not in seen: seen.add(h); H.append(h)
    return H, notes

def verify_build(staging_path):
    """Build to a TEMP file (never the tracked index.html) just to confirm
    build.py succeeds and to read the counts. Returns the build stdout line."""
    tmp = os.path.join(R, "_dr_index_verify.html")
    pr = subprocess.run([PY, os.path.join(R, "build.py"), staging_path, tmp],
                        capture_output=True, text=True, cwd=R)
    try: os.remove(tmp)
    except OSError: pass
    return (pr.stdout or pr.stderr).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paste")
    ap.add_argument("--today", default=None)
    ap.add_argument("--staging", default=os.path.join(R, "staging.json"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--auto-rollover", action="store_true")
    a = ap.parse_args()

    today = a.today or datetime.datetime.now().strftime("%Y-%m-%d")
    staging = json.load(open(a.staging, encoding="utf-8"))
    prior = staging.get("date")
    mode = ("rollover" if (prior or "") < today else
            "same-day-add" if prior == today else "ERROR")
    print("=== daily_run ===")
    print("today:", today, "| staging date:", prior, "| MODE:", mode,
          "| dry-run:", a.dry_run)
    if mode == "ERROR":
        print("REFUSE: staging date", prior, "is AFTER today", today, "- not touching anything.")
        return 2

    data, out, err = run_parser(a.paste)
    bets = data["bets"]
    print("parsed:", len(bets), "bets,", sum(len(b["legs"]) for b in bets), "legs, $%.2f" %
          sum((b["wager"] or 0) for b in bets))

    holds, notes = gate(bets, out)
    for n in notes: print("  note:", n)
    if holds:
        print("GATE: HOLD - nothing written. Offending bets:")
        for bid, why in holds: print("   ", bid, "->", why)
        return 1
    print("GATE: PASS (all bets clean)")

    # build the new staging
    if mode == "rollover":
        # HARD GATE (2026-07-18, Backlog #22): a rollover WRITE requires --auto-rollover.
        # Without it, the old code skipped the archive but still overwrote staging -
        # the exact missed-archive data-loss path the runbook warns about.
        if not a.dry_run and not a.auto_rollover:
            print("REFUSE: rollover write requires --auto-rollover (or --dry-run to preview).")
            print("NOT touching staging.json - prior day", prior, "is not archived yet.")
            return 1
        existing_ids = set()
        new_bets = bets
        # archive guard - per FILE (an OR-guard let one existing file suppress the other copy)
        ah = os.path.join(R, "archive", prior + ".html")
        aj = os.path.join(R, "archive", prior + ".json")
        for src, dst in ((os.path.join(R, "index.html"), ah), (a.staging, aj)):
            if os.path.exists(dst):
                print("archive exists - skip:", os.path.basename(dst))
            elif a.dry_run:
                print("WOULD archive", os.path.basename(src), "->", os.path.basename(dst))
            else:
                shutil.copy(src, dst)
                print("archived", os.path.basename(src), "->", os.path.basename(dst))
        new_staging = {"date": today, "bets": new_bets}
    else:  # same-day-add
        cur = staging["bets"]
        have = {b["full_id"] for b in cur}
        added, dup = [], []
        for b in bets:
            fid = b["full_id"]
            if fid in have:
                dup.append(b["id"])          # already in staging OR already seen in this paste
            else:
                have.add(fid)                # dedup WITHIN the incoming paste too (doubled screens)
                added.append(b)
        new_staging = {"date": today, "bets": cur + added}
        print("same-day add: +%d new, %d dup-skipped %s" % (len(added), len(dup), dup or ""))

    print("RESULT staging: date", new_staging["date"], "bets", len(new_staging["bets"]))
    if a.dry_run:
        print("DRY-RUN: not writing staging.json or building.")
        print("(verify-build on the prospective staging below)")
        tmps = os.path.join(R, "_dr_staging_preview.json")
        json.dump(new_staging, open(tmps, "w", encoding="utf-8"), indent=2)
        print(" ", verify_build(tmps))
        os.remove(tmps)
        return 0

    # BELT-AND-SUSPENDERS (Backlog #22): never overwrite an un-archived prior day.
    if mode == "rollover":
        assert os.path.exists(ah) and os.path.exists(aj), \
            "archive files for %s missing - refusing to overwrite staging" % prior
    # write staging (utf-8, no BOM) and verify byte0
    with open(a.staging, "w", encoding="utf-8") as f:
        json.dump(new_staging, f, indent=2)
    assert open(a.staging, "rb").read(1) == b"{", "staging byte0 not '{'"
    print(" ", verify_build(a.staging))
    print("WROTE", a.staging)
    print("--- NEXT: commit ONLY staging.json (Action builds+commits index.html) ---")
    if mode == "rollover":
        print('  git add archive/%s.html archive/%s.json ; git commit -m "archive %s board + data"' % (prior, prior, prior))
    print('  git add staging.json ; git commit -m "intake %s: %d bets" ; git pull --no-edit ; git push' %
          (today, len(new_staging["bets"])))
    return 0

if __name__ == "__main__":
    sys.exit(main())
