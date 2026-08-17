# Project Constitution — Jira Test Plan Agent

## Purpose
Fetch a Jira ticket's full details and generate a structured test plan + BDD test cases as local markdown files.

---

## Data Schemas

### Input
```json
{
  "ticket_id": "string"  // e.g. "PROJ-1234"  — passed as CLI arg
}
```

### Jira Fetch Payload (raw)
```json
{
  "ticket_id":    "string",
  "summary":      "string",
  "description":  "string",
  "status":       "string",
  "priority":     "string",
  "assignee":     "string",
  "reporter":     "string",
  "labels":       ["string"],
  "comments":     [
    { "author": "string", "body": "string", "created": "ISO8601" }
  ],
  "attachments":  [
    { "filename": "string", "url": "string", "mime_type": "string" }
  ],
  "screenshots":  ["string"]  // local paths of downloaded image attachments
}
```

### AI Generation Input
```json
{
  "jira_payload":  "<JiraFetchPayload>",
  "format":        "gherkin_bdd",
  "model":         "claude-sonnet-4-6"
}
```

### Output Files
```
output/
  <TICKET_ID>_test_plan.md
  <TICKET_ID>_test_cases.md
```

### test_plan.md structure
```
# Test Plan — <TICKET_ID>: <summary>

## Objective
## Scope (In / Out)
## Test Strategy
## Entry / Exit Criteria
## Test Environment
## Risks & Mitigations
```

### test_cases.md structure (Gherkin BDD)
```
# Test Cases — <TICKET_ID>: <summary>

## Feature: <feature name>

### Scenario: <title>
  Given ...
  When  ...
  Then  ...
  [And  ...]
```
### test_report.md structure 
```
## Feature: <feature name>
## Page details : <page url where test run>

### Scenario: <title>
  issue details...
```

---

## Behavioral Rules
- NEVER hardcode credentials. Always read from `.env`.
- Token from `objective.md` must be copied to `.env` as `JIRA_TOKEN`.
- Download image attachments to `.tmp/<TICKET_ID>/` before passing to Claude.
- Download excel attachments to `.tmp/<TICKET_ID_EXCEL>/` before passing to Claude.
- Claude model: `claude-sonnet-4-6`.
- If Jira description is empty, use comments + summary as context.
- Output files go to `output/` directory. Create it if missing.
- Do not overwrite existing output — append timestamp suffix if file exists.
- After saving artifacts, post a completion notice to the `#vector-notifications` Slack channel via `SLACK_WEBHOOK_URL` (`.env`). Optional — skip silently if unset. Notification failures must never fail the save.

---

## Architectural Invariants
1. `tools/` scripts are atomic and independently testable.
2. `.tmp/` holds all intermediate/downloaded files — never commit.
3. `architecture/` SOPs are the canonical logic spec — update before updating code.
4. The main orchestrator `main.py` only calls tools in sequence; no business logic inline.

---

## Architecture: MCP Server Pattern
Claude Code IS the AI engine — no external AI API key needed.
The Python MCP server exposes Jira data as tools; Claude Code calls them and generates output.

```
User: "Generate test plan for PROJ-1234"
  → Claude Code calls fetch_jira_ticket("PROJ-1234")
  → Claude Code calls download_jira_attachment(...) for each screenshot
  → Claude Code generates test plan + BDD test cases
  → Claude Code calls save_test_artifacts(ticket_id, plan, cases)
  → Files written to output/
  → save_test_artifacts posts completion notice to #vector-notifications (Slack)
```

## Maintenance Log
| Date       | Change                                        | Author   |
|------------|-----------------------------------------------|----------|
| 2026-06-18 | Initial constitution draft                    | venkatas |
| 2026-06-18 | Switched to MCP architecture (no API key needed) | venkatas |
| 2026-07-29 | Added Slack notification (#vector-notifications) on test artifact save | venkatas |
---

## sample prompts

Kick start:
generate test plan for MWPW-XXXXXX

Automation Prompt:
Automate all test cases using playwright MCP from MWPW-200902_test_cases.md output file. Create folder with name ‘firefly-remove-background’ and create individual test files for every test case feature, page objects, tests as separate files for understanding and maintainability. For the file upload cases take the image from “…/blast-agent\tests\assets\female.png”. once automation script generated, update us back. Do not run until we ask

Automation run:
Run the automated tests in sequential order, show the browser where tests are running. give the result via allure report which clearly indicating what tests are run, how many pass and fail.

Bug report:
Report all failure in to jira and get me back the jira
