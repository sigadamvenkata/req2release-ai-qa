"""
Spec: Scenario Group 8 — Page-Level Layout
Ticket: MWPW-199796
Feature: YouTube Gallery Block — No overflow on desktop, meta description present
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery — UI")
@allure.story("MWPW-199796 | Group 8: Page-Level Layout")
class TestPageLayout:

    @allure.title("[ui] Page renders without horizontal overflow on 1440x900 desktop")
    @allure.description(
        "Verify document.body.scrollWidth does not exceed window.innerWidth "
        "at the 1440x900 desktop viewport (no horizontal scrollbar)."
    )
    @pytest.mark.ui
    def test_no_horizontal_overflow(self, gallery: YouTubeGalleryPage):
        scroll_w = gallery.page.evaluate("document.body.scrollWidth")
        inner_w  = gallery.page.evaluate("window.innerWidth")

        allure.attach(
            f"scrollWidth={scroll_w}  innerWidth={inner_w}",
            name="scroll_dimensions",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            gallery.screenshot_bytes(),
            name="full_page_layout",
            attachment_type=allure.attachment_type.PNG,
        )
        assert scroll_w <= inner_w, (
            f"Horizontal overflow detected: scrollWidth={scroll_w} > innerWidth={inner_w}."
        )

    @allure.title("[ui] Page has a non-empty meta description")
    @allure.description(
        "Verify the <meta name='description'> tag is present "
        "and its content attribute is not empty."
    )
    @pytest.mark.ui
    def test_meta_description_present_and_non_empty(self, gallery: YouTubeGalleryPage):
        meta = gallery.get_meta_description()
        allure.attach(
            f"meta description: '{meta}'",
            name="meta_description",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert meta, "Meta description tag is missing or has empty content."
        assert len(meta) > 10, (
            f"Meta description is too short to be meaningful: '{meta}'"
        )
