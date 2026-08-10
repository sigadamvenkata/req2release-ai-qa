"""
Spec: Accordion / FAQ Block Tests
Ticket: MWPW-199605
Feature: Accordion block — 'How to remove a background with Adobe Firefly'
"""
import pytest
import allure
from tests.pages.remove_bg_page import RemoveBgPage


@allure.feature("Accordion Block")
@allure.story("MWPW-199605 — FAQ and How-To Accordion")
class TestAccordion:

    @allure.title("H2 heading 'How to remove a background with Adobe Firefly' is on the page")
    @pytest.mark.accordion
    @pytest.mark.smoke
    def test_how_to_h2_present(self, remove_bg: RemoveBgPage):
        h2 = remove_bg.get_how_to_h2_text()
        assert h2, (
            "H2 heading containing 'How to remove a background with Adobe Firefly' not found"
        )
        assert "how to remove" in h2.lower(), f"H2 text unexpected: {h2}"

    @allure.title("At least one accordion item is present on the page")
    @pytest.mark.accordion
    def test_accordion_items_present(self, remove_bg: RemoveBgPage):
        count = remove_bg.get_accordion_count()
        assert count > 0, "No accordion trigger buttons found on the page"

    @allure.title("First accordion item expands when clicked")
    @pytest.mark.accordion
    def test_first_accordion_expands(self, remove_bg: RemoveBgPage):
        remove_bg.click_accordion_item(index=0)
        # Wait up to 5s for aria-expanded to become "true"
        remove_bg.page.wait_for_function(
            "() => {"
            " const b = document.querySelector('button.accordion-trigger');"
            " return b && b.getAttribute('aria-expanded') === 'true';"
            "}",
            timeout=5000,
        )
        assert remove_bg.is_accordion_expanded(index=0), (
            "First accordion item did not expand after clicking its trigger"
        )

    @allure.title("First accordion item collapses when clicked a second time")
    @pytest.mark.accordion
    def test_first_accordion_collapses(self, remove_bg: RemoveBgPage):
        remove_bg.click_accordion_item(index=0)   # expand
        remove_bg.page.wait_for_function(
            "() => {"
            " const b = document.querySelector('button.accordion-trigger');"
            " return b && b.getAttribute('aria-expanded') === 'true';"
            "}",
            timeout=5000,
        )
        remove_bg.click_accordion_item(index=0)   # collapse
        assert not remove_bg.is_accordion_expanded(index=0), (
            "First accordion item did not collapse after clicking its trigger a second time"
        )

    @allure.title("'What file formats does the Adobe Firefly background remover support' FAQ is present")
    @pytest.mark.accordion
    def test_file_formats_faq_present(self, remove_bg: RemoveBgPage):
        count = remove_bg.page.locator(
            "button.accordion-trigger:has-text('file format')"
        ).count()
        assert count > 0, "File formats FAQ accordion item not found"

    @allure.title("'Is the Adobe Firefly background remover free' FAQ is present")
    @pytest.mark.accordion
    def test_is_free_faq_present(self, remove_bg: RemoveBgPage):
        count = remove_bg.page.locator(
            "button.accordion-trigger:has-text('free')"
        ).count()
        assert count > 0, "Free/pricing FAQ accordion item not found"
