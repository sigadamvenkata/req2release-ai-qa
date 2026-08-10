"""
Spec: Group 8 — Cross-Browser Compatibility
Feature file: features/08_cross_browser.feature
Ticket: MWPW-199796  |  Tags: @smoke @compat
Known bug: MWPW-199812 — heading may fail on Firefox/WebKit due to locale modal
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 8: Cross-Browser — Firefox & WebKit")
class TestCrossBrowser:

    @allure.title("[8.1][smoke][compat] Firefox — heading visible, >=1 card present")
    @allure.description(
        "Open the gallery in Firefox headless 1440x900, dismiss locale modal, "
        "verify h2.heading-xl is visible and at least 1 card is present. "
        "Known bug: MWPW-199812 may intermittently block heading."
    )
    @pytest.mark.smoke
    @pytest.mark.compat
    def test_firefox_heading_and_cards(self, gallery_firefox: YouTubeGalleryPage):
        allure.attach(
            gallery_firefox.screenshot_bytes(),
            name="firefox_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

        assert gallery_firefox.is_heading_visible(), (
            "[Firefox] Gallery heading (h2.heading-xl) is not visible. "
            "Bug: MWPW-199812"
        )

        count = gallery_firefox.get_card_count()
        allure.attach(
            f"Firefox card count: {count}",
            name="firefox_card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, f"[Firefox] Expected >=1 card, found {count}."

    @allure.title("[8.2][smoke][compat] WebKit — heading visible, >=1 card present")
    @allure.description(
        "Open the gallery in WebKit (Safari engine) headless 1440x900, "
        "dismiss locale modal, verify heading and cards. "
        "Known bug: MWPW-199812 may intermittently block heading."
    )
    @pytest.mark.smoke
    @pytest.mark.compat
    def test_webkit_heading_and_cards(self, gallery_webkit: YouTubeGalleryPage):
        allure.attach(
            gallery_webkit.screenshot_bytes(),
            name="webkit_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

        assert gallery_webkit.is_heading_visible(), (
            "[WebKit] Gallery heading (h2.heading-xl) is not visible. "
            "Bug: MWPW-199812"
        )

        count = gallery_webkit.get_card_count()
        allure.attach(
            f"WebKit card count: {count}",
            name="webkit_card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, f"[WebKit] Expected >=1 card, found {count}."
