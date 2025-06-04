"""Wizard to set the report output directory."""

from modules.config_utils import load_env, save_env

LABEL = "Output Directory"


def run_wizard() -> None:
    print("\n=== Output Directory Setup ===")
    env = load_env()
    current = env.get("OUTPUT_DIR", "output")
    path = input(f"Output directory [{current}]: ").strip() or current
    env["OUTPUT_DIR"] = path
    save_env(env)
    print(f"Output directory saved to config/.env as '{path}'.\n")
