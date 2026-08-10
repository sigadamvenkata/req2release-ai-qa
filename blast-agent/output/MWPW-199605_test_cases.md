# Test Cases — MWPW-199605
## Firefly Remove Background — SEO Page Functionality

Format: Gherkin BDD  
Page URL: https://www.adobe.com/products/firefly/features/remove-background.html  
Ticket: MWPW-199605

---

## Feature: Page Load and SEO Elements

### Scenario: Page loads successfully and displays correct title
  Given I open a browser and navigate to "https://www.adobe.com/products/firefly/features/remove-background.html"
  When the page fully loads
  Then the browser tab title contains "Remove Background" and "Firefly" or "Adobe"
  And the page H1 heading is visible and references removing a background with Firefly
  And no 404 or 5xx error is displayed

### Scenario: Page meta description is present for SEO
  Given the remove background SEO page is loaded
  When I inspect the page HTML head section
  Then a meta description tag is present and contains relevant keywords about removing backgrounds
  And the canonical URL tag points to the correct page URL

### Scenario: Page renders correctly on desktop viewport
  Given I open the page in a browser at 1440px viewport width
  When the page loads completely
  Then all sections are visible — marquee, feature blocks, and accordion
  And no horizontal scrollbar appears
  And no layout overflow or clipping is present

---

## Feature: Global Navigation — Login CTA

### Scenario: Login CTA is visible in the Global Navigation (logged-out state)
  Given I am not logged into any Adobe account
  And I navigate to the remove background SEO page
  When I view the Global Navigation bar
  Then a Login or "Sign In" CTA is visible in the navigation
  And the CTA is clearly labelled and distinguishable from other nav items

### Scenario: Clicking Login CTA redirects to Adobe sign-in page
  Given I am not logged in and the remove background page is open
  When I click the Login CTA in the Global Navigation
  Then I am redirected to the Adobe Identity Management sign-in page
  And the redirect URL contains "adobeid" or "account.adobe.com" or equivalent
  And the sign-in page loads without errors

### Scenario: Login CTA is not shown when user is already signed in
  Given I am signed in to my Adobe account
  When I navigate to the remove background SEO page
  Then the Login CTA is replaced by the user profile icon or account indicator
  And no duplicate Login CTA appears in the navigation

---

## Feature: Global Navigation — Firefly Navigation CTA

### Scenario: Firefly navigation CTA is present in the Global Navigation
  Given I navigate to the remove background SEO page
  When I view the Global Navigation bar
  Then a Firefly navigation link or CTA is present
  And it is labelled correctly (e.g. "Firefly" or "Adobe Firefly")

### Scenario: Firefly navigation CTA navigates to the correct Firefly destination
  Given I am on the remove background SEO page
  When I click the Firefly navigation CTA in the Global Navigation
  Then I am taken to the Firefly product page or Firefly web app
  And the destination page loads without errors
  And the URL corresponds to an expected Firefly destination (e.g. firefly.adobe.com or adobe.com/products/firefly)

---

## Feature: Marquee — Title and Branding

### Scenario: Marquee displays the correct Remove Background title
  Given I navigate to the remove background SEO page
  When I view the marquee (hero) section at the top of the page
  Then a prominent heading referencing "remove background" and "Firefly" is visible
  And the title text is correctly spelled with no truncation or clipping

### Scenario: Marquee title is visible on mobile viewport
  Given I view the remove background page at mobile breakpoint (375px–767px)
  When I look at the marquee section
  Then the remove background title is fully visible and not overlapped by other elements
  And the font size is legible on a small screen

---

## Feature: Marquee — Remove Background Animation

### Scenario: Remove background animation plays in the marquee
  Given I navigate to the remove background SEO page
  When the marquee section loads
  Then a remove background animation is visible and plays automatically
  And the animation demonstrates the background removal effect
  And the animation runs smoothly without flickering or freezing

### Scenario: Animation is visible on desktop without user interaction
  Given I am on the page at desktop viewport (1440px+)
  When I do not scroll or interact with the page
  Then the marquee animation plays on its own to give users an overview of the feature
  And the animation does not block or overlap other marquee content

### Scenario: Animation does not cause layout shift during playback
  Given the marquee animation is playing
  When I observe the page layout
  Then no visible layout shift (CLS) occurs during animation playback
  And surrounding text and CTAs remain in their correct positions

---

## Feature: Image Upload Block — Supported Formats

### Scenario: User can upload a valid JPG image via the upload block
  Given I am on the remove background SEO page
  And I locate the Unity image upload block in the marquee
  When I upload a valid JPG file smaller than 40 MB
  Then the image is accepted and loaded into the upload block
  And the remove background process initiates or a preview is shown
  And no error message is displayed

### Scenario: User can upload a valid PNG image via the upload block
  Given I am on the remove background SEO page
  And I locate the Unity image upload block
  When I upload a valid PNG file smaller than 40 MB
  Then the image is accepted and loaded into the upload block
  And the remove background process initiates or a preview is shown
  And no error message is displayed

### Scenario: Upload block accepts drag-and-drop of a valid image
  Given I am on the remove background SEO page
  When I drag and drop a valid JPG or PNG image onto the upload block
  Then the image is accepted
  And the upload block processes it the same as a file picker upload

### Scenario: Upload block accepts images at the 40 MB size boundary
  Given I have a valid JPG file that is exactly at or just below 40 MB
  When I upload it to the image upload block
  Then the image is accepted without error
  And the upload block processes it normally

---

## Feature: Image Upload Block — Error Handling

### Scenario: Uploading an unsupported file format shows an error
  Given I am on the remove background SEO page
  When I attempt to upload a file in an unsupported format (e.g. PDF, GIF, BMP, TIFF, WEBP, SVG)
  Then an error message is displayed to the user
  And the error message clearly communicates that only JPG and PNG formats are accepted
  And the upload block returns to its initial state ready for a new upload

### Scenario: Uploading a file larger than 40 MB shows a size error
  Given I am on the remove background SEO page
  When I attempt to upload an image file that exceeds 40 MB
  Then an error message is displayed to the user
  And the error message indicates that the file size limit is 40 MB
  And the upload block does not proceed with processing the oversized file

### Scenario: Error message disappears when a valid image is uploaded after an error
  Given an error message is displayed due to an invalid upload attempt
  When I upload a valid JPG or PNG file under 40 MB
  Then the error message is dismissed
  And the valid image is accepted and processed normally

### Scenario: Upload block does not accept multiple files simultaneously
  Given I am on the remove background SEO page
  When I attempt to select or drop multiple files at once
  Then only one image is processed
  Or a clear message is shown indicating only single file upload is supported

---

## Feature: Accordion Block — Feature Usage Details

### Scenario: Accordion block with heading "How to remove a background with Adobe Firefly" is present
  Given I navigate to the remove background SEO page
  When I scroll down past the marquee to the feature details section
  Then an accordion block is visible on the page
  And the accordion heading reads "How to remove a background with Adobe Firefly." exactly or substantially

### Scenario: Accordion items expand and collapse correctly
  Given I am viewing the accordion block on the remove background page
  When I click on an accordion item heading
  Then the accordion item expands to reveal its content
  And the content is readable and correctly formatted
  When I click the same heading again
  Then the accordion item collapses and the content is hidden

### Scenario: Only one accordion item is open at a time (if exclusive mode)
  Given the accordion block supports exclusive open mode
  When I open one accordion item and then click a different item
  Then the previously open item collapses
  And the newly clicked item expands
  And no two items are open simultaneously

### Scenario: Accordion block is accessible via keyboard navigation
  Given I am using the keyboard to navigate the page
  When I Tab to an accordion item heading and press Enter or Space
  Then the accordion item expands
  And pressing Enter or Space again collapses it
  And focus remains on the accordion heading after interaction

---

## Feature: Cross-Browser Compatibility

### Scenario: Page renders and functions correctly on Chrome
  Given I open the remove background SEO page in Google Chrome (latest version)
  When I interact with the navigation CTAs, image upload, and accordion
  Then all features work as expected with no browser-specific errors

### Scenario: Page renders and functions correctly on Safari
  Given I open the remove background SEO page in Apple Safari (latest version)
  When I interact with the navigation CTAs, image upload, and accordion
  Then all features work as expected
  And the marquee animation plays correctly on Safari's rendering engine

### Scenario: Page renders and functions correctly on Firefox
  Given I open the remove background SEO page in Mozilla Firefox (latest version)
  When I interact with all page features
  Then all functionality works as expected with no Firefox-specific layout issues

### Scenario: Page renders and functions correctly on Microsoft Edge
  Given I open the remove background SEO page in Microsoft Edge (latest version)
  When I interact with all page features
  Then all functionality works correctly with no Edge-specific issues

---

## Feature: Cross-OS Compatibility

### Scenario: Page works correctly on Windows 11
  Given I access the remove background SEO page from a Windows 11 machine
  When I test all key features — NAV CTAs, upload block, animation, accordion
  Then all features function as expected on Windows 11

### Scenario: Page works correctly on macOS
  Given I access the remove background SEO page from a macOS machine
  When I test all key features
  Then all features function as expected on macOS
  And the marquee animation renders correctly on macOS display rendering

### Scenario: Page is usable on iOS mobile browser
  Given I open the remove background SEO page on an iPhone using Safari (iOS latest)
  When I view and interact with the page at mobile breakpoint
  Then the page layout is correct and all sections are accessible
  And the image upload block is functional on iOS
  And the accordion expands and collapses correctly on touch input

### Scenario: Page is usable on Android mobile browser
  Given I open the remove background SEO page on an Android device using Chrome
  When I view and interact with the page
  Then the page renders correctly at mobile breakpoint
  And all features — upload, accordion, navigation — are functional via touch
