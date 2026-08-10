"""
Spec: Scenario Group 3 — Valid Format Upload via Click CTA
Ticket: MWPW-200902  |  Tags: @upload

NOTE: All upload scenarios in this suite use tests/assets/female.png as the
single designated valid test asset (per automation instructions). The original
test_cases.md Group 3 called out separate JPG/PNG/WEBP scenarios; since only
one valid asset (a PNG) was provided for automation, those are consolidated
into a single "valid image is accepted" case here. Add JPG/WEBP assets and
extra parametrized cases if per-format coverage is required later.
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage

VALID_IMAGE = "female.png"


@allure.feature("Background Generator — Image Upload")
@allure.story("MWPW-200902 | Group 3: Valid Upload via Click CTA")
class TestUploadValidClick:

    @allure.title("[upload] Valid image upload via the 'Upload your image' CTA is accepted")
    @allure.description(
        f"Upload '{VALID_IMAGE}' via the hidden file input behind the 'Upload your "
        "image' CTA and verify no error message is displayed."
    )
    @pytest.mark.upload
    def test_upload_valid_image_via_click(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file(VALID_IMAGE)
        allure.attach(
            bg_gen.screenshot_bytes(),
            name="after_upload_click",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not bg_gen.is_error_visible(), (
            f"Error shown after uploading valid image '{VALID_IMAGE}': "
            f"{bg_gen.get_error_message()}"
        )
