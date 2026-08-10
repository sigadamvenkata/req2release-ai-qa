"""
Spec: Scenario Group 11 — Stock API Integration
Ticket: MWPW-200902  |  Tags: @integration

IMPORTANT — endpoint not yet confirmed:
No request to any "stock-api" host was observed during a plain page load
(read-only discovery, 2026-07-17). Unlike the YouTube Gallery block
(MWPW-199796), this block's Stock API call — if any — appears to be tied to
the upload/processing action rather than page load, and may in fact happen on
the Firefly product app after redirect rather than on this acom page at all.
STOCK_API_STAGE / STOCK_API_PROD in locators/bg_generator_locators.py are
carried over from the YT Gallery suite's convention as a placeholder pattern
and MUST be confirmed with dev before these assertions are trusted.
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.background_generator_page import BackgroundGeneratorPage
from locators.bg_generator_locators import PAGE_URL, STOCK_API_STAGE, STOCK_API_PROD

VALID_IMAGE = "female.png"


@allure.feature("Background Generator — Stock API")
@allure.story("MWPW-200902 | Group 11: Stock API Integration")
class TestStockAPI:

    @allure.title("[integration][SKIPPED] Stock API is called during upload processing on stage")
    @allure.description(
        "Intercept all network requests during and after the upload flow and "
        f"verify at least one request is made to the stage Stock API endpoint "
        f"({STOCK_API_STAGE})."
    )
    @pytest.mark.integration
    @pytest.mark.skip(
        reason="Stock API endpoint/trigger for this block is unconfirmed — no call was "
               "observed on plain page load, and it may occur on the Firefly product page "
               "post-redirect rather than on this acom page. Confirm with dev, update "
               "STOCK_API_STAGE/PROD in locators/bg_generator_locators.py, then enable."
    )
    def test_stock_api_called_during_upload(self, page_raw: Page):
        captured_requests = []
        page_raw.on(
            "request",
            lambda r: captured_requests.append(r.url)
            if STOCK_API_STAGE in r.url or STOCK_API_PROD in r.url
            else None,
        )

        bg_gen = BackgroundGeneratorPage(page_raw)
        bg_gen.open()
        bg_gen.upload_file(VALID_IMAGE)
        bg_gen.wait_for_firefly_redirect(timeout=60000)
        page_raw.wait_for_timeout(3000)

        allure.attach(
            "\n".join(captured_requests) if captured_requests else "(none captured)",
            name="stock_api_requests",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert captured_requests, (
            f"No Stock API request detected during the upload flow. "
            f"Expected a request to: {STOCK_API_STAGE} or {STOCK_API_PROD}"
        )

    @allure.title("[integration][SKIPPED] Stock API returns a 2xx response on stage")
    @pytest.mark.integration
    @pytest.mark.skip(reason="Depends on confirmed Stock API endpoint — see test above")
    def test_stock_api_returns_2xx(self, page_raw: Page):
        captured_responses = {}
        page_raw.on(
            "response",
            lambda r: captured_responses.update({r.url: r.status})
            if STOCK_API_STAGE in r.url or STOCK_API_PROD in r.url
            else None,
        )

        bg_gen = BackgroundGeneratorPage(page_raw)
        bg_gen.open()
        bg_gen.upload_file(VALID_IMAGE)
        bg_gen.wait_for_firefly_redirect(timeout=60000)
        page_raw.wait_for_timeout(3000)

        failed = {url: status for url, status in captured_responses.items() if not (200 <= status < 300)}
        assert not failed, f"Stock API returned non-2xx response(s): {failed}"

    @allure.title("[integration][SKIPPED] Stage page calls the stage Stock API endpoint only")
    @pytest.mark.integration
    @pytest.mark.skip(reason="Depends on confirmed Stock API endpoint — see first test in this file")
    def test_stage_calls_stage_endpoint_only(self, page_raw: Page):
        stage_hits, prod_hits = [], []
        page_raw.on(
            "request",
            lambda r: stage_hits.append(r.url) if STOCK_API_STAGE in r.url
            else prod_hits.append(r.url) if STOCK_API_PROD in r.url
            else None,
        )

        bg_gen = BackgroundGeneratorPage(page_raw)
        bg_gen.open()
        bg_gen.upload_file(VALID_IMAGE)
        bg_gen.wait_for_firefly_redirect(timeout=60000)
        page_raw.wait_for_timeout(3000)

        allure.attach(
            f"Stage hits : {stage_hits}\nProd hits  : {prod_hits}",
            name="endpoint_routing",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert stage_hits, f"Expected at least one request to stage Stock API ({STOCK_API_STAGE})."
        assert not prod_hits, f"Stage page should NOT call production Stock API, found: {prod_hits}"
