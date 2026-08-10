"""
BasePage — shared navigation and utility methods for all page objects.

Every page object extends BasePage. Add only truly common behaviour here;
keep page-specific logic in the page's own class.
"""
from __future__ import annotations

from playwright.sync_api import Page, TimeoutError as PWTimeout

from locators.gallery_locators import PAGE_URL, L


class BasePage:
    """Thin wrapper around a Playwright Page with reusable helpers."""

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self, url: str = PAGE_URL, wait: str = "networkidle") -> None:
        """Open the URL and wait until the network is idle."""
        self.page.goto(url, wait_until=wait, timeout=40_000)

    def get_current_url(self) -> str:
        return self.page.url

    # ── Locale modal ──────────────────────────────────────────────────────────

    def dismiss_modal(self) -> None:
        """
        Dismiss the locale modal if it is blocking the page.
        The .modal-curtain.is-open element intercepts all pointer events —
        clicking it closes the overlay. Falls back to Escape key if the
        curtain click does not disappear within 5 s.
        """
        curtain = self.page.locator(L.MODAL_CURTAIN)
        try:
            curtain.wait_for(state="visible", timeout=6_000)
        except PWTimeout:
            return  # modal never appeared — nothing to dismiss

        try:
            curtain.first.click(timeout=5_000)
            curtain.wait_for(state="hidden", timeout=5_000)
        except PWTimeout:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(600)

    # ── DOM helpers ───────────────────────────────────────────────────────────

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).first.is_visible()

    def get_text(self, selector: str) -> str:
        return (self.page.locator(selector).first.text_content() or "").strip()

    def get_attr(self, selector: str, attr: str) -> str | None:
        return self.page.locator(selector).first.get_attribute(attr)

    def count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    def get_meta_content(self, selector: str) -> str:
        return self.page.locator(selector).get_attribute("content") or ""

    def get_page_title(self) -> str:
        return self.page.title()

    # ── Screenshot ────────────────────────────────────────────────────────────

    def screenshot_bytes(self) -> bytes:
        return self.page.screenshot(full_page=False)
