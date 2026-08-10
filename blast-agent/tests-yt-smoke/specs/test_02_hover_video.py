"""
Spec: Scenario Group 4 — Hover Behaviour (Video Playback)
Ticket: MWPW-199796  |  Tags: @smoke @functional
"""
import pytest
import allure
from pages.yt_gallery_page import YouTubeGalleryPage


@allure.feature("YouTube Gallery — Smoke")
@allure.story("MWPW-199796 | Group 4: Hover → Video Playback")
class TestHoverVideo:

    @allure.title("[smoke][functional] Hovering over a card starts inline video playback")
    @allure.description(
        "Verify that hovering over the first .pre-yt-card causes its video element "
        "to transition from paused to playing. "
        "Note: locale modal is dismissed before hover to unblock pointer events. "
        "Chromium is launched with --autoplay-policy=no-user-gesture-required."
    )
    @pytest.mark.smoke
    @pytest.mark.functional
    def test_hover_plays_video(self, gallery: YouTubeGalleryPage):
        # Confirm video is initially paused
        playing_before = gallery.is_first_card_video_playing()
        allure.attach(
            f"Video playing before hover: {playing_before}",
            name="video_state_before_hover",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert not playing_before, (
            "Video was already playing before hover — expected paused initial state."
        )

        # Hover and check
        gallery.hover_first_card()
        allure.attach(
            gallery.screenshot_bytes(),
            name="after_hover",
            attachment_type=allure.attachment_type.PNG,
        )
        playing_after = gallery.is_first_card_video_playing()
        allure.attach(
            f"Video playing after hover: {playing_after}",
            name="video_state_after_hover",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert playing_after, (
            "Video did not start playing after hovering over the card. "
            "Expected video.paused == False."
        )
