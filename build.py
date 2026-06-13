# -*- coding: utf-8 -*-
# build.py - single-source tracker build.
# Reads a staging file {"date":"YYYY-MM-DD","bets":[...]} and emits index.html
# from tracker_template.html. Stdlib only -> CI-friendly, no build-time network.
# Usage: python build.py [staging.json] [out.html]   (defaults: staging.json -> index.html)
import json, re, datetime, sys, os
BASE=os.path.dirname(os.path.abspath(__file__))

# 30-team abbreviation -> display nickname (covers every matchup; no per-day editing)
TEAM={"ARI":"Diamondbacks","ATL":"Braves","BAL":"Orioles","BOS":"Red Sox","CHC":"Cubs",
"CWS":"White Sox","CIN":"Reds","CLE":"Guardians","COL":"Rockies","DET":"Tigers",
"HOU":"Astros","KC":"Royals","LAA":"Angels","LAD":"Dodgers","MIA":"Marlins",
"MIL":"Brewers","MIN":"Twins","NYM":"Mets","NYY":"Yankees","ATH":"Athletics",
"PHI":"Phillies","PIT":"Pirates","SD":"Padres","SF":"Giants","SEA":"Mariners",
"STL":"Cardinals","TB":"Rays","TEX":"Rangers","TOR":"Blue Jays","WSH":"Nationals"}
PSET={"NH3","NH5","NH7","UP9","UP6","K1","ALTK"}  # pitcher prop codes
# FanDuel-disambiguated name -> MLBAM id, for collision-proof grading of duplicate names.
# "Max P. Muncy" = Athletics (691777); the Dodgers' Max Muncy = 571970 (not in our slate).
KNOWN_IDS={"Max P. Muncy":691777}

def ts_of(p):
    m=re.search(r"(\d+):(\d+)\s*([AP]M)",p)
    if not m: return 0
    h=int(m.group(1))%12
    if m.group(3)=="PM": h+=12
    return h*100+int(m.group(2))

def game_pair(g):
    a,h=g.split("@"); return [TEAM.get(a,a),TEAM.get(h,h)]

def build(staging_path,out_path):
    data=json.load(open(staging_path,encoding="utf-8"))
    date=data["date"]; stage=data["bets"]
    games_used=sorted({l["g"] for b in stage for l in b["legs"]})
    GAMES={g:game_pair(g) for g in games_used}
    players={}; pitchers={}
    for b in stage:
        for l in b["legs"]:
            nm,pr,g=l["p"],l["prop"],l["g"]
            mlbid=l.get("mlb") or KNOWN_IDS.get(nm,"")
            if pr in PSET: pitchers.setdefault(nm,g)
            else:
                d=players.setdefault(nm,{"g":g,"pr":set(),"mlb":""})
                if mlbid: d["mlb"]=mlbid
                d["pr"].add("HR" if pr=="HR" else ("SB" if pr in ("SB","SB2") else pr))
    players_list=[{"n":nm,"tm":"","g":d["g"],"pr":sorted(d["pr"]) or ["HR"],"od":"","mlb":d.get("mlb","")} for nm,d in players.items()]
    pitchers_list=[{"n":nm,"tm":"","g":g} for nm,g in pitchers.items()]
    out_bets=[]
    for b in stage:
        placed=b["placed"].split(" ",1)[-1]
        placed=re.sub(r"([AP]M)$",r" \1",placed)
        legs=[(dict(p=l["p"],prop=l["prop"],void=True) if l.get("void") else dict(p=l["p"],prop=l["prop"])) for l in b["legs"]]
        out_bets.append({"id":b["id"],"kind":b["kind"],"odds":b["odds"],"wager":b["wager"],"payout":b["payout"],"placed":placed,"ts":ts_of(b["placed"]),"legs":legs})
    dt=datetime.datetime.strptime(date,"%Y-%m-%d")
    TITLEDATE="%s %d %d"%(dt.strftime("%B"),dt.day,dt.year)
    H1DATE="%s %d"%(dt.strftime("%A, %B"),dt.day)
    tpl=open(os.path.join(BASE,"tracker_template.html"),encoding="utf-8").read()
    out=(tpl.replace("__GAMES__",json.dumps(GAMES)).replace("__PLAYERS__",json.dumps(players_list))
            .replace("__PITCHERS__",json.dumps(pitchers_list)).replace("__BETS__",json.dumps(out_bets))
            .replace("__DATE__",date).replace("__TITLEDATE__",TITLEDATE).replace("__H1DATE__",H1DATE))
    out=out.replace("__BUILD__",datetime.datetime.now().strftime("%m/%d %H:%M"))
    open(out_path,"w",encoding="utf-8",newline="\n").write(out)
    print("wrote %s | bets=%d games=%d players=%d pitchers=%d | date=%s"%(out_path,len(out_bets),len(GAMES),len(players_list),len(pitchers_list),date))

if __name__=="__main__":
    staging=sys.argv[1] if len(sys.argv)>1 else os.path.join(BASE,"staging.json")
    out=sys.argv[2] if len(sys.argv)>2 else os.path.join(BASE,"index.html")
    build(staging,out)
