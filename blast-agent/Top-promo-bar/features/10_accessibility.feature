# Feature: Accessibility
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: Banner accessibility
  As a QA engineer testing MWPW-203117
  I want to verify the banner is keyboard-navigable and screen-reader friendly
  So that it meets baseline accessibility requirements

  @a11y @smoke
  Scenario: Banner is keyboard navigable
    Given an active promo banner is visible on the page
    When I navigate the page using only the Tab key
    Then focus reaches the banner's CTA in a logical order
    And the focused CTA has a visible focus indicator

  @a11y
  Scenario: Banner passes baseline automated accessibility scan
    Given an active promo banner is visible in both Maximized and Minimized states
    When an accessibility scan (axe-core) is run against the banner region
    Then there are no Critical or Serious violations reported

  @a11y
  Scenario: Banner content is announced correctly by assistive technology
    Given an active promo banner is visible on the page
    When a screen reader traverses the banner
    Then the promo headline, supporting copy, and CTA are announced with meaningful labels
    And the countdown timer, if present, is not read as a distracting live-updating announcement on every tick
