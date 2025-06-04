import json
import os
from typing import Dict, List, Optional

try:
    import openai
except Exception:
    openai = None


MAPPING_FILE = os.path.join(os.path.dirname(__file__), '..', 'Config', 'term_mapping.json')
MAPPING_FILE = os.path.abspath(MAPPING_FILE)


def load_mapping() -> Dict[str, List[str]]:
    if not os.path.isfile(MAPPING_FILE):
        return {}
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_mapping(mapping: Dict[str, List[str]]):
    os.makedirs(os.path.dirname(MAPPING_FILE), exist_ok=True)
    with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2)


def _normalize(text: str) -> str:
    return text.strip().lower()


def add_alias(canonical: str, alias: str):
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
    if openai is None or not os.getenv('OPENAI_API_KEY'):
        return None
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')
        prompt = (
            "You are an assistant that maps financial sector or industry terms to a canonical term. "
            f"Given the term '{term}', choose the best match from the following options: {', '.join(options)}. "
            "Respond with only the best matching option or 'Unknown'."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=6
        )
        choice = response.choices[0].message.content.strip()
        if choice and choice != 'Unknown':
            return choice
    except Exception:
        return None
    return None


def resolve_term(term: str) -> str:
    """Return canonical term for given term. If unknown, ask user."""
    if not term:
        return term
    mapping = load_mapping()
    norm = _normalize(term)
    # direct match
    for canonical, aliases in mapping.items():
        if norm == _normalize(canonical) or norm in [_normalize(a) for a in aliases]:
            return canonical
    # not found; try openai suggestion
    suggestion = _suggest_with_openai(term, list(mapping.keys()))
    if suggestion:
        resp = input(f"Map '{term}' to '{suggestion}'? (Y/n): ").strip().lower()
        if resp in ('', 'y', 'yes'):
            add_alias(suggestion, term)
            return suggestion
    # manual selection
    print(f"\nUnknown term: '{term}'.")
    if mapping:
        print("Available canonical terms:")
        canonicals = list(mapping.keys())
        for idx, c in enumerate(canonicals, start=1):
            print(f"  {idx}) {c}")
        print(f"  {len(canonicals)+1}) Create new canonical term")
        choice = input(f"Select 1-{len(canonicals)+1}: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(canonicals):
                canonical = canonicals[idx-1]
                add_alias(canonical, term)
                return canonical
    # create new canonical
    canonical = input("Enter new canonical term: ").strip()
    if canonical:
        add_alias(canonical, term)
        return canonical
    return term
