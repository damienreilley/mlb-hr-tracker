"""Cache backtest rows once, then sweep regression constants for calibration.

Fetching 70+ boxscores per iteration is wasteful, so pull once to disk and tune
against the cached set. Tuning K on the same sample carries mild overfit risk -
one parameter against 1200 observations, which I judge acceptable, and the
resulting calibration is reported honestly rather than assumed.
"""
import json, os, time
import hr_model as M
from hr_backtest import boxscore_rows, DATES

CACHE = "_bt_rows.json"


def collect():
    if os.path.exists(CACHE):
        return json.load(open(CACHE))
    rows = []
    for d in DATES:
        sch = M.gj("https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=%s" % d)
        pks = [g["gamePk"] for dt in (sch or {}).get("dates", []) for g in dt.get("games", [])
               if g["status"]["detailedState"] == "Final"]
        for pk in pks:
            rows += boxscore_rows(pk)
            time.sleep(0.05)
    json.dump(rows, open(CACHE, "w"))
    return rows


def score(rows, bat, pit, ind, lg_hand, lg, kbat, kpit, shrink=1.0):
    out = []
    for r in rows:
        b = bat.get(r["name"]); spd = pit.get(r["sp"])
        if not b or not spd or not r["slot"]:
            continue
        oh = spd["throws"]; key = (r["name"], oh)
        if key in ind:
            ihr, ipa = ind[key]
            base = (ihr + lg_hand[oh] * kbat) / (ipa + kbat)
        else:
            base = (b["hr"] + lg * kbat) / (b["pa"] + kbat)
            base *= lg_hand[oh] / lg
        sp_rate = (spd["hr"] + lg * kpit) / (spd["bf"] + kpit)
        pa_tot = M.SLOT_PA.get(r["slot"], 4.0)
        pa_sp = min(M.PA_VS_SP, pa_tot); pa_pen = pa_tot - pa_sp
        r_sp = min(base * sp_rate / lg * shrink, 0.30)
        r_pen = min(base * shrink, 0.30)
        p = 1 - ((1 - r_sp) ** pa_sp) * ((1 - r_pen) ** pa_pen)
        out.append((p, r["hr"]))
    return out


def metrics(preds):
    n = len(preds)
    pm = sum(p for p, _ in preds) / n
    am = sum(h for _, h in preds) / n
    brier = sum((p - h) ** 2 for p, h in preds) / n
    s = sorted(preds); k = max(1, n // 10)
    top = sum(h for _, h in s[-k:]) / k
    bot = sum(h for _, h in s[:k]) / k
    return pm, am, brier, top, bot


def main():
    rows = collect()
    bat, pit, pen = M.load_rosters()
    ind, lg_hand = M.platoon_splits()
    q = sum(lg_hand.values()) / 2.0
    lg_hand = {k: v * (M.LG_HR_PA / q) for k, v in lg_hand.items()}
    lg = M.LG_HR_PA
    print("cached rows: %d" % len(rows))
    print("%-7s %-7s %-8s %-8s %-8s %-8s %s" % ("K_BAT", "K_PIT", "PRED", "ACTUAL", "BIAS", "BRIER", "TOP/BOT"))
    best = None
    for kbat in (60, 90, 120, 170, 250):
        for kpit in (300, 450, 700):
            pr = score(rows, bat, pit, ind, lg_hand, lg, kbat, kpit)
            pm, am, br, top, bot = metrics(pr)
            bias = pm / am
            print("%-7d %-7d %7.2f%% %7.2f%% %7.2fx %8.5f %.1fx" %
                  (kbat, kpit, pm * 100, am * 100, bias, br, top / max(bot, 1e-9)))
            if best is None or abs(bias - 1) < best[0]:
                best = (abs(bias - 1), kbat, kpit, bias)
    print()
    print("closest to unbiased: K_BAT=%d K_PIT=%d (bias %.2fx)" % (best[1], best[2], best[3]))
    sh = 1.0 / best[3]
    pr = score(rows, bat, pit, ind, lg_hand, lg, best[1], best[2], shrink=sh)
    pm, am, br, top, bot = metrics(pr)
    print("with rate shrink %.3f -> pred %.2f%% vs actual %.2f%%  brier %.5f  top/bot %.1fx"
          % (sh, pm * 100, am * 100, br, top / max(bot, 1e-9)))
    print()
    print("%-16s %6s %10s %10s" % ("BUCKET", "N", "PRED", "ACTUAL"))
    for lo, hi in [(0, .06), (.06, .09), (.09, .12), (.12, .15), (.15, .19), (.19, 1)]:
        g = [(p, h) for p, h in pr if lo <= p < hi]
        if g:
            print("%-16s %6d %9.1f%% %9.1f%%" % ("%.0f-%.0f%%" % (lo * 100, hi * 100), len(g),
                  100 * sum(p for p, _ in g) / len(g), 100 * sum(h for _, h in g) / len(g)))
    json.dump({"K_BAT": best[1], "K_PIT": best[2], "SHRINK": sh}, open("_hr_tuned.json", "w"))


if __name__ == "__main__":
    main()
