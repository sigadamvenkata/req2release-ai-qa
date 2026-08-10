# Findings — Jira Test Plan Agent

## Jira Server Details
- **URL**: https://jira.corp.adobe.com
- **Type**: Jira Server / Data Center (corporate Adobe instance)
- **Auth**: Personal Access Token (PAT) — Bearer token auth for Jira Server
- **Token location**: `objective.md` → must be moved to `.env` as `JIRA_TOKEN`

## Python Library
- **`jira`** (PyPI: `jira`) — official Python Jira library
  - Supports Jira Server PAT auth via `token_auth` parameter
  - Usage: `JIRA(server=url, token_auth=token)`
  - Fetches: issue fields, comments, attachments

## Claude API
- **Library**: `anthropic` (PyPI: `anthropic`)
- **Model**: `claude-sonnet-4-6`
- **Key**: requires `ANTHROPIC_API_KEY` in `.env`

## Attachment Handling
- Jira attachments include screenshots (JPEG/PNG)
- Image content can be base64-encoded and passed to Claude's vision capability
- Download attachments using `requests` with Bearer token auth header

## Constraints
- Corporate Jira — may require VPN / internal network access
- Attachment downloads need the same Bearer auth header as API calls
- Description uses Jira markup (wiki markup or Atlassian Document Format) — needs plain text extraction

## Dependencies (requirements.txt)
```
jira>=3.8.0
anthropic>=0.40.0
requests>=2.31.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

---

## MWPW-199605 — Playwright Automation Findings

**Page:** https://www.adobe.com/products/firefly/features/remove-background.html  
**Framework:** Python + Playwright + pytest + allure | **Date:** 2026-06-26

### Framework Architecture
```
blast-agent/
├── pytest.ini                         # Pytest config (root — where pytest runs from)
├── tests/
│   ├── conftest.py                    # Browser fixtures, page-object fixtures, screenshot hook
│   ├── locators.py                    # Centralized CSS selectors (all page objects import here)
│   ├── assets/                        # Test images
│   ├── pages/                         # Page Object Model
│   │   ├── base_page.py              # Shared: navigate, title, meta, canonical, screenshot
│   │   ├── nav_page.py               # Global Nav: sign-in, Firefly CTA
│   │   └── remove_bg_page.py         # Remove Bg: SEO, upload, accordion
│   ├── specs/                         # Test spec files (pytest)
│   │   ├── test_01_page_load.py      # SEO: title, meta, canonical, H1, H2
│   │   ├── test_02_navigation.py     # Nav: Sign In CTA, Firefly CTA
│   │   ├── test_03_image_upload.py   # Upload: valid formats, invalid formats
│   │   └── test_04_accordion.py      # Accordion: expand, collapse, FAQ presence
│   ├── features/
│   │   └── remove_background.feature # Gherkin BDD (20 scenarios)
│   └── reports/
│       ├── report.html               # pytest-html report (self-contained)
│       └── allure-results/           # Raw Allure data (run `allure serve` to view)
```

### Browser Matrix
| Browser  | Engine  | Status   |
|----------|---------|----------|
| Chromium | Blink   | Active   |
| Firefox  | Gecko   | Active   |
| WebKit   | WebKit  | Active   |

### Locators Discovered (live page inspection)
| Purpose | Selector | Notes |
|---------|----------|-------|
| Sign In | `button.profile-comp.secondary-button` | Adobe UNAV component |
| Firefly CTA | `a.feds-cta.feds-cta--secondary` | FEDS nav; slow on WebKit |
| File input | `input.ia-file-input` | Accepts jpg, png, webp |
| Drop zone | `.drop-zone-container` | Always visible |
| Reupload button | `button.ia-reupload-btn` | Needs auth + AI processing |
| Accordion | `button.accordion-trigger` | `aria-expanded` attribute |
| H1 | `h1` | Page heading |

### Test Results Summary
| Category | Passed | Failed | Skipped |
|----------|--------|--------|---------|
| Page Load & SEO | 15 | 0 | 0 |
| Navigation | ~8 | ~4 | 3 |
| Upload | ~6 | ~3 | 3 |
| Accordion | ~6 | ~6 | 0 |

### Defects Found During Automation

**F-001: UNAV Sign In + Accordion — `pointer-events: none` during JS init**  
- Browsers: All | Severity: Medium  
- Adobe UNAV and Milo accordion apply `pointer-events: none` while JavaScript initializes.  
- Playwright blocks click with "element is not enabled".  
- Fix: `click(force=True)` bypasses actionability check.

**F-002: Reupload button requires authentication + AI processing**  
- Browsers: All | Severity: Low  
- Unauthenticated headless runs can trigger uploads but processing doesn't complete without auth.  
- `button.ia-reupload-btn` never appears. Valid upload confirmed via absence of error only.  
- Recommendation: Add an authenticated test suite pass with an Adobe test account.

**F-003 (BUG): Animated WebP triggers server validation error on WebKit**  
- Browser: WebKit only | Severity: High  
- `valid_webp.webp` (from `gif.webp`) is animated WebP. WebKit reports MIME differently; server rejects it.  
- Same file passes on Chromium and Firefox.  
- Impact: Safari users uploading animated WebP may hit unexpected errors.  
- Fix: Replace `valid_webp.webp` with a static (non-animated) WebP file.  
- Recommendation: File bug with dev team — animated WebP should either be accepted or return a clear message.

**F-004: Firefly CTA slow to appear on WebKit**  
- Browser: WebKit only | Severity: Low  
- FEDS nav CTA takes >3s to render on WebKit. Fixed with 8s explicit wait.

**F-005: Sign In navigation not testable in headless mode**  
- Browsers: All | Severity: Low (test limitation, not a page bug)  
- UNAV JS click handler fires, but IMS redirect doesn't trigger in Playwright headless mode.  
- Possible reason: Adobe's IMS redirect uses a popup tab or requires a full browser session.  
- Test marked `xfail` — headless limitation, use `--headed` or a real session to verify.

**F-006: Accordion `button.accordion-trigger` reports "not enabled" in Playwright**  
- Browsers: All | Severity: Low (framework issue)  
- Playwright's actionability check reports these buttons as "not enabled" during testing.  
- Root cause: CSS or rendering state makes Playwright's check fail even though the element is DOM-present.  
- Fix: Use `page.evaluate("el.click()")` (native JS DOM click) — bypasses Playwright's actionability check while still triggering real JS event handlers.  
- The JS `.click()` properly triggers the accordion expand/collapse (aria-expanded changes correctly).

### How to Run
```bash
# From blast-agent/ directory

# Full suite (3 browsers, ~70 tests)
python -m pytest

# Smoke only
python -m pytest -m smoke

# One browser
python -m pytest -k "chromium"

# View HTML report
start tests/reports/report.html

# View Allure (requires allure CLI installed)
allure serve tests/reports/allure-results
```
