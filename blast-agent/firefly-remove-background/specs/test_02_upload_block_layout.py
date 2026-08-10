"""
Spec: Scenario Group 2 — Upload Block & CTA Layout
Ticket: MWPW-200902  |  Tags: @ui
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage


@allure.feature("Background Generator — Upload Block")
@allure.story("MWPW-200902 | Group 2: Upload Block & CTA Layout")
class TestUploadBlockLayout:

    @allure.title("[ui] Upload CTA and drop zone are visible")
    @allure.description(
        "Verify the 'Upload your image' CTA and the drag-and-drop zone are both "
        "visible in the currently-active breakpoint variant of the upload block."
    )
    @pytest.mark.ui
    def test_upload_cta_and_drop_zone_visible(self, bg_gen: BackgroundGeneratorPage):
        assert bg_gen.is_upload_cta_visible(), (
            "'Upload your image' CTA is not visible."
        )
        cta_text = bg_gen.get_upload_cta_text()
        assert "Upload your image" in cta_text, (
            f"Expected CTA text to contain 'Upload your image', got: '{cta_text}'"
        )
        assert bg_gen.is_drop_zone_visible(), (
            "Drag-and-drop zone (.drop-zone) is not visible."
        )

    @allure.title("[ui] File format guidance text is correct")
    @allure.description(
        "Verify the format/size hint reads exactly: "
        "'File must be JPEG(JPG), PNG, or WEBP and up to 100MB.'"
    )
    @pytest.mark.ui
    def test_format_hint_text(self, bg_gen: BackgroundGeneratorPage):
        expected = "File must be JPEG(JPG), PNG, or WEBP and up to 100MB."
        actual = bg_gen.get_format_hint_text()
        assert actual == expected, (
            f"Format hint text mismatch.\nExpected: '{expected}'\nActual:   '{actual}'"
        )

    @allure.title("[ui] Terms of Use and Privacy Policy links are present")
    @allure.description(
        "Verify the upload block footer links to the Terms of Use and Privacy "
        "Policy pages."
    )
    @pytest.mark.ui
    def test_terms_and_privacy_links(self, bg_gen: BackgroundGeneratorPage):
        terms_href = bg_gen.get_terms_href()
        privacy_href = bg_gen.get_privacy_href()
        assert "terms.html" in terms_href, (
            f"Expected a Terms of Use link containing 'terms.html', got: '{terms_href}'"
        )
        assert "privacy.html" in privacy_href, (
            f"Expected a Privacy Policy link containing 'privacy.html', got: '{privacy_href}'"
        )
