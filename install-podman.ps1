#!/usr/bin/env powershell
<#
.SYNOPSIS
    Automated Podman Desktop Installation for Windows
    
.DESCRIPTION
    Downloads and installs Podman Desktop - a Docker-compatible container engine
    that doesn't require Docker Desktop or admin privileges during runtime.
    
.NOTES
    Compatible with: Windows 10/11
    No Docker Desktop required
    Company policy compliant (no license issues)
#>

param(
    [switch]$SkipDownload = $false,
    [switch]$AutoInstall = $false
)

$ErrorActionPreference = "Stop"

# Configuration
$PodmanVersion = "1.9.0"
$DownloadUrl = "https://github.com/containers/podman-desktop/releases/download/v$PodmanVersion/podman-desktop-$PodmanVersion-setup.exe"
$InstallerPath = "$env:TEMP\podman-desktop-setup.exe"

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "  PODMAN DESKTOP INSTALLATION FOR AGENTIC DEMO" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Podman Desktop is a Docker-compatible container engine" -ForegroundColor Green
Write-Host "   • No Docker Desktop license required" -ForegroundColor Gray
Write-Host "   • No admin privileges needed for runtime" -ForegroundColor Gray
Write-Host "   • 100% compatible with docker-compose.yml" -ForegroundColor Gray
Write-Host "   • Free and open source" -ForegroundColor Gray
Write-Host ""

# Step 1: Download Podman Desktop
if (-not $SkipDownload) {
    Write-Host "📥 Step 1: Downloading Podman Desktop v$PodmanVersion..." -ForegroundColor Yellow
    Write-Host "   URL: $DownloadUrl" -ForegroundColor Gray
    Write-Host ""
    
    try {
        # Check if already downloaded
        if (Test-Path $InstallerPath) {
            Write-Host "✅ Installer already downloaded: $InstallerPath" -ForegroundColor Green
        } else {
            $ProgressPreference = 'SilentlyContinue'
            Invoke-WebRequest -Uri $DownloadUrl -OutFile $InstallerPath -UseBasicParsing
            Write-Host "✅ Download complete: $InstallerPath" -ForegroundColor Green
        }
        Write-Host ""
    } catch {
        Write-Host "❌ Download failed: $_" -ForegroundColor Red
        Write-Host ""
        Write-Host "📝 Manual download instructions:" -ForegroundColor Yellow
        Write-Host "   1. Open: https://podman-desktop.io/downloads" -ForegroundColor Gray
        Write-Host "   2. Download: Windows Installer" -ForegroundColor Gray
        Write-Host "   3. Run the installer" -ForegroundColor Gray
        Write-Host "   4. Return here and run: .\install-podman.ps1 -SkipDownload" -ForegroundColor Gray
        exit 1
    }
}

# Step 2: Install Podman Desktop
Write-Host "🔧 Step 2: Installing Podman Desktop..." -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path $InstallerPath)) {
    Write-Host "❌ Installer not found at: $InstallerPath" -ForegroundColor Red
    Write-Host "   Run without -SkipDownload flag" -ForegroundColor Gray
    exit 1
}

Write-Host "⚠️  IMPORTANT: The installer will launch now" -ForegroundColor Magenta
Write-Host "   • Click through the installation wizard" -ForegroundColor Gray
Write-Host "   • Accept default settings" -ForegroundColor Gray
Write-Host "   • Wait for installation to complete" -ForegroundColor Gray
Write-Host ""

if ($AutoInstall) {
    Write-Host "Starting silent installation..." -ForegroundColor Gray
    Start-Process -FilePath $InstallerPath -ArgumentList "/S" -Wait
} else {
    Write-Host "Press ENTER to launch the installer..." -ForegroundColor Yellow
    Read-Host
    Start-Process -FilePath $InstallerPath -Wait
}

Write-Host ""
Write-Host "✅ Installation initiated" -ForegroundColor Green
Write-Host ""

# Step 3: Wait for installation
Write-Host "⏳ Waiting for installation to complete..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Step 4: Verify installation
Write-Host ""
Write-Host "🔍 Step 3: Verifying installation..." -ForegroundColor Yellow
Write-Host ""

$maxRetries = 12
$retryCount = 0
$podmanFound = $false

while ($retryCount -lt $maxRetries -and -not $podmanFound) {
    $retryCount++
    
    # Refresh PATH
    $machinePath = [System.Environment]::GetEnvironmentVariable("Path","Machine")
    $userPath = [System.Environment]::GetEnvironmentVariable("Path","User")
    $env:Path = $machinePath + ";" + $userPath
            $podmanFound = $true
            Write-Host "✅ Podman installed successfully: $podmanVersion" -ForegroundColor Green
        }
    } catch {
        # Still installing
    }
    
    if (-not $podmanFound) {
        Write-Host "   Attempt $retryCount/$maxRetries - Still installing..." -ForegroundColor Gray
        Start-Sleep -Seconds 5
    }
}

if (-not $podmanFound) {
    Write-Host ""
    Write-Host "⚠️  Podman not detected yet" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This is normal! Podman Desktop might still be installing." -ForegroundColor Gray
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "  1. Wait for Podman Desktop installation to finish" -ForegroundColor Gray
    Write-Host "  2. Launch Podman Desktop from Start Menu" -ForegroundColor Gray
    Write-Host "  3. Complete the first-time setup wizard" -ForegroundColor Gray
    Write-Host "  4. Close this terminal and open a NEW terminal" -ForegroundColor Gray
    Write-Host "  5. Run: podman --version" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# Step 5: Initialize Podman Machine
Write-Host ""
Write-Host "🚀 Step 4: Initializing Podman machine..." -ForegroundColor Yellow
Write-Host ""

try {
    # Check if machine already exists
    $machines = & podman machine list 2>$null
    if ($machines -match "podman-machine-default") {
        Write-Host "✅ Podman machine already exists" -ForegroundColor Green
    } else {
        Write-Host "Creating Podman machine..." -ForegroundColor Gray
        & podman machine init
        Write-Host "✅ Podman machine initialized" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Starting Podman machine..." -ForegroundColor Gray
    & podman machine start
    Write-Host "✅ Podman machine started" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Machine initialization skipped: $_" -ForegroundColor Yellow
    Write-Host "   You may need to do this manually via Podman Desktop UI" -ForegroundColor Gray
}

# Step 6: Test Docker compatibility
Write-Host ""
Write-Host "🧪 Step 5: Testing Docker compatibility..." -ForegroundColor Yellow
Write-Host ""

try {
    # Create docker alias if it doesn't exist
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Host "Creating docker alias..." -ForegroundColor Gray
        New-Alias -Name docker -Value podman -Scope Global -Force
    }
    
    $dockerVersion = & podman version --format "{{.Client.Version}}"
    Write-Host "✅ Docker-compatible CLI ready (Podman $dockerVersion)" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Will use 'podman' command instead of 'docker'" -ForegroundColor Yellow
}

# Success!
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "  ✅ PODMAN DESKTOP INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣  CLOSE this terminal and open a NEW PowerShell terminal" -ForegroundColor Yellow
Write-Host ""
Write-Host "2️⃣  Verify Podman is working:" -ForegroundColor Yellow
Write-Host "    podman --version" -ForegroundColor Gray
Write-Host "    podman machine list" -ForegroundColor Gray
Write-Host ""
Write-Host "3️⃣  Start the containerized demo:" -ForegroundColor Yellow
Write-Host "    cd C:\Users\julio.sanchez\agentic-vscode-demo" -ForegroundColor Gray
Write-Host "    podman-compose up -d" -ForegroundColor Gray
Write-Host ""
Write-Host "    OR use our helper script:" -ForegroundColor Gray
Write-Host "    .\start-podman.ps1 up" -ForegroundColor Gray
Write-Host ""
Write-Host "4️⃣  View running containers:" -ForegroundColor Yellow
Write-Host "    podman ps" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 TIP: Podman commands work exactly like Docker:" -ForegroundColor Cyan
Write-Host "    podman ps        = docker ps" -ForegroundColor Gray
Write-Host "    podman-compose   = docker-compose" -ForegroundColor Gray
Write-Host "    podman run       = docker run" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Documentation: See INSTALL_ALTERNATIVES.md" -ForegroundColor Cyan
Write-Host ""
