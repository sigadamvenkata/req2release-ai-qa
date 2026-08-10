Feature: YouTube Gallery — Card Metadata
  As a QA engineer testing MWPW-199796
  I want to verify every card shows correct metadata
  So that gallery cards render all required content

  Background:
    Given the YouTube Gallery staging page is open

  @ui @metadata
  Scenario 3.1: Each card has a unique identifier
    When I read the "id" or "data-id" attribute of each ".pre-yt-card"
    Then no two cards should share the same identifier

  @ui @metadata
  Scenario 3.2: Each card displays a label text
    When I read the text of the label element inside each ".pre-yt-card"
    Then every card should have a non-empty label text

  @ui @metadata
  Scenario 3.3: At least one card displays a free tag
    When I look for ".pre-yt-free-tag" within the gallery
    Then at least one card should contain a visible free tag element

  @ui @metadata
  Scenario 3.4: Each card displays a thumbnail image
    When I inspect ".image-wrapper img" within each ".pre-yt-card"
    Then every card should contain an image element
    And the image "src" attribute should not be empty
    And the first thumbnail image should be visible in the viewport

  @ui @metadata @a11y
  Scenario 3.5: Card thumbnail has a valid alt attribute
    When I read the "alt" attribute of ".image-wrapper img" in each card
    Then the alt attribute should not be null or empty
