# Test Cases — MWPW-199796: YouTube Gallery Block for CC Pages

**Ticket:** [MWPW-199796](https://jira.corp.adobe.com/browse/MWPW-199796)
**Format:** Gherkin BDD
**Generated:** 2026-07-03
**Test Page:** https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery

---

## Feature: YouTube Gallery Block — UI Layout

### Group 1: Heading Validity `@ui`

#### Scenario 1.1: Gallery heading is visible on page load
```gherkin
Given the YouTube Gallery page is open at the staging URL
And the locale modal is dismissed
When the page reaches network idle state
Then the element "h2.heading-xl" should be visible in the viewport
```

#### Scenario 1.2: Gallery heading contains non-empty text
```gherkin
Given the YouTube Gallery page is open at the staging URL
And the locale modal is dismissed
When I read the text content of "h2.heading-xl"
Then the heading text should not be empty
And the heading text should contain meaningful content
```

#### Scenario 1.3: Only one H2 heading exists in the gallery block
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I count all "h2" elements within ".prm-yt-gallery"
Then there should be exactly 1 H2 heading element
```

---

### Group 2: Grid & Card Layout `@ui`

#### Scenario 2.1: Gallery grid is visible
```gherkin
Given the YouTube Gallery page is open at the staging URL
When the page renders completely
Then the grid container ".pre-yt-grid" should be visible
```

#### Scenario 2.2: Gallery contains at least one card
```gherkin
Given the YouTube Gallery page is open at the staging URL
When the page renders completely
Then the count of ".pre-yt-card" elements should be greater than or equal to 1
```

#### Scenario 2.3: Cards are arranged in a grid layout
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I inspect the layout of ".pre-yt-grid"
Then the CSS display property should indicate a grid or flex layout
And cards should not overflow the grid container horizontally
```

#### Scenario 2.4: Each card occupies a consistent width
```gherkin
Given the YouTube Gallery page is open at the staging URL
And there are multiple ".pre-yt-card" elements
When I measure the bounding box of each card
Then each card should have a non-zero width and height
And card widths should be consistent within a 5px tolerance
```

---

### Group 3: Card Metadata `@ui`

#### Scenario 3.1: Each card has a unique identifier
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I read the "id" or "data-id" attribute of each ".pre-yt-card"
Then no two cards should share the same identifier value
```

#### Scenario 3.2: Each card displays a label text
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I read the text of the label element inside each ".pre-yt-card"
Then every card should have a non-empty label text
```

#### Scenario 3.3: Each card displays a free tag
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I look for ".pre-yt-free-tag" within each ".pre-yt-card"
Then at least one card should contain a visible free tag element
```

#### Scenario 3.4: Each card displays a thumbnail image
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I inspect ".image-wrapper img" within each ".pre-yt-card"
Then every card should contain an image element
And the image "src" attribute should not be empty or a placeholder
And the image should be visible in the viewport
```

#### Scenario 3.5: Card thumbnail has a valid alt attribute
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I read the "alt" attribute of ".image-wrapper img" in each card
Then the alt attribute should not be null
And the alt text should not be empty (for accessibility)
```

---

### Group 4: Page Layout & SEO `@ui`

#### Scenario 4.1: Page title is non-empty
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I read the document "<title>" tag
Then the page title should not be empty
```

#### Scenario 4.2: Meta description tag is present and non-empty
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I query "meta[name='description']"
Then the element should exist in the DOM
And its "content" attribute should not be empty
```
> **Known Bug:** MWPW-199810 — Meta description is missing on AEM Live staging URL.

#### Scenario 4.3: Gallery block is positioned within the main content area
```gherkin
Given the YouTube Gallery page is open at the staging URL
When I check the DOM position of ".prm-yt-gallery"
Then it should be a descendant of the main content element
And its bounding box should be within the page scroll area
```

---

## Feature: YouTube Gallery Block — Interactions

### Group 5: Page Load & HTTP Status `@smoke`

#### Scenario 5.1: Page returns HTTP 200
```gherkin
Given the staging URL "https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery"
When a GET request is made to the URL
Then the HTTP response status should be 200
And the response should not be a 404, 500, or redirect to an error page
```

#### Scenario 5.2: Gallery block is present after page load
```gherkin
Given the YouTube Gallery page loads successfully
When the page reaches network idle state
Then ".prm-yt-gallery" should exist in the DOM
And ".pre-yt-grid" should be visible
And at least 1 ".pre-yt-card" should be present
```

#### Scenario 5.3: Card thumbnail image is visible on load
```gherkin
Given the YouTube Gallery page loads successfully
When the page reaches network idle state
Then the first ".image-wrapper img" should be visible
And the image should not be a broken image (no 404 on image src)
```

---

### Group 6: Hover-to-Play Video `@smoke`

#### Scenario 6.1: Hovering over a card triggers video playback
```gherkin
Given the YouTube Gallery page is open at the staging URL
And the locale modal is dismissed
When I hover over the first ".pre-yt-card"
Then the ".video-wrapper video" element within that card should become visible
And the video element should have a valid src or srcset attribute
```

#### Scenario 6.2: Video is not playing before hover
```gherkin
Given the YouTube Gallery page is open at the staging URL
And no hover action has been performed
When I inspect ".video-wrapper video" in the first card
Then the video element should not be visible or should have display:none
```

---

### Group 7: No Click Navigation `@smoke`

#### Scenario 7.1: Clicking a card does not navigate away from the page
```gherkin
Given the YouTube Gallery page is open at the staging URL
And the locale modal is dismissed
When I click the first ".pre-yt-card"
Then the browser URL should remain unchanged
And no new page navigation should occur
And the gallery block should still be visible
```

---

## Feature: YouTube Gallery Block — Cross-Browser Compatibility

### Group 8: Cross-Browser `@smoke @compat`

#### Scenario 8.1: Gallery heading and cards are visible in Firefox
```gherkin
Given the YouTube Gallery page is opened in Firefox headless at 1440x900
And the locale modal is dismissed
When the page reaches network idle state
Then "h2.heading-xl" should be visible
And at least 1 ".pre-yt-card" should be present
```

#### Scenario 8.2: Gallery heading and cards are visible in WebKit (Safari)
```gherkin
Given the YouTube Gallery page is opened in WebKit headless at 1440x900
And the locale modal is dismissed
When the page reaches network idle state
Then "h2.heading-xl" should be visible
And at least 1 ".pre-yt-card" should be present
```

---

## Feature: YouTube Gallery Block — Mobile Compatibility

### Group 9: Mobile Viewports `@smoke @mobile`

#### Scenario 9.1: Gallery grid and cards are visible on 375x812 portrait (iPhone)
```gherkin
Given the browser viewport is set to 375x812 (mobile portrait)
And the YouTube Gallery page is open
When the page renders completely
Then ".pre-yt-grid" should be visible
And at least 1 ".pre-yt-card" should be present
And the page should have no horizontal overflow (scrollWidth <= innerWidth)
```

#### Scenario 9.2: Gallery renders correctly in landscape orientation (812x375)
```gherkin
Given the browser viewport is set to 812x375 (mobile landscape)
And the YouTube Gallery page is open
When the page renders completely
Then ".pre-yt-grid" should be visible
And at least 1 ".pre-yt-card" should be present
And the page should have no horizontal overflow
```

#### Scenario 9.3: Gallery heading is visible on mobile
```gherkin
Given the browser viewport is set to 375x812 (mobile portrait)
And the YouTube Gallery page is open
And the locale modal is dismissed
When the page renders completely
Then "h2.heading-xl" should be visible
```

---

## Feature: YouTube Gallery Block — Stock API Integration

### Group 10: Stock API Integration `@smoke @integration`

#### Scenario 10.1: Stock API is called during page load on stage
```gherkin
Given network request interception is active before page navigation
When the YouTube Gallery staging page loads
Then at least one request to "www.stage.adobe.com/stock-api" should be detected
```

#### Scenario 10.2: Stock API returns a 2xx response on stage
```gherkin
Given network request interception is active before page navigation
When the YouTube Gallery staging page loads
And requests to the Stock API endpoint are captured
Then all captured Stock API responses should have HTTP status 2xx (200-299)
And no 4xx or 5xx errors should be returned by the Stock API
```

#### Scenario 10.3: Stage page calls stage Stock API endpoint only (not production)
```gherkin
Given network request interception is active before page navigation
When the YouTube Gallery staging page loads
Then requests to "www.stage.adobe.com/stock-api" should be present
And no requests to "www.adobe.com/stock-api" (production) should be detected
```

---

## Summary

| Group | Tag | Scenarios | Priority |
|---|---|---|---|
| 1 — Heading Validity | @ui | 3 | High |
| 2 — Grid & Card Layout | @ui | 4 | High |
| 3 — Card Metadata | @ui | 5 | High |
| 4 — Page Layout & SEO | @ui | 3 | Medium |
| 5 — Page Load & HTTP | @smoke | 3 | Critical |
| 6 — Hover-to-Play Video | @smoke | 2 | High |
| 7 — No Click Navigation | @smoke | 1 | High |
| 8 — Cross-Browser | @smoke @compat | 2 | High |
| 9 — Mobile Viewports | @smoke @mobile | 3 | Medium |
| 10 — Stock API Integration | @smoke @integration | 3 | High |
| **Total** | | **29** | |

## Automation Coverage

| Tag | Automated | Suite |
|---|---|---|
| @ui | Yes | `tests-yt-gallery/` |
| @smoke | Yes | `tests-yt-smoke/` |
| @compat | Yes | `tests-yt-smoke/test_04_cross_browser.py` |
| @mobile | Yes | `tests-yt-smoke/test_05_mobile.py` |
| @integration | Yes | `tests-yt-smoke/test_06_stock_api.py` |
