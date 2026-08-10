"""
Spec: Scenario Group 6 — Upload Progress ("Splash") UI
Ticket: MWPW-200902  |  Tags: @upload

Splash screen structure confirmed from live rendered DOM (2026-07-17):
  .splash-loader (role="dialog", aria-modal="true", display:none until triggered)
    h2 "Adobe Firefly"
    body-m "One moment as we take you to Firefly"
    body-m "[[progress-bar]] Loading % Completed" (token populated at runtime)
    Cancel CTA -> "#_cancel"
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage

VALID_IMAGE = "female.png"


@allure.feature("Background Generator — Upload Progress")
@allure.story("MWPW-200902 | Group 6: Splash/Progress Indicator")
class TestProgressSplash:

    @allure.title("[upload] Splash/progress screen appears after selecting a valid image")
    @allure.description(
        f"Upload '{VALID_IMAGE}' and verify the .splash-loader dialog becomes "
        "visible within 5 seconds, displaying the 'Adobe Firefly' heading and the "
        "'One moment as we take you to Firefly' message."
    )
    @pytest.mark.upload
    def test_splash_appears_after_upload(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file(VALID_IMAGE)
        bg_gen.wait_for_splash_visible(timeout=5000)
        allure.attach(
            bg_gen.screenshot_bytes(),
            name="splash_visible",
            attachment_type=allure.attachment_type.PNG,
        )
        assert bg_gen.is_splash_visible(), (
            "Splash/progress screen (.splash-loader) did not become visible after upload."
        )
        message = bg_gen.get_splash_message()
        assert "Firefly" in message, (
            f"Expected splash message to reference Firefly, got: '{message}'"
        )

    @allure.title("[upload] Splash/progress screen is dismissed once processing completes")
    @allure.description(
        f"Upload '{VALID_IMAGE}' and verify the .splash-loader dialog is no longer "
        "visible once upload processing finishes (or the page navigates away)."
    )
    @pytest.mark.upload
    def test_splash_dismissed_after_processing(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file(VALID_IMAGE)
        bg_gen.wait_for_splash_visible(timeout=5000)
        bg_gen.wait_for_splash_hidden(timeout=60000)
        assert not bg_gen.is_splash_visible(), (
            "Splash/progress screen (.splash-loader) is still visible after processing "
            "should have completed."
        )
