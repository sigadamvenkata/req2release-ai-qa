"""
Top Promo Banner Locators — MWPW-203117: [Site Redesign][Nav] Top Promo Banner (Not Sticky)

UPDATE (2026-08-05, verified against live www.adobe.com): a promo bar component
already exists in production under Adobe's "feds-" (federated nav) naming — this is
almost certainly the PRE-redesign component that MWPW-203117 (still in Draft) will
extend. Selectors below were captured directly from the live DOM and are now the
primary/authoritative selectors, replacing the earlier `.top-promo-banner` guesses.

What was verified live (C2 homepage, www.adobe.com):
  - Banner loads asynchronously ~1-2s after DOMContentLoaded (comfortably inside our
    5-10s wait window).
  - Markup: .feds-promo-aside-wrapper > .feds-promo-bar (role="region",
    aria-label="Promotion", daa-lh="promo-bar") containing icon, eyebrow label,
    h2 headline, body copy with inline "See terms" link, and a.feds-primary-cta.
  - State ("--maximized") and theme ("--light") are BEM modifier classes on the
    SAME .feds-promo-bar element, not separate elements.
  - No close button in the DOM — matches the ticket's "no close button" requirement.
  - Renders identically at 375x812 mobile — responsive markup is shared.
  - GNAV is <header class="global-navigation ..."> ; it gains "has-promo
    feds-promo-showing" classes when a promo is active.
  - The promo campaign is currently only configured on the C2 homepage — it was
    NOT present on the C1 Creative Cloud page or on an RTL locale URL
    (www.adobe.com/ae_ar/) at the time of writing. That's a content/campaign
    configuration fact, not a selector bug — tests should skip, not fail, when a
    page has no active promo.
  - OS/browser dark-mode emulation (`color_scheme: dark`) has NO effect on the
    banner — it stayed `feds-promo-bar--light` regardless. Theme is an
    authoring-time choice per campaign, not a client-adaptive property. Theming
    tests were redesigned around this (see specs/test_05_theming.py).

FINDING — likely a real gap, not a script bug: `.feds-promo-aside-wrapper` is
`position: fixed` and its bounding box was IDENTICAL before and after a 2000px
scroll — i.e. the live banner is sticky. This conflicts with the ticket's
"(Not Sticky)" requirement (see MWPW-203117_test_plan.md Risks & Mitigations).
Feature 7 scroll-behavior tests intentionally assert the *required* non-sticky
behavior, so they will keep failing against this component until MWPW-203117 ships.

Still unverified — no live example found, kept as documented placeholders:
  - Minimized state markup (only "--maximized" observed).
  - Dark theme markup (only "--light" observed).
  - Countdown timer markup (no live countdown promo found).
  - Minimized-state chevron controls (not present on the Maximized example).
"""

# ── URLs ──────────────────────────────────────────────────────────────────────
C2_URL = "https://www.adobe.com/?georouting=off"                          # verified: promo bar live here
C1_URL = "https://www.adobe.com/creativecloud.html?georouting=off"        # verified: no active promo here as of 2026-08-05
RTL_URL = "https://www.adobe.com/ae_ar/?georouting=off"                   # verified dir="rtl" lang="ar"; no active promo here as of 2026-08-05
INTL_URL = "https://www.adobe.com/fr/?georouting=off"                     # French (non-English LTR); no active promo here as of 2026-08-05
NO_PROMO_URL = C1_URL                                                      # best current stand-in for "no active promo" until a dedicated stage flag is known


class L:
    """CSS selectors for the Top Promo Banner and the GNAV it sits above."""

    # ── Banner container & state (verified live) ──────────────────────────────
    BANNER               = ".feds-promo-bar, [daa-lh='promo-bar']"
    BANNER_WRAPPER       = ".feds-promo-aside-wrapper"                     # the actual `position: fixed` element
    BANNER_MAXIMIZED     = ".feds-promo-bar.feds-promo-bar--maximized"     # verified
    BANNER_MINIMIZED     = ".feds-promo-bar.feds-promo-bar--minimized"     # UNVERIFIED — inferred naming, no live example found

    # ── Banner content (verified) ────────────────────────────────────────────
    PRODUCT_ICON         = "img.feds-promo-bar-icon"
    PROMO_LABEL          = "p.feds-promo-bar-product"                      # eyebrow text, e.g. "Limited-time offer"
    HEADLINE             = "h2.feds-promo-bar-headline"
    SUPPORTING_COPY      = "p.feds-promo-bar-body"
    SEE_TERMS_LINK       = ".feds-promo-bar-body a"
    PRIMARY_CTA          = "a.feds-primary-cta"
    COUNTDOWN            = ".feds-promo-bar-countdown, [class*='countdown']"  # UNVERIFIED — no live countdown promo found

    # ── Minimized-state controls — UNVERIFIED, not present on the live Maximized
    #    example inspected; behavior also unconfirmed in the ticket itself ─────
    CHEVRON_LEFT         = ".feds-promo-bar button[aria-label*='previous' i]"
    CHEVRON_RIGHT        = ".feds-promo-bar button[aria-label*='next' i]"

    # ── Absent-by-design control — verified NOT present live, matching the
    #    ticket's "no close button" requirement ───────────────────────────────
    CLOSE_BUTTON         = ".feds-promo-bar button[aria-label*='close' i], .feds-promo-bar button:has-text('×')"

    # ── Theming (modifier lives on the same node as BANNER/BANNER_WRAPPER) ───
    THEME_LIGHT          = ".feds-promo-bar--light"
    THEME_DARK           = ".feds-promo-bar--dark"                         # UNVERIFIED — only light observed live

    # ── GNAV (verified: header.global-navigation, gains "has-promo
    #    feds-promo-showing" classes when a promo is active) ──────────────────
    GNAV                 = "header.global-navigation"
    GNAV_HAS_PROMO_CLASS = "has-promo"
    GNAV_PRODUCTS_TRIGGER = "header.global-navigation button[aria-controls='products']"
    GNAV_MEGA_MENU       = "[class*='feds-popup'], [class*='mega-menu']"
    GNAV_SIGN_IN         = "button.profile-comp.secondary-button"

    # ── Document root (theming / RTL checks) ──────────────────────────────────
    HTML_ROOT            = "html"
