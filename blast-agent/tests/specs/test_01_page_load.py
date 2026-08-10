"""
Spec: Page Load & SEO Tests
Ticket: MWPW-199605
Feature: Firefly Remove Background SEO Page — Page Load & SEO
"""
import pytest
import allure
from tests.pages.remove_bg_page import RemoveBgPage


@allure.feature("Page Load & SEO")
@allure.story("MWPW-199605 — Remove Background SEO Page")
class TestPageLoad:

    @allure.title("Page title contains 'Remove Background' and 'Firefly'")
    @pytest.mark.seo
    @pytest.mark.smoke
    def test_page_title_contains_remove_background(self, remove_bg: RemoveBgPage):
        title = remove_bg.get_page_title()
        assert "Remove" in title or "remove" in title, f"Expected 'Remove' in title, got: {title}"
        assert "Firefly" in title or "firefly" in title, f"Expected 'Firefly' in title, got: {title}"

    @allure.title("Meta description is present and non-empty")
    @pytest.mark.seo
    def test_meta_description_present(self, remove_bg: RemoveBgPage):
        meta = remove_bg.get_meta_description()
        assert meta, "Meta description tag is missing or empty"
        assert len(meta) > 20, f"Meta description too short: '{meta}'"

    @allure.title("Canonical URL tag is present")
    @pytest.mark.seo
    def test_canonical_url_present(self, remove_bg: RemoveBgPage):
        canonical = remove_bg.get_canonical_url()
        assert canonical, "Canonical URL tag is missing"
        assert "adobe.com" in canonical, f"Canonical URL unexpected: {canonical}"

    @allure.title("H1 heading is visible and contains 'remove' and 'background'")
    @pytest.mark.seo
    @pytest.mark.smoke
    def test_h1_is_visible_and_correct(self, remove_bg: RemoveBgPage):
        assert remove_bg.is_h1_visible(), "H1 heading is not visible on the page"
        h1 = remove_bg.get_h1_text().lower()
        assert "remove" in h1, f"H1 does not mention 'remove': {h1}"
        assert "background" in h1, f"H1 does not mention 'background': {h1}"

    @allure.title("'How to remove a background with Adobe Firefly' H2 is present")
    @pytest.mark.seo
    def test_how_to_h2_present(self, remove_bg: RemoveBgPage):
        h2 = remove_bg.get_how_to_h2_text()
        assert h2, "H2 'How to remove a background with Adobe Firefly' not found on page"
        assert "how to remove" in h2.lower(), f"H2 text unexpected: {h2}"
