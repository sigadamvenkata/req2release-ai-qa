# Feature: Non-sticky scroll behavior
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: Non-sticky scroll behavior
  As a QA engineer testing MWPW-203117
  I want to verify the banner scrolls off screen with the page
  So that it behaves as "Not Sticky" per the ticket title

  @scroll @smoke
  Scenario: Banner scrolls off screen with the page
    Given an active promo banner is visible at the top of the page
    When I scroll down the page by one viewport height
    Then the promo banner is no longer visible in the viewport

  @scroll
  Scenario: Banner does not reserve fixed/sticky space during scroll
    Given an active promo banner is visible at the top of the page
    When I scroll down and then back up to the top of the page
    Then the promo banner reappears in its original position
    And no duplicate or ghost banner element remains fixed on screen
