"""
Spec: Group 10 — Stock API Integration
Feature file: features/10_stock_api.feature
Ticket: MWPW-199796  |  Tags: @smoke @integration

Uses page_raw fixture (Chromium with no pre-navigation) so request
interception can be set up before the page loads.
"""
import allure
import pytest
from playwright.sync_api import Page
from locators.gallery_locators import PAGE_URL, STOCK_API_STAGE, STOCK_API_PROD


@allure.feature("YouTube Gallery Block — MWPW-199796")
@allure.story("Group 10: Stock API Integration — Stage vs Prod Routing")
class TestStockAPI:

    @allure.title("[10.1][smoke][integration] Stock API called during page load")
    @allure.description(
        f"Intercept network before navigation and verify at least one request "
        f"hits {STOCK_API_STAGE} during page load."
    )
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_stock_api_called(self, page_raw: Page):
        captured = []
        page_raw.on(
            "request",
            lambda r: captured.append(r.url)
            if STOCK_API_STAGE in r.url or STOCK_API_PROD in r.url
            else None,
        )
        page_raw.goto(PAGE_URL, wait_until="networkidle", timeout=40_000)
        page_raw.wait_for_timeout(3_000)

        allure.attach(
            "\n".join(captured) if captured else "(none)",
            name="stock_api_requests",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert captured, (
            "No Stock API request detected during page load. "
            f"Expected a request to: {STOCK_API_STAGE}"
        )

    @allure.title("[10.2][smoke][integration] Stock API returns 2xx on stage")
    @allure.description(
        "All intercepted Stock API responses must be HTTP 2xx."
    )
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_stock_api_2xx_response(self, page_raw: Page):
        responses: dict[str, int] = {}
        page_raw.on(
            "response",
            lambda r: responses.update({r.url: r.status})
            if STOCK_API_STAGE in r.url or STOCK_API_PROD in r.url
            else None,
        )
        page_raw.goto(PAGE_URL, wait_until="networkidle", timeout=40_000)
        page_raw.wait_for_timeout(3_000)

        allure.attach(
            str(responses) if responses else "(no responses captured)",
            name="stock_api_responses",
            attachment_type=allure.attachment_type.TEXT,
        )

        if not responses:
            pytest.skip("No Stock API response captured — skipping status check.")

        failed = {url: st for url, st in responses.items() if not (200 <= st < 300)}
        assert not failed, (
            f"Stock API returned non-2xx responses: {failed}"
        )

    @allure.title("[10.3][smoke][integration] Stage page only calls stage endpoint")
    @allure.description(
        "The staging URL must call the stage Stock API only. "
        f"Prod endpoint ({STOCK_API_PROD}) must NOT be called."
    )
    @pytest.mark.smoke
    @pytest.mark.integration
    def test_stage_calls_stage_endpoint_only(self, page_raw: Page):
        stage_hits: list[str] = []
        prod_hits: list[str]  = []

        page_raw.on(
            "request",
            lambda r: (
                stage_hits.append(r.url) if STOCK_API_STAGE in r.url
                else prod_hits.append(r.url) if STOCK_API_PROD in r.url
                else None
            ),
        )
        page_raw.goto(PAGE_URL, wait_until="networkidle", timeout=40_000)
        page_raw.wait_for_timeout(3_000)

        allure.attach(
            f"Stage hits : {stage_hits}\nProd hits  : {prod_hits}",
            name="endpoint_routing",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert stage_hits, (
            f"No request to stage Stock API ({STOCK_API_STAGE}) detected."
        )
        assert not prod_hits, (
            f"Stage page is calling PRODUCTION Stock API — wrong routing! "
            f"Prod hits: {prod_hits}"
        )
