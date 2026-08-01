#!/usr/bin/env python3
# parse_fanduel.py v2 - FanDuel "Open Bets" paste -> staging bets[] (DRAFT).
# Deterministic event-walk. Tracks nearest inner SGP for game attribution.
# Handles batter props, ML, ALTK, TR, and tags rare un-graded props (F5/Race) as NA.
# Never guesses: unresolved game -> g:"??" + FLAG. Usage: python parse_fanduel.py <paste.txt> <out.json>
import sys, re, json

TEAM_NAME = {
 "Arizona Diamondbacks":"ARI","Atlanta Braves":"ATL","Baltimore Orioles":"BAL",
 "Boston Red Sox":"BOS","Chicago Cubs":"CHC","Chicago White Sox":"CWS",
 "Cincinnati Reds":"CIN","Cleveland Guardians":"CLE","Colorado Rockies":"COL",
 "Detroit Tigers":"DET","Houston Astros":"HOU","Kansas City Royals":"KC",
 "Los Angeles Angels":"LAA","Los Angeles Dodgers":"LAD","Miami Marlins":"MIA",
 "Milwaukee Brewers":"MIL","Minnesota Twins":"MIN","New York Mets":"NYM",
 "New York Yankees":"NYY","Athletics":"ATH","Philadelphia Phillies":"PHI",
 "Pittsburgh Pirates":"PIT","San Diego Padres":"SD","San Francisco Giants":"SF",
 "Seattle Mariners":"SEA","St. Louis Cardinals":"STL","Tampa Bay Rays":"TB",
 "Texas Rangers":"TEX","Toronto Blue Jays":"TOR","Washington Nationals":"WSH",
}
PROP_MAP = {
 "To Hit A Home Run":"HR","To Hit 2+ Home Runs":"HR2","To Hit A Single":"1B","To Hit A Double":"2B","To Hit A Triple":"3B",
 "To Record A Hit":"HIT","To Record 2+ Hits":"HIT2","To Record 3+ Hits":"HIT3","To Record 4+ Hits":"HIT4",
 "To Record A Stolen Base":"SB","To Record 2+ Stolen Bases":"SB2",
 "To Record An RBI":"RBI","To Record 2+ RBIs":"RBI2","To Record 3+ RBIs":"RBI3","To Record 4+ RBIs":"RBI4",
 "To Record A Run":"RUN","To Record 2+ Runs":"RUN2","To Record 3+ Runs":"RUN3",
 "To Record 2+ Total Bases":"TB2","To Record 3+ Total Bases":"TB3",
 "To Record 4+ Total Bases":"TB","To Record 5+ Total Bases":"TB5",
 "To Record 2+ Hits + Runs + RBIs":"HRR2","Player To Record 2+ Hits + Runs + RBIs":"HRR2","To Record 3+ Hits + Runs + RBIs":"HRR3","Player To Record 3+ Hits + Runs + RBIs":"HRR3",
 # First-plate-appearance HR (2026-07-29, Backlog #26). The ENGINE has graded FPA all
 # along (fpaDone/fpaHR off allPlays, label "1st-PA HR", own colour+category) - only the
 # parser phrase mapping was missing, so the leg was DROPPED and the bet held on a leg-count
 # mismatch. Both observed wordings mapped; CI lookup covers ALL-CAPS screenshot pastes.
 "Player to Hit a Home Run in First Plate Appearance":"FPA",
 "To Hit A Home Run in First Plate Appearance":"FPA",
}
PROP_MAP_CI = {k.lower(): v for k, v in PROP_MAP.items()}
def prop_code(ln):
    # exact match first (paste format), then case-insensitive (screenshot ALL-CAPS display)
    return PROP_MAP[ln] if ln in PROP_MAP else PROP_MAP_CI.get(ln.lower())
def pitcher_prop(t):
    if "No-Hitter Through 5" in t: return "NH5"
    if "No-Hitter Through 7" in t: return "NH7"
    if "No-Hitter Through 3" in t: return "NH3"
    if "3+ Strikeouts in the 1st Inning" in t: return "K1"
    if "9 up 9 down" in t.lower(): return "UP9"
    if "6 up 6 down" in t.lower(): return "UP6"
    return None
def strip_paren(s): return re.sub(r"\s*\([^()]*\)\s*$","",s).strip()
def paren_last(s):
    m=re.search(r"\(([^()]*)\)\s*$", s.strip())
    if not m: return ""
    parts=m.group(1).strip().split()
    return parts[-1].lower() if parts else ""
def team_code(s):
    if " @ " in s: return None
    key=strip_paren(s)
    c=TEAM_NAME.get(key)
    if c: return c
    # tolerant: FanDuel truncates team names in the expanded multi-SGP view
    # (e.g. "Kansas City Ro...") -> resolve only if a UNIQUE team name has this prefix.
    kc=key.rstrip(". ").strip()
    if len(kc)>=6:
        cands={v for name,v in TEAM_NAME.items() if name.startswith(kc)}
        if len(cands)==1: return next(iter(cands))
    return None
def mkid(fid):
    if fid.startswith("O/"): return "#"+str(int(fid.split("/")[-1]))
    return "#"+fid[-6:].lower()
def reformat_placed(s):
    s=s.replace(" ET","").strip()
    m=re.match(r"^(\d+)/(\d+)/\d+ (.+)$", s)
    return ("%s/%s %s"%(m.group(1),m.group(2),m.group(3))) if m else s
def is_header(ln):
    return bool(re.match(r"^\d+ leg ", ln)) or ln.startswith("Same Game Parlay") or pitcher_prop(ln) is not None
def _clean_side(s):
    # strip a trailing game-time and/or truncation ellipsis that FanDuel renders on the
    # matchup line in screenshots (e.g. "...(A Nola)  6:41PM ET" or "Kansas City Ro...").
    s=re.sub(r"\s+\d{1,2}:\d{2}\s*[ap]m\s*et\s*$","",s,flags=re.I)
    s=re.sub(r"\s*(?:\.\.\.|\u2026)\s*$","",s)
    s=re.sub(r"\s*\([^)]*$","",s)
    return s.strip()
def at_game(ln):
    if " @ " in ln:
        a,b=ln.split(" @ ",1)
        a=_clean_side(a); b=_clean_side(b)
        ca,cb=team_code(a),team_code(b)
        if ca and cb: return (ca+"@"+cb, paren_last(a), paren_last(b))
    return None
def find_home(lines,i,window=5):
    for j in range(i+1, min(i+1+window, len(lines))):
        c=team_code(lines[j])
        if c: return c, j
    return None, None
def prev_name(lines,i):
    j=i-1
    while j>=0 and (re.match(r"^[+-]\d+$", lines[j]) or lines[j]=="Void"): j-=1
    return lines[j] if j>=0 else "??"
def prev_team(lines,i):
    j=i-1
    while j>=0:
        if team_code(lines[j]): return lines[j].split(" (")[0].strip()
        if lines[j] not in ("Moneyline","Void") and not re.match(r"^[+-]\d+$", lines[j]) and lines[j]!="First 5 Innings Result": break
        j-=1
    return "??"
def money_before(lines,label):
    # Tolerant money reader for TOTAL WAGER / TOTAL PAYOUT. Finds the $amount
    # whether it is inline ("LABEL: $x"), directly ABOVE the label (FanDuel
    # native paste), or directly BELOW it (some phone/screenshot layouts). When
    # an amount sits on BOTH sides, the one sandwiched against the PARTNER label
    # belongs to that partner, so we take the other side. Case-insensitive.
    pat=r"\$\s*([\d,]+\.\d{2})"
    def val(s):
        m=re.search(pat,s); return float(m.group(1).replace(",","")) if m else None
    def is_lbl(s):
        s=s.lower(); return ("total wager" in s) or ("total payout" in s) or ("returned" in s)
    lab=label.lower(); n=len(lines)
    for i,ln in enumerate(lines):
        if lab in ln.lower():
            v=val(ln)
            if v is not None: return v
            above=val(lines[i-1]) if i>0 else None
            below=val(lines[i+1]) if i+1<n else None
            if above is not None and below is None: return above
            if below is not None and above is None: return below
            if above is not None and below is not None:
                if i+2<n and is_lbl(lines[i+2]): return above   # below belongs to partner
                if i-2>=0 and is_lbl(lines[i-2]): return below  # above belongs to partner
                return above
    return None
def is_selection_subject(lines,i):
    # True if this team line is a BET SELECTION subject (next meaningful line is Moneyline / a prop),
    # not the away side of a box-score matchup (which is followed by AB:/P:/lineup).
    j=i+1
    if j<len(lines) and re.match(r"^[+-]\d+$", lines[j]): j+=1
    if j>=len(lines): return False
    nx=lines[j]
    return nx=="Moneyline" or prop_code(nx) is not None or nx=="First 5 Innings Result" or bool(re.match(r"^Race To \d+ Runs$", nx))

def void_around(lines,lo,hi):
    # FanDuel marks a voided leg with a standalone 'Void' token where the leg odds go.
    # It sits immediately BEFORE the leg's first line (player/Void/prop) or immediately
    # AFTER the leg's last line (player/prop/Void). Either adjacency => the leg is void.
    n=len(lines)
    return (lo-1>=0 and lines[lo-1]=="Void") or (hi+1<n and lines[hi+1]=="Void")

def tokenize(lines):
    toks=[]; i=0; n=len(lines)
    while i<n:
        ln=lines[i]
        if ln.startswith("Same Game Parlay"):
            toks.append(("SGP",)); i+=1; continue
        g=at_game(ln)
        if g: toks.append(("MATCH",)+g); i+=1; continue
        m=re.match(r"^(.+?) (\d+)\+ Strikeouts$", ln)
        if m and i+1<n and lines[i+1].endswith("- Alt Strikeouts"):
            d={"p":m.group(1).strip(),"prop":"ALTK","k":int(m.group(2))}
            if void_around(lines,i,i+1): d["void"]=True
            toks.append(("LEG",d)); i+=2; continue
        m=re.match(r"^(Over|Under) (\d+(?:\.\d+)?)$", ln)
        if m:
            # The "Total Runs" label normally sits on the very next line, but when the
            # totals leg is a STANDALONE selection inside an SGP+ (not nested in an SGP)
            # FanDuel interposes that leg's own odds - and possibly a Void marker -
            # between the line and the label. Skip those. (2026-07-22, TRODDS)
            j=i+1; saw_void=False
            while j<n and (re.match(r"^[+-]\d+$", lines[j]) or lines[j]=="Void"):
                if lines[j]=="Void": saw_void=True
                j+=1
            if j<n and "Total Runs" in lines[j]:
                d={"p":"","prop":"TR","line":float(m.group(2)),"side":m.group(1).lower()}
                if saw_void or void_around(lines,i,j): d["void"]=True
                toks.append(("LEG",d)); i=j+1; continue
        mch=re.match(r"^Players To Combine For (?:A Home Run|(\d+)\+ Home Runs?)$", ln)
        mck=re.match(r"^Players To Combine For (\d+)\+ Hits$", ln)
        if mch or mck:
            j=i-1
            while j>=0 and (i-j)<=3 and (" & " not in lines[j] or " @ " in lines[j]): j-=1
            pair=lines[j] if (j>=0 and " & " in lines[j] and " @ " not in lines[j]) else prev_name(lines,i)
            ps=[x.strip() for x in pair.split(" & ")] if " & " in pair else [pair]
            if mch: d={"p":pair,"prop":"CMBHR","ps":ps,"line":int(mch.group(1)) if mch.group(1) else 1}
            else:   d={"p":pair,"prop":"CMBHIT","ps":ps,"line":int(mck.group(1))}
            if void_around(lines,i,i): d["void"]=True
            toks.append(("LEG",d)); i+=1; continue
        if ln.strip().lower()=="to hit first home run":
            # First-HR-of-game is not auto-gradable (needs cross-player HR ordering);
            # carry as a labeled manual/NA leg so the bet publishes and is tracked on FD.
            d={"p":prev_name(lines,i),"prop":"NA","txt":"First HR of game (manual/FD)"}
            if void_around(lines,i,i): d["void"]=True
            toks.append(("LEG",d)); i+=1; continue
        pc=prop_code(ln)
        if pc is not None:
            d={"p":prev_name(lines,i),"prop":pc}
            if void_around(lines,i,i): d["void"]=True
            toks.append(("LEG",d)); i+=1; continue
        if ln=="Moneyline":
            d={"p":prev_team(lines,i),"prop":"ML"}
            if void_around(lines,i,i): d["void"]=True
            toks.append(("LEG",d)); i+=1; continue
        if ln=="First 5 Innings Result":
            toks.append(("LEG",{"p":prev_team(lines,i),"prop":"NA","txt":"First 5 Innings Result"})); i+=1; continue
        if ln.strip().lower()=="correct score":
            # Correct Score (2026-07-23, Backlog #24): selection sits 1-3 lines back as
            # "<Team> H-A" (e.g. "Toronto Blue Jays 8-3"). No grader yet -> NA/manual,
            # same treatment as First 5 / Race To N. Was silently DROPPED before this.
            sel, j = None, i-1
            while j >= 0 and (i-j) <= 3:
                ms = re.match(r"^(.+?)\s+(\d+)-(\d+)$", lines[j].strip())
                if ms: sel = (ms.group(1).strip(), ms.group(2), ms.group(3)); break
                j -= 1
            if not sel:
                # No "<Team> H-A" selection nearby -> not an MLB correct-score single
                # (e.g. legacy soccer SGP legs). Emit nothing rather than invent a leg.
                i+=1; continue
            # CS leg carries the NAMED team + its runs first. This is NOT an assumption:
            # MLB has no draws, and a correct-score selection is labeled with the team that
            # achieves the HIGHER score ("Toronto Blue Jays 8-3" = TOR wins 8-3). A
            # "home-team-first" reading would label an away selection with the LOSING team's
            # name, which is incoherent - so named-team-first is the only consistent reading,
            # and it holds regardless of whether the named team is home or away.
            # Self-check below: if the named team is NOT the winner the premise is violated,
            # so flag rather than grade on a bad orientation.
            d = {"p": sel[0], "prop": "CS", "tm": team_code(sel[0]) or "",
                 "nr": int(sel[1]), "opp": int(sel[2])}
            if void_around(lines,i,i): d["void"]=True
            toks.append(("LEG",d)); i+=1; continue
        m=re.match(r"^Race To (\d+) Runs$", ln)
        if m:
            toks.append(("LEG",{"p":prev_team(lines,i),"prop":"NA","txt":"Race To %s Runs"%m.group(1)})); i+=1; continue
        if team_code(ln) and not is_selection_subject(lines,i):
            hc,hidx=find_home(lines,i)
            if hc: toks.append(("MATCH",team_code(ln)+"@"+hc,paren_last(ln),paren_last(lines[hidx]))); i=hidx+1; continue
        i+=1
    return toks

def parse_bet(lines):
    flags=[]
    full_id=next((l.split("BET ID:",1)[1].strip() for l in lines if l.startswith("BET ID:")), None)
    placed_raw=next((l.split("PLACED:",1)[1].strip() for l in lines if l.startswith("PLACED:")), "")
    if not full_id: return None,[("no BET ID in block",lines[0] if lines else "?")]
    header=lines[0]
    odds=None
    for l in lines[1:]:
        mm=re.search(r"(?<!\d)\+(\d{3,})(?!\d)",l)
        if mm: odds=int(mm.group(1)); break
    wager=money_before(lines,"TOTAL WAGER"); payout=money_before(lines,"TOTAL PAYOUT")
    # SETTLEMENT (2026-07-24, Backlog #25): a FanDuel-settled bet shows "RETURNED"
    # instead of "TOTAL PAYOUT" - the $ amount above it is what was returned
    # ($0.00 = lost, >0 = won/cashed). This is AUTHORITATIVE: honor FD's result
    # rather than re-deriving from live feeds (which may never mark every leg).
    settled=False; settled_won=None
    if any(re.match(r"^\s*RETURNED\s*$",l,re.I) for l in lines):
        settled=True
        ret=money_before(lines,"RETURNED")
        if ret is not None: payout=ret
        settled_won = (payout is not None and payout>0)
    m1=re.match(r"^(\d+) leg Same Game Parlay\+",header)
    m2=re.match(r"^(\d+) leg parlay",header)
    pp=pitcher_prop(header)
    toks=tokenize(lines)
    legs=[]; cur=None; cur_ap=""; cur_hp=""; expect=False
    for t in toks:
        if t[0]=="SGP": expect=True
        elif t[0]=="MATCH":
            g=t[1]; ap=t[2] if len(t)>2 else ""; hp=t[3] if len(t)>3 else ""
            if expect: cur=g; cur_ap=ap; cur_hp=hp; expect=False
            elif legs:
                legs[-1]["g"]=g
                if ap or hp: legs[-1]["asp"]=ap; legs[-1]["hsp"]=hp
                cur=g; cur_ap=ap; cur_hp=hp
            else: cur=g; cur_ap=ap; cur_hp=hp
        else:
            d=dict(t[1]); d["g"]=cur
            if cur_ap or cur_hp: d["asp"]=cur_ap; d["hsp"]=cur_hp
            legs.append(d)
    if pp is not None and not any(l.get("prop")==pp for l in legs):
        # Carry the MATCH token's starting pitchers (asp/hsp) onto the synthesized
        # pitcher-special leg. Without them a DOUBLEHEADER leg cannot be resolved to a
        # gamePk client-side and _lpk falls back to game 1 - wrong game, wrong grade.
        # Only bites when one game key maps to 2 gamePks. (2026-07-22, PSPK)
        mt=next((t for t in toks if t[0]=="MATCH"), None)
        gme=mt[1] if mt else None
        d={"p":header.split(" to ",1)[0].strip(),"prop":pp,"g":gme or "??"}
        if mt and len(mt)>3 and (mt[2] or mt[3]): d["asp"]=mt[2]; d["hsp"]=mt[3]
        legs=[d]
    for d in legs:
        if not d.get("g"):
            d["g"]="??"; flags.append(("no game for leg",d.get("p","?")))
        if d.get("prop")=="CS":
            # ORIENTATION IS STATED BY THE BET ITSELF: the selection reads
            # "<Team> <n>-<m>", which binds the NAMED team to the FIRST number
            # ("Toronto Blue Jays 8-3" = TOR 8, opponent 3). No convention to infer.
            # Note only (never blocks grading): the named team is normally the winner.
            if d.get("nr") is not None and d.get("opp") is not None and d["nr"] <= d["opp"]:
                flags.append(("note: CS names %s with the lower score (%s-%s) - grading per label, verify vs FD"%(d.get("tm"),d["nr"],d["opp"]),full_id))
            # Resolve NAMED-team runs -> canonical away/home runs using the matchup.
            g=d.get("g") or ""
            aw,hm=(g.split("@",1)+[""])[:2] if "@" in g else ("","")
            tm=d.get("tm") or ""
            if tm and tm==hm:   d["hs"]=d["nr"]; d["as"]=d["opp"]
            elif tm and tm==aw: d["as"]=d["nr"]; d["hs"]=d["opp"]
            else:
                d["prop"]="NA"; d["txt"]="Correct score %s %s-%s (team not in matchup - manual/FD)"%(tm or d.get("p"),d.get("nr"),d.get("opp"))
                flags.append(("CS team %r not in matchup %r - downgraded to manual"%(tm,g),full_id))
                continue
            d["lbl"]="%s %s-%s"%(tm,d["nr"],d["opp"])
            d["side"]="home" if tm==hm else "away"
    if m1: kind="%s-leg SGP+"%m1.group(1); expected=int(m1.group(1))
    elif m2: kind="%s-leg parlay"%m2.group(1); expected=int(m2.group(1))
    elif pp is not None: kind="Pitcher Special"; expected=1
    elif not any(t[0]=="SGP" for t in toks) and len(legs)==1:
        kind="Single"; expected=1   # straight single (Backlog #23); leg-count check now armed
    else:
        kind="%d-leg SGP"%len(legs)
        summ=next((l for l in lines[1:] if ", " in l and re.search(r"To (Hit|Record)|Strikeouts|Total Runs|Moneyline|Innings Result|Race To",l,re.I)), None)
        expected=len(summ.split(", ")) if summ else None
    if expected is not None and len(legs)!=expected:
        flags.append(("LEG COUNT MISMATCH header=%s parsed=%d (possible unexpanded bet)"%(expected,len(legs)),full_id))
    if not legs:
        # Safety net (2026-07-23): a bet with zero legs can never grade or display
        # meaningfully - always a parser miss. Fail loud instead of publishing a shell.
        flags.append(("ZERO LEGS parsed (unknown market/format)",full_id))
    for l in legs:
        if l.get("prop")=="NA": flags.append(("MANUAL leg (NA, not auto-graded): %s"%l.get("txt",""),full_id))
    bet={"full_id":full_id,"id":mkid(full_id),"kind":kind,"odds":odds,"wager":wager,
         "payout":payout,"placed":reformat_placed(placed_raw),"status":"open","legs":legs}
    if settled:
        bet["status"]="settled"
        bet["settled"]=True
        bet["result"]="won" if settled_won else "lost"
        flags.append(("SETTLED by FanDuel: %s (returned %s)"%("WON" if settled_won else "LOST", ("$%.2f"%payout) if payout is not None else "?"),full_id))
    return bet,flags

SINGLE_MARKETS = ("correct score",)   # market-label lines that stand in for a prop code

def single_start(b):
    # Straight-single fallback anchor (2026-07-18, Backlog #23): a plain single has
    # no is_header line (player / +odds / prop shape), so header-less blocks were
    # silently DROPPED before parse_bet - invisible to the GATE. Anchor at the
    # selection line: b[i+1] is bare +odds AND b[i+2] is a known prop OR a known
    # game-market label (Correct Score - added 2026-07-23, Backlog #24).
    for i in range(len(b)-2):
        if not re.fullmatch(r"\+\d+", b[i+1]): continue
        if prop_code(b[i+2]) is not None or b[i+2].strip().lower() in SINGLE_MARKETS:
            return i
    return None

# FUTURES (2026-08-01, Backlog #28). Long-dated markets - World Series exact
# result, pennant/division winners etc - settle months out (e.g. Nov 1) and have
# no same-day game, so the board's engine cannot grade them. Damien's decision
# 2026-08-01: EXCLUDE them from the board entirely.
# They must be excluded DELIBERATELY, not via the drop detector: an unrecognised
# block is supposed to HOLD the intake (#24), and futures would trip that hold
# every day. Recognising them here keeps the detector meaningful for genuinely
# new bet types while skipping futures quietly-but-visibly (see FUTURES_SKIPPED).
FUTURES_MARKERS = ("world series", "to win the", "pennant",
                   "division winner", "exact result")
FUTURES_SKIPPED = []   # populated per split_blocks_checked call, for reporting


def is_futures_block(b):
    """TRUE only when the block's MARKET LABEL says futures.

    The label sits in a fixed position: the line immediately AFTER the bare
    "+odds" line (e.g. "WORLD SERIES 2026 - EXACT RESULT"), or a standalone
    "MLB Futures <year>" line. Scanning the whole block for keywords was TOO
    GREEDY - on 2026-08-01 it swallowed bet #4435, a real $9.00 same-day SGP+
    with a $63k payout, because the file header contained Damien's note
    mentioning "world series". Position-anchored matching only.
    """
    for i, l in enumerate(b):
        s = l.strip().lower()
        if s.startswith("mlb futures"):
            return True
        if i > 0 and re.fullmatch(r"\+\d+", b[i-1].strip()):
            for m in FUTURES_MARKERS:
                if m in s:
                    return True
    return False


def split_blocks_checked(lines):
    """split_blocks + DROP DETECTOR (2026-07-23). Returns (blocks, dropped).
    'dropped' lists the BET IDs of blocks that carried a BET ID but matched no
    anchor, so an unknown bet type fails LOUD at the gate instead of vanishing -
    the structural hole behind Backlog #23 and #24. Futures blocks are excluded
    on purpose and recorded in FUTURES_SKIPPED rather than reported as dropped."""
    del FUTURES_SKIPPED[:]
    raw, cur = [], []
    for ln in lines:
        cur.append(ln)
        if ln.startswith("PLACED:"): raw.append(cur); cur=[]
    blocks, dropped = [], []
    for b in raw:
        bid = next((l.split("BET ID:",1)[1].strip() for l in b if l.startswith("BET ID:")), None)
        if is_futures_block(b):
            if bid: FUTURES_SKIPPED.append(bid)
            continue
        hi = next((i for i,l in enumerate(b) if is_header(l)), None)
        if hi is None: hi = single_start(b)
        if hi is not None:
            blocks.append(b[hi:])
        else:
            if bid: dropped.append(bid)
    return blocks, dropped

def split_blocks(lines):
    blocks=[]; cur=[]
    for ln in lines:
        cur.append(ln)
        if ln.startswith("PLACED:"): blocks.append(cur); cur=[]
    out=[]
    for b in blocks:
        hi=next((i for i,l in enumerate(b) if is_header(l)), None)
        if hi is None: hi=single_start(b)
        if hi is not None: out.append(b[hi:])
    return out

def main():
    paste,outp=sys.argv[1],sys.argv[2]
    raw=open(paste,encoding="utf-8").read().splitlines()
    lines=[l.strip() for l in raw if l.strip()!=""]
    bets=[]; allflags=[]
    blks, dropped = split_blocks_checked(lines)
    if FUTURES_SKIPPED:
        print("FUTURES SKIPPED (long-dated, not gradable - excluded by design): %d" % len(FUTURES_SKIPPED))
        for f in FUTURES_SKIPPED: print("   ", f)
    for fid in dropped:
        allflags.append(("UNPARSED BLOCK (unknown bet type - NOT on board, fix parser)", fid))
    for b in blks:
        bet,flags=parse_bet(b)
        if bet: bets.append(bet)
        allflags+=flags
    json.dump({"date":None,"bets":bets}, open(outp,"w",encoding="utf-8",newline="\n"), indent=2)
    ids=[x["id"] for x in bets]
    dups=sorted(set(i for i in ids if ids.count(i)>1))
    print("PARSED bets=%d legs=%d wager=$%.2f"%(len(bets),sum(len(x['legs']) for x in bets),sum((x['wager'] or 0) for x in bets)))
    print("DUP IDS:", dups or "none")
    miss=[x['id'] for x in bets if x['odds'] is None or x['wager'] is None or x['payout'] is None]
    print("MISSING odds/wager/payout:", miss or "none")
    qq=[(x['id'],l['p'],l['prop']) for x in bets for l in x['legs'] if l['g']=="??"]
    print("UNRESOLVED GAMES (g=??):", qq or "none")
    na=[(x['id'],l.get('p'),l.get('txt')) for x in bets for l in x['legs'] if l.get('prop')=="NA"]
    print("MANUAL/NA legs:", na or "none")
    if allflags:
        print("FLAGS (%d):"%len(allflags))
        for msg,ctx in allflags: print("  -",msg,"|",ctx)
    else:
        print("FLAGS: none")

if __name__=="__main__":
    main()
