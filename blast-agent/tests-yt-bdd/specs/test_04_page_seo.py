"""
Spec: Group 4 — Page Layout & SEO
Feature file: features/04_page_seo.feature
Ticket: MWPW-199796  |  Tags: @ui @seo
Known bug: MWPW-199810 — meta description missing on AEM Live staging URL
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 4: Page Layout & SEO")
class TestPageSEO:

    @allure.title("[4.1][ui][seo] Page <title> is non-empty")
    @pytest.mark.ui
    @pytest.mark.seo
    def test_page_title_non_empty(self, gallery: YouTubeGalleryPage):
        title = gallery.get_page_title()
        allure.attach(
            f"Page title: '{title}'",
            name="page_title",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert title, "Document <title> is empty."

    @allure.title("[4.2][ui][seo] Meta description is present and non-empty")
    @allure.description(
        "meta[name='description'] must exist with a non-empty content attribute. "
        "Known Bug: MWPW-199810 — this test is expected to FAIL on AEM Live staging."
    )
    @pytest.mark.ui
    @pytest.mark.seo
    @pytest.mark.xfail(reason="MWPW-199810: Meta description missing on AEM Live staging URL", strict=False)
    def test_meta_description_present(self, gallery: YouTubeGalleryPage):
        present = gallery.is_meta_desc_present()
        content = gallery.get_meta_description()
        allure.attach(
            f"meta[name='description'] present: {present}\ncontent: '{content}'",
            name="meta_description",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert present, "meta[name='description'] element is missing from the DOM."
        assert content, (
            "meta[name='description'] exists but content attribute is empty."
        )

    @allure.title("[4.3][ui] Gallery block is inside the <main> content area")
    @allure.description(
        "Verifies .prm-yt-gallery is a descendant of <main> and has "
        "a non-zero bounding box within the page scroll area."
    )
    @pytest.mark.ui
    @pytest.mark.layout
    def test_gallery_inside_main(self, gallery: YouTubeGalleryPage):
        in_main = gallery.is_gallery_in_main()
        box = gallery.get_gallery_bounding_box()
        allure.attach(
            f"In <main>: {in_main}\nBounding box: {box}",
            name="gallery_position",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert in_main, (
            ".prm-yt-gallery is not inside the <main> element — check page structure."
        )
        assert box and box["height"] > 0 and box["width"] > 0, (
            ".prm-yt-gallery bounding box is zero — gallery may not be rendered."
        )
