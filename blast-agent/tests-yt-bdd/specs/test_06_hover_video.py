"""
Spec: Group 6 — Hover-to-Play Video
Feature file: features/06_hover_video.feature
Ticket: MWPW-199796  |  Tags: @smoke @functional

Chromium is launched with --autoplay-policy=no-user-gesture-required
so the video can play without a click gesture in headless mode.
"""
import allure
import pytest
from pages.gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 6: Hover-to-Play Video")
class TestHoverVideo:

    @allure.title("[6.1][smoke] Video becomes visible and has a src after hover")
    @allure.description(
        "Mouse hover over the first .pre-yt-card should make the "
        ".video-wrapper video element visible and populate its src."
    )
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_hover_shows_video(self, gallery: YouTubeGalleryPage):
        gallery.hover_first_card()

        allure.attach(
            gallery.screenshot_bytes(),
            name="after_hover_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

        visible = gallery.is_video_visible_in_first_card()
        src = gallery.get_video_src_in_first_card()
        allure.attach(
            f"Video visible: {visible}\nVideo src: '{src}'",
            name="video_state_after_hover",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert visible, (
            ".video-wrapper video is not visible after hovering over the first card."
        )
        assert src, (
            "Video element is visible but src attribute is empty after hover."
        )

    @allure.title("[6.2][smoke] Video is hidden before any hover action")
    @allure.description(
        "Before mouse hover, the video element inside the first card "
        "should not be visible (display:none or hidden by CSS)."
    )
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_video_hidden_before_hover(self, gallery_no_hover: YouTubeGalleryPage):
        allure.attach(
            gallery_no_hover.screenshot_bytes(),
            name="before_hover_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
        hidden = gallery_no_hover.is_video_hidden_before_hover()
        allure.attach(
            f"Video hidden before hover: {hidden}",
            name="video_hidden_state",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert hidden, (
            "Video is already visible before any hover — expected hidden state."
        )
