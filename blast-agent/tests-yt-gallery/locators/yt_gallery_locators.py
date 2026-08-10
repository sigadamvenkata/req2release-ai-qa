"""
Locators for the YouTube Gallery block — MWPW-199796
All selectors discovered from live DOM inspection of:
  https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery

DOM facts:
  - Gallery wrapper : .prm-yt-gallery
  - Grid container  : .pre-yt-grid
  - Card            : .pre-yt-card  (has data-template-id for unique ID)
  - Card label      : aria-label attribute on .pre-yt-card
  - Free tag        : .pre-yt-free-tag  (innerText == "Free")
  - Thumbnail       : .image-wrapper img  (src = ftcdn CDN URL)
  - Video           : .video-wrapper video
  - Heading         : h2.heading-xl  (id="get-inspired-with-on-trend-templates")
"""

PAGE_URL = "https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery"


class YTGalleryLocators:
    GALLERY_CONTAINER = ".prm-yt-gallery"
    GRID              = ".pre-yt-grid"
    CARD              = ".pre-yt-card"
    FREE_TAG          = ".pre-yt-free-tag"
    THUMBNAIL         = ".image-wrapper img"
    VIDEO             = ".video-wrapper video"
    HEADING           = "h2.heading-xxxl"
    META_DESCRIPTION  = 'meta[name="description"]'
