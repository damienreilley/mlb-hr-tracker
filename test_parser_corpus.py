import os, re, glob, subprocess, sys
R=r"C:\Users\damie\OneDrive\1-Sports-Fantasy-Betting\betting\Claude\mlb-hr-tracker"
PY=sys.executable
pastes=sorted(glob.glob(os.path.join(R,"_paste_*.txt")), key=os.path.getmtime)
print("%-34s %6s %5s %6s  %s" % ("paste","bets","legs","flags","note"))
for p in pastes:
    out=os.path.join(R,"_tp_out.json")
    pr=subprocess.run([PY, os.path.join(R,"parse_fanduel.py"), p, out], capture_output=True, text=True, cwd=R)
    s=pr.stdout
    mb=re.search(r"PARSED bets=(\d+) legs=(\d+)", s)
    bets=mb.group(1) if mb else "ERR"; legs=mb.group(2) if mb else "-"
    mf=re.search(r"FLAGS \((\d+)\)", s)
    flags=mf.group(1) if mf else ("0" if "FLAGS: none" in s else "?")
    note=""
    if pr.returncode!=0: note="CRASH: "+(pr.stderr.strip()[-80:])
    elif "COLLAPSED" in open(p,encoding="utf-8",errors="replace").read()[:80] or p.endswith("0624C.txt"):
        note="(collapsed view - parser reads expanded; flags expected)"
    print("%-34s %6s %5s %6s  %s" % (os.path.basename(p), bets, legs, flags, note))
try: os.remove(out)
except: pass
