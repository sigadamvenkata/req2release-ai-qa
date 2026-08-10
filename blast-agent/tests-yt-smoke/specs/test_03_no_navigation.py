"""
Spec: Scenario Group 5 — No Click Action / Navigation
Ticket: MWPW-199796  |  Tags: @smoke @functional
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage
from locators.yt_smoke_locators import PAGE_URL


@allure.feature("YouTube Gallery — Smoke")
@allure.story("MWPW-199796 | Group 5: No Click Navigation from Card")
class TestNoNavigation:

    @allure.title("[smoke][functional] Clicking a card does not navigate away from the page")
    @allure.description(
        "Verify that clicking the first .pre-yt-card does not trigger "
        "any URL change or page navigation. The URL must remain the same after click."
    )
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_click_card_no_navigation(self, gallery: YouTubeGalleryPage):
        url_before = gallery.get_current_url()
        allure.attach(
            f"URL before click: {url_before}",
            name="url_before_click",
            attachment_type=allure.attachment_type.TEXT,
        )

        gallery.click_first_card()

        url_after = gallery.get_current_url()
        allure.attach(
            f"URL after click:  {url_after}",
            name="url_after_click",
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
