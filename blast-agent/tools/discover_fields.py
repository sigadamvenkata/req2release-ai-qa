"""
Discover required field values for MWPW Bug creation by reading the parent ticket.
Uses project_issue_fields API (Jira 10.x).
"""
import os, json
import truststore; truststore.inject_into_ssl()
from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA

load_dotenv(Path(__file__).parent.parent / ".env")
jira = JIRA(server=os.getenv("JIRA_URL"), token_auth=os.getenv("JIRA_TOKEN"))

PARENT = "MWPW-199605"

# Read the parent ticket — copy its component + custom field values
issue = jira.issue(PARENT)
f = issue.fields

print(f"=== Parent ticket: {PARENT} ===")
print(f"Components: {[c.name + ' (id=' + c.id + ')' for c in (f.components or [])]}")
print(f"customfield_12900 (Team): {getattr(f, 'customfield_12900', None)}")
print(f"customfield_14101 (Method Found): {getattr(f, 'customfield_14101', None)}")
print()

# Also try project_issue_fields for Bug to see allowed values
try:
    issue_types = jira.project_issue_types("MWPW")
    bug_type = next((it for it in issue_types if it.name == "Bug"), None)
    if bug_type:
        print(f"Bug issue type id: {bug_type.id}")
        fields_meta = jira.project_issue_fields("MWPW", bug_type.id)
        for fm in fields_meta:
            if fm.fieldId in ("customfield_12900", "customfield_14101", "components"):
                print(f"\nField: {fm.fieldId} - {fm.name}")
                avs = getattr(fm, "allowedValues", []) or []
                for v in list(avs)[:20]:
                    vid = getattr(v, "id", getattr(v, "accountId", ""))
                    vname = getattr(v, "name", getattr(v, "value", str(v)))
                    print(f"  id={vid}  name={vname}")
except Exception as e:
    print(f"project_issue_fields error: {e}")
