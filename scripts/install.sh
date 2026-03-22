#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$ROOT_DIR/.github/templates/alphapatch.yml"
WORKFLOW_DIR="$ROOT_DIR/.github/workflows"
WORKFLOW_FILE="$WORKFLOW_DIR/alphapatch.yml"

if [[ ! -f "$TEMPLATE" ]]; then
  echo "Template not found: $TEMPLATE"
  exit 1
fi

mkdir -p "$WORKFLOW_DIR"

if [[ -f "$WORKFLOW_FILE" ]]; then
  echo "Workflow already exists: $WORKFLOW_FILE"
  echo "If you want to overwrite it, delete the file and re-run this script."
  exit 0
fi

cp "$TEMPLATE" "$WORKFLOW_FILE"

echo "Installed workflow to $WORKFLOW_FILE"

echo "Next steps:"

echo "1. Add repo secrets for your provider (e.g., GEMINI_API_KEY, GEMINI_MODEL)."

echo "2. Ensure Actions permissions allow PR creation."

echo "3. Open a new issue to trigger AlphaPatch."
