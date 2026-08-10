# Test Plan — MWPW-199796: YouTube Gallery Block

## Objective
Validate the YouTube Gallery block on CC pages meets all UI, functional, integration, and cross-platform compatibility requirements. The block must render a grid of video cards, each with a heading, unique ID, label text, Free tag, and thumbnail image — play its video inline on mouse hover with no click-through navigation — and correctly call the Stock API to fetch card data, using the appropriate endpoint per environment (stage vs. production).

## Scope

### In Scope
- Gallery block heading visibility and accuracy
- Grid layout and card alignment
- Per-card metadata: unique ID, label text, Free tag, thumbnail image
- Hover-triggered inline video playback
- Absence of click actions or page navigation from cards
- **Stock API integration**: verify the API is called on page load and returns card data
- **Environment routing**: stage page calls stage endpoint; production page calls production endpoint
- Cross-browser: Chrome, Firefox, Safari, Edge
- Cross-OS: Windows, macOS
- Mobile: Android and iOS (Chrome, Safari)
- Responsive layout: landscape and portrait orientations

### Out of Scope
- YouTube API internals / CDN video delivery
- Backend CMS authoring workflow
- Stock API server-side logic or backend reliability
- Analytics tracking events
- Accessibility (WCAG) — separate audit

## Test Strategy
| Layer | Approach |
|-------|----------|
| Smoke | Page 200 OK, heading present, at least one card visible |
| UI | Grid structure, card elements (ID, label, tag, image) per card |
| Functional | Hover events: confirm video plays; confirm no navigation on click |
| Integration | Intercept network requests; assert Stock API is called with correct endpoint per environment; assert response populates gallery cards |
| Compatibility | Smoke + functional suites across Chrome, Firefox, Safari, Edge; mobile viewports |
| Regression | Full suite re-run after any block, API endpoint, or template change |

Automation framework: **Playwright + pytest + Allure** (mirrors existing suite in this repo).

## Entry Criteria
- Page accessible at target URL (HTTP 200)
- At least one fully-authored gallery card present
- Playwright browsers installed and configured
- Stage and production Stock API base URLs confirmed and documented in test config

## Exit Criteria
- All @smoke scenarios pass on Chromium, Firefox, WebKit
- All @ui and @functional scenarios pass on Chromium
- All @integration scenarios pass for both stage and production endpoint routing
- No P1/P2 defects open related to card structure, hover playback, or API calls
- Allure report generated and linked in Jira

## Test Environment
| Item | Value |
|------|-------|
| Test URL (stage) | https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery |
| Test URL (prod) | https://www.adobe.com/products/firefly/features/youtube-gallery.html *(confirm with team)* |
| Stock API — Stage | https://www.stage.adobe.com/stock-api |
| Stock API — Prod | https://www.adobe.com/stock-api |
| Browsers | Chromium, Firefox, WebKit (Playwright); Edge (optional) |
| Viewport (desktop) | 1440 x 900 |
| Viewport (mobile portrait) | 375 x 812 |
| Viewport (mobile landscape) | 812 x 375 |
| OS | Windows 11, macOS |
| Mobile OS | Android 13 (Chrome), iOS 17 (Safari) |
| Framework | Playwright 1.x + pytest + Allure |
| API interception | Playwright `page.route()` / `page.on("request")` |

## Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Hover video may not fire in headless browser | Run hover tests headed; use page.hover() + wait for video[src] |
| Dynamic card count from CMS | Assert at least 1 card; use count >= threshold |
| WebKit limited autoplay support | Assert paused property changes; skip audio check on WebKit |
| Mobile touch — no hover equivalent | Test touchstart; document as known gap if autoplay not triggered |
| AEM Live staging URL may be gated | Add auth header fixture if needed |
| Stock API stage endpoint unknown | Confirm exact URLs with backend team before writing integration tests; use placeholder config |
| Stock API returns empty/error response | Assert HTTP 2xx status and non-empty payload; treat API failure as P1 blocking defect |
| Stage/prod endpoint mismatch causes wrong data | Parameterise base URL via env var; run suite against each environment separately in CI |
