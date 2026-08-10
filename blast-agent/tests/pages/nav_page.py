"""
Navigation Page Object — Global Navigation bar actions and assertions.
"""
from playwright.sync_api import Page
from tests.pages.base_page import BasePage
from tests.locators import NavLocators


class NavPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    # ── Queries ──────────────────────────────────────────────────────────
    def is_sign_in_visible(self) -> bool:
        """True when the Sign In / Log in button is visible (logged-out state).
        Waits up to 8s for UNAV to render on slower engines (WebKit)."""
        try:
            self.page.locator(NavLocators.SIGN_IN_BUTTON).first.wait_for(
                state="visible", timeout=8000
            )
            return True
        except Exception:
            return False

    def is_firefly_cta_visible(self) -> bool:
        """True when the 'Go to Firefly' CTA is visible in the nav.
        Waits up to 8s for UNAV to render on slower engines (WebKit)."""
        try:
            self.page.locator(NavLocators.GO_TO_FIREFLY_CTA).first.wait_for(
                state="visible", timeout=8000
            )
            return True
        except Exception:
            return False

    def get_firefly_cta_href(self) -> str:
        cta = self.page.locator(NavLocators.GO_TO_FIREFLY_CTA)
        if cta.count():
            return cta.first.get_attribute("href") or ""
        return ""

    def get_sign_in_text(self) -> str:
        btn = self.page.locator(NavLocators.SIGN_IN_BUTTON)
        if btn.count():
            return btn.first.inner_text().strip()
        return ""

    # ── Actions ──────────────────────────────────────────────────────────
    def click_sign_in(self):
        """Click the Sign In button and wait for navigation.
        Uses native JS .click() to trigger delegated event handlers on UNAV."""
        self.page.evaluate(
            "document.querySelector('button.profile-comp.secondary-button').click()"
        )
        self.page.wait_for_load_state("domcontentloaded", timeout=15000)

    def get_current_url(self) -> str:
        return self.page.url

    def click_firefly_cta(self):
        """Click the 'Go to Firefly' CTA and wait for navigation."""
        with self.page.expect_navigation(timeout=15000):
            self.page.locator(NavLocators.GO_TO_FIREFLY_CTA).first.click()
