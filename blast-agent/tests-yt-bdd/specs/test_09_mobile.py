"""
Spec: Group 9 — Mobile Compatibility
Feature file: features/09_mobile.feature
Ticket: MWPW-199796  |  Tags: @smoke @mobile
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 9: Mobile Viewports — Portrait & Landscape")
class TestMobile:

    @allure.title("[9.1][smoke][mobile] Portrait 375x812 — grid, cards, no overflow")
    @allure.description(
        "Simulate iPhone portrait (375x812). The gallery grid must be visible, "
        "at least 1 card present, and no horizontal scroll must occur."
    )
    @pytest.mark.smoke
    @pytest.mark.mobile
    def test_portrait_375x812(self, gallery_portrait: YouTubeGalleryPage):
        allure.attach(
            gallery_portrait.screenshot_bytes(),
            name="portrait_375x812",
            attachment_type=allure.attachment_type.PNG,
        )

        assert gallery_portrait.is_grid_visible(), (
            "[Portrait 375x812] .pre-yt-grid is not visible."
        )

        count = gallery_portrait.get_card_count()
        allure.attach(
            f"Portrait card count: {count}",
            name="portrait_card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, f"[Portrait 375x812] Expected >=1 card, found {count}."

        scroll_w, inner_w = gallery_portrait.get_scroll_vs_inner_width()
        allure.attach(
            f"scrollWidth={scroll_w}  innerWidth={inner_w}",
            name="scroll_dimensions",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert scroll_w <= inner_w, (
            f"[Portrait 375x812] Horizontal overflow: scrollWidth={scroll_w} > innerWidth={inner_w}"
        )

    @allure.title("[9.2][smoke][mobile] Landscape 812x375 — grid, cards, no overflow")
    @allure.description(
        "Simulate mobile landscape (812x375). Same checks as portrait."
    )
    @pytest.mark.smoke
    @pytest.mark.mobile
    def test_landscape_812x375(self, gallery_landscape: YouTubeGalleryPage):
        allure.attach(
            gallery_landscape.screenshot_bytes(),
            name="landscape_812x375",
            attachment_type=allure.attachment_type.PNG,
        )

        assert gallery_landscape.is_grid_visible(), (
            "[Landscape 812x375] .pre-yt-grid is not visible."
        )

        count = gallery_landscape.get_card_count()
        allure.attach(
            f"Landscape card count: {count}",
            name="landscape_card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, f"[Landscape 812x375] Expected >=1 card, found {count}."

        scroll_w, inner_w = gallery_landscape.get_scroll_vs_inner_width()
        allure.attach(
            f"scrollWidth={scroll_w}  innerWidth={inner_w}",
            name="landscape_scroll",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert scroll_w <= inner_w, (
            f"[Landscape 812x375] Horizontal overflow: scrollWidth={scroll_w} > innerWidth={inner_w}"
        )

    @allure.title("[9.3][smoke][mobile] Portrait 375x812 — heading visible on mobile")
    @pytest.mark.smoke
    @pytest.mark.mobile
    def test_heading_visible_on_mobile(self, gallery_portrait: YouTubeGalleryPage):
        allure.attach(
            gallery_portrait.screenshot_bytes(),
            name="mobile_heading_check",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery_portrait.is_heading_visible(), (
            "[Mobile 375x812] h2.heading-xl is not visible. "
            "Check locale modal dismiss on mobile viewport."
        )
