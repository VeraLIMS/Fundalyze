import os
import subprocess
import time
from pathlib import Path
from typing import List

import openai
from dotenv import load_dotenv

# === Load environment ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Configuration ===
REPO_ROOT = Path(__file__).resolve().parent
TARGET_DIR = REPO_ROOT / "modules"  # Only refactor Python files in modules
AGENT_DOC = REPO_ROOT / "agent.md"
TEST_RESULTS = REPO_ROOT / "test_findings.txt"
DELAY_BETWEEN_REQUESTS = 2  # seconds between API calls

REFRACTOR_PROMPT = """
Codex, apply the refactor prompt template to Focus on readability, structure, and testability.

# Task: Refactor Code Module
# Objective: Improve code quality while preserving all functionality.

# Refactor Guidelines:
- Maintain all original logic and output.
- Improve readability and structure.
- Eliminate duplicate logic.
- Split large functions into smaller, single-purpose functions if beneficial.
- Add or improve function/class docstrings (Google-style).
- Use modern Python features (f-strings, type hints, pathlib, etc.).
- Keep naming consistent and descriptive.
- Apply consistent error handling and logging patterns.
- Preserve compatibility with related modules (e.g., config, API clients).
- Ensure it remains testable and extensible.

# Do NOT:
- Change filenames, function signatures, or input/output behavior.
- Introduce external dependencies unless explicitly requested.

# Output:
- The refactored code (fully self-contained)
- A brief summary of key changes (e.g., structure, naming, new functions)
"""


def run_command(command: List[str], cwd: Path = REPO_ROOT) -> str:
    """Run a shell command and return the captured stdout."""
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(command)}")
        if result.stderr:
            print(result.stderr)
    return result.stdout.strip()


def get_python_files(directory: Path) -> List[Path]:
    """Return a list of Python files under ``directory`` excluding hidden paths."""
    return [
        path
        for path in directory.rglob("*.py")
        if ".venv" not in path.parts and not any(part.startswith(".") for part in path.parts)
    ]


def extract_refactored_code(response_text: str) -> str:
    """Extract the refactored code block from an OpenAI response."""
    if "```python" in response_text:
        return response_text.split("```python", 1)[1].split("```", 1)[0].strip()
    if "```" in response_text:
        return response_text.split("```", 1)[1].strip()
    return response_text.strip()


def refactor_file(file_path: Path) -> None:
    """Send the file contents to the LLM and overwrite the file with the response."""
    original_code = file_path.read_text(encoding="utf-8")
    print(f"🧠 Refactoring: {file_path.relative_to(REPO_ROOT)}")

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are Codex, a senior Python engineer."},
            {
                "role": "user",
                "content": f"{REFRACTOR_PROMPT}\n\n```python\n{original_code}\n```",
            },
        ],
        temperature=0.2,
    )

    refactored_code = extract_refactored_code(response["choices"][0]["message"]["content"])
    file_path.write_text(refactored_code, encoding="utf-8")
    time.sleep(DELAY_BETWEEN_REQUESTS)


def run_tests() -> None:
    """Execute pytest and save output to ``TEST_RESULTS``."""
    print("🧪 Running test suite...")
    with open(TEST_RESULTS, "w", encoding="utf-8") as f:
        subprocess.run(["pytest", "-q", "-W", "once"], stdout=f, stderr=subprocess.STDOUT)


def update_agent_doc() -> None:
    """Append the latest test results to ``agent.md``."""
    print("📄 Updating agent.md with test results...")
    with open(AGENT_DOC, "a", encoding="utf-8") as doc, TEST_RESULTS.open("r", encoding="utf-8") as results:
        doc.write("\n## Recent Findings\n\n```")
        doc.write(results.read())
        doc.write("\n```")


def main() -> None:
    print("🚀 Starting Codex Refactor Agent")

    files = get_python_files(TARGET_DIR)
    print(f"📂 Found {len(files)} Python files in '{TARGET_DIR.relative_to(REPO_ROOT)}'")

    for file in files:
        try:
            refactor_file(file)
        except Exception as exc:  # noqa: BLE001
            print(f"[ERROR] Refactoring failed for {file.name}: {exc}")

    run_tests()
    update_agent_doc()
    print("✅ All tasks complete.")


if __name__ == "__main__":
    main()
