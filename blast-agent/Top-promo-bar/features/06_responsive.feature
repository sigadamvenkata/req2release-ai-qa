# Feature: Responsive layout
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: Responsive layout
  As a QA engineer testing MWPW-203117
  I want to verify the banner adapts to desktop and mobile viewports
  So that no content is clipped or overflowing on any device

  @responsive @smoke
  Scenario Outline: Banner adapts to viewport size
    Given the viewport is set to "<viewport>"
    And an active promo banner is configured in the "<state>" state
    When I wait up to 5 seconds for the banner to appear
    Then the banner renders without horizontal overflow or clipped text

    Examples:
      | viewport         | state     |
      | 1440x900 desktop | Maximized |
      | 1440x900 desktop | Minimized |
      | 375x812 mobile   | Maximized |
      | 375x812 mobile   | Minimized |
