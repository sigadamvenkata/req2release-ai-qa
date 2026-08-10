Feature: YouTube Gallery — Mobile Compatibility
  As a QA engineer testing MWPW-199796
  I want to verify the gallery renders correctly on mobile viewports
  So that Android and iOS users can view the gallery without issues

  @smoke @mobile
  Scenario 9.1: Gallery grid and cards visible on 375x812 portrait (iPhone)
    Given the browser viewport is set to 375x812 mobile portrait
    And the YouTube Gallery staging page is open
    When the page renders completely
    Then ".pre-yt-grid" should be visible
    And at least 1 ".pre-yt-card" should be present
    And the page should have no horizontal overflow (scrollWidth <= innerWidth)

  @smoke @mobile
  Scenario 9.2: Gallery renders correctly in landscape orientation (812x375)
    Given the browser viewport is set to 812x375 mobile landscape
    And the YouTube Gallery staging page is open
    When the page renders completely
    Then ".pre-yt-grid" should be visible
    And at least 1 ".pre-yt-card" should be present
    And the page should have no horizontal overflow

  @smoke @mobile
  Scenario 9.3: Gallery heading is visible on mobile portrait
    Given the browser viewport is set to 375x812 mobile portrait
    And the YouTube Gallery staging page is open
    And the locale modal is dismissed
    When the page renders completely
    Then "h2.heading-xl" should be visible
