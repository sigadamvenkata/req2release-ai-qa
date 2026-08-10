"""
Spec: Group 7 — No Click Navigation
Feature file: features/07_no_navigation.feature
Ticket: MWPW-199796  |  Tags: @smoke @functional
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 7: No Click Navigation from Card")
class TestNoNavigation:

    @allure.title("[7.1][smoke] Clicking a card does not navigate away from the page")
    @allure.description(
        "Per spec, cards should not act as links. Clicking .pre-yt-card "
        "must leave the browser URL unchanged."
    )
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_click_card_no_navigation(self, gallery: YouTubeGalleryPage):
        url_before = gallery.get_current_url()
        allure.attach(
            f"URL before click: {url_before}",
            name="url_before",
            attachment_type=allure.attachment_type.TEXT,
        )

        gallery.click_first_card()

        url_after = gallery.get_current_url()
        allure.attach(
            f"URL after click: {url_after}",
            name="url_after",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            gallery.screenshot_bytes(),
            name="after_card_click",
            attachment_type=allure.attachment_type.PNG,
        )

        assert url_before == url_after, (
            f"Page navigated after clicking a card!\n"
            f"  Before: {url_before}\n"
            f"  After : {url_after}"
        )
        assert gallery.is_grid_visible(), (
            "Gallery grid (.pre-yt-grid) disappeared after clicking a card."
        )
