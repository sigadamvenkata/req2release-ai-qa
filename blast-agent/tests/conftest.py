"""
conftest.py — pytest fixtures for the Remove Background test suite.

Browser matrix: chromium, firefox, webkit (Safari)
All browsers run headless. Override with PWDEBUG=1 locally.

NOTE: Uses custom fixture name 'target_browser' (not 'browser_name')
to avoid conflict with the pytest-playwright built-in fixture.
"""
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from tests.pages.nav_page import NavPage
from tests.pages.remove_bg_page import RemoveBgPage
from tests.pages.youtube_gallery_page import YouTubeGalleryPage

REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


# ── Browser fixtures ─────────────────────────────────────────────────────────

@pytest.fixture(scope="session", params=["chromium", "firefox", "webkit"])
def target_browser(request) -> str:
    """Parametrized fixture — yields browser name for each test run."""
    return request.param


@pytest.fixture(scope="function")
def page(target_browser: str) -> Page:
    """Provide a fresh browser page per test, per browser."""
    with sync_playwright() as pw:
        if target_browser == "chromium":
            browser: Browser = pw.chromium.launch(headless=True)
        elif target_browser == "firefox":
            browser = pw.firefox.launch(headless=True)
        elif target_browser == "webkit":
            browser = pw.webkit.launch(headless=True)
        else:
            browser = pw.chromium.launch(channel="msedge", headless=True)

        context: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        p: Page = context.new_page()
        yield p
        p.close()
        context.close()
        browser.close()


# ── Page Object fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def remove_bg(page: Page) -> RemoveBgPage:
    """RemoveBgPage opened and ready."""
    pg = RemoveBgPage(page)
    pg.open()
    return pg


@pytest.fixture
def nav(page: Page) -> NavPage:
    """NavPage opened on the Remove Background SEO page."""
    pg = RemoveBgPage(page)
    pg.open()
    return NavPage(page)


# ── Screenshot on failure ─────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page_fixture = item.funcargs.get("page")
        if page_fixture:
            browser = item.funcargs.get("target_browser", "unknown")
            name = item.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")
            path = REPORTS_DIR / f"FAIL_{browser}_{name}.png"
            try:
                page_fixture.screenshot(path=str(path), full_page=True)
            except Exception:
                pass
