# Test Cases — MWPW-200902: Adobe.com SEO page for Firefly "Remove Background" feature

**Ticket:** [MWPW-200902](https://jira.corp.adobe.com/browse/MWPW-200902)
**Format:** Gherkin BDD
**Generated:** 2026-07-17
**Test Page:** https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html

---

## Feature: Background Generator Marquee — Branding & Copy

### Group 1: Marquee Branding & Heading `@ui`

#### Scenario 1.1: Firefly mnemonic/wordmark is visible above the heading
```gherkin
Given the Background Generator page is open at the staging URL
When the marquee section renders
Then the Firefly logo/mnemonic image should be visible
And the text "Adobe Firefly" should be present near the mnemonic
```

#### Scenario 1.2: H1 heading is visible and non-empty
```gherkin
Given the Background Generator page is open at the staging URL
When the page reaches network idle state
Then the "h1" element should be visible
And the heading text should not be empty
```
> **Note:** Live stage H1 reads "AI background generator: Transform photos in a click." — ticket requests "Adobe Firefly AI background generator: Transform photos in a click" as the H1 text itself. Confirm with reporter whether the mnemonic + wordmark satisfies this or if the H1 copy needs to change.

#### Scenario 1.3: Subheading copy matches ticket requirement
```gherkin
Given the Background Generator page is open at the staging URL
When I read the paragraph following the H1
Then the text should read "From a busy street scene to an alien planet, effortlessly create high-quality, detailed background settings for any image."
```

#### Scenario 1.4: Marquee upload prompt is positioned on the left side of the marquee
```gherkin
Given the Background Generator page is open at the staging URL
When I inspect the layout of the marquee container
Then the upload/heading content block should be positioned left of the hero image on desktop viewports
```

---

## Feature: Background Generator — Upload Block Layout

### Group 2: Upload Block & CTA `@ui`

#### Scenario 2.1: Upload CTA and drop zone are visible
```gherkin
Given the Background Generator page is open at the staging URL
When the ".unity.feature-upload-image" block renders
Then the "Upload your image" CTA should be visible
And the drag-and-drop zone should be visible
```

#### Scenario 2.2: File format guidance text is visible
```gherkin
Given the Background Generator page is open at the staging URL
When I read the text near the upload CTA
Then it should read "File must be JPEG(JPG), PNG, or WEBP and up to 100MB."
```

#### Scenario 2.3: Terms of Use and Privacy Policy links are present
```gherkin
Given the Background Generator page is open at the staging URL
When I inspect the upload block footer text
Then a link to "adobe.com/legal/terms.html" should be present
And a link to "adobe.com/privacy.html" should be present
```

---

## Feature: Background Generator — Image Upload (Valid Formats)

### Group 3: Valid Format Upload via Click CTA `@upload`

#### Scenario 3.1: User can upload a valid JPG via the upload CTA
```gherkin
Given the Background Generator page is open at the staging URL
When I click "Upload your image" and select a valid JPG file (< 100MB, ≥ 512x512px)
Then no error message should be displayed
And an upload-in-progress indicator should appear
```

#### Scenario 3.2: User can upload a valid PNG via the upload CTA
```gherkin
Given the Background Generator page is open at the staging URL
When I click "Upload your image" and select a valid PNG file (< 100MB, ≥ 512x512px)
Then no error message should be displayed
And an upload-in-progress indicator should appear
```

#### Scenario 3.3: User can upload a valid WEBP via the upload CTA
```gherkin
Given the Background Generator page is open at the staging URL
When I click "Upload your image" and select a valid WEBP file (< 100MB, ≥ 512x512px)
Then no error message should be displayed
And an upload-in-progress indicator should appear
```

### Group 4: Valid Format Upload via Drag-and-Drop `@upload`

#### Scenario 4.1: User can upload a valid image via drag and drop
```gherkin
Given the Background Generator page is open at the staging URL
When I drag a valid JPG file and drop it onto the upload drop zone
Then no error message should be displayed
And an upload-in-progress indicator should appear
```

---

## Feature: Background Generator — Image Upload (Errors)

### Group 5: Invalid Format / Size / Dimension Rejection `@upload @error`

#### Scenario 5.1: Unsupported file type shows the file-type error
```gherkin
Given the Background Generator page is open at the staging URL
When I upload a file of an unsupported type (e.g. PDF)
Then the error "We are unable to process this file type. Please try again." should be displayed
```

#### Scenario 5.2: Selecting multiple files shows the file-count error
```gherkin
Given the Background Generator page is open at the staging URL
When I attempt to select more than one file at once for upload
Then the error "Only one file can be uploaded at a time." should be displayed
```

#### Scenario 5.3: A backend/request failure shows the generic request error
```gherkin
Given the Background Generator page is open at the staging URL
And the upload request is simulated to fail (network error or 5xx response)
When I upload a valid image
Then the error "Unable to process the request" should be displayed
```

---

## Feature: Background Generator — Upload Progress ("Splash") UI

### Group 6: Progress Indicator `@upload`

#### Scenario 6.1: Progress/splash indicator appears immediately after file selection
```gherkin
Given the Background Generator page is open at the staging URL
When I select a valid image file for upload
Then a progress/splash indicator should become visible within 1 second
```

#### Scenario 6.2: Progress indicator is dismissed once processing completes
```gherkin
Given the Background Generator page is open at the staging URL
And I have selected a valid image file for upload
When the upload processing completes
Then the progress/splash indicator should no longer be visible
```

---

## Feature: Background Generator — Cross-App Handoff

### Group 7: Redirect to Firefly Product App `@redirect @integration`

#### Scenario 7.1: Successful upload redirects to the Firefly generate/image page
```gherkin
Given the Background Generator page is open at the staging URL
When I upload a valid image and processing completes successfully
Then the browser should navigate to "https://firefly-stage.corp.adobe.com/generate/image"
```

#### Scenario 7.2: The uploaded image is carried over to the Firefly product page
```gherkin
Given a valid image has been uploaded and processed on the Background Generator page
When I land on "https://firefly-stage.corp.adobe.com/generate/image"
Then the uploaded image (or a reference to it) should be present/loaded in the Firefly editor
```

---

## Feature: Background Generator — Page Load & Smoke

### Group 8: Page Load & HTTP Status `@smoke`

#### Scenario 8.1: Page returns HTTP 200
```gherkin
Given the staging URL "https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html"
When a GET request is made to the URL
Then the HTTP response status should be 200
```

#### Scenario 8.2: Upload block is present after page load
```gherkin
Given the Background Generator page loads successfully
When the page reaches network idle state
Then ".unity.feature-upload-image" should exist in the DOM
And the "Upload your image" CTA should be visible
```

---

## Feature: Background Generator — Cross-Browser Compatibility

### Group 9: Cross-Browser `@compat`

#### Scenario 9.1: Marquee and upload block render correctly in Firefox
```gherkin
Given the Background Generator page is opened in Firefox headless at 1440x900
When the page reaches network idle state
Then the "h1" heading should be visible
And the upload CTA should be visible
```

#### Scenario 9.2: Marquee and upload block render correctly in WebKit (Safari)
```gherkin
Given the Background Generator page is opened in WebKit headless at 1440x900
When the page reaches network idle state
Then the "h1" heading should be visible
And the upload CTA should be visible
```

---

## Feature: Background Generator — Mobile Compatibility

### Group 10: Mobile Viewports `@mobile`

#### Scenario 10.1: Upload block renders on 375x812 portrait (iPhone)
```gherkin
Given the browser viewport is set to 375x812 (mobile portrait)
And the Background Generator page is open
When the page renders completely
Then the upload CTA should be visible
And the page should have no horizontal overflow (scrollWidth <= innerWidth)
```

#### Scenario 10.2: Upload block renders in landscape orientation (812x375)
```gherkin
Given the browser viewport is set to 812x375 (mobile landscape)
And the Background Generator page is open
When the page renders completely
Then the upload CTA should be visible
And the page should have no horizontal overflow
```

#### Scenario 10.3: Click-to-upload works on a mobile (Android/iOS) viewport
```gherkin
Given the browser viewport is set to 375x812 (mobile portrait, Android or iOS)
And the Background Generator page is open
When I tap "Upload your image" and select a valid image file
Then no error message should be displayed
And an upload-in-progress indicator should appear
```

---

#### Scenario 11.3: Stage page calls the stage Stock API endpoint only (not production)
```gherkin
Given network request interception is active before page navigation
When I upload a valid image on the staging page
Then requests to the stage Stock API endpoint should be present
And no requests to the production Stock API endpoint should be detected
```

---

## Feature: Background Generator — Accessibility

### Group 12: Baseline Accessibility `@a11y`

#### Scenario 12.1: Hero and card images have meaningful alt text
```gherkin
Given the Background Generator page is open at the staging URL
When I read the "alt" attribute of the marquee hero image
Then the alt attribute should not be null or empty
And the alt text should describe the image content
```

#### Scenario 12.2: Heading hierarchy is valid (single H1, logical H2 order)
```gherkin
Given the Background Generator page is open at the staging URL
When I inspect all heading elements on the page
Then there should be exactly one "h1" element
And subsequent headings should not skip heading levels
```

#### Scenario 12.3: Upload control is keyboard accessible
```gherkin
Given the Background Generator page is open at the staging URL
When I navigate to the upload CTA using the Tab key
Then the upload CTA should receive visible focus
And pressing Enter or Space should open the file picker
```

---

## Summary

| Group | Tag | Scenarios | Priority |
|---|---|---|---|
| 1 — Marquee Branding & Heading | @ui | 4 | High |
| 2 — Upload Block & CTA | @ui | 3 | High |
| 3 — Valid Upload (Click CTA) | @upload | 3 | Critical |
| 4 — Valid Upload (Drag & Drop) | @upload | 1 | High |
| 5 — Invalid Upload / Errors | @upload @error | 5 | Critical |
| 6 — Progress Indicator | @upload | 2 | Medium |
| 7 — Redirect to Firefly App | @redirect @integration | 2 | Critical |
| 8 — Page Load & HTTP | @smoke | 2 | Critical |
| 9 — Cross-Browser | @compat | 2 | High |
| 10 — Mobile Viewports | @mobile | 3 | Medium |
| 11 — Stock API Integration | @integration | 3 | High |
| 12 — Accessibility | @a11y | 3 | Medium |
| **Total** | | **33** | |

## Assumptions & Open Items
- Exact Stock API endpoint hostnames/paths are not stated in the ticket — assumed to follow the `www.stage.adobe.com/stock-api` vs `www.adobe.com/stock-api` pattern used on other Firefly SEO pages. Confirm with dev before automating Group 11.
- Selectors referenced above (e.g. `.unity.feature-upload-image`) come from the raw (pre-JS-decoration) page source fetched 2026-07-17. The rendered DOM (post block-decorator JS) must be inspected via a real browser before writing automation locators.
- Production SEO page URL is not yet defined in this ticket; production-specific scenarios (7.1, 11.3) should be re-pointed once available.
- No screenshots, mockups, or comments were attached to the ticket — all requirements are derived solely from the ticket description text.
