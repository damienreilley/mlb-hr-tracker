# DEPLOY-RUNBOOK.md
Deploy the add_bet MCP server to Vercel and connect it to Claude.

Status: ready to run. Companion to PHONE-ADD-BET-DESIGN.md. Created 2026-06-18.
Auth = NO-AUTH MVP (design section 9). OAuth 2.1 = fast-follow (Step 6).

## WHO DOES WHAT
- Damien (manual, cannot be automated): create the GitHub token, the Vercel project, set the secret
  env var, add the connector URL on claude.ai. Secrets never pass through Claude.
- Claude (via the Vercel connector, once the FULL connector is active in a desktop chat): trigger
  redeploys, read build/runtime logs, fetch the deployment URL, help debug. (Note: a chat may expose
  only a subset of Vercel tools; the deploy/logs tools must be present for Claude's part.)

## WHAT GETS DEPLOYED   (this folder: add-bet-server/)
  api/server.py        - the MCP server (tool: add_bet) + GitHub Contents API read/append/commit
  add_bet_core.py      - parse + flag-gate + dedup + date-check  (LOCALLY TESTED, 4/4)
  requirements.txt     - mcp
  vercel.json          - clean /mcp endpoint
The server imports the repo's parse_fanduel.py (single source of truth); it must be BUNDLED with the
function at deploy (see the Step 2 bundling note).

## STEP 1 - GitHub fine-grained PAT   [Damien]
GitHub > Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate.
  - Token name: mlb-hr-tracker-add-bet
  - Resource owner: damienreilley
  - Expiration: No expiration is fine here - the token is scoped to only this repo's Contents, so the worst case is write access to mlb-hr-tracker until you revoke it. (Or pick a duration like 90 days and rotate when it lapses.) Revoke/regenerate anytime from the same settings page.
  - Repository access: Only select repositories > damienreilley/mlb-hr-tracker
  - Permissions > Repository permissions > Contents: Read and write   (the ONLY permission needed)
  - Generate, then COPY the token (shown once).
SECRET HANDLING: paste this token ONLY into the Vercel env var field in Step 2. Never commit it,
never paste it into this chat, never share it with Claude. If it ever leaks, revoke + regenerate.

## STEP 2 - Vercel project   [Damien]
vercel.com > Add New > Project > Import Git Repository > damienreilley/mlb-hr-tracker.
  - Root Directory: add-bet-server
  - Framework Preset: Other
  - Environment Variables: add  GITHUB_TOKEN = <the PAT from Step 1>
  - (optional, only if a default is wrong) GH_REPO=damienreilley/mlb-hr-tracker,
    STAGING_PATH=staging.json, GH_BRANCH=main
  - Deploy.

  BUNDLING NOTE (the one technical unknown - we verify via build logs):
  The function needs parse_fanduel.py (repo root) AND add_bet_core.py bundled with it. Because Root
  Directory is add-bet-server, the repo-root parse_fanduel.py is one level up. To bundle it, set the
  Vercel Install Command to copy it in first:
      cp ../parse_fanduel.py ./parse_fanduel.py && pip install -r requirements.txt
  (Vercel checks out the whole repo, so ../ is available at build time.) The build-time copy is
  gitignored (add-bet-server/.gitignore) so only ONE parser lives in git.
  If the first build shows an import error for parse_fanduel or add_bet_core, that is the thing to fix
  here - Claude reads the build logs via the Vercel connector and adjusts (e.g. an includeFiles entry
  in vercel.json, or the copy step).

## STEP 3 - Verify the deploy   [Claude, via Vercel connector]
Once deployed, in a desktop chat with the full Vercel connector active, Claude will:
  - Get deployment build logs  -> confirm the build + pip install + the parser copy succeeded
  - Get access to vercel url   -> capture the production URL (e.g. https://<project>.vercel.app)
  - Get runtime logs           -> watch the first tool call
The MCP endpoint will be:  https://<project>.vercel.app/mcp

## STEP 4 - Add the connector on claude.ai   [Damien]
claude.ai > Settings > Connectors > Add custom connector.
  - Name: MLB Tracker - Add Bet
  - URL:  https://<project>.vercel.app/mcp   (from Step 3)
  - Auth: none (leave the OAuth Client ID / Secret fields blank)
  - Add. It syncs to the mobile app, so the add_bet tool becomes usable from the phone.

## STEP 5 - End-to-end test   [together]
From the phone (or desktop), send a screenshot of a placed bet and let it flow:
  transcribe -> add_bet -> parser gate -> append staging.json -> Action builds -> live -> receipt.
Confirm the bet appears on https://damienreilley.github.io/mlb-hr-tracker/ and the receipt matches.
Test the GATE too: a deliberately garbled shot (drop a leg) should HALT with flags and NOT publish.

## STEP 6 - OAuth 2.1 hardening   [fast-follow, after the MVP works]
Replace no-auth with OAuth 2.1 (DCR + PKCE) so the endpoint is not openly writable. See design
section 9; Vercel's mcp-handler or an external IdP (Auth0) can provide it. Until then the endpoint is
write-only to a public fun tracker (accepted MVP risk).

## SAFETY / ROLLBACK
- The server only ever APPENDS to staging.json (dedup by id) and commits; it never deletes.
- A new-day bet HALTS (date_mismatch) rather than crossing days - run the daily rollover first
  (DAILY-ROLLOVER-RUNBOOK.md), then re-send.
- To disable instantly: remove the connector on claude.ai, or pause/delete the Vercel project. The
  tracker keeps working (Pages + the paste pipeline are independent of this).
- Revoke the GitHub PAT any time to cut write access.

## ENTRYPOINT CAVEAT
api/server.py ends with `app = mcp.streamable_http_app()`. If the deployed build cannot serve the MCP
handshake, verify that export against the current Python-MCP-on-Vercel boilerplate (sdiehl/mcp-on-vercel
or Vercel's MCP template) - the method name / ASGI export can differ by mcp SDK version. Claude reads
the runtime logs via the connector and adjusts.
