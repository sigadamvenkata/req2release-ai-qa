# Feature: No dismiss control and no session persistence
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: No dismiss control and no session persistence
  As a QA engineer testing MWPW-203117
  I want to verify there is no close button and no dismissal persistence
  So that the banner behaves as specified: no close button, no session management

  @no_dismiss @smoke
  Scenario: Banner has no close/dismiss button
    Given an active promo banner is configured in either Maximized or Minimized state
    When I inspect the banner
    Then no close ("X") or dismiss control is present

  @no_dismiss
  Scenario: Banner reappears on navigation without session persistence
    Given an active promo banner is visible on the current page
    When I navigate to a different page that also has the same promo active
    Then the promo banner is shown again
    And no cookie, localStorage, or sessionStorage state suppresses it
