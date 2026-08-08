#!/usr/bin/env bash
set -euo pipefail

OWNER="ShalvaLekishvili"
REPO="SentinelForge"
PROJECT_TITLE="SentinelForge — Development Roadmap"

echo "[1/5] Checking GitHub CLI authentication"
gh auth status

echo "[2/5] Ensuring GitHub Projects scope"
gh auth refresh -s project

echo "[3/5] Checking repository"
if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$OWNER/$REPO" --public --source=. --remote=origin --push \
    --description "Defensive SOC investigation and detection engineering workbench."
else
  echo "Repository exists: $OWNER/$REPO"
fi

echo "[4/5] Creating GitHub Project"
PROJECT_JSON=$(gh project create --owner "$OWNER" --title "$PROJECT_TITLE" --format json)
PROJECT_NUMBER=$(printf '%s' "$PROJECT_JSON" | python -c 'import json,sys; print(json.load(sys.stdin)["number"])')
gh project link "$PROJECT_NUMBER" --owner "$OWNER" --repo "$REPO"

gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Priority" --data-type SINGLE_SELECT --single-select-options "P0,P1,P2,P3"
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Component" --data-type SINGLE_SELECT --single-select-options "API,Parser,Detection,Correlation,UI,Docs,DevOps"
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Release" --data-type SINGLE_SELECT --single-select-options "v0.2,v0.3,v0.5,v0.7,v1.0"
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Start Date" --data-type DATE
gh project field-create "$PROJECT_NUMBER" --owner "$OWNER" --name "Target Date" --data-type DATE

echo "[5/5] Seeding v0.3 roadmap items"
while IFS= read -r title; do
  [[ -z "$title" ]] && continue
  gh project item-create "$PROJECT_NUMBER" --owner "$OWNER" --title "$title" >/dev/null
done <<'EOF'
SF-101 Add logsource-aware rule pre-filtering
SF-102 Version the normalized event schema
SF-103 Add per-rule positive and negative fixtures
SF-104 Add investigation full-text search
SF-105 Add timeline filters by host, user and Event ID
SF-106 Add rule false-positive metadata
SF-107 Add richer Sysmon semantic helpers
SF-108 Add CI rule validation command
SF-201 Persist local investigation cases with SQLite
SF-205 Generate HTML investigation reports
SF-302 Evaluate optional Sigma validation/import
EOF

echo "Done. Project #$PROJECT_NUMBER is linked to $OWNER/$REPO."
