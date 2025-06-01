# bootstrap_env.ps1
# PowerShell script to ensure Python 3.10.10 is installed, create .venv with that version, activate it, and install requirements.

param(
    [string]$VenvDir = ".venv",
    [string]$ReqFile = "requirements.txt"
)

function Install-Python310 {
    # Check if Python 3.10.10 is already available via the Python launcher
    try {
        $versionOutput = & py -3.10 --version 2>&1
    } catch {
        $versionOutput = ""
    }
    if ($versionOutput -match "Python 3\.10\.10") {
        Write-Host "Python 3.10.10 is already installed." -ForegroundColor Green
        return
    }

    Write-Host "Python 3.10.10 not found. Downloading and installing..." -ForegroundColor Cyan

    # Determine download URL and target file
    $installerUrl = "https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe"
    $tempInstaller = Join-Path $env:TEMP "python-3.10.10-amd64.exe"

    # Download installer
    Write-Host "Downloading Python 3.10.10 installer to $tempInstaller" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $installerUrl -OutFile $tempInstaller

    # Run installer silently for current user, add to PATH, include pip
    Write-Host "Running Python 3.10.10 installer..." -ForegroundColor Cyan
    & $tempInstaller /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1

    # Remove installer
    Remove-Item $tempInstaller -Force

    # Verify installation
    try {
        $versionOutput = & py -3.10 --version 2>&1
    } catch {
        $versionOutput = ""
    }
    if ($versionOutput -match "Python 3\.10\.10") {
        Write-Host "Python 3.10.10 installed successfully." -ForegroundColor Green
    } else {
        Write-Host "Failed to install Python 3.10.10." -ForegroundColor Red
        Exit 1
    }
}

# 1) Ensure Python 3.10.10 is available
Install-Python310

# 2) If .venv/ doesn’t exist, create it using Python 3.10.10
if (-not (Test-Path $VenvDir)) {
    Write-Host "`nCreating virtual environment in $VenvDir using Python 3.10.10..." -ForegroundColor Cyan
    & py -3.10 -m venv $VenvDir
    if (-not (Test-Path $VenvDir)) {
        Write-Host "Failed to create $VenvDir. Exiting." -ForegroundColor Red
        Exit 1
    }
    Write-Host "Virtual environment created."
} else {
    Write-Host "`nVirtual environment $VenvDir already exists; skipping creation." -ForegroundColor Yellow
}

# 3) Activate the venv in this PowerShell session
$activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "Could not find activation script at $activateScript" -ForegroundColor Red
    Exit 1
}

Write-Host "`nActivating virtual environment..." -ForegroundColor Cyan
& $activateScript

# 4) Install requirements inside the venv
if (-not (Test-Path $ReqFile)) {
    Write-Host "Cannot find $ReqFile. Please create it and list your dependencies." -ForegroundColor Red
    Exit 1
}

Write-Host "`nUpgrading pip and installing dependencies from $ReqFile..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r $ReqFile

Write-Host "`nAll dependencies installed into $VenvDir." -ForegroundColor Green
Write-Host "You are now in the activated virtual environment. Run 'python src/main.py' as usual.`n" -ForegroundColor Green
