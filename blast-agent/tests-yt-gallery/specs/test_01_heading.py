"""
Spec: Scenario Group 1 — Page Load & Heading
Ticket: MWPW-199796
Feature: YouTube Gallery Block — Gallery heading is valid and visible
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery — UI")
@allure.story("MWPW-199796 | Group 1: Page Load & Heading")
class TestHeading:

    @allure.title("[smoke][ui] Gallery block has a valid visible heading")
    @allure.description(
        "Verify that the gallery H2 heading is rendered on the page "
        "and contains non-empty text."
    )
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_heading_is_visible(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="page_on_load",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_heading_visible(), (
            "Gallery heading (h2.heading-xl) is not visible on the page."
        )

    @allure.title("[ui] Heading text is non-empty")
    @allure.description(
        "Verify the gallery heading contains meaningful text "
        "(not blank or whitespace-only)."
    )
    @pytest.mark.ui
    def test_heading_text_is_not_empty(self, gallery: YouTubeGalleryPage):
        text = gallery.get_heading_text()
        assert text, f"Heading text is empty. Got: '{text}'"
        assert len(text) > 3, f"Heading text too short: '{text}'"
