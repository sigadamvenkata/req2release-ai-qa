# Test Plan — MWPW-199796: YouTube Gallery Block for CC Pages

**Ticket:** [MWPW-199796](https://jira.corp.adobe.com/browse/MWPW-199796)
**Status:** Draft
**Assignee:** Sigadam Venkata Ramesh
**Generated:** 2026-07-03
**Test Page:** https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery

---

## 1. Objective

Validate the new YouTube Gallery block for CC (Creative Cloud) pages. The block must satisfy all UI layout requirements, interactive video behaviour on hover, cross-browser/mobile compatibility, and Stock API integration — both for the stage and production environments.

---

## 2. Scope

### In Scope
| Area | Details |
|---|---|
| UI / Layout | Heading, grid, card structure, free tag, card image |
| Interaction | Hover-to-play video, no click navigation from card |
| Cross-browser | Chrome, Firefox, Safari (WebKit), Edge |
| Mobile | Android & iOS viewports — portrait and landscape |
| Stock API | Stage endpoint called from stage; prod endpoint from prod |
| SEO | Meta description tag present and non-empty |
| Accessibility | Heading semantics, alt text on images |
| Performance | Page load within acceptable threshold |

### Out of Scope
- Backend/CMS authoring of the block
- Adobe IMS login flows
- Video playback duration / quality metrics
- CDN caching behaviour
- WCAG 2.1 full audit (basic a11y only)

---

## 3. Test Strategy

| Layer | Approach | Tools |
|---|---|---|
| @smoke | Critical path — page loads, heading visible, API called | Playwright (Chromium) |
| @ui | Full UI coverage — grid, cards, metadata, layout | Playwright (Chromium) |
| @compat | Cross-browser heading + card presence | Playwright (Firefox, WebKit) |
| @mobile | Portrait + landscape viewport simulation | Playwright (Chromium, mobile) |
| @integration | Stock API network interception — stage vs prod routing | Playwright page.on("request") |
| Manual | Visual design review, actual video play on hover | Chrome DevTools |

**Test suites:**
- `blast-agent/tests-yt-gallery/` — @ui
- `blast-agent/tests-yt-smoke/` — @smoke, @compat, @mobile, @integration

---

## 4. Entry Criteria

- [ ] AEM Live staging URL is accessible (HTTP 200): `https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery`
- [ ] `.prm-yt-gallery` block is present in the DOM
- [ ] At least 1 YouTube card is rendered
- [ ] Playwright browsers installed (`playwright install`)
- [ ] `.env` configured with valid Jira token

## 5. Exit Criteria

- [ ] All @smoke tests pass
- [ ] All @ui tests pass or failures are documented as Jira bugs
- [ ] Cross-browser tests run on Chromium, Firefox, WebKit
- [ ] Mobile portrait and landscape verified
- [ ] Stock API network call confirmed on stage environment
- [ ] All failures linked to parent ticket MWPW-199796

---

## 6. Test Environment

| Env | URL | Stock API Endpoint |
|---|---|---|
| Stage | `https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery` | `www.stage.adobe.com/stock-api` |
| Production | `https://www.adobe.com/<cc-page-path>` | `www.adobe.com/stock-api` |

**Browsers:** Chromium 1440×900, Firefox 1440×900, WebKit 1440×900
**Mobile:** Chromium 375×812 (portrait), 812×375 (landscape)
**OS:** Windows 11 (CI), macOS (local)

### Known Issue — Locale Modal
The page shows a locale selector modal (`.modal-curtain.is-open`) on first load that intercepts pointer events. All automation must dismiss this modal before asserting heading/card visibility.
**Bugs filed:** MWPW-199809, MWPW-199812

---

## 7. Test Case Groups

| Group | Tag | Description | Count |
|---|---|---|---|
| 1 | @ui | Heading validity | 3 |
| 2 | @ui | Grid & card layout | 4 |
| 3 | @ui | Card metadata (ID, label, free tag, image) | 5 |
| 4 | @ui | Page layout & SEO | 3 |
| 5 | @smoke | Page load & HTTP status | 3 |
| 6 | @smoke | Hover-to-play video | 2 |
| 7 | @smoke | No click navigation | 1 |
| 8 | @compat | Cross-browser (Firefox, WebKit) | 2 |
| 9 | @mobile | Mobile portrait & landscape | 3 |
| 10 | @integration | Stock API — call detected, 2xx, stage routing | 3 |
| **Total** | | | **29** |

---

## 8. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Locale modal blocks heading assertion | High | High | Dismiss curtain before each test; filed MWPW-199809, MWPW-199812 |
| AEM Live staging URL goes offline | Medium | High | Smoke test checks HTTP 200 as gate |
| Hover video requires user gesture policy | Medium | Medium | Launch Chromium with `--autoplay-policy=no-user-gesture-required` |
| Stock API stage/prod routing misconfigured | Low | High | Network intercept test catches prod URL calls from stage |
| Meta description missing on staging | High | Medium | Existing bug MWPW-199810 filed; excluded from smoke gate |
| Mobile overflow due to card grid | Low | Medium | Assert `scrollWidth <= innerWidth` in mobile test |

---

## 9. Bug Tracking

| Bug | Summary | Suite | Status |
|---|---|---|---|
| MWPW-199809 | Heading not visible — locale modal overlay (@ui) | @ui | Open |
| MWPW-199810 | Meta description missing on AEM Live staging URL | @ui | Open |
| MWPW-199812 | Heading not visible across Chromium/Firefox/WebKit (@smoke) | @smoke | Open |

---

## 10. Automation Artifacts

```
blast-agent/
├── tests-yt-gallery/          # @ui suite
│   ├── locators/              # YTGalleryLocators
│   ├── pages/                 # BasePage + YouTubeGalleryPage
│   ├── specs/                 # test_01_heading … test_04_page_layout
│   ├── conftest.py
│   ├── pytest.ini
│   └── reports/               # allure-results + allure-report + report.html
└── tests-yt-smoke/            # @smoke suite
    ├── locators/              # yt_smoke_locators
    ├── pages/                 # YouTubeGalleryPage
    ├── specs/                 # test_01_page_load … test_06_stock_api
    ├── conftest.py
    ├── pytest.ini
    └── reports/               # allure-results + allure-report + report.html
```
