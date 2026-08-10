Feature: YouTube Gallery — Page Load & HTTP Status
  As a QA engineer testing MWPW-199796
  I want to verify the page loads successfully with HTTP 200
  So that the block is accessible in the staging environment

  @smoke @critical
  Scenario 5.1: Page returns HTTP 200
    Given the staging URL for the YouTube Gallery page
    When a GET request is made to the URL
    Then the HTTP response status should be 200
    And the response should not be 404, 500, or an error page

  @smoke @critical
  Scenario 5.2: Gallery block is present after page load
    Given the YouTube Gallery staging page is open
    When the page reaches network idle state
    Then ".prm-yt-gallery" should exist in the DOM
    And ".pre-yt-grid" should be visible
    And at least 1 ".pre-yt-card" should be present

  @smoke @critical
  Scenario 5.3: Card thumbnail image is visible on load
    Given the YouTube Gallery staging page is open
    When the page reaches network idle state
    Then the first ".image-wrapper img" should be visible
    And the image should not be broken (no 404 on image src)
