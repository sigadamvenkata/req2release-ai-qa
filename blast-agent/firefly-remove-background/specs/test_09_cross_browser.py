"""
Spec: Scenario Group 9 — Cross-Browser Compatibility
Ticket: MWPW-200902  |  Tags: @compat
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage


@allure.feature("Background Generator — Cross-Browser")
@allure.story("MWPW-200902 | Group 9: Cross-Browser Compatibility")
class TestCrossBrowser:

    @allure.title("[compat] Marquee heading and upload CTA render correctly in Firefox")
    @allure.description(
        "Open the Background Generator page in Firefox headless at 1440x900 and "
        "verify the H1 heading and upload CTA are visible."
    )
    @pytest.mark.compat
    def test_firefox_heading_and_upload_cta(self, bg_gen_firefox: BackgroundGeneratorPage):
        allure.attach(
            bg_gen_firefox.screenshot_bytes(),
            name="firefox_page_load",
            attachment_type=allure.attachment_type.PNG,
        )
        assert bg_gen_firefox.is_h1_visible(), "[Firefox] H1 heading is not visible."
        assert bg_gen_firefox.is_upload_cta_visible(), (
            "[Firefox] 'Upload your image' CTA is not visible."
        )

    @allure.title("[compat] Marquee heading and upload CTA render correctly in WebKit (Safari)")
    @allure.description(
        "Open the Background Generator page in WebKit headless at 1440x900 and "
        "verify the H1 heading and upload CTA are visible."
    )
    @pytest.mark.compat
    def test_webkit_heading_and_upload_cta(self, bg_gen_webkit: BackgroundGeneratorPage):
        allure.attach(
            bg_gen_webkit.screenshot_bytes(),
            name="webkit_page_load",
            attachment_type=allure.attachment_type.PNG,
        )
        assert bg_gen_webkit.is_h1_visible(), "[WebKit] H1 heading is not visible."
        assert bg_gen_webkit.is_upload_cta_visible(), (
            "[WebKit] 'Upload your image' CTA is not visible."
        )
