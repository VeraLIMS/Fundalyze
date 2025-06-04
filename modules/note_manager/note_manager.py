import os
import re
from pathlib import Path
from typing import List, Optional


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
    """Interactive menu for creating and viewing notes."""
    while True:
        print("\n=== Notes ===")
        print("1) List notes")
        print("2) View note")
        print("3) Create note")
        print("4) Exit")
        choice = input("Enter 1-4: ").strip()

        if choice == "1":
            notes = list_notes()
            if not notes:
                print("No notes found.")
            else:
                for n in notes:
                    print(f"- {n}")
        elif choice == "2":
            title = input("Note title: ").strip()
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
            title = input("New note title: ").strip()
            print("Enter note content. End with an empty line.")
            lines: list[str] = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            create_note(title, "\n".join(lines))
            print(f"Created note '{title}'.")
        elif choice == "4":
            break
        else:
            print("Invalid choice.\n")
