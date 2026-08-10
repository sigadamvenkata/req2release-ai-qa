"""
BasePage — shared navigation and utility methods for all Top Promo Banner page objects.

Every page object extends BasePage. Add only truly common behaviour here;
keep banner-specific logic in PromoBannerPage.
"""
from __future__ import annotations

from typing import Optional
from playwright.sync_api import Page, TimeoutError as PWTimeout

AXE_CORE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"


class BasePage:
    """Thin wrapper around a Playwright Page with reusable helpers."""

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ────────────────────────────────────────────────────────────
    def navigate(self, url: str, wait: str = "domcontentloaded") -> None:
        self.page.goto(url, wait_until=wait, timeout=30_000)

    def reload(self) -> None:
        self.page.reload(wait_until="domcontentloaded", timeout=30_000)

    def get_current_url(self) -> str:
        return self.page.url

    # ── DOM helpers ───────────────────────────────────────────────────────────
    def is_visible(self, selector: str) -> bool:
        loc = self.page.locator(selector)
        return loc.count() > 0 and loc.first.is_visible()

    def get_text(self, selector: str) -> str:
        return (self.page.locator(selector).first.text_content() or "").strip()

    def get_attr(self, selector: str, attr: str) -> Optional[str]:
        loc = self.page.locator(selector)
        return loc.first.get_attribute(attr) if loc.count() > 0 else None

    def count(self, selector: str) -> int:
        return self.page.locator(selector).count()

    def wait_for_visible(self, selector: str, timeout: int = 10_000) -> bool:
        """Explicit wait for an element to become visible. Returns False (does not
        raise) on timeout so callers can assert with a clear message instead of a
        raw Playwright TimeoutError — the Top Promo Banner is expected to load
        asynchronously ~5s after the page, so callers should pass a generous
        timeout rather than relying on the element being present immediately."""
        try:
            self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
            return True
        except PWTimeout:
            return False

    def get_bounding_box(self, selector: str) -> Optional[dict]:
        loc = self.page.locator(selector)
        return loc.first.bounding_box() if loc.count() > 0 else None

    def get_computed_style(self, selector: str, prop: str) -> str:
        return self.page.eval_on_selector(
            selector, "(el, prop) => getComputedStyle(el)[prop]", prop
        )

    # ── Scroll helpers ────────────────────────────────────────────────────────
    def scroll_by(self, y: int) -> None:
        self.page.evaluate("(y) => window.scrollBy(0, y)", y)
        self.page.wait_for_timeout(300)

    def scroll_to_top(self) -> None:
        self.page.evaluate("window.scrollTo(0, 0)")
        self.page.wait_for_timeout(300)

    def get_scroll_vs_inner_width(self) -> tuple[int, int]:
        scroll_w = self.page.evaluate("document.body.scrollWidth")
        inner_w = self.page.evaluate("window.innerWidth")
        return scroll_w, inner_w

    # ── Theming / locale ──────────────────────────────────────────────────────
    def get_html_dir(self) -> str:
        return self.page.locator("html").get_attribute("dir") or ""

    # ── Accessibility (axe-core injected via CDN — no extra pip dependency) ──
    def run_axe_scan(self, selector: Optional[str] = None) -> list[dict]:
        """Inject axe-core from CDN and run a scan, optionally scoped to `selector`.
        Returns the list of violations (empty list if none). Requires the test
        browser context to have network access to the axe-core CDN."""
        self.page.add_script_tag(url=AXE_CORE_CDN)
        context = f"document.querySelector({selector!r})" if selector else "document"
        result = self.page.evaluate(f"async () => (await axe.run({context})).violations")
        return result or []

    # ── Screenshot ────────────────────────────────────────────────────────────
    def screenshot_bytes(self) -> bytes:
        return self.page.screenshot(full_page=False)
