# Feature: Promo Countdown banner
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: Promo Countdown banner
  As a QA engineer testing MWPW-203117
  I want to verify the countdown timer variant ticks and expires correctly
  So that time-limited promos display accurate, non-broken countdowns

  @countdown @smoke
  Scenario: Countdown timer renders and ticks down
    Given an active "Promo Countdown" banner is configured with a future end time
    When I view the page in the Minimized state
    Then a countdown timer is visible in the format "DD:HH:MM:SS"
    And the countdown value decreases over a 5 second observation window

  @countdown
  Scenario: Countdown banner handles expiry gracefully
    Given an active "Promo Countdown" banner is configured with an end time about to elapse
    When the countdown reaches zero
    Then the banner does not display a broken or negative time value
    And the banner either hides, freezes at zero, or switches to a non-countdown state without breaking page layout
