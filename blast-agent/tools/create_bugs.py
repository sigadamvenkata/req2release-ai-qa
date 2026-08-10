"""
Create Jira bugs for all findings discovered during MWPW-199605 automation.
Reads credentials from .env — never hardcoded.
"""
import os
import json
import truststore
truststore.inject_into_ssl()

from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA

load_dotenv(Path(__file__).parent.parent / ".env")

JIRA_URL   = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_TOKEN = os.getenv("JIRA_TOKEN", "")
JIRA_PROJECT_RAW = os.getenv("JIRA_PROJECT", "MWPW")
ASSIGNEE   = os.getenv("JIRA_AssignTo", "")

# Extract project key from "MWP Web (MWPW)" → "MWPW"
import re
match = re.search(r'\((\w+)\)', JIRA_PROJECT_RAW)
PROJECT_KEY = match.group(1) if match else JIRA_PROJECT_RAW.strip()

PARENT_TICKET = "MWPW-199605"

# ── Bug definitions ──────────────────────────────────────────────────────────

BUGS = [
    {
        "finding": "F-001",
        "summary": "[Remove Background] UNAV Sign In & Accordion buttons have pointer-events:none during JS init — blocks user interaction",
        "priority": "Normal",
        "description": (
            "h3. Summary\n"
            "The Adobe UNAV Sign In button and Milo accordion triggers have {{pointer-events: none}} applied while their "
            "JavaScript event handlers are being registered during page initialisation.\n\n"
            "h3. Steps to Reproduce\n"
            "# Open https://www.adobe.com/products/firefly/features/remove-background.html\n"
            "# Immediately click the Sign In button in the global navigation before JS has fully initialised\n"
            "# Repeat for any accordion item in the FAQ section\n\n"
            "h3. Expected Result\n"
            "Buttons are clickable or display a loading indicator while JS initialises. "
            "Pointer events should be disabled only for decorative / truly non-interactive elements.\n\n"
            "h3. Actual Result\n"
            "Buttons are unclickable ({{pointer-events: none}}) during a JS initialisation window. "
            "Automated testing with Playwright fails with 'element is not enabled'. "
            "Real users on slow connections may experience the same dead-click behaviour.\n\n"
            "h3. Environment\n"
            "* Browsers: Chromium, Firefox, WebKit\n"
            "* Automated test: Python + Playwright (headless)\n\n"
            "h3. Workaround\n"
            "Playwright workaround: {{page.evaluate(\"el.click()\")}} — native JS DOM click bypasses Playwright's actionability check. "
            "Root fix: ensure buttons remain interactable (or show a spinner) before handlers are attached.\n\n"
            f"h3. Linked Ticket\n[{PARENT_TICKET}]"
        ),
        "labels": ["automation", "accessibility", "unav", "accordion"],
    },
    {
        "finding": "F-002",
        "summary": "[Remove Background] Reupload button (ia-reupload-btn) not shown to unauthenticated users after image upload",
        "priority": "Minor",
        "description": (
            "h3. Summary\n"
            "After uploading a valid image (JPG/PNG), the reupload button ({{button.ia-reupload-btn}}) never appears "
            "for unauthenticated users. The AI background-removal processing requires an active Adobe account session.\n\n"
            "h3. Steps to Reproduce\n"
            "# Open https://www.adobe.com/products/firefly/features/remove-background.html without signing in\n"
            "# Upload a valid JPG or PNG image\n"
            "# Observe what happens after the upload completes\n\n"
            "h3. Expected Result\n"
            "Page should clearly prompt the user to sign in to process the image, "
            "OR show the reupload button with a sign-in gate.\n\n"
            "h3. Actual Result\n"
            "No reupload button appears and no clear message is shown indicating that sign-in is required "
            "to proceed with background removal. UX is ambiguous — user does not know why nothing happens.\n\n"
            "h3. Environment\n"
            "* Browsers: Chromium, Firefox, WebKit\n"
            "* User state: unauthenticated (no Adobe IMS session)\n\n"
            "h3. Recommendation\n"
            "Show a sign-in prompt or a tooltip on the reupload button explaining that "
            "an Adobe account is required to process images.\n\n"
            f"h3. Linked Ticket\n[{PARENT_TICKET}]"
        ),
        "labels": ["automation", "ux", "authentication"],
    },
    {
        "finding": "F-003",
        "summary": "[Remove Background] Animated WebP upload returns server validation error on WebKit/Safari — real user impact",
        "priority": "Major",
        "description": (
            "h3. Summary\n"
            "Uploading an animated WebP file on WebKit (Safari) triggers a server-side validation error. "
            "The same file uploads successfully on Chromium and Firefox. This is a cross-browser inconsistency "
            "with direct user impact on Safari.\n\n"
            "h3. Steps to Reproduce\n"
            "# Open https://www.adobe.com/products/firefly/features/remove-background.html in Safari (WebKit)\n"
            "# Prepare an animated WebP file (e.g. a converted animated GIF)\n"
            "# Upload the file using the drop zone or file picker\n\n"
            "h3. Expected Result\n"
            "* *If animated WebP is unsupported:* Show a friendly error message: "
            "'Animated WebP files are not supported. Please upload a static image.'\n"
            "* *If animated WebP should be supported:* Process the first frame and remove background successfully.\n\n"
            "h3. Actual Result\n"
            "Server returns a validation error for the upload. WebKit sends a different MIME type for animated WebP "
            "than Chromium/Firefox, causing the server to reject the file without a user-friendly message.\n\n"
            "h3. Environment\n"
            "* Browser: WebKit (Safari engine) — does NOT reproduce on Chromium or Firefox\n"
            "* File type: Animated WebP (MIME: image/webp with animation data)\n\n"
            "h3. Impact\n"
            "All Safari users who upload animated WebP files will encounter this error silently. "
            "Animated WebP is common output from tools like GIPHY, Lottie exports, and WhatsApp stickers.\n\n"
            "h3. Recommendation\n"
            "# Normalise MIME type handling server-side — accept all WebP variants uniformly.\n"
            "# If animated WebP is intentionally unsupported, detect it client-side and show a clear error before upload.\n\n"
            f"h3. Linked Ticket\n[{PARENT_TICKET}]"
        ),
        "labels": ["automation", "safari", "webkit", "webp", "file-upload", "cross-browser"],
    },
    {
        "finding": "F-004",
        "summary": "[Remove Background] Firefly CTA in global navigation is slow to appear on WebKit/Safari (>3s render delay)",
        "priority": "Minor",
        "description": (
            "h3. Summary\n"
            "The 'Go to Firefly' CTA link ({{a.feds-cta.feds-cta--secondary}}) in the FEDS global navigation "
            "takes more than 3 seconds to become visible on WebKit. Chromium and Firefox render it within ~1–2 seconds.\n\n"
            "h3. Steps to Reproduce\n"
            "# Open https://www.adobe.com/products/firefly/features/remove-background.html in Safari\n"
            "# Observe the global navigation bar — time how long the Firefly CTA takes to appear\n\n"
            "h3. Expected Result\n"
            "Navigation CTAs render within 2 seconds on all browsers including Safari.\n\n"
            "h3. Actual Result\n"
            "On WebKit, the CTA takes 3–8 seconds to become visible. "
            "During this window, the CTA is absent — users may think it is missing.\n\n"
            "h3. Environment\n"
            "* Browser: WebKit (Safari engine)\n"
            "* Network: Standard broadband\n\n"
            "h3. Recommendation\n"
            "Profile FEDS nav initialisation on Safari. "
            "Consider SSR or skeleton rendering for nav CTAs to avoid blank nav on slow-starting JS engines.\n\n"
            f"h3. Linked Ticket\n[{PARENT_TICKET}]"
        ),
        "labels": ["automation", "performance", "safari", "webkit", "navigation"],
    },
    {
        "finding": "F-005",
        "summary": "[Remove Background] Sign In button click does not trigger IMS navigation on WebKit/Safari in automated testing",
        "priority": "Normal",
        "description": (
            "h3. Summary\n"
            "Clicking the Sign In button via native JS {{.click()}} fires the event handler, but IMS redirect "
            "(to {{account.adobe.com}} or {{adobeid}} login) does not trigger on WebKit in headless automated tests. "
            "The page stays on {{remove-background.html}}.\n\n"
            "h3. Steps to Reproduce\n"
            "# Open https://www.adobe.com/products/firefly/features/remove-background.html\n"
            "# Click the Sign In button in the global nav\n"
            "# Observe whether the page navigates to the Adobe IMS login page\n\n"
            "h3. Expected Result\n"
            "Clicking Sign In redirects to {{account.adobe.com}} or Adobe IMS login within 5 seconds on all browsers.\n\n"
            "h3. Actual Result\n"
            "In Playwright headless mode, the click does not trigger IMS navigation on any browser. "
            "This may indicate the IMS redirect relies on a popup window or browser session cookies "
            "that are unavailable in a clean headless context.\n\n"
            "h3. Environment\n"
            "* Browsers: Chromium, Firefox, WebKit (headless)\n"
            "* Test framework: Python + Playwright\n\n"
            "h3. Note\n"
            "This may be a test-environment limitation (clean session, no cookies) rather than a page bug. "
            "Manual verification in a real browser is recommended to confirm expected IMS redirect behaviour.\n\n"
            f"h3. Linked Ticket\n[{PARENT_TICKET}]"
        ),
        "labels": ["automation", "authentication", "ims", "sign-in"],
    },
    {
        "finding": "F-006",
        "summary": "[Remove Background] Milo accordion expand/collapse fails Playwright actionability check — potential accessibility concern",
        "priority": "Minor",
        "description": (
            "h3. Summary\n"
            "The Milo accordion buttons ({{button.accordion-trigger}}) on the Remove Background page report "
            "'element is not enabled' in Playwright's actionability check, even when the buttons are visually rendered "
            "and DOM-present.\n\n"
            "h3. Steps to Reproduce\n"
            "# Open https://www.adobe.com/products/firefly/features/remove-background.html\n"
            "# Scroll to the FAQ / How To section\n"
            "# Click any accordion trigger button\n\n"
            "h3. Expected Result\n"
            "Accordion expands — {{aria-expanded}} changes from {{false}} to {{true}}. "
            "Button should be fully interactable (no {{pointer-events: none}}, no {{disabled}} attribute).\n\n"
            "h3. Actual Result\n"
            "Playwright reports the button as 'not enabled'. Native JS {{el.click()}} works as a workaround, "
            "confirming the button is DOM-present and event-handlers are attached — "
            "but Playwright's enabled-state check (which checks ARIA + CSS) reports it as disabled.\n\n"
            "h3. Accessibility Impact\n"
            "If the button fails Playwright's enabled check, it may also fail assistive technology checks "
            "(screen readers) that rely on the same ARIA / CSS cues. "
            "Recommend running an axe-core audit on the accordion component.\n\n"
            "h3. Environment\n"
            "* Browsers: Chromium, Firefox, WebKit\n\n"
            "h3. Recommendation\n"
            "Audit the Milo accordion component for correct ARIA roles and states. "
            "Ensure {{aria-disabled}} and {{disabled}} attributes are not erroneously set during JS init.\n\n"
            f"h3. Linked Ticket\n[{PARENT_TICKET}]"
        ),
        "labels": ["automation", "accessibility", "accordion", "aria"],
    },
]

# ── Jira connection ──────────────────────────────────────────────────────────

def connect():
    if not JIRA_URL or not JIRA_TOKEN:
        raise ValueError("JIRA_URL and JIRA_TOKEN must be set in .env")
    return JIRA(server=JIRA_URL, token_auth=JIRA_TOKEN)


def resolve_assignee(jira: JIRA, display_name: str):
    """Search for user by display name and return their accountId / key."""
    try:
        users = jira.search_users(display_name)
        for u in users:
            if display_name.lower() in u.displayName.lower():
                # Jira Server uses 'name' (username); Jira Cloud uses 'accountId'
                return getattr(u, "name", None) or getattr(u, "accountId", None)
    except Exception:
        pass
    return None


def create_bug(jira: JIRA, bug: dict, assignee_key: str | None) -> str:
    fields = {
        "project":            {"key": PROJECT_KEY},
        "issuetype":          {"name": "Bug"},
        "summary":            bug["summary"],
        "description":        bug["description"],
        "priority":           {"name": bug["priority"]},
        "labels":             bug["labels"],
        # Mandatory MWPW custom fields — values copied from parent ticket MWPW-199605
        "components":         [{"id": "68446"}],          # "None" component (same as parent)
        "customfield_12900":  {"id": "34413"},             # Team = Brahmos
        "customfield_14101":  {"id": "12534"},             # Method Found = Testing - Automation
    }
    if assignee_key:
        fields["assignee"] = {"name": assignee_key}

    issue = jira.create_issue(fields=fields)

    # Link to parent MWPW-199605
    try:
        jira.create_issue_link(
            type="relates to",
            inwardIssue=issue.key,
            outwardIssue=PARENT_TICKET,
        )
    except Exception as e:
        print(f"  [warn] Could not link to {PARENT_TICKET}: {e}")

    return issue.key


def main():
    print(f"Connecting to {JIRA_URL} ...")
    jira = connect()
    print(f"Connected. Project: {PROJECT_KEY}\n")

    assignee_key = resolve_assignee(jira, ASSIGNEE)
    if assignee_key:
        print(f"Assignee resolved: '{ASSIGNEE}' -> {assignee_key}\n")
    else:
        print(f"[warn] Could not resolve assignee '{ASSIGNEE}' -- bugs will be unassigned.\n")

    results = []
    for bug in BUGS:
        print(f"Creating [{bug['finding']}] {bug['summary'][:70]}…")
        try:
            key = create_bug(jira, bug, assignee_key)
            results.append({"finding": bug["finding"], "key": key, "status": "created"})
            print(f"  -> {key}\n")
        except Exception as e:
            results.append({"finding": bug["finding"], "key": None, "status": f"ERROR: {e}"})
            print(f"  -> FAILED: {e}\n")

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for r in results:
        status = r["key"] if r["key"] else r["status"]
        print(f"  {r['finding']}: {status}")

    # Write results to file for reference
    out = Path(__file__).parent.parent / "output" / "bug_report_results.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved -> {out}")


if __name__ == "__main__":
    main()
