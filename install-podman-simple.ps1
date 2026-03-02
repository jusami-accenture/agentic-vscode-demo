# Podman Desktop Installation Script for Windows
# Simple version without encoding issues

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=================================================================="
Write-Host "  PODMAN DESKTOP INSTALLATION"
Write-Host "=================================================================="
Write-Host ""

# Configuration
$PodmanVersion = "1.9.0"
$DownloadUrl = "https://github.com/containers/podman-desktop/releases/download/v$PodmanVersion/podman-desktop-$PodmanVersion-setup.exe"
$InstallerPath = "$env:TEMP\podman-desktop-setup.exe"

Write-Host "[INFO] Podman Desktop is Docker-compatible (no Desktop license needed)"
Write-Host ""

# Download
Write-Host "[STEP 1] Downloading Podman Desktop v$PodmanVersion..."
try {
    if (Test-Path $InstallerPath) {
        Write-Host "[OK] Already downloaded: $InstallerPath"
    } else {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $DownloadUrl -OutFile $InstallerPath -UseBasicParsing
        Write-Host "[OK] Download complete"
    }
} catch {
    Write-Host "[ERROR] Download failed: $_"
    Write-Host ""
    Write-Host "Manual download: https://podman-desktop.io/downloads"
    exit 1
}

# Install
Write-Host ""
Write-Host "[STEP 2] Installing Podman Desktop..."
Write-Host "[INFO] The installer window will open - follow the prompts"
Write-Host ""
Write-Host "Press ENTER to continue..."
Read-Host

Start-Process -FilePath $InstallerPath -Wait

Write-Host ""
Write-Host "[OK] Installation completed"
Write-Host ""

# Verify
Write-Host "[STEP 3] Verification"
Write-Host ""
Write-Host "IMPORTANT: Close this terminal and open a NEW terminal, then run:"
Write-Host ""
Write-Host "  podman --version"
Write-Host "  podman machine init"
Write-Host "  podman machine start"
Write-Host ""
Write-Host "Then start the demo:"
Write-Host "  cd C:\Users\julio.sanchez\agentic-vscode-demo"
Write-Host "  podman-compose up -d"
Write-Host ""
Write-Host "OR use the helper script:"
Write-Host "  .\start-podman.ps1 up"
Write-Host ""
Write-Host ""
Write-Host "=================================================================="
Write-Host ""
