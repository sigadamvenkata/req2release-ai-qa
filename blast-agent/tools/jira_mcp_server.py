"""
Jira MCP Server — exposes Jira ticket data to Claude Code.

Tools:
  fetch_jira_ticket        — fetches all text fields + attachment metadata
  download_jira_attachment — downloads one image attachment (Claude sees it visually)
  save_test_artifacts      — writes test_plan.md + test_cases.md to output/

Usage (Claude Code registers this via .claude/settings.json):
  python tools/jira_mcp_server.py
"""
import os
import ssl
import json
import time
import requests
import truststore
truststore.inject_into_ssl()  # use Windows cert store — trusts Adobe corporate CA

from pathlib import Path
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Image

load_dotenv(Path(__file__).parent.parent / ".env")

JIRA_URL  = os.getenv("JIRA_URL", "").rstrip("/")
JIRA_TOKEN = os.getenv("JIRA_TOKEN", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")

mcp = FastMCP("jira-test-agent")

IMAGE_MIME_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"}


def _jira_client():
    from jira import JIRA
    if not JIRA_URL or not JIRA_TOKEN:
        raise ValueError("JIRA_URL and JIRA_TOKEN must be set in .env")
    return JIRA(server=JIRA_URL, token_auth=JIRA_TOKEN)


def _notify_slack(ticket_id: str, plan_path: Path, cases_path: Path) -> str | None:
    """
    Post a completion message to the #vector-notifications Slack channel via
    an Incoming Webhook. Returns an error string on failure, None on success
    (or when SLACK_WEBHOOK_URL is unset — Slack notifications are optional).
    """
    if not SLACK_WEBHOOK_URL:
        return None

    message = {
        "text": (
            f":white_check_mark: Test plan + test cases generated for *{ticket_id}*\n"
            f"• `{plan_path.name}`\n"
            f"• `{cases_path.name}`"
        )
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return str(e)

    return None


@mcp.tool()
def fetch_jira_ticket(ticket_id: str) -> str:
    """
    Fetch all details of a Jira ticket: summary, description, status, priority,
    assignee, reporter, labels, components, comments, and attachment metadata.

    Call this first to get full context before generating a test plan.

    Args:
        ticket_id: Jira ticket ID, e.g. "PROJ-1234"

    Returns:
        JSON string with all ticket details. Attachments list includes
        filename, mime_type, and url — pass image urls to download_jira_attachment.
    """
    jira = _jira_client()

    try:
        issue = jira.issue(ticket_id, expand="comments,attachment")
    except Exception as e:
        raise ValueError(f"Could not fetch ticket '{ticket_id}': {e}")

    f = issue.fields

    comments = [
        {
            "author":  c.author.displayName,
            "created": c.created,
            "body":    c.body,
        }
        for c in (f.comment.comments if f.comment else [])
    ]

    attachments = [
        {
            "filename":  a.filename,
            "mime_type": a.mimeType,
            "url":       a.content,
            "is_image":  a.mimeType in IMAGE_MIME_TYPES,
        }
        for a in (f.attachment if f.attachment else [])
    ]

    payload = {
        "ticket_id":   ticket_id,
        "summary":     f.summary or "",
        "description": f.description or "",
        "status":      f.status.name if f.status else "Unknown",
        "priority":    f.priority.name if f.priority else "None",
        "assignee":    f.assignee.displayName if f.assignee else "Unassigned",
        "reporter":    f.reporter.displayName if f.reporter else "Unknown",
        "labels":      list(f.labels) if f.labels else [],
        "components":  [c.name for c in f.components] if f.components else [],
        "comments":    comments,
        "attachments": attachments,
    }

    return json.dumps(payload, indent=2, ensure_ascii=False)


@mcp.tool()
def download_jira_attachment(ticket_id: str, filename: str, attachment_url: str) -> Image:
    """
    Download an image attachment from Jira and return it so Claude can see it visually.
    Only call this for attachments where is_image is true (from fetch_jira_ticket).

    Args:
        ticket_id:      Jira ticket ID (used to organise temp files)
        filename:       Attachment filename from fetch_jira_ticket
        attachment_url: Attachment URL from fetch_jira_ticket

    Returns:
        The image — Claude will see it inline.
    """
    headers = {"Authorization": f"Bearer {JIRA_TOKEN}"}

    tmp_dir = Path(__file__).parent.parent / ".tmp" / ticket_id
    tmp_dir.mkdir(parents=True, exist_ok=True)
    local_path = tmp_dir / filename

    response = requests.get(attachment_url, headers=headers, stream=True, timeout=30)
    response.raise_for_status()

    with open(local_path, "wb") as fh:
        for chunk in response.iter_content(chunk_size=8192):
            fh.write(chunk)

    return Image(path=str(local_path))


@mcp.tool()
def save_test_artifacts(ticket_id: str, test_plan: str, test_cases: str) -> str:
    """
    Save the generated test plan and BDD test cases to the output/ directory.
    Call this as the final step after generating both documents.

    Args:
        ticket_id:   Jira ticket ID — used as the filename prefix
        test_plan:   Full markdown content of the test plan
        test_cases:  Full markdown content of the BDD test cases

    Returns:
        JSON with the paths of both saved files.
    """
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)

    plan_path  = output_dir / f"{ticket_id}_test_plan.md"
    cases_path = output_dir / f"{ticket_id}_test_cases.md"

    if plan_path.exists():
        ts = int(time.time())
        plan_path  = output_dir / f"{ticket_id}_test_plan_{ts}.md"
        cases_path = output_dir / f"{ticket_id}_test_cases_{ts}.md"

    plan_path.write_text(test_plan, encoding="utf-8")
    cases_path.write_text(test_cases, encoding="utf-8")

    slack_error = _notify_slack(ticket_id, plan_path, cases_path)

    return json.dumps({
        "status":          "saved",
        "test_plan_path":  str(plan_path),
        "test_cases_path": str(cases_path),
        "slack_notified":  SLACK_WEBHOOK_URL != "" and slack_error is None,
        "slack_error":     slack_error,
    })


if __name__ == "__main__":
    mcp.run()
