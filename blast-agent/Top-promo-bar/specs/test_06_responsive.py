"""
Spec: Feature 6 — Responsive Layout
Feature file: features/06_responsive.feature
Ticket: MWPW-203117
"""
import allure
import pytest
from pages.promo_banner_page import PromoBannerPage


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 6: Responsive Layout")
class TestResponsive:

    @allure.title("Banner renders without horizontal overflow on desktop (1440x900)")
    @pytest.mark.responsive
    @pytest.mark.smoke
    def test_desktop_no_overflow(self, promo_banner: PromoBannerPage):
        allure.attach(
            promo_banner.screenshot_bytes(),
            name="desktop_1440x900",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not promo_banner.has_horizontal_overflow(), (
            "Horizontal overflow detected on desktop (1440x900)"
        )
        box = promo_banner.get_banner_bounding_box()
        assert box is not None, "Could not read banner bounding box on desktop"

    @allure.title("Banner renders without horizontal overflow on mobile portrait (375x812)")
    @pytest.mark.responsive
    @pytest.mark.smoke
    def test_mobile_portrait_no_overflow(self, promo_banner_portrait: PromoBannerPage):
        allure.attach(
            promo_banner_portrait.screenshot_bytes(),
            name="mobile_portrait_375x812",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not promo_banner_portrait.has_horizontal_overflow(), (
            "Horizontal overflow detected on mobile portrait (375x812)"
        )
        assert promo_banner_portrait.is_banner_visible(), (
            "Banner is not visible on mobile portrait (375x812)"
        )

    @allure.title("Banner renders without horizontal overflow on mobile landscape (812x375)")
    @pytest.mark.responsive
    def test_mobile_landscape_no_overflow(self, promo_banner_landscape: PromoBannerPage):
        allure.attach(
            promo_banner_landscape.screenshot_bytes(),
            name="mobile_landscape_812x375",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not promo_banner_landscape.has_horizontal_overflow(), (
            "Horizontal overflow detected on mobile landscape (812x375)"
        )
        assert promo_banner_landscape.is_banner_visible(), (
            "Banner is not visible on mobile landscape (812x375)"
        )
