"""add_bet_core.py - pure logic for the phone add_bet pipeline.

Imports the REPO's parse_fanduel.py (single source of truth) - no reimplementation.
This module does NO network/disk I/O for the bet write; the Vercel handler supplies
the current staging dict and persists the returned one. That keeps this core unit-testable.

process(text, staging) is the entry point:
  - parse text with parse_fanduel.py
  - GATE: if the parser raises ANY flag -> ok=False (do not publish)
  - DATE CHECK: bet's PLACED date must match staging date (else rollover needed)
  - DEDUP: skip a bet whose #id is already in staging
  - return the (mutated) staging + a receipt
"""
import json, re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)            # add-bet-server/ sits inside the repo root
if REPO not in sys.path:
    sys.path.insert(0, REPO)
import parse_fanduel as P               # noqa: E402  (path set above)


def parse_text(text):
    """Run the repo parser over raw text. Returns (bets, flags)."""
    lines = [l.strip() for l in text.splitlines() if l.strip() != ""]
    bets, flags = [], []
    for blk in P.split_blocks(lines):
        bet, fl = P.parse_bet(blk)
        if bet:
            bets.append(bet)
        flags += fl
    return bets, flags


_DATE_RE = re.compile(r"PLACED:\s*(\d{1,2})/(\d{1,2})/(\d{4})")
def bet_date_from_text(text):
    m = _DATE_RE.search(text)
    if not m:
        return None
    mo, d, y = m.groups()
    return "%04d-%02d-%02d" % (int(y), int(mo), int(d))


def add_bets(staging, bets, bet_date=None):
    """Append bets to staging['bets'], dedup by id, honor the staging date.
    Returns (staging, summary). Mutates the staging dict in place."""
    existing = {b["id"] for b in staging.get("bets", [])}
    added, skipped, date_flags = [], [], []
    sdate = staging.get("date")
    for b in bets:
        if bet_date and sdate and bet_date != sdate:
            date_flags.append((b["id"], "placed date %s != staging date %s (rollover needed first)" % (bet_date, sdate)))
            continue
        if b["id"] in existing:
            skipped.append(b["id"])
        else:
            staging.setdefault("bets", []).append(b)
            existing.add(b["id"])
            added.append(b["id"])
    return staging, {"added": added, "skipped_dup": skipped, "date_flags": date_flags}


def process(text, staging):
    """Full add_bet pipeline against an in-memory staging dict.
    Returns a result dict; on ok=True, result['staging'] is the new staging to persist."""
    bets, flags = parse_text(text)
    if flags:
        return {"ok": False, "reason": "parser_flags",
                "flags": ["%s | %s" % (m, c) for m, c in flags],
                "parsed_ids": [b["id"] for b in bets]}
    if not bets:
        return {"ok": False, "reason": "no_bets", "flags": ["no bet parsed from text"]}
    bd = bet_date_from_text(text)
    staging, summ = add_bets(staging, bets, bd)
    if summ["date_flags"]:
        return {"ok": False, "reason": "date_mismatch",
                "flags": ["%s | %s" % (i, m) for i, m in summ["date_flags"]]}
    receipt = [{"id": b["id"], "kind": b["kind"], "legs": len(b["legs"]),
                "odds": b["odds"], "wager": b["wager"], "payout": b["payout"]}
               for b in bets if b["id"] in summ["added"]]
    return {"ok": True, "added": summ["added"], "skipped_dup": summ["skipped_dup"],
            "staging": staging, "receipt": receipt}
