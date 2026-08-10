"""
Spec: Scenario Group 7 — Mobile Compatibility (Viewport Simulation)
Ticket: MWPW-199796  |  Tags: @smoke @mobile
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery — Smoke")
@allure.story("MWPW-199796 | Group 7: Mobile Portrait Viewport 375x812")
class TestMobile:

    @allure.title("[smoke][mobile] Gallery grid and cards visible on 375x812 portrait viewport")
    @allure.description(
        "Set viewport to 375x812 (iPhone portrait), open the YouTube Gallery page, "
        "and verify the grid container and at least 1 card are visible "
        "without horizontal overflow."
    )
    @pytest.mark.smoke
    @pytest.mark.mobile
    def test_mobile_portrait_grid_visible(self, gallery_mobile: YouTubeGalleryPage):
        allure.attach(
            gallery_mobile.screenshot_bytes(),
            name="mobile_portrait_375x812",
            attachment_type=allure.attachment_type.PNG,
        )

        assert gallery_mobile.is_grid_visible(), (
            "[Mobile 375x812] Gallery grid (.pre-yt-grid) is not visible."
        )

        count = gallery_mobile.get_card_count()
        allure.attach(
            f"Mobile card count: {count}",
            name="mobile_card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, (
            f"[Mobile 375x812] Expected at least 1 gallery card, found {count}."
        )

        scroll_w = gallery_mobile.page.evaluate("document.body.scrollWidth")
        inner_w  = gallery_mobile.page.evaluate("window.innerWidth")
        allure.attach(
            f"scrollWidth={scroll_w}  innerWidth={inner_w}",
            name="mobile_scroll_dimensions",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert scroll_w <= inner_w, (
            f"[Mobile 375x812] Horizontal overflow: scrollWidth={scroll_w} > innerWidth={inner_w}."
        )
