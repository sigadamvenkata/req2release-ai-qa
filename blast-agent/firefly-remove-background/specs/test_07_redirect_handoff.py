"""
Spec: Scenario Group 7 — Cross-App Handoff (Redirect to Firefly Product App)
Ticket: MWPW-200902  |  Tags: @redirect @integration

NOTE: firefly-stage.corp.adobe.com is a corp-internal host. These tests may
require the runner to be on Adobe's corporate network/VPN. The redirect
target/pattern is taken from the ticket text and has not yet been confirmed
against a live successful upload (see locators/bg_generator_locators.py).
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage

VALID_IMAGE = "female.png"


@allure.feature("Background Generator — Cross-App Handoff")
@allure.story("MWPW-200902 | Group 7: Redirect to Firefly Product App")
class TestRedirectHandoff:

    @allure.title("[redirect][integration] Successful upload redirects to the Firefly generate/image page")
    @allure.description(
        f"Upload '{VALID_IMAGE}', wait for processing to complete, and verify the "
        "browser navigates to https://firefly-stage.corp.adobe.com/generate/image."
    )
    @pytest.mark.redirect
    @pytest.mark.integration
    def test_upload_redirects_to_firefly_generate_image(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file(VALID_IMAGE)
        final_url = bg_gen.wait_for_firefly_redirect(timeout=60000)
        allure.attach(
            f"Final URL: {final_url}",
            name="post_upload_url",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert "firefly-stage.corp.adobe.com/generate/image" in final_url, (
            f"Expected redirect to firefly-stage.corp.adobe.com/generate/image, "
            f"landed on: {final_url}. If this fails on a non-VPN runner, confirm "
            f"network access to firefly-stage.corp.adobe.com first."
        )

    @allure.title("[redirect][integration][SKIPPED] Uploaded image is carried over to the Firefly editor")
    @allure.description(
        f"After '{VALID_IMAGE}' is uploaded and processed, verify the Firefly product "
        "page loads with the image (or a reference to it) present in its editor."
    )
    @pytest.mark.redirect
    @pytest.mark.integration
    @pytest.mark.skip(
        reason="Confirmed live 2026-07-17: using page.wait_for_load_state('networkidle') here "
               "times out — the Firefly editor SPA has continuous background network activity "
               "and never goes idle (that part is a fixed script bug, see wait_for_load_state('load') "
               "below). But even after switching to a bounded wait, a fresh unauthenticated Playwright "
               "context lands on a blank editor canvas with 0 canvas/img elements — the editor likely "
               "requires a signed-in session to render the generated result. Needs an authenticated "
               "test account and a confirmed image-presence selector before this can be un-skipped."
    )
    def test_image_carried_over_to_firefly_editor(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file(VALID_IMAGE)
        bg_gen.wait_for_firefly_redirect(timeout=60000)
        page = bg_gen.page
        page.wait_for_load_state("load", timeout=30000)
        page.wait_for_timeout(4000)
        allure.attach(
            page.screenshot(full_page=True),
            name="firefly_editor_after_redirect",
            attachment_type=allure.attachment_type.PNG,
        )
        # Exact selector for the loaded-image element on the Firefly editor is not yet
        # confirmed (out of scope of the acom page's DOM) — presence of a canvas/image
        # element is used as a best-effort signal pending confirmation.
        has_media = page.locator("canvas, img[src*='blob:'], img[src*='firefly']").count() > 0
        assert has_media, (
            "Expected an image/canvas element on the Firefly editor page after redirect, "
            "found none. Selector needs confirmation against the live Firefly editor DOM."
        )
