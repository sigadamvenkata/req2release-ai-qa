"""
Spec: Scenario Group 8 — Page Load & HTTP Status
Ticket: MWPW-200902  |  Tags: @smoke
"""
import pytest
import allure
import requests as http_requests
from pages.background_generator_page import BackgroundGeneratorPage
from locators.bg_generator_locators import PAGE_URL, L


@allure.feature("Background Generator — Smoke")
@allure.story("MWPW-200902 | Group 8: Page Load & HTTP Status")
class TestSmoke:

    @allure.title("[smoke] Page returns HTTP 200")
    @allure.description("Verify the staging URL returns HTTP 200 and the page title is non-empty.")
    @pytest.mark.smoke
    def test_http_200(self, bg_gen: BackgroundGeneratorPage):
        resp = http_requests.get(PAGE_URL, timeout=15)
        allure.attach(
            f"URL: {PAGE_URL}\nStatus: {resp.status_code}",
            name="http_response",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert resp.status_code == 200, (
            f"Expected HTTP 200, got {resp.status_code} for {PAGE_URL}"
        )
        title = bg_gen.get_page_title()
        assert title, "Page title is empty after successful load."

    @allure.title("[smoke] Upload block is present after page load")
    @allure.description(
        "Verify the marquee block and the 'Upload your image' CTA are present "
        "in the DOM after the page reaches network idle state."
    )
    @pytest.mark.smoke
    def test_upload_block_present_after_load(self, bg_gen: BackgroundGeneratorPage):
        assert bg_gen.is_visible(L.MARQUEE), (
            "Marquee block (.upload-marquee) is not present/visible after page load."
        )
        assert bg_gen.is_upload_cta_visible(), (
            "'Upload your image' CTA is not visible after page load."
        )
