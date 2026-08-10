"""
conftest.py — fixtures for the Firefly Background Generator suite (MWPW-200902).
Self-contained; no shared state with any other suite in this repo.

Fixtures:
  page                    — Chromium 1440x900 (headed by default, see HEADLESS below)
  page_firefox             — Firefox  1440x900
  page_webkit              — WebKit   1440x900
  page_mobile               — Chromium 375x812  (portrait, is_mobile)
  page_mobile_landscape    — Chromium 812x375  (landscape, is_mobile)
  page_raw                 — Chromium 1440x900, no page opened (for request interception)

Set HEADLESS=true in the environment to run headless (e.g. in CI).

  bg_gen                   — BackgroundGeneratorPage opened on `page`
  bg_gen_firefox           — BackgroundGeneratorPage opened on `page_firefox`
  bg_gen_webkit            — BackgroundGeneratorPage opened on `page_webkit`
  bg_gen_mobile            — BackgroundGeneratorPage opened on `page_mobile`
  bg_gen_mobile_landscape  — BackgroundGeneratorPage opened on `page_mobile_landscape`
"""
import os
import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

from pages.background_generator_page import BackgroundGeneratorPage

REPORTS_DIR = Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# HEADLESS=true switches back to headless for CI; defaults to headed so the
# browser is visible while running locally.
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
SLOW_MO = 0 if HEADLESS else 150

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


# ── Chromium 1440x900 (default) ──────────────────────────────────────────────

@pytest.fixture(scope="function")
def page() -> Page:
    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
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
        browser = pw.firefox.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── WebKit 1440x900 ──────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page_webkit() -> Page:
    with sync_playwright() as pw:
        browser = pw.webkit.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Chromium 375x812 portrait (mobile) ───────────────────────────────────────

@pytest.fixture(scope="function")
def page_mobile() -> Page:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        ctx = browser.new_context(
            viewport={"width": 375, "height": 812}, user_agent=_UA, is_mobile=True
        )
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Chromium 812x375 landscape (mobile) ──────────────────────────────────────

@pytest.fixture(scope="function")
def page_mobile_landscape() -> Page:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        ctx = browser.new_context(
            viewport={"width": 812, "height": 375}, user_agent=_UA, is_mobile=True
        )
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Chromium raw (no page opened — for pre-nav request interception) ────────

@pytest.fixture(scope="function")
def page_raw() -> Page:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        p = ctx.new_page()
        yield p
        p.close(); ctx.close(); browser.close()


# ── Page-object fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def bg_gen(page: Page) -> BackgroundGeneratorPage:
    pg = BackgroundGeneratorPage(page)
    pg.open()
    return pg


@pytest.fixture
def bg_gen_firefox(page_firefox: Page) -> BackgroundGeneratorPage:
    pg = BackgroundGeneratorPage(page_firefox)
    pg.open()
    return pg


@pytest.fixture
def bg_gen_webkit(page_webkit: Page) -> BackgroundGeneratorPage:
    pg = BackgroundGeneratorPage(page_webkit)
    pg.open()
    return pg


@pytest.fixture
def bg_gen_mobile(page_mobile: Page) -> BackgroundGeneratorPage:
    pg = BackgroundGeneratorPage(page_mobile)
    pg.open()
    return pg


@pytest.fixture
def bg_gen_mobile_landscape(page_mobile_landscape: Page) -> BackgroundGeneratorPage:
    pg = BackgroundGeneratorPage(page_mobile_landscape)
    pg.open()
    return pg


# ── Screenshot on failure ─────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        for fixture_name in (
            "page", "page_firefox", "page_webkit",
            "page_mobile", "page_mobile_landscape", "page_raw",
        ):
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
