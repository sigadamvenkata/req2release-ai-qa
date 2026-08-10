"""
Spec: Scenario Group 10 — Mobile Compatibility
Ticket: MWPW-200902  |  Tags: @mobile

Breakpoint visibility confirmed via live resize test (2026-07-17):
  <600px wide     -> .drop-zone-container.mobile-up  visible
  600-1199px wide -> .drop-zone-container.tablet-up  visible
  >=1200px wide   -> .drop-zone-container.desktop-up visible
No horizontal overflow was observed at 375x812, 812x375, or 768x1024.
Mobile has no native OS drag-and-drop, so only the click-to-upload CTA is
exercised on mobile viewports.
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage

VALID_IMAGE = "female.png"


@allure.feature("Background Generator — Mobile")
@allure.story("MWPW-200902 | Group 10: Mobile Viewports")
class TestMobile:

    @allure.title("[mobile] Upload block renders on 375x812 portrait (iPhone) with no overflow")
    @allure.description(
        "Set viewport to 375x812 (mobile portrait), open the page, and verify the "
        "upload CTA is visible with no horizontal overflow."
    )
    @pytest.mark.mobile
    def test_mobile_portrait_upload_cta_visible(self, bg_gen_mobile: BackgroundGeneratorPage):
        allure.attach(
            bg_gen_mobile.screenshot_bytes(),
            name="mobile_portrait_375x812",
            attachment_type=allure.attachment_type.PNG,
        )
        assert bg_gen_mobile.is_upload_cta_visible(), (
            "[Mobile 375x812] 'Upload your image' CTA is not visible."
        )
        scroll_w = bg_gen_mobile.page.evaluate("document.body.scrollWidth")
        inner_w = bg_gen_mobile.page.evaluate("window.innerWidth")
        allure.attach(
            f"scrollWidth={scroll_w}  innerWidth={inner_w}",
            name="mobile_scroll_dimensions",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert scroll_w <= inner_w, (
            f"[Mobile 375x812] Horizontal overflow: scrollWidth={scroll_w} > innerWidth={inner_w}."
        )

    @allure.title("[mobile] Upload block renders in landscape orientation (812x375) with no overflow")
    @allure.description(
        "Set viewport to 812x375 (mobile landscape), open the page, and verify the "
        "upload CTA is visible with no horizontal overflow."
    )
    @pytest.mark.mobile
    def test_mobile_landscape_upload_cta_visible(
        self, bg_gen_mobile_landscape: BackgroundGeneratorPage
    ):
        allure.attach(
            bg_gen_mobile_landscape.screenshot_bytes(),
            name="mobile_landscape_812x375",
            attachment_type=allure.attachment_type.PNG,
        )
        assert bg_gen_mobile_landscape.is_upload_cta_visible(), (
            "[Mobile 812x375] 'Upload your image' CTA is not visible."
        )
        scroll_w = bg_gen_mobile_landscape.page.evaluate("document.body.scrollWidth")
        inner_w = bg_gen_mobile_landscape.page.evaluate("window.innerWidth")
        assert scroll_w <= inner_w, (
            f"[Mobile 812x375] Horizontal overflow: scrollWidth={scroll_w} > innerWidth={inner_w}."
        )

    @allure.title("[mobile] Click-to-upload works on a mobile (portrait) viewport")
    @allure.description(
        f"On a 375x812 mobile viewport, tap the upload CTA and select '{VALID_IMAGE}'. "
        "Verify no error message is displayed."
    )
    @pytest.mark.mobile
    def test_mobile_click_upload(self, bg_gen_mobile: BackgroundGeneratorPage):
        bg_gen_mobile.upload_file(VALID_IMAGE)
        allure.attach(
            bg_gen_mobile.screenshot_bytes(),
            name="mobile_after_upload",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not bg_gen_mobile.is_error_visible(), (
            f"[Mobile 375x812] Error shown after uploading valid image: "
            f"{bg_gen_mobile.get_error_message()}"
        )
