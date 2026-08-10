"""
BasePage — shared utilities for the Firefly Background Generator suite (MWPW-200902).
Self-contained; no imports from any other suite in this repo.
"""
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="networkidle", timeout=45000)
        self.page.wait_for_timeout(2000)

    def get_title(self) -> str:
        return self.page.title()

    def get_meta_content(self, name: str) -> str:
        return self.page.evaluate(
            f"() => document.querySelector('meta[name=\"{name}\"]')?.content || ''"
        )

    def is_visible(self, selector: str) -> bool:
        loc = self.page.locator(selector).first
        return loc.count() > 0 and loc.is_visible()

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).first.inner_text().strip()

    def screenshot_bytes(self) -> bytes:
        return self.page.screenshot(full_page=True)
