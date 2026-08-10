# Framework Progress — tests-yt-bdd
**Ticket:** MWPW-199796 | **Suite:** tests-yt-bdd | **Last Updated:** 2026-07-03

---

## Framework Structure

```
tests-yt-bdd/
├── assets/                      ← Test images (corporate-magizine.png from desktop)
├── features/                    ← Gherkin .feature files (10 groups, documentation)
│   ├── 01_heading.feature
│   ├── 02_grid_layout.feature
│   ├── 03_card_metadata.feature
│   ├── 04_page_seo.feature
│   ├── 05_page_load.feature
│   ├── 06_hover_video.feature
│   ├── 07_no_navigation.feature
│   ├── 08_cross_browser.feature
│   ├── 09_mobile.feature
│   └── 10_stock_api.feature
├── locators/
│   └── gallery_locators.py      ← All CSS selectors + URLs (single source of truth)
├── pages/
│   ├── base_page.py             ← BasePage: navigate, dismiss_modal, common helpers
│   └── gallery_page.py          ← YouTubeGalleryPage: all gallery-specific methods
├── specs/                       ← pytest test files (one per feature group)
│   ├── test_01_heading.py       ← Group 1: 3 tests
│   ├── test_02_grid_layout.py   ← Group 2: 4 tests
│   ├── test_03_card_metadata.py ← Group 3: 5 tests
│   ├── test_04_page_seo.py      ← Group 4: 3 tests
│   ├── test_05_page_load.py     ← Group 5: 3 tests
│   ├── test_06_hover_video.py   ← Group 6: 2 tests
│   ├── test_07_no_navigation.py ← Group 7: 1 test
│   ├── test_08_cross_browser.py ← Group 8: 2 tests
│   ├── test_09_mobile.py        ← Group 9: 3 tests
│   └── test_10_stock_api.py     ← Group 10: 3 tests
├── conftest.py                  ← All browser fixtures + screenshot-on-fail hook
├── pytest.ini                   ← pytest config, marker definitions
├── PROGRESS.md                  ← This file
└── FINDINGS.md                  ← Bug findings and test results
```

---

## How to Run

```powershell
# From the tests-yt-bdd directory:
cd blast-agent/tests-yt-bdd

# Run all tests
python -m pytest

# Run only smoke tests
python -m pytest -m smoke

# Run only UI tests
python -m pytest -m ui

# Run specific group
python -m pytest specs/test_05_page_load.py -v

# Generate Allure report (after run)
npx allure generate --cwd . -o reports/allure-report --name "YT Gallery BDD" --clean
npx allure open reports/allure-report
```

---

## Fixture Map

| Fixture | Browser | Viewport | Nav | Modal |
|---|---|---|---|---|
| `gallery` | Chromium | 1440×900 | Yes | Dismissed |
| `gallery_no_hover` | Chromium | 1440×900 | Yes | Dismissed |
| `gallery_firefox` | Firefox | 1440×900 | Yes | Dismissed |
| `gallery_webkit` | WebKit | 1440×900 | Yes | Dismissed |
| `gallery_portrait` | Chromium | 375×812 | Yes | Dismissed |
| `gallery_landscape` | Chromium | 812×375 | Yes | Dismissed |
| `page_raw` | Chromium | 1440×900 | No | — |

---

## Page Object Methods

| Method | Purpose |
|---|---|
| `navigate()` | Open PAGE_URL, wait=networkidle |
| `dismiss_modal()` | Click .modal-curtain.is-open, fallback Escape |
| `is_heading_visible()` | Check h2.heading-xl visibility |
| `get_heading_text()` | Read heading text content |
| `count_h2_in_gallery()` | Count h2 inside .prm-yt-gallery |
| `is_grid_visible()` | Check .pre-yt-grid visibility |
| `get_card_count()` | Count .pre-yt-card elements |
| `get_grid_display_property()` | CSS display of grid container |
| `get_card_bounding_boxes()` | Width/height of all cards |
| `get_card_identifiers()` | id or data-id from cards |
| `get_card_labels()` | Text from .pre-yt-card-label |
| `get_free_tag_count()` | Count .pre-yt-free-tag |
| `get_thumbnail_srcs()` | src of all .image-wrapper img |
| `get_thumbnail_alts()` | alt of all .image-wrapper img |
| `is_first_thumbnail_visible()` | First thumbnail visibility |
| `get_meta_description()` | meta[name=description] content |
| `is_meta_desc_present()` | meta tag exists check |
| `is_gallery_in_main()` | .prm-yt-gallery inside <main> |
| `get_gallery_bounding_box()` | Gallery block bounding box |
| `hover_first_card()` | Hover over first .pre-yt-card |
| `is_video_visible_in_first_card()` | .video-wrapper video visible |
| `get_video_src_in_first_card()` | Video src attribute |
| `is_video_hidden_before_hover()` | Video hidden state (pre-hover) |
| `click_first_card()` | Click first card |
| `get_current_url()` | Current browser URL |
| `get_scroll_vs_inner_width()` | (scrollWidth, innerWidth) for overflow check |
| `get_page_title()` | document.title |
| `screenshot_bytes()` | PNG screenshot bytes |

---

## Test Run History

| Date | Total | Passed | Failed | xpassed | Notes |
|---|---|---|---|---|---|
| 2026-07-03 | 29 | 20 | 8 | 1 | See FINDINGS.md for breakdown |
