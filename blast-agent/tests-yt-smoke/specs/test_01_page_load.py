"""
Spec: Scenario Groups 1, 2, 3 — Page Load, Heading, Grid, Thumbnail
Ticket: MWPW-199796  |  Tags: @smoke @ui
"""
import pytest
import allure
import requests as http_requests
from pages.yt_gallery_page import YouTubeGalleryPage
from locators.yt_smoke_locators import PAGE_URL


@allure.feature("YouTube Gallery — Smoke")
@allure.story("MWPW-199796 | Group 1-3: Page Load, Heading, Grid, Thumbnail")
class TestPageLoad:

    @allure.title("[smoke] Page loads successfully with HTTP 200")
    @allure.description("Verify the gallery page URL returns HTTP 200 and the page title is non-empty.")
    @pytest.mark.smoke
    def test_http_200(self, gallery: YouTubeGalleryPage):
        resp = http_requests.get(PAGE_URL, timeout=15)
        allure.attach(
            f"URL: {PAGE_URL}\nStatus: {resp.status_code}",
            name="http_response",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert resp.status_code == 200, (
            f"Expected HTTP 200, got {resp.status_code} for {PAGE_URL}"
        )
        title = gallery.get_page_title()
        assert title, "Page title is empty after successful load."

    @allure.title("[smoke][ui] Gallery heading is visible and non-empty")
    @allure.description(
        "Verify h2.heading-xl is visible after dismissing the locale modal "
        "and contains non-empty text."
    )
    @pytest.mark.smoke
    def test_heading_visible(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="page_after_modal_dismiss",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_heading_visible(), (
            "Gallery heading (h2.heading-xl) is not visible after modal dismiss."
        )
        text = gallery.get_heading_text()
        assert text, f"Heading text is empty. Got: '{text}'"

    @allure.title("[smoke][ui] Gallery grid is visible with at least 1 card")
    @allure.description(
        "Verify .pre-yt-grid is present and contains at least one .pre-yt-card."
    )
    @pytest.mark.smoke
    def test_grid_with_cards(self, gallery: YouTubeGalleryPage):
        assert gallery.is_grid_visible(), (
            "Gallery grid (.pre-yt-grid) is not visible on the page."
        )
        count = gallery.get_card_count()
        allure.attach(
            f"Card count: {count}",
            name="card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, (
            f"Expected at least 1 gallery card, found {count}."
        )

    @allure.title("[smoke][ui] First card displays a thumbnail image")
    @allure.description(
        "Verify the first .pre-yt-card has a visible thumbnail (.image-wrapper img) "
        "with a non-empty src attribute."
    )
    @pytest.mark.smoke
    def test_thumbnail_visible(self, gallery: YouTubeGalleryPage):
        assert gallery.is_first_thumbnail_visible(), (
            "First card thumbnail (.image-wrapper img) is not visible."
        )
        src = gallery.get_first_thumbnail_src()
        allure.attach(
            f"Thumbnail src: {src}",
            name="thumbnail_src",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert src, "First card thumbnail has an empty src attribute."
