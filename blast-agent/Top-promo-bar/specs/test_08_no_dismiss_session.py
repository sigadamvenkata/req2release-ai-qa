"""
Spec: Feature 8 — No Dismiss Control & No Session Persistence
Feature file: features/08_no_dismiss_session.feature
Ticket: MWPW-203117
"""
import allure
import pytest
from pages.promo_banner_page import PromoBannerPage


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 8: No Dismiss Control & No Session Persistence")
class TestNoDismissSession:

    @allure.title("Banner has no close/dismiss button")
    @pytest.mark.no_dismiss
    @pytest.mark.smoke
    def test_no_close_button_present(self, promo_banner: PromoBannerPage):
        allure.attach(
            promo_banner.screenshot_bytes(),
            name="banner_no_close_button",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not promo_banner.has_close_button(), (
            "A close/dismiss control was found on the banner — "
            "the ticket specifies no close button is required"
        )

    @allure.title("Banner reappears on a fresh visit without session persistence")
    @pytest.mark.no_dismiss
    def test_banner_reappears_without_session_persistence(self, promo_banner: PromoBannerPage):
        # NOTE: the promo campaign is currently only configured on the C2
        # homepage (verified 2026-08-05 — absent on C1/RTL/Intl pages), so we
        # can't use "navigate to a different page with the same promo" as
        # originally designed. Reloading the same URL still validates the core
        # requirement: the banner must not remember/suppress itself via
        # cookies/localStorage/sessionStorage across repeat visits.
        assert promo_banner.is_banner_visible(), "Banner is not visible on the first visit"

        storage_before = promo_banner.get_storage_snapshot()
        allure.attach(
            str(storage_before),
            name="storage_before_reload",
            attachment_type=allure.attachment_type.TEXT,
        )

        promo_banner.reload()
        promo_banner.wait_for_banner(timeout=10_000)

        assert promo_banner.is_banner_visible(), (
            "Banner did not reappear after a page reload — "
            "possible unexpected dismissal/session persistence"
        )
