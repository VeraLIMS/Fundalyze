# Fundalyze

This repository includes a **bootstrap script** (`bootstrap_env.ps1` for Windows) that:

1. **Creates** a Python virtual environment in `./.venv/` (if it doesn’t already exist).  
2. **Activates** that venv in the current shell session.  
3. **Installs** all packages listed in `requirements.txt` into the newly created venv.

---

## Usage (Windows PowerShell)

1. Open PowerShell in the project root.  
2. Run:
   ```powershell
   .\bootstrap_env.ps1

If ./.venv/ is missing, it will be created.

The script will then activate the venv for you.

Finally, it installs everything from requirements.txt.

Once complete, you remain inside the activated venv. Simply run:

python src/main.py

to launch the application.

