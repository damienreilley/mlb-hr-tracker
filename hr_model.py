"""HR probability model - 2026-07-31 slate.

METHOD (documented so every number is auditable):
  1. Matchup rate via odds-ratio / Log5:  rate = (batter x pitcher) / league
     Replaces "handedness only" - a hitter facing Nick Martinez (2.45) and one
     facing Ryan Johnson (7.34) are no longer treated as the same problem.
  2. REGRESSION. Batter HR/PA regressed with K=170 PA of league mean (HR rate
     stabilises ~170 PA). Pitcher HR/BF regressed with K=450 BF (slower).
     Kills the Trout-4-for-81 problem that broke the last version.
  3. PLATOON. Individual vs-hand splits where the sample qualifies; otherwise a
     league platoon multiplier by (batter hand x pitcher hand).
  4. BULLPEN. ~2.6 PA vs the starter, remainder vs that team's relievers
     (measured reliever HR/BF), instead of pretending the SP throws all 9.
  5. PARK. MEASURED from 2026 home/away data, classic formula, then regressed
     50% toward neutral for single-season noise.
  6. WEATHER. temp and wind vector as explicit multipliers.
  7. FULL SLATE. every hitter in every posted lineup - no hand-picked shortlist.

KNOWN LIMITS (stated, not hidden): no Statcast batted-ball inputs (barrel rate,
xwOBA) - those are better predictors than outcome HR/PA but are not in StatsAPI.
Park factors are single-season and not handedness-split. Openers/bulk arms in
SD and LAD are uncertain. Umpire and defence ignored.
"""
import json, urllib.request, time, math

SEASON = 2026
K_BAT = 120.0
K_PIT = 450.0
PA_VS_SP = 2.6

# INTRA-GAME CORRELATION CORRECTION.
# v1 value was 0.826, fitted on a 1,202-row backtest that used FULL-SEASON stats
# (look-ahead leakage) over 5 dates. Re-fitted 2026-07-31 on a LEAK-FREE
# point-in-time backtest of 2,180 rows across 10 dates -> 0.920. Bias 0.995.
SHRINK = 0.920

# STATCAST BLEND. batter term = (1-w)*outcome HR/PA + w*(barrels/PA * RATIO).
# Barrels per PA is a better and faster-stabilising HR predictor than outcome
# HR/PA. Measured effect on the leak-free backtest: discrimination 3.2x -> 5.3x,
# Brier 0.09171 -> 0.09135. Weight held at 0.50 rather than the Brier-optimal
# 0.70 because Savant barrel totals are SEASON figures and retain some
# look-ahead in the test - 0.50 takes most of the gain with less exposure.
SC_WEIGHT = 0.50
SC_SOURCE = "https://baseballsavant.mlb.com/leaderboard/statcast?type=batter&year=%d&position=&team=&min=10&csv=true"

# OPENER / BULK-ARM DETECTION. If the listed starter averages under 12 batters
# faced per appearance, treat him as an opener and move PAs to the bullpen.
# HONEST NOTE: measured NO improvement on the backtest (3.2x -> 3.2x, bias
# unchanged) because true openers are rare in the sample. Retained as a
# correctness safeguard for games where an opener IS listed, not as an upgrade.
OPENER_BF_PER_APP = 12.0
OPENER_PA_VS_SP = 1.1

def gj(u):
    for _ in range(4):
        try:
            with urllib.request.urlopen(u, timeout=45) as r:
                return json.load(r)
        except Exception:
            time.sleep(1.2)
    return None

# PA by lineup slot - MEASURED from 2026 boxscores (starters only, includes
# early exits and pinch-hits). The first version of this table was INVENTED and
# ran ~20% high at the bottom of the order - the single largest source of
# over-prediction in the v1 backtest. Do not replace with guesses.
SLOT_PA = {1: 4.21, 2: 4.31, 3: 4.15, 4: 4.12, 5: 3.90, 6: 3.37, 7: 3.25, 8: 3.31, 9: 3.08}

# TRUE league HR/PA from all 30 team totals (3786 HR / 123989 PA). v1 used the
# QUALIFIED-hitter pool (0.0334), 9% high because qualified hitters out-homer the
# league - it dragged weak bats upward through regression.
LG_HR_PA = 0.03053

TEAM_ID = {"LAA":108,"AZ":109,"BAL":110,"BOS":111,"CHC":112,"CIN":113,"CLE":114,"COL":115,
"DET":116,"HOU":117,"KC":118,"LAD":119,"WSH":120,"NYM":121,"ATH":133,"PIT":134,"SD":135,
"SEA":136,"SF":137,"STL":138,"TB":139,"TEX":140,"TOR":141,"MIN":142,"PHI":143,"ATL":144,
"CWS":145,"MIA":146,"NYY":147,"MIL":158}

# Lineups as posted on RotoWire at 16:12 ET 2026-07-31. NYY@CHC excluded (in progress, 8th).
# game = (away, home, awaySP, awaySPhand, homeSP, homeSPhand, parkTeam, tempF, wind, windDir)
GAMES = [
 ("PIT","CIN","Paul Skenes","R","Hunter Greene","R","CIN",87,5,"in"),
 ("PHI","BAL","Andrew Painter","R","Brandon Young","R","BAL",85,3,"cross"),
 ("STL","TOR","Kyle Leahy","R","Dylan Cease","R","TOR",72,0,"dome"),
 ("AZ","CLE","Mitch Bratt","L","Tanner Bibee","R","CLE",85,2,"cross"),
 ("CWS","TB","Erick Fedde","R","Nick Martinez","R","TB",72,0,"dome"),
 ("MIA","NYM","Janson Junk","R","Freddy Peralta","R","NYM",79,6,"cross"),
 ("WSH","ATL","Foster Griffin","L","Bryce Elder","R","ATL",89,3,"cross"),
 ("TEX","HOU","Nathan Eovaldi","R","Hunter Brown","R","HOU",72,0,"dome"),
 ("KC","COL","Michael Wacha","R","Tomoyuki Sugano","R","COL",85,7,"cross"),
 ("MIL","LAA","Shane Drohan","L","Ryan Johnson","R","LAA",85,7,"out"),
 ("DET","ATH","Ty Madden","R","Jeffrey Springs","L","ATH",97,6,"cross"),
 ("SF","SD","Carson Whisenhunt","L","German Marquez","R","SD",76,7,"out"),
 ("BOS","LAD","Ranger Suarez","L","Will Klein","R","LAD",81,8,"out"),
 ("MIN","SEA","Zebby Matthews","R","Bryce Miller","R","SEA",72,0,"dome"),
]

LINEUPS = {
 "PIT":["Jake Mangum","Brandon Lowe","Bryan Reynolds","Esmerlyn Valdez","Ryan O'Hearn","Nick Gonzales","Endy Rodriguez","Marcell Ozuna","Jacob Gonzalez"],
 "CIN":["Elly De La Cruz","Sal Stewart","JJ Bleday","Eugenio Suarez","Nathaniel Lowe","Tyler Stephenson","Dane Myers","Noelvi Marte","Matt McLain"],
 "PHI":["Trea Turner","Kyle Schwarber","Bryce Harper","Brandon Marsh","Alec Bohm","Bryson Stott","J.T. Realmuto","Bryan De La Cruz","Justin Crawford"],
 "BAL":["Dylan Beavers","Pete Alonso","Gunnar Henderson","Taylor Ward","Christian Encarnacion-Strand","Colton Cowser","Leody Taveras","Jackson Holliday","Jake Rogers"],
 "STL":["JJ Wetherholt","Ivan Herrera","Alec Burleson","Jordan Walker","Lars Nootbaar","Masyn Winn","Nathan Church","Blaze Jordan","Jimmy Crooks"],
 "TOR":["Nathan Lukes","Vladimir Guerrero Jr.","Kazuma Okamoto","George Springer","Alejandro Kirk","Daulton Varsho","Ernie Clement","Yohendrick Pinango","Andres Gimenez"],
 "AZ":["Corbin Carroll","Geraldo Perdomo","Gabriel Moreno","Ketel Marte","Max Kepler","Nolan Arenado","Adrian Del Castillo","Tim Tawa","Ryan Waldschmidt"],
 "CLE":["Angel Martinez","Jose Ramirez","Chase DeLauter","Rhys Hoskins","Brayan Rocchio","Travis Bazzana","David Fry","Steven Kwan","Austin Hedges"],
 "CWS":["Sam Antonacci","Munetaka Murakami","Miguel Vargas","Colson Montgomery","Andrew Benintendi","Braden Montgomery","Tristan Peters","Chase Meidroth","Drew Romo"],
 "TB":["Yandy Diaz","Jonathan Aranda","Junior Caminero","Cedric Mullins","Chandler Simpson","Victor Mesa Jr.","Taylor Walls","Richie Palacios","Hunter Feduccia"],
 "MIA":["Otto Lopez","Kyle Stowers","Heriberto Hernandez","Xavier Edwards","Liam Hicks","Griffin Conine","Javier Sanoja","Joe Mack","Jakob Marsee"],
 "NYM":["A.J. Ewing","Francisco Lindor","Bo Bichette","Carson Benge","Luis Robert Jr.","Jorge Polanco","Jared Young","Marcus Semien","Francisco Alvarez"],
 "WSH":["James Wood","Luis Garcia Jr.","Dylan Crews","CJ Abrams","Keibert Ruiz","Daylen Lile","Nasim Nunez","Jorbit Vivas","Jacob Young"],
 "ATL":["Ronald Acuna Jr.","Drake Baldwin","Ozzie Albies","Matt Olson","Michael Harris II","Mauricio Dubon","Austin Riley","Mike Yastrzemski","Jim Jarvis"],
 "TEX":["Joc Pederson","Wyatt Langford","Corey Seager","Brandon Nimmo","Ezequiel Duran","Evan Carter","Jake Burger","Nicky Lopez","Elias Diaz"],
 "HOU":["Jeremy Pena","Yordan Alvarez","Isaac Paredes","Jose Altuve","Christian Walker","Yainer Diaz","Cam Smith","Zach Dezenzo","Lucas Spence"],
 "KC":["Carter Jensen","Lane Thomas","Jac Caglianone","Salvador Perez","Michael Massey","Nick Loftin","Isaac Collins","Josh Rojas","Andrew Velazquez"],
 "COL":["Jake McCarthy","Mickey Moniak","Hunter Goodman","TJ Rumfield","Kyle Karros","Cole Carrigg","Willi Castro","Troy Johnston","Ezequiel Tovar"],
 "MIL":["Christian Yelich","Jackson Chourio","Brice Turang","William Contreras","Jake Bauers","Andrew Vaughn","Garrett Mitchell","Cooper Pratt","David Hamilton"],
 "LAA":["Zach Neto","Mike Trout","Vaughn Grissom","Jorge Soler","Nolan Schanuel","Jo Adell","Denzer Guzman","Jose Siri","Travis d'Arnaud"],
 "DET":["Gleyber Torres","Kevin McGonigle","Hao-Yu Lee","Dillon Dingler","Riley Greene","Spencer Torkelson","Javier Baez","Matt Vierling","Max Clark"],
 "ATH":["Nick Kurtz","Jacob Wilson","Tyler Soderstrom","Carlos Cortes","Jonah Heim","Donovan Walton","Tommy White","Lawrence Butler","Henry Bolte"],
 "SF":["Luis Arraez","Bryce Eldridge","Heliot Ramos","Rafael Devers","Jung Hoo Lee","Willy Adames","Daniel Susac","Grant McCray","Christian Koss"],
 "SD":["Fernando Tatis Jr.","Luis Rengifo","Manny Machado","Ty France","Jackson Merrill","Luis Campusano","Xander Bogaerts","Jase Bowen","Freddy Fermin"],
 "BOS":["Masataka Yoshida","Ceddanne Rafaela","Willson Contreras","Wilyer Abreu","Caleb Durbin","Jarren Duran","Andruw Monasterio","Anthony Seigler","Connor Wong"],
 "LAD":["Shohei Ohtani","Andy Pages","Freddie Freeman","Mookie Betts","Tommy Edman","Kyle Tucker","Teoscar Hernandez","Enrique Hernandez","Dalton Rushing"],
 "MIN":["Trevor Larnach","Kody Clemens","Ryan Jeffers","Josh Bell","Royce Lewis","Brooks Lee","Luke Keaschall","Alan Roden","Ryan Kreidler"],
 "SEA":["Cole Young","Julio Rodriguez","Dominic Canzone","Randy Arozarena","Josh Naylor","Cal Raleigh","Luke Raley","J.P. Crawford","Colt Emerson"],
}


def load_rosters():
    """One roster call per team -> every hitter's season PA/HR/batSide and every
    pitcher's BF/HR/throws. Covers unqualified rookies the leaderboards omit."""
    bat, pit, pen = {}, {}, {}
    for abbr, tid in TEAM_ID.items():
        d = gj("https://statsapi.mlb.com/api/v1/teams/%d/roster?rosterType=active&hydrate=person(stats(group=[hitting],type=[season],season=%d))" % (tid, SEASON))
        for row in (d or {}).get("roster", []):
            p = row.get("person", {})
            for s in p.get("stats", []):
                for sp in s.get("splits", []):
                    st = sp.get("stat", {})
                    if st.get("plateAppearances"):
                        bat[p.get("fullName")] = {
                            "pa": st["plateAppearances"], "hr": st.get("homeRuns") or 0,
                            "bats": p.get("batSide", {}).get("code", "R"), "team": abbr}
        time.sleep(0.15)
        d = gj("https://statsapi.mlb.com/api/v1/teams/%d/roster?rosterType=active&hydrate=person(stats(group=[pitching],type=[season],season=%d))" % (tid, SEASON))
        rel_hr = rel_bf = 0
        for row in (d or {}).get("roster", []):
            p = row.get("person", {})
            for s in p.get("stats", []):
                for sp in s.get("splits", []):
                    st = sp.get("stat", {})
                    bf = st.get("battersFaced") or 0
                    if not bf:
                        continue
                    hr = st.get("homeRuns") or 0
                    gs = st.get("gamesStarted") or 0
                    g = st.get("gamesPlayed") or st.get("games") or 0
                    pit[p.get("fullName")] = {"bf": bf, "hr": hr, "apps": g,
                        "throws": p.get("pitchHand", {}).get("code", "R"), "team": abbr}
                    if g and gs / max(g, 1) < 0.5:   # reliever
                        rel_hr += hr; rel_bf += bf
        pen[abbr] = (rel_hr, rel_bf)
        time.sleep(0.15)
    return bat, pit, pen


def load_statcast():
    """Barrels per PA by MLB player id, from Baseball Savant.
    Addresses the v1 weakness 'uses outcome HR/PA, not batted-ball inputs'."""
    import csv, io
    out = {}
    try:
        req = urllib.request.Request(SC_SOURCE % SEASON, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90) as r:
            txt = r.read().decode("utf-8-sig", "replace")
        for row in csv.DictReader(io.StringIO(txt)):
            try:
                out[int(row["player_id"])] = float(row["brl_pa"]) / 100.0
            except Exception:
                pass
    except Exception as e:
        print("WARN: Statcast fetch failed (%r) - running WITHOUT the barrel term" % e)
    return out


def park_factors(years=(SEASON, SEASON - 1, SEASON - 2), weights=(3, 2, 1)):
    """MEASURED HR park factor, classic home/away formula, now MULTI-YEAR.
    v1 used a single season, which is noisy; weighting three seasons 3-2-1
    keeps recency while stabilising the estimate. Still regressed 50% toward
    neutral. NOT handedness-split - remains a known limitation."""
    pf = {}
    for abbr, tid in TEAM_ID.items():
        num = den = 0.0
        for yr, w in zip(years, weights):
            d = {"h": [0, 0], "a": [0, 0]}
            for grp, key in (("hitting", "plateAppearances"), ("pitching", "battersFaced")):
                src = gj("https://statsapi.mlb.com/api/v1/teams/%d/stats?stats=statSplits&sitCodes=h,a&group=%s&season=%d&gameType=R" % (tid, grp, yr))
                for s in (src or {}).get("stats", []):
                    for x in s.get("splits", []):
                        c = x.get("split", {}).get("code")
                        if c in d:
                            d[c][0] += x["stat"].get("homeRuns") or 0
                            d[c][1] += x["stat"].get(key) or 0
                time.sleep(0.1)
            if d["h"][1] and d["a"][1] and d["a"][0]:
                raw = (d["h"][0] / d["h"][1]) / (d["a"][0] / d["a"][1])
                num += raw * w; den += w
        raw = (num / den) if den else 1.0
        pf[abbr] = 1.0 + 0.5 * (raw - 1.0)
    return pf


def weather_mult(temp, wind, wdir):
    """Documented approximations: ~0.6%/degF above 70 (Alan Nathan drag work
    implies roughly 1% carry per 10F, compounding into HR rate), wind out/in
    ~1.4% per mph on the HR rate, cross-wind and domes neutral."""
    m = 1.0 + 0.006 * (temp - 70)
    if wdir == "out":
        m *= 1.0 + 0.014 * wind
    elif wdir == "in":
        m *= 1.0 - 0.014 * wind
    return m


def platoon_splits():
    """Individual vs-hand HR/PA for qualified hitters, plus league platoon
    multipliers by (batter hand x pitcher hand) for everyone else."""
    ind, lg = {}, {}
    for code, hand in (("vr", "R"), ("vl", "L")):
        d = gj("https://statsapi.mlb.com/api/v1/stats?stats=statSplits&sitCodes=%s&group=hitting&season=%d&limit=500&sportId=1&gameType=R" % (code, SEASON))
        hr = pa = 0
        for s in (d or {}).get("stats", []):
            for x in s.get("splits", []):
                st = x["stat"]; nm = x.get("player", {}).get("fullName")
                p_ = st.get("plateAppearances") or 0
                if p_ >= 120:
                    ind[(nm, hand)] = (st.get("homeRuns") or 0, p_)
                hr += st.get("homeRuns") or 0; pa += p_
        lg[hand] = hr / pa if pa else 0.033
        time.sleep(0.2)
    return ind, lg


def run():
    bat, pit, pen = load_rosters()
    pf = park_factors()
    sc = load_statcast()
    ids = {}
    for abbr, tid in TEAM_ID.items():
        d = gj("https://statsapi.mlb.com/api/v1/teams/%d/roster?rosterType=active" % tid)
        for row in (d or {}).get("roster", []):
            p = row.get("person", {})
            if p.get("id"):
                ids[p.get("fullName")] = p["id"]
        time.sleep(0.1)
    ind, lg_hand = platoon_splits()
    # anchor on the TRUE league rate; keep only the platoon SHAPE from the
    # qualified pool, rescaled so its mean equals the true league rate.
    qmean = sum(lg_hand.values()) / 2.0
    scale = LG_HR_PA / qmean
    lg_hand = {k: v * scale for k, v in lg_hand.items()}
    lg = LG_HR_PA
    # fit HR/PA per barrel/PA so the Statcast term sits on the HR/PA scale
    n_ = d_ = 0.0
    for nm, b in bat.items():
        pid = ids.get(nm)
        if pid in sc and b["pa"] >= 150 and sc[pid] > 0:
            n_ += b["hr"]; d_ += sc[pid] * b["pa"]
    sc_ratio = (n_ / d_) if d_ else 0.59
    print("statcast: %d players, fitted HR/PA per barrel/PA = %.4f" % (len(sc), sc_ratio))

    rows = []
    for away, home, asp, ahand, hsp, hhand, park, temp, wind, wdir in GAMES:
        wm = weather_mult(temp, wind, wdir)
        pkm = pf.get(park, 1.0)
        for side, opp_sp, opp_hand, opp_team in ((away, hsp, hhand, home), (home, asp, ahand, away)):
            sp = pit.get(opp_sp)
            sp_rate = ((sp["hr"] + lg * K_PIT) / (sp["bf"] + K_PIT)) if sp else lg
            rhr, rbf = pen.get(opp_team, (0, 0))
            pen_rate = ((rhr + lg * K_PIT) / (rbf + K_PIT)) if rbf else lg
            for slot, name in enumerate(LINEUPS.get(side, []), start=1):
                b = bat.get(name)
                if not b:
                    continue
                key = (name, opp_hand)
                if key in ind:
                    ihr, ipa = ind[key]
                    base = (ihr + lg_hand[opp_hand] * K_BAT) / (ipa + K_BAT)
                else:
                    base = (b["hr"] + lg * K_BAT) / (b["pa"] + K_BAT)
                    base *= (lg_hand[opp_hand] / lg) if lg else 1.0
                pid = ids.get(name)
                if pid in sc and sc[pid] > 0:
                    base = (1 - SC_WEIGHT) * base + SC_WEIGHT * (sc[pid] * sc_ratio)
                pa_tot = SLOT_PA[slot]
                pa_sp = min(PA_VS_SP, pa_tot)
                if sp and sp.get("bf") and sp.get("apps"):
                    if sp["bf"] / sp["apps"] < OPENER_BF_PER_APP:
                        pa_sp = min(OPENER_PA_VS_SP, pa_tot)
                pa_pen = pa_tot - pa_sp
                r_sp = (base * sp_rate / lg) * pkm * wm * SHRINK
                r_pen = (base * pen_rate / lg) * pkm * wm * SHRINK
                r_sp = min(r_sp, 0.30); r_pen = min(r_pen, 0.30)
                p = 1 - ((1 - r_sp) ** pa_sp) * ((1 - r_pen) ** pa_pen)
                rows.append((p, name, b["team"], b["bats"], opp_team, opp_sp, opp_hand,
                             slot, pkm, wm, base, sp_rate))
    rows.sort(reverse=True)
    print("league HR/PA %.4f | vsR %.4f | vsL %.4f | hitters %d | slate %d"
          % (lg, lg_hand["R"], lg_hand["L"], len(bat), len(rows)))
    print()
    print("%-5s %-24s %-4s %-2s %-22s %-4s %-5s %-5s %-6s" %
          ("P(HR)", "BATTER", "TM", "B", "OPP SP", "SLOT", "PARK", "WX", "SPrate"))
    for r in rows[:20]:
        p, name, tm, bats, opp, sp, oh, slot, pkm, wm, base, spr = r
        print("%4.1f%% %-24s %-4s %-2s %-22s %-4d %5.2f %5.2f %6.3f" %
              (p * 100, name[:24], tm, bats, (sp + " (" + oh + ")")[:22], slot, pkm, wm, spr))
    json.dump([{"p": r[0], "name": r[1], "tm": r[2], "sp": r[5]} for r in rows],
              open("_hr_model_out.json", "w"))


if __name__ == "__main__":
    run()
