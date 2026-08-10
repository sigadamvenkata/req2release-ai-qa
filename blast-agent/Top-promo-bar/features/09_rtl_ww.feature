# Feature: WW rollout and RTL support
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: WW rollout and RTL support
  As a QA engineer testing MWPW-203117
  I want to verify the banner supports worldwide rollout including RTL locales
  So that non-English and right-to-left users see a correctly mirrored, localized banner

  @rtl @smoke
  Scenario: RTL locale page renders with dir="rtl"
    Given I navigate to the real RTL locale URL (not just a browser locale header)
    Then the page's <html> element has dir="rtl"

  @rtl @smoke
  Scenario: Banner renders correctly in an RTL locale
    Given the site locale is set to a right-to-left language
    When I view a page with an active promo banner
    Then the banner layout is mirrored correctly
    And no text is clipped, overlapped, or rendered out of its container

  @rtl
  Scenario: Banner renders correctly in a non-English LTR locale
    Given the site locale is set to a non-English left-to-right language
    When I view a page with an active promo banner
    Then the banner text is fully translated/localized
    And the layout matches the equivalent English reference frame
