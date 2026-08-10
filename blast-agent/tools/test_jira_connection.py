"""
Phase 2 (Link) — verify Jira API connection before building full logic.
Run: python tools/test_jira_connection.py
"""
import os
import sys
import ssl
import truststore
truststore.inject_into_ssl()  # use Windows cert store — trusts Adobe corporate CA

from pathlib import Path

# Load .env from blast-agent root
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

def test_connection():
    url = os.getenv("JIRA_URL")
    token = os.getenv("JIRA_TOKEN")

    if not url:
        print("FAIL: JIRA_URL not set in .env")
        return False
    if not token:
        print("FAIL: JIRA_TOKEN not set in .env")
        return False

    print(f"Connecting to {url} ...")

    try:
        from jira import JIRA
        jira = JIRA(server=url, token_auth=token)
        user = jira.myself()
        print(f"OK  : Connected as '{user['displayName']}' ({user.get('emailAddress', 'n/a')})")
        return True
    except Exception as e:
        print(f"FAIL: {e}")
        return False

if __name__ == "__main__":
    ok = test_connection()
    sys.exit(0 if ok else 1)
