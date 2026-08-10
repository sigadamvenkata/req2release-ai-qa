# Feature: Top Promo Banner rendering and placement
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md

Feature: Top Promo Banner rendering and placement
  As a QA engineer testing MWPW-203117
  I want to verify the Top Promo Banner renders directly above the GNAV
  So that promo content is correctly placed on C2, C1, and other GNAV pages

  @placement @smoke
  Scenario: Banner renders above the GNAV on a C2 page
    Given I navigate to the C2 homepage with an active promo configured
    And I wait up to 5 seconds for the banner to appear
    Then the Top Promo Banner is visible directly above the GNAV
    And the GNAV renders below the banner

  @placement @smoke
  Scenario: Banner renders above the GNAV on a C1 (Creative Cloud) page
    Given I navigate to the C1 Creative Cloud page with an active promo configured
    And I wait up to 5 seconds for the banner to appear
    Then the Top Promo Banner is visible directly above the GNAV

  @placement
  Scenario: Banner renders on other pages using the GNAV or Products mega menu
    Given I navigate to a page that uses the standard GNAV configuration
    And I wait up to 5 seconds for the banner to appear
    When I open the Products mega menu
    Then the Top Promo Banner is visible directly above the GNAV
    And the mega menu does not visually overlap the banner

  @placement
  Scenario: No banner is shown when no promo is active
    Given I navigate to a page with no active promo configured
    And I wait up to 5 seconds
    Then the Top Promo Banner is not rendered
    And the GNAV renders at the top of the page with no layout gap
