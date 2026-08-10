"""
Spec: Feature 7 — Non-sticky Scroll Behavior
Feature file: features/07_scroll_behavior.feature
Ticket: MWPW-203117
"""
import allure
import pytest
from pages.promo_banner_page import PromoBannerPage
from locators.promo_locators import L


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 7: Non-sticky Scroll Behavior")
class TestScrollBehavior:

    @allure.title("Banner scrolls off screen with the page (not sticky)")
    @pytest.mark.scroll
    @pytest.mark.smoke
    def test_banner_scrolls_off_with_page(self, promo_banner: PromoBannerPage):
        assert promo_banner.is_banner_in_viewport(), (
            "Banner is not in the viewport before scrolling — cannot verify scroll-off behavior"
        )
        promo_banner.scroll_by(1000)
        allure.attach(
            promo_banner.screenshot_bytes(),
            name="after_scroll_down",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not promo_banner.is_banner_in_viewport(), (
            "Banner is still visible in the viewport after scrolling down — "
            "expected non-sticky behavior (banner should scroll off with the page)"
        )

    @allure.title("Banner reappears at the top without leaving a ghost/duplicate element")
    @pytest.mark.scroll
    def test_banner_reappears_at_top_no_duplicate(self, promo_banner: PromoBannerPage):
        promo_banner.scroll_by(1000)
        promo_banner.scroll_to_top()
        allure.attach(
            promo_banner.screenshot_bytes(),
            name="after_scroll_back_to_top",
            attachment_type=allure.attachment_type.PNG,
        )
        assert promo_banner.is_banner_in_viewport(), (
            "Banner did not reappear at the top of the page after scrolling back up"
        )
        assert promo_banner.count(L.BANNER) == 1, (
            "More than one banner element found in the DOM — possible duplicate/ghost element"
        )
