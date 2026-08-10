"""
Spec: Scenario Group 4 — Valid Format Upload via Drag-and-Drop
Ticket: MWPW-200902  |  Tags: @upload

Uses tests/assets/female.png as the designated valid test asset.
Real OS-level drag-and-drop cannot be automated; this simulates the browser's
HTML5 drop event with an in-memory DataTransfer carrying the file bytes
(see BackgroundGeneratorPage.upload_file_via_drag_and_drop).
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage

VALID_IMAGE = "female.png"


@allure.feature("Background Generator — Image Upload")
@allure.story("MWPW-200902 | Group 4: Valid Upload via Drag-and-Drop")
class TestUploadValidDragDrop:

    @allure.title("[upload] Valid image dropped onto the drop zone is accepted")
    @allure.description(
        f"Simulate dragging and dropping '{VALID_IMAGE}' onto the drop zone and "
        "verify no error message is displayed."
    )
    @pytest.mark.upload
    def test_upload_valid_image_via_drag_and_drop(self, bg_gen: BackgroundGeneratorPage):
        bg_gen.upload_file_via_drag_and_drop(VALID_IMAGE)
        allure.attach(
            bg_gen.screenshot_bytes(),
            name="after_drag_and_drop",
            attachment_type=allure.attachment_type.PNG,
        )
        assert not bg_gen.is_error_visible(), (
            f"Error shown after dropping valid image '{VALID_IMAGE}': "
            f"{bg_gen.get_error_message()}"
        )
