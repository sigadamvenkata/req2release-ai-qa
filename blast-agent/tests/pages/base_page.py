"""
Base Page — shared utility methods inherited by all page objects.
Every page object extends BasePage.
"""
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
        self.page.wait_for_timeout(3000)  # allow JS hydration

    def get_title(self) -> str:
        return self.page.title()

    def get_meta_content(self, name: str) -> str:
        el = self.page.locator(f'meta[name="{name}"]')
        if el.count():
            return el.get_attribute("content") or ""
        return ""

    def get_canonical_url(self) -> str:
        el = self.page.locator('link[rel="canonical"]')
        if el.count():
            return el.get_attribute("href") or ""
        return ""

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).first.is_visible()

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).first.inner_text().strip()

    def scroll_to(self, selector: str):
        self.page.locator(selector).first.scroll_into_view_if_needed()

    def wait_for(self, selector: str, timeout: int = 10000):
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)

    def take_screenshot(self, name: str):
        self.page.screenshot(path=f"tests/reports/{name}.png", full_page=False)
