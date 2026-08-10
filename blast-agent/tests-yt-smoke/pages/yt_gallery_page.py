"""
YouTube Gallery Page Object — MWPW-199796 @smoke suite
Handles all interactions against the gallery page including locale modal dismissal.
"""
from playwright.sync_api import Page, TimeoutError as PWTimeout
from pages.base_page import BasePage
from locators.yt_smoke_locators import PAGE_URL, L


class YouTubeGalleryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Open & modal handling ─────────────────────────────────────────────────

    def open(self):
        """Navigate to the gallery page and dismiss the locale modal if present."""
        self.navigate(PAGE_URL)
        self._dismiss_modal_if_present()

    def _dismiss_modal_if_present(self):
        """
        The locale/region modal (.modal-curtain.is-open) auto-opens on page load
        and blocks all pointer events. Clicking the curtain closes it
        (daa-ll="localeModal:modalClose:curtainClose").
        """
        curtain = self.page.locator(L.MODAL_CURTAIN)
        if curtain.count() > 0 and curtain.first.is_visible():
            try:
                curtain.first.click(timeout=5000)
                self.page.wait_for_selector(
                    L.MODAL_CURTAIN, state="hidden", timeout=5000
                )
            except PWTimeout:
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(500)

    # ── Page-level ────────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self.get_title()

    def get_current_url(self) -> str:
        return self.page.url

    # ── Heading ───────────────────────────────────────────────────────────────

    def is_heading_visible(self) -> bool:
        return self.is_visible(L.HEADING)

    def get_heading_text(self) -> str:
        return self.get_text(L.HEADING)

    # ── Gallery / Grid / Cards ────────────────────────────────────────────────

    def is_grid_visible(self) -> bool:
        return self.is_visible(L.GRID)

    def get_card_count(self) -> int:
        return self.page.locator(L.CARD).count()

    # ── Thumbnail ─────────────────────────────────────────────────────────────

    def is_first_thumbnail_visible(self) -> bool:
        thumb = self.page.locator(L.CARD_THUMBNAIL).first
        return thumb.count() > 0 and thumb.is_visible()

    def get_first_thumbnail_src(self) -> str:
        return self.page.locator(L.CARD_THUMBNAIL).first.get_attribute("src") or ""

    # ── Hover → Video ─────────────────────────────────────────────────────────

    def hover_first_card(self):
        self.page.locator(L.CARD).first.hover()
        self.page.wait_for_timeout(2000)

    def is_first_card_video_playing(self) -> bool:
        return self.page.evaluate(
            "() => { const v = document.querySelector('.pre-yt-card video'); "
            "return v ? !v.paused : false; }"
        )

    # ── Click navigation guard ────────────────────────────────────────────────

    def click_first_card(self):
        self.page.locator(L.CARD).first.click()
        self.page.wait_for_timeout(1000)
