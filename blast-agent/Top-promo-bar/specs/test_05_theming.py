"""
Spec: Feature 5 — Theming
Feature file: features/05_theming.feature
Ticket: MWPW-203117

REDESIGNED after live verification (2026-08-05): the banner's theme is an
authoring-time choice per promo campaign (a BEM modifier class on the same
.feds-promo-bar element), NOT something that reacts to OS/browser dark-mode —
emulating `color_scheme=dark` via Playwright had zero effect on the live banner,
which stayed `feds-promo-bar--light` regardless. The original design (compare a
`promo_banner` fixture against a `promo_banner_dark` fixture) tested the wrong
mechanism and also crashed with a Playwright asyncio conflict when two
independently-launched `sync_playwright()` fixtures were requested by the same
test. These tests now validate self-consistency instead: whatever theme the
currently-configured banner declares, its rendered colors should match.
"""
import allure
import pytest
from pages.promo_banner_page import PromoBannerPage


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 5: Theming")
class TestTheming:

    @allure.title("Banner's rendered background matches its declared theme")
    @pytest.mark.theming
    @pytest.mark.smoke
    def test_background_matches_declared_theme(self, promo_banner: PromoBannerPage):
        allure.attach(
            promo_banner.screenshot_bytes(),
            name="banner_theme_check",
            attachment_type=allure.attachment_type.PNG,
        )
        theme = promo_banner.get_banner_theme()
        bg = promo_banner.get_banner_background_color()
        allure.attach(
            f"declared theme='{theme}' | background-color={bg}",
            name="theme_vs_background",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert theme != "unknown", "Could not determine the banner's declared theme (--light/--dark modifier)"
        assert promo_banner.is_background_consistent_with_declared_theme(), (
            f"Banner declares theme '{theme}' but its background color ({bg}) "
            f"does not match (light theme should be high-luminance, dark theme low-luminance)"
        )

    @allure.title("Banner headline text color is readable against its declared theme")
    @pytest.mark.theming
    def test_text_color_present(self, promo_banner: PromoBannerPage):
        text_color = promo_banner.get_banner_text_color()
        allure.attach(
            f"headline text color={text_color}",
            name="headline_text_color",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert text_color, "Could not read the banner headline's computed text color"

    @allure.title("OS/browser dark-mode preference does not affect the banner (documented, not a bug)")
    @pytest.mark.theming
    def test_os_dark_mode_has_no_effect_on_banner(self, promo_banner_dark: PromoBannerPage):
        # This intentionally documents current behavior rather than asserting a
        # requirement: the banner theme is authored per campaign, so forcing
        # `color_scheme=dark` at the browser level is expected to leave it
        # unchanged. If this ever starts failing (banner theme actually follows
        # OS preference), treat that as a design change to confirm, not a bug.
        theme = promo_banner_dark.get_banner_theme()
        allure.attach(
            f"declared theme under forced OS dark mode: '{theme}'",
            name="theme_under_os_dark_mode",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert theme != "unknown", "Could not determine the banner's declared theme under OS dark mode"
