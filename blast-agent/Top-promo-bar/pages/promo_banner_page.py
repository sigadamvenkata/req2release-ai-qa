"""
PromoBannerPage — all interactions specific to the Top Promo Banner (MWPW-203117).

Each method maps to one or more Gherkin steps in features/*.feature.
Selectors come from locators/promo_locators.py — see the caveat at the top of that
file: MWPW-203117 was still in Draft with no live implementation when this suite was
authored, so selectors are best-effort placeholders pending the real build.
"""
from __future__ import annotations

import re
from typing import Optional

from playwright.sync_api import Page

from pages.base_page import BasePage
from locators.promo_locators import L, C1_URL, C2_URL


class PromoBannerPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ══════════════════════════════════════════════════════════════════════
    # Navigation
    # ══════════════════════════════════════════════════════════════════════
    def open_c2(self) -> None:
        self.navigate(C2_URL)

    def open_c1(self) -> None:
        self.navigate(C1_URL)

    # ══════════════════════════════════════════════════════════════════════
    # Feature 1 — Rendering & placement
    # ══════════════════════════════════════════════════════════════════════
    def is_banner_visible(self) -> bool:
        return self.is_visible(L.BANNER)

    def has_active_promo(self, timeout: int = 10_000) -> bool:
        """Whether this page currently has an active promo configured at all.
        The promo campaign is content-driven and may be absent on a given page/
        locale (verified: absent on the C1 and RTL pages as of 2026-08-05) — use
        this to skip tests gracefully instead of failing on missing content."""
        return self.wait_for_visible(L.BANNER, timeout=timeout)

    def is_gnav_visible(self) -> bool:
        return self.is_visible(L.GNAV)

    def is_banner_above_gnav(self) -> bool:
        """True if the banner's bounding box sits fully above the GNAV's."""
        banner_box = self.get_bounding_box(L.BANNER)
        gnav_box = self.get_bounding_box(L.GNAV)
        if not banner_box or not gnav_box:
            return False
        return (banner_box["y"] + banner_box["height"]) <= gnav_box["y"] + 1

    def open_products_mega_menu(self) -> None:
        self.page.locator(L.GNAV_PRODUCTS_TRIGGER).first.click()
        self.page.wait_for_timeout(500)

    def is_mega_menu_overlapping_banner(self) -> bool:
        menu_box = self.get_bounding_box(L.GNAV_MEGA_MENU)
        banner_box = self.get_bounding_box(L.BANNER)
        if not menu_box or not banner_box:
            return False
        return not (menu_box["y"] >= banner_box["y"] + banner_box["height"])

    def is_gnav_flush_with_top(self, tolerance: int = 5) -> bool:
        gnav_box = self.get_bounding_box(L.GNAV)
        return bool(gnav_box) and gnav_box["y"] <= tolerance

    # ══════════════════════════════════════════════════════════════════════
    # Feature 2 — Delayed / asynchronous load
    # ══════════════════════════════════════════════════════════════════════
    def wait_for_banner(self, timeout: int = 10_000) -> bool:
        """Explicit wait for the banner — the banner is expected to appear ~5s
        after page load, so tests must never assert on it immediately."""
        return self.wait_for_visible(L.BANNER, timeout=timeout)

    def wait_for_gnav(self, timeout: int = 8_000) -> bool:
        """Explicit wait for the GNAV itself — verified live that the GNAV also
        hydrates asynchronously (not present at raw DOMContentLoaded), so this
        must not be asserted on instantly either."""
        return self.wait_for_visible(L.GNAV, timeout=timeout)

    def is_gnav_interactive(self, timeout: int = 8_000) -> bool:
        """Basic proxy for 'page is usable while banner is still loading':
        GNAV Sign In is present and clickable. Waits for the GNAV to hydrate
        rather than checking instantly (see wait_for_gnav)."""
        if not self.wait_for_visible(L.GNAV_SIGN_IN, timeout=timeout):
            return False
        return self.page.locator(L.GNAV_SIGN_IN).first.is_enabled()

    # ══════════════════════════════════════════════════════════════════════
    # Feature 3 — Maximized / minimized states & content
    # ══════════════════════════════════════════════════════════════════════
    def get_banner_state(self) -> str:
        """State is a BEM modifier class on the same .feds-promo-bar element
        (e.g. "feds-promo-bar feds-promo-bar--maximized feds-promo-bar--light"),
        not a separate element — check the class list rather than counting
        distinct selectors."""
        classes = self.get_attr(L.BANNER, "class") or ""
        if "feds-promo-bar--maximized" in classes:
            return "maximized"
        if "feds-promo-bar--minimized" in classes:
            return "minimized"
        return "unknown"

    def get_banner_theme(self) -> str:
        """Theme is likewise a BEM modifier class on the same element — this is
        an authoring-time choice per campaign, NOT client-adaptive (verified:
        browser dark-mode emulation has no effect on the live banner)."""
        classes = self.get_attr(L.BANNER, "class") or ""
        if "feds-promo-bar--dark" in classes:
            return "dark"
        if "feds-promo-bar--light" in classes:
            return "light"
        return "unknown"

    def get_headline_text(self) -> str:
        return self.get_text(L.HEADLINE)

    def get_supporting_copy_text(self) -> str:
        return self.get_text(L.SUPPORTING_COPY)

    def get_see_terms_href(self) -> Optional[str]:
        return self.get_attr(L.SEE_TERMS_LINK, "href")

    def get_cta_text(self) -> str:
        return self.get_text(L.PRIMARY_CTA)

    def get_cta_href(self) -> Optional[str]:
        return self.get_attr(L.PRIMARY_CTA, "href")

    def click_cta(self) -> None:
        with self.page.expect_navigation(timeout=15_000):
            self.page.locator(L.PRIMARY_CTA).first.click()

    # ══════════════════════════════════════════════════════════════════════
    # Feature 4 — Countdown
    # ══════════════════════════════════════════════════════════════════════
    def is_countdown_visible(self) -> bool:
        return self.is_visible(L.COUNTDOWN)

    def get_countdown_text(self) -> str:
        return self.get_text(L.COUNTDOWN)

    @staticmethod
    def _parse_countdown_seconds(text: str) -> Optional[int]:
        """Parse a DD:HH:MM:SS (or HH:MM:SS) string into total seconds."""
        parts = re.findall(r"\d+", text)
        if len(parts) not in (3, 4):
            return None
        nums = [int(p) for p in parts]
        if len(nums) == 4:
            d, h, m, s = nums
        else:
            d = 0
            h, m, s = nums
        return d * 86_400 + h * 3_600 + m * 60 + s

    def get_countdown_seconds(self) -> Optional[int]:
        return self._parse_countdown_seconds(self.get_countdown_text())

    def wait_and_get_countdown_delta(self, wait_seconds: int = 5) -> Optional[int]:
        """Return how many seconds the countdown decreased over `wait_seconds`."""
        before = self.get_countdown_seconds()
        self.page.wait_for_timeout(wait_seconds * 1000)
        after = self.get_countdown_seconds()
        if before is None or after is None:
            return None
        return before - after

    # ══════════════════════════════════════════════════════════════════════
    # Feature 5 — Theming
    # ══════════════════════════════════════════════════════════════════════
    def get_banner_background_color(self) -> str:
        return self.get_computed_style(L.BANNER, "backgroundColor")

    def get_banner_text_color(self) -> str:
        return self.get_computed_style(L.HEADLINE, "color")

    @staticmethod
    def _rgb_luminance(rgb_string: str) -> Optional[float]:
        """Parse 'rgb(r, g, b)' / 'rgba(r, g, b, a)' and return perceived
        luminance (0=black, 255=white), or None if unparseable."""
        nums = re.findall(r"[\d.]+", rgb_string)
        if len(nums) < 3:
            return None
        r, g, b = (float(n) for n in nums[:3])
        return 0.299 * r + 0.587 * g + 0.114 * b

    def is_background_consistent_with_declared_theme(self) -> bool:
        """Self-consistency check: a banner declared '--light' should render a
        light (high-luminance) background, and '--dark' a dark one. This is the
        correct check here because the banner's theme is an authoring-time
        choice per campaign, not something that reacts to OS/browser dark-mode
        (verified: emulating color_scheme=dark has no effect on the live
        banner) — so comparing against a second, separately-themed fixture
        doesn't apply."""
        theme = self.get_banner_theme()
        luminance = self._rgb_luminance(self.get_banner_background_color())
        if theme == "unknown" or luminance is None:
            return False
        return luminance >= 128 if theme == "light" else luminance < 128

    # ══════════════════════════════════════════════════════════════════════
    # Feature 6 — Responsive layout
    # ══════════════════════════════════════════════════════════════════════
    def has_horizontal_overflow(self) -> bool:
        scroll_w, inner_w = self.get_scroll_vs_inner_width()
        return scroll_w > inner_w

    def get_banner_bounding_box(self) -> Optional[dict]:
        return self.get_bounding_box(L.BANNER)

    # ══════════════════════════════════════════════════════════════════════
    # Feature 7 — Non-sticky scroll behavior
    # ══════════════════════════════════════════════════════════════════════
    def is_banner_in_viewport(self) -> bool:
        box = self.get_bounding_box(L.BANNER)
        if not box:
            return False
        viewport = self.page.viewport_size
        return 0 <= box["y"] < viewport["height"] and box["y"] + box["height"] > 0

    # ══════════════════════════════════════════════════════════════════════
    # Feature 8 — No dismiss control / no session persistence
    # ══════════════════════════════════════════════════════════════════════
    def has_close_button(self) -> bool:
        return self.count(L.CLOSE_BUTTON) > 0

    def get_storage_snapshot(self) -> dict:
        """Best-effort snapshot of localStorage/sessionStorage/cookies to check for
        a 'promo dismissed' flag. Key names are unknown until the real
        implementation ships — inspect this snapshot manually if a persistence
        bug is suspected."""
        local_storage = self.page.evaluate("() => JSON.stringify(window.localStorage)")
        session_storage = self.page.evaluate("() => JSON.stringify(window.sessionStorage)")
        cookies = self.page.context.cookies()
        return {
            "localStorage": local_storage,
            "sessionStorage": session_storage,
            "cookies": cookies,
        }

    # ══════════════════════════════════════════════════════════════════════
    # Feature 9 — WW rollout / RTL
    # ══════════════════════════════════════════════════════════════════════
    def get_html_dir_attr(self) -> str:
        return self.get_html_dir()

    def is_banner_rtl_mirrored(self) -> bool:
        """Best-effort check: in RTL locales the banner's computed CSS
        `direction` should be rtl."""
        direction = self.get_computed_style(L.BANNER, "direction")
        return direction.lower() == "rtl"

    # ══════════════════════════════════════════════════════════════════════
    # Feature 10 — Accessibility
    # ══════════════════════════════════════════════════════════════════════
    def get_countdown_aria_live(self) -> Optional[str]:
        return self.get_attr(L.COUNTDOWN, "aria-live")

    def tab_to_banner_cta(self, max_tabs: int = 20) -> bool:
        """Press Tab repeatedly until the primary CTA receives focus, or give up
        after `max_tabs` presses. Returns True if the CTA was reached."""
        for _ in range(max_tabs):
            self.page.keyboard.press("Tab")
            focused_matches = self.page.evaluate(
                """(sel) => {
                    const el = document.activeElement;
                    return !!el && !!el.closest(sel);
                }""",
                L.PRIMARY_CTA,
            )
            if focused_matches:
                return True
        return False
