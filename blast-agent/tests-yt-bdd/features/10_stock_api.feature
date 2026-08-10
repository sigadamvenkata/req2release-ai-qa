Feature: YouTube Gallery — Stock API Integration
  As a QA engineer testing MWPW-199796
  I want to verify Stock API calls happen on page load
  So that the gallery correctly fetches stock content from the right environment

  @smoke @integration
  Scenario 10.1: Stock API is called during page load on stage
    Given network request interception is active before page navigation
    When the YouTube Gallery staging page loads
    Then at least one request to "www.stage.adobe.com/stock-api" should be detected

  @smoke @integration
  Scenario 10.2: Stock API returns a 2xx response on stage
    Given network request interception is active before page navigation
    When the YouTube Gallery staging page loads
    And requests to the Stock API endpoint are captured
    Then all captured Stock API responses should have HTTP status 2xx (200-299)
    And no 4xx or 5xx errors should be returned

  @smoke @integration
  Scenario 10.3: Stage page calls stage Stock API only (not production)
    Given network request interception is active before page navigation
    When the YouTube Gallery staging page loads
    Then requests to "www.stage.adobe.com/stock-api" should be present
    And no requests to "www.adobe.com/stock-api" (production) should be detected
