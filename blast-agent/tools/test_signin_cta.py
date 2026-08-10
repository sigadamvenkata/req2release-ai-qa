"""
Test: Verify that the Sign In CTA exists on adobe.com
Usage: python tools/test_signin_cta.py
"""
import asyncio
import sys
from playwright.async_api import async_playwright

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding="utf-8")

URL = "https://www.adobe.com"

# Adobe GNAV-specific selectors (Milo/Franklin/FEDS framework)
SELECTORS = [
    ".feds-signIn",
    "[class*='feds-signIn']",
    "a[href*='ims-na1.adobelogin.com']",
    "a[href*='adobeid']",
    "a[data-id='feds-profile']",
    "[class*='profile-toggle']",
    "a[daa-ll*='sign-in' i]",
    "a[data-analytics-link-name*='sign in' i]",
    "a[aria-label*='Sign In' i]",
    "button[aria-label*='Sign In' i]",
    "a:has-text('Sign In')",
    "a:has-text('Sign in')",
    "a:has-text('Log in')",
]


async def test_signin_cta():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )

        print(f"Opening {URL} ...")
        await page.goto(URL, wait_until="domcontentloaded", timeout=30000)

        # Wait for the Adobe GNAV header to hydrate
        try:
            await page.wait_for_selector("header, nav, [class*='gnav'], [class*='feds']", timeout=10000)
            print("NAV element detected — waiting 2s for JS hydration ...")
            await page.wait_for_timeout(2000)
        except Exception:
            print("NAV selector not found within 10s, continuing anyway ...")

        title = await page.title()
        print(f"Page title : {title}")
        print()

        # Check targeted selectors
        found = []
        for sel in SELECTORS:
            try:
                count = await page.locator(sel).count()
                if count > 0:
                    el      = page.locator(sel).first
                    text    = (await el.inner_text()).strip()
                    href    = await el.get_attribute("href") or ""
                    visible = await el.is_visible()
                    found.append({
                        "selector": sel,
                        "text":     text,
                        "href":     href,
                        "visible":  visible,
                    })
            except Exception:
                pass

        # Broad fallback: scan all <a> tags for sign-in keywords
        all_links = await page.eval_on_selector_all(
            "a",
            "els => els.map(e => ({text: e.innerText.trim(), href: e.href, visible: e.offsetParent !== null}))"
        )
        signin_links = [
            l for l in all_links
            if any(kw in l["text"].lower() for kw in ["sign in", "sign-in", "log in", "login"])
            and l["text"].strip()
        ]

        # Debug: show first 30 links on page
        print("First 20 links found on page (debug):")
        for l in all_links[:20]:
            print(f"  [{'+' if l['visible'] else '-'}] \"{l['text'][:60]}\" -> {l['href'][:80]}")
        print()

        await browser.close()

        # ── Report ──────────────────────────────────────────────
        print("=" * 55)
        print("TEST: Sign In CTA exists on adobe.com")
        print("=" * 55)

        if found or signin_links:
            print("RESULT : PASS  -- Sign In CTA EXISTS on adobe.com")
            print()
            if found:
                print("Matched via targeted selectors:")
                for f in found:
                    status = "VISIBLE" if f["visible"] else "HIDDEN"
                    print(f"  [{status}]  text=\"{f['text']}\"")
                    print(f"            selector : {f['selector']}")
                    print(f"            href     : {f['href']}")
                    print()
            if signin_links:
                print("Sign-in links found via full-page scan:")
                for l in signin_links:
                    status = "visible" if l["visible"] else "hidden"
                    print(f"  [{status}]  \"{l['text']}\"  ->  {l['href']}")
        else:
            print("RESULT : FAIL  -- Sign In CTA NOT FOUND on adobe.com")

        print("=" * 55)


if __name__ == "__main__":
    asyncio.run(test_signin_cta())
