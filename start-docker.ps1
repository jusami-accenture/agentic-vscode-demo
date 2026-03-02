# PowerShell script to manage Docker-based Agentic Platform
# Usage: .\start-docker.ps1 [command]

param(
    [Parameter(Position=0)]
    [ValidateSet("up", "down", "ps", "logs", "restart", "build", "clean", "scale", "health", "help")]
    [string]$Command = "help"
)

$ErrorActionPreference = "Stop"

function Write-Banner {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "   🐳 Docker Multi-Agent Platform Manager" -ForegroundColor Cyan
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

function Test-DockerAvailable {
    try {
        $dockerVersion = docker --version 2>&1
        Write-Info "Docker: $dockerVersion"
        return $true
    }
    catch {
        Write-Error-Message "Docker not found. Please install Docker Desktop."
        Write-Host ""
        Write-Host "Download from: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
        return $false
    }
}

function Test-DockerRunning {
    try {
        docker ps | Out-Null
        return $true
    }
    catch {
        Write-Error-Message "Docker daemon is not running."
        Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
        return $false
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
    Write-Host "  scale    - Scale agents (e.g., scale it-agent=5)" -ForegroundColor Green
    Write-Host "  health   - Check health of all services" -ForegroundColor Green
    Write-Host "  help     - Show this help message" -ForegroundColor Green
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\start-docker.ps1 up              # Start everything" -ForegroundColor Gray
    Write-Host "  .\start-docker.ps1 logs it-agent   # View IT agent logs" -ForegroundColor Gray
    Write-Host "  .\start-docker.ps1 scale           # Scale IT agents to 3" -ForegroundColor Gray
    Write-Host "  .\start-docker.ps1 health          # Check service health" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Access Points:" -ForegroundColor Cyan
    Write-Host "  Orchestrator:      http://localhost:8001" -ForegroundColor Gray
    Write-Host "  MCP Server:        http://localhost:3000" -ForegroundColor Gray
    Write-Host "  IT Agent:          http://localhost:8002" -ForegroundColor Gray
    Write-Host "  K8s Agent:         http://localhost:8003" -ForegroundColor Gray
    Write-Host "  Inference Server:  http://localhost:8080" -ForegroundColor Gray
    Write-Host "  Grafana:           http://localhost:3001" -ForegroundColor Gray
    Write-Host "  Prometheus:        http://localhost:9090" -ForegroundColor Gray
    Write-Host "  Jaeger:            http://localhost:16686" -ForegroundColor Gray
    Write-Host ""
}

function Start-Platform {
    Write-Banner
    Write-Info "Starting containerized multi-agent platform..."
    Write-Host ""
    
    Write-Step "Building container images (this may take a few minutes)..."
    docker compose build
    
    Write-Host ""
    Write-Step "Starting all services..."
    docker compose up -d
    
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
    Write-Info "View logs with: .\start-docker.ps1 logs"
    Write-Info "Check status with: .\start-docker.ps1 ps"
    Write-Host ""
}

function Stop-Platform {
    Write-Banner
    Write-Info "Stopping all containers..."
    docker compose down
    Write-Host ""
    Write-Info "Platform stopped. Data volumes preserved."
    Write-Host "To remove volumes too, use: .\start-docker.ps1 clean"
    Write-Host ""
}

function Show-Status {
    Write-Banner
    Write-Info "Container Status:"
    Write-Host ""
    docker compose ps
    Write-Host ""
}

function Show-Logs {
    Write-Banner
    Write-Info "Container Logs (press Ctrl+C to exit):"
    Write-Host ""
    
    if ($args.Count -gt 0) {
        $service = $args[0]
        Write-Info "Showing logs for: $service"
        docker compose logs -f $service
    }
    else {
        Write-Info "Showing logs for all services"
        docker compose logs -f
    }
}

function Restart-Platform {
    Write-Banner
    Write-Info "Restarting all containers..."
    docker compose restart
    Write-Host ""
    Write-Info "Platform restarted!"
    Write-Host ""
}

function Build-Platform {
    Write-Banner
    Write-Info "Rebuilding all container images..."
    Write-Host ""
    docker compose build --no-cache
    Write-Host ""
    Write-Info "Build complete! Start with: .\start-docker.ps1 up"
    Write-Host ""
}

function Clean-Platform {
    Write-Banner
    Write-Host "⚠️  WARNING: This will remove all containers, images, and volumes!" -ForegroundColor Red
    Write-Host ""
    $confirm = Read-Host "Continue? (yes/no)"
    
    if ($confirm -eq "yes") {
        Write-Info "Stopping and removing all containers..."
        docker compose down -v --rmi all
        
        Write-Info "Pruning Docker system..."
        docker system prune -f
        
        Write-Host ""
        Write-Info "Cleanup complete!"
    }
    else {
        Write-Info "Cleanup cancelled."
    }
    Write-Host ""
}

function Scale-Agents {
    Write-Banner
    Write-Info "Current agent configuration:"
    docker compose ps | Select-String "agent"
    Write-Host ""
    
    Write-Host "Scale agents:" -ForegroundColor Yellow
    Write-Host "Example: docker compose up -d --scale it-agent=3 --scale k8s-agent=2"
    Write-Host ""
    
    $itAgents = Read-Host "Number of IT agents (default: 1)"
    $k8sAgents = Read-Host "Number of K8s agents (default: 1)"
    
    if ([string]::IsNullOrEmpty($itAgents)) { $itAgents = "1" }
    if ([string]::IsNullOrEmpty($k8sAgents)) { $k8sAgents = "1" }
    
    Write-Info "Scaling: IT agents=$itAgents, K8s agents=$k8sAgents"
    docker compose up -d --scale it-agent=$itAgents --scale k8s-agent=$k8sAgents
    
    Write-Host ""
    Write-Info "Agents scaled!"
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
        @{Name="Jaeger"; Url="http://localhost:16686"}
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
    Write-Info "Container health status:"
    docker ps --format "table {{.Names}}\t{{.Status}}"
    Write-Host ""
}

# Main execution
Write-Host ""

if (-not (Test-DockerAvailable)) {
    exit 1
}

if ($Command -ne "help" -and -not (Test-DockerRunning)) {
    exit 1
}

switch ($Command) {
    "up" { Start-Platform }
    "down" { Stop-Platform }
    "ps" { Show-Status }
    "logs" { Show-Logs @args }
    "restart" { Restart-Platform }
    "build" { Build-Platform }
    "clean" { Clean-Platform }
    "scale" { Scale-Agents }
    "health" { Check-Health }
    "help" { Show-Help }
    default { Show-Help }
}
