Feature: YouTube Gallery — Page Layout & SEO
  As a QA engineer testing MWPW-199796
  I want to verify SEO meta tags and page structure
  So that the page is crawlable and correctly positioned

  Background:
    Given the YouTube Gallery staging page is open

  @ui @seo
  Scenario 4.1: Page title is non-empty
    When I read the document "<title>" tag
    Then the page title should not be empty

  @ui @seo
  Scenario 4.2: Meta description tag is present and non-empty
    When I query 'meta[name="description"]'
    Then the element should exist in the DOM
    And its "content" attribute should not be empty
    # Known Bug: MWPW-199810 — meta description missing on AEM Live staging

  @ui @layout
  Scenario 4.3: Gallery block is inside the main content area
    When I check the DOM position of ".prm-yt-gallery"
    Then it should be a descendant of the <main> element
    And its bounding box should be within the page scroll area
