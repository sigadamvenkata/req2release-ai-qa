Feature: YouTube Gallery — Heading Validity
  As a QA engineer testing MWPW-199796
  I want to verify the gallery heading is correct
  So that content authors know the heading renders properly

  Background:
    Given the YouTube Gallery staging page is open
    And the locale modal is dismissed

  @ui @heading
  Scenario 1.1: Gallery heading is visible on page load
    When the page reaches network idle state
    Then the element "h2.heading-xl" should be visible in the viewport

  @ui @heading
  Scenario 1.2: Gallery heading contains non-empty text
    When I read the text content of "h2.heading-xl"
    Then the heading text should not be empty
    And the heading text should contain meaningful content

  @ui @heading
  Scenario 1.3: Only one H2 heading exists in the gallery block
    When I count all "h2" elements within ".prm-yt-gallery"
    Then there should be exactly 1 H2 heading element
