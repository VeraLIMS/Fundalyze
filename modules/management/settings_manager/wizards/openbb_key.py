"""Wizard to set the OpenBB API token."""

from modules.config_utils import load_env, save_env

LABEL = "OpenBB API Token"


def run_wizard() -> None:
    print("\n=== OpenBB API Token Setup ===")
    print("Obtain a free API token at https://docs.openbb.co/platform/getting_started/api_requests\n")
    token = input("Enter OpenBB API token: ").strip()
    if not token:
        print("No token provided.\n")
        return
    env = load_env()
    env["OPENBB_TOKEN"] = token
    save_env(env)
    print("Token saved to config/.env.\n")
