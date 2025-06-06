import subprocess


def test_no_todo_comments():
    files = subprocess.check_output(["git", "ls-files"]).decode().splitlines()
    for path in files:
        if path == 'tests/test_todo_removed.py':
            continue
        # Only check text-based files
        if path.endswith((
            ".py",
            ".md",
            ".txt",
            ".rst",
            ".json",
            ".yaml",
            ".yml",
            ".toml",
            ".cfg",
            ".ini",
            ".sh",
            ".ps1",
        )):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            assert "TODO" not in content, f"TODO found in {path}"
