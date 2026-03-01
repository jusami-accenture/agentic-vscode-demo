# PowerShell script to start the Agentic Demo Environment
# Usage: .\start-demo.ps1 [option]

param(
    [Parameter(Position=0)]
    [ValidateSet("server", "laptop", "k8s", "observability", "all", "webapp", "stop", "help")]
    [string]$Mode = "help"
)

$ErrorActionPreference = "Stop"

function Write-Banner {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "   Agentic Development Environment - Demo Launcher" -ForegroundColor Cyan
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

function Test-Dependencies {
    Write-Info "Checking dependencies..."
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Info "[OK] Python: $pythonVersion"
    }
    catch {
        Write-Error-Message "[ERROR] Python not found. Please install Python 3.12+"
        exit 1
    }
    
    # Check Docker (for observability)
    try {
        $dockerVersion = docker --version 2>&1
        Write-Info "[OK] Docker: $dockerVersion"
    }
    catch {
        Write-Warning "[WARNING] Docker not found. Observability stack won't be available."
    }
    
    Write-Host ""
}

function Start-MCPServer {
    Write-Step "Starting MCP Server..."
    Write-Info "MCP Server will run on http://localhost:3000"
    Write-Info "Press Ctrl+C to stop"
    Write-Host ""
    
    python mcp-server/server.py
}

function Start-LaptopRefreshDemo {
    Write-Step "Starting Laptop Refresh Demo..."
    Write-Host ""
    
    # Check if MCP server is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -ErrorAction SilentlyContinue
        Write-Info "[OK] MCP Server is running"
    }
    catch {
        Write-Error-Message "[ERROR] MCP Server not running. Please start it first:"
        Write-Host "   .\start-demo.ps1 server" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Or run in another terminal:" -ForegroundColor Yellow
        Write-Host "   python mcp-server/server.py" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host ""
    python examples/laptop_refresh.py
}

function Start-K8sDiagnosticsDemo {
    Write-Step "Starting Kubernetes Diagnostics Demo..."
    Write-Host ""
    
    # Check if MCP server is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -ErrorAction SilentlyContinue
        Write-Info "[OK] MCP Server is running"
    }
    catch {
        Write-Error-Message "[ERROR] MCP Server not running. Please start it first:"
        Write-Host "   .\start-demo.ps1 server" -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host ""
    python examples/k8s_diagnostics.py --interactive
}

function Start-ObservabilityStack {
    Write-Step "Starting Observability Stack..."
    Write-Info "This will start: Prometheus, Grafana, Jaeger"
    Write-Host ""
    
    if (-not (Test-Path "observability/docker-compose.yml")) {
        Write-Error-Message "docker-compose.yml not found in observability/"
        exit 1
    }
    
    Push-Location observability
    
    try {
        Write-Info "Starting containers..."
        docker-compose up -d
        
        Write-Host ""
        Write-Info "[OK] Observability stack started!"
        Write-Host ""
        Write-Host "Access dashboards:" -ForegroundColor Green
        Write-Host "  • Prometheus:  http://localhost:9090" -ForegroundColor Cyan
        Write-Host "  • Grafana:     http://localhost:3001 (admin/admin)" -ForegroundColor Cyan
        Write-Host "  • Jaeger:      http://localhost:16686" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "To stop: docker-compose down" -ForegroundColor Yellow
    }
    finally {
        Pop-Location
    }
}

function StartAll {
    Write-Banner
    Write-Step "Starting Complete Demo Environment..."
    Write-Host ""
    
    # Start observability (if Docker available)
    try {
        docker --version | Out-Null
        Start-ObservabilityStack
        Write-Host ""
    }
    catch {
        Write-Warning "Skipping observability stack (Docker not available)"
        Write-Host ""
    }
    
    # Start MCP server in background
    Write-Step "Starting MCP Server in background..."
    $mcpProcess = Start-Process python -ArgumentList "mcp-server/server.py" -PassThru -WindowStyle Hidden
    
    Write-Info "Waiting for MCP Server to start..."
    Start-Sleep -Seconds 3
    
    # Verify MCP server
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing
        Write-Info "[OK] MCP Server running (PID: $($mcpProcess.Id))"
    }
    catch {
        Write-Error-Message "Failed to start MCP Server"
        exit 1
    }
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "   Demo Environment Ready!" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Run demos:" -ForegroundColor Yellow
    Write-Host "  .\start-demo.ps1 laptop    # Laptop refresh automation" -ForegroundColor Cyan
    Write-Host "  .\start-demo.ps1 k8s       # Kubernetes diagnostics" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Access services:" -ForegroundColor Yellow
    Write-Host "  • MCP Server:  http://localhost:3000" -ForegroundColor Cyan
    Write-Host "  • Prometheus:  http://localhost:9090" -ForegroundColor Cyan
    Write-Host "  • Grafana:     http://localhost:3001" -ForegroundColor Cyan
    Write-Host "  • Jaeger:      http://localhost:16686" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "To stop MCP server:" -ForegroundColor Yellow
    Write-Host "  Stop-Process -Id $($mcpProcess.Id)" -ForegroundColor Cyan
    Write-Host ""
}

function Start-WebApp {
    Write-Banner
    Write-Step "Starting Web Interface..."
    Write-Info "Web UI will be available at http://localhost:8080"
    Write-Host ""
    
    python webapp/server.py
}

function Stop-All {
    Write-Banner
    Write-Step "Stopping all demo processes..."
    Write-Host ""
    
    # Stop Python processes
    $pythonProcs = Get-Process python -ErrorAction SilentlyContinue
    if ($pythonProcs) {
        Write-Info "Stopping Python processes..."
        $pythonProcs | Stop-Process -Force
        Write-Info "[OK] All Python processes stopped"
    } else {
        Write-Info "No Python processes running"
    }
    
    # Stop Docker containers if running
    if (Test-Path "observability/docker-compose.yml") {
        Push-Location observability
        try {
            $containers = docker-compose ps -q 2>$null
            if ($containers) {
                Write-Info "Stopping observability stack..."
                docker-compose down 2>$null
                Write-Info "[OK] Observability stack stopped"
            }
        }
        catch {
            # Docker not available or no containers
        }
        finally {
            Pop-Location
        }
    }
    
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "   All Demo Processes Stopped" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
}

function Show-Help {
    Write-Banner
    Write-Host "Usage: .\start-demo.ps1 [option]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Green
    Write-Host "  server         Start MCP server only" -ForegroundColor Cyan
    Write-Host "  webapp         Start web interface (http://localhost:8080)" -ForegroundColor Cyan
    Write-Host "  laptop         Run laptop refresh demo" -ForegroundColor Cyan
    Write-Host "  k8s            Run Kubernetes diagnostics demo" -ForegroundColor Cyan
    Write-Host "  observability  Start monitoring stack (Prometheus, Grafana, Jaeger)" -ForegroundColor Cyan
    Write-Host "  all            Start everything" -ForegroundColor Cyan
    Write-Host "  stop           Stop all running processes" -ForegroundColor Cyan
    Write-Host "  help           Show this help" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\start-demo.ps1 server          # Start MCP server" -ForegroundColor Gray
    Write-Host "  .\start-demo.ps1 laptop          # Run laptop demo" -ForegroundColor Gray
    Write-Host "  .\start-demo.ps1 all             # Start complete environment" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Manual Commands:" -ForegroundColor Green
    Write-Host "  python mcp-server/server.py               # Start MCP server" -ForegroundColor Gray
    Write-Host "  python examples/laptop_refresh.py         # Laptop demo" -ForegroundColor Gray
    Write-Host "  python examples/k8s_diagnostics.py        # K8s demo" -ForegroundColor Gray
    Write-Host "  python agent/orchestrator.py --help       # Agent help" -ForegroundColor Gray
    Write-Host ""
}

# Main execution
try {
    switch ($Mode) {
        "server" {
            Write-Banner
            Test-Dependencies
            Start-MCPServer
        }
        "laptop" {
            Write-Banner
            Test-Dependencies
            Start-LaptopRefreshDemo
        }
        "k8s" {
            Write-Banner
            Test-Dependencies
            Start-K8sDiagnosticsDemo
        }
        "observability" {
            Write-Banner
            Start-ObservabilityStack
        }
        "webapp" {
            Test-Dependencies
            Start-WebApp
        }
        "stop" {
            Stop-All
        }
        "all" {
            Test-Dependencies
            StartAll
        }
        default {
            Show-Help
        }
    }
}
catch {
    Write-Error-Message "An error occurred: $_"
    exit 1
}
