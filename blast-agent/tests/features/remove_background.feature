# Feature: Firefly Remove Background SEO Page
# Ticket: MWPW-199605
# URL: https://www.adobe.com/products/firefly/features/remove-background.html

Feature: Firefly Remove Background SEO Page
  As a QA engineer
  I want to verify the Remove Background SEO page works correctly
  So that users can discover and use the Firefly background removal feature

  Background:
    Given I open the Remove Background SEO page

  # ─────────────────────────────────────────────
  # PAGE LOAD & SEO
  # ─────────────────────────────────────────────

  @seo @smoke
  Scenario: Page loads with correct browser title
    Then the page title contains "Remove Background"
    And the page title contains "Firefly"

  @seo
  Scenario: Page has a meta description for SEO
    Then the meta description is present and not empty

  @seo
  Scenario: Page has a canonical URL tag
    Then the canonical URL tag is present

  @seo @smoke
  Scenario: Page H1 heading is visible
    Then the H1 heading is visible on the page
    And the H1 text contains "remove" and "background"

  @seo
  Scenario: Page renders without layout overflow on desktop
    Given the viewport is set to 1440 x 900
    Then the page is visible with no horizontal scrollbar

  # ─────────────────────────────────────────────
  # GLOBAL NAVIGATION — SIGN IN CTA
  # ─────────────────────────────────────────────

  @navigation @smoke
  Scenario: Sign In CTA is visible in the navigation when logged out
    Then the Sign In button is visible in the Global Navigation

  @navigation
  Scenario: Sign In button has the correct label
    Then the Sign In button text is "Sign in"

  @navigation
  Scenario: Clicking Sign In redirects to Adobe login page
    When I click the Sign In button
    Then the current URL contains "adobeid" or "account.adobe.com" or "auth"

  # ─────────────────────────────────────────────
  # GLOBAL NAVIGATION — FIREFLY CTA
  # ─────────────────────────────────────────────

  @navigation @smoke
  Scenario: Firefly CTA is visible in the navigation
    Then the Firefly navigation CTA is visible

  @navigation
  Scenario: Firefly CTA links to the correct destination
    Then the Firefly CTA href contains "firefly"

  # ─────────────────────────────────────────────
  # MARQUEE — TITLE & ANIMATION
  # ─────────────────────────────────────────────

  @marquee @smoke
  Scenario: Marquee displays remove background heading
    Then the H1 heading is visible on the page

  @marquee
  Scenario: Animation video element is present in the marquee
    Then at least one video element is present on the page

  # ─────────────────────────────────────────────
  # IMAGE UPLOAD — HAPPY PATH
  # ─────────────────────────────────────────────

  @upload @smoke
  Scenario: Upload zone is visible on the page
    Then the image upload drop zone is visible

  @upload
  Scenario: User can upload a valid JPG image
    When I upload the file "valid_jpg.jpg"
    Then no error message is displayed
    And the reupload button becomes visible

  @upload
  Scenario: User can upload a valid PNG image
    When I upload the file "valid_png.png"
    Then no error message is displayed
    And the reupload button becomes visible

  @upload
  Scenario: User can upload a valid WEBP image
    When I upload the file "valid_webp.webp"
    Then no error message is displayed
    And the reupload button becomes visible

  # ─────────────────────────────────────────────
  # IMAGE UPLOAD — ERROR HANDLING
  # ─────────────────────────────────────────────

  @upload @error
  Scenario: Uploading a PDF shows an error message
    When I upload the file "invalid_pdf.pdf"
    Then an error message is displayed to the user

  @upload @error
  Scenario: Uploading a HEIC file shows an error message
    When I upload the file "invalid_heic.heic"
    Then an error message is displayed to the user

  # ─────────────────────────────────────────────
  # ACCORDION BLOCK
  # ─────────────────────────────────────────────

  @accordion @smoke
  Scenario: How to remove background H2 heading is present
    Then the page contains the H2 heading "How to remove a background with Adobe Firefly"

  @accordion
  Scenario: Accordion items are present on the page
    Then at least one accordion trigger is visible

  @accordion
  Scenario: Accordion item expands when clicked
    When I click the first accordion trigger
    Then the first accordion item is expanded

  @accordion
  Scenario: Accordion item collapses when clicked again
    When I click the first accordion trigger
    And I click the first accordion trigger again
    Then the first accordion item is collapsed
