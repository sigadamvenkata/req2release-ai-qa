"""
Spec: Group 2 — Grid & Card Layout
Feature file: features/02_grid_layout.feature
Ticket: MWPW-199796  |  Tags: @ui @layout
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 2: Grid & Card Layout")
class TestGridLayout:

    @allure.title("[2.1][ui] Gallery grid container (.pre-yt-grid) is visible")
    @pytest.mark.ui
    @pytest.mark.layout
    def test_grid_visible(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="grid_visible",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_grid_visible(), (
            "Grid container (.pre-yt-grid) is not visible on the page."
        )

    @allure.title("[2.2][ui] Gallery contains at least one card")
    @pytest.mark.ui
    @pytest.mark.layout
    def test_at_least_one_card(self, gallery: YouTubeGalleryPage):
        count = gallery.get_card_count()
        allure.attach(
            f"Card count: {count}",
            name="card_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, (
            f"Expected at least 1 .pre-yt-card in the gallery, found {count}."
        )

    @allure.title("[2.3][ui] Grid display property is 'grid' or 'flex'")
    @allure.description(
        "The CSS display of .pre-yt-grid must be a grid or flex layout. "
        "This confirms the grid is rendered as a grid, not block/inline."
    )
    @pytest.mark.ui
    @pytest.mark.layout
    def test_grid_display_property(self, gallery: YouTubeGalleryPage):
        display = gallery.get_grid_display_property()
        allure.attach(
            f"CSS display of .pre-yt-grid: '{display}'",
            name="grid_display",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert "grid" in display or "flex" in display, (
            f"Expected display:grid or display:flex on .pre-yt-grid, got: '{display}'"
        )

    @allure.title("[2.4][ui] Each card has a non-zero width and height")
    @allure.description(
        "All .pre-yt-card elements must have a non-zero bounding box, "
        "confirming they are rendered and visible on screen."
    )
    @pytest.mark.ui
    @pytest.mark.layout
    def test_card_bounding_boxes(self, gallery: YouTubeGalleryPage):
        boxes = gallery.get_card_bounding_boxes()
        allure.attach(
            f"Card bounding boxes: {boxes}",
            name="card_bounding_boxes",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert boxes, "No card bounding boxes found — cards may not be rendered."
        for i, box in enumerate(boxes):
            assert box["width"] > 0, f"Card {i} has zero width."
            assert box["height"] > 0, f"Card {i} has zero height."

        widths = [b["width"] for b in boxes]
        if len(widths) > 1:
            spread = max(widths) - min(widths)
            assert spread <= 5, (
                f"Card widths are inconsistent: min={min(widths)}, max={max(widths)} "
                f"(spread={spread}px, tolerance=5px)"
            )
