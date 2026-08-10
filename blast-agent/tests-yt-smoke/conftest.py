"""
conftest.py — fixtures for the YouTube Gallery @smoke test suite (MWPW-199796).
Self-contained; no shared state with any other suite in this repo.

Fixtures:
  page          — Chromium 1440x900 headless, autoplay enabled
  page_firefox  — Firefox 1440x900 headless
  page_webkit   — WebKit  1440x900 headless
  page_mobile   — Chromium 375x812 headless (portrait)
  page_raw      — Chromium 1440x900, no page opened (for request interception)

  gallery         — YouTubeGalleryPage opened on `page`
  gallery_firefox — YouTubeGalleryPage opened on `page_firefox`
  gallery_webkit  — YouTubeGalleryPage opened on `page_webkit`
  gallery_mobile  — YouTubeGalleryPage opened on `page_mobile`
"""
import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.yt_gallery_page import YouTubeGalleryPage

REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

# ── Chromium 1440x900 (default, autoplay enabled) ────────────────────────────

@pytest.fixture(scope="function")
def page() -> Page:
    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(
            headless=True,
            args=["--autoplay-policy=no-user-gesture-required"],
        )
        ctx: BrowserContext = browser.new_context(
            viewport={"width": 1440, "height": 900}, user_agent=_UA
        )
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Firefox 1440x900 ─────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page_firefox() -> Page:
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── WebKit 1440x900 ──────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page_webkit() -> Page:
    with sync_playwright() as pw:
        browser = pw.webkit.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Chromium 375x812 portrait (mobile) ───────────────────────────────────────

@pytest.fixture(scope="function")
def page_mobile() -> Page:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 375, "height": 812},
            user_agent=_UA,
            is_mobile=True,
        )
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Chromium raw (no page opened — for pre-nav request interception) ──────────

@pytest.fixture(scope="function")
def page_raw() -> Page:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Page-object fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def gallery(page: Page) -> YouTubeGalleryPage:
    pg = YouTubeGalleryPage(page)
    pg.open()
    return pg


@pytest.fixture
def gallery_firefox(page_firefox: Page) -> YouTubeGalleryPage:
    pg = YouTubeGalleryPage(page_firefox)
    pg.open()
    return pg


@pytest.fixture
def gallery_webkit(page_webkit: Page) -> YouTubeGalleryPage:
    pg = YouTubeGalleryPage(page_webkit)
    pg.open()
    return pg


@pytest.fixture
def gallery_mobile(page_mobile: Page) -> YouTubeGalleryPage:
    pg = YouTubeGalleryPage(page_mobile)
    pg.open()
    return pg


# ── Screenshot on failure ─────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        for fixture_name in ("page", "page_firefox", "page_webkit", "page_mobile", "page_raw"):
            p = item.funcargs.get(fixture_name)
            if p:
                safe = item.nodeid.replace("/", "_").replace("::", "_").replace(" ", "_")
                png = REPORTS_DIR / f"FAIL_{fixture_name}_{safe}.png"
                try:
                    shot = p.screenshot(full_page=True)
                    png.write_bytes(shot)
                    allure.attach(shot, name="failure_screenshot",
                                  attachment_type=allure.attachment_type.PNG)
                except Exception:
                    pass
                break
