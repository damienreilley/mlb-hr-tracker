"""Point-in-time stat cache - removes look-ahead leakage from the backtest.

The v1 backtest scored past games using FULL-SEASON rates, which include the very
games being predicted. That inflates discrimination and makes the validation
partly circular. This module caches every relevant hitter's and pitcher's game
log, so stats can be rebuilt as of the morning of any test date - genuinely
out-of-sample.
"""
import json, os, time
import hr_model as M

HIT_CACHE = "_pit_hitters.json"
PIT_CACHE = "_pit_pitchers.json"


def player_id_map():
    ids = {}
    for abbr, tid in M.TEAM_ID.items():
        for grp in ("hitting", "pitching"):
            d = M.gj("https://statsapi.mlb.com/api/v1/teams/%d/roster?rosterType=active&hydrate=person(stats(group=[%s],type=[season],season=%d))" % (tid, grp, M.SEASON))
            for row in (d or {}).get("roster", []):
                p = row.get("person", {})
                if p.get("id"):
                    ids[p["fullName"]] = p["id"]
            time.sleep(0.12)
    return ids


def build(names, ids, group, cache):
    """Cache per-date game logs: name -> [(date, hr, pa) ...] for hitters,
    or name -> [(date, hr_allowed, bf)] for pitchers."""
    have = json.load(open(cache)) if os.path.exists(cache) else {}
    todo = [n for n in names if n in ids and n not in have]
    print("  %s: %d cached, %d to fetch" % (group, len(have), len(todo)))
    for i, n in enumerate(todo):
        d = M.gj("https://statsapi.mlb.com/api/v1/people/%d/stats?stats=gameLog&season=%d&group=%s" % (ids[n], M.SEASON, group))
        rows = []
        for s in (d or {}).get("stats", []):
            for sp in s.get("splits", []):
                st = sp.get("stat", {})
                if group == "hitting":
                    pa = st.get("plateAppearances") or 0
                    if pa:
                        rows.append([sp.get("date"), st.get("homeRuns") or 0, pa])
                else:
                    bf = st.get("battersFaced") or 0
                    if bf:
                        rows.append([sp.get("date"), st.get("homeRuns") or 0, bf])
        have[n] = rows
        if i % 40 == 0:
            json.dump(have, open(cache, "w"))
            print("     ...%d/%d" % (i, len(todo)))
        time.sleep(0.12)
    json.dump(have, open(cache, "w"))
    return have


def as_of(cache, name, date):
    """Cumulative totals STRICTLY BEFORE `date`. Returns (hr, denom)."""
    hr = den = 0
    for d, h, n in cache.get(name, []):
        if d < date:
            hr += h; den += n
    return hr, den


if __name__ == "__main__":
    rows = json.load(open("_bt_rows2.json"))
    hitters = sorted({r["name"] for r in rows if r.get("name")})
    pitchers = sorted({r["sp"] for r in rows if r.get("sp")})
    print("building point-in-time caches for %d hitters / %d pitchers" % (len(hitters), len(pitchers)))
    ids = player_id_map()
    print("id map: %d players" % len(ids))
    build(hitters, ids, "hitting", HIT_CACHE)
    build(pitchers, ids, "pitching", PIT_CACHE)
    json.dump(ids, open("_pit_ids.json", "w"))
    print("done")
