# SOP: Jira MCP Server

## Purpose
Expose Jira ticket data to Claude Code via the Model Context Protocol (MCP).
Claude Code uses these tools to fetch ticket context and generate test plans + BDD test cases.

## Tools Exposed

### 1. `fetch_jira_ticket(ticket_id)`
**Input:** Jira ticket ID string (e.g. `"PROJ-1234"`)  
**Output:** JSON string containing:
- `ticket_id`, `summary`, `description`, `status`, `priority`
- `assignee`, `reporter`, `labels`, `components`
- `comments[]` — each with `author`, `created`, `body`
- `attachments[]` — each with `filename`, `mime_type`, `url`

**Logic:**
1. Load credentials from `.env`
2. Connect via `jira.JIRA(server=JIRA_URL, token_auth=JIRA_TOKEN)`
3. Call `jira.issue(ticket_id, expand='comments,attachments')`
4. Extract and serialize all fields
5. Return JSON

**Edge cases:**
- If `description` is `None` → return empty string `""`
- If `assignee` is `None` → return `"Unassigned"`
- If `priority` is `None` → return `"None"`
- Ticket not found → raise with clear message including ticket ID

---

### 2. `download_jira_attachment(ticket_id, filename, attachment_url)`
**Input:** ticket ID, filename, attachment URL (from `fetch_jira_ticket`)  
**Output:** MCP `Image` object (Claude sees it visually)

**Logic:**
1. `GET attachment_url` with `Authorization: Bearer <JIRA_TOKEN>` header
2. Save to `.tmp/<ticket_id>/<filename>`
3. Return `Image(path=local_path)` — FastMCP handles base64 encoding

**Edge cases:**
- Only call for image MIME types: `image/png`, `image/jpeg`, `image/gif`, `image/webp`
- Non-image attachments (PDFs, ZIPs): skip or return text description
- HTTP errors → raise with status code and URL

---

### 3. `save_test_artifacts(ticket_id, test_plan, test_cases)`
**Input:** ticket ID, test plan markdown string, test cases markdown string  
**Output:** JSON with saved file paths and Slack notification status

**Logic:**
1. Ensure `output/` directory exists
2. If `output/<ticket_id>_test_plan.md` already exists, append Unix timestamp suffix
3. Write both files with UTF-8 encoding
4. Post a completion message to the `#vector-notifications` Slack channel via `SLACK_WEBHOOK_URL` (see below)
5. Return paths of written files plus `slack_notified` / `slack_error`

**Slack notification:**
- Sent via Incoming Webhook (`SLACK_WEBHOOK_URL` in `.env`), one `requests.post` with a `text` payload
- Webhook is created once in the Slack workspace, scoped to `#vector-notifications` — no channel param needed in the payload
- Optional: if `SLACK_WEBHOOK_URL` is unset, notification is skipped silently (`slack_notified: false`, `slack_error: null`)
- Non-fatal: a failed Slack post (bad URL, network error, Slack outage) never fails the tool call — `save_test_artifacts` still reports `status: "saved"` and returns `slack_error` with the failure reason

---

## Auth Model
- Jira Server / Data Center uses **Bearer token** (Personal Access Token)
- Header: `Authorization: Bearer <token>`
- `jira` Python library: `JIRA(server=url, token_auth=token)` sends Bearer auth automatically
- Slack uses an **Incoming Webhook URL** (`SLACK_WEBHOOK_URL`) — the URL itself is the credential, no separate auth header

## File Layout
```
blast-agent/
├── .env                        ← credentials (gitignored)
├── tools/
│   ├── jira_mcp_server.py      ← MCP server (this tool)
│   └── test_jira_connection.py ← Phase 2 connection test
├── .tmp/<ticket_id>/           ← downloaded attachments (gitignored)
└── output/                     ← generated test plans (gitignored)
```
