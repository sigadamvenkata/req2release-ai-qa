"""
Spec: Scenario Group 9 — Stock API Integration
Ticket: MWPW-199796  |  Tags: @smoke @integration

Stock API confirmed from network inspection:
  Stage : https://www.stage.adobe.com/stock-api/Rest/Media/1/Search/Collections
  Prod  : https://www.adobe.com/stock-api/Rest/Media/1/Search/Collections
"""
import pytest
import allure
from playwright.sync_api import Page
from locators.yt_smoke_locators import PAGE_URL, STOCK_API_STAGE, STOCK_API_PROD


@allure.feature("YouTube Gallery — Smoke")
@allure.story("MWPW-199796 | Group 9: Stock API Called on Page Load")
class TestStockAPI:

    @allure.title("[smoke][integration] Stock API is called and returns 2xx on page load (stage)")
    @allure.description(
        "Intercept all network requests during page load and verify that at least "
        "one request is made to the stage Stock API endpoint "
        f"({STOCK_API_STAGE}). "
        "Also verify the response carries an HTTP 2xx status code."
    )
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_stock_api_called_on_page_load(self, page_raw: Page):
        captured_requests  = []
        captured_responses = {}

        # Intercept before navigation
        page_raw.on(
            "request",
            lambda r: captured_requests.append(r.url)
            if STOCK_API_STAGE in r.url or STOCK_API_PROD in r.url
            else None,
        )
        page_raw.on(
            "response",
            lambda r: captured_responses.update({r.url: r.status})
            if STOCK_API_STAGE in r.url or STOCK_API_PROD in r.url
            else None,
        )

        page_raw.goto(PAGE_URL, wait_until="networkidle", timeout=40000)
        page_raw.wait_for_timeout(3000)

        allure.attach(
            "\n".join(captured_requests) if captured_requests else "(none captured)",
            name="stock_api_requests",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            str(captured_responses) if captured_responses else "(none captured)",
            name="stock_api_responses",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert captured_requests, (
            f"No Stock API request was detected during page load.\n"
            f"Expected a request to: {STOCK_API_STAGE} or {STOCK_API_PROD}"
        )

        failed = {url: status for url, status in captured_responses.items()
                  if not (200 <= status < 300)}
        assert not failed, (
            f"Stock API returned non-2xx response(s): {failed}"
        )

    @allure.title("[smoke][integration] Stage environment calls stage Stock API endpoint only")
    @allure.description(
        "Verify that the staging page URL triggers requests to the stage Stock API "
        f"({STOCK_API_STAGE}) and not the production endpoint ({STOCK_API_PROD})."
    )
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_stage_calls_stage_endpoint(self, page_raw: Page):
        stage_hits = []
        prod_hits  = []

        page_raw.on(
            "request",
            lambda r: stage_hits.append(r.url) if STOCK_API_STAGE in r.url
            else prod_hits.append(r.url) if STOCK_API_PROD in r.url
            else None,
        )

        page_raw.goto(PAGE_URL, wait_until="networkidle", timeout=40000)
        page_raw.wait_for_timeout(3000)

        allure.attach(
            f"Stage hits : {stage_hits}\nProd hits  : {prod_hits}",
            name="endpoint_routing",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert stage_hits, (
            f"Expected at least one request to stage Stock API ({STOCK_API_STAGE}), found none."
        )
        assert not prod_hits, (
            f"Stage page should NOT call production Stock API, but found: {prod_hits}"
        )
