"""Wizard to set the Financial Modeling Prep API key."""

from modules.config_utils import load_env, save_env

LABEL = "FMP API Key"


def run_wizard() -> None:
    print("\n=== FMP API Key Setup ===")
    print("Obtain a free API key at https://financialmodelingprep.com\n")
    key = input("Enter FMP API key: ").strip()
    if not key:
        print("No key provided.\n")
        return
    env = load_env()
    env["FMP_API_KEY"] = key
    save_env(env)
    print("API key saved to config/.env.\n")
