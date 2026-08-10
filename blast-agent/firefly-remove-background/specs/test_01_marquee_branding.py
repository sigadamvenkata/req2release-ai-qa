"""
Spec: Scenario Group 1 — Marquee Branding & Heading
Ticket: MWPW-200902  |  Tags: @ui
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage


@allure.feature("Background Generator — Marquee")
@allure.story("MWPW-200902 | Group 1: Marquee Branding & Heading")
class TestMarqueeBranding:

    @allure.title("[ui] Firefly mnemonic and wordmark are visible above the heading")
    @allure.description(
        "Verify the Firefly mnemonic image (firefly.svg) and the 'Adobe Firefly' "
        "wordmark text are visible in the marquee content block."
    )
    @pytest.mark.ui
    def test_mnemonic_and_wordmark_visible(self, bg_gen: BackgroundGeneratorPage):
        assert bg_gen.is_mnemonic_visible(), (
            "Firefly mnemonic image (img[src*='firefly.svg']) is not visible in the marquee."
        )
        wordmark = bg_gen.get_wordmark_text()
        assert "Adobe Firefly" in wordmark, (
            f"Expected 'Adobe Firefly' wordmark text near the mnemonic, got: '{wordmark}'"
        )

    @allure.title("[ui] H1 heading is visible and non-empty")
    @allure.description("Verify the marquee <h1> is visible and its text is not empty.")
    @pytest.mark.ui
    def test_h1_visible_and_non_empty(self, bg_gen: BackgroundGeneratorPage):
        allure.attach(
            bg_gen.screenshot_bytes(),
            name="marquee_after_modal_dismiss",
            attachment_type=allure.attachment_type.PNG,
        )
        assert bg_gen.is_h1_visible(), "Marquee <h1> is not visible."
        text = bg_gen.get_h1_text()
        assert text, f"H1 text is empty. Got: '{text}'"

    @allure.title(
        "[ui][known-issue] H1 text matches ticket-specified copy "
        "'Adobe Firefly AI background generator: Transform photos in a click'"
    )
    @allure.description(
        "MWPW-200902 requests the H1 itself read "
        "'Adobe Firefly AI background generator: Transform photos in a click'. "
        "As of 2026-07-17 the live stage H1 reads "
        "'AI background generator: Transform photos in a click.' — 'Adobe Firefly' "
        "appears only as separate branding text above the H1, not inside it. "
        "Marked xfail until confirmed with the reporter/design whether the "
        "mnemonic + wordmark satisfies the requirement or the H1 copy must change."
    )
    @pytest.mark.ui
    @pytest.mark.xfail(
        reason="Known discrepancy vs. MWPW-200902 ticket copy — H1 omits 'Adobe Firefly' prefix. "
               "Confirm intent before treating as a bug.",
        strict=False,
    )
    def test_h1_matches_ticket_copy(self, bg_gen: BackgroundGeneratorPage):
        text = bg_gen.get_h1_text()
        assert "Adobe Firefly" in text, (
            f"Ticket requires 'Adobe Firefly' inside the H1 text; got: '{text}'"
        )

    @allure.title("[ui] Subheading copy matches the ticket requirement")
    @allure.description(
        "Verify the subheading paragraph reads exactly: 'From a busy street scene "
        "to an alien planet, effortlessly create high-quality, detailed background "
        "settings for any image.'"
    )
    @pytest.mark.ui
    def test_subheading_text(self, bg_gen: BackgroundGeneratorPage):
        expected = (
            "From a busy street scene to an alien planet, effortlessly create "
            "high-quality, detailed background settings for any image."
        )
        actual = bg_gen.get_subheading_text()
        assert actual == expected, (
            f"Subheading text mismatch.\nExpected: '{expected}'\nActual:   '{actual}'"
        )

    @allure.title("[ui] Upload/heading content is positioned left of the hero media on desktop")
    @allure.description(
        "Verify .upload-marquee-left (mnemonic/heading/upload block) renders to the "
        "left of .upload-marquee-right (hero image) on a desktop viewport, per the "
        "ticket's 'unity block authored in page marquee left side' requirement."
    )
    @pytest.mark.ui
    def test_upload_content_left_of_media(self, bg_gen: BackgroundGeneratorPage):
        assert bg_gen.is_upload_content_left_of_media(), (
            "Expected .upload-marquee-left to be positioned left of .upload-marquee-right "
            "on a 1440x900 desktop viewport."
        )
