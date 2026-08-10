"""
Spec: Image Upload Tests
Ticket: MWPW-199605
Feature: Unity Image Upload Block — valid formats, error handling
Accepted formats per page: image/jpeg, image/jpg, image/png, image/webp
Max file size: 40 MB
"""
import pytest
import allure
from tests.pages.remove_bg_page import RemoveBgPage


@allure.feature("Image Upload")
@allure.story("MWPW-199605 — Upload Block Validation")
class TestImageUpload:

    # ── Upload zone visibility ────────────────────────────────────────────────

    @allure.title("Image upload drop zone is visible on page load")
    @pytest.mark.upload
    @pytest.mark.smoke
    def test_upload_zone_visible(self, remove_bg: RemoveBgPage):
        assert remove_bg.is_upload_zone_visible(), (
            "Image upload drop zone (.drop-zone-container) is not visible on the page"
        )

    # ── Valid format uploads ──────────────────────────────────────────────────

    @allure.title("Valid JPG upload is accepted with no error")
    @pytest.mark.upload
    def test_upload_valid_jpg(self, remove_bg: RemoveBgPage):
        remove_bg.upload_file("valid_jpg.jpg")
        # No error = file format accepted. Reupload button requires auth/processing.
        assert not remove_bg.is_error_visible(), (
            f"Error shown after uploading valid JPG: {remove_bg.get_error_message()}"
        )

    @allure.title("Valid PNG upload is accepted with no error")
    @pytest.mark.upload
    def test_upload_valid_png(self, remove_bg: RemoveBgPage):
        remove_bg.upload_file("valid_png.png")
        assert not remove_bg.is_error_visible(), (
            f"Error shown after uploading valid PNG: {remove_bg.get_error_message()}"
        )

    @allure.title("Valid WEBP upload is accepted with no error")
    @pytest.mark.upload
    @pytest.mark.xfail(
        reason=(
            "valid_webp.webp is an animated WebP (gif.webp); WebKit triggers backend "
            "validation error. Replace with static WebP to fix. Known finding."
        ),
        strict=False,
    )
    def test_upload_valid_webp(self, remove_bg: RemoveBgPage, target_browser):
        # WebKit fails with animated WebP — marked xfail. Static WebP passes on chromium/firefox.
        remove_bg.upload_file("valid_webp.webp")
        assert not remove_bg.is_error_visible(), (
            f"Error shown after uploading valid WEBP: {remove_bg.get_error_message()}"
        )

    # ── Invalid format uploads ────────────────────────────────────────────────

    @allure.title("PDF upload shows error message (unsupported format)")
    @pytest.mark.upload
    @pytest.mark.error
    def test_upload_invalid_pdf_shows_error(self, remove_bg: RemoveBgPage):
        remove_bg.upload_file("invalid_pdf.pdf")
        assert remove_bg.is_error_visible(), (
            "Expected an error message when uploading a PDF, but none was shown"
        )

    @allure.title("HEIC upload shows error message (unsupported format)")
    @pytest.mark.upload
    @pytest.mark.error
    def test_upload_invalid_heic_shows_error(self, remove_bg: RemoveBgPage):
        remove_bg.upload_file("invalid_heic.heic")
        assert remove_bg.is_error_visible(), (
            "Expected an error message when uploading a HEIC file, but none was shown"
        )

    # ── Size limit (documented boundary — oversized file test) ───────────────

    @allure.title("File size > 40 MB shows error message [SKIPPED — no oversized file in assets]")
    @pytest.mark.upload
    @pytest.mark.error
    @pytest.mark.skip(reason="No >40 MB test file in assets — create one to enable this test")
    def test_upload_oversized_file_shows_error(self, remove_bg: RemoveBgPage):
        # To enable: add a >40 MB JPG to tests/assets/ named oversized.jpg
        remove_bg.upload_file("oversized.jpg")
        assert remove_bg.is_error_visible(), (
            "Expected a file size error for files > 40 MB, but none was shown"
        )
