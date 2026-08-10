Feature: YouTube Gallery — Grid & Card Layout
  As a QA engineer testing MWPW-199796
  I want to verify the card grid renders correctly
  So that the gallery displays in proper grid alignment

  Background:
    Given the YouTube Gallery staging page is open

  @ui @layout
  Scenario 2.1: Gallery grid is visible
    When the page renders completely
    Then the grid container ".pre-yt-grid" should be visible

  @ui @layout
  Scenario 2.2: Gallery contains at least one card
    When the page renders completely
    Then the count of ".pre-yt-card" elements should be >= 1

  @ui @layout
  Scenario 2.3: Cards are arranged in a grid layout
    When I inspect the layout of ".pre-yt-grid"
    Then the CSS display property should be "grid" or "flex"
    And cards should not overflow the grid container horizontally

  @ui @layout
  Scenario 2.4: Each card has a non-zero bounding box
    Given there are multiple ".pre-yt-card" elements
    When I measure the bounding box of each card
    Then each card should have a non-zero width and height
    And card widths should be consistent within a 5px tolerance
