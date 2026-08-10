"""
YouTube Gallery Page Object — MWPW-199796
Page: https://main--da-cc--adobecom.aem.live/drafts/automation-pw/youtube-gallery
"""
from playwright.sync_api import Page
from tests.pages.base_page import BasePage
from tests.locators import YT_GALLERY_URL, YTGalleryLocators as L


class YouTubeGalleryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.navigate(YT_GALLERY_URL)

    # ── Heading ──────────────────────────────────────────────────────────
    def is_heading_visible(self) -> bool:
        return self.is_visible(L.HEADING)

    def get_heading_text(self) -> str:
        return self.get_text(L.HEADING)

    # ── Grid / Cards ─────────────────────────────────────────────────────
    def is_grid_visible(self) -> bool:
        return self.is_visible(L.GRID)

    def get_card_count(self) -> int:
        return self.page.locator(L.CARD).count()

    def get_card_widths(self) -> list[float]:
        return self.page.eval_on_selector_all(
            L.CARD,
            "els => els.map(e => Math.round(e.getBoundingClientRect().width))"
        )

    def has_horizontal_overflow(self) -> bool:
        return self.page.evaluate(
            "() => document.body.scrollWidth > window.innerWidth"
        )

    # ── Card metadata ─────────────────────────────────────────────────────
    def get_card_template_ids(self) -> list[str]:
        return self.page.eval_on_selector_all(
            L.CARD,
            "els => els.map(e => e.dataset.templateId || '')"
        )

    def get_card_aria_labels(self) -> list[str]:
        return self.page.eval_on_selector_all(
            L.CARD,
            "els => els.map(e => (e.getAttribute('aria-label') || '').trim())"
        )

    def get_free_tag_texts(self) -> list[str]:
        return self.page.eval_on_selector_all(
            L.FREE_TAG,
            "els => els.map(e => e.innerText.trim())"
        )

    def get_thumbnail_srcs(self) -> list[str]:
        return self.page.eval_on_selector_all(
            L.THUMBNAIL,
            "els => els.map(e => e.src || e.getAttribute('src') || '')"
        )

    def is_first_thumbnail_visible(self) -> bool:
        thumb = self.page.locator(L.THUMBNAIL).first
        return thumb.count() > 0 and thumb.is_visible()

    # ── Meta description ──────────────────────────────────────────────────
    def get_meta_description(self) -> str:
        return self.get_meta_content("description")
