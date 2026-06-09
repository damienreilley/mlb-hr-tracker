# -*- coding: utf-8 -*-
import json
GAMES = {
 "NYY@CLE":["Yankees","Guardians"],"BOS@TB":["Red Sox","Rays"],"SEA@BAL":["Mariners","Orioles"],
 "PHI@TOR":["Phillies","Blue Jays"],"HOU@LAA":["Astros","Angels"],"MIL@ATH":["Brewers","Athletics"],
 "WSH@SF":["Nationals","Giants"],
}
players=[
 {"n":"Alec Bohm","tm":"PHI","g":"PHI@TOR","pr":["HIT","TB"],"od":""},
 {"n":"Trea Turner","tm":"PHI","g":"PHI@TOR","pr":["HIT"],"od":""},
 {"n":"J.T. Realmuto","tm":"PHI","g":"PHI@TOR","pr":["HR","HIT","TB"],"od":""},
 {"n":"Vladimir Guerrero Jr.","tm":"TOR","g":"PHI@TOR","pr":["HIT"],"od":""},
 {"n":"Bryce Harper","tm":"PHI","g":"PHI@TOR","pr":["HR","HIT"],"od":""},
 {"n":"George Springer","tm":"TOR","g":"PHI@TOR","pr":["HIT"],"od":""},
 {"n":"Bryson Stott","tm":"PHI","g":"PHI@TOR","pr":["HIT"],"od":""},
 {"n":"Andres Gimenez","tm":"TOR","g":"PHI@TOR","pr":["HIT"],"od":""},
 {"n":"Kyle Schwarber","tm":"PHI","g":"PHI@TOR","pr":["HR"],"od":""},
 {"n":"Dominic Canzone","tm":"SEA","g":"SEA@BAL","pr":["HR"],"od":""},
 {"n":"Luke Raley","tm":"SEA","g":"SEA@BAL","pr":["HR"],"od":""},
 {"n":"Jose Caballero","tm":"NYY","g":"NYY@CLE","pr":["HR"],"od":""},
 {"n":"Trent Grisham","tm":"NYY","g":"NYY@CLE","pr":["HR"],"od":""},
 {"n":"Ben Rice","tm":"NYY","g":"NYY@CLE","pr":["HR"],"od":""},
 {"n":"Shea Langeliers","tm":"ATH","g":"MIL@ATH","pr":["HR"],"od":""},
 {"n":"Jackson Chourio","tm":"MIL","g":"MIL@ATH","pr":["HR"],"od":""},
 {"n":"Yordan Alvarez","tm":"HOU","g":"HOU@LAA","pr":["HR"],"od":""},
 {"n":"Christian Walker","tm":"HOU","g":"HOU@LAA","pr":["HR"],"od":""},
 {"n":"Willy Adames","tm":"SF","g":"WSH@SF","pr":["HR"],"od":""},
 {"n":"Casey Schmitt","tm":"SF","g":"WSH@SF","pr":["HR"],"od":""},

  {"n": "Henry Bolte", "tm": "", "g": "MIL@ATH", "pr": ["3B"], "od": ""},
  {"n": "Brent Rooker", "tm": "", "g": "MIL@ATH", "pr": ["TB", "HR"], "od": ""},
  {"n": "Andrew Vaughn", "tm": "", "g": "MIL@ATH", "pr": ["HR"], "od": ""},
  {"n": "Christian Yelich", "tm": "", "g": "MIL@ATH", "pr": ["TB", "HR"], "od": ""},
  {"n": "Brice Turang", "tm": "", "g": "MIL@ATH", "pr": ["SB"], "od": ""},
]
pitchers=[
 {"n":"Gavin Williams","tm":"CLE","g":"NYY@CLE"},
 {"n":"Will Warren","tm":"NYY","g":"NYY@CLE"},
 {"n":"Connelly Early","tm":"BOS","g":"BOS@TB"},
 {"n":"Emerson Hancock","tm":"SEA","g":"SEA@BAL"},
 {"n":"Cristopher Sanchez","tm":"PHI","g":"PHI@TOR"},
 {"n":"Spencer Arrighetti","tm":"HOU","g":"HOU@LAA"},
 {"n":"Kyle Harrison","tm":"MIL","g":"MIL@ATH"},
]
def H(p): return {"p":p,"prop":"HR"}
def T(p): return {"p":p,"prop":"HIT"}
def F(p): return {"p":p,"prop":"FPA"}
def B(p): return {"p":p,"prop":"TB"}
def P(p,c): return {"p":p,"prop":c}
def PK(p,k): return {"p":p,"prop":"ALTK","k":k}
def D1(p): return {"p":p,"prop":"1B"}
def D2(p): return {"p":p,"prop":"2B"}
def D3(p): return {"p":p,"prop":"3B"}
def SBL(p): return {"p":p,"prop":"SB"}
def HRX(p): return {"p":p,"prop":"HR2"}
def TRn(g,line): return {"p":g+" Total","prop":"TR","g":g,"line":line}
def CTB(lbl,ps,line,g): return {"p":lbl,"prop":"CTB","ps":ps,"line":line,"g":g}
bets=[
 {"id":"#pynjyg","kind":"3-leg parlay","odds":9726,"wager":1.00,"payout":98.26,"placed":"5:24 PM","ts":1724,"legs":[PK("Gavin Williams",9),PK("Spencer Arrighetti",9),PK("Kyle Harrison",9)]},
 {"id":"#6q7q9","kind":"4-leg parlay","odds":43936,"wager":0.23,"payout":101.29,"placed":"5:22 PM","ts":1722,"legs":[PK("Gavin Williams",10),PK("Will Warren",5),PK("Spencer Arrighetti",9),PK("Kyle Harrison",10)]},
 {"id":"#7t9bg","kind":"5-leg parlay","odds":40584,"wager":0.25,"payout":101.71,"placed":"5:20 PM","ts":1720,"legs":[PK("Gavin Williams",9),PK("Will Warren",5),PK("Connelly Early",6),PK("Spencer Arrighetti",9),PK("Kyle Harrison",9)]},
 {"id":"#8vjt7","kind":"5-leg parlay","odds":8973,"wager":0.10,"payout":9.07,"placed":"5:17 PM","ts":1717,"legs":[PK("Will Warren",6),PK("Gavin Williams",8),PK("Connelly Early",6),PK("Spencer Arrighetti",8),PK("Kyle Harrison",6)]},
 {"id":"#7q13y","kind":"5-leg parlay","odds":868,"wager":0.25,"payout":2.42,"placed":"5:15 PM","ts":1715,"legs":[PK("Will Warren",4),PK("Gavin Williams",7),PK("Connelly Early",5),PK("Spencer Arrighetti",6),PK("Kyle Harrison",6)]},
 {"id":"#tdtx5","kind":"Pitcher Special","odds":1100,"wager":0.10,"payout":1.20,"placed":"4:40 PM","ts":1640,"legs":[P("Gavin Williams","K1")]},
 {"id":"#sq5m9","kind":"Pitcher Special","odds":2200,"wager":0.15,"payout":3.45,"placed":"4:40 PM","ts":1640.1,"legs":[P("Gavin Williams","NH5")]},
 {"id":"#2cbj0","kind":"Pitcher Special","odds":900,"wager":0.20,"payout":2.00,"placed":"4:40 PM","ts":1640.2,"legs":[P("Gavin Williams","UP9")]},
 {"id":"#3fmrw","kind":"Pitcher Special","odds":3000,"wager":0.10,"payout":3.10,"placed":"4:39 PM","ts":1639,"legs":[P("Will Warren","NH5")]},
 {"id":"#459yj","kind":"Pitcher Special","odds":2700,"wager":0.10,"payout":2.80,"placed":"4:39 PM","ts":1639.1,"legs":[P("Will Warren","K1")]},
 {"id":"#spqe0","kind":"Pitcher Special","odds":1100,"wager":0.15,"payout":1.80,"placed":"4:39 PM","ts":1639.2,"legs":[P("Will Warren","UP9")]},
 {"id":"#x72gf","kind":"Pitcher Special","odds":2200,"wager":0.10,"payout":2.30,"placed":"4:38 PM","ts":1638,"legs":[P("Connelly Early","K1")]},
 {"id":"#8jt5a","kind":"Pitcher Special","odds":2700,"wager":0.10,"payout":2.80,"placed":"4:38 PM","ts":1638.1,"legs":[P("Connelly Early","NH5")]},
 {"id":"#x1mvc","kind":"Pitcher Special","odds":1100,"wager":0.10,"payout":1.20,"placed":"4:38 PM","ts":1638.2,"legs":[P("Connelly Early","UP9")]},
 {"id":"#59t17","kind":"Pitcher Special","odds":1200,"wager":0.10,"payout":1.30,"placed":"4:37 PM","ts":1637,"legs":[P("Emerson Hancock","UP9")]},
 {"id":"#jw605","kind":"Pitcher Special","odds":3500,"wager":0.10,"payout":3.60,"placed":"4:37 PM","ts":1637.1,"legs":[P("Emerson Hancock","NH5")]},
 {"id":"#chbxy","kind":"Pitcher Special","odds":10000,"wager":0.10,"payout":10.10,"placed":"4:36 PM","ts":1636,"legs":[P("Cristopher Sanchez","NH7")]},
 {"id":"#xfg30","kind":"Pitcher Special","odds":500,"wager":0.50,"payout":3.00,"placed":"4:36 PM","ts":1636.1,"legs":[P("Cristopher Sanchez","NH3")]},
 {"id":"#pewt2","kind":"Pitcher Special","odds":2700,"wager":0.15,"payout":4.20,"placed":"4:36 PM","ts":1636.2,"legs":[P("Cristopher Sanchez","NH5")]},
 {"id":"#e9d5x","kind":"Pitcher Special","odds":2500,"wager":0.10,"payout":2.60,"placed":"4:36 PM","ts":1636.3,"legs":[P("Cristopher Sanchez","K1")]},
 {"id":"#pw7w9","kind":"Same Game Parlay","odds":66648,"wager":0.20,"payout":133.51,"placed":"6:23 PM","ts":1823,"legs":[{"p":"Alec Bohm","prop":"HIT4"},{"p":"Trea Turner","prop":"HIT2"},{"p":"J.T. Realmuto","prop":"HIT3"},{"p":"Vladimir Guerrero Jr.","prop":"HIT2"}]},
 {"id":"#3e130","kind":"Same Game Parlay","odds":74964,"wager":0.45,"payout":337.79,"placed":"6:23 PM","ts":1823.1,"legs":[{"p":"J.T. Realmuto","prop":"HIT4"},{"p":"Bryce Harper","prop":"HIT3"},{"p":"Vladimir Guerrero Jr.","prop":"HIT3"},{"p":"Alec Bohm","prop":"HIT2"}]},
 {"id":"#rraft","kind":"Same Game Parlay","odds":48604,"wager":0.12,"payout":58.45,"placed":"6:21 PM","ts":1821,"legs":[D3("J.T. Realmuto"),D2("Alec Bohm"),H("J.T. Realmuto")]},
 {"id":"#k0aj9","kind":"Same Game Parlay","odds":54528,"wager":0.45,"payout":245.88,"placed":"6:21 PM","ts":1821.1,"legs":[T("George Springer"),T("Bryson Stott"),{"p":"Alec Bohm","prop":"HIT3"},{"p":"Vladimir Guerrero Jr.","prop":"HIT2"},{"p":"J.T. Realmuto","prop":"HIT2"},{"p":"Bryce Harper","prop":"HIT2"},SBL("Trea Turner")]},
 {"id":"#x6q2g","kind":"Same Game Parlay","odds":85628,"wager":0.45,"payout":385.84,"placed":"6:19 PM","ts":1819,"legs":[T("Andres Gimenez"),{"p":"Vladimir Guerrero Jr.","prop":"HIT2"},{"p":"Bryce Harper","prop":"HIT3"},{"p":"Alec Bohm","prop":"HIT2"},SBL("Trea Turner"),H("J.T. Realmuto"),H("Bryce Harper")]},
 {"id":"#nepa6","kind":"Same Game Parlay","odds":85639,"wager":0.25,"payout":214.36,"placed":"6:18 PM","ts":1818,"legs":[T("Andres Gimenez"),{"p":"Vladimir Guerrero Jr.","prop":"HIT2"},{"p":"Bryce Harper","prop":"HIT3"},{"p":"Alec Bohm","prop":"HIT2"},{"p":"J.T. Realmuto","prop":"HIT2"},SBL("Trea Turner"),SBL("Bryson Stott")]},
 {"id":"#5hkcp","kind":"3-leg parlay","odds":52178,"wager":0.15,"payout":78.42,"placed":"6:14 PM","ts":1814,"legs":[H("Dominic Canzone"),H("Jose Caballero"),H("Bryce Harper")]},
 {"id":"#f080k","kind":"5-leg parlay","odds":52612,"wager":0.20,"payout":105.43,"placed":"6:13 PM","ts":1813,"legs":[H("Shea Langeliers"),H("Jackson Chourio"),H("Bryce Harper"),H("Kyle Schwarber"),H("Yordan Alvarez")]},
 {"id":"#e9nm9","kind":"4-leg parlay","odds":11956,"wager":0.10,"payout":12.06,"placed":"6:12 PM","ts":1812,"legs":[H("Shea Langeliers"),H("Jackson Chourio"),H("Kyle Schwarber"),H("Yordan Alvarez")]},
 {"id":"#z621x","kind":"3-leg parlay","odds":23135,"wager":0.15,"payout":34.85,"placed":"6:07 PM","ts":1807,"legs":[H("Luke Raley"),H("Jose Caballero"),H("Shea Langeliers")]},
 {"id":"#zfkm0","kind":"5-leg parlay","odds":471318,"wager":0.10,"payout":471.43,"placed":"6:01 PM","ts":1801,"legs":[H("Luke Raley"),H("Dominic Canzone"),H("Trent Grisham"),H("Jose Caballero"),H("Shea Langeliers")]},
 {"id":"#e1z2t","kind":"3-leg parlay","odds":8428,"wager":0.10,"payout":8.53,"placed":"5:48 PM","ts":1748,"legs":[H("Dominic Canzone"),H("Ben Rice"),H("Yordan Alvarez")]},
 {"id":"#rswb4","kind":"5-leg parlay","odds":97784,"wager":0.10,"payout":97.88,"placed":"5:48 PM","ts":1748.1,"legs":[H("Luke Raley"),H("Dominic Canzone"),H("Ben Rice"),H("Yordan Alvarez"),H("Shea Langeliers")]},
 {"id":"#t19f8","kind":"5-leg parlay","odds":183567,"wager":0.10,"payout":183.67,"placed":"5:48 PM","ts":1748.2,"legs":[H("Luke Raley"),H("Ben Rice"),H("Christian Walker"),H("Willy Adames"),H("Shea Langeliers")]},
 {"id":"#5xfjr","kind":"4-leg parlay","odds":41687,"wager":0.10,"payout":41.79,"placed":"5:47 PM","ts":1747,"legs":[H("Dominic Canzone"),H("Ben Rice"),H("Yordan Alvarez"),H("Casey Schmitt")]},
 {"id":"#4067","kind":"8-leg parlay","odds":6816302,"wager":0.10,"payout":6816.40,"placed":"5:47 PM","ts":1747.1,"legs":[H("Casey Schmitt"),H("Willy Adames"),H("Yordan Alvarez"),H("Christian Walker"),H("Luke Raley"),H("Dominic Canzone"),H("Ben Rice"),H("Shea Langeliers")]},
 {"id":"#trfbj","kind":"2-leg parlay","odds":8000,"wager":0.10,"payout":8.10,"placed":"5:37 PM","ts":1737,"legs":[{"p":"Cristopher Sanchez","prop":"NA","lbl":"NL Cy Young 2026 (futures)"},{"p":"Tarik Skubal","prop":"NA","lbl":"AL Cy Young 2026 (futures)"}]},
 {"id":"#avfc1","kind":"3-leg parlay","odds":10333,"wager":0.10,"payout":10.43,"placed":"5:28 PM","ts":1728,"legs":[{"p":"Gavin Williams","prop":"NA","lbl":"AL Cy Young 2026 (futures)"},{"p":"Shohei Ohtani","prop":"NA","lbl":"NL Cy Young 2026 (futures)"},{"p":"Kevin McGonigle","prop":"NA","lbl":"AL ROY 2026 (futures)"}]},
 {"id":"#q11x4","kind":"3-leg parlay","odds":253075,"wager":0.10,"payout":253.18,"placed":"5:27 PM","ts":1727,"legs":[{"p":"Gavin Williams","prop":"NA","lbl":"AL Cy Young 2026 (futures)"},{"p":"Shohei Ohtani","prop":"NA","lbl":"NL Cy Young 2026 (futures)"},{"p":"TJ Rumfield","prop":"NA","lbl":"NL ROY 2026 (futures)"}]},
 {"id":"#az4k0","kind":"Futures","odds":10000,"wager":0.10,"payout":10.10,"placed":"5:26 PM","ts":1726,"legs":[{"p":"Kevin McGonigle","prop":"NA","lbl":"AL MVP 2026 (futures)"}]},

  {"id": "#3ceee", "kind": "4-leg parlay", "odds": 54164, "wager": 0.09, "payout": 48.84, "placed": "9:42 PM", "ts": 2142, "legs": [{"p": "Henry Bolte", "prop": "3B"}, {"p": "Jackson Chourio", "prop": "TB5"}, {"p": "Brent Rooker", "prop": "TB"}, {"p": "Christian Yelich", "prop": "TB"}]},
  {"id": "#79ppt", "kind": "4-leg parlay", "odds": 37160, "wager": 0.09, "payout": 33.53, "placed": "9:38 PM", "ts": 2138, "legs": [{"p": "Henry Bolte", "prop": "3B"}, {"p": "Jackson Chourio", "prop": "HIT2"}, {"p": "Brice Turang", "prop": "SB"}, {"p": "Shea Langeliers", "prop": "TB"}]},
  {"id": "#sdgw1", "kind": "5-leg parlay", "odds": 66650, "wager": 0.1, "payout": 66.75, "placed": "9:33 PM", "ts": 2133, "legs": [{"p": "Shea Langeliers", "prop": "HR"}, {"p": "Brent Rooker", "prop": "HR"}, {"p": "Jackson Chourio", "prop": "HR"}, {"p": "Andrew Vaughn", "prop": "HR"}, {"p": "Christian Yelich", "prop": "HR"}]},
]

TPL = r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MLB Bet Tracker - June 8 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Spline+Sans+Mono:wght@500;600;700&family=Spline+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
 --bg:#eef1ef;--panel:#ffffff;--panel2:#f7f9f8;--line:#e0e6e2;--line2:#eef2ef;
 --ink:#172019;--ink2:#36443c;--dim:#74857b;--faint:#9fb0a6;
 --live:#e23a3a;--alive:#2563eb;--dead:#d4313a;--won:#0f9b4e;
 --c-hr:#11924f;--c-fpa:#0d8d9c;--c-tb:#7c3aed;--c-hit:#2563eb;--c-pitch:#c2700a;--c-mix:#566472;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Spline Sans',sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:14px 13px 80px}
.kicker{font-family:'Spline Sans Mono';color:var(--c-hr);font-weight:700;letter-spacing:.16em;font-size:10.5px;text-transform:uppercase}
h1{font-family:'Archivo';font-weight:900;font-size:clamp(22px,5.5vw,34px);line-height:1;margin:3px 0 2px;letter-spacing:-.01em}
.updbar{display:flex;align-items:center;gap:12px;margin-top:8px}
.upd{font-family:'Spline Sans Mono';font-size:11px;color:var(--dim)}
.btn{font-family:'Spline Sans Mono';font-weight:700;background:var(--c-hr);color:#fff;border:0;padding:7px 13px;border-radius:8px;cursor:pointer;font-size:12.5px}
.tabs{position:sticky;top:0;z-index:20;display:flex;gap:4px;margin:14px 0 16px;padding:5px;background:var(--panel);border:1px solid var(--line);border-radius:13px;box-shadow:0 2px 10px rgba(20,40,30,.04)}
.tabs button{flex:1;font-family:'Archivo';font-weight:800;font-size:13.5px;background:transparent;border:0;color:var(--dim);padding:9px 6px;border-radius:9px;cursor:pointer;transition:.12s}
.tabs button.active{background:var(--ink);color:#fff}
.tab{display:none}.tab.show{display:block;animation:fade .18s ease}
@keyframes fade{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:none}}
.muted{font-family:'Spline Sans Mono';font-size:11px;color:var(--dim)}
h2{font-family:'Archivo';font-weight:900;font-size:16px;margin:22px 0 9px}h2:first-child{margin-top:2px}
.statgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:9px;margin-bottom:14px}
.statcard{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 13px}
.statcard .n{font-family:'Archivo';font-weight:900;font-size:26px;line-height:1}
.statcard .l{font-family:'Spline Sans Mono';font-size:10.5px;color:var(--dim);text-transform:uppercase;letter-spacing:.06em;margin-top:3px}
.statcard.alive .n{color:var(--alive)}.statcard.dead .n{color:var(--dead)}.statcard.won .n{color:var(--won)}.statcard.hr .n{color:var(--c-hr)}.statcard.live .n{color:var(--live)}
.money{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:9px;margin-bottom:8px}
.moneycard.cash{background:linear-gradient(135deg,#b8860b,#8a6508)}
.moneycard{background:linear-gradient(135deg,var(--ink),#243a30);color:#fff;border-radius:12px;padding:13px 15px}
.moneycard .l{font-family:'Spline Sans Mono';font-size:10.5px;opacity:.75;text-transform:uppercase;letter-spacing:.06em}
.moneycard .n{font-family:'Archivo';font-weight:900;font-size:23px;margin-top:2px}
.moneycard.pot{background:linear-gradient(135deg,#0f9b4e,#0b6f39)}
.cattable{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.catrow{display:grid;grid-template-columns:1.4fr .6fr 1fr 1.2fr;gap:6px;padding:9px 13px;border-bottom:1px solid var(--line2);align-items:center;font-size:13px}
.catrow:last-child{border-bottom:0}.catrow.head{background:var(--panel2);font-family:'Spline Sans Mono';font-size:10px;text-transform:uppercase;letter-spacing:.05em;color:var(--dim)}
.catrow.tot{background:var(--panel2);font-weight:700}
.catchip{display:inline-flex;align-items:center;gap:6px;font-weight:700;font-size:12.5px}
.catdot{width:9px;height:9px;border-radius:3px;flex:none}.mono{font-family:'Spline Sans Mono'}
.hrtrack{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:14px;padding:11px 14px;background:var(--panel);border:1px solid var(--line);border-radius:12px}
.hrt-stat{font-family:'Spline Sans Mono';font-size:13px;color:var(--dim)}.hrt-stat b{font-family:'Archivo';font-size:21px;color:var(--c-hr);margin-right:3px}
.hrt-stat.live b{color:var(--live)}
.hrt-pills{display:flex;gap:7px;flex-wrap:wrap;margin-left:auto}
.hrpill{font-family:'Spline Sans Mono';font-size:11.5px;background:#e3f6ec;border:1px solid #bfe8d0;color:var(--c-hr);padding:4px 9px;border-radius:20px;font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:11px}
.game{background:var(--panel);border:1px solid var(--line);border-radius:13px;overflow:hidden}
.g-head{display:flex;justify-content:space-between;align-items:center;padding:9px 12px;background:var(--panel2);border-bottom:1px solid var(--line)}
.g-match{font-weight:700;font-size:13px}.g-score{font-family:'Spline Sans Mono';color:var(--dim);font-weight:500}
.g-state{font-family:'Spline Sans Mono';font-size:10.5px;padding:3px 8px;border-radius:7px;font-weight:700;white-space:nowrap}
.s-live{background:#fde7e7;color:var(--live);border:1px solid #f6c9c9}
.s-warm{background:#fbeccb;color:#9a6800;border:1px solid #f0d79a}
.s-final{background:#eef2ef;color:var(--dim);border:1px solid var(--line)}
.s-prev{background:#e8f0fb;color:var(--alive);border:1px solid #cfe0f7}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--live);margin-right:5px;animation:p 1.1s infinite}@keyframes p{0%,100%{opacity:1}50%{opacity:.25}}
.plist{padding:3px 12px 9px}
.prow{display:flex;align-items:center;gap:8px;padding:7px 2px;border-bottom:1px solid var(--line2)}.prow:last-child{border-bottom:0}
.prow.hit{background:linear-gradient(90deg,rgba(17,146,79,.1),transparent);border-radius:8px}
.mk{width:19px;height:19px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;flex:none;border:1px solid var(--line);background:var(--panel2);color:var(--faint)}
.mk.hit{background:var(--c-hr);color:#fff;border-color:var(--c-hr);font-weight:900}
.pn{font-weight:600;font-size:13px;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pn.hit{color:var(--c-hr)}
.tmtag{font-family:'Spline Sans Mono';font-size:10px;color:var(--faint);font-weight:600}
.abtag{font-family:'Spline Sans Mono';font-size:9px;font-weight:700;padding:2px 6px;border-radius:5px;white-space:nowrap;flex:none}
.abtag.ab{background:#fbeccb;color:#9a6800;border:1px solid #f0d79a;animation:p 1.3s infinite}
.abtag.od{background:#e8f0fb;color:var(--alive);border:1px solid #cfe0f7}
.podds{font-family:'Spline Sans Mono';font-size:11px;color:var(--dim);white-space:nowrap}.hitcount{font-family:'Spline Sans Mono';font-size:11px;font-weight:600;color:var(--dim);white-space:nowrap}.hrt-stat.hits b{color:var(--c-hit)}
.hrbadge{font-family:'Spline Sans Mono';font-size:11px;font-weight:700;color:#fff;background:var(--c-hr);padding:2px 8px;border-radius:20px;white-space:nowrap}
.hitbadge{font-family:'Spline Sans Mono';font-size:10.5px;font-weight:700;color:#fff;background:var(--c-hit);padding:2px 8px;border-radius:20px;white-space:nowrap}
.tbbadge{font-family:'Spline Sans Mono';font-size:10.5px;font-weight:700;color:#fff;background:var(--c-tb);padding:2px 8px;border-radius:20px;white-space:nowrap}
.pitchstat{display:flex;flex-direction:column;gap:6px;margin-top:2px}
.pchip{display:flex;justify-content:space-between;align-items:center;font-family:'Spline Sans';font-size:13.5px;font-weight:600;padding:8px 11px;border-radius:8px;border:1px solid var(--line);background:var(--panel2);color:var(--ink)}
.pchip .pcd{font-family:'Spline Sans Mono';font-size:12px;color:var(--dim);font-weight:600}
.pchip.hit{background:#e3f6ec;color:var(--won);border-color:#bfe8d0}.pchip.hit .pcd{color:var(--won)}
.pchip.miss{background:#fbe6e7;color:var(--dead);border-color:#f2c9cc}.pchip.miss .pcd{color:var(--dead)}
.filterbar{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:2px 0 14px}
.filterbtn{font-family:'Spline Sans Mono';font-weight:700;background:var(--panel);border:1px solid var(--line);color:var(--ink2);padding:6px 11px;border-radius:9px;cursor:pointer;font-size:12px}
.filterbtn.active{background:var(--alive);color:#fff;border-color:var(--alive)}
.filterbtn.s.active{background:var(--ink);border-color:var(--ink)}
.catsection{margin-bottom:14px}
.cathead{display:flex;align-items:center;gap:9px;margin:0 0 9px;padding:8px 2px;border-bottom:2px solid var(--line);cursor:pointer;user-select:none}
.cathead .bar{width:5px;height:18px;border-radius:3px;flex:none}
.cathead h3{font-family:'Archivo';font-weight:900;font-size:15px;margin:0}
.cathead .cnt{font-family:'Spline Sans Mono';font-size:11px;color:var(--dim);margin-left:auto}
.chev{font-size:12px;color:var(--dim);transition:transform .15s;width:14px;text-align:center}
.catsection.collapsed .catbody{display:none}.catsection.collapsed .cathead .chev{transform:rotate(-90deg)}
.bet{background:var(--panel);border:1px solid var(--line);border-left-width:5px;border-radius:11px;overflow:hidden}
.bet.b-dead{opacity:.62}.bet.b-won{box-shadow:0 0 0 1px var(--won) inset}
.b-head{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px 12px;cursor:pointer;user-select:none}
.b-left{min-width:0}
.b-kind{font-family:'Archivo';font-weight:800;font-size:13px}.b-kind-name{font-size:15px}.b-id{font-family:'Spline Sans Mono';font-size:10px;color:var(--faint)}
.b-meta{font-family:'Spline Sans Mono';font-size:10.5px;color:var(--dim);margin-top:3px}
.b-stat{font-family:'Spline Sans Mono';font-weight:700;font-size:10px;padding:2px 7px;border-radius:6px;white-space:nowrap;margin-left:7px}
.b-stat.b-alive{background:#e8f0fb;color:var(--alive)}.b-stat.b-dead{background:#fbe6e7;color:var(--dead)}.b-stat.b-won{background:#e3f6ec;color:var(--won)}
.b-right{display:flex;flex-direction:column;align-items:flex-end;flex:none}
.b-pay{font-family:'Archivo';font-weight:900;font-size:19px;color:var(--won);line-height:1;white-space:nowrap}
.bet.b-dead .b-pay{color:var(--faint)}
.b-chev{font-size:11px;color:var(--faint);margin-top:3px}
.b-legs{padding:2px 12px 10px;display:flex;flex-direction:column;gap:1px;border-top:1px dashed var(--line)}
.bet.collapsed .b-legs{display:none}.bet.collapsed .b-chev{transform:rotate(-90deg)}
.leg{display:flex;align-items:center;gap:8px;padding:5px 2px;font-size:13px}
.lmk{width:16px;text-align:center;font-weight:900;flex:none}
.l-hit .lmk{color:var(--c-hr)}.l-hit .lname{color:var(--c-hr);font-weight:600}
.l-miss .lmk{color:var(--dead)}.l-miss .lname{text-decoration:line-through;color:var(--faint)}
.l-pend .lmk{color:var(--faint)}
.lname{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lprop{font-family:'Spline Sans Mono';font-size:11px;color:var(--dim);white-space:nowrap}
.labtag{font-family:'Spline Sans Mono';font-size:8.5px;font-weight:700;padding:1px 5px;border-radius:4px;flex:none}
.labtag.ab{background:#fbeccb;color:#9a6800}.labtag.od{background:#e8f0fb;color:var(--alive)}
.pspec{display:flex;justify-content:space-between;align-items:center;padding:8px 2px;font-size:15px;font-weight:600;border-top:1px dashed var(--line)}
.pspec .psp{display:flex;align-items:center;gap:8px}.pspec .psd{font-family:'Spline Sans Mono';font-size:13px;color:var(--dim)}
.pspec.l-hit{color:var(--won)}.pspec.l-hit .psd{color:var(--won)}
.pspec.l-miss{color:var(--dead)}.pspec.l-miss .psp .pst{text-decoration:line-through}
footer{margin-top:24px;padding-top:14px;border-top:1px solid var(--line);color:var(--dim);font-size:10.5px;line-height:1.6;font-family:'Spline Sans Mono'}
</style></head><body><div class="wrap">
<div class="kicker">Live Bet Tracker</div>
<h1>Monday, June 8 &mdash; MLB Bets</h1>
<div class="updbar"><span class="upd" id="updated">Loading...</span><button class="btn" id="refresh">Refresh</button></div>
<nav class="tabs">
 <button data-tab="summary" class="active">Summary</button>
 <button data-tab="hitters">Hitters</button>
 <button data-tab="pitchers">Pitchers</button>
 <button data-tab="bets">Bets</button>
</nav>
<section id="tab-summary" class="tab show"></section>
<section id="tab-hitters" class="tab"><div id="hitters"><p class="muted">Connecting to MLB live feed...</p></div></section>
<section id="tab-pitchers" class="tab">
 <div class="filterbar"><span class="muted">Show:</span>
  <button class="filterbtn active" data-pf="all">All</button>
  <button class="filterbtn" data-pf="alive">Alive</button>
  <button class="filterbtn" data-pf="dead">Dead</button>
  <button class="filterbtn" data-pf="won">Cashed</button>
 </div>
 <div id="pitchersv"></div>
</section>
<section id="tab-bets" class="tab">
 <div class="filterbar"><span class="muted">Show:</span>
  <button class="filterbtn active" data-f="all">All</button>
  <button class="filterbtn" data-f="alive">Alive</button>
  <button class="filterbtn" data-f="dead">Dead</button>
  <button class="filterbtn" data-f="won">Cashed</button>
  <span class="muted" style="margin-left:8px">Sort:</span>
  <button class="filterbtn s active" data-s="payout">Payout</button>
  <button class="filterbtn s" data-s="legs">Legs</button>
 </div>
 <div id="bets"></div>
</section>
<footer>Auto-refreshes every 60s while the tab is open (your browser polls statsapi.mlb.com; not a push alert; stops when closed). Odds are the FanDuel prices from your betslips. Pitcher specials, total bases, and exotic props are tracked live, best-effort &mdash; confirm final settlement on FanDuel. A bet goes DEAD when any leg can no longer hit.</footer>
</div>
<script>
const DATE="2026-06-08";
const SCHED="https://statsapi.mlb.com/api/v1/schedule?sportId=1&date="+DATE+"&hydrate=linescore,team";
const FEED=function(pk){return "https://statsapi.mlb.com/api/v1.1/game/"+pk+"/feed/live";};
const GAMES=__GAMES__;const players=__PLAYERS__;const pitchers=__PITCHERS__;const allBets=__BETS__;const bets=allBets.filter(function(b){return !(b.legs&&b.legs.length&&b.legs.every(function(l){return l.prop==='NA';}));});
const norm=function(s){return (s||"").normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z ]/g,'').replace(/\s+/g,' ').trim();};
players.forEach(function(p){p.k=norm(p.n);});pitchers.forEach(function(p){p.k=norm(p.n);});
const pByKey={};players.forEach(function(p){pByKey[p.k]=p;});
const pitByKey={};pitchers.forEach(function(p){pitByKey[p.k]=p;});
const CATS=[{k:'PARLAY',label:'Parlays',v:'--c-fpa'},{k:'HR',label:'Home Runs',v:'--c-hr'},{k:'FPA',label:'First-PA HR',v:'--c-fpa'},{k:'TB',label:'Total Bases',v:'--c-tb'},{k:'HIT',label:'Hits',v:'--c-hit'},{k:'PITCH',label:'Pitcher Specials',v:'--c-pitch'},{k:'MIX',label:'Mixed',v:'--c-mix'}];
const CATMAP={};CATS.forEach(function(c){CATMAP[c.k]=c;});
const PITCHSET={NH3:1,NH5:1,NH7:1,K1:1,UP9:1,UP6:1,ALTK:1};
const BATSET={HR:1,HIT:1,FPA:1,TB:1,'1B':1,'2B':1,'3B':1,SB:1,HR2:1,HIT2:1,TB2:1,TB3:1,TB5:1,RUN:1,RBI:1,RBI2:1,RBI3:1,RBI4:1,HRR2:1,HIT3:1,HIT4:1,RUN2:1,SB2:1};
const HITEV={single:1,double:2,triple:3,home_run:4};
const PLAB={HR:'HR',HIT:'Hit',FPA:'1st-PA HR',TB:'4+ TB','1B':'Single','2B':'Double','3B':'Triple','SB':'Stolen Base',HR2:'2+ HR',HIT2:'2+ Hits',TB2:'2+ TB',TB3:'3+ TB',TB5:'5+ TB',RUN:'Run',RBI:'RBI',RBI2:'2+ RBIs',RBI3:'3+ RBIs',RBI4:'4+ RBIs',HRR2:'2+ H+R+RBI',HIT3:'3+ Hits',HIT4:'4+ Hits',RUN2:'2+ Runs',SB2:'2+ SB',NA:'Manual (FD)',CTB:'Combined TB',NH3:'No-hit thru 3',NH5:'No-hit thru 5',NH7:'No-hit thru 7',K1:'3+ K in 1st',UP9:'9 up 9 down',UP6:'6 up 6 down'};
let filterMode='all';let betSort='payout';let betSortDir='desc';let pitchFilter='all';let GS={};let STATS={};let collapsedSecs={};let collapsedBets={};
const $=function(id){return document.getElementById(id);};
function resetStats(){players.forEach(function(p){p.hr=[];p.atbat=false;p.ondeck=false;p.fpaDone=false;p.fpaHR=false;p.tmLive='';});pitchers.forEach(function(p){p.h3=0;p.h5=0;p.h7=0;p.k1=0;p.kTot=0;p.seq=[];p.tmLive='';});STATS={};}
resetStats();
async function gj(u){const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);return r.json();}
function ordSuffix(n){if(n%10==1&&n%100!=11)return n+'st';if(n%10==2&&n%100!=12)return n+'nd';if(n%10==3&&n%100!=13)return n+'rd';return n+'th';}
function etTime(iso){try{return new Date(iso).toLocaleTimeString('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit'})+' ET';}catch(e){return '';}}
function amStr(o){return (o>0?'+':'')+o.toLocaleString();}
function money(n){return '$'+n.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});}
function statOf(name){return STATS[norm(name)]||{hits:0,doubles:0,triples:0,hr:0,sb:0,tb:0,runs:0,rbi:0};}
function teamOf(name){const s=STATS[norm(name)];if(s&&s.tm)return s.tm;const p=pByKey[norm(name)];if(p)return p.tmLive||p.tm||'';const q=pitByKey[norm(name)];return q?(q.tmLive||q.tm||''):'';}
function legGame(l){if(l.g)return l.g;const p=pByKey[norm(l.p)];if(p)return p.g;const q=pitByKey[norm(l.p)];if(q)return q.g;return '?';}
async function refresh(){
 $('updated').textContent='Updating...';
 let sched;try{sched=await gj(SCHED);}catch(e){$('updated').textContent="Can't reach MLB feed - retrying";return;}
 const allGames=(sched.dates&&sched.dates[0]&&sched.dates[0].games)?sched.dates[0].games:[];
 resetStats();GS={};const keyToGame={};
 for(const key in GAMES){const a=GAMES[key][0],b=GAMES[key][1];
  const g=allGames.find(function(x){const an=x.teams.away.team.name,hn=x.teams.home.team.name;return (an.includes(a)||hn.includes(a))&&(an.includes(b)||hn.includes(b));});
  if(g)keyToGame[key]=g;}
 const careGames={};for(const key in keyToGame){careGames[keyToGame[key].gamePk]=keyToGame[key];}
 let live=0;const feedByPk={};
 for(const pk in careGames){const g=careGames[pk];const st=g.status.abstractGameState;if(st==='Live')live++;
  if(st==='Live'||st==='Final'){try{feedByPk[pk]=await gj(FEED(pk));}catch(e){feedByPk[pk]={__err:true};}}}
 for(const pk in feedByPk){const f=feedByPk[pk];if(f.__err)continue;
  const box=f.liveData&&f.liveData.boxscore&&f.liveData.boxscore.teams;
  if(box){['away','home'].forEach(function(side){const tb=box[side];if(!tb)return;const ab=tb.team&&tb.team.abbreviation?tb.team.abbreviation:'';const pl=tb.players||{};
   for(const id in pl){const per=pl[id].person;const nm=per?norm(per.fullName):'';if(!nm)continue;
    const bt=(pl[id].stats&&pl[id].stats.batting)?pl[id].stats.batting:{};
    const hits=bt.hits||0,d=bt.doubles||0,t=bt.triples||0,hr=bt.homeRuns||0,sb=bt.stolenBases||0,rns=bt.runs||0,rbiv=bt.rbi||0;
    STATS[nm]={hits:hits,doubles:d,triples:t,hr:hr,sb:sb,tb:hits+d+2*t+3*hr,runs:rns,rbi:rbiv,tm:ab};
    if(pByKey[nm])pByKey[nm].tmLive=ab;if(pitByKey[nm])pitByKey[nm].tmLive=ab;}});}
  const plays=(f.liveData&&f.liveData.plays&&f.liveData.plays.allPlays)?f.liveData.plays.allPlays:[];
  for(const pl of plays){const ev=pl.result&&pl.result.eventType;if(!ev)continue;
   const inn=(pl.about&&pl.about.inning)?pl.about.inning:99;
   const bk=norm(pl.matchup&&pl.matchup.batter?pl.matchup.batter.fullName:'');const pp=pByKey[bk];
   if(pp){if(ev==='home_run')pp.hr.push(inn);if(!pp.fpaDone){pp.fpaDone=true;pp.fpaHR=(ev==='home_run');}}
   const ptk=norm(pl.matchup&&pl.matchup.pitcher?pl.matchup.pitcher.fullName:'');const ptp=pitByKey[ptk];
   if(ptp){if(HITEV[ev]){if(inn<=3)ptp.h3++;if(inn<=5)ptp.h5++;if(inn<=7)ptp.h7++;}if(ev==='strikeout'&&inn===1)ptp.k1++;if(ev==='strikeout'||ev==='strikeout_double_play')ptp.kTot++;ptp.seq.push((HITEV[ev]||ev==='walk'||ev==='intent_walk'||ev==='hit_by_pitch'||ev==='field_error'||ev==='catcher_interf'||ev==='fielders_choice')?0:1);}}
  const off=f.liveData&&f.liveData.linescore&&f.liveData.linescore.offense;
  if(off){const ab=off.batter&&off.batter.fullName?norm(off.batter.fullName):'';const od=off.onDeck&&off.onDeck.fullName?norm(off.onDeck.fullName):'';
   if(pByKey[ab])pByKey[ab].atbat=true;if(pByKey[od])pByKey[od].ondeck=true;}}
 for(const key in GAMES){const g=keyToGame[key];if(!g){GS[key]={state:'NA'};continue;}
  const ls=g.linescore||{};const st=g.status.abstractGameState;
  GS[key]={state:st,detail:g.status.detailedState,inn:ls.currentInning||0,half:ls.inningState,
   as:(ls.teams&&ls.teams.away&&ls.teams.away.runs!=null)?ls.teams.away.runs:(g.teams.away.score||0),
   hs:(ls.teams&&ls.teams.home&&ls.teams.home.runs!=null)?ls.teams.home.runs:(g.teams.home.score||0),time:g.gameDate};}
 bets.forEach(function(b){b._cat=betCat(b);const s=betStatus(b);b._st=s.st;b._hit=s.hit;});
 renderSummary(live);renderHitters(live);renderPitchers();renderBets();
 $('updated').textContent='Updated '+new Date().toLocaleTimeString('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit',second:'2-digit'})+' ET';
}
function legMet(leg){const pr=leg.prop;
 if(pr==='TR'){const gs=GS[leg.g]||{};const tot=(gs.as||0)+(gs.hs||0);if(tot>(leg.line||8.5))return 'hit';if(gs.state==='Final')return 'miss';return 'pending';}
 if(pr==='CTB'){const gs=GS[leg.g]||{};let sum=0;leg.ps.forEach(function(n){sum+=(statOf(n).tb||0);});if(sum>=(leg.line||6))return 'hit';if(gs.state==='Final')return 'miss';return 'pending';}
 if(BATSET[pr]){const p=pByKey[norm(leg.p)];const gs=p?GS[p.g]:null;const fin=gs&&gs.state==='Final';const s=statOf(leg.p);
  if(pr==='HR')return (s.hr>=1||(p&&p.hr.length>0))?'hit':(fin?'miss':'pending');
  if(pr==='HIT')return (s.hits>=1)?'hit':(fin?'miss':'pending');
  if(pr==='TB')return (s.tb>=4)?'hit':(fin?'miss':'pending');
  if(pr==='2B')return (s.doubles>=1)?'hit':(fin?'miss':'pending');
  if(pr==='3B')return (s.triples>=1)?'hit':(fin?'miss':'pending');
  if(pr==='HR2')return (s.hr>=2)?'hit':(fin?'miss':'pending');
  if(pr==='HIT2')return (s.hits>=2)?'hit':(fin?'miss':'pending');
  if(pr==='TB2')return (s.tb>=2)?'hit':(fin?'miss':'pending');
  if(pr==='TB3')return (s.tb>=3)?'hit':(fin?'miss':'pending');
  if(pr==='TB5')return (s.tb>=5)?'hit':(fin?'miss':'pending');
  if(pr==='RUN')return (s.runs>=1)?'hit':(fin?'miss':'pending');
  if(pr==='RBI')return (s.rbi>=1)?'hit':(fin?'miss':'pending');
  if(pr==='RBI2')return (s.rbi>=2)?'hit':(fin?'miss':'pending');
  if(pr==='RBI3')return (s.rbi>=3)?'hit':(fin?'miss':'pending');
  if(pr==='RBI4')return (s.rbi>=4)?'hit':(fin?'miss':'pending');
  if(pr==='HRR2')return ((s.hits+s.runs+s.rbi)>=2)?'hit':(fin?'miss':'pending');
  if(pr==='HIT3')return (s.hits>=3)?'hit':(fin?'miss':'pending');
  if(pr==='HIT4')return (s.hits>=4)?'hit':(fin?'miss':'pending');
  if(pr==='RUN2')return (s.runs>=2)?'hit':(fin?'miss':'pending');
  if(pr==='SB2')return (s.sb>=2)?'hit':(fin?'miss':'pending');
  if(pr==='SB')return (s.sb>=1)?'hit':(fin?'miss':'pending');
  if(pr==='1B')return ((s.hits-s.doubles-s.triples-s.hr)>=1)?'hit':(fin?'miss':'pending');
  if(pr==='FPA'){if(p&&p.fpaDone)return p.fpaHR?'hit':'miss';return fin?'miss':'pending';}}
 const p=pitByKey[norm(leg.p)];if(!p)return 'pending';const gs=GS[p.g]||{};const inn=gs.inn||0;
 if(pr==='NH3'||pr==='NH5'||pr==='NH7'){const N=pr==='NH3'?3:(pr==='NH5'?5:7);const h=pr==='NH3'?p.h3:(pr==='NH5'?p.h5:p.h7);if(h>0)return 'miss';if(inn>N)return 'hit';return 'pending';}
 if(pr==='K1'){if(p.k1>=3)return 'hit';if(inn>1)return 'miss';return 'pending';}
 if(pr==='ALTK'){if(p.kTot>=(leg.k||0))return 'hit';if(gs.state==='Final')return 'miss';return 'pending';}
 if(pr==='UP9'||pr==='UP6'){const N=pr==='UP9'?9:6;let reached=false;const m=Math.min(N,p.seq.length);for(let i=0;i<m;i++){if(p.seq[i]===0){reached=true;break;}}if(reached)return 'miss';if(p.seq.length>=N)return 'hit';if(gs.state==='Final')return 'miss';return 'pending';}
 return 'pending';}
function betCat(b){if(b.legs.length>1)return 'PARLAY';const props=Array.from(new Set(b.legs.map(function(l){return l.prop;})));
 if(props.every(function(p){return PITCHSET[p];}))return 'PITCH';
 if(props.length===1&&CATMAP[props[0]])return props[0];
 return 'MIX';}
function betStatus(b){let hit=0,miss=0;for(const lg of b.legs){const s=legMet(lg);if(s==='hit')hit++;else if(s==='miss')miss++;}const st=miss>0?'dead':(hit===b.legs.length?'won':'alive');return {st:st,hit:hit,total:b.legs.length};}
function pitchDetail(leg){const pr=leg.prop;const p=pitByKey[norm(leg.p)];if(!p)return '';
 if(pr==='NH3')return p.h3+' hits';if(pr==='NH5')return p.h5+' hits';if(pr==='NH7')return p.h7+' hits';if(pr==='K1')return 'now '+p.k1;if(pr==='ALTK')return 'now '+p.kTot;
 if(pr==='UP9'||pr==='UP6'){let r=0;for(const x of p.seq){if(x===1)r++;else break;}return r+' retired';}return '';}
function legNameHTML(leg){if(leg.prop==='TR'||leg.prop==='CTB')return leg.p;const t=teamOf(leg.p);return leg.p+(t?' <span class="tmtag">('+t+')</span>':'');}
function lpropText(leg){if(leg.prop==='TR')return 'Over '+(leg.line||8.5)+' Runs';if(leg.prop==='CTB')return (leg.line||6)+'+ Combined TB';if(leg.prop==='ALTK')return (leg.k||0)+'+ K';let t=PLAB[leg.prop]||leg.prop;const pp=leg.prop;if(pp==='NA')return leg.lbl||'Manual (track on FD)';if(pp==='TB'||pp==='TB2'||pp==='TB3'||pp==='TB5'){t+=' &middot; now '+statOf(leg.p).tb;}else if(pp==='HIT2'||pp==='HIT3'||pp==='HIT4'){t+=' &middot; now '+statOf(leg.p).hits;}else if(pp==='RBI'||pp==='RBI2'||pp==='RBI3'||pp==='RBI4'){t+=' &middot; now '+statOf(leg.p).rbi;}else if(pp==='RUN'||pp==='RUN2'){t+=' &middot; now '+statOf(leg.p).runs;}else if(pp==='SB2'){t+=' &middot; now '+statOf(leg.p).sb;}else if(pp==='HRR2'){const ss=statOf(leg.p);t+=' &middot; now '+(ss.hits+ss.runs+ss.rbi);}return t;}
function betCardHTML(b){
 const cat=CATMAP[b._cat];const cvar='var('+cat.v+')';
 const cl=b._st==='dead'?'b-dead':(b._st==='won'?'b-won':'b-alive');
 const lbl=b._st==='dead'?'DEAD':(b._st==='won'?'CASHED':'ALIVE');const isPS=b._cat==='PITCH';
  let body='';
 for(const lg of b.legs){const st=legMet(lg);const isP=PITCHSET[lg.prop];const p=isP?null:pByKey[norm(lg.p)];
   const mk=st==='hit'?'&#10003;':(st==='miss'?'&#10007;':'&middot;');const lc=st==='hit'?'l-hit':(st==='miss'?'l-miss':'l-pend');
   const inn=(st==='hit'&&(lg.prop==='HR'||lg.prop==='FPA')&&p&&p.hr.length)?(' '+ordSuffix(p.hr[0])):'';
   let lab='';if(!isP&&st==='pending'&&p){if(p.atbat)lab='<span class="labtag ab">AB</span>';else if(p.ondeck)lab='<span class="labtag od">OD</span>';}
   let propTxt=lpropText(lg);if(isP){const d=pitchDetail(lg);if(d)propTxt+=' &middot; '+d;}
   body+='<div class="leg '+lc+'"><span class="lmk">'+mk+'</span>'+(isPS?'':'<span class="lname">'+legNameHTML(lg)+'</span>')+lab+'<span class="lprop">'+propTxt+inn+'</span></div>';}
 return '<div class="bet '+cl+(collapsedBets[b.id]?' collapsed':'')+'" data-bid="'+b.id+'" style="border-left-color:'+cvar+'"><div class="b-head" onclick="toggleBet(this)"><div class="b-left"><span class="b-kind'+(isPS?' b-kind-name':'')+'">'+(isPS?legNameHTML(b.legs[0]):b.kind)+'</span> <span class="b-id">'+b.id+'</span><span class="b-stat '+cl+'">'+lbl+(b.legs.length>1?(' '+b._hit+'/'+b.legs.length):'')+'</span><div class="b-meta">'+amStr(b.odds)+' &middot; '+money(b.wager)+' wager</div></div><div class="b-right"><span class="b-pay">'+money(b.payout)+'</span><span class="b-chev">&#9660;</span></div></div><div class="b-legs">'+body+'</div></div>';
}
function renderSummary(live){
 let alive=0,dead=0,won=0,wonPay=0,totW=0,totP=0;const byCat={};CATS.forEach(function(c){byCat[c.k]={n:0,w:0,p:0};});
 bets.forEach(function(b){totW+=b.wager;totP+=b.payout;const c=byCat[b._cat];c.n++;c.w+=b.wager;c.p+=b.payout;if(b._st==='dead')dead++;else if(b._st==='won'){won++;wonPay+=b.payout;}else alive++;});
 const homered=players.filter(function(p){return p.hr.length>0;}).length;
 let h='<div class="statgrid">'+
  '<div class="statcard alive"><div class="n">'+alive+'</div><div class="l">Bets alive</div></div>'+
  '<div class="statcard dead"><div class="n">'+dead+'</div><div class="l">Dead</div></div>'+
  '<div class="statcard won"><div class="n">'+won+'</div><div class="l">Cashed</div></div>'+
  '<div class="statcard hr"><div class="n">'+homered+'</div><div class="l">Homered</div></div>'+
  '<div class="statcard live"><div class="n">'+live+'</div><div class="l">Games live</div></div></div>';
 h+='<div class="money"><div class="moneycard"><div class="l">Total wagered today</div><div class="n">'+money(totW)+'</div></div><div class="moneycard pot"><div class="l">Total potential payout</div><div class="n">'+money(totP)+'</div></div><div class="moneycard cash"><div class="l">Cashed so far ('+won+' bet'+(won===1?'':'s')+')</div><div class="n">'+money(wonPay)+'</div></div></div>';
 h+='<div class="cattable"><div class="catrow head"><span>Bet type</span><span>Bets</span><span>Wagered</span><span>Potential</span></div>';
 CATS.forEach(function(c){const d=byCat[c.k];if(!d.n)return;h+='<div class="catrow"><span class="catchip"><span class="catdot" style="background:var('+c.v+')"></span>'+c.label+'</span><span class="mono">'+d.n+'</span><span class="mono">'+money(d.w)+'</span><span class="mono">'+money(d.p)+'</span></div>';});
 h+='<div class="catrow tot"><span>All bets</span><span class="mono">'+bets.length+'</span><span class="mono">'+money(totW)+'</span><span class="mono">'+money(totP)+'</span></div></div>';
 const al=bets.filter(function(b){return b._st!=='dead';}).sort(function(a,b){return b.payout-a.payout;}).slice(0,6);
 h+='<h2>Biggest tickets still alive</h2>';
 h+=al.length?('<div class="grid">'+al.map(betCardHTML).join('')+'</div>'):'<p class="muted">Nothing alive right now.</p>';
 $('tab-summary').innerHTML=h;
}
function gameBadge(gs){let badge,cls;
 if(gs.state==='Live'&&(gs.detail==='Warmup'||!gs.inn)){cls='s-warm';badge='<span class="dot"></span>Warmup';}
 else if(gs.state==='Live'){cls='s-live';badge='<span class="dot"></span>'+(gs.half?gs.half+' ':'')+ordSuffix(gs.inn);}
 else if(gs.state==='Final'){cls='s-final';badge=gs.detail||'Final';}
 else if(gs.state==='Preview'||gs.state==='Pre-Game'){cls='s-prev';badge=etTime(gs.time);}
 else{cls='s-prev';badge='--';}return {badge:badge,cls:cls};}
function renderHitters(live){
 const order=Object.keys(GAMES);
 order.sort(function(A,B){const rk=function(key){const hr=players.some(function(p){return p.g===key&&p.hr.length>0;});if(hr)return 0;const s=GS[key]?GS[key].state:'NA';return s==='Live'?1:((s==='Preview'||s==='Pre-Game')?2:(s==='Final'?3:4));};return rk(A)-rk(B);});
 const homered=players.filter(function(p){return p.hr.length>0;});const totalP=players.length;const totHits=players.reduce(function(a,p){return a+(statOf(p.n).hits||0);},0);
 let track='<div class="hrtrack"><div class="hrt-stat"><b>'+homered.length+'</b> of '+totalP+' homered</div><div class="hrt-stat hits"><b>'+totHits+'</b> hits</div><div class="hrt-stat live"><b>'+live+'</b> games live</div><div class="hrt-pills">'+(homered.length?homered.map(function(p){return '<span class="hrpill">&#9733; '+p.n+(p.hr.length>1?' x'+p.hr.length:'')+'</span>';}).join(''):'<span class="muted">none yet</span>')+'</div></div>';
 let html=track+'<div class="grid">';
 for(const key of order){const ps=players.filter(function(p){return p.g===key;});if(!ps.length)continue;
  const gs=GS[key]||{};const gb=gameBadge(gs);const showScore=(gs.state==='Live'||gs.state==='Final');
  const psort=ps.slice().sort(function(a,b){return (b.hr.length>0?1:0)-(a.hr.length>0?1:0);});
  let rows='';
  for(const p of psort){const homer=p.hr.length>0;const s=statOf(p.n);const hasHit=p.pr.some(function(x){return x.indexOf('HIT')===0;});const hasTB=p.pr.some(function(x){return x.indexOf('TB')===0;});const tm=p.tmLive||p.tm;
   let right;
   if(homer)right='<span class="hrbadge">&#128165; HR &middot; '+p.hr.map(function(i){return ordSuffix(i);}).join(', ')+'</span>';
   else if(hasTB&&s.tb>=4)right='<span class="tbbadge">&#10003; '+s.tb+' TB</span>';
   else if(hasHit&&s.hits>=1)right='<span class="hitbadge">&#10003; '+s.hits+' H</span>';
   else if(s.hits>=1)right='<span class="hitcount">'+s.hits+' H</span>';
   else right='<span class="podds">'+(p.od?p.od:'&mdash;')+'</span>';
   let abt='';if(!homer){if(p.atbat)abt='<span class="abtag ab">AT BAT</span>';else if(p.ondeck)abt='<span class="abtag od">ON DECK</span>';}
   const hc=(homer||(hasTB&&s.tb>=4)||(hasHit&&s.hits>=1))?' hit':'';
   rows+='<div class="prow'+hc+'"><div class="mk'+(homer?' hit':'')+'">'+(homer?'&#9733;':'&middot;')+'</div><span class="pn'+(homer?' hit':'')+'">'+p.n+(tm?' <span class="tmtag">('+tm+')</span>':'')+'</span>'+abt+right+'</div>';}
  html+='<div class="game"><div class="g-head"><div class="g-match">'+key.replace('@',' @ ')+(showScore?'<span class="g-score"> &nbsp;'+gs.as+'-'+gs.hs+'</span>':'')+'</div><div class="g-state '+gb.cls+'">'+gb.badge+'</div></div><div class="plist">'+rows+'</div></div>';}
 html+='</div>';$('hitters').innerHTML=html;
}
function renderPitchers(){
 const pbets=bets.filter(function(b){return b._cat==='PITCH'&&(pitchFilter==='all'||b._st===pitchFilter);});
 const sortedP=pitchers.slice().sort(function(a,b){return a.n.localeCompare(b.n);});
 let html='';
 sortedP.forEach(function(pt){const grp=pbets.filter(function(b){return norm(b.legs[0].p)===pt.k;});if(!grp.length)return;
  grp.sort(function(a,b){return b.payout-a.payout;});
  const gs=GS[pt.g]||{};const gb=gameBadge(gs);const tm=pt.tmLive||pt.tm;const ck='p:'+pt.k;
  html+='<div class="catsection'+(collapsedSecs[ck]?' collapsed':'')+'" data-ck="'+ck+'"><div class="cathead" onclick="toggleCat(this)"><span class="bar" style="background:var(--c-pitch)"></span><h3>'+pt.n+(tm?' <span class="tmtag" style="font-size:12px">('+tm+')</span>':'')+'</h3><span class="cnt"><span class="g-state '+gb.cls+'">'+gb.badge+'</span> &nbsp;'+grp.length+' bet'+(grp.length>1?'s':'')+'</span><span class="chev">&#9660;</span></div><div class="catbody"><div class="grid">'+grp.map(betCardHTML).join('')+'</div></div></div>';});
 $('pitchersv').innerHTML=html||'<p class="muted">No pitcher specials match this filter.</p>';
}
function renderBets(){
 let pool=bets.filter(function(b){return filterMode==='all'||b._st===filterMode;});let html='';
 CATS.forEach(function(c){let grp=pool.filter(function(b){return b._cat===c.k;});if(!grp.length)return;
  if(c.k==='PITCH')grp.sort(function(a,b){return norm(a.legs[0].p).localeCompare(norm(b.legs[0].p))||(b.payout-a.payout);});
  else{if(betSort==='legs')grp.sort(function(a,b){return (b.legs.length-a.legs.length)||(b.payout-a.payout);});else grp.sort(function(a,b){return b.payout-a.payout;});if(betSortDir==='asc')grp.reverse();}
  const ck='b:'+c.k;
  html+='<div class="catsection'+(collapsedSecs[ck]?' collapsed':'')+'" data-ck="'+ck+'"><div class="cathead" onclick="toggleCat(this)"><span class="bar" style="background:var('+c.v+')"></span><h3>'+c.label+'</h3><span class="cnt">'+grp.length+' bet'+(grp.length>1?'s':'')+'</span><span class="chev">&#9660;</span></div><div class="catbody"><div class="grid">'+grp.map(betCardHTML).join('')+'</div></div></div>';});
 $('bets').innerHTML=html||'<p class="muted">No bets match this filter.</p>';
}
function toggleBet(el){const b=el.closest('.bet');const id=b.dataset.bid;if(collapsedBets[id])delete collapsedBets[id];else collapsedBets[id]=1;b.classList.toggle('collapsed');}
function toggleCat(el){const s=el.closest('.catsection');const k=s.dataset.ck;if(collapsedSecs[k])delete collapsedSecs[k];else collapsedSecs[k]=1;s.classList.toggle('collapsed');}
function showTab(t){document.querySelectorAll('.tabs button').forEach(function(b){b.classList.toggle('active',b.dataset.tab===t);});document.querySelectorAll('.tab').forEach(function(s){s.classList.toggle('show',s.id==='tab-'+t);});}
document.querySelectorAll('.tabs button').forEach(function(b){b.addEventListener('click',function(){showTab(b.dataset.tab);});});
document.querySelectorAll('.filterbtn[data-f]').forEach(function(b){b.addEventListener('click',function(){filterMode=b.dataset.f;document.querySelectorAll('.filterbtn[data-f]').forEach(function(x){x.classList.toggle('active',x.dataset.f===filterMode);});renderBets();});});
function updateSortBtns(){document.querySelectorAll('.filterbtn[data-s]').forEach(function(x){const base=x.dataset.s==='payout'?'Payout':'Legs';const on=x.dataset.s===betSort;x.classList.toggle('active',on);x.textContent=base+(on?(betSortDir==='desc'?' \u2193':' \u2191'):'');});}
document.querySelectorAll('.filterbtn[data-s]').forEach(function(b){b.addEventListener('click',function(){if(betSort===b.dataset.s){betSortDir=(betSortDir==='desc'?'asc':'desc');}else{betSort=b.dataset.s;betSortDir='desc';}updateSortBtns();renderBets();});});
document.querySelectorAll('.filterbtn[data-pf]').forEach(function(b){b.addEventListener('click',function(){pitchFilter=b.dataset.pf;document.querySelectorAll('.filterbtn[data-pf]').forEach(function(x){x.classList.toggle('active',x.dataset.pf===pitchFilter);});renderPitchers();});});
updateSortBtns();
$('refresh').addEventListener('click',refresh);
refresh();setInterval(refresh,60000);
</script></body></html>"""
out = TPL.replace("__GAMES__", json.dumps(GAMES)).replace("__PLAYERS__", json.dumps(players)).replace("__PITCHERS__", json.dumps(pitchers)).replace("__BETS__", json.dumps(bets))
open(r"C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker\index.html","w",encoding="utf-8").write(out)
print("wrote index.html bytes:", len(out), "| bets:", len(bets), "| players:", len(players), "| pitchers:", len(pitchers))
