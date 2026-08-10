"""
BasePage — shared utilities for the YouTube Gallery test suite.
Completely independent of any other test suite in this repo.
"""
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="networkidle", timeout=30000)
        self.page.wait_for_timeout(2000)

    def get_title(self) -> str:
        return self.page.title()

    def get_meta_content(self, name: str) -> str:
        el = self.page.locator(f'meta[name="{name}"]')
        return el.get_attribute("content") or "" if el.count() else ""

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).first.is_visible()

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).first.inner_text().strip()

    def screenshot_bytes(self) -> bytes:
        return self.page.screenshot(full_page=True)
