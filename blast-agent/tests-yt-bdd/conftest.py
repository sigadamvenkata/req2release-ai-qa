"""
conftest.py — fixtures for the tests-yt-bdd suite.

Fixtures provided:
  page              → Chromium 1440x900 desktop (pre-navigated + modal dismissed)
  page_firefox      → Firefox  1440x900 desktop (raw page, no navigation)
  page_webkit       → WebKit   1440x900 desktop (raw page, no navigation)
  page_portrait     → Chromium 375x812 mobile portrait
  page_landscape    → Chromium 812x375 mobile landscape
  page_raw          → Chromium 1440x900, NO navigation (for request interception)

  gallery           → YouTubeGalleryPage backed by Chromium page (navigated + modal dismissed)
  gallery_no_hover  → same as gallery but no hover performed (for pre-hover video tests)
  gallery_firefox   → YouTubeGalleryPage backed by Firefox (navigated + modal dismissed)
  gallery_webkit    → YouTubeGalleryPage backed by WebKit   (navigated + modal dismissed)
  gallery_portrait  → YouTubeGalleryPage backed by mobile portrait
  gallery_landscape → YouTubeGalleryPage backed by mobile landscape
"""
import pytest
import allure
from playwright.sync_api import sync_playwright, Page

from pages.gallery_page import YouTubeGalleryPage
from locators.gallery_locators import PAGE_URL

# ── Browser args ──────────────────────────────────────────────────────────────
CHROMIUM_ARGS = ["--autoplay-policy=no-user-gesture-required"]
DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
PORTRAIT_VIEWPORT = {"width": 375, "height": 812}
LANDSCAPE_VIEWPORT = {"width": 812, "height": 375}


# ══════════════════════════════════════════════════════════════════════════════
# Raw page fixtures (browser + context only, no navigation)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="function")
def page():
    """Chromium desktop 1440x900 page (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=CHROMIUM_ARGS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT)
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_firefox():
    """Firefox desktop 1440x900 page (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=True)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT)
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_webkit():
    """WebKit desktop 1440x900 page (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.webkit.launch(headless=True)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT)
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_portrait():
    """Chromium mobile portrait 375x812 (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=CHROMIUM_ARGS)
        ctx = browser.new_context(viewport=PORTRAIT_VIEWPORT, is_mobile=True)
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_landscape():
    """Chromium mobile landscape 812x375 (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=CHROMIUM_ARGS)
        ctx = browser.new_context(viewport=LANDSCAPE_VIEWPORT, is_mobile=True)
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_raw():
    """
    Chromium 1440x900 with NO page opened — for Stock API request interception.
    Tests must call page.goto() themselves after setting up listeners.
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=CHROMIUM_ARGS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT)
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════════════
# Page-object fixtures (navigate + dismiss modal)
# ══════════════════════════════════════════════════════════════════════════════

def _make_gallery(raw_page: Page, dismiss: bool = True) -> YouTubeGalleryPage:
    gp = YouTubeGalleryPage(raw_page)
    gp.navigate()
    if dismiss:
        gp.dismiss_modal()
    return gp


@pytest.fixture(scope="function")
def gallery(page: Page) -> YouTubeGalleryPage:
    """Chromium desktop gallery — navigated, modal dismissed."""
    return _make_gallery(page)


@pytest.fixture(scope="function")
def gallery_no_hover(page: Page) -> YouTubeGalleryPage:
    """Chromium desktop gallery — navigated, modal dismissed, NO hover performed."""
    return _make_gallery(page, dismiss=True)


@pytest.fixture(scope="function")
def gallery_firefox(page_firefox: Page) -> YouTubeGalleryPage:
    """Firefox desktop gallery — navigated, modal dismissed."""
    return _make_gallery(page_firefox)


@pytest.fixture(scope="function")
def gallery_webkit(page_webkit: Page) -> YouTubeGalleryPage:
    """WebKit desktop gallery — navigated, modal dismissed."""
    return _make_gallery(page_webkit)


@pytest.fixture(scope="function")
def gallery_portrait(page_portrait: Page) -> YouTubeGalleryPage:
    """Mobile portrait 375x812 gallery — navigated, modal dismissed."""
    return _make_gallery(page_portrait)


@pytest.fixture(scope="function")
def gallery_landscape(page_landscape: Page) -> YouTubeGalleryPage:
    """Mobile landscape 812x375 gallery — navigated, modal dismissed."""
    return _make_gallery(page_landscape)


# ══════════════════════════════════════════════════════════════════════════════
# Screenshot on failure hook
# ══════════════════════════════════════════════════════════════════════════════

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        for fixture_name in ("gallery", "gallery_firefox", "gallery_webkit",
                             "gallery_portrait", "gallery_landscape",
                             "gallery_no_hover"):
            gp: YouTubeGalleryPage = item.funcargs.get(fixture_name)
            if gp:
                try:
                    allure.attach(
                        gp.screenshot_bytes(),
                        name=f"FAILURE_{fixture_name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception:
                    pass
                break
