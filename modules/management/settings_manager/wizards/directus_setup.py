"""Wizard to configure Directus connection details."""

from modules.config_utils import load_env, save_env

LABEL = "Directus Connection"


def run_wizard() -> None:
    print("\n=== Directus Connection Setup ===")
    env = load_env()
    current_url = env.get("DIRECTUS_URL", "")
    current_token = env.get("DIRECTUS_TOKEN", "")
    current_portfolio = env.get("DIRECTUS_PORTFOLIO_COLLECTION", "portfolio")
    current_groups = env.get("DIRECTUS_GROUPS_COLLECTION", "groups")

    url = input(f"Directus URL [{current_url}]: ").strip() or current_url
    token = input(f"API Token [{current_token}]: ").strip() or current_token
    portfolio = input(f"Portfolio collection [{current_portfolio}]: ").strip() or current_portfolio
    groups = input(f"Groups collection [{current_groups}]: ").strip() or current_groups

    if url:
        env["DIRECTUS_URL"] = url
    if token:
        env["DIRECTUS_TOKEN"] = token
    env["DIRECTUS_PORTFOLIO_COLLECTION"] = portfolio
    env["DIRECTUS_GROUPS_COLLECTION"] = groups
    save_env(env)
    print("Directus configuration saved to config/.env.\n")
