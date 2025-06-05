"""Wizard to configure Cloudflare Access credentials for Directus."""

from modules.config_utils import load_env, save_env

LABEL = "Cloudflare Access"


def run_wizard() -> None:
    print("\n=== Cloudflare Access Setup ===")
    env = load_env()
    current_id = env.get("CF_ACCESS_CLIENT_ID", "")
    current_secret = env.get("CF_ACCESS_CLIENT_SECRET", "")
    client_id = input("CF-Access-Client-Id: ").strip() or current_id
    client_secret = input("CF-Access-Client-Secret: ").strip() or current_secret
    if client_id:
        env["CF_ACCESS_CLIENT_ID"] = client_id
    if client_secret:
        env["CF_ACCESS_CLIENT_SECRET"] = client_secret
    save_env(env)
    print("Cloudflare credentials saved to config/.env.\n")
