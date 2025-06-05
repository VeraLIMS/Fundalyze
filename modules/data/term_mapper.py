"""Utilities to normalize sector and industry terminology."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

from modules.config_utils import load_settings  # noqa: E402

load_settings()

logger = logging.getLogger(__name__)

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None


# Configuration file lives in the project's top-level `config/` directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MAPPING_FILE = PROJECT_ROOT / "config" / "term_mapping.json"

OPENAI_MODEL = "gpt-3.5-turbo"
UNKNOWN_RESPONSE = "Unknown"


def load_mapping() -> Dict[str, List[str]]:
    """Return term mapping dictionary from :data:`MAPPING_FILE`."""
    if not MAPPING_FILE.is_file():
        return {}
    return json.loads(MAPPING_FILE.read_text(encoding="utf-8"))


def save_mapping(mapping: Dict[str, List[str]]) -> None:
    """Write ``mapping`` to :data:`MAPPING_FILE`."""
    MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    MAPPING_FILE.write_text(json.dumps(mapping, indent=2), encoding="utf-8")


def _normalize(text: str) -> str:
    """Return lowercase, trimmed representation of ``text``."""
    return text.strip().lower()


def _find_direct_match(mapping: Dict[str, List[str]], norm: str) -> Optional[str]:
    """Return canonical term if ``norm`` matches a canonical or alias."""
    for canonical, aliases in mapping.items():
        if norm == _normalize(canonical) or norm in map(_normalize, aliases):
            return canonical
    return None


def _confirm_suggestion(term: str, suggestion: str) -> bool:
    """Return True if user confirms mapping ``term`` to ``suggestion``."""
    resp = input(f"Map '{term}' to '{suggestion}'? (Y/n): ").strip().lower()
    return resp in ("", "y", "yes")


def _manual_selection(term: str, mapping: Dict[str, List[str]]) -> Optional[str]:
    """Interactively choose or create a canonical term for ``term``."""
    print(f"\nUnknown term: '{term}'.")
    if mapping:
        print("Available canonical terms:")
        canonicals = list(mapping.keys())
        for idx, canonical in enumerate(canonicals, start=1):
            print(f"  {idx}) {canonical}")
        print(f"  {len(canonicals) + 1}) Create new canonical term")
        choice = input(f"Select 1-{len(canonicals) + 1}: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(canonicals):
                return canonicals[idx - 1]
    canonical = input("Enter new canonical term: ").strip()
    return canonical or None


def add_alias(canonical: str, alias: str) -> None:
    """Persist ``alias`` as an alternative spelling for ``canonical``."""
    mapping = load_mapping()
    canonical_norm = canonical.strip()
    alias_norm = alias.strip()
    if not canonical_norm or not alias_norm:
        return
    aliases = mapping.get(canonical_norm, [])
    if alias_norm not in aliases:
        aliases.append(alias_norm)
        mapping[canonical_norm] = aliases
        save_mapping(mapping)


def _suggest_with_openai(term: str, options: List[str]) -> Optional[str]:
    """Return best matching option suggested by OpenAI or ``None``."""
    if openai is None or not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        prompt = (
            "You are an assistant that maps financial sector or industry terms to a canonical term. "
            f"Given the term '{term}', choose the best match from the following options: {', '.join(options)}. "
            f"Respond with only the best matching option or '{UNKNOWN_RESPONSE}'."
        )
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=6,
        )
        choice = response.choices[0].message.content.strip()
        if choice and choice != UNKNOWN_RESPONSE:
            return choice
    except Exception as exc:  # pragma: no cover - network errors nondeterministic
        logger.error("OpenAI suggestion failed: %s", exc)
    return None


def resolve_term(term: str) -> str:
    """Return canonical representation for ``term``.

    The function checks existing aliases, optionally queries OpenAI for a best
    guess and finally prompts the user to pick or create a mapping. Any new
    mapping is saved via :func:`add_alias`.
    """
    if not term:
        return term

    mapping = load_mapping()
    norm = _normalize(term)

    canonical = _find_direct_match(mapping, norm)
    if canonical:
        return canonical

    suggestion = _suggest_with_openai(term, list(mapping.keys()))
    if suggestion and _confirm_suggestion(term, suggestion):
        add_alias(suggestion, term)
        return suggestion

    canonical = _manual_selection(term, mapping)
    if canonical:
        add_alias(canonical, term)
        return canonical

    return term
