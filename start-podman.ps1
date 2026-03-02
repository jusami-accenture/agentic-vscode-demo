# PowerShell script to manage Podman-based Agentic Platform
# Usage: .\start-podman.ps1 [command]

param(
    [Parameter(Position=0)]
    [ValidateSet("up", "down", "ps", "logs", "restart", "build", "clean", "scale", "health", "help")]
    [string]$Command = "help"
)

$ErrorActionPreference = "Stop"

function Write-Banner {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "   🐳 Podman Multi-Agent Platform Manager" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Step {
    param([string]$Message)
    Write-Host "[STEP] $Message" -ForegroundColor Yellow
}

function Write-Error-Message {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Test-PodmanAvailable {
    try {
        $podmanVersion = podman --version 2>&1
        Write-Info "Podman: $podmanVersion"
        return $true
    }
    catch {
        Write-Error-Message "Podman not found. Please install Podman Desktop."
        Write-Host ""
        Write-Host "Download from: https://podman-desktop.io/downloads" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Or see INSTALL_ALTERNATIVES.md for other options." -ForegroundColor Yellow
        return $false
    }
}

function Test-PodmanMachineRunning {
    try {
        $machineStatus = podman machine inspect 2>&1 | ConvertFrom-Json
        if ($machineStatus.State -eq "running") {
            return $true
        }
        else {
            Write-Info "Starting Podman machine..."
            podman machine start
            Start-Sleep -Seconds 5
            return $true
        }
    }
    catch {
        Write-Info "Initializing Podman machine..."
        podman machine init
        podman machine start
        Start-Sleep -Seconds 5
        return $true
    }
}

function Show-Help {
    Write-Banner
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  up       - Start all containers (full platform)" -ForegroundColor Green
    Write-Host "  down     - Stop all containers" -ForegroundColor Green
    Write-Host "  ps       - Show container status" -ForegroundColor Green
    Write-Host "  logs     - Show logs from all containers" -ForegroundColor Green
    Write-Host "  restart  - Restart all containers" -ForegroundColor Green
    Write-Host "  build    - Rebuild all container images" -ForegroundColor Green
    Write-Host "  clean    - Remove all containers and volumes" -ForegroundColor Green
    Write-Host "  scale    - Scale agents" -ForegroundColor Green
    Write-Host "  health   - Check health of all services" -ForegroundColor Green
    Write-Host "  help     - Show this help message" -ForegroundColor Green
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\start-podman.ps1 up              # Start everything" -ForegroundColor Gray
    Write-Host "  .\start-podman.ps1 logs it-agent   # View IT agent logs" -ForegroundColor Gray
    Write-Host "  .\start-podman.ps1 health          # Check service health" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Note: Uses Podman instead of Docker (no admin required!)" -ForegroundColor Yellow
    Write-Host ""
}

function Start-Platform {
    Write-Banner
    Write-Info "Starting containerized multi-agent platform with Podman..."
    Write-Host ""
    
    Write-Step "Building container images..."
    podman-compose build
    
    Write-Host ""
    Write-Step "Starting all services..."
    podman-compose up -d
    
    Write-Host ""
    Write-Step "Waiting for services to become healthy..."
    Start-Sleep -Seconds 5
    
    Write-Host ""
    Write-Info "Platform started! Services available at:"
    Write-Host ""
    Write-Host "  🎯 Orchestrator:      http://localhost:8001" -ForegroundColor Cyan
    Write-Host "  🔧 MCP Server:        http://localhost:3000" -ForegroundColor Cyan
    Write-Host "  💼 IT Agent:          http://localhost:8002" -ForegroundColor Cyan
    Write-Host "  ☸️  K8s Agent:         http://localhost:8003" -ForegroundColor Cyan
    Write-Host "  🤖 Inference Server:  http://localhost:8080" -ForegroundColor Cyan
    Write-Host "  📊 Grafana:           http://localhost:3001 (admin/admin)" -ForegroundColor Cyan
    Write-Host "  📈 Prometheus:        http://localhost:9090" -ForegroundColor Cyan
    Write-Host "  🔍 Jaeger:            http://localhost:16686" -ForegroundColor Cyan
    Write-Host ""
    Write-Info "View logs with: .\start-podman.ps1 logs"
    Write-Info "Check status with: .\start-podman.ps1 ps"
    Write-Host ""
}

function Stop-Platform {
    Write-Banner
    Write-Info "Stopping all containers..."
    podman-compose down
    Write-Host ""
    Write-Info "Platform stopped."
    Write-Host ""
}

function Show-Status {
    Write-Banner
    Write-Info "Container Status:"
    Write-Host ""
    podman-compose ps
    Write-Host ""
}

function Show-Logs {
    Write-Banner
    Write-Info "Container Logs (press Ctrl+C to exit):"
    Write-Host ""
    
    if ($args.Count -gt 0) {
        $service = $args[0]
        Write-Info "Showing logs for: $service"
        podman-compose logs -f $service
    }
    else {
        Write-Info "Showing logs for all services"
        podman-compose logs -f
    }
}

function Restart-Platform {
    Write-Banner
    Write-Info "Restarting all containers..."
    podman-compose restart
    Write-Host ""
    Write-Info "Platform restarted!"
    Write-Host ""
}

function Build-Platform {
    Write-Banner
    Write-Info "Rebuilding all container images..."
    Write-Host ""
    podman-compose build --no-cache
    Write-Host ""
    Write-Info "Build complete! Start with: .\start-podman.ps1 up"
    Write-Host ""
}

function Clean-Platform {
    Write-Banner
    Write-Host "⚠️  WARNING: This will remove all containers, images, and volumes!" -ForegroundColor Red
    Write-Host ""
    $confirm = Read-Host "Continue? (yes/no)"
    
    if ($confirm -eq "yes") {
        Write-Info "Stopping and removing all containers..."
        podman-compose down -v
        
        Write-Info "Removing images..."
        podman rmi -a -f
        
        Write-Info "Pruning system..."
        podman system prune -f
        
        Write-Host ""
        Write-Info "Cleanup complete!"
    }
    else {
        Write-Info "Cleanup cancelled."
    }
    Write-Host ""
}

function Check-Health {
    Write-Banner
    Write-Info "Checking service health..."
    Write-Host ""
    
    $services = @(
        @{Name="Inference Server"; Url="http://localhost:8080/health"}
        @{Name="MCP Server"; Url="http://localhost:3000/health"}
        @{Name="Orchestrator"; Url="http://localhost:8001/health"}
        @{Name="IT Agent"; Url="http://localhost:8002/health"}
        @{Name="K8s Agent"; Url="http://localhost:8003/health"}
        @{Name="Prometheus"; Url="http://localhost:9090/-/healthy"}
        @{Name="Grafana"; Url="http://localhost:3001/api/health"}
    )
    
    foreach ($service in $services) {
        try {
            $response = Invoke-WebRequest -Uri $service.Url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            Write-Host "✅ $($service.Name): Healthy" -ForegroundColor Green
        }
        catch {
            Write-Host "❌ $($service.Name): Unhealthy or not responding" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Info "Container status:"
    podman ps --format "table {{.Names}}\t{{.Status}}"
    Write-Host ""
}

# Main execution
Write-Host ""

if (-not (Test-PodmanAvailable)) {
    Write-Host ""
    Write-Host "💡 Alternative: Run without containers" -ForegroundColor Yellow
    Write-Host "   .\start-demo.ps1 all" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   See INSTALL_ALTERNATIVES.md for more options." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

if ($Command -ne "help") {
    if (-not (Test-PodmanMachineRunning)) {
        Write-Error-Message "Podman machine not running and failed to start."
        exit 1
    }
}

switch ($Command) {
    "up" { Start-Platform }
    "down" { Stop-Platform }
    "ps" { Show-Status }
    "logs" { Show-Logs @args }
    "restart" { Restart-Platform }
    "build" { Build-Platform }
    "clean" { Clean-Platform }
    "health" { Check-Health }
    "help" { Show-Help }
    default { Show-Help }
}
