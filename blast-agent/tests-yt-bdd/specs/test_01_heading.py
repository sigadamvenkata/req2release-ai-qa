"""
Spec: Group 1 — Heading Validity
Feature file: features/01_heading.feature
Ticket: MWPW-199796  |  Tags: @ui @heading
Known bug: MWPW-199809, MWPW-199812 — locale modal may block heading
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 1: Heading Validity")
class TestHeadingValidity:

    @allure.title("[1.1][ui] Gallery heading is visible on page load")
    @allure.description(
        "After dismissing the locale modal, h2.heading-xl must be visible. "
        "Known bug: MWPW-199809 / MWPW-199812 — modal may intermittently block."
    )
    @pytest.mark.ui
    @pytest.mark.heading
    def test_heading_visible(self, gallery: YouTubeGalleryPage):
        allure.attach(
            gallery.screenshot_bytes(),
            name="heading_visible_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        assert gallery.is_heading_visible(), (
            "Gallery heading (h2.heading-xl) is not visible. "
            "Check if locale modal is still blocking the element. "
            "Bug: MWPW-199809 / MWPW-199812"
        )

    @allure.title("[1.2][ui] Gallery heading contains non-empty meaningful text")
    @allure.description(
        "The h2.heading-xl must have non-empty text content."
    )
    @pytest.mark.ui
    @pytest.mark.heading
    def test_heading_text_non_empty(self, gallery: YouTubeGalleryPage):
        text = gallery.get_heading_text()
        allure.attach(
            f"Heading text: '{text}'",
            name="heading_text",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert text, "Gallery heading text is empty — h2.heading-xl has no text content."
        assert len(text) >= 3, f"Heading text is suspiciously short: '{text}'"

    @allure.title("[1.3][ui] Exactly one H2 heading inside the gallery block")
    @allure.description(
        "Only one h2 should exist inside .prm-yt-gallery."
    )
    @pytest.mark.ui
    @pytest.mark.heading
    def test_single_h2_in_gallery(self, gallery: YouTubeGalleryPage):
        count = gallery.count_h2_in_gallery()
        allure.attach(
            f"H2 count inside .prm-yt-gallery: {count}",
            name="h2_count",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert count == 1, (
            f"Expected exactly 1 H2 inside .prm-yt-gallery, found {count}."
        )
