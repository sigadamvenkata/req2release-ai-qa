"""
Gallery Locators — MWPW-199796: YouTube Gallery Block
All CSS selectors, URLs, and constants in one place.
To update a selector, change it here — all tests pick it up automatically.
"""

# ── URLs ──────────────────────────────────────────────────────────────────────
PAGE_URL        = "https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery"
STOCK_API_STAGE = "www.stage.adobe.com/stock-api"
STOCK_API_PROD  = "www.adobe.com/stock-api"


class L:
    """CSS selectors for the YouTube Gallery block."""

    # ── Gallery structure ─────────────────────────────────────────────────────
    GALLERY         = ".prm-yt-gallery"          # top-level gallery wrapper
    GRID            = ".pre-yt-grid"             # card grid container
    CARD            = ".pre-yt-card"             # individual gallery card
    HEADING         = "h2.heading-xl"            # gallery heading (h2)
    HEADING_IN_GALLERY = ".prm-yt-gallery h2"   # all h2s inside gallery block

    # ── Card internals ────────────────────────────────────────────────────────
    CARD_THUMBNAIL  = ".image-wrapper img"       # thumbnail image inside card
    CARD_VIDEO      = ".video-wrapper video"     # video element (shown on hover)
    FREE_TAG        = ".pre-yt-free-tag"         # "Free" badge on card
    CARD_LABEL      = ".pre-yt-card-label"       # label / title text on card

    # ── Locale modal (auto-opens, must be dismissed) ──────────────────────────
    MODAL_CURTAIN   = ".modal-curtain.is-open"   # semi-transparent overlay
    LOCALE_MODAL    = "#locale-modal-v2"         # locale selector dialog

    # ── SEO / meta ────────────────────────────────────────────────────────────
    META_DESC       = 'meta[name="description"]' # meta description tag
    META_OG_TITLE   = 'meta[property="og:title"]'

    # ── Page structure ────────────────────────────────────────────────────────
    MAIN_CONTENT    = "main"                     # main content area
