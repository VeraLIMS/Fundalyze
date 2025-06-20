"""Command line note manager with wiki-style links."""

import os
import re
from pathlib import Path
from typing import List, Optional

from modules.interface import print_invalid_choice, print_header, print_menu


def get_notes_dir() -> Path:
    """Return the notes directory, creating it if needed."""
    notes_dir = Path(os.environ.get("NOTES_DIR", "notes"))
    notes_dir.mkdir(parents=True, exist_ok=True)
    return notes_dir


def slugify(title: str) -> str:
    """Convert a note title into a filesystem-friendly slug."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")


def get_note_path(title: str) -> Path:
    """Return the Path for a given note title."""
    return get_notes_dir() / f"{slugify(title)}.md"


def create_note(title: str, content: str = "") -> Path:
    """Create a new note with the given title and content."""
    path = get_note_path(title)
    header = f"# {title}\n\n"
    if not path.exists():
        path.write_text(header + content)
    return path


def read_note(title: str) -> Optional[str]:
    """Return the contents of a note, or None if it doesn't exist."""
    path = get_note_path(title)
    if path.is_file():
        return path.read_text()
    return None


def list_notes() -> List[str]:
    """Return a list of available note titles (slugs)."""
    notes_dir = get_notes_dir()
    return [p.stem for p in notes_dir.glob("*.md")]


def parse_links(content: str) -> List[str]:
    """Return a list of note titles referenced via [[wikilink]] syntax."""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


# ──────────────────────────────────────────────────────────────────────────────
# Simple CLI interface


def run_note_manager() -> None:
    """Run the interactive notes manager CLI."""
    while True:
        print_header("📝 Notes")
        options = [
            "List Notes",
            "View Note",
            "Create Note",
            "Return to Main Menu",
        ]
        print_menu(options)
        choice = input(f"Select an option [1-{len(options)}]: ").strip()

        if choice == "1":
            notes = list_notes()
            if not notes:
                print("No notes found.")
            else:
                for n in notes:
                    print(f"- {n}")
        elif choice == "2":
            title = input("Note title (or press Enter to cancel): ").strip()
            if not title:
                print("Canceled.\n")
                continue
            content = read_note(title)
            if content is None:
                print("Note not found.")
            else:
                print("\n" + content)
                links = parse_links(content)
                if links:
                    print("\nLinks:")
                    for link in links:
                        print(f"- {link}")
        elif choice == "3":
            title = input("New note title (or press Enter to cancel): ").strip()
            if not title:
                print("Canceled.\n")
                continue
            print("Enter note content. Finish with an empty line or 'q' to cancel.")
            lines: list[str] = []
            while True:
                line = input()
                if line.lower() == "q":
                    print("Canceled.\n")
                    return
                if line == "":
                    break
                lines.append(line)
            create_note(title, "\n".join(lines))
            print(f"Created note '{title}'.")
        elif choice == "4":
            break
        else:
            print_invalid_choice()
