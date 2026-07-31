"""Rebuild backtest rows WITH the game date attached (needed for point-in-time
stats). Also widens the window to 10 dates for a larger validation sample.
Writes _bt_rows2.json.
"""
import json, time
import hr_model as M

DATES = ["2026-07-19","2026-07-20","2026-07-21","2026-07-22","2026-07-23",
         "2026-07-24","2026-07-25","2026-07-26","2026-07-27","2026-07-28"]


def rows_for(pk, date):
    b = M.gj("https://statsapi.mlb.com/api/v1/game/%d/boxscore" % pk)
    if not b:
        return []
    out = []
    teams = b.get("teams", {})
    sp = {}
    for side in ("away", "home"):
        ps = teams.get(side, {}).get("pitchers", [])
        if ps:
            pl = teams[side]["players"].get("ID%d" % ps[0], {})
            sp[side] = pl.get("person", {}).get("fullName")
    for side, opp in (("away", "home"), ("home", "away")):
        t = teams.get(side, {})
        order = t.get("battingOrder", [])[:9]
        for i, pid in enumerate(order, start=1):
            pl = t["players"].get("ID%d" % pid, {})
            nm = pl.get("person", {}).get("fullName")
            hr = (pl.get("stats", {}).get("batting", {}) or {}).get("homeRuns", 0) or 0
            out.append({"name": nm, "hr": 1 if hr >= 1 else 0, "sp": sp.get(opp),
                        "slot": i, "date": date})
    return out


if __name__ == "__main__":
    allrows = []
    for d in DATES:
        sch = M.gj("https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=%s" % d)
        pks = [g["gamePk"] for dt in (sch or {}).get("dates", []) for g in dt.get("games", [])
               if g["status"]["detailedState"] == "Final"]
        n0 = len(allrows)
        for pk in pks:
            allrows += rows_for(pk, d)
            time.sleep(0.05)
        print("%s  games=%d rows=%d" % (d, len(pks), len(allrows) - n0))
    json.dump(allrows, open("_bt_rows2.json", "w"))
    print("TOTAL rows: %d over %d dates" % (len(allrows), len(DATES)))
