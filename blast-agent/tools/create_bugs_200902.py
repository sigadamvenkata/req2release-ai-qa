"""
Create Jira bugs for findings discovered while automating MWPW-200902.
Reads credentials from .env — never hardcoded.
"""
import os
import re
import json
import truststore
truststore.inject_into_ssl()

from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA

load_dotenv(Path(__file__).parent.parent / ".env")

JIRA_URL = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_TOKEN = os.getenv("JIRA_TOKEN", "")
JIRA_PROJECT_RAW = os.getenv("JIRA_PROJECT", "MWPW")
ASSIGNEE = os.getenv("JIRA_AssignTo", "")
DEFAULT_PRIORITY = os.getenv("JIRA_Priority", "Major")

match = re.search(r'\((\w+)\)', JIRA_PROJECT_RAW)
PROJECT_KEY = match.group(1) if match else JIRA_PROJECT_RAW.strip()

PARENT_TICKET = "MWPW-200902"

BUGS = [
    {
        "finding": "F-001",
        "summary": "[Background Generator] Firefly mnemonic/wordmark branding missing from marquee content",
        "priority": DEFAULT_PRIORITY,
        "description": (
            "h3. Summary\n"
            "The ticket requires the unity block's marquee heading to display "
            "\"Adobe Firefly AI background generator: Transform photos in a click\" "
            "*with product mnemonic*. As of this test run, {{.upload-marquee-content}} "
            "on the staging page contains only the H1 and subheading — the Firefly "
            "mnemonic image ({{firefly.svg}}) and the \"Adobe Firefly\" wordmark text "
            "that previously appeared above the heading are no longer present in the DOM.\n\n"
            "h3. Steps to Reproduce\n"
            "# Open https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html\n"
            "# Dismiss the locale modal if present\n"
            "# Inspect {{.upload-marquee-content}} in the marquee's left column\n\n"
            "h3. Expected Result\n"
            "The marquee content should include the Firefly mnemonic image and the "
            "\"Adobe Firefly\" wordmark above the H1 heading, per the ticket's UI requirement: "
            "\"unity block has valid firefly heading ... with product mnemonic.\"\n\n"
            "h3. Actual Result\n"
            "{code:html}\n"
            "<div class=\"upload-marquee-content\">\n"
            "  <h1 id=\"ai-background-generator-transform-photos-in-a-click\">AI background generator: Transform photos in a click.</h1>\n"
            "  <p>From a busy street scene to an alien planet, effortlessly create high-quality, detailed background settings for any image.</p>\n"
            "</div>\n"
            "{code}\n"
            "No {{img[src*='firefly.svg']}} element and no \"Adobe Firefly\" text node are present "
            "anywhere in the marquee content block. The H1 text itself also does not include "
            "\"Adobe Firefly\" — so there is currently no Firefly branding/mnemonic visible "
            "anywhere in the marquee.\n\n"
            "h3. Environment\n"
            "* Page: https://www.stage.adobe.com/creativecloud/animation/testdoc/background-generator.html\n"
            "* Browser: Chromium (headless), 1440x900\n"
            "* Automated test: Python + Playwright — "
            "{{firefly-remove-background/specs/test_01_marquee_branding.py::test_mnemonic_and_wordmark_visible}}\n\n"
            "h3. Note\n"
            "An earlier pass of this same automation (same day) observed the mnemonic image and "
            "\"Adobe Firefly\" wordmark present in {{.upload-marquee-content}}, just structured as a "
            "separate paragraph from the H1. Between that check and this one, the paragraph appears "
            "to have been removed from the authored content — recommend confirming with content authoring "
            "whether this was an intentional edit or a regression.\n\n"
            f"h3. Linked Ticket\n[{PARENT_TICKET}]"
        ),
        "labels": ["automation", "content", "branding", "marquee"],
    },
]


def connect():
    if not JIRA_URL or not JIRA_TOKEN:
        raise ValueError("JIRA_URL and JIRA_TOKEN must be set in .env")
    return JIRA(server=JIRA_URL, token_auth=JIRA_TOKEN)


def resolve_assignee(jira: JIRA, display_name: str):
    try:
        users = jira.search_users(display_name)
        for u in users:
            if display_name.lower() in u.displayName.lower():
                return getattr(u, "name", None) or getattr(u, "accountId", None)
    except Exception:
        pass
    return None


def create_bug(jira: JIRA, bug: dict, assignee_key, screenshot_path: Path | None) -> str:
    fields = {
        "project": {"key": PROJECT_KEY},
        "issuetype": {"name": "Bug"},
        "summary": bug["summary"],
        "description": bug["description"],
        "priority": {"name": bug["priority"]},
        "labels": bug["labels"],
        "components": [{"id": "272118"}],       # unity-firefly-widget
        "customfield_12900": {"id": "34413"},  # Team = Brahmos (matches parent)
        "customfield_14101": {"id": "12534"},  # Method Found = Testing - Automation
    }
    if assignee_key:
        fields["assignee"] = {"name": assignee_key}

    issue = jira.create_issue(fields=fields)

    if screenshot_path and screenshot_path.exists():
        try:
            jira.add_attachment(issue=issue, attachment=str(screenshot_path))
        except Exception as e:
            print(f"  [warn] Could not attach screenshot: {e}")

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

    screenshot_path = Path(__file__).parent.parent / ".tmp" / "evidence_marquee.png"

    results = []
    for bug in BUGS:
        print(f"Creating [{bug['finding']}] {bug['summary'][:70]}...")
        try:
            key = create_bug(jira, bug, assignee_key, screenshot_path)
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

    out = Path(__file__).parent.parent / "output" / "bug_report_results_200902.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved -> {out}")


if __name__ == "__main__":
    main()
