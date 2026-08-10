"""
Locators for the Firefly Background Generator marquee/upload block — MWPW-200902.
All selectors discovered from live rendered-DOM inspection (Playwright, headless
Chromium) of:
  https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html
(fetched 2026-07-17 — re-verify if the block markup changes.)

Key DOM facts:
  Block         : .upload-marquee.unity-enabled  (data-block-status="loaded")
  Left column   : .upload-marquee-left > .upload-marquee-content
                    (mnemonic <img>, "Adobe Firefly" <strong>, <h1>, subheading <p>)
  Right column  : .upload-marquee-right > .upload-marquee-media (hero image)
  Upload block  : .upload-marquee-uploads contains THREE responsive variants of
                  .drop-zone-container — only one is visible at a time, gated by
                  viewport width (confirmed via live resize test):
                    .mobile-up   -> visible only <  600px  wide
                    .tablet-up   -> visible only  600-1199px wide
                    .desktop-up  -> visible only >= 1200px wide
                  Each variant duplicates the same ids (#file-upload) — always
                  scope selectors to the currently-VISIBLE container.
  Splash/progress: .splash-loader (role="dialog", display:none until upload starts)
                  Contains: h2 "Adobe Firefly", body-m "One moment as we take you
                  to Firefly", body-m progress text, and a Cancel CTA.
  Locale modal  : .modal-curtain.is-open — confirmed present & auto-open on load,
                  same pattern as the YouTube Gallery block (MWPW-199796). Must be
                  dismissed before asserting visibility of anything below it.

Confirmed page copy (exact strings, do not rephrase in assertions):
  Format hint : "File must be JPEG(JPG), PNG, or WEBP and up to 100MB."
  Error copy (from the always-present .workflow-upload config block — canonical
  reference text; the *live* toast/error element was not triggered during
  read-only discovery and must be re-confirmed the first time these tests run):
    - "File size larger than 100MB"
    - "Unable to process the request"
    - "We are unable to process this file type. Please try again."
    - "Only one file can be uploaded at a time."
    - "Image is smaller than the minimum dimensions (512 x 512 pixels). Please resize and try again."

NOT YET CONFIRMED (flagged in test docstrings, do not treat as ground truth):
  - Exact Stock API endpoint hostnames/paths for this specific block (no
    stock-api request was observed on plain page load — it likely fires only
    after a successful upload, or on the Firefly product page post-redirect).
  - The exact redirect URL / timing to firefly-stage.corp.adobe.com/generate/image
    (per ticket text only; requires corp network/VPN to verify).
"""

PAGE_URL = "https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html"

# Per ticket MWPW-200902 — not yet confirmed against a live successful upload
FIREFLY_REDIRECT_PATTERN = r"firefly-stage\.corp\.adobe\.com/generate/image"

# ASSUMPTIONS — confirm exact endpoint with dev before trusting these in CI (see test_11_stock_api.py)
STOCK_API_STAGE = "www.stage.adobe.com/stock-api"
STOCK_API_PROD = "www.adobe.com/stock-api"


class L:
    # ── Locale modal ──────────────────────────────────────────────────────────
    MODAL_CURTAIN = ".modal-curtain.is-open"

    # ── Marquee / branding ────────────────────────────────────────────────────
    MARQUEE = ".upload-marquee"
    MARQUEE_LEFT = ".upload-marquee-left"
    MARQUEE_RIGHT = ".upload-marquee-right"
    MARQUEE_CONTENT = ".upload-marquee-content"
    FIREFLY_MNEMONIC = ".upload-marquee-content img[src*='firefly.svg']"
    FIREFLY_WORDMARK = ".upload-marquee-content strong"
    H1 = ".upload-marquee-content h1"
    SUBHEADING = ".upload-marquee-content p:nth-of-type(2)"
    HERO_MEDIA = ".upload-marquee-media img, .upload-marquee-media source"

    # ── Upload block (always scope to the visible breakpoint variant) ───────
    VISIBLE_DROP_ZONE_CONTAINER = ".drop-zone-container:visible"
    DROP_ZONE = ".drop-zone-container:visible .drop-zone"
    UPLOAD_CTA = ".drop-zone-container:visible a.con-button"
    FILE_INPUT = ".drop-zone-container:visible input.file-upload"
    DROP_ZONE_HEADING = ".drop-zone-container:visible .drop-zone-heading"
    DROP_ZONE_BODY = ".drop-zone-container:visible .drop-zone-body"
    TERMS_LINK = ".drop-zone-container:visible a[href*='terms.html']"
    PRIVACY_LINK = ".drop-zone-container:visible a[href*='privacy.html']"

    # ── Errors ────────────────────────────────────────────────────────────────
    # Confirmed live 2026-07-17 by triggering real uploads: the block renders
    # THREE .alert-holder duplicates (one per responsive breakpoint, same
    # pattern as .drop-zone-container) and toggles the "show" class on ALL of
    # them — "show" alone does NOT identify the active one. Only the one in
    # the currently-visible breakpoint variant is actually rendered visible,
    # so the Playwright `:visible` pseudo-class (real rendered visibility,
    # not just the "show" class) is required to scope to the right element.
    ERROR_CANDIDATES = [
        ".alert-holder:visible .alert-text",
        # Fallbacks in case the block markup changes:
        ".error-toast:visible",
        "[class*='error-message']:visible",
        "[role='alert']:visible",
    ]
    # Always-present reference block mapping icon -> error copy (not the live toast)
    ERROR_CONFIG_ITEMS = ".workflow-upload li"

    # ── Splash / upload-progress screen ──────────────────────────────────────
    SPLASH_LOADER = ".splash-loader"
    SPLASH_HEADING = ".splash-loader h2"
    SPLASH_MESSAGE = ".splash-loader .body-m"
    SPLASH_CANCEL_CTA = ".splash-loader a.con-button"

    # ── SEO / accessibility ───────────────────────────────────────────────────
    META_DESCRIPTION = 'meta[name="description"]'
    ALL_HEADINGS = "h1, h2, h3, h4, h5, h6"
