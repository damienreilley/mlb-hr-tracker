"""
api/server.py - Vercel-hosted remote MCP server exposing the add_bet tool.

DEPLOY-READY DRAFT. The add_bet_core pipeline this calls is LOCALLY TESTED
(see add-bet-server/test_add_bet_core.py). The GitHub Contents API I/O below is standard
but only fully exercised once a real GITHUB_TOKEN is set on Vercel. The FastMCP/Vercel
entrypoint (the `app` export at the bottom) must be verified against the current
Python-MCP-on-Vercel boilerplate at deploy time - see DEPLOY-RUNBOOK.md.

Auth: NONE (MVP) - see PHONE-ADD-BET-DESIGN.md section 9. OAuth 2.1 is the fast-follow.
"""
import os, sys, json, base64, urllib.request

# make add_bet_core (and, through it, the repo's parse_fanduel) importable
HERE = os.path.dirname(os.path.abspath(__file__))            # .../add-bet-server/api
sys.path.insert(0, os.path.dirname(HERE))                    # .../add-bet-server
import add_bet_core as C                                     # noqa: E402

REPO   = os.environ.get("GH_REPO", "damienreilley/mlb-hr-tracker")
PATH   = os.environ.get("STAGING_PATH", "staging.json")
BRANCH = os.environ.get("GH_BRANCH", "main")
LIVEURL = "https://damienreilley.github.io/mlb-hr-tracker/"
API = "https://api.github.com/repos/%s/contents/%s" % (REPO, PATH)

def _headers():
    tok = os.environ["GITHUB_TOKEN"]                         # set in Vercel env vars; never in repo
    return {"Authorization": "Bearer %s" % tok,
            "Accept": "application/vnd.github+json",
            "User-Agent": "mlb-hr-tracker-add-bet",
            "X-GitHub-Api-Version": "2022-11-28"}

def get_staging():
    req = urllib.request.Request(API + "?ref=" + BRANCH, headers=_headers())
    with urllib.request.urlopen(req, timeout=8) as r:
        j = json.loads(r.read().decode())
    staging = json.loads(base64.b64decode(j["content"]).decode("utf-8"))
    return staging, j["sha"]

def put_staging(staging, sha, message):
    body = json.dumps({
        "message": message,
        "content": base64.b64encode(json.dumps(staging, indent=2).encode("utf-8")).decode("ascii"),
        "sha": sha,
        "branch": BRANCH,
    }).encode("utf-8")
    req = urllib.request.Request(API, data=body, headers=_headers(), method="PUT")
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.loads(r.read().decode())

def add_bet_impl(text):
    """Fetch live staging, run the (tested) core, persist only if the parse is clean."""
    try:
        staging, sha = get_staging()
    except Exception as e:
        return {"ok": False, "reason": "github_read_error", "detail": str(e)}
    result = C.process(text, staging)
    if not result.get("ok"):
        return result                                        # flags / date_mismatch / no_bets: write nothing
    try:
        ids = ", ".join(result["added"]) or "(none)"
        put_staging(result["staging"], sha, "bets: add %s via phone add_bet" % ids)
    except Exception as e:
        return {"ok": False, "reason": "github_write_error", "detail": str(e)}
    out = {k: result[k] for k in ("ok", "added", "skipped_dup", "receipt")}
    out["url"] = LIVEURL
    return out

# --- MCP wiring (FastMCP / StreamableHTTP) ---
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("mlb-hr-tracker-add-bet")

@mcp.tool()
def add_bet(text: str) -> dict:
    """Add a placed FanDuel bet to Damien's live MLB tracker.

    `text` = the FanDuel open-bet text transcribed from the screenshot(s)
    (format in PHONE-ADD-BET-DESIGN.md section 5). The repo's parse_fanduel.py does all
    structuring; if it raises any flag the bet is NOT published and the flags are returned.

    Returns {ok:true, added, skipped_dup, receipt, url} on publish, or
    {ok:false, reason, flags} when the parser flagged the bet (nothing written)."""
    return add_bet_impl(text)

# Vercel serves this ASGI app. VERIFY this export against the current boilerplate at deploy
# (method name / entrypoint may differ by mcp SDK version) - see DEPLOY-RUNBOOK.md.
app = mcp.streamable_http_app()
