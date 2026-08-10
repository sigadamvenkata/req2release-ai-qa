"""
Spec: Scenario Group 2 — Grid Layout & Card Structure
Ticket: MWPW-199796
Feature: YouTube Gallery Block — Grid renders correctly with aligned cards
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery — UI")
@allure.story("MWPW-199796 | Group 2: Grid Layout & Card Structure")
class TestGridLayout:

    @allure.title("[smoke][ui] Gallery renders at least one card in a grid layout")
    @allure.description(
        "Verify the .pre-yt-grid container is visible and contains "
        "at least one .pre-yt-card element."
    )
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_grid_is_visible_with_cards(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="grid_view",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_grid_visible(), (
            "Gallery grid container (.pre-yt-grid) is not visible on the page."
        )
        count = gallery.get_card_count()
        assert count >= 1, (
            f"Expected at least 1 gallery card (.pre-yt-card), found {count}."
        )

    @allure.title("[ui] Cards are arranged in a grid with consistent alignment")
    @allure.description(
        "Verify all cards share the same rendered pixel width "
        "and none overflow the grid container."
    )
    @pytest.mark.ui
    def test_cards_have_consistent_width(self, gallery: YouTubeGalleryPage):
        widths = gallery.get_card_widths()
        assert widths, "No cards found — cannot check alignment."

        allure.attach(
            str(widths),
            name="card_widths_px",
            attachment_type=allure.attachment_type.TEXT,
        )

        unique_widths = set(widths)
        assert len(unique_widths) == 1, (
            f"Cards do not have a consistent width. Found widths: {unique_widths}"
        )

    @allure.title("[ui] No card overflows the grid container horizontally")
    @pytest.mark.ui
    def test_cards_do_not_overflow_grid(self, gallery: YouTubeGalleryPage):
        overflows = gallery.cards_overflow_grid()
        assert not overflows, (
            "One or more cards overflow the grid container horizontally."
        )
