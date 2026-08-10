Feature: YouTube Gallery — Hover-to-Play Video
  As a QA engineer testing MWPW-199796
  I want to verify that hovering over a card plays the video
  So that the interactive video behaviour works correctly

  Background:
    Given the YouTube Gallery staging page is open
    And the locale modal is dismissed

  @smoke @functional
  Scenario 6.1: Hovering over a card triggers video playback
    When I hover over the first ".pre-yt-card"
    Then the ".video-wrapper video" element should become visible
    And the video element should have a valid src attribute

  @smoke @functional
  Scenario 6.2: Video is hidden before hover
    Given no hover action has been performed
    When I inspect ".video-wrapper video" in the first card
    Then the video element should not be visible (display:none or hidden)
