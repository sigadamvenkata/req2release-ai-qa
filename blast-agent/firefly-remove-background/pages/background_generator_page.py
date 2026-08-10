"""
Background Generator Page Object — MWPW-200902
Encapsulates all queries/actions against the Firefly "AI Background Generator"
marquee + Unity upload block.

URL: https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html
"""
import base64
import mimetypes
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PWTimeout

from pages.base_page import BasePage
from locators.bg_generator_locators import PAGE_URL, FIREFLY_REDIRECT_PATTERN, L

# tests/assets is shared at the repo root: blast-agent/tests/assets
ASSETS_DIR = Path(__file__).parent.parent.parent / "tests" / "assets"


class BackgroundGeneratorPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Open & modal handling ─────────────────────────────────────────────────

    def open(self):
        """Navigate to the page and dismiss the locale modal if present."""
        self.navigate(PAGE_URL)
        self._dismiss_modal_if_present()

    def _dismiss_modal_if_present(self):
        """
        The locale/region modal (.modal-curtain.is-open) auto-opens on page load
        and blocks all pointer events, same pattern as the YouTube Gallery block
        (MWPW-199796). Clicking the curtain closes it; Escape is the fallback.
        """
        curtain = self.page.locator(L.MODAL_CURTAIN)
        if curtain.count() > 0 and curtain.first.is_visible():
            try:
                curtain.first.click(timeout=5000)
                self.page.wait_for_selector(L.MODAL_CURTAIN, state="hidden", timeout=5000)
            except PWTimeout:
                self.page.keyboard.press("Escape")
                self.page.wait_for_timeout(500)

    # ── Page-level ────────────────────────────────────────────────────────────

    def get_page_title(self) -> str:
        return self.get_title()

    def get_current_url(self) -> str:
        return self.page.url

    def get_meta_description(self) -> str:
        return self.get_meta_content("description")

    # ── Marquee / branding ────────────────────────────────────────────────────

    def is_mnemonic_visible(self) -> bool:
        return self.is_visible(L.FIREFLY_MNEMONIC)

    def get_wordmark_text(self) -> str:
        return self.get_text(L.FIREFLY_WORDMARK)

    def is_h1_visible(self) -> bool:
        return self.is_visible(L.H1)

    def get_h1_text(self) -> str:
        return self.get_text(L.H1)

    def get_subheading_text(self) -> str:
        return self.get_text(L.SUBHEADING)

    def is_upload_content_left_of_media(self) -> bool:
        """True if .upload-marquee-left is positioned left of .upload-marquee-right."""
        return self.page.evaluate(
            """() => {
                const left = document.querySelector('.upload-marquee-left');
                const right = document.querySelector('.upload-marquee-right');
                if (!left || !right) return false;
                return left.getBoundingClientRect().left < right.getBoundingClientRect().left;
            }"""
        )

    # ── Upload block layout ───────────────────────────────────────────────────

    def is_upload_cta_visible(self) -> bool:
        return self.is_visible(L.UPLOAD_CTA)

    def get_upload_cta_text(self) -> str:
        return self.get_text(L.UPLOAD_CTA)

    def is_drop_zone_visible(self) -> bool:
        return self.is_visible(L.DROP_ZONE)

    def get_format_hint_text(self) -> str:
        return self.get_text(L.DROP_ZONE_BODY)

    def get_drop_zone_heading_text(self) -> str:
        return self.get_text(L.DROP_ZONE_HEADING)

    def get_terms_href(self) -> str:
        return self.page.locator(L.TERMS_LINK).first.get_attribute("href") or ""

    def get_privacy_href(self) -> str:
        return self.page.locator(L.PRIVACY_LINK).first.get_attribute("href") or ""

    # ── Upload actions (click CTA) ────────────────────────────────────────────

    def upload_file(self, filename: str):
        """Upload a single file via the hidden file input of the visible drop zone."""
        file_path = str(ASSETS_DIR / filename)
        self.page.locator(L.FILE_INPUT).set_input_files(file_path)
        self.page.wait_for_timeout(1500)

    # ── Upload actions (native drag-and-drop simulation) ─────────────────────

    def upload_file_via_drag_and_drop(self, filename: str):
        """
        Simulate an OS-level drag-and-drop of a file onto the drop zone.
        Real OS drag-and-drop cannot be automated directly, so this builds an
        in-page DataTransfer carrying the file bytes and dispatches the
        dragenter/dragover/drop sequence — the standard documented Playwright
        technique for testing HTML5 file-drop targets.
        """
        self._drop_files([filename])

    def upload_files_via_drag_and_drop(self, filenames: list):
        """
        Drag-and-drop multiple files at once onto the drop zone.
        Confirmed live (2026-07-17): the real <input type="file"> has no
        `multiple` attribute, so Playwright's set_input_files() correctly
        refuses more than one file — the "Only one file can be uploaded at a
        time" error is only reachable via a multi-file drop, not the picker.
        """
        self._drop_files(filenames)

    def _drop_files(self, filenames: list):
        items = []
        for filename in filenames:
            file_path = ASSETS_DIR / filename
            buffer_b64 = base64.b64encode(file_path.read_bytes()).decode()
            mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
            items.append({"bufferData": buffer_b64, "fileName": filename, "fileType": mime_type})

        data_transfer = self.page.evaluate_handle(
            """(files) => {
                const dt = new DataTransfer();
                for (const f of files) {
                    const bytes = Uint8Array.from(atob(f.bufferData), c => c.charCodeAt(0));
                    dt.items.add(new File([bytes], f.fileName, { type: f.fileType }));
                }
                return dt;
            }""",
            items,
        )

        drop_zone = self.page.locator(L.DROP_ZONE)
        drop_zone.dispatch_event("dragenter", {"dataTransfer": data_transfer})
        drop_zone.dispatch_event("dragover", {"dataTransfer": data_transfer})
        drop_zone.dispatch_event("drop", {"dataTransfer": data_transfer})
        self.page.wait_for_timeout(1500)

    # ── Errors ────────────────────────────────────────────────────────────────

    def get_error_message(self) -> str:
        """Return the first visible error message text, or '' if none is shown."""
        for selector in L.ERROR_CANDIDATES:
            el = self.page.locator(selector)
            if el.count() and el.first.is_visible():
                return el.first.inner_text().strip()
        return ""

    def is_error_visible(self) -> bool:
        return bool(self.get_error_message())

    def get_error_config_texts(self) -> list:
        """Reference error copy from the always-present .workflow-upload config block."""
        return self.page.eval_on_selector_all(
            L.ERROR_CONFIG_ITEMS, "els => els.map(e => e.innerText.trim())"
        )

    # ── Splash / upload-progress screen ──────────────────────────────────────

    def is_splash_visible(self) -> bool:
        return self.is_visible(L.SPLASH_LOADER)

    def wait_for_splash_visible(self, timeout: int = 5000):
        self.page.wait_for_selector(L.SPLASH_LOADER, state="visible", timeout=timeout)

    def wait_for_splash_hidden(self, timeout: int = 60000):
        self.page.wait_for_selector(L.SPLASH_LOADER, state="hidden", timeout=timeout)

    def get_splash_message(self) -> str:
        return self.get_text(L.SPLASH_MESSAGE)

    # ── Cross-app redirect ────────────────────────────────────────────────────

    def wait_for_firefly_redirect(self, timeout: int = 60000) -> str:
        """Wait for navigation to the Firefly product app and return the final URL."""
        self.page.wait_for_url(f"**{FIREFLY_REDIRECT_PATTERN.replace(chr(92), '')}**", timeout=timeout)
        return self.page.url

    # ── Accessibility ─────────────────────────────────────────────────────────

    def get_hero_image_alt(self) -> str:
        img = self.page.locator(".upload-marquee-media img").first
        return img.get_attribute("alt") if img.count() else None

    def get_all_heading_levels(self) -> list:
        """Return [(tagName, text), ...] for every heading element in document order."""
        return self.page.eval_on_selector_all(
            L.ALL_HEADINGS,
            "els => els.map(e => [e.tagName.toLowerCase(), e.innerText.trim()])",
        )

    def focus_upload_cta_via_tab(self, max_tabs: int = 30) -> bool:
        """
        Press Tab repeatedly until the upload CTA receives focus, or max_tabs is hit.

        The three .drop-zone-container breakpoint variants are toggled visible
        via CSS media queries (no inline "display: none"), so the visible one
        must be identified by actual rendered size (offsetWidth/Height), not
        by inspecting inline styles or classes.
        """
        for _ in range(max_tabs):
            self.page.keyboard.press("Tab")
            if self.page.evaluate(
                """() => {
                    const ctas = Array.from(document.querySelectorAll('.drop-zone-container a.con-button'));
                    const visibleCta = ctas.find(el => el.offsetWidth || el.offsetHeight);
                    return !!visibleCta && document.activeElement === visibleCta;
                }"""
            ):
                return True
        return False
