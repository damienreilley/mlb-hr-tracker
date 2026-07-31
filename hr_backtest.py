"""Calibration backtest for hr_model.

Reconstructs REAL lineups and REAL outcomes from boxscores on past dates, scores
each hitter with the model's structure, then asks the only question that matters:
when the model says 20%, does it happen 20% of the time?

HONEST LIMITATION: player rates come from full-season 2026 stats, which include
the backtest dates themselves. That is mild look-ahead leakage and will flatter
discrimination somewhat. It cannot, however, hide gross miscalibration - if the
model systematically over- or under-predicts, the buckets will show it.
"""
import json, time, urllib.request
import hr_model as M

DATES = ["2026-07-24", "2026-07-25", "2026-07-26", "2026-07-27", "2026-07-28"]


def boxscore_rows(pk):
    b = M.gj("https://statsapi.mlb.com/api/v1/game/%d/boxscore" % pk)
    if not b:
        return []
    out = []
    teams = b.get("teams", {})
    sp = {}
    for side in ("away", "home"):
        pitchers = teams.get(side, {}).get("pitchers", [])
        if pitchers:
            pid = pitchers[0]
            pl = teams[side]["players"].get("ID%d" % pid, {})
            sp[side] = pl.get("person", {}).get("fullName")
    for side, opp in (("away", "home"), ("home", "away")):
        t = teams.get(side, {})
        for pid in t.get("battingOrder", [])[:9]:
            pl = t["players"].get("ID%d" % pid, {})
            nm = pl.get("person", {}).get("fullName")
            hr = (pl.get("stats", {}).get("batting", {}) or {}).get("homeRuns", 0) or 0
            order = len(out) % 9 + 1
            out.append({"name": nm, "hr": 1 if hr >= 1 else 0,
                        "sp": sp.get(opp), "slot": order})
    return out


def main():
    bat, pit, pen = M.load_rosters()
    ind, lg_hand = M.platoon_splits()
    qmean = sum(lg_hand.values()) / 2.0
    lg_hand = {k: v * (M.LG_HR_PA / qmean) for k, v in lg_hand.items()}
    lg = M.LG_HR_PA
    preds = []
    for d in DATES:
        sch = M.gj("https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=%s" % d)
        pks = [g["gamePk"] for dt in (sch or {}).get("dates", []) for g in dt.get("games", [])
               if g["status"]["detailedState"] == "Final"]
        for pk in pks:
            for r in boxscore_rows(pk):
                b = bat.get(r["name"]); spd = pit.get(r["sp"])
                if not b or not spd or not r["slot"]:
                    continue
                oh = spd["throws"]
                key = (r["name"], oh)
                if key in ind:
                    ihr, ipa = ind[key]
                    base = (ihr + lg_hand[oh] * M.K_BAT) / (ipa + M.K_BAT)
                else:
                    base = (b["hr"] + lg * M.K_BAT) / (b["pa"] + M.K_BAT)
                    base *= lg_hand[oh] / lg
                sp_rate = (spd["hr"] + lg * M.K_PIT) / (spd["bf"] + M.K_PIT)
                pa_tot = M.SLOT_PA.get(r["slot"], 4.2)
                pa_sp = min(M.PA_VS_SP, pa_tot); pa_pen = pa_tot - pa_sp
                r_sp = min(base * sp_rate / lg, 0.30)
                r_pen = min(base, 0.30)
                p = 1 - ((1 - r_sp) ** pa_sp) * ((1 - r_pen) ** pa_pen)
                preds.append((p, r["hr"]))
            time.sleep(0.05)
    preds.sort()
    n = len(preds)
    print("backtest PA-games: %d over %d dates" % (n, len(DATES)))
    print("predicted mean %.4f | actual mean %.4f" %
          (sum(p for p, _ in preds) / n, sum(h for _, h in preds) / n))
    print()
    print("%-16s %6s %10s %10s" % ("BUCKET", "N", "PRED", "ACTUAL"))
    B = [(0, .08), (.08, .11), (.11, .14), (.14, .17), (.17, .21), (.21, 1)]
    for lo, hi in B:
        g = [(p, h) for p, h in preds if lo <= p < hi]
        if not g:
            continue
        print("%-16s %6d %9.1f%% %9.1f%%" % ("%.0f-%.0f%%" % (lo * 100, hi * 100), len(g),
              100 * sum(p for p, _ in g) / len(g), 100 * sum(h for _, h in g) / len(g)))
    k = max(1, n // 10)
    top = preds[-k:]; bot = preds[:k]
    print()
    print("top decile actual HR rate  %.1f%% (n=%d)" % (100 * sum(h for _, h in top) / k, k))
    print("bottom decile actual HR rate %.1f%% (n=%d)" % (100 * sum(h for _, h in bot) / k, k))
    print("discrimination ratio: %.2fx" %
          ((sum(h for _, h in top) / k) / max(sum(h for _, h in bot) / k, 1e-9)))


if __name__ == "__main__":
    main()
