"""
YouTube Gallery Page Object — MWPW-199796
Encapsulates all queries against the YouTube Gallery block.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage
from locators.yt_gallery_locators import PAGE_URL, YTGalleryLocators as L


class YouTubeGalleryPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.navigate(PAGE_URL)

    # ── Heading ───────────────────────────────────────────────────────────
    def is_heading_visible(self) -> bool:
        return self.is_visible(L.HEADING)

    def get_heading_text(self) -> str:
        return self.get_text(L.HEADING)

    # ── Gallery container & grid ──────────────────────────────────────────
    def is_gallery_visible(self) -> bool:
        return self.is_visible(L.GALLERY_CONTAINER)

    def is_grid_visible(self) -> bool:
        return self.is_visible(L.GRID)

    def get_card_count(self) -> int:
        return self.page.locator(L.CARD).count()

    def get_card_widths(self) -> list:
        """Return the rendered pixel width of every card (rounded to int)."""
        return self.page.eval_on_selector_all(
            L.CARD,
            "els => els.map(e => Math.round(e.getBoundingClientRect().width))"
        )

    def cards_overflow_grid(self) -> bool:
        """True if any card overflows the grid container horizontally."""
        return self.page.evaluate("""() => {
            const grid = document.querySelector('.pre-yt-grid');
            if (!grid) return false;
            const gridRight = grid.getBoundingClientRect().right;
            const cards = Array.from(document.querySelectorAll('.pre-yt-card'));
            return cards.some(c => c.getBoundingClientRect().right > gridRight + 2);
        }""")

    # ── Card metadata ─────────────────────────────────────────────────────
    def get_card_template_ids(self) -> list:
        return self.page.eval_on_selector_all(
            L.CARD,
            "els => els.map(e => (e.dataset.templateId || '').trim())"
        )

    def get_card_aria_labels(self) -> list:
        """aria-label on each card is the visible label/description text."""
        return self.page.eval_on_selector_all(
            L.CARD,
            "els => els.map(e => (e.getAttribute('aria-label') || '').trim())"
        )

    def get_free_tag_texts(self) -> list:
        return self.page.eval_on_selector_all(
            L.FREE_TAG,
            "els => els.map(e => e.innerText.trim())"
        )

    def is_first_thumbnail_visible(self) -> bool:
        thumb = self.page.locator(L.THUMBNAIL).first
        return thumb.count() > 0 and thumb.is_visible()

    def get_thumbnail_srcs(self) -> list:
        return self.page.eval_on_selector_all(
            L.THUMBNAIL,
            "els => els.map(e => (e.src || e.getAttribute('src') || '').trim())"
        )

    # ── Page layout ────────────────────────────────────────────────────────
    def has_horizontal_overflow(self) -> bool:
        return self.page.evaluate(
            "() => document.body.scrollWidth > window.innerWidth"
        )

    def get_meta_description(self) -> str:
        return self.get_meta_content("description")
