#!/usr/bin/env bash
set -euo pipefail

OWNER="ShalvaLekishvili"
REPO="SentinelForge"
PROJECT_TITLE="SentinelForge — Development Roadmap"

echo "[1/5] Checking GitHub CLI authentication"
gh auth status

echo "[2/5] Requesting GitHub Projects token scope"
gh auth refresh -s project

echo "[3/5] Creating repository if needed"
if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$OWNER/$REPO" --public --source=. --remote=origin --push --description "Open-source SOC investigation and detection engineering workbench."
else
  echo "Repository already exists: $OWNER/$REPO"
fi

echo "[4/5] Creating GitHub Project"
PROJECT_JSON=$(gh project create --owner "$OWNER" --title "$PROJECT_TITLE" --format json)
PROJECT_NUMBER=$(printf '%s' "$PROJECT_JSON" | python -c 'import json,sys; print(json.load(sys.stdin)["number"])')
gh project link "$PROJECT_NUMBER" --owner "$OWNER" --repo "$REPO"

gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Priority" --data-type SINGLE_SELECT --single-select-options "Critical,High,Medium,Low"
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Component" --data-type SINGLE_SELECT --single-select-options "Backend,Frontend,Detection,Parser,Reporting,DevOps"
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Release" --data-type SINGLE_SELECT --single-select-options "v0.1,v0.2,v0.5,v1.0"
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Start Date" --data-type DATE
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Target Date" --data-type DATE

echo "[5/5] Creating initial project draft items"
while IFS= read -r title; do
  [[ -z "$title" ]] && continue
  gh project item-create "$PROJECT_NUMBER" --owner "$OWNER" --title "$title" >/dev/null
done <<'EOF'
SF-001 Publish v0.1.0 MVP dashboard
SF-002 Add YAML detection rule loader
SF-003 Add Windows EVTX parser
SF-004 Add Sysmon event normalizer
SF-005 Build process-tree reconstruction
SF-006 Add MITRE ATT&CK metadata catalog
SF-007 Add investigation case persistence
SF-008 Generate HTML incident report
SF-009 Generate PDF incident report
SF-010 Add Wazuh alert JSON adapter
SF-011 Add dashboard filters and search
SF-012 Prepare v1.0 stable release
EOF

echo "Done. Project #$PROJECT_NUMBER is linked to $OWNER/$REPO."
