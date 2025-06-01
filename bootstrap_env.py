# bootstrap_env.py

import os
import sys
import subprocess
import shutil
from pathlib import Path
import venv

PROJECT_ROOT = Path(__file__).parent.resolve()
VENV_DIR     = PROJECT_ROOT / ".venv"
REQ_FILE     = PROJECT_ROOT / "requirements.txt"


def in_venv() -> bool:
    """
    Return True if the current interpreter is running inside a virtual environment
    whose root is PROJECT_ROOT/.venv (or at least some venv).
    We check by comparing sys.prefix to sys.base_prefix (CPython) or
    looking for VIRTUAL_ENV environment variable.
    """
    # If VIRTUAL_ENV is set, we are in a venv
    if "VIRTUAL_ENV" in os.environ:
        return True

    # For Python 3.3+, sys.prefix != sys.base_prefix when in a venv
    return getattr(sys, "base_prefix", sys.prefix) != sys.prefix


def create_venv():
    """
    Create a new virtual environment in .venv/ using the standard library venv module.
    If .venv/ already exists, we leave it as-is.
    """
    if VENV_DIR.exists():
        print(f"  [INFO] .venv/ already exists; skipping creation")
        return

    print("  → Creating virtual environment in .venv/ …")
    venv.create(str(VENV_DIR), with_pip=True)
    print("  √ Virtual environment created.")


def install_requirements(python_executable: Path):
    """
    Run `python_executable -m pip install -r requirements.txt` (upgrading pip first).
    """
    print(f"  → Installing dependencies from {REQ_FILE.name} using {python_executable} …")
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "-r", str(REQ_FILE)])
    print("  √ Dependencies installed.")


def main():
    # 1) Check that requirements.txt exists
    if not REQ_FILE.exists():
        print(f"[ERROR] Cannot find {REQ_FILE}. Please create one listing your dependencies.")
        sys.exit(1)

    # 2) If not in any venv at all, create .venv/ and re‐invoke under that Python
    if not in_venv():
        print(f"[INFO] Not running inside a virtual environment.")
        create_venv()

        # Figure out path to the venv’s python
        if sys.platform.startswith("win"):
            venv_python = VENV_DIR / "Scripts" / "python.exe"
        else:
            venv_python = VENV_DIR / "bin" / "python"

        if not venv_python.exists():
            print(f"[ERROR] Couldn’t find {venv_python}. Something went wrong during venv creation.")
            sys.exit(1)

        # Re‐invoke this script under the venv’s python
        print(f"[INFO] Re‐invoking under {venv_python} to install requirements…\n")
        os.execv(str(venv_python), [str(venv_python), str(__file__)])

    # 3) If we reach here, we are inside the venv
    print(f"[INFO] Running inside a virtual environment ({sys.executable}).")

    # Optionally check .venv/ is actually the venv we expect
    if VENV_DIR not in Path(sys.executable).resolve().parents:
        print("  [WARNING] You are in a different venv than .venv/. "
              "Proceeding will install into the currently active venv.")
        resp = input("  Continue installing deps here? [y/N]: ").strip().lower()
        if resp not in ("y", "yes"):
            print("  Aborting installation.")
            sys.exit(0)

    # 4) Install requirements into this venv
    install_requirements(Path(sys.executable))

    # 5) Remind user to activate (Windows vs. POSIX)
    print("\nDone. To activate this environment, run:")
    if sys.platform.startswith("win"):
        print("  .\\.venv\\Scripts\\activate  (in PowerShell or CMD)")
    else:
        print("  source .venv/bin/activate  (in bash/zsh/fish)")
    print("\nAny python/pip calls from now on will use this .venv/. ")
    print("You can now run `python src/main.py` as usual.\n")


if __name__ == "__main__":
    main()
