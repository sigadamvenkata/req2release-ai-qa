# B.L.A.S.T Agent — Complete Repository Overview

## What This Tool Is

**B.L.A.S.T Agent** (Blueprint, Link, Architect, Stylize, Trigger) is an AI-powered QA automation system built at Adobe. It uses **Claude Code as the AI engine** with no separate Anthropic API key — Claude Code itself reads Jira tickets, reasons about them, and generates test artifacts via an MCP server bridge.

---

## Repository Layout

```
3x-jiraagent/
├── .claude/
│   └── settings.json          ← MCP server registrations
├── .vscode/                   ← VS Code workspace config
└── blast-agent/               ← Main project root
    ├── B.L.A.S.T.md           ← Framework methodology spec
    ├── claude.md / CLAUDE.md  ← Project Constitution (data schemas + behavioral rules)
    ├── task_plan.md           ← Phase blueprints & checklists
    ├── findings.md            ← Discovered bugs and constraints
    ├── progress.md            ← Execution log (all test runs)
    ├── pytest.ini             ← pytest configuration
    ├── requirements.txt       ← Python dependencies
    ├── .env                   ← Credentials (gitignored)
    │
    ├── app/                   ← React + Vite UI (dashboard concept)
    ├── architecture/          ← Technical SOPs in Markdown
    │   └── jira_mcp_sop.md
    ├── tools/                 ← Deterministic Python tools
    │   ├── jira_mcp_server.py   ← MCP server (3 tools exposed)
    │   ├── create_bugs.py       ← Auto-creates Jira bugs from findings
    │   ├── discover_fields.py   ← Discovers Jira custom field IDs
    │   └── test_jira_connection.py
    │
    ├── tests/                 ← Remove Background page test suite
    ├── tests-yt-bdd/          ← YouTube Gallery BDD suite
    ├── tests-yt-gallery/      ← YouTube Gallery functional suite
    ├── tests-yt-smoke/        ← YouTube Gallery smoke suite
    └── output/                ← Generated test plans + bug reports
```

---

## MCP Server Configuration

Registered in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "jira-test-agent": {
      "command": "C:\\Python314\\python.exe",
      "args": ["...tools/jira_mcp_server.py"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

| Server | Purpose |
|---|---|
| `jira-test-agent` | Python MCP server — exposes 3 Jira tools to Claude Code |
| `playwright` | Official Playwright MCP — lets Claude Code control a browser directly |

---

## The MCP Server — 3 Exposed Tools

**File:** `tools/jira_mcp_server.py` — built with `FastMCP` from the `mcp[cli]` package.

| Tool | Purpose |
|---|---|
| `fetch_jira_ticket(ticket_id)` | Fetches summary, description, status, priority, assignee, labels, components, comments, and attachment metadata as JSON |
| `download_jira_attachment(ticket_id, filename, url)` | Downloads an image attachment and returns it as an MCP `Image` object — Claude sees it visually |
| `save_test_artifacts(ticket_id, test_plan, test_cases)` | Writes generated markdown files to `output/` |

**Auth model:** Jira Server Bearer token (`JIRA_TOKEN` from `.env`).
**SSL:** `truststore.inject_into_ssl()` — uses the Windows corporate cert store to trust Adobe's internal CA (required behind GlobalProtect VPN).

---

## End-to-End Workflow

```
User: "Generate test plan for MWPW-199605"
  │
  ▼
Claude Code (AI engine)
  → calls fetch_jira_ticket("MWPW-199605")     [via jira-test-agent MCP]
  → calls download_jira_attachment(...)         [for each screenshot attachment]
  → reasons about ticket content + screenshots
  → generates test_plan.md  (Objective, Scope, Strategy, Entry/Exit Criteria, Environment, Risks)
  → generates test_cases.md (Gherkin BDD scenarios)
  → calls save_test_artifacts(...)
  → writes output/MWPW-199605_test_plan.md
  → writes output/MWPW-199605_test_cases.md
```

---

## Python Dependencies

**File:** `requirements.txt`

| Package | Version | Role |
|---|---|---|
| `jira` | ≥3.8.0 | Jira REST API client |
| `mcp[cli]` | ≥1.0.0 | MCP server framework (`FastMCP`) |
| `requests` | ≥2.31.0 | HTTP client for attachment downloads |
| `python-dotenv` | ≥1.0.0 | `.env` credential loading |
| `truststore` | ≥0.10.0 | Windows cert store injection for SSL |

---

## Playwright Test Suites

All test suites follow the same **Page Object Model (POM) + BDD Gherkin** architecture.

### Suite 1: `tests/` — Firefly Remove Background (MWPW-199605)

| File | Purpose |
|---|---|
| `locators.py` | Centralized CSS selectors (NavLocators, UploadLocators, AccordionLocators, SEOLocators) |
| `conftest.py` | Browser matrix fixtures + screenshot-on-failure hook |
| `pages/base_page.py` | Shared POM utilities |
| `pages/nav_page.py` | Global navigation actions |
| `pages/remove_bg_page.py` | Remove Background page actions |
| `features/remove_background.feature` | 20 Gherkin BDD scenarios |
| `specs/test_01_page_load.py` | Page title, meta description, canonical, H1, H2 |
| `specs/test_02_navigation.py` | Sign In CTA, Firefly CTA visibility + click |
| `specs/test_03_image_upload.py` | JPG/PNG/WebP uploads, PDF/HEIC error handling |
| `specs/test_04_accordion.py` | FAQ accordion expand/collapse |

**Browser matrix:** Chromium, Firefox, WebKit — all headless, 1440×900.
**Final result (Run 4):** 60 passed / 0 failed / 6 skipped / 4 xfailed / 2 xpassed.

### Suite 2: `tests-yt-bdd/` — YouTube Gallery (MWPW-199796)

10 spec files covering heading, grid layout, card metadata, SEO, page load, hover video, no-navigation click, cross-browser (Chromium/Firefox/WebKit), mobile (375×812 portrait / 812×375 landscape), and Stock API request interception.
**Latest result:** 20 passed / 8 failed / 1 xpassed.

**Spec files:**

| File | Coverage |
|---|---|
| `test_01_heading.py` | Gallery heading visibility |
| `test_02_grid_layout.py` | CSS grid, card bounding boxes |
| `test_03_card_metadata.py` | Unique IDs, labels, free tags, thumbnails |
| `test_04_page_seo.py` | Page title, meta description, main landmark |
| `test_05_page_load.py` | HTTP 200, gallery present, first thumbnail |
| `test_06_hover_video.py` | Video hidden before hover, plays on hover |
| `test_07_no_navigation.py` | Card click stays on same page |
| `test_08_cross_browser.py` | Heading + cards on Firefox and WebKit |
| `test_09_mobile.py` | Portrait 375×812 and landscape 812×375 |
| `test_10_stock_api.py` | Stock API called, 2xx response, stage endpoint |

### Suites 3 & 4: `tests-yt-gallery/` and `tests-yt-smoke/`

Functional and smoke variants of the YouTube Gallery tests with the same POM structure.

---

## Automated Bug Creation

**File:** `tools/create_bugs.py`

After automation reveals failures, this script automatically creates Jira bug tickets (type `Bug`) with:
- Structured descriptions in Jira markup (h3 headings, steps, expected/actual, environment)
- Correct custom fields (`customfield_12900` = Team: Brahmos, `customfield_14101` = Method Found: Testing - Automation)
- Component assignment
- `relates to` link back to the parent ticket
- Assignee resolved by display name lookup

**6 bugs auto-created:**

| Finding | Jira Key | Summary |
|---|---|---|
| F-001 | MWPW-199610 | pointer-events:none on Sign In & Accordion during JS init |
| F-002 | MWPW-199611 | Reupload button not shown to unauthenticated users |
| F-003 | MWPW-199612 | Animated WebP upload server error on WebKit/Safari |
| F-004 | MWPW-199613 | Firefly CTA slow to appear on WebKit/Safari (>3s delay) |
| F-005 | MWPW-199614 | Sign In click does not trigger IMS navigation on WebKit headless |
| F-006 | MWPW-199615 | Milo accordion fails Playwright actionability check |

---

## Generated Outputs

All written to `output/`:

| File | Description |
|---|---|
| `MWPW-199605_test_plan.md` | Structured test plan (Objective, Scope, Strategy, Criteria, Environment, Risks) |
| `MWPW-199605_test_cases.md` | Gherkin BDD test cases generated from ticket |
| `MWPW-199796_test_plan.md` | Test plan for YouTube Gallery ticket |
| `MWPW-199796_test_cases.md` | BDD test cases for YouTube Gallery |
| `figma_venkata-fullpage1_test_plan.md` | Test plan generated from a Figma design |
| `figma_venkata-fullpage1_test_cases.md` | BDD test cases from Figma design |
| `bug_report_results.json` | JSON log of all auto-created Jira bug keys |

---

## Report Generation

Tests produce two report formats:

| Format | Path | Tool |
|---|---|---|
| HTML report (self-contained) | `tests/reports/report.html` | `pytest-html` |
| Allure report | `tests/reports/allure-results/` + `allure-report/index.html` | `allure-pytest` |

Configured in `pytest.ini`:
```ini
addopts = -v --tb=short --html=tests/reports/report.html --self-contained-html --alluredir=tests/reports/allure-results
```

Test specs use `@allure.feature`, `@allure.story`, and `@allure.title` decorators for structured Allure output. On test failure, a full-page screenshot is automatically captured and attached to the report.

---

## App Layer (React Dashboard)

`app/` is a **React 19 + Vite + Tailwind CSS** frontend — a UI dashboard concept for the test plan generator. It uses the Playwright MCP (`drive.mjs`) for screenshot-driven UI verification of the dashboard itself.

| Package | Purpose |
|---|---|
| React 19 + React DOM | UI framework |
| Vite 8 | Build tool + dev server |
| Tailwind CSS v4 | Utility-first styling |
| Playwright (JS) | Drive/screenshot the UI for verification |
| ESLint | Code linting with React Hooks and React Refresh plugins |

---

## B.L.A.S.T Methodology (5 Phases)

| Phase | Name | What happens |
|---|---|---|
| **B** | Blueprint | Discovery questions, JSON data schema defined in `claude.md`, GitHub research |
| **L** | Link | API connection tests, credential verification, minimal handshake scripts |
| **A** | Architect | 3-layer build: Architecture SOPs (`architecture/`) → Navigation (Claude's reasoning) → Tools (`tools/`) |
| **S** | Stylize | Format outputs, polish Slack/HTML reports, UI/UX refinement |
| **T** | Trigger | Cloud deployment, cron/webhook setup, maintenance log in `claude.md` |

**3-Layer Architecture detail:**

- **Layer 1 — Architecture (`architecture/`):** Technical SOPs written in Markdown. Define goals, inputs, tool logic, and edge cases. SOPs are updated before code changes.
- **Layer 2 — Navigation:** Claude Code's reasoning layer. Routes data between SOPs and tools. Does not perform complex logic inline.
- **Layer 3 — Tools (`tools/`):** Deterministic Python scripts. Atomic and independently testable. All intermediate files in `.tmp/`, credentials only from `.env`.

---

## Environment Requirements

| Requirement | Detail |
|---|---|
| Python | 3.14 (`C:\Python314\python.exe`) |
| Node.js / npx | For Playwright MCP and React app |
| VPN | GlobalProtect — required for Jira API access |
| `.env` variables | `JIRA_URL`, `JIRA_TOKEN`, `JIRA_PROJECT`, `JIRA_AssignTo` |
| Claude Code | AI engine — no separate Anthropic API key needed |
| Playwright browsers | Chromium (pre-installed), Firefox 150.0.2, WebKit 26.4 |

**`.env` example:**
```
JIRA_URL=https://jira.corp.adobe.com
JIRA_TOKEN=<personal-access-token>
JIRA_PROJECT=MWP Web (MWPW)
JIRA_AssignTo=Sigadam Venkata Ramesh
```

---

## Technology Stack Summary

| Layer | Technology | Version |
|---|---|---|
| AI Engine | Claude Code (claude-sonnet-4-6) | — |
| MCP Framework | FastMCP (`mcp[cli]`) | ≥1.0.0 |
| Jira Integration | `jira` Python library | ≥3.8.0 |
| Test Framework | pytest | — |
| Browser Automation | Playwright (Python sync API) | — |
| BDD Format | Gherkin `.feature` files | — |
| Reporting | pytest-html + Allure | — |
| SSL/Cert | truststore | ≥0.10.0 |
| Frontend | React 19 + Vite 8 + Tailwind v4 | — |
| Runtime | Python 3.14, Node.js/npx | — |
| OS | Windows 11 Enterprise | — |

---

## Key Architecture Decision

> **Claude Code IS the AI.** There is no OpenAI/Anthropic API call in the Python code. The MCP server only handles data fetching and file writing. Claude Code — running in the terminal — is the reasoning engine that reads the Jira data, analyzes screenshots, and generates test plans. This is the "no API key needed" design: Claude Code's built-in intelligence drives the entire generation pipeline through MCP tool calls.
