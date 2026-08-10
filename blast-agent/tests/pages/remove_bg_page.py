"""
Remove Background Page Object — all actions and assertions for the SEO page.
URL: https://www.adobe.com/products/firefly/features/remove-background.html
"""
from pathlib import Path
from playwright.sync_api import Page
from tests.pages.base_page import BasePage
from tests.locators import (
    PAGE_URL, MarqueeLocators, UploadLocators, AccordionLocators, SEOLocators
)

ASSETS_DIR = Path(__file__).parent.parent / "assets"


class RemoveBgPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def open(self):
        self.navigate(PAGE_URL)

    # ── SEO ──────────────────────────────────────────────────────────────
    def get_page_title(self) -> str:
        return self.get_title()

    def get_meta_description(self) -> str:
        return self.get_meta_content("description")

    def get_canonical_url(self) -> str:
        return super().get_canonical_url()

    def get_h1_text(self) -> str:
        return self.get_text(SEOLocators.H1)

    def get_all_h2_texts(self) -> list[str]:
        return self.page.eval_on_selector_all(
            SEOLocators.H2, "els => els.map(e => e.innerText.trim())"
        )

    # ── Marquee ──────────────────────────────────────────────────────────
    def is_h1_visible(self) -> bool:
        return self.is_visible(MarqueeLocators.H1_HEADING)

    def is_animation_present(self) -> bool:
        """Check that at least one <video> element exists on the page."""
        return self.page.locator(MarqueeLocators.ANIMATION_VIDEO).count() > 0

    def is_animation_playing(self) -> bool:
        """Check that the first video is not paused (i.e. playing)."""
        return self.page.evaluate(
            "document.querySelector('video') && !document.querySelector('video').paused"
        )

    # ── Upload ───────────────────────────────────────────────────────────
    def is_upload_zone_visible(self) -> bool:
        return self.is_visible(UploadLocators.DROP_ZONE)

    def upload_file(self, filename: str):
        """Upload a file by setting it on the hidden file input."""
        file_path = str(ASSETS_DIR / filename)
        self.page.locator(UploadLocators.FILE_INPUT).set_input_files(file_path)
        self.page.wait_for_timeout(3000)  # allow upload processing

    def get_error_message(self) -> str:
        """Return error message text if visible, empty string otherwise."""
        for sel in [".ia-error", "[class*='error-message']", "[class*='upload-error']",
                    "[class*='alert']", ".notification", "[role='alert']"]:
            el = self.page.locator(sel)
            if el.count() and el.first.is_visible():
                return el.first.inner_text().strip()
        return ""

    def is_error_visible(self) -> bool:
        return bool(self.get_error_message())

    def is_download_button_visible(self) -> bool:
        return self.is_visible(UploadLocators.DOWNLOAD_BUTTON)

    def is_reupload_button_visible(self) -> bool:
        btn = self.page.locator(UploadLocators.REUPLOAD_BUTTON)
        return btn.count() > 0 and btn.first.is_visible()

    # ── Accordion ────────────────────────────────────────────────────────
    def get_how_to_h2_text(self) -> str:
        """Find the H2 heading that contains 'How to remove a background'."""
        h2s = self.get_all_h2_texts()
        for h2 in h2s:
            if "how to remove" in h2.lower():
                return h2
        return ""

    def get_accordion_count(self) -> int:
        return self.page.locator(AccordionLocators.ACCORDION_TRIGGER).count()

    def click_accordion_item(self, index: int = 0):
        """Click the Nth accordion trigger (0-based).
        Uses native JS .click() to trigger delegated event handlers."""
        triggers = self.page.locator(AccordionLocators.ACCORDION_TRIGGER)
        triggers.nth(index).scroll_into_view_if_needed()
        self.page.evaluate(
            "(idx) => {"
            " const els = document.querySelectorAll('button.accordion-trigger');"
            " if (els[idx]) els[idx].click();"
            "}",
            index,
        )
        self.page.wait_for_timeout(500)

    def is_accordion_expanded(self, index: int = 0) -> bool:
        """Return True if the Nth accordion item is expanded."""
        trigger = self.page.locator(AccordionLocators.ACCORDION_TRIGGER).nth(index)
        aria = trigger.get_attribute("aria-expanded") or ""
        return aria.lower() == "true"

    def click_accordion_by_text(self, text: str):
        """Click an accordion item whose button text contains the given string."""
        trigger = self.page.locator(f"button.accordion-trigger:has-text('{text}')")
        trigger.first.scroll_into_view_if_needed()
        trigger.first.click()
        self.page.wait_for_timeout(500)
