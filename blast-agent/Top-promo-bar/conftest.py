"""
conftest.py — fixtures for the Top-promo-bar suite (MWPW-203117).

Raw page fixtures (browser + context only, no navigation):
  page              -> Chromium desktop 1440x900, light theme, en-US
  page_firefox      -> Firefox  desktop 1440x900, light theme, en-US
  page_webkit       -> WebKit   desktop 1440x900, light theme, en-US
  page_dark         -> Chromium desktop 1440x900, dark theme, en-US
  page_portrait     -> Chromium mobile 375x812 portrait, light theme
  page_landscape    -> Chromium mobile 812x375 landscape, light theme
  page_rtl          -> Chromium desktop 1440x900, locale "ar" (RTL check)
  page_intl         -> Chromium desktop 1440x900, locale "fr-FR" (non-English LTR check)

Page-object fixtures (navigate to C2 + wait for the banner to load):
  promo_banner            -> backed by `page`
  promo_banner_c1         -> backed by `page`, opened on the C1 (Creative Cloud) URL
  promo_banner_no_wait    -> backed by `page`, navigated but does NOT wait for the
                             banner (for Feature 2 — delayed/async load tests)
  promo_banner_firefox    -> backed by `page_firefox`
  promo_banner_webkit     -> backed by `page_webkit`
  promo_banner_dark       -> backed by `page_dark`
  promo_banner_portrait   -> backed by `page_portrait`
  promo_banner_landscape  -> backed by `page_landscape`
  promo_banner_rtl        -> backed by `page_rtl`
  promo_banner_intl       -> backed by `page_intl`

NOTE: The banner is expected to load asynchronously ~5s after the page — every
`promo_banner*` fixture (except `_no_wait`) waits up to 10s for it via
PromoBannerPage.wait_for_banner() before handing the page object to the test.
"""
import os

import pytest
import allure
from playwright.sync_api import sync_playwright, Page

from pages.promo_banner_page import PromoBannerPage
from locators.promo_locators import C1_URL, C2_URL, RTL_URL, INTL_URL

DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
PORTRAIT_VIEWPORT = {"width": 375, "height": 812}
LANDSCAPE_VIEWPORT = {"width": 812, "height": 375}

BANNER_WAIT_TIMEOUT_MS = 10_000  # banner is expected ~5s after load; allow headroom

# Headless by default (CI-friendly), matching the rest of the suites in this repo.
# Set PW_HEADED=1 to watch the browser locally, e.g.: PW_HEADED=1 pytest
HEADLESS = os.environ.get("PW_HEADED", "0") not in ("1", "true", "True")
SLOW_MO_MS = int(os.environ.get("PW_SLOWMO", "0"))  # optional slow-motion when headed


# ══════════════════════════════════════════════════════════════════════════════
# Raw page fixtures (browser + context only, no navigation)
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="function")
def page():
    """Chromium desktop 1440x900, light theme, en-US (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT, color_scheme="light", locale="en-US")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_firefox():
    """Firefox desktop 1440x900, light theme, en-US (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT, color_scheme="light", locale="en-US")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_webkit():
    """WebKit desktop 1440x900, light theme, en-US (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.webkit.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT, color_scheme="light", locale="en-US")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_dark():
    """Chromium desktop 1440x900, dark theme, en-US (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT, color_scheme="dark", locale="en-US")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_portrait():
    """Chromium mobile portrait 375x812, light theme (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=PORTRAIT_VIEWPORT, is_mobile=True, color_scheme="light")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_landscape():
    """Chromium mobile landscape 812x375, light theme (no navigation yet)."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=LANDSCAPE_VIEWPORT, is_mobile=True, color_scheme="light")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_rtl():
    """Chromium desktop 1440x900, Arabic locale — representative RTL check."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT, color_scheme="light", locale="ar-AE")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page_intl():
    """Chromium desktop 1440x900, French locale — representative non-English LTR check."""
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO_MS)
        ctx = browser.new_context(viewport=DESKTOP_VIEWPORT, color_scheme="light", locale="fr-FR")
        pg = ctx.new_page()
        yield pg
        ctx.close()
        browser.close()


# ══════════════════════════════════════════════════════════════════════════════
# Page-object fixtures (navigate + wait for the banner)
# ══════════════════════════════════════════════════════════════════════════════

def _make_promo_banner(raw_page: Page, url: str = C2_URL, wait: bool = True) -> PromoBannerPage:
    pb = PromoBannerPage(raw_page)
    pb.navigate(url)
    if wait:
        pb.wait_for_banner(timeout=BANNER_WAIT_TIMEOUT_MS)
    return pb


@pytest.fixture(scope="function")
def promo_banner(page: Page) -> PromoBannerPage:
    """Chromium desktop, C2 page, banner awaited."""
    return _make_promo_banner(page, url=C2_URL)


@pytest.fixture(scope="function")
def promo_banner_c1(page: Page) -> PromoBannerPage:
    """Chromium desktop, C1 (Creative Cloud) page, banner awaited."""
    return _make_promo_banner(page, url=C1_URL)


@pytest.fixture(scope="function")
def promo_banner_no_wait(page: Page) -> PromoBannerPage:
    """Chromium desktop, C2 page, navigated but NOT waiting for the banner —
    used to inspect the pre-load window for Feature 2 (delayed/async load)."""
    return _make_promo_banner(page, url=C2_URL, wait=False)


@pytest.fixture(scope="function")
def promo_banner_firefox(page_firefox: Page) -> PromoBannerPage:
    return _make_promo_banner(page_firefox, url=C2_URL)


@pytest.fixture(scope="function")
def promo_banner_webkit(page_webkit: Page) -> PromoBannerPage:
    return _make_promo_banner(page_webkit, url=C2_URL)


@pytest.fixture(scope="function")
def promo_banner_dark(page_dark: Page) -> PromoBannerPage:
    return _make_promo_banner(page_dark, url=C2_URL)


@pytest.fixture(scope="function")
def promo_banner_portrait(page_portrait: Page) -> PromoBannerPage:
    return _make_promo_banner(page_portrait, url=C2_URL)


@pytest.fixture(scope="function")
def promo_banner_landscape(page_landscape: Page) -> PromoBannerPage:
    return _make_promo_banner(page_landscape, url=C2_URL)


@pytest.fixture(scope="function")
def promo_banner_rtl(page_rtl: Page) -> PromoBannerPage:
    # adobe.com locale is URL-path-driven, not Accept-Language-driven — the
    # `locale="ar-AE"` context option on page_rtl alone does NOT change the
    # site's rendered locale (verified). Navigate to the real RTL URL instead.
    return _make_promo_banner(page_rtl, url=RTL_URL)


@pytest.fixture(scope="function")
def promo_banner_intl(page_intl: Page) -> PromoBannerPage:
    # Same reasoning as promo_banner_rtl — navigate to the real French URL
    # rather than relying on the browser's locale context option alone.
    return _make_promo_banner(page_intl, url=INTL_URL)


# ══════════════════════════════════════════════════════════════════════════════
# Screenshot on failure hook
# ══════════════════════════════════════════════════════════════════════════════

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        for fixture_name in (
            "promo_banner", "promo_banner_c1", "promo_banner_no_wait",
            "promo_banner_firefox", "promo_banner_webkit", "promo_banner_dark",
            "promo_banner_portrait", "promo_banner_landscape",
            "promo_banner_rtl", "promo_banner_intl",
        ):
            pb: PromoBannerPage = item.funcargs.get(fixture_name)
            if pb:
                try:
                    allure.attach(
                        pb.screenshot_bytes(),
                        name=f"FAILURE_{fixture_name}",
                        attachment_type=allure.attachment_type.PNG,
                    )
                except Exception:
                    pass
                break
