"""
Spec: Global Navigation Tests
Ticket: MWPW-199605
Feature: Global Navigation — Login CTA and Firefly CTA
"""
import pytest
import allure
from tests.pages.nav_page import NavPage
from tests.pages.remove_bg_page import RemoveBgPage


@allure.feature("Global Navigation")
@allure.story("MWPW-199605 — Login CTA and Firefly Navigation CTA")
class TestNavigation:

    @allure.title("Sign In button is visible in the navigation (logged-out state)")
    @pytest.mark.navigation
    @pytest.mark.smoke
    def test_sign_in_button_is_visible(self, nav: NavPage):
        assert nav.is_sign_in_visible(), (
            "Sign In button not found in Global Navigation. "
            "Expected: button.profile-comp.secondary-button"
        )

    @allure.title("Sign In button label is 'Sign in'")
    @pytest.mark.navigation
    def test_sign_in_button_label(self, nav: NavPage):
        text = nav.get_sign_in_text()
        assert text.lower() == "sign in", (
            f"Sign In button text expected 'Sign in', got: '{text}'"
        )

    @allure.title("Clicking Sign In navigates to Adobe login page [headless limitation]")
    @pytest.mark.navigation
    @pytest.mark.xfail(
        reason=(
            "UNAV JS click handler fires but IMS navigation does not trigger in "
            "headless browsers. Use --headed or a real browser session to verify."
        ),
        strict=False,
    )
    def test_sign_in_navigates_to_login(self, nav: NavPage):
        nav.click_sign_in()
        current_url = nav.get_current_url().lower()
        assert any(kw in current_url for kw in ["adobeid", "account.adobe.com", "auth", "ims"]), (
            f"Expected login URL after clicking Sign In, got: {nav.get_current_url()}"
        )

    @allure.title("Firefly navigation CTA is visible in the nav bar")
    @pytest.mark.navigation
    @pytest.mark.smoke
    def test_firefly_cta_is_visible(self, nav: NavPage):
        assert nav.is_firefly_cta_visible(), (
            "Firefly 'Go to Firefly' CTA not found in Global Navigation."
        )

    @allure.title("Firefly CTA href links to a Firefly destination")
    @pytest.mark.navigation
    def test_firefly_cta_href(self, nav: NavPage):
        href = nav.get_firefly_cta_href().lower()
        assert href, "Firefly CTA has no href attribute"
        assert "firefly" in href, (
            f"Firefly CTA href does not contain 'firefly': {href}"
        )

    @allure.title("Logged-in state: Sign In replaced by profile icon [SKIPPED — needs auth]")
    @pytest.mark.navigation
    @pytest.mark.skip_auth
    @pytest.mark.skip(reason="Requires Adobe account credentials — marked pending")
    def test_sign_in_hidden_when_logged_in(self, nav: NavPage):
        # This test requires: 1) sign-in flow, 2) Adobe test account
        pass
