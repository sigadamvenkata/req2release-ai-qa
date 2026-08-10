"""
Spec: Scenario Group 12 — Baseline Accessibility
Ticket: MWPW-200902  |  Tags: @a11y
"""
import pytest
import allure
from pages.background_generator_page import BackgroundGeneratorPage


@allure.feature("Background Generator — Accessibility")
@allure.story("MWPW-200902 | Group 12: Baseline Accessibility")
class TestAccessibility:

    @allure.title("[a11y] Hero image has an alt attribute")
    @allure.description(
        "Verify the marquee hero image has an 'alt' attribute (may legitimately be "
        "empty/decorative, but must be present)."
    )
    @pytest.mark.a11y
    def test_hero_image_has_alt_attribute(self, bg_gen: BackgroundGeneratorPage):
        alt = bg_gen.get_hero_image_alt()
        assert alt is not None, (
            "Marquee hero image is missing an 'alt' attribute entirely."
        )

    @allure.title("[a11y] Heading hierarchy contains exactly one H1")
    @allure.description(
        "Verify there is exactly one <h1> element on the page (heading levels "
        "should not be skipped)."
    )
    @pytest.mark.a11y
    def test_single_h1(self, bg_gen: BackgroundGeneratorPage):
        headings = bg_gen.get_all_heading_levels()
        allure.attach(
            str(headings), name="heading_hierarchy", attachment_type=allure.attachment_type.TEXT
        )
        h1_count = sum(1 for tag, _ in headings if tag == "h1")
        assert h1_count == 1, f"Expected exactly one <h1>, found {h1_count}. Headings: {headings}"

    @allure.title("[a11y] Upload CTA is reachable and focusable via keyboard")
    @allure.description(
        "Tab through the page and verify the 'Upload your image' CTA receives "
        "visible keyboard focus."
    )
    @pytest.mark.a11y
    def test_upload_cta_keyboard_focusable(self, bg_gen: BackgroundGeneratorPage):
        focused = bg_gen.focus_upload_cta_via_tab(max_tabs=30)
        assert focused, (
            "Upload CTA never received keyboard focus within 30 Tab presses."
        )
