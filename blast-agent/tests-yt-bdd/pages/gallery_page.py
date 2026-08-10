"""
YouTubeGalleryPage — all interactions specific to the YouTube Gallery block.

Inherits navigation and utility from BasePage.
Each method maps to one or more Gherkin steps in the feature files.
"""
from __future__ import annotations

from typing import List, Dict, Optional
from playwright.sync_api import Page, TimeoutError as PWTimeout

from pages.base_page import BasePage
from locators.gallery_locators import L


class YouTubeGalleryPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ══════════════════════════════════════════════════════════════════════════
    # Group 1 — Heading
    # ══════════════════════════════════════════════════════════════════════════

    def is_heading_visible(self) -> bool:
        """True if h2.heading-xl is in the viewport and not obscured."""
        return self.is_visible(L.HEADING)

    def get_heading_text(self) -> str:
        """Return the text content of the gallery heading."""
        return self.get_text(L.HEADING)

    def count_h2_in_gallery(self) -> int:
        """Count h2 elements inside the .prm-yt-gallery container."""
        return self.count(L.HEADING_IN_GALLERY)

    # ══════════════════════════════════════════════════════════════════════════
    # Group 2 — Grid & Card Layout
    # ══════════════════════════════════════════════════════════════════════════

    def is_grid_visible(self) -> bool:
        return self.is_visible(L.GRID)

    def get_card_count(self) -> int:
        return self.count(L.CARD)

    def get_grid_display_property(self) -> str:
        """Return the CSS display value of the grid container."""
        return self.page.eval_on_selector(
            L.GRID,
            "el => window.getComputedStyle(el).display"
        )

    def get_card_bounding_boxes(self) -> List[Dict]:
        """Return list of bounding boxes for every card."""
        cards = self.page.locator(L.CARD)
        boxes = []
        for i in range(cards.count()):
            box = cards.nth(i).bounding_box()
            if box:
                boxes.append(box)
        return boxes

    # ══════════════════════════════════════════════════════════════════════════
    # Group 3 — Card Metadata
    # ══════════════════════════════════════════════════════════════════════════

    def get_card_identifiers(self) -> List[Optional[str]]:
        """Return list of id or data-id attribute from every card."""
        cards = self.page.locator(L.CARD)
        ids = []
        for i in range(cards.count()):
            card = cards.nth(i)
            val = card.get_attribute("id") or card.get_attribute("data-id")
            ids.append(val)
        return ids

    def get_card_labels(self) -> List[str]:
        """Return text content of the label element inside every card."""
        cards = self.page.locator(L.CARD)
        labels = []
        for i in range(cards.count()):
            label_loc = cards.nth(i).locator(L.CARD_LABEL)
            text = ""
            if label_loc.count() > 0:
                text = (label_loc.first.text_content() or "").strip()
            labels.append(text)
        return labels

    def get_free_tag_count(self) -> int:
        return self.count(L.FREE_TAG)

    def get_thumbnail_srcs(self) -> List[str]:
        """Return the src attribute of every card thumbnail."""
        imgs = self.page.locator(L.CARD_THUMBNAIL)
        return [
            imgs.nth(i).get_attribute("src") or ""
            for i in range(imgs.count())
        ]

    def get_thumbnail_alts(self) -> List[Optional[str]]:
        """Return the alt attribute (may be None) of every card thumbnail."""
        imgs = self.page.locator(L.CARD_THUMBNAIL)
        return [imgs.nth(i).get_attribute("alt") for i in range(imgs.count())]

    def is_first_thumbnail_visible(self) -> bool:
        return self.page.locator(L.CARD_THUMBNAIL).first.is_visible()

    # ══════════════════════════════════════════════════════════════════════════
    # Group 4 — Page Layout & SEO
    # ══════════════════════════════════════════════════════════════════════════

    def get_meta_description(self) -> str:
        return self.get_meta_content(L.META_DESC)

    def is_meta_desc_present(self) -> bool:
        return self.count(L.META_DESC) > 0

    def is_gallery_in_main(self) -> bool:
        """True if .prm-yt-gallery is a descendant of <main>."""
        return self.page.eval_on_selector(
            L.GALLERY,
            "el => !!el.closest('main')"
        )

    def get_gallery_bounding_box(self) -> Optional[Dict]:
        return self.page.locator(L.GALLERY).first.bounding_box()

    # ══════════════════════════════════════════════════════════════════════════
    # Group 6 — Hover-to-Play Video
    # ══════════════════════════════════════════════════════════════════════════

    def hover_first_card(self) -> None:
        """Move mouse to centre of the first card."""
        self.page.locator(L.CARD).first.hover(timeout=8_000)
        self.page.wait_for_timeout(800)  # allow CSS transition

    def is_video_visible_in_first_card(self) -> bool:
        video = self.page.locator(L.CARD).first.locator(L.CARD_VIDEO)
        return video.count() > 0 and video.first.is_visible()

    def get_video_src_in_first_card(self) -> str:
        video = self.page.locator(L.CARD).first.locator(L.CARD_VIDEO)
        if video.count() == 0:
            return ""
        return video.first.get_attribute("src") or video.first.get_attribute("data-src") or ""

    def is_video_hidden_before_hover(self) -> bool:
        """Return True if video element is hidden (not yet hovered)."""
        video = self.page.locator(L.CARD).first.locator(L.CARD_VIDEO)
        if video.count() == 0:
            return True
        return not video.first.is_visible()

    # ══════════════════════════════════════════════════════════════════════════
    # Group 7 — No Click Navigation
    # ══════════════════════════════════════════════════════════════════════════

    def click_first_card(self) -> None:
        self.page.locator(L.CARD).first.click(timeout=8_000)
        self.page.wait_for_timeout(500)

    # ══════════════════════════════════════════════════════════════════════════
    # Group 9 — Mobile
    # ══════════════════════════════════════════════════════════════════════════

    def get_scroll_vs_inner_width(self) -> tuple[int, int]:
        """Return (scrollWidth, innerWidth) to detect horizontal overflow."""
        scroll_w = self.page.evaluate("document.body.scrollWidth")
        inner_w  = self.page.evaluate("window.innerWidth")
        return scroll_w, inner_w
