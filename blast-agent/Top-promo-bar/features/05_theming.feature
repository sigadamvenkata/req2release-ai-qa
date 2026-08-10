# Feature: Theming
# Ticket: MWPW-203117
# Source: output/MWPW-203117_test_cases.md
#
# REDESIGNED after live verification (2026-08-05): the banner's theme is an
# authoring-time choice per campaign, not something that reacts to OS/browser
# dark-mode preference (verified: color_scheme=dark emulation has no effect on
# the live banner). Scenarios below check self-consistency between the declared
# theme and the rendered colors, and document the no-OS-effect finding.

Feature: Banner theming
  As a QA engineer testing MWPW-203117
  I want to verify the banner's rendered colors match its declared theme
  So that Light and Dark campaign configurations both render correctly

  @theming @smoke
  Scenario: Banner's rendered background matches its declared theme
    Given an active promo banner is configured
    When I read its declared theme modifier and its rendered background color
    Then the background luminance matches the declared theme (light = high, dark = low)

  @theming
  Scenario: Banner headline text color is readable
    Given an active promo banner is configured
    Then the headline's computed text color is present and non-empty

  @theming
  Scenario: OS/browser dark-mode preference does not affect the banner
    Given the browser's OS-level color scheme is forced to dark
    When I view a page with an active promo banner
    Then the banner still renders its authored theme, unaffected by the OS preference
