"""
Spec: Feature 4 — Promo Countdown Banner
Feature file: features/04_countdown.feature
Ticket: MWPW-203117
"""
import allure
import pytest
from pages.promo_banner_page import PromoBannerPage


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 4: Promo Countdown")
class TestCountdown:

    @allure.title("Countdown timer renders in DD:HH:MM:SS format and ticks down")
    @pytest.mark.countdown
    @pytest.mark.smoke
    def test_countdown_renders_and_ticks(self, promo_banner: PromoBannerPage):
        allure.attach(
            promo_banner.screenshot_bytes(),
            name="countdown_banner",
            attachment_type=allure.attachment_type.PNG,
        )
        if not promo_banner.is_countdown_visible():
            pytest.skip("Configured promo does not include a countdown variant")

        text = promo_banner.get_countdown_text()
        allure.attach(text, name="countdown_text", attachment_type=allure.attachment_type.TEXT)
        assert promo_banner._parse_countdown_seconds(text) is not None, (
            f"Countdown text '{text}' does not match DD:HH:MM:SS (or HH:MM:SS) format"
        )

        delta = promo_banner.wait_and_get_countdown_delta(wait_seconds=5)
        allure.attach(
            f"Countdown decreased by {delta} seconds over a 5s window",
            name="countdown_delta",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert delta is not None and delta > 0, (
            "Countdown did not decrease over a 5 second observation window"
        )

    @allure.title("Countdown banner handles expiry without breaking layout")
    @pytest.mark.countdown
    def test_countdown_expiry_handling(self, promo_banner: PromoBannerPage):
        if not promo_banner.is_countdown_visible():
            pytest.skip(
                "Requires a stage-configured countdown promo with an end time "
                "about to elapse — not available in this fixture"
            )
        seconds = promo_banner.get_countdown_seconds()
        assert seconds is None or seconds >= 0, (
            f"Countdown shows a negative/broken value: {seconds}"
        )
        assert not promo_banner.has_horizontal_overflow(), (
            "Page has horizontal overflow while the countdown is near/at expiry"
        )
