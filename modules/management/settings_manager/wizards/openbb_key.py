"""Wizard to set the OpenBB API token."""

from modules.config_utils import load_env, save_env

LABEL = "OpenBB API Token"


def run_wizard() -> None:
    print("\n=== OpenBB API Token Setup ===")
    print(
        "More information about API requests: "
        "https://docs.openbb.co/platform/getting_started/api_requests"
    )
    print("First login or register: https://my.openbb.co/login")
    print("Obtain an API code here: https://my.openbb.co/app/platform/pat\n")
    token = input("Enter OpenBB API token: ").strip()
    if not token:
        print("No token provided.\n")
        return
    env = load_env()
    env["OPENBB_TOKEN"] = token
    save_env(env)
    print("Token saved to config/.env.\n")
