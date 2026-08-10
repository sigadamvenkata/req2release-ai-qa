# Feature: Delayed/asynchronous banner load
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: Delayed/asynchronous banner load
  As a QA engineer testing MWPW-203117
  I want to verify the banner appears within an acceptable delay window
  So that automation and users do not treat a normal load delay as a defect

  @delayed_load @smoke
  Scenario: Banner is not present at initial page load
    Given I navigate to a page with an active promo configured
    When the page first finishes loading (DOMContentLoaded)
    Then the Top Promo Banner element may not yet be visible
    And the GNAV is still fully visible and usable

  @delayed_load @smoke
  Scenario: Banner appears within an acceptable wait window
    Given I navigate to a page with an active promo configured
    When I wait up to 5 seconds after page load
    Then the Top Promo Banner becomes visible directly above the GNAV
    And the banner does not take longer than an agreed maximum threshold to appear

  @delayed_load
  Scenario: Page remains usable while the banner is still loading
    Given I navigate to a page with an active promo configured
    When the banner has not yet appeared
    Then the GNAV Sign In control remains present and clickable
    And no blocking overlay prevents interaction with the rest of the page

  @delayed_load
  Scenario: Banner injection does not cause a disruptive layout shift
    Given I navigate to a page with an active promo configured
    When the banner appears after the initial load delay
    Then the GNAV renders below the banner once it appears
    And no content is unexpectedly obscured, overlapped, or cut off

  @delayed_load
  Scenario: Automated checks use explicit waits rather than fixed sleeps
    Given an automated test is asserting on the presence of the Top Promo Banner
    When the test executes
    Then it polls/waits for the banner element up to a defined timeout
    And it does not rely on a fixed unconditional sleep shorter than the observed load delay
