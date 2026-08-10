# Feature: Maximized and Minimized banner states
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: Maximized and Minimized banner states
  As a QA engineer testing MWPW-203117
  I want to verify the banner's content and CTAs in both display states
  So that the Standard Promo, Promo Countdown, and Feature Release variants match Figma

  @states @smoke
  Scenario: Maximized Promo banner matches design
    Given an active "Standard Promo" is configured in the Maximized state
    When I view the page on desktop
    Then the banner shows the product icon, headline, supporting copy, "See terms" link, and "Save now" CTA

  @states
  Scenario: Minimized Promo banner matches design
    Given an active "Standard Promo" is configured in the Minimized state
    When I view the page on desktop
    Then the banner collapses to a single-line bar with promo message and CTA

  @states
  Scenario: Maximized Feature Release banner matches design
    Given an active "Feature Release" promo is configured in the Maximized state
    When I view the page on desktop
    Then the banner shows the feature headline, supporting copy, and a "Learn more" CTA

  @states
  Scenario Outline: Banner CTA link navigates correctly
    Given an active promo banner is configured with a "<cta_label>" CTA
    When I click the "<cta_label>" CTA
    Then I am navigated to the expected destination URL for that promo

    Examples:
      | cta_label    |
      | Save now     |
      | See terms    |
      | Learn more   |
      | Get free app |
