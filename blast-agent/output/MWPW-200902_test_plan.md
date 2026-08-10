# Test Plan — MWPW-200902: Adobe.com SEO page for Firefly product "Remove Background" feature

**Ticket:** [MWPW-200902](https://jira.corp.adobe.com/browse/MWPW-200902)
**Type:** Story
**Status:** Draft
**Priority:** Normal
**Assignee:** Sigadam Venkata Ramesh
**Reporter:** Shruthi Channagiri
**Generated:** 2026-07-17
**Test Page:** https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html
**Redirect Target:** https://firefly-stage.corp.adobe.com/generate/image

---

## 1. Objective

Validate the Firefly "AI Background Generator" Unity block embedded in the Adobe.com SEO marquee. Coverage includes marquee content/branding, the image upload block (click + drag-and-drop, format/size validation), the upload progress ("splash") experience, the cross-domain handoff into the Firefly product app, Stock API integration on stage vs. production, and cross-browser/OS/mobile compatibility, plus baseline accessibility.

---

## 2. Scope

### In Scope
| Area | Details |
|---|---|
| Marquee content | Firefly branding/mnemonic, H1 heading, subheading copy, hero imagery |
| Upload block (Unity `feature-upload-image`) | Click-to-upload CTA, drag-and-drop zone, file picker |
| Format/size validation | Accepts JPEG/JPG, PNG, WEBP; rejects other types; enforces max size and min dimensions |
| Upload progress UI | Splash/progress indicator shown while the image is processed |
| Cross-app handoff | Successful upload redirects to `firefly-stage.corp.adobe.com/generate/image` with the image carried over |
| Stock API integration | Correct endpoint called per environment (stage vs. production), 2xx responses |
| Cross-browser | Chrome, Firefox, Safari (WebKit), Edge |
| Mobile | Android & iOS viewports — portrait and landscape |
| Accessibility | Alt text, heading semantics, keyboard focus order, basic ARIA on upload controls |

### Out of Scope
- Firefly product app's actual background-generation/AI processing quality (post-redirect experience beyond confirming successful landing)
- Payment / subscription / entitlement flows
- Full WCAG 2.1 AA manual audit (automated/basic a11y checks only)
- Production Stock API data correctness (only endpoint routing is verified, not response payload content)
- CDN caching / performance budget testing

---

## 3. Test Strategy

| Layer | Approach | Tools |
|---|---|---|
| @smoke | Page loads, marquee + upload block render, HTTP 200 | Playwright (Chromium) |
| @ui | Marquee copy, mnemonic, heading/subheading, block layout | Playwright (Chromium) |
| @upload | Valid format upload, drag-and-drop, invalid format/size rejection | Playwright (Chromium), `set_input_files` |
| @redirect | Post-upload navigation to `firefly-stage.corp.adobe.com/generate/image` | Playwright `page.wait_for_url` |
| @compat | Cross-browser heading + upload block presence | Playwright (Firefox, WebKit) |
| @mobile | Portrait + landscape viewport simulation, click-upload (no OS drag-drop) | Playwright (Chromium, mobile emulation) |
| @integration | Stock API network interception — stage vs. prod routing | Playwright `page.on("request")` |
| @a11y | Alt text, heading order, aria-live on error/progress states | axe-core or manual DevTools audit |
| Manual | Actual drag-and-drop feel, splash screen animation, visual QA | Chrome DevTools |

**Suggested suite location:** `blast-agent/tests-bg-generator/` (new suite — no existing automation for this specific block; can reuse `BasePage` and the `RemoveBgPage`/`locators.py` patterns from MWPW-199605 since both use the same Unity upload component family).

---

## 4. Entry Criteria

- [ ] Stage URL returns HTTP 200: `https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html`
- [ ] `.unity.feature-upload-image` block is present in the DOM
- [ ] Valid test assets available: JPG, PNG, WEBP (each < 100MB, ≥ 512×512px)
- [ ] Invalid test assets available: unsupported type (e.g. PDF/HEIC/GIF), oversized (> 100MB), undersized (< 512×512px)
- [ ] `firefly-stage.corp.adobe.com` is reachable from the test network (VPN/corp network may be required)
- [ ] `.env` configured with valid `JIRA_TOKEN` for defect filing
- [ ] Playwright browsers installed (`playwright install`)

## 5. Exit Criteria

- [ ] All @smoke tests pass
- [ ] Upload happy path (JPEG, PNG, WEBP) verified via click-CTA and drag-and-drop
- [ ] All 5 documented error states reproduced (filesize, request failure, filetype, filecount, min-dimension)
- [ ] Successful upload redirects to `firefly-stage.corp.adobe.com/generate/image`
- [ ] Stock API stage endpoint call confirmed; no calls to the production endpoint from the stage page
- [ ] Cross-browser tests run on Chromium, Firefox, and WebKit
- [ ] Mobile portrait and landscape verified on at least one Android and one iOS viewport
- [ ] Basic accessibility checks pass or are documented as known issues
- [ ] All failures linked to parent ticket MWPW-200902

---

## 6. Test Environment

| Env | URL | Redirect Target | Stock API Endpoint |
|---|---|---|---|
| Stage | `https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html` | `https://firefly-stage.corp.adobe.com/generate/image` | `www.stage.adobe.com/stock-api` *(assumed — confirm exact path with dev)* |
| Production | *(not yet provisioned per this ticket — SEO page URL TBD)* | `https://firefly.adobe.com/generate/image` *(assumed)* | `www.adobe.com/stock-api` *(assumed)* |

**Browsers:** Chromium 1440×900, Firefox 1440×900, WebKit 1440×900
**Mobile:** Chromium 375×812 (portrait), 812×375 (landscape) — Android/iOS emulation
**OS:** Windows 11 (CI), macOS (local)

### Discovered Page Details (from stage source, fetched 2026-07-17)
- Block classes: `unity workflow-upload product-firefly feature-upload-image dark`
- Workflow/module id: `cgen` (background-generator workflow), `promoid=QTV3NS2W&mv=other`
- Declared limits: max file size **100MB**, min image dimensions **512×512px**
- Accepted formats (per page copy): **JPEG(JPG), PNG, WEBP**
- Error copy (verbatim, 5 states):
  1. "File size larger than 100MB"
  2. "Unable to process the request"
  3. "We are unable to process this file type. Please try again."
  4. "Only one file can be uploaded at a time."
  5. "Image is smaller than the minimum dimensions (512 x 512 pixels). Please resize and try again."

### ⚠️ Discrepancy vs. Ticket Requirement
The ticket specifies the H1 should read **"Adobe Firefly AI background generator: Transform photos in a click"**. The live stage H1 is **"AI background generator: Transform photos in a click."** — "Adobe Firefly" appears only as separate branding text (mnemonic + wordmark) above the heading, not inside the H1 itself. Flag for confirmation with the reporter/design — may be intentional (mnemonic satisfies "with product mnemonic") or a content gap.

---

## 7. Test Case Groups

| Group | Tag | Description | Count |
|---|---|---|---|
| 1 | @ui | Marquee branding & heading/subheading copy | 4 |
| 2 | @ui | Upload block layout & CTA/drop-zone presence | 3 |
| 3 | @upload | Valid format upload (JPG, PNG, WEBP) — click CTA | 3 |
| 4 | @upload | Valid format upload — drag and drop | 1 |
| 5 | @upload @error | Invalid format / size / dimension rejection | 5 |
| 6 | @upload | Splash/progress indicator during processing | 2 |
| 7 | @redirect @integration | Post-upload redirect to Firefly product app | 2 |
| 8 | @smoke | Page load & HTTP status | 2 |
| 9 | @compat | Cross-browser (Firefox, WebKit) | 2 |
| 10 | @mobile | Mobile portrait & landscape, click-upload only | 3 |
| 11 | @integration | Stock API — call detected, 2xx, stage routing | 3 |
| 12 | @a11y | Alt text, heading order, upload control ARIA | 3 |
| **Total** | | | **33** |

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| H1 heading text does not match ticket wording exactly | High | Low | Documented as a discrepancy (Section 6); confirm intent before filing as a bug |
| Splash/progress screen timing is flaky in automation | Medium | Medium | Wait on progress element visibility or `networkidle`, not fixed sleeps |
| Cross-domain redirect (adobe.com → firefly-stage.corp.adobe.com) blocked in headless/CORS contexts | Medium | High | Verify via `page.wait_for_url()` after upload; ensure test runs against corp network/VPN |
| `firefly-stage.corp.adobe.com` requires VPN/corp network access | Medium | High | Document as environment prerequisite; CI runners must have network access |
| Stock API endpoint hostnames not explicitly named in the ticket | Medium | Medium | Assumption flagged in Section 6; confirm exact endpoint path with dev before automating |
| Rendered DOM class names differ from raw AEM source (block is JS-decorated) | Medium | Medium | Selectors must be re-verified against the live rendered DOM (via Playwright) before automation, not just page source |
| Animated/oversized test assets unavailable in repo | Low | Medium | Reuse `tests/assets/` files from MWPW-199605 where compatible (JPG/PNG/WEBP/PDF/HEIC); add a >100MB and <512px asset for full coverage |
| Production SEO page URL not yet defined in this ticket | Low | Medium | Prod-specific test cases marked TBD until URL is confirmed |
| Mobile OS lacks native drag-and-drop | Low | Low | Mobile suite only exercises click-to-upload CTA, not drag-and-drop |

---

## 9. Automation Artifacts (Proposed)

```
blast-agent/
└── tests-bg-generator/            # new suite — reuse BasePage from tests/pages/
    ├── locators/                  # BGGeneratorLocators (verify against rendered DOM first)
    ├── pages/                     # BackgroundGeneratorPage(BasePage)
    ├── specs/                     # test_01_marquee … test_07_stock_api
    ├── conftest.py
    ├── pytest.ini
    └── reports/                   # allure-results + allure-report + report.html
```
