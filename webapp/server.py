#!/usr/bin/env python3
"""
Web Application Server for Agentic Demo Environment
Provides an interactive UI for launching and monitoring demos
"""

import os
import subprocess
import json
import logging
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn
import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agentic Development Environment - Web Interface")

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent

class DemoRequest(BaseModel):
    demo_type: str
    options: dict = {}

class ServerStatus(BaseModel):
    service: str
    status: str
    url: str = None
    message: str = None

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main web interface"""
    html_path = PROJECT_ROOT / "webapp" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/execution", response_class=HTMLResponse)
async def read_execution():
    """Serve the execution page"""
    html_path = PROJECT_ROOT / "webapp" / "execution.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/status")
async def get_status():
    """Get status of all services"""
    statuses = []
    
    # Check MCP Server
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:3000", timeout=2)
            if response.status_code == 200:
                data = response.json()
                statuses.append(ServerStatus(
                    service="MCP Server",
                    status="running",
                    url="http://localhost:3000",
                    message=f"Version {data.get('version', 'unknown')}"
                ))
            else:
                statuses.append(ServerStatus(
                    service="MCP Server",
                    status="error",
                    message=f"HTTP {response.status_code}"
                ))
    except Exception as e:
        statuses.append(ServerStatus(
            service="MCP Server",
            status="stopped",
            message="Not responding on port 3000"
        ))
    
    return {"statuses": [s.dict() for s in statuses], "timestamp": datetime.now().isoformat()}

@app.post("/api/start-mcp")
async def start_mcp_server():
    """Start the MCP server"""
    try:
        # Check if already running
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:3000", timeout=2)
                if response.status_code == 200:
                    return {"status": "already_running", "message": "MCP Server is already running"}
        except:
            pass
        
        # Start the server
        server_path = PROJECT_ROOT / "mcp-server" / "server.py"
        process = subprocess.Popen(
            ["python", str(server_path)],
            cwd=str(PROJECT_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        
        # Wait a bit for startup
        import asyncio
        await asyncio.sleep(3)
        
        # Verify it started
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:3000", timeout=2)
                if response.status_code == 200:
                    return {
                        "status": "started",
                        "message": "MCP Server started successfully",
                        "pid": process.pid
                    }
        except:
            pass
            
        return {
            "status": "error",
            "message": "Server started but not responding"
        }
        
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/launch-demo")
async def launch_demo(request: DemoRequest):
    """Launch a specific demo"""
    try:
        demo_type = request.demo_type
        
        if demo_type == "laptop":
            script_path = PROJECT_ROOT / "examples" / "laptop_refresh.py"
            demo_name = "Laptop Refresh Automation"
        elif demo_type == "k8s":
            script_path = PROJECT_ROOT / "examples" / "k8s_diagnostics.py"
            demo_name = "Kubernetes Diagnostics"
        else:
            raise HTTPException(status_code=400, detail="Invalid demo type")
        
        # Launch in new terminal/console
        if os.name == 'nt':  # Windows
            cmd = f'start "Agentic Demo - {demo_name}" cmd /k python "{script_path}"'
            if demo_type == "k8s":
                cmd = f'start "Agentic Demo - {demo_name}" cmd /k python "{script_path}" --interactive'
            subprocess.Popen(cmd, shell=True, cwd=str(PROJECT_ROOT))
        else:  # Unix-like
            subprocess.Popen(
                ["xterm", "-e", f"python {script_path}"],
                cwd=str(PROJECT_ROOT)
            )
        
        return {
            "status": "launched",
            "demo": demo_name,
            "message": f"Demo launched in new terminal window"
        }
        
    except Exception as e:
        logger.error(f"Failed to launch demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tools")
async def get_available_tools():
    """Get list of available MCP tools"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:3000/tools", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=503, detail="MCP Server not available")
    except Exception as e:
        raise HTTPException(status_code=503, detail="Cannot connect to MCP Server")

@app.get("/api/demos")
async def get_demo_info():
    """Get information about available demos"""
    demos = [
        {
            "id": "laptop",
            "name": "Laptop Refresh Automation",
            "description": "IT self-service automation demonstrating human-in-the-loop workflow",
            "features": [
                "Policy validation and compliance checking",
                "ServiceNow ticket automation",
                "Knowledge base integration",
                "Human approval workflow"
            ],
            "steps": [
                "Query organizational laptop refresh policy",
                "Validate user eligibility against policy rules",
                "Search knowledge base for procedures",
                "Create ServiceNow ticket automatically",
                "Verify ticket creation and notify user"
            ],
            "duration": "2-3 minutes",
            "difficulty": "Beginner"
        },
        {
            "id": "k8s",
            "name": "Kubernetes Diagnostics",
            "description": "Cloud-native troubleshooting with autonomous root cause analysis",
            "features": [
                "Automatic pod health detection",
                "Log analysis and error identification",
                "Resource configuration review",
                "Remediation suggestions",
                "Tracking ticket creation"
            ],
            "steps": [
                "List all pods in namespace",
                "Identify failing pods (CrashLoopBackOff)",
                "Fetch and analyze pod logs",
                "Describe deployment configuration",
                "Identify root cause (e.g., missing env vars)",
                "Suggest remediation steps",
                "Create tracking ticket"
            ],
            "duration": "3-4 minutes",
            "difficulty": "Intermediate"
        }
    ]
    return {"demos": demos}

if __name__ == "__main__":
    logger.info("Starting Agentic Development Environment Web Interface...")
    logger.info("Web UI will be available at: http://localhost:8080")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
