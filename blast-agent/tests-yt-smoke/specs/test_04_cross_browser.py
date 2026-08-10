"""
Spec: Scenario Group 6 — Cross-Browser Compatibility
Ticket: MWPW-199796  |  Tags: @smoke @compat
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery — Smoke")
@allure.story("MWPW-199796 | Group 6: Cross-Browser — Heading & Cards")
class TestCrossBrowser:

    @allure.title("[smoke][compat] Firefox — gallery heading visible and at least 1 card present")
    @allure.description(
        "Open the YouTube Gallery page in Firefox headless, dismiss locale modal, "
        "and verify heading (h2.heading-xl) is visible and card count >= 1."
    )
    @pytest.mark.smoke
    @pytest.mark.compat
    def test_firefox_heading_and_cards(self, gallery_firefox: YouTubeGalleryPage):
        allure.attach(
            gallery_firefox.screenshot_bytes(),
            name="firefox_page_load",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery_firefox.is_heading_visible(), (
            "[Firefox] Gallery heading (h2.heading-xl) is not visible."
        )
        count = gallery_firefox.get_card_count()
        allure.attach(
            f"Firefox card count: {count}",
            name="firefox_card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, (
            f"[Firefox] Expected at least 1 gallery card, found {count}."
        )

    @allure.title("[smoke][compat] WebKit (Safari) — gallery heading visible and at least 1 card present")
    @allure.description(
        "Open the YouTube Gallery page in WebKit headless, dismiss locale modal, "
        "and verify heading (h2.heading-xl) is visible and card count >= 1."
    )
    @pytest.mark.smoke
    @pytest.mark.compat
    def test_webkit_heading_and_cards(self, gallery_webkit: YouTubeGalleryPage):
        allure.attach(
            gallery_webkit.screenshot_bytes(),
            name="webkit_page_load",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery_webkit.is_heading_visible(), (
            "[WebKit] Gallery heading (h2.heading-xl) is not visible."
        )
        count = gallery_webkit.get_card_count()
        allure.attach(
            f"WebKit card count: {count}",
            name="webkit_card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, (
            f"[WebKit] Expected at least 1 gallery card, found {count}."
        )
