# Test Findings — tests-yt-bdd
**Ticket:** MWPW-199796 | **Suite:** tests-yt-bdd | **Last Run:** 2026-07-03
**Result:** 20 passed · 8 failed · 1 xpassed | Duration: 5m 18s

---

## Run Summary

| Group | Test | Result | Root Cause |
|---|---|---|---|
| 1.1 | test_heading_visible | **FAIL** | Locale modal blocks h2.heading-xl — MWPW-199809 |
| 1.2 | test_heading_text_non_empty | **FAIL** | h2.heading-xl not in DOM (modal blocking, timeout 30s) |
| 1.3 | test_single_h2_in_gallery | **FAIL** | 0 h2 found inside `.prm-yt-gallery` — selector mismatch |
| 2.1 | test_grid_visible | PASS | |
| 2.2 | test_at_least_one_card | PASS | |
| 2.3 | test_grid_display_property | PASS | |
| 2.4 | test_card_bounding_boxes | PASS | |
| 3.1 | test_unique_card_identifiers | PASS | |
| 3.2 | test_card_labels_non_empty | **FAIL** | `.pre-yt-card-label` selector returns empty text on all 15 cards |
| 3.3 | test_free_tag_present | PASS | |
| 3.4 | test_thumbnail_src_and_visibility | PASS | |
| 3.5 | test_thumbnail_alt_attributes | PASS | |
| 4.1 | test_page_title_non_empty | PASS | |
| 4.2 | test_meta_description_present | **XPASS** | Expected to fail (MWPW-199810) but PASSED — bug may be fixed |
| 4.3 | test_gallery_inside_main | PASS | |
| 5.1 | test_page_http_200 | PASS | |
| 5.2 | test_gallery_present_after_load | PASS | |
| 5.3 | test_first_thumbnail_visible | PASS | |
| 6.1 | test_hover_shows_video | PASS | |
| 6.2 | test_video_hidden_before_hover | **FAIL** | Video already visible before hover — always-on rendering |
| 7.1 | test_click_card_no_navigation | PASS | |
| 8.1 | test_firefox_heading_and_cards | **FAIL** | Heading not visible — MWPW-199812 |
| 8.2 | test_webkit_heading_and_cards | **FAIL** | Heading not visible — MWPW-199812 |
| 9.1 | test_portrait_375x812 | PASS | |
| 9.2 | test_landscape_812x375 | PASS | |
| 9.3 | test_heading_visible_on_mobile | **FAIL** | Heading not visible on mobile — MWPW-199812 |
| 10.1 | test_stock_api_called | PASS | |
| 10.2 | test_stock_api_2xx_response | PASS | |
| 10.3 | test_stage_calls_stage_endpoint_only | PASS | |

---

## Failure Analysis

### Category A — Known Bugs (already filed in Jira)

**Heading not visible — locale modal race condition** (5 tests)
- `test_heading_visible` (Chromium) — blocked by `.modal-curtain.is-open`
- `test_heading_text_non_empty` — h2 times out (30s) because heading not in DOM
- `test_firefox_heading_and_cards` (Firefox) — MWPW-199812
- `test_webkit_heading_and_cards` (WebKit) — MWPW-199812
- `test_heading_visible_on_mobile` (Mobile portrait) — MWPW-199812

**Root cause:** The `.modal-curtain.is-open` overlay is not fully dismissed before the heading
assertion runs. Even after `curtain.click()`, the CSS transition takes longer than 5s on some runs.

**Jira bugs:** MWPW-199809 (@ui) · MWPW-199812 (@smoke/@bdd)

---

### Category B — New Findings (investigation needed)

#### Finding B1: H2 heading not inside `.prm-yt-gallery` container
**Test:** `test_single_h2_in_gallery` (1.3)
**Error:** `Expected exactly 1 H2 inside .prm-yt-gallery, found 0`
**Analysis:** The selector `.prm-yt-gallery h2` returns 0 elements. Either:
- The heading `h2.heading-xl` is a sibling of `.prm-yt-gallery`, not a child
- The gallery block has a different outer class name
**Action:** Inspect actual DOM structure. Update locator `HEADING_IN_GALLERY` if needed.
**Status:** Under investigation — may be a locator issue, not a product bug.

#### Finding B2: Card label selector `.pre-yt-card-label` matches no text
**Test:** `test_card_labels_non_empty` (3.2)
**Error:** All 15 cards at index [0–14] have empty label text
**Analysis:** `.pre-yt-card-label` is present in DOM but `text_content()` returns empty.
The actual label text may be in a child element, or the CSS class name is different.
**Action:** Inspect a card's DOM to find the correct label selector.
**Status:** Under investigation — likely a locator mismatch.

#### Finding B3: Video element visible before hover
**Test:** `test_video_hidden_before_hover` (6.2)
**Error:** `Video is already visible before any hover — expected hidden state`
**Analysis:** The `.video-wrapper video` is rendered visible in the DOM from page load.
The hover effect may use opacity/transform animation rather than `display:none`.
**Action:** Verify if the video is actually _playing_ before hover (not just visible).
If the video is always rendered but starts playing only on hover, the test expectation
needs to be updated — check for `paused` attribute instead of visibility.
**Status:** Test expectation may need refinement — not a product bug.

---

### Category C — XPASS (unexpected pass)

#### Finding C1: Meta description now present (MWPW-199810)
**Test:** `test_meta_description_present` (4.2) marked `@xfail`
**Result:** XPASS — meta description tag IS present with non-empty content
**Analysis:** Bug MWPW-199810 may have been fixed since it was filed.
**Action:** Verify MWPW-199810 and close/resolve if confirmed fixed. Remove `@xfail` marker from test 4.2.

---

## Known Bugs Summary

| Bug | Summary | Status |
|---|---|---|
| MWPW-199809 | Heading not visible — locale modal overlay (@ui) | Open |
| MWPW-199810 | Meta description missing on AEM Live staging | **Possibly Fixed** (XPASS) |
| MWPW-199812 | Heading not visible across all browsers (@smoke/@bdd) | Open |
| **MWPW-199900** | H2 heading not inside .prm-yt-gallery container | **New — Open** |
| **MWPW-199901** | Card label text empty on all 15 cards (.pre-yt-card-label) | **New — Open** |
| **MWPW-199902** | Video visible before hover — always-on rendering | **New — Open** |

---

## Reports

- HTML Report: [reports/report.html](reports/report.html)
- Allure Report: [reports/allure-report/index.html](reports/allure-report/index.html)
- Allure Results: `reports/allure-results/`
