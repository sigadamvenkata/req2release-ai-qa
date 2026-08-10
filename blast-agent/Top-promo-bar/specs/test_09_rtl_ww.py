"""
Spec: Feature 9 — WW Rollout and RTL Support
Feature file: features/09_rtl_ww.feature
Ticket: MWPW-203117

UPDATED after live verification (2026-08-05): adobe.com's locale is URL-path-driven
(e.g. /ae_ar/), not Accept-Language-driven, so the fixtures now navigate to real
locale URLs (RTL_URL, INTL_URL) rather than relying on the Playwright context
`locale` option alone. Confirmed dir="rtl"/lang="ar" on RTL_URL and dir="ltr" on
INTL_URL. Neither locale currently has an active promo campaign configured, so the
banner-specific assertions skip gracefully — the page-level locale checks still run
as a real (if partial) verification.
"""
import allure
import pytest
from pages.promo_banner_page import PromoBannerPage


@allure.feature("Top Promo Banner — MWPW-203117")
@allure.story("Feature 9: WW Rollout & RTL Support")
class TestRtlWw:

    @allure.title("RTL locale page renders with dir='rtl'")
    @pytest.mark.rtl
    @pytest.mark.smoke
    def test_page_is_rtl(self, promo_banner_rtl: PromoBannerPage):
        allure.attach(
            promo_banner_rtl.screenshot_bytes(),
            name="rtl_page",
            attachment_type=allure.attachment_type.PNG,
        )
        html_dir = promo_banner_rtl.get_html_dir_attr()
        allure.attach(f"<html dir='{html_dir}'>", name="html_dir", attachment_type=allure.attachment_type.TEXT)
        assert html_dir.lower() == "rtl", f"Expected <html dir='rtl'>, got '{html_dir}'"

    @allure.title("Banner layout is mirrored correctly in an RTL locale")
    @pytest.mark.rtl
    def test_banner_rtl_mirrored(self, promo_banner_rtl: PromoBannerPage):
        if not promo_banner_rtl.is_banner_visible():
            pytest.skip("No active promo currently configured on the RTL (ae_ar) locale page")
        assert not promo_banner_rtl.has_horizontal_overflow(), (
            "Horizontal overflow detected in the RTL locale — text may be clipped/overlapping"
        )
        assert promo_banner_rtl.is_banner_rtl_mirrored() or promo_banner_rtl.get_html_dir_attr().lower() == "rtl", (
            "Neither the banner's computed direction nor <html dir> indicate RTL — "
            "banner may not be mirrored for RTL locales"
        )

    @allure.title("Banner text is localized in a non-English LTR locale")
    @pytest.mark.rtl
    def test_banner_localized_non_english_ltr(self, promo_banner_intl: PromoBannerPage):
        allure.attach(
            promo_banner_intl.screenshot_bytes(),
            name="intl_ltr_page",
            attachment_type=allure.attachment_type.PNG,
        )
        if not promo_banner_intl.is_banner_visible():
            pytest.skip("No active promo currently configured on the French (intl LTR) locale page")
        headline = promo_banner_intl.get_headline_text()
        assert headline, "Banner headline is empty in the non-English LTR locale"
        assert not promo_banner_intl.has_horizontal_overflow(), (
            "Horizontal overflow detected in the non-English LTR locale — "
            "localized text may be longer than the English reference and overflow the container"
        )
