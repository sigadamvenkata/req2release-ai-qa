"""
Spec: Scenario Group 3 — Card Metadata
Ticket: MWPW-199796
Feature: YouTube Gallery Block — Each card has thumbnail, unique ID, label, Free tag
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery — UI")
@allure.story("MWPW-199796 | Group 3: Card Metadata")
class TestCardMetadata:

    @allure.title("[smoke][ui] Each card displays a thumbnail image")
    @allure.description(
        "Verify the first card's thumbnail (.image-wrapper img) is visible "
        "and all thumbnails have a non-empty src URL."
    )
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_thumbnail_is_visible(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="card_thumbnail_view",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_first_thumbnail_visible(), (
            "First card thumbnail (.image-wrapper img) is not visible."
        )
        srcs = gallery.get_thumbnail_srcs()
        allure.attach(
            "\n".join(srcs),
            name="thumbnail_srcs",
            attachment_type=allure.attachment_type.TEXT,
        )
        empty = [i for i, s in enumerate(srcs) if not s]
        assert not empty, (
            f"Cards at index {empty} have empty thumbnail src."
        )

    @allure.title("[ui] Each card has a unique data-template-id (unique ID)")
    @allure.description(
        "Verify every .pre-yt-card has a non-empty data-template-id attribute "
        "and all IDs are unique across the gallery."
    )
    @pytest.mark.ui
    def test_cards_have_unique_ids(self, gallery: YouTubeGalleryPage):
        ids = gallery.get_card_template_ids()
        allure.attach(
            "\n".join(ids),
            name="card_template_ids",
            attachment_type=allure.attachment_type.TEXT,
        )
        empty = [i for i, v in enumerate(ids) if not v]
        assert not empty, (
            f"Cards at index {empty} have an empty data-template-id."
        )
        assert len(ids) == len(set(ids)), (
            f"Duplicate data-template-id values found: {ids}"
        )

    @allure.title("[ui] Each card displays label text (aria-label)")
    @allure.description(
        "Verify every .pre-yt-card has a non-empty aria-label attribute "
        "which serves as the accessible label/description for the card."
    )
    @pytest.mark.ui
    def test_cards_have_label_text(self, gallery: YouTubeGalleryPage):
        labels = gallery.get_card_aria_labels()
        allure.attach(
            "\n".join(labels[:5]) + ("\n..." if len(labels) > 5 else ""),
            name="card_aria_labels_sample",
            attachment_type=allure.attachment_type.TEXT,
        )
        empty = [i for i, v in enumerate(labels) if not v]
        assert not empty, (
            f"Cards at index {empty} have an empty aria-label (label text)."
        )

    @allure.title('[ui] Each card displays a "Free" tag')
    @allure.description(
        'Verify every card has a .pre-yt-free-tag element '
        'with the exact text "Free".'
    )
    @pytest.mark.ui
    def test_cards_have_free_tag(self, gallery: YouTubeGalleryPage):
        tags = gallery.get_free_tag_texts()
        card_count = gallery.get_card_count()

        allure.attach(
            f"Cards: {card_count}, Free tags found: {len(tags)}\nValues: {tags}",
            name="free_tag_details",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert tags, "No .pre-yt-free-tag elements found on the page."
        assert len(tags) == card_count, (
            f"Expected {card_count} Free tags (one per card), found {len(tags)}."
        )
        wrong = [t for t in tags if t != "Free"]
        assert not wrong, (
            f"Some tags do not have the text 'Free'. Got: {wrong}"
        )
