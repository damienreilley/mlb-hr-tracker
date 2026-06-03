# -*- coding: utf-8 -*-
import json
GAMES = {
 "NYM@SEA":["Mets","Mariners"],"CWS@MIN":["White Sox","Twins"],"SD@PHI":["Padres","Phillies"],
 "BAL@BOS":["Orioles","Red Sox"],"KC@CIN":["Royals","Reds"],"SF@MIL":["Giants","Brewers"],
 "TEX@STL":["Rangers","Cardinals"],"ATH@CHC":["Athletics","Cubs"],"PIT@HOU":["Pirates","Astros"],
 "LAD@ARI":["Dodgers","Diamondbacks"],
}
players=[
 {"n":"Colson Montgomery","g":"CWS@MIN","pr":["HR"]},
 {"n":"Byron Buxton","g":"CWS@MIN","pr":["HR"]},
 {"n":"Juan Soto","g":"NYM@SEA","pr":["HR"]},
 {"n":"Kyle Schwarber","g":"SD@PHI","pr":["HR"]},
 {"n":"Bryce Harper","g":"SD@PHI","pr":["HR"]},
 {"n":"Brandon Marsh","g":"SD@PHI","pr":["HR"]},
 {"n":"Fernando Tatis Jr.","g":"SD@PHI","pr":["HR"]},
 {"n":"Pete Alonso","g":"BAL@BOS","pr":["HR"]},
 {"n":"Carter Jensen","g":"KC@CIN","pr":["HR"]},
 {"n":"Rafael Devers","g":"SF@MIL","pr":["HR"]},
 {"n":"Ezequiel Duran","g":"TEX@STL","pr":["HR"]},
 {"n":"Jake Burger","g":"TEX@STL","pr":["HR"]},
 {"n":"Shea Langeliers","g":"ATH@CHC","pr":["HR"]},
 {"n":"Christian Walker","g":"PIT@HOU","pr":["HR"]},
 {"n":"Yordan Alvarez","g":"PIT@HOU","pr":["HR"]},
 {"n":"Max Muncy","g":"LAD@ARI","pr":["HR"]},
 {"n":"Kyle Tucker","g":"LAD@ARI","pr":["HR"]},
 {"n":"Andy Pages","g":"LAD@ARI","pr":["HR","HIT"]},
 {"n":"Mookie Betts","g":"LAD@ARI","pr":["HIT"]},
 {"n":"Freddie Freeman","g":"LAD@ARI","pr":["HIT"]},
]
def H(p): return {"p":p,"prop":"HR"}
def T(p): return {"p":p,"prop":"HIT"}
bets=[
 {"id":"#4007","kind":"6-leg parlay","odds":3159870,"wager":0.10,"payout":3159.97,"placed":"1:56 PM","ts":1356,
  "legs":[H("Colson Montgomery"),H("Kyle Schwarber"),H("Pete Alonso"),H("Rafael Devers"),H("Ezequiel Duran"),H("Max Muncy")]},
 {"id":"#4008","kind":"6-leg SGP+","odds":5597508,"wager":0.10,"payout":5597.61,"placed":"1:57 PM","ts":1357,
  "legs":[H("Andy Pages"),H("Kyle Tucker"),H("Kyle Schwarber"),H("Pete Alonso"),H("Rafael Devers"),H("Ezequiel Duran")]},
 {"id":"#4006","kind":"6-leg SGP+","odds":9771167,"wager":0.10,"payout":9771.27,"placed":"1:53 PM","ts":1353,
  "legs":[H("Bryce Harper"),H("Brandon Marsh"),H("Fernando Tatis Jr."),H("Andy Pages"),H("Kyle Tucker"),H("Christian Walker")]},
 {"id":"#ts2w","kind":"6-leg SGP+","odds":143437,"wager":0.10,"payout":143.55,"placed":"1:52 PM","ts":1352,
  "legs":[H("Bryce Harper"),H("Brandon Marsh"),H("Yordan Alvarez"),H("Christian Walker"),T("Andy Pages"),T("Mookie Betts")]},
 {"id":"#4005","kind":"9-leg SGP+","odds":377869329,"wager":0.10,"payout":377869.43,"placed":"1:46 PM","ts":1346,
  "legs":[H("Ezequiel Duran"),H("Jake Burger"),H("Colson Montgomery"),H("Kyle Schwarber"),H("Pete Alonso"),H("Carter Jensen"),H("Rafael Devers"),H("Shea Langeliers"),H("Max Muncy")]},
 {"id":"#4004","kind":"10-leg SGP+","odds":720108740,"wager":0.13,"payout":936141.49,"placed":"1:44 PM","ts":1344,
  "legs":[H("Byron Buxton"),H("Colson Montgomery"),H("Juan Soto"),H("Bryce Harper"),H("Pete Alonso"),H("Carter Jensen"),H("Rafael Devers"),H("Jake Burger"),H("Shea Langeliers"),H("Max Muncy")]},
 {"id":"#nm3","kind":"5-leg SGP+","odds":341459,"wager":0.25,"payout":853.92,"placed":"1:32 PM","ts":1332,
  "legs":[H("Kyle Schwarber"),H("Fernando Tatis Jr."),H("Byron Buxton"),H("Carter Jensen"),H("Christian Walker")]},
 {"id":"#cfx","kind":"4-leg parlay","odds":14497,"wager":0.25,"payout":36.49,"placed":"1:31 PM","ts":1331.1,
  "legs":[H("Byron Buxton"),H("Bryce Harper"),H("Carter Jensen"),T("Andy Pages")]},
 {"id":"#d09e","kind":"4-leg parlay","odds":23460,"wager":0.25,"payout":58.90,"placed":"1:31 PM","ts":1331.0,
  "legs":[H("Byron Buxton"),H("Brandon Marsh"),H("Carter Jensen"),T("Andy Pages")]},
 {"id":"#4003","kind":"6-leg SGP+","odds":3904708,"wager":0.10,"payout":3904.81,"placed":"1:29 PM","ts":1329,
  "legs":[H("Bryce Harper"),H("Fernando Tatis Jr."),H("Byron Buxton"),H("Carter Jensen"),H("Christian Walker"),H("Kyle Tucker")]},
 {"id":"#4002","kind":"7-leg SGP+","odds":32787353,"wager":0.10,"payout":32787.45,"placed":"1:28 PM","ts":1328.1,
  "legs":[H("Bryce Harper"),H("Brandon Marsh"),H("Fernando Tatis Jr."),H("Byron Buxton"),H("Carter Jensen"),H("Christian Walker"),H("Kyle Tucker")]},
 {"id":"#4001","kind":"8-leg SGP+","odds":192128924,"wager":0.10,"payout":192129.02,"placed":"1:28 PM","ts":1328.0,
  "legs":[H("Bryce Harper"),H("Brandon Marsh"),H("Fernando Tatis Jr."),H("Andy Pages"),H("Kyle Tucker"),H("Byron Buxton"),H("Carter Jensen"),H("Christian Walker")]},
 {"id":"#d9q","kind":"7-leg SGP+","odds":559291,"wager":0.10,"payout":559.43,"placed":"1:24 PM","ts":1324,
  "legs":[H("Bryce Harper"),H("Brandon Marsh"),T("Andy Pages"),T("Mookie Betts"),H("Byron Buxton"),H("Carter Jensen"),H("Yordan Alvarez")]},
 {"id":"#4000","kind":"9-leg SGP+","odds":3468177,"wager":0.10,"payout":3468.28,"placed":"1:23 PM","ts":1323,
  "legs":[H("Bryce Harper"),H("Brandon Marsh"),H("Yordan Alvarez"),H("Christian Walker"),T("Freddie Freeman"),T("Andy Pages"),T("Mookie Betts"),H("Byron Buxton"),H("Carter Jensen")]},
]
TPL = r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HR Bet Tracker - June 3 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@800;900&family=Spline+Sans+Mono:wght@500;700&family=Spline+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0e0c;--panel:#111714;--panel2:#161e1a;--line:#243029;--ink:#e8efe9;--dim:#8aa093;--grn:#39e07b;--amber:#f5b342;--red:#ff5d5d;--blue:#5db0ff;--live:#ff4d4d}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(1200px 600px at 50% -10%,#13201a,var(--bg) 60%);color:var(--ink);font-family:'Spline Sans',sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1100px;margin:0 auto;padding:16px 13px 70px}
.kicker{font-family:'Spline Sans Mono';color:var(--grn);font-weight:700;letter-spacing:.18em;font-size:11px;text-transform:uppercase}
h1{font-family:'Archivo';font-weight:900;font-size:clamp(24px,6vw,40px);line-height:.95;margin:3px 0;letter-spacing:-.01em}
.bar{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin:12px 0;padding:11px 14px;background:var(--panel);border:1px solid var(--line);border-radius:12px}
.stat{font-family:'Spline Sans Mono';font-size:13px;color:var(--dim)}.stat b{font-family:'Archivo';font-size:20px;margin-right:4px}
.stat.a b{color:var(--grn)}.stat.d b{color:var(--red)}.stat.h b{color:var(--amber)}.stat.l b{color:var(--blue)}
.upd{font-family:'Spline Sans Mono';font-size:11.5px;color:var(--dim);margin-left:auto}
.btn{font-family:'Spline Sans Mono';font-weight:700;background:var(--grn);color:#04140a;border:0;padding:8px 14px;border-radius:9px;cursor:pointer;font-size:13px}
h2{font-family:'Archivo';font-weight:900;font-size:18px;letter-spacing:.02em;margin:26px 0 4px;padding-top:14px;border-top:1px solid var(--line)}
.muted{font-family:'Spline Sans Mono';font-size:11px;color:var(--dim)}
.tot{display:flex;gap:7px;flex-wrap:wrap;margin:8px 0 4px}
.hrpill{font-family:'Spline Sans Mono';font-size:12px;background:#0c1a12;border:1px solid #1d3a28;color:var(--grn);padding:5px 10px;border-radius:20px;font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:11px}
.game{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:13px;overflow:hidden}
.g-head{display:flex;justify-content:space-between;align-items:center;padding:9px 12px;background:#0e1512;border-bottom:1px solid var(--line)}
.g-match{font-weight:600;font-size:13px}.g-score{font-family:'Spline Sans Mono';color:var(--dim)}
.g-state{font-family:'Spline Sans Mono';font-size:11px;padding:3px 8px;border-radius:7px;font-weight:700;white-space:nowrap}
.s-live{background:#2a0f0f;color:var(--live);border:1px solid #4a1d1d}.s-final{background:#1a1f1c;color:var(--dim);border:1px solid var(--line)}.s-prev{background:#10243a;color:var(--blue);border:1px solid #1d3550}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--live);margin-right:5px;animation:p 1.1s infinite}@keyframes p{0%,100%{opacity:1}50%{opacity:.25}}
.plist{padding:4px 12px 10px}
.prow{display:flex;align-items:center;gap:8px;padding:7px 2px;border-bottom:1px solid #1a221d}.prow:last-child{border-bottom:0}
.prow.hit{background:linear-gradient(90deg,rgba(57,224,123,.16),transparent);border-radius:8px}
.mk{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;flex:none;border:1px solid var(--line);background:#0e1512;color:var(--dim)}
.mk.hit{background:var(--grn);color:#04140a;border-color:var(--grn);font-weight:900}
.pn{font-weight:600;font-size:13.5px;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pn.hit{color:var(--grn)}
.abtag{font-family:'Spline Sans Mono';font-size:9px;font-weight:700;padding:2px 6px;border-radius:5px;white-space:nowrap;flex:none}
.abtag.ab{background:#3a2a0a;color:var(--amber);border:1px solid #5a4310;animation:p 1.3s infinite}
.abtag.od{background:#10243a;color:var(--blue);border:1px solid #1d3550}
.hrbadge{font-family:'Spline Sans Mono';font-size:11.5px;font-weight:700;color:#04140a;background:var(--grn);padding:2px 8px;border-radius:20px;white-space:nowrap;box-shadow:0 0 10px rgba(57,224,123,.45)}
.hitbadge{font-family:'Spline Sans Mono';font-size:11px;font-weight:700;color:#04140a;background:var(--blue);padding:2px 8px;border-radius:20px;white-space:nowrap}
.sortbar{display:flex;gap:7px;align-items:center;flex-wrap:wrap;margin:6px 0 12px}
.sortbtn,.filterbtn{font-family:'Spline Sans Mono';font-weight:700;background:var(--panel2);border:1px solid var(--line);color:var(--ink);padding:6px 11px;border-radius:9px;cursor:pointer;font-size:12px}
.sortbtn.active{background:var(--grn);color:#04140a;border-color:var(--grn)}
.filterbtn.active{background:var(--blue);color:#04140a;border-color:var(--blue)}
.bet{background:linear-gradient(180deg,var(--panel2),var(--panel));border:1px solid var(--line);border-radius:13px;overflow:hidden}
.bet.b-dead{opacity:.6}.bet.b-won{border-color:var(--grn)}
.b-head{display:flex;justify-content:space-between;align-items:flex-start;gap:8px;padding:10px 12px;background:#0e1512;border-bottom:1px dashed var(--line)}
.b-kind{font-family:'Archivo';font-weight:800;font-size:13px}.b-id{font-family:'Spline Sans Mono';font-size:10px;color:var(--dim)}
.b-meta{font-family:'Spline Sans Mono';font-size:10.5px;color:var(--dim);margin-top:2px}.b-meta b{color:var(--ink)}
.b-stat{font-family:'Spline Sans Mono';font-weight:700;font-size:11px;padding:3px 8px;border-radius:7px;white-space:nowrap}
.b-stat.b-alive{background:#10243a;color:var(--blue);border:1px solid #1d3550}
.b-stat.b-dead{background:#2a0f0f;color:var(--red);border:1px solid #4a1d1d}
.b-stat.b-won{background:#0c2e1a;color:var(--grn);border:1px solid #1d3a28}
.b-legs{padding:5px 12px 10px;display:flex;flex-direction:column;gap:1px}
.leg{display:flex;align-items:center;gap:8px;padding:5px 2px;font-size:12.5px}
.lmk{width:17px;text-align:center;font-weight:900;flex:none}
.l-hit .lmk{color:var(--grn)}.l-hit .lname{color:var(--grn);font-weight:600}
.l-miss .lmk{color:var(--red)}.l-miss .lname{text-decoration:line-through;color:var(--dim)}
.l-pend .lmk{color:var(--dim)}
.l-pend.ab .lname{color:var(--amber)}
.lname{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lprop{font-family:'Spline Sans Mono';font-size:10.5px;color:var(--dim);white-space:nowrap}
.labtag{font-family:'Spline Sans Mono';font-size:8.5px;font-weight:700;padding:1px 5px;border-radius:4px;flex:none}
.labtag.ab{background:#3a2a0a;color:var(--amber)}.labtag.od{background:#10243a;color:var(--blue)}
footer{margin-top:26px;padding-top:14px;border-top:1px solid var(--line);color:var(--dim);font-size:11px;line-height:1.6;font-family:'Spline Sans Mono'}
</style></head><body><div class="wrap">
<div class="kicker">Live Bet Tracker</div>
<h1>Wednesday, June 3 - HR Bets</h1>
<div class="bar">
 <div class="stat a"><b id="betsalive">0</b>bets alive</div>
 <div class="stat d"><b id="betsdead">0</b>dead</div>
 <div class="stat h"><b id="hrcount">0</b>players homered</div>
 <div class="stat l"><b id="livecount">0</b>games live</div>
 <div class="upd" id="updated">Loading...</div>
 <button class="btn" id="refresh">Refresh</button>
</div>
<div class="tot" id="hrpills"></div>
<h2>Players</h2>
<div id="players"><p class="muted">Connecting to MLB live feed...</p></div>
<h2>Your Bets</h2>
<div class="sortbar"><span class="muted">Sort:</span>
 <button class="sortbtn active" data-m="odds">Odds</button>
 <button class="sortbtn" data-m="time">Placed</button>
 <button class="sortbtn" data-m="legs">Legs</button>
 <span class="muted" style="margin-left:8px">Show:</span>
 <button class="filterbtn active" data-f="all">All</button>
 <button class="filterbtn" data-f="alive">Alive</button>
 <button class="filterbtn" data-f="dead">Dead</button>
 <button class="filterbtn" data-f="won">Cashed</button></div>
<div id="bets"></div>
<footer>Auto-refreshes every 30s while open (polls statsapi.mlb.com from your browser; not a push alert; stops when the tab closes). AT BAT / ON DECK may lag the live game by a few seconds. HR/Hit matched by batter name; a bet goes DEAD when any leg's game ends without hitting. Confirm official results on FanDuel.</footer>
</div>
<script>
const DATE="2026-06-03";
const SCHED="https://statsapi.mlb.com/api/v1/schedule?sportId=1&date="+DATE+"&hydrate=linescore,team";
const FEED=function(pk){return "https://statsapi.mlb.com/api/v1.1/game/"+pk+"/feed/live";};
const GAMES=__GAMES__;
const players=__PLAYERS__;
const bets=__BETS__;
const norm=function(s){return (s||"").normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z ]/g,'').replace(/\s+/g,' ').trim();};
players.forEach(function(p){p.k=norm(p.n);p.hr=[];p.hit=false;p.atbat=false;p.ondeck=false;});
const pByKey={};players.forEach(function(p){pByKey[p.k]=p;});
let sortMode='odds';let filterMode='all';let GS={};
const $=function(id){return document.getElementById(id);};
async function gj(u){const r=await fetch(u,{cache:'no-store'});if(!r.ok)throw new Error('HTTP '+r.status);return r.json();}
function ordSuffix(n){if(n%10==1&&n%100!=11)return n+'st';if(n%10==2&&n%100!=12)return n+'nd';if(n%10==3&&n%100!=13)return n+'rd';return n+'th';}
function etTime(iso){try{return new Date(iso).toLocaleTimeString('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit'})+' ET';}catch(e){return '';}}
function amStr(o){return (o>0?'+':'')+o.toLocaleString();}
async function refresh(){
 $('updated').textContent='Updating...';
 let sched;try{sched=await gj(SCHED);}catch(e){$('updated').textContent="Can't reach MLB feed - retrying";return;}
 const allGames=(sched.dates&&sched.dates[0]&&sched.dates[0].games)?sched.dates[0].games:[];
 players.forEach(function(p){p.hr=[];p.hit=false;p.atbat=false;p.ondeck=false;});GS={};
 const keyToGame={};
 for(const key in GAMES){const a=GAMES[key][0],b=GAMES[key][1];
  const g=allGames.find(function(x){const an=x.teams.away.team.name,hn=x.teams.home.team.name;return (an.includes(a)||hn.includes(a))&&(an.includes(b)||hn.includes(b));});
  if(g)keyToGame[key]=g;}
 const careGames={};for(const key in keyToGame){careGames[keyToGame[key].gamePk]=keyToGame[key];}
 let live=0;const feedByPk={};
 for(const pk in careGames){const g=careGames[pk];const st=g.status.abstractGameState;if(st==='Live')live++;
  if(st==='Live'||st==='Final'){try{feedByPk[pk]=await gj(FEED(pk));}catch(e){feedByPk[pk]={__err:true};}}}
 for(const pk in feedByPk){const f=feedByPk[pk];if(f.__err)continue;
  const plays=(f.liveData&&f.liveData.plays&&f.liveData.plays.allPlays)?f.liveData.plays.allPlays:[];
  for(const pl of plays){const ev=pl.result&&pl.result.eventType;if(!ev)continue;
   const bk=norm(pl.matchup&&pl.matchup.batter?pl.matchup.batter.fullName:'');const pp=pByKey[bk];if(!pp)continue;
   if(ev==='home_run'){pp.hr.push(pl.about&&pl.about.inning?pl.about.inning:'?');}
   if(ev==='single'||ev==='double'||ev==='triple'||ev==='home_run'){pp.hit=true;}}
  const off=f.liveData&&f.liveData.linescore&&f.liveData.linescore.offense;
  if(off){const ab=off.batter&&off.batter.fullName?norm(off.batter.fullName):'';const od=off.onDeck&&off.onDeck.fullName?norm(off.onDeck.fullName):'';
   if(pByKey[ab])pByKey[ab].atbat=true;if(pByKey[od])pByKey[od].ondeck=true;}}
 for(const key in GAMES){const g=keyToGame[key];
  if(!g){GS[key]={state:'NA'};continue;}
  const ls=g.linescore||{};const st=g.status.abstractGameState;
  GS[key]={state:st,detail:g.status.detailedState,inn:ls.currentInning,ord:ls.currentInningOrdinal,half:ls.inningState,
   as:(ls.teams&&ls.teams.away&&ls.teams.away.runs!=null)?ls.teams.away.runs:g.teams.away.score,
   hs:(ls.teams&&ls.teams.home&&ls.teams.home.runs!=null)?ls.teams.home.runs:g.teams.home.score,
   time:g.gameDate};}
 renderPlayers(live);renderBets();
 $('updated').textContent='Updated '+new Date().toLocaleTimeString('en-US',{timeZone:'America/New_York',hour:'numeric',minute:'2-digit',second:'2-digit'})+' ET';
}
function legMet(leg){const p=pByKey[norm(leg.p)];if(!p)return 'pending';const met=leg.prop==='HR'?p.hr.length>0:p.hit;if(met)return 'hit';const gs=GS[p.g];if(gs&&gs.state==='Final')return 'miss';return 'pending';}
function betStatus(b){let hit=0,miss=0;for(const lg of b.legs){const s=legMet(lg);if(s==='hit')hit++;else if(s==='miss')miss++;}const st=miss>0?'dead':(hit===b.legs.length?'won':'alive');return {st:st,hit:hit,total:b.legs.length};}
function renderPlayers(live){
 const homered=players.filter(function(p){return p.hr.length>0;});
 $('hrcount').textContent=homered.length;$('livecount').textContent=live;
 $('hrpills').innerHTML=homered.length?homered.map(function(p){return '<span class="hrpill">&#9733; '+p.n+(p.hr.length>1?' x'+p.hr.length:'')+'</span>';}).join(''):'<span class="muted">No tracked player has homered yet.</span>';
 const order=Object.keys(GAMES);
 order.sort(function(A,B){
  const rk=function(key){const hr=players.some(function(p){return p.g===key&&p.hr.length>0;});if(hr)return 0;const s=GS[key]?GS[key].state:'NA';return s==='Live'?1:((s==='Preview'||s==='Pre-Game')?2:(s==='Final'?3:4));};
  return rk(A)-rk(B);});
 let html='<div class="grid">';
 for(const key of order){const ps=players.filter(function(p){return p.g===key;});if(!ps.length)continue;
  const gs=GS[key]||{};let badge,cls;
  if(gs.state==='Live'){cls='s-live';badge='<span class="dot"></span>'+(gs.half?gs.half+' ':'')+(gs.inn?ordSuffix(gs.inn):'');}
  else if(gs.state==='Final'){cls='s-final';badge=gs.detail||'Final';}
  else if(gs.state==='Preview'||gs.state==='Pre-Game'){cls='s-prev';badge=etTime(gs.time);}
  else{cls='s-prev';badge='--';}
  const showScore=(gs.state==='Live'||gs.state==='Final');
  const psort=ps.slice().sort(function(a,b){return (b.hr.length>0?1:0)-(a.hr.length>0?1:0);});
  let rows='';
  for(const p of psort){const homer=p.hr.length>0;const hasHit=p.pr.indexOf('HIT')>=0;
   let right;
   if(homer){right='<span class="hrbadge">&#128165; HR &middot; '+p.hr.map(function(i){return ordSuffix(i);}).join(', ')+'</span>';}
   else if(hasHit&&p.hit){right='<span class="hitbadge">&#10003; HIT</span>';}
   else{right='<span class="muted">'+(hasHit?'Hit/HR':'HR')+'</span>';}
   let abt='';if(!homer){if(p.atbat)abt='<span class="abtag ab">AT BAT</span>';else if(p.ondeck)abt='<span class="abtag od">ON DECK</span>';}
   const hc=(homer||(hasHit&&p.hit))?' hit':'';
   rows+='<div class="prow'+hc+'"><div class="mk'+(homer?' hit':'')+'">'+(homer?'&#9733;':'&middot;')+'</div><span class="pn'+(homer?' hit':'')+'">'+p.n+'</span>'+abt+right+'</div>';}
  html+='<div class="game"><div class="g-head"><div class="g-match">'+key.replace('@',' @ ')+(showScore&&gs.as!=null?'<span class="g-score"> &nbsp;'+gs.as+'-'+gs.hs+'</span>':'')+'</div><div class="g-state '+cls+'">'+badge+'</div></div><div class="plist">'+rows+'</div></div>';}
 html+='</div>';$('players').innerHTML=html;}
function renderBets(){
 let s=bets.slice();
 if(sortMode==='odds')s.sort(function(a,b){return b.odds-a.odds;});
 else if(sortMode==='time')s.sort(function(a,b){return b.ts-a.ts;});
 else s.sort(function(a,b){return (b.legs.length-a.legs.length)||(b.odds-a.odds);});
 let alive=0,dead=0;
 bets.forEach(function(b){const st=betStatus(b).st;if(st==='dead')dead++;else alive++;});
 $('betsalive').textContent=alive;$('betsdead').textContent=dead;
 let html='<div class="grid">';let shown=0;
 for(const b of s){const bs=betStatus(b);
  if(filterMode!=='all'&&bs.st!==filterMode)continue;shown++;
  const cl=bs.st==='dead'?'b-dead':(bs.st==='won'?'b-won':'b-alive');
  const lbl=bs.st==='dead'?'DEAD':(bs.st==='won'?'CASHED':'ALIVE');
  let legs='';
  for(const lg of b.legs){const st=legMet(lg);const p=pByKey[norm(lg.p)];
   const inn=(st==='hit'&&lg.prop==='HR'&&p&&p.hr.length)?(' '+ordSuffix(p.hr[0])):'';
   const mk=st==='hit'?'&#10003;':(st==='miss'?'&#10007;':'&middot;');
   let lc=st==='hit'?'l-hit':(st==='miss'?'l-miss':'l-pend');
   let lab='';if(st==='pend'||st==='pending'){if(p&&p.atbat){lab='<span class="labtag ab">AB</span>';}else if(p&&p.ondeck){lab='<span class="labtag od">OD</span>';}}
   legs+='<div class="leg '+lc+'"><span class="lmk">'+mk+'</span><span class="lname">'+lg.p+'</span>'+lab+'<span class="lprop">'+(lg.prop==='HR'?'HR'+inn:'Hit')+'</span></div>';}
  html+='<div class="bet '+cl+'"><div class="b-head"><div><span class="b-kind">'+b.kind+'</span> <span class="b-id">'+b.id+'</span><div class="b-meta">'+amStr(b.odds)+' &middot; $'+b.wager.toFixed(2)+' &rarr; <b>$'+b.payout.toLocaleString()+'</b> &middot; '+b.placed+'</div></div><span class="b-stat '+cl+'">'+lbl+' '+bs.hit+'/'+bs.total+'</span></div><div class="b-legs">'+legs+'</div></div>';}
 html+='</div>';if(!shown)html='<p class="muted">No bets match this filter.</p>';$('bets').innerHTML=html;}
document.querySelectorAll('.sortbtn').forEach(function(b){b.addEventListener('click',function(){sortMode=b.dataset.m;document.querySelectorAll('.sortbtn').forEach(function(x){x.classList.toggle('active',x.dataset.m===sortMode);});renderBets();});});
document.querySelectorAll('.filterbtn').forEach(function(b){b.addEventListener('click',function(){filterMode=b.dataset.f;document.querySelectorAll('.filterbtn').forEach(function(x){x.classList.toggle('active',x.dataset.f===filterMode);});renderBets();});});
$('refresh').addEventListener('click',refresh);
refresh();setInterval(refresh,30000);
</script></body></html>"""
out = TPL.replace("__GAMES__", json.dumps(GAMES)).replace("__PLAYERS__", json.dumps(players)).replace("__BETS__", json.dumps(bets))
open(r"C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker\index.html","w",encoding="utf-8").write(out)
print("wrote index.html bytes:", len(out), "| bets:", len(bets), "| players:", len(players))
