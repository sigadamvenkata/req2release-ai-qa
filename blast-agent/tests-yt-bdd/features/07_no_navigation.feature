Feature: YouTube Gallery — No Click Navigation
  As a QA engineer testing MWPW-199796
  I want to verify that clicking a card does not navigate away
  So that the gallery stays on the same page after card interaction

  Background:
    Given the YouTube Gallery staging page is open
    And the locale modal is dismissed

  @smoke @functional
  Scenario 7.1: Clicking a card does not navigate away from the page
    When I record the current browser URL
    And I click the first ".pre-yt-card"
    Then the browser URL should remain unchanged
    And no new page navigation should occur
    And the gallery block should still be visible
