# bootstrap_env.ps1
# PowerShell script to create .venv, activate it, and install requirements.

param(
    [string]$VenvDir = ".venv",
    [string]$ReqFile = "requirements.txt"
)

# 1) If .venv/ doesn’t exist, create it:
if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating virtual environment in $VenvDir..." -ForegroundColor Cyan
    python -m venv $VenvDir
    if (-not (Test-Path $VenvDir)) {
        Write-Host "Failed to create $VenvDir. Exiting." -ForegroundColor Red
        exit 1
    }
    Write-Host "Virtual environment created."
} else {
    Write-Host "Virtual environment $VenvDir already exists; skipping creation." -ForegroundColor Yellow
}

# 2) Activate the venv in this PowerShell session:
$activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "Could not find activation script at $activateScript" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& $activateScript

# 3) Now that venv is active, install requirements:
if (-not (Test-Path $ReqFile)) {
    Write-Host "Cannot find $ReqFile. Please create it and list your dependencies." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Upgrading pip and installing dependencies from $ReqFile..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r $ReqFile

Write-Host ""
Write-Host "All dependencies installed into $VenvDir." -ForegroundColor Green
Write-Host "You are now in the activated virtual environment. Run 'python src/main.py' as usual.`n" -ForegroundColor Green
