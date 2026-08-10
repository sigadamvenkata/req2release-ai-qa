"""
Spec: Group 3 — Card Metadata
Feature file: features/03_card_metadata.feature
Ticket: MWPW-199796  |  Tags: @ui @metadata
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 3: Card Metadata — ID, Label, Free Tag, Thumbnail, Alt")
class TestCardMetadata:

    @allure.title("[3.1][ui] Each card has a unique identifier")
    @allure.description(
        "Reads id or data-id from every .pre-yt-card and verifies no duplicates."
    )
    @pytest.mark.ui
    @pytest.mark.metadata
    def test_unique_card_identifiers(self, gallery: YouTubeGalleryPage):
        ids = gallery.get_card_identifiers()
        allure.attach(
            f"Card identifiers: {ids}",
            name="card_ids",
            attachment_type=allure.attachment_type.TEXT,
        )
        non_null = [i for i in ids if i]
        if non_null:
            assert len(non_null) == len(set(non_null)), (
                f"Duplicate card identifiers detected: {non_null}"
            )

    @allure.title("[3.2][ui] Each card displays a non-empty label text")
    @pytest.mark.ui
    @pytest.mark.metadata
    def test_card_labels_non_empty(self, gallery: YouTubeGalleryPage):
        labels = gallery.get_card_labels()
        allure.attach(
            f"Card labels: {labels}",
            name="card_labels",
            attachment_type=allure.attachment_type.TEXT,
        )
        if labels:
            empty = [i for i, lbl in enumerate(labels) if not lbl]
            assert not empty, (
                f"Cards at index {empty} have empty label text."
            )

    @allure.title("[3.3][ui] At least one card has a Free tag (.pre-yt-free-tag)")
    @pytest.mark.ui
    @pytest.mark.metadata
    def test_free_tag_present(self, gallery: YouTubeGalleryPage):
        count = gallery.get_free_tag_count()
        allure.attach(
            f"Free tag count: {count}",
            name="free_tag_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count >= 1, (
            f"Expected at least 1 .pre-yt-free-tag, found {count}."
        )

    @allure.title("[3.4][ui] Each card thumbnail has a non-empty src and is visible")
    @pytest.mark.ui
    @pytest.mark.metadata
    def test_thumbnail_src_and_visibility(self, gallery: YouTubeGalleryPage):
        srcs = gallery.get_thumbnail_srcs()
        allure.attach(
            f"Thumbnail srcs: {srcs}",
            name="thumbnail_srcs",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            gallery.screenshot_bytes(),
            name="thumbnails_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        assert srcs, "No thumbnail images (.image-wrapper img) found in cards."
        empty_srcs = [i for i, s in enumerate(srcs) if not s]
        assert not empty_srcs, (
            f"Cards at index {empty_srcs} have empty thumbnail src."
        )
        assert gallery.is_first_thumbnail_visible(), (
            "First card thumbnail is not visible in the viewport."
        )

    @allure.title("[3.5][ui][a11y] Card thumbnails have valid alt attributes")
    @allure.description(
        "Alt text must not be None for accessibility (WCAG 1.1.1). "
        "Empty string is acceptable for decorative images but None is not."
    )
    @pytest.mark.ui
    @pytest.mark.metadata
    @pytest.mark.a11y
    def test_thumbnail_alt_attributes(self, gallery: YouTubeGalleryPage):
        alts = gallery.get_thumbnail_alts()
        allure.attach(
            f"Alt attributes: {alts}",
            name="thumbnail_alts",
            attachment_type=allure.attachment_type.TEXT,
        )
        null_alts = [i for i, a in enumerate(alts) if a is None]
        assert not null_alts, (
            f"Cards at index {null_alts} are missing the alt attribute entirely "
            f"(alt=None). This breaks accessibility."
        )
