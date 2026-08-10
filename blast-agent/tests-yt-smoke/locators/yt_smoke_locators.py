"""
Locators for the YouTube Gallery @smoke test suite — MWPW-199796
All selectors discovered from live DOM inspection of:
  https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery

Key DOM facts:
  Gallery block   : .prm-yt-gallery
  Grid container  : .pre-yt-grid
  Card            : .pre-yt-card  (data-template-id = unique ID)
  Card thumbnail  : .image-wrapper img
  Card video      : .video-wrapper video  (paused on load; plays on hover)
  Free tag        : .pre-yt-free-tag
  Heading         : h2.heading-xl
  Locale modal    : #locale-modal-v2 / .modal-curtain.is-open
                    (auto-opens on page load and blocks pointer events)

Stock API (stage): www.stage.adobe.com/stock-api/Rest/Media/1/Search/Collections
Stock API (prod) : www.adobe.com/stock-api/Rest/Media/1/Search/Collections
"""

PAGE_URL   = "https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery"

STOCK_API_STAGE  = "www.stage.adobe.com/stock-api"
STOCK_API_PROD   = "www.adobe.com/stock-api"


class L:
    # Page structure
    GALLERY           = ".prm-yt-gallery"
    GRID              = ".pre-yt-grid"
    CARD              = ".pre-yt-card"
    CARD_THUMBNAIL    = ".image-wrapper img"
    CARD_VIDEO        = ".video-wrapper video"
    FREE_TAG          = ".pre-yt-free-tag"
    HEADING           = "h2.heading-xl"

    # Locale modal — opens automatically; blocks hover/click until dismissed
    MODAL_CURTAIN     = ".modal-curtain.is-open"

    # Meta / SEO
    META_DESCRIPTION  = 'meta[name="description"]'
