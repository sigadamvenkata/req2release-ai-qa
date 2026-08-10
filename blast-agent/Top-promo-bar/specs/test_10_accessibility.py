"""
Spec: Feature 10 — Accessibility
Feature file: features/10_accessibility.feature
Ticket: MWPW-203117

Accessibility scans use axe-core injected from a CDN at runtime (see
BasePage.run_axe_scan) rather than adding a new pip dependency — requires the
test browser context to have outbound network access.
"""
import allure
import pytest
from pages.promo_banner_page import PromoBannerPage
from locators.promo_locators import L


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 10: Accessibility")
class TestAccessibility:

    @allure.title("Keyboard Tab navigation reaches the banner's CTA")
    @pytest.mark.a11y
    @pytest.mark.smoke
    def test_keyboard_navigation_reaches_cta(self, promo_banner: PromoBannerPage):
        reached = promo_banner.tab_to_banner_cta(max_tabs=20)
        allure.attach(
            promo_banner.screenshot_bytes(),
            name="keyboard_focus_state",
            attachment_type=allure.attachment_type.PNG,
        )
        assert reached, (
            "Tabbing through the page (up to 20 presses) never reached the banner's primary CTA"
        )

    @allure.title("Banner passes baseline axe-core accessibility scan")
    @pytest.mark.a11y
    def test_axe_scan_no_critical_serious_violations(self, promo_banner: PromoBannerPage):
        violations = promo_banner.run_axe_scan(selector=L.BANNER)
        critical_or_serious = [
            v for v in violations if v.get("impact") in ("critical", "serious")
        ]
        allure.attach(
            str(violations),
            name="axe_violations",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert not critical_or_serious, (
            f"axe-core found {len(critical_or_serious)} Critical/Serious violation(s) "
            f"on the banner: {[v.get('id') for v in critical_or_serious]}"
        )

    @allure.title("Countdown timer does not spam assistive technology with live updates")
    @pytest.mark.a11y
    def test_countdown_not_aggressively_live_announced(self, promo_banner: PromoBannerPage):
        if not promo_banner.is_countdown_visible():
            pytest.skip("Configured promo does not include a countdown variant")
        aria_live = promo_banner.get_countdown_aria_live()
        allure.attach(
            f"aria-live='{aria_live}'",
            name="countdown_aria_live",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert aria_live != "assertive", (
            "Countdown timer uses aria-live='assertive', which will announce every "
            "tick to screen reader users — should be 'off', 'polite', or unset"
        )
