"""
Centralized locator registry for the Firefly Remove Background SEO page.
All selectors are discovered from the live page — update here if the page changes.

Page: https://www.adobe.com/products/firefly/features/remove-background.html
"""

PAGE_URL = "https://www.adobe.com/products/firefly/features/remove-background.html"


class NavLocators:
    """Global Navigation bar selectors."""
    SIGN_IN_BUTTON          = "button.profile-comp.secondary-button"          # "Sign in" button
    PROFILE_ICON            = ".profile-comp:not(.secondary-button)"          # Logged-in profile indicator
    HAMBURGER_MENU          = "button.feds-toggle"                            # Mobile nav toggle
    FIREFLY_NAV_LINK        = "a.feds-navLink[href*='products/firefly']"      # Firefly link in nav menu
    GO_TO_FIREFLY_CTA       = "a.feds-cta.feds-cta--secondary"               # "Go to Firefly" CTA button
    NAV_BAR                 = "header"                                         # Top navigation bar container


class MarqueeLocators:
    """Hero / Marquee section selectors."""
    H1_HEADING              = "h1"                                             # "Remove the background from your image for free."
    HERO_SECTION            = ".hero-marquee"                                  # Marquee container
    ANIMATION_VIDEO         = "video"                                          # Remove-background animation (3 videos on page)
    FIRST_VIDEO             = "video:first-of-type"                           # First/main animation


class UploadLocators:
    """Image upload block selectors."""
    FILE_INPUT              = "input.ia-file-input"                            # Hidden file <input> (accepts jpg,jpeg,png,webp)
    DROP_ZONE               = ".drop-zone-container"                           # Drag-and-drop zone
    DROPZONE_SHELL          = ".ia-dropzone-shell"                             # Inner dropzone wrapper
    REUPLOAD_BUTTON         = "button.ia-reupload-btn"                        # "Upload another image" button
    DOWNLOAD_BUTTON         = "button.ia-download-btn"                        # Download result button
    EDIT_IN_FIREFLY         = "button.ia-edit-in-firefly"                     # "Edit in Firefly" button
    ERROR_MESSAGE           = ".ia-error, [class*='error']:visible"           # Error messages shown on bad upload

    # Accepted MIME types (as declared by the page's file input)
    ACCEPTED_TYPES          = ["image/jpeg", "image/jpg", "image/png", "image/webp"]


class AccordionLocators:
    """FAQ / Accordion block selectors."""
    ACCORDION_SECTION       = "section:has(button.accordion-trigger)"         # Accordion section wrapper
    ACCORDION_TRIGGER       = "button.accordion-trigger"                      # All accordion expand/collapse buttons
    ACCORDION_CONTENT       = ".accordion-content"                            # Expanded accordion content panels

    # FAQ accordion heading (H2 above the questions)
    HOW_TO_H2               = "h2"                                             # Match via text: "How to remove a background with Adobe Firefly."

    # Individual FAQ question buttons (by text)
    FAQ_WHAT_IS_BEST        = "button.accordion-trigger:has-text('What is the best background remover')"
    FAQ_FILE_FORMATS        = "button.accordion-trigger:has-text('What file formats')"
    FAQ_IS_FREE             = "button.accordion-trigger:has-text('free')"


class SEOLocators:
    """SEO metadata selectors."""
    META_DESCRIPTION        = 'meta[name="description"]'
    CANONICAL_LINK          = 'link[rel="canonical"]'
    H1                      = "h1"
    H2                      = "h2"


YT_GALLERY_URL = "https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery"


class YTGalleryLocators:
    """YouTube Gallery block selectors — discovered from live page DOM."""
    GALLERY_CONTAINER       = ".prm-yt-gallery"                  # outer block wrapper
    GRID                    = ".pre-yt-grid"                     # CSS grid container
    CARD                    = ".pre-yt-card"                     # individual card (has data-template-id)
    CARD_INNER              = ".pre-yt-card-inner"               # inner card wrapper
    FREE_TAG                = ".pre-yt-free-tag"                 # "Free" badge on each card
    THUMBNAIL               = ".image-wrapper img"               # card thumbnail image
    VIDEO                   = ".video-wrapper video"             # hover-play video per card
    INFO_BUTTON             = ".pre-yt-info-button"              # info (i) button on each card
    CLOSE_BUTTON            = ".pre-yt-close-card-button"        # close button on expanded card
    HEADING                 = "h2.heading-xl"                    # "Get inspired with on-trend templates."
    META_DESCRIPTION        = 'meta[name="description"]'
