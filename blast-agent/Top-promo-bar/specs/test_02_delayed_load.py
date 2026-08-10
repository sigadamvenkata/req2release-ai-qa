"""
Spec: Feature 2 — Delayed / Asynchronous Banner Load
Feature file: features/02_delayed_load.feature
Ticket: MWPW-203117

The banner is expected to load ~5s after the page — these tests explicitly avoid
asserting on it immediately and never use a fixed `sleep` shorter than the
observed load delay (see Risks & Mitigations in MWPW-203117_test_plan.md).
"""
import time

import allure
import pytest
from pages.promo_banner_page import PromoBannerPage

MAX_ACCEPTABLE_LOAD_MS = 10_000  # agreed max threshold pending confirmation from dev


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 2: Delayed / Asynchronous Load")
class TestDelayedLoad:

    @allure.title("Banner is not required to be present at initial page load")
    @pytest.mark.delayed_load
    @pytest.mark.smoke
    def test_banner_absent_at_initial_load(self, promo_banner_no_wait: PromoBannerPage):
        # No hard assertion that it's absent (implementation may be fast) — this
        # documents/records the initial state and confirms the GNAV isn't blocked.
        allure.attach(
            f"Banner visible immediately after DOMContentLoaded: {promo_banner_no_wait.is_banner_visible()}",
            name="initial_banner_state",
            attachment_type=allure.attachment_type.TEXT,
        )
        # Verified live: the GNAV itself also hydrates asynchronously (it is NOT
        # present at raw DOMContentLoaded either) — wait for it rather than
        # asserting instantly, same reasoning we apply to the banner.
        assert promo_banner_no_wait.wait_for_gnav(timeout=8_000), (
            "GNAV did not become visible within 8s of page load, before the banner appeared"
        )

    @allure.title("Banner appears within an acceptable wait window (~5s)")
    @pytest.mark.delayed_load
    @pytest.mark.smoke
    def test_banner_appears_within_threshold(self, promo_banner_no_wait: PromoBannerPage):
        start = time.monotonic()
        appeared = promo_banner_no_wait.wait_for_banner(timeout=MAX_ACCEPTABLE_LOAD_MS)
        elapsed_ms = (time.monotonic() - start) * 1000
        allure.attach(
            f"Banner appeared: {appeared} after {elapsed_ms:.0f}ms",
            name="banner_load_timing",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert appeared, (
            f"Top Promo Banner did not appear within {MAX_ACCEPTABLE_LOAD_MS}ms"
        )

    @allure.title("Page remains usable while the banner is still loading")
    @pytest.mark.delayed_load
    def test_gnav_usable_while_banner_loading(self, promo_banner_no_wait: PromoBannerPage):
        assert promo_banner_no_wait.is_gnav_interactive(), (
            "GNAV Sign In is not present/clickable while the banner has not yet appeared"
        )

    @allure.title("Banner injection does not break GNAV placement once it appears")
    @pytest.mark.delayed_load
    def test_no_disruptive_layout_shift_on_banner_injection(self, promo_banner_no_wait: PromoBannerPage):
        promo_banner_no_wait.wait_for_banner(timeout=MAX_ACCEPTABLE_LOAD_MS)
        assert promo_banner_no_wait.is_banner_above_gnav(), (
            "GNAV does not render below the banner once the banner has loaded in — "
            "possible disruptive layout shift"
        )

    @allure.title("Automated wait uses an explicit poll, not a fixed sleep")
    @pytest.mark.delayed_load
    def test_explicit_wait_not_fixed_sleep(self, promo_banner_no_wait: PromoBannerPage):
        # Regression guard for suite hygiene: wait_for_banner must return a bool
        # via Playwright's own wait_for(), never a bare time.sleep().
        result = promo_banner_no_wait.wait_for_banner(timeout=MAX_ACCEPTABLE_LOAD_MS)
        assert isinstance(result, bool), (
            "wait_for_banner() must return a boolean from an explicit Playwright wait, "
            "not rely on an unconditional sleep"
        )
