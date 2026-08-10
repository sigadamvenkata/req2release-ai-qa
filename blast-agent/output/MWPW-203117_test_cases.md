# Test Cases — MWPW-203117: [Site Redesign] [Nav] | Top Promo Banner (Not Sticky)

## Feature: Top Promo Banner rendering and placement

### Scenario: Banner renders above the GNAV on a C2 page
  Given I navigate to "www.adobe.com/?georouting=off" with an active promo configured
  When the page finishes loading
  And I wait up to 5 seconds for the banner to appear
  Then the Top Promo Banner is visible directly above the GNAV
  And the GNAV (Products, Use Cases, Solutions, Learn & Support, Plans, Sign In) renders below the banner

### Scenario: Banner renders above the GNAV on a C1 (Creative Cloud) page
  Given I navigate to "www.adobe.com/creativecloud.html?georouting=off" with an active promo configured
  When the page finishes loading
  And I wait up to 5 seconds for the banner to appear
  Then the Top Promo Banner is visible directly above the GNAV
  And the banner content matches the promo configured for that page

### Scenario: Banner renders on other pages using the GNAV or Products mega menu
  Given I navigate to a page that uses the standard GNAV configuration or the Products mega menu
  When the page finishes loading
  And I wait up to 5 seconds for the banner to appear
  Then the Top Promo Banner is visible directly above the GNAV
  And opening the Products mega menu does not visually break or overlap the banner

### Scenario: No banner is shown when no promo is active
  Given I navigate to a page with no active promo configured
  When the page finishes loading
  And I wait up to 5 seconds
  Then the Top Promo Banner is not rendered
  And the GNAV renders at the top of the page with no layout gap

## Feature: Delayed/asynchronous banner load

### Scenario: Banner is not present at initial page load
  Given I navigate to a page with an active promo configured
  When the page first finishes loading (DOMContentLoaded)
  Then the Top Promo Banner element may not yet be visible
  And the GNAV is still fully visible, usable, and not blocked or shifted by a placeholder

### Scenario: Banner appears within an acceptable wait window
  Given I navigate to a page with an active promo configured
  When I wait up to 5 seconds after page load
  Then the Top Promo Banner becomes visible directly above the GNAV
  And the banner does not take longer than an agreed maximum threshold (e.g. 8-10 seconds) to appear

### Scenario: Page remains usable while the banner is still loading
  Given I navigate to a page with an active promo configured
  When the banner has not yet appeared
  Then the GNAV links, Sign In, and Products mega menu remain clickable and functional
  And no loading spinner or blocking overlay prevents interaction with the rest of the page

### Scenario: Banner injection does not cause a disruptive layout shift
  Given I navigate to a page with an active promo configured
  When the banner appears after the initial load delay
  Then the GNAV and page content shift down smoothly to accommodate the banner
  And no content is unexpectedly obscured, overlapped, or cut off by the newly injected banner

### Scenario: Automated checks use explicit waits rather than fixed sleeps
  Given an automated test is asserting on the presence of the Top Promo Banner
  When the test executes
  Then it polls/waits for the banner element (e.g. via an explicit element-wait) up to a defined timeout
  And it does not rely on a fixed unconditional sleep shorter than the observed load delay

## Feature: Maximized and Minimized banner states

### Scenario: Maximized Promo banner matches design
  Given an active "Standard Promo" is configured in the Maximized state
  When I view the page on desktop
  Then the banner shows the product icon, headline, supporting copy, "See terms" link, and "Save now" CTA
  And the layout matches the "Maximized - Light" and "Maximized - Dark" Figma reference frames

### Scenario: Minimized Promo banner matches design
  Given an active "Standard Promo" is configured in the Minimized state
  When I view the page on desktop
  Then the banner collapses to a single-line bar with promo message and CTA
  And the layout matches the "Minimized - Light" and "Minimized - Dark" Figma reference frames

### Scenario: Maximized Feature Release banner matches design
  Given an active "Feature Release" promo (e.g. "Share it all in PDF Spaces") is configured in the Maximized state
  When I view the page on desktop
  Then the banner shows the feature headline, supporting copy, and a "Learn more" (or equivalent) CTA
  And the layout matches the "Maximized Feature Release Banner" Figma reference frames

### Scenario Outline: Banner CTA link navigates correctly
  Given an active promo banner is configured with a "<cta_label>" CTA
  When I click the "<cta_label>" CTA
  Then I am navigated to the expected destination URL for that promo

  Examples:
    | cta_label   |
    | Save now    |
    | See terms   |
    | Learn more  |
    | Get free app|

## Feature: Promo Countdown banner

### Scenario: Countdown timer renders and ticks down
  Given an active "Promo Countdown" banner is configured with a future end time
  When I view the page in the Minimized state
  Then a countdown timer is visible in the format "DD:HH:MM:SS"
  And the countdown value decreases over a 5 second observation window

### Scenario: Countdown banner handles expiry gracefully
  Given an active "Promo Countdown" banner is configured with an end time in the past or about to elapse
  When the countdown reaches zero
  Then the banner does not display a broken or negative time value
  And the banner either hides, freezes at zero, or switches to a non-countdown state without breaking page layout

## Feature: Theming

### Scenario Outline: Banner renders correctly in light and dark themes
  Given the page theme is set to "<theme>"
  And an active promo banner is configured in the "<state>" state
  When the page finishes loading
  Then the banner background, text, and CTA colors match the "<theme>" Figma reference frame for that state

  Examples:
    | theme | state     |
    | light | Maximized |
    | dark  | Maximized |
    | light | Minimized |
    | dark  | Minimized |

## Feature: Responsive layout

### Scenario Outline: Banner adapts to viewport size
  Given the viewport is set to "<viewport>"
  And an active promo banner is configured in the "<state>" state
  When the page finishes loading
  Then the banner renders without horizontal overflow or clipped text
  And the banner layout matches the corresponding mobile/desktop Figma reference frame

  Examples:
    | viewport         | state     |
    | 1440x900 desktop | Maximized |
    | 1440x900 desktop | Minimized |
    | 375x812 mobile   | Maximized |
    | 375x812 mobile   | Minimized |

## Feature: Non-sticky scroll behavior

### Scenario: Banner scrolls off screen with the page
  Given an active promo banner is visible at the top of the page
  When I scroll down the page by one viewport height
  Then the promo banner is no longer visible in the viewport
  And the banner does not reappear or re-pin while scrolling further down

### Scenario: Banner does not reserve fixed/sticky space during scroll
  Given an active promo banner is visible at the top of the page
  When I scroll down and then back up to the top of the page
  Then the promo banner reappears in its original position
  And no duplicate or ghost banner element remains fixed on screen during the scroll

## Feature: No dismiss control and no session persistence

### Scenario: Banner has no close/dismiss button
  Given an active promo banner is configured in either Maximized or Minimized state
  When I inspect the banner
  Then no close ("X") or dismiss control is present

### Scenario: Banner reappears on navigation without session persistence
  Given an active promo banner is visible on the current page
  When I navigate to a different page that also has the same promo active
  Then the promo banner is shown again
  And no cookie, localStorage, or sessionStorage state is used to suppress it

## Feature: WW rollout and RTL support

### Scenario: Banner renders correctly in an RTL locale
  Given the site locale is set to a right-to-left language (e.g. Arabic)
  When I view a page with an active promo banner
  Then the banner layout is mirrored correctly (icon, text, and CTA order flow right-to-left)
  And no text is clipped, overlapped, or rendered out of its container

### Scenario: Banner renders correctly in a non-English LTR locale
  Given the site locale is set to a non-English left-to-right language
  When I view a page with an active promo banner
  Then the banner text is fully translated/localized
  And the layout matches the equivalent English reference frame

## Feature: Accessibility

### Scenario: Banner is keyboard navigable
  Given an active promo banner is visible on the page
  When I navigate the page using only the Tab key
  Then focus moves through the banner's interactive elements (CTA link/button) in a logical order
  And each focused element has a visible focus indicator

### Scenario: Banner passes baseline automated accessibility scan
  Given an active promo banner is visible in both Maximized and Minimized states
  When an accessibility scan (e.g. axe-core) is run against the banner region
  Then there are no Critical or Serious violations reported

### Scenario: Banner content is announced correctly by assistive technology
  Given an active promo banner is visible on the page
  When a screen reader traverses the banner
  Then the promo headline, supporting copy, and CTA are announced with meaningful labels
  And the countdown timer (if present) is not read as a distracting live-updating announcement on every tick
