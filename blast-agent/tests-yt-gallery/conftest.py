"""
conftest.py — fixtures for the YouTube Gallery UI test suite (MWPW-199796).
Completely self-contained; no imports from any other test suite.

Browser: Chromium headless at 1440x900 (desktop @ui tests).
Screenshots are captured as Allure attachments on every test failure.
"""
import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.yt_gallery_page import YouTubeGalleryPage

REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


# ── Browser / Page ────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page() -> Page:
    """Fresh Chromium page at 1440x900 for each test."""
    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=True)
        ctx: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        p: Page = ctx.new_page()
        yield p
        p.close()
        ctx.close()
        browser.close()


# ── Page-object fixture ───────────────────────────────────────────────────────

@pytest.fixture
def gallery(page: Page) -> YouTubeGalleryPage:
    """Open YouTube Gallery page and return a ready page object."""
    pg = YouTubeGalleryPage(page)
    pg.open()
    return pg


# ── Screenshot on failure (Allure + file) ────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page_obj: Page | None = item.funcargs.get("page")
        if page_obj:
            safe_name = item.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")
            png_path = REPORTS_DIR / f"FAIL_{safe_name}.png"
            try:
                screenshot = page_obj.screenshot(full_page=True)
                with open(png_path, "wb") as f:
                    f.write(screenshot)
                allure.attach(
                    screenshot,
                    name=f"failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
