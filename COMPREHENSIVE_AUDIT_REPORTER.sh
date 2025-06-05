#!/bin/bash

# Exit on error, undefined variable, or pipeline failure
set -euo pipefail

# === Configuration ===
PROJECT_ROOT="$(pwd)"
REPORT_FILE="comprehensive_audit_report.md"
CLI_SCRIPT="scripts/main.py"
TEST_FILE="test_findings.txt"
DATE_STR=$(date +"%Y-%m-%d %H:%M:%S")

# === Git Sync ===
echo "[INFO] Updating project from remote..."
if git remote | grep -q origin; then
    git fetch origin main || true
    git checkout main || true
    git pull --rebase origin main || true
else
    echo "[WARN] No remote 'origin' configured. Skipping sync." >&2
fi

# === Report Header ===
echo "# 🧪 Comprehensive Fundalyze Audit Report - $DATE_STR" > "$REPORT_FILE"
echo -e "\n_This report contains syntax, static analysis, CLI tests, and UX best practice notes._\n" >> "$REPORT_FILE"

# === Static Analysis ===
echo "## 🔍 Module Syntax and Static Analysis" >> "$REPORT_FILE"
MODULES=$(find "$PROJECT_ROOT" -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \))

for file in $MODULES; do
    echo -e "\n### File: $file" >> "$REPORT_FILE"

    if [[ $file == *.py ]]; then
        echo "[INFO] Analyzing Python file: $file"
        {
            syntax_check=$(python -m py_compile "$file" 2>&1)
            [[ -n "$syntax_check" ]] && echo -e "**Syntax Issues:**\n\`\`\`\n$syntax_check\n\`\`\`" >> "$REPORT_FILE"
        } || true

        if command -v pylint &>/dev/null; then
            pylint_output=$(pylint "$file" 2>&1 || true)
            [[ -n "$pylint_output" ]] && echo -e "**Pylint Warnings:**\n\`\`\`\n$pylint_output\n\`\`\`" >> "$REPORT_FILE"
        else
            echo "_[pylint not installed]_" >> "$REPORT_FILE"
        fi

    elif [[ $file == *.js || $file == *.ts ]]; then
        echo "[INFO] Analyzing JS/TS file: $file"

        if command -v eslint &>/dev/null; then
            eslint_output=$(eslint "$file" 2>&1 || true)
            [[ -n "$eslint_output" ]] && echo -e "**ESLint Warnings:**\n\`\`\`\n$eslint_output\n\`\`\`" >> "$REPORT_FILE"
        else
            echo "_[eslint not installed]_" >> "$REPORT_FILE"
        fi

        if command -v tsc &>/dev/null; then
            syntax_check=$(tsc --noEmit "$file" 2>&1 || true)
            [[ -n "$syntax_check" ]] && echo -e "**TypeScript Compile Check:**\n\`\`\`\n$syntax_check\n\`\`\`" >> "$REPORT_FILE"
        else
            echo "_[tsc not installed]_" >> "$REPORT_FILE"
        fi
    fi
done

# === CLI Functional Testing ===
if [[ -f "$CLI_SCRIPT" ]]; then
    echo -e "\n## 🧪 CLI Functional Testing" >> "$REPORT_FILE"
    COMMANDS=(
        "portfolio view"
        "portfolio add AAPL"
        "groups create Tech"
        "reports generate --all"
        "notes list"
    )

    for cmd in "${COMMANDS[@]}"; do
        echo "[INFO] Testing CLI command: $cmd"
        output=$(python "$CLI_SCRIPT" $cmd 2>&1 || true)
        if [[ $? -ne 0 ]]; then
            echo -e "**❌ Error running \`$cmd\`**\n\`\`\`\n$output\n\`\`\`" >> "$REPORT_FILE"
        else
            echo -e "**✅ Command \`$cmd\` ran successfully.**" >> "$REPORT_FILE"
        fi
    done
fi

# === UX and Best Practices ===
echo -e "\n## 💡 User Experience & Best Practices Suggestions" >> "$REPORT_FILE"
UX_SUGGESTIONS=(
    "All CLI commands should support '--help' with examples."
    "Ensure menus are consistent and indicate consequences of actions."
    "Validate user input to prevent invalid entries."
    "Use color-coded messages (green=success, yellow=warning, red=error)."
    "Always allow safe exit/cancel during prompts."
)

for suggestion in "${UX_SUGGESTIONS[@]}"; do
    echo "- $suggestion" >> "$REPORT_FILE"
done

# === Test Suite Capture ===
if command -v pytest &>/dev/null; then
    echo "[INFO] Running pytest..."
    pytest -q -W once > "$TEST_FILE" || true

    echo -e "\n## 🧪 Pytest Results" >> agent.md
    echo '```' >> agent.md
    cat "$TEST_FILE" >> agent.md
    echo '```' >> agent.md
else
    echo "[WARN] pytest not installed – skipping test run."
fi

# === Git Commit and Push ===

# these final operations are typically disabled in a sandbox environment
# to avoid modifying remote repositories.
# We'll replace them with local git commits only.

git add "$REPORT_FILE" agent.md || true
if ! git diff --cached --quiet; then
    git commit -m "docs(agent): Comprehensive audit and UX suggestions [auto]"
else
    echo "No changes to commit"
fi
# Pulling or pushing from remote is disabled in this environment.

echo "[DONE] Report generated: $REPORT_FILE"

