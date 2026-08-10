"""
Spec: Group 5 — Page Load & HTTP Status
Feature file: features/05_page_load.feature
Ticket: MWPW-199796  |  Tags: @smoke @critical
"""
import allure
import pytest
import requests as http
import truststore
truststore.inject_into_ssl()

from locators.gallery_locators import PAGE_URL
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 5: Page Load & HTTP Status")
class TestPageLoad:

    @allure.title("[5.1][smoke] Page returns HTTP 200")
    @allure.description(
        f"A GET request to {PAGE_URL} must return HTTP 200. "
        "If this fails the page is not accessible and all other tests are invalid."
    )
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_page_http_200(self):
        resp = http.get(PAGE_URL, timeout=30, allow_redirects=True)
        allure.attach(
            f"URL: {PAGE_URL}\nStatus: {resp.status_code}\nFinal URL: {resp.url}",
            name="http_response",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert resp.status_code == 200, (
            f"Expected HTTP 200, got {resp.status_code} for {PAGE_URL}"
        )

    @allure.title("[5.2][smoke] Gallery block, grid and cards present after page load")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_gallery_present_after_load(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="page_load_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_grid_visible(), (
            ".pre-yt-grid is not visible after page load."
        )
        count = gallery.get_card_count()
        allure.attach(
            f"Card count: {count}",
            name="card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, (
            f"Expected at least 1 .pre-yt-card after page load, found {count}."
        )

    @allure.title("[5.3][smoke] First card thumbnail image is visible on load")
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_first_thumbnail_visible(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="thumbnail_on_load",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_first_thumbnail_visible(), (
            "First .image-wrapper img is not visible after page load."
        )
        srcs = gallery.get_thumbnail_srcs()
        if srcs:
            allure.attach(
                f"First thumbnail src: {srcs[0]}",
                name="first_thumbnail_src",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert srcs[0], "First thumbnail src attribute is empty."
