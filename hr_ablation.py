"""Feature ablation - measures what each proposed upgrade is actually worth.

All variants score the SAME 2,466 observations using POINT-IN-TIME stats
(cumulative strictly before each game date), so this is genuinely out-of-sample
for the outcome-based terms and the comparison between variants is fair.

Variants:
  base      point-in-time outcome HR/PA only  (the leak-free baseline)
  +sc(w)    blends Statcast barrels-per-PA into the batter term at weight w
  +opener   detects openers/bulk arms (low batters-faced per appearance) and
            shifts plate appearances from "starter" to "bullpen"

RESIDUAL LEAKAGE, stated plainly: the Statcast barrel figures are season totals
(Savant does not expose a cheap point-in-time endpoint), so the +sc variants
retain some look-ahead. Their improvement should be read as an upper bound.
"""
import json
import hr_model as M
import hr_pit_cache as P

ROWS = json.load(open("_bt_rows2.json"))
HIT = json.load(open(P.HIT_CACHE))
PIT = json.load(open(P.PIT_CACHE))
IDS = json.load(open("_pit_ids.json"))
ID2NAME = {v: k for k, v in IDS.items()}

SC = {}
for row in json.load(open("_sc_statcast.json")):
    try:
        SC[int(row["player_id"])] = float(row["brl_pa"]) / 100.0
    except Exception:
        pass


def fit_ratio():
    """League-fitted HR/PA per unit of barrels/PA, so the Statcast term lands on
    the HR/PA scale rather than an arbitrary one."""
    hr = pa = brl_w = 0.0
    for pid, brl in SC.items():
        nm = ID2NAME.get(pid)
        if not nm or nm not in HIT:
            continue
        h = sum(x[1] for x in HIT[nm]); p = sum(x[2] for x in HIT[nm])
        if p >= 150:
            hr += h; pa += p; brl_w += brl * p
    return (hr / brl_w) if brl_w else 1.0


RATIO = fit_ratio()


def as_of(cache, name, date, k, lg):
    hr, den = P.as_of(cache, name, date)
    return (hr + lg * k) / (den + k), den


def apps_before(name, date):
    return sum(1 for d, _, _ in PIT.get(name, []) if d < date)


def score(sc_w=0.0, opener=False):
    lg = M.LG_HR_PA
    out = []
    for r in ROWS:
        nm, sp, slot, date = r.get("name"), r.get("sp"), r.get("slot"), r.get("date")
        if not (nm and sp and slot and date):
            continue
        b_rate, b_pa = as_of(HIT, nm, date, M.K_BAT, lg)
        p_rate, p_bf = as_of(PIT, sp, date, M.K_PIT, lg)
        if b_pa < 20 or p_bf < 20:
            continue
        pid = IDS.get(nm)
        if sc_w and pid in SC:
            b_rate = (1 - sc_w) * b_rate + sc_w * (SC[pid] * RATIO)
        pa_tot = M.SLOT_PA.get(slot, 4.0)
        pa_sp = min(M.PA_VS_SP, pa_tot)
        if opener:
            a = apps_before(sp, date)
            if a and (p_bf / a) < 12:
                pa_sp = min(1.1, pa_tot)
        pa_pen = pa_tot - pa_sp
        r_sp = min(b_rate * p_rate / lg * M.SHRINK, 0.30)
        r_pen = min(b_rate * M.SHRINK, 0.30)
        out.append((1 - ((1 - r_sp) ** pa_sp) * ((1 - r_pen) ** pa_pen), r["hr"]))
    return out


def metrics(pr):
    n = len(pr)
    pm = sum(p for p, _ in pr) / n
    am = sum(h for _, h in pr) / n
    br = sum((p - h) ** 2 for p, h in pr) / n
    s = sorted(pr); k = max(1, n // 10)
    return n, pm, am, br, sum(h for _, h in s[-k:]) / k, sum(h for _, h in s[:k]) / k


if __name__ == "__main__":
    print("fitted HR/PA per barrel/PA: %.4f" % RATIO)
    print()
    print("%-22s %6s %8s %8s %8s %9s %8s" %
          ("VARIANT", "N", "PRED", "ACTUAL", "BIAS", "BRIER", "TOP/BOT"))
    for label, kw in [("base (leak-free)", {}),
                      ("+sc w=0.25", dict(sc_w=.25)),
                      ("+sc w=0.40", dict(sc_w=.40)),
                      ("+sc w=0.55", dict(sc_w=.55)),
                      ("+sc w=0.70", dict(sc_w=.70)),
                      ("+opener only", dict(opener=True)),
                      ("+sc 0.40 +opener", dict(sc_w=.40, opener=True))]:
        n, pm, am, br, top, bot = metrics(score(**kw))
        print("%-22s %6d %7.2f%% %7.2f%% %7.3fx %9.5f %7.1fx" %
              (label, n, pm * 100, am * 100, pm / am, br, top / max(bot, 1e-9)))
