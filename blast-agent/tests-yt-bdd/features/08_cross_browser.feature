Feature: YouTube Gallery — Cross-Browser Compatibility
  As a QA engineer testing MWPW-199796
  I want to verify the gallery works in Firefox and WebKit (Safari)
  So that the block is accessible across all major browsers

  @smoke @compat
  Scenario 8.1: Gallery heading and cards visible in Firefox
    Given the YouTube Gallery page is opened in Firefox headless at 1440x900
    And the locale modal is dismissed
    When the page reaches network idle state
    Then "h2.heading-xl" should be visible
    And at least 1 ".pre-yt-card" should be present

  @smoke @compat
  Scenario 8.2: Gallery heading and cards visible in WebKit (Safari)
    Given the YouTube Gallery page is opened in WebKit headless at 1440x900
    And the locale modal is dismissed
    When the page reaches network idle state
    Then "h2.heading-xl" should be visible
    And at least 1 ".pre-yt-card" should be present
