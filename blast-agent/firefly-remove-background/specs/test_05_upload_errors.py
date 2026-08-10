"""
Spec: Scenario Group 5 — Invalid Format / Size / Dimension Rejection
Ticket: MWPW-200902  |  Tags: @upload @error

Error copy confirmed from the always-present .workflow-upload config block
(live rendered DOM, 2026-07-17). The live toast/error element itself was not
triggered during read-only discovery — ERROR_CANDIDATES in
locators/bg_generator_locators.py must be re-confirmed the first time these
tests are actually run.
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage

VALID_IMAGE = "female.png"


@allure.feature("Background Generator — Image Upload")
@allure.story("MWPW-200902 | Group 5: Invalid Upload / Errors")
class TestUploadErrors:

    @allure.title("[upload][error] Unsupported file type (PDF) shows the file-type error")
    @allure.description(
        "Upload invalid_pdf.pdf and verify the error "
        "'We are unable to process this file type. Please try again.' is displayed."
    )
    @pytest.mark.upload
    @pytest.mark.error
    def test_unsupported_pdf_shows_filetype_error(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file("invalid_pdf.pdf")
        assert bg_gen.is_error_visible(), (
            "Expected a file-type error after uploading a PDF, but none was shown."
        )
        assert "unable to process this file type" in bg_gen.get_error_message().lower(), (
            f"Unexpected error text: '{bg_gen.get_error_message()}'"
        )

    @allure.title("[upload][error] Unsupported file type (HEIC) shows the file-type error")
    @allure.description(
        "Upload invalid_heic.heic and verify the error "
        "'We are unable to process this file type. Please try again.' is displayed."
    )
    @pytest.mark.upload
    @pytest.mark.error
    def test_unsupported_heic_shows_filetype_error(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file("invalid_heic.heic")
        assert bg_gen.is_error_visible(), (
            "Expected a file-type error after uploading a HEIC file, but none was shown."
        )
        assert "unable to process this file type" in bg_gen.get_error_message().lower(), (
            f"Unexpected error text: '{bg_gen.get_error_message()}'"
        )

    @allure.title("[upload][error] Dropping more than one file at once shows the file-count error")
    @allure.description(
        "Drag-and-drop two files onto the drop zone at once and verify the error "
        "'Only one file can be uploaded at a time.' is displayed. Note: the real "
        "<input type=\"file\"> has no 'multiple' attribute (Playwright's "
        "set_input_files() correctly refuses >1 file on it), so this error is "
        "only reachable via a multi-file drop, not the file picker."
    )
    @pytest.mark.upload
    @pytest.mark.error
    def test_multiple_files_shows_filecount_error(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_files_via_drag_and_drop([VALID_IMAGE, "landscape.jpg"])
        assert bg_gen.is_error_visible(), (
            "Expected a file-count error after dropping two files, but none was shown."
        )
        assert "only one file" in bg_gen.get_error_message().lower(), (
            f"Unexpected error text: '{bg_gen.get_error_message()}'"
        )

    @allure.title(
        "[upload][error][SKIPPED] File size > 100MB shows the file-size error"
    )
    @pytest.mark.upload
    @pytest.mark.error
    @pytest.mark.skip(reason="No >100MB test asset in tests/assets/ — add one to enable this test")
    def test_oversized_file_shows_filesize_error(self, bg_gen: BackgroundGeneratorPage):
        # To enable: add a >100MB image to tests/assets/ named oversized.jpg
        bg_gen.upload_file("oversized.jpg")
        assert bg_gen.is_error_visible(), (
            "Expected a file-size error for files > 100MB, but none was shown."
        )
        assert "100mb" in bg_gen.get_error_message().lower(), (
            f"Unexpected error text: '{bg_gen.get_error_message()}'"
        )

    @allure.title(
        "[upload][error][SKIPPED] Image smaller than 512x512px shows the min-dimension error"
    )
    @pytest.mark.upload
    @pytest.mark.error
    @pytest.mark.skip(reason="No <512x512px test asset in tests/assets/ — add one to enable this test")
    def test_undersized_image_shows_dimension_error(self, bg_gen: BackgroundGeneratorPage):
        # To enable: add a valid-format image smaller than 512x512px to tests/assets/
        # named undersized.png
        bg_gen.upload_file("undersized.png")
        assert bg_gen.is_error_visible(), (
            "Expected a minimum-dimension error for an image < 512x512px, but none was shown."
        )
        assert "minimum dimensions" in bg_gen.get_error_message().lower(), (
            f"Unexpected error text: '{bg_gen.get_error_message()}'"
        )

    @allure.title(
        "[upload][error][SKIPPED] Backend/request failure shows the generic request error"
    )
    @pytest.mark.upload
    @pytest.mark.error
    @pytest.mark.skip(
        reason="Requires a confirmed upload API endpoint to intercept and force-fail — "
               "endpoint not yet confirmed for this block (see locators module docstring)"
    )
    def test_request_failure_shows_generic_error(self, bg_gen: BackgroundGeneratorPage):
        # To enable: page.route() the confirmed upload endpoint and fulfill with a 5xx,
        # then upload a valid image and assert the "Unable to process the request" error.
        bg_gen.upload_file(VALID_IMAGE)
        assert bg_gen.is_error_visible(), (
            "Expected a generic request-failure error, but none was shown."
        )
        assert "unable to process the request" in bg_gen.get_error_message().lower(), (
            f"Unexpected error text: '{bg_gen.get_error_message()}'"
        )
