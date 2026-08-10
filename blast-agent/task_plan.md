# Task Plan — Jira Test Plan Agent

## Goal
Given a Jira ticket ID, automatically fetch all ticket details and generate a test plan + BDD test cases as markdown files.

---

## Approved Blueprint

### Input → Processing → Output
```
CLI: python main.py <TICKET_ID>
         │
         ▼
[Layer 3: tools/jira_fetcher.py]
  - Connect to https://jira.corp.adobe.com via Jira Python API
  - Fetch: summary, description, comments, attachments
  - Download image attachments to .tmp/<TICKET_ID>/
         │
         ▼
[Layer 3: tools/ai_generator.py]
  - Send Jira payload to Claude claude-sonnet-4-6
  - Prompt: generate test plan + Gherkin BDD test cases
  - Return: structured markdown strings
         │
         ▼
[Layer 3: tools/file_writer.py]
  - Write output/<TICKET_ID>_test_plan.md
  - Write output/<TICKET_ID>_test_cases.md
         │
         ▼
Console: Success message + file paths
```

---

## Phases & Checklist

### Phase 0 — Initialization
- [x] Create claude.md (Project Constitution)
- [x] Create task_plan.md
- [ ] Create findings.md
- [ ] Create progress.md

### Phase 1 — Blueprint (B)
- [x] Discovery questions answered
- [x] Data Schema defined in claude.md
- [ ] Blueprint approved by user

### Phase 2 — Link (L)
- [x] Create `.env` with JIRA_TOKEN, JIRA_URL
- [x] `tools/test_jira_connection.py` — Jira API verified (connected as venkatas@adobe.com)
- [x] No Claude API key needed — using MCP architecture with Claude Code

### Phase 3 — Architect (A)
- [x] `architecture/jira_mcp_sop.md`
- [x] `tools/jira_mcp_server.py` (3 tools: fetch_jira_ticket, download_jira_attachment, save_test_artifacts)
- [x] `.claude/settings.json` — MCP server registered in Claude Code

### Phase 4 — Stylize (S)
- [ ] Review sample output with user
- [ ] Refine prompts based on feedback

### Phase 5 — Trigger (T)
- [ ] Final documentation in claude.md
- [ ] Optional: batch processing mode
