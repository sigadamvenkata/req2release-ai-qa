# Test Plan — MWPW-203117: [Site Redesign] [Nav] | Top Promo Banner (Not Sticky)

## Objective
Validate the new Top Promo Banner that surfaces marketing promos (standard promo, promo with countdown, and feature-release promo) above the C2/C1 global navigation on adobe.com. The banner must render correctly in its Maximized and Minimized states, support light and dark themes, work across desktop/tablet/mobile viewports, support WW rollout including RTL locales, scroll off with the page (non-sticky, no pinning, no dismiss/session state), and meet accessibility requirements — ahead of the BTS promo go-live on 8/17.

## Scope

### In Scope
- Top Promo Banner rendering directly above the GNAV on:
  - C2 pages using the standard GNAV (e.g. `www.adobe.com`)
  - C1 pages using the Creative Cloud nav (e.g. `www.adobe.com/creativecloud.html`)
  - Any additional page using the GNAV configuration or the Products mega menu
- Three banner content variants per the Figma:
  - **Standard Promo** (e.g. "Save 50% for Black Friday")
  - **Promo Countdown** (same as standard + live DD:HH:MM:SS countdown timer)
  - **Feature Release** (e.g. "Share it all in PDF Spaces", "Introducing Color Mode")
- Two display states: **Maximized** (full promo copy + hero-adjacent CTA) and **Minimized** (single-line collapsed banner)
- Light theme and Dark theme rendering for both states and all variants
- Responsive behavior: Desktop, and Mobile (per Figma minimized/maximized mobile frames)
- Non-sticky scroll behavior — banner (and nav) scrolls off-screen with page scroll, no fixed/pinned positioning
- Absence of a close/dismiss control and absence of any session/cookie-based "already dismissed" persistence
- In-banner interactive elements: promo message link/CTA (e.g. "See terms", "Save now", "Learn more", "Get free app"), and any expand/collapse chevron controls shown in the Minimized frames
- Countdown timer accuracy, format, and expiry behavior (variant 3)
- Delayed/asynchronous banner load — banner is not present at initial page load and appears ~5 seconds later; verify it eventually renders within an acceptable wait window and does not break the page while loading
- RTL layout mirroring for WW/RTL locales
- Baseline accessibility checks (keyboard nav, focus order, contrast, screen reader labeling, reduced-motion for countdown)

### Out of Scope
- Authoring/CMS workflow used to configure promo content (Franklin/AEM authoring side)
- Promo scheduling/targeting logic (geo, entitlement, A/B) beyond confirming the banner renders when active
- Visual/pixel-perfect design QA beyond the four supplied Figma reference frames
- Regression of unrelated GNAV/mega-menu functionality not touched by this banner
- Performance/load testing

## Test Strategy
- **Design-driven functional testing**: Use the four Figma reference frames (Maximized Promo, Minimized Promo, Minimized Promo Countdown, Maximized Feature Release) as the source of truth for layout, copy placement, and CTA styling in each theme/state.
- **Page Object Model + Playwright (Python)**, following the existing suite pattern (`tests/` for Remove Background, `tests-yt-*` for YouTube Gallery): add a new `tests-promo-banner/` suite with `locators.py` (PromoBannerLocators), `pages/promo_banner_page.py`, and Gherkin `.feature` files consumed via `pytest-bdd`.
- **Cross-browser matrix**: Chromium, Firefox, WebKit — headless, matching existing suites.
- **Cross-viewport matrix**: Desktop 1440×900, Mobile 375×812 portrait (per existing mobile pattern), plus 812×375 landscape as a secondary check.
- **Theme matrix**: force/verify both `light` and `dark` theme contexts (via system `prefers-color-scheme` or the page's theme toggle, whichever the implementation exposes).
- **Manual + exploratory pass**: scroll behavior, countdown live-tick accuracy, and RTL mirroring are easier to verify with a quick manual check per browser before automating, since these are novel to this component.
- **Delayed-load handling**: the banner is expected to load asynchronously, appearing roughly 5 seconds after initial page load rather than being present in the initial DOM. All automation must use an explicit wait (e.g. Playwright `wait_for_selector(..., timeout=10000)` / polling assertion) for the banner element rather than asserting immediately on page load, to avoid false negatives. Manual/exploratory checks will also confirm the page and GNAV remain fully usable during the pre-load window.
- **Accessibility pass**: axe-core (or Playwright's built-in accessibility snapshot) scan on the banner region in both states/themes, plus manual keyboard/tab-order and screen-reader spot check.
- Any deviation between the live implementation and the Figma frames (e.g. the exact behavior of the chevron controls on the Minimized variant, which is not explained in the ticket description) will be logged as a **finding/question for design/dev**, not assumed.

## Entry Criteria
- Feature branch/preview build deployed to a stage/preview URL with the promo banner enabled for at least one C2 page and one C1 page
- Figma designs (4 reference frames, attached to MWPW-203117) available and unchanged from what was reviewed
- Test promo content configured for all three variants (standard, countdown, feature release) in both themes
- `www.adobe.com/?georouting=off` and `www.adobe.com/creativecloud.html?georouting=off` (or stage equivalents) reachable without VPN/geo restrictions blocking the promo

## Exit Criteria
- All P1 (banner renders, correct placement above nav, non-sticky scroll, no close button, no session persistence, CTA links work) test cases pass on Chromium, Firefox, and WebKit
- No open Blocker/Critical defects against banner rendering, layout, or CTA functionality
- Light/dark theme and desktop/mobile layouts match the Figma reference frames within agreed visual tolerance
- Countdown timer ticks correctly and handles expiry without breaking layout
- Baseline accessibility scan shows no Critical/Serious violations on the banner region
- Banner consistently appears within an acceptable wait window (~5s, not exceeding an agreed max threshold) after page load, on every browser/viewport combination, without errors or layout breakage during the pre-load window
- Any open questions (chevron behavior, RTL mirror confirmation) have been answered by design/dev and re-verified, or explicitly deferred with sign-off

## Test Environment
- **URLs**: `www.adobe.com/?georouting=off` (C2), `www.adobe.com/creativecloud.html?georouting=off` (C1), plus one additional GNAV/mega-menu page
- **Browsers**: Chromium, Firefox, WebKit (headless, per existing suite convention)
- **Viewports**: 1440×900 (desktop), 375×812 (mobile portrait), 812×375 (mobile landscape)
- **Themes**: Light, Dark
- **Locales**: en-US (primary), one LTR non-English locale, one RTL locale (e.g. ar) for WW/RTL verification
- **Framework**: pytest + Playwright (Python), pytest-bdd for Gherkin, pytest-html + Allure reporting (consistent with existing suites)
- **Test data**: Stage-configured promo content for Standard, Countdown, and Feature Release variants

## Risks & Mitigations
| Risk | Mitigation |
|---|---|
| Ticket is still in **Draft** status and has no comments — some behavior (e.g. minimized-state chevron controls, whether the banner can be manually collapsed by the user) is inferred from Figma only, not explicit in the description | Log an open question to the reporter/PdM (Robert Repass / Cindy James) before finalizing automated assertions on chevron behavior; treat as exploratory until confirmed |
| "Not Sticky" + "locked to top of page and scrolls off when user scrolls" appears to describe the **NAV**, not explicitly the promo banner itself — ambiguity on whether banner and nav scroll together or independently | Verify actual scroll behavior against the live build first; write test assertions from observed behavior, flag any mismatch with the ticket wording as a finding |
| No close button + no session management means the banner will show on every page load — could be seen as a UX regression if promo is dismissed but reappears on navigation | Explicitly test and confirm this is intended (per ticket) so it isn't mistakenly filed as a bug |
| RTL and WW rollout support is broad (many locales) but no locale list is attached to the ticket | Scope automated RTL coverage to one representative RTL locale and one representative LTR non-English locale; flag full WW locale matrix as a follow-up if required |
| BTS promo go-live is 8/17 with GNAV rollout on 7/13 — tight timeline for a net-new nav component | Prioritize P1 rendering/placement/CTA test cases first; defer deep accessibility/RTL edge cases if timeline is at risk, with explicit sign-off |
| Countdown timer is time-based and can be flaky in automated tests (race conditions, timezone handling) | Assert on format and monotonic decrease rather than exact second-level values; test expiry behavior with a stage-configured near-expired countdown |
| Banner loads asynchronously (~5s after page load, not immediately in the DOM) — tests asserting on it too early will fail intermittently, and the delay itself could be perceived as a layout-shift/UX issue | Use explicit waits (not fixed `sleep`) with a generous timeout in all automated checks; add a dedicated test asserting the banner appears within an agreed max threshold; confirm with dev whether the delay is expected/by-design and whether it causes a CLS (layout shift) once the banner injects above the GNAV |
