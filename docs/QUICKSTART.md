# Quick Start Guide

Get up and running with the Agentic Development Environment in minutes.

## Prerequisites

- **VS Code**: Version 1.80 or higher
- **Docker**: Docker Desktop or Podman
- **Git**: For cloning the repository
- **Python**: 3.12+ (for local development)
- **Node.js**: 22+ (optional, for MCP extensions)

## Installation

### 1. Clone the Repository

```bash
cd C:\Users\julio.sanchez
git clone https://github.com/your-org/agentic-vscode-demo.git
cd agentic-vscode-demo
```

### 2. Open in VS Code

```bash
code .
```

### 3. Start Dev Container

In VS Code:
1. Press `F1` or `Ctrl+Shift+P`
2. Type: `Dev Containers: Reopen in Container`
3. Wait for container to build (first time takes 2-3 minutes)

## Running Your First Demo

### Option A: Simple Demo (Recommended)

```bash
# Terminal 1: Start MCP server
python mcp-server/server.py

# Terminal 2: Run simple demo
python agent/orchestrator.py --task simple-demo --preview
```

### Option B: Laptop Refresh Demo

```bash
# Terminal 1: Start MCP server
python mcp-server/server.py

# Terminal 2: Run laptop refresh
python examples/laptop_refresh.py --user jane.doe@example.com
```

### Option C: Kubernetes Diagnostics

```bash
# Terminal 1: Start MCP server
python mcp-server/server.py

# Terminal 2: Run diagnostics
python examples/k8s_diagnostics.py --interactive
```

## Understanding the Output

### Planning Phase

The agent will display a workflow plan:

```
======================================================================
📋 Task Plan: Laptop Refresh Automation
======================================================================
Description: Automate laptop refresh request for user: jane.doe@example.com

Steps (5 total):
----------------------------------------------------------------------
⏳ Step 1: Query laptop refresh policy [query_policy]
⏳ Step 2: Validate user eligibility against policy
⏳ Step 3: Search for laptop refresh procedures [search_documentation]
⏳ Step 4: Create ServiceNow ticket for laptop refresh [create_ticket] (depends on: [2])
⏳ Step 5: Verify ticket was created successfully (depends on: [4])
======================================================================
```

### Execution Phase

Watch the agent execute each step:

```
▶️  Executing Step 1: Query laptop refresh policy
   📚 Retrieved: Laptop Refresh Policy
      Eligibility criteria found
   ✅ Step 1 completed successfully

▶️  Executing Step 2: Validate user eligibility against policy
   ✓ Internal processing completed
   ✅ Step 2 completed successfully
```

## Exploring the Environment

### 1. MCP Server

The MCP server provides tools for the agent:

```bash
# Check available tools
curl http://localhost:3000/tools | jq

# Execute a tool manually
curl -X POST http://localhost:3000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "list_pods",
    "arguments": {"namespace": "default"}
  }'
```

### 2. Agent Orchestrator

The agent orchestrator decomposes and executes tasks:

```bash
# Preview a plan without executing
python agent/orchestrator.py --task laptop-refresh --preview

# Execute with custom parameters
python agent/orchestrator.py --task k8s-diagnose \
  --pod backend-service-abc \
  --namespace production
```

### 3. Observability Stack

```bash
# Start monitoring services
cd observability
docker-compose up -d

# Access dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/admin)
# Jaeger: http://localhost:16686
```

## Common Commands

### Managing the Dev Container

```bash
# Rebuild container after changes
# F1 > Dev Containers: Rebuild Container

# View container logs
docker logs -f <container-name>

# Shell into running container
docker exec -it <container-name> bash
```

### Working with MCP Server

```bash
# Start in foreground
python mcp-server/server.py

# Start in background (PowerShell)
Start-Process python -ArgumentList "mcp-server/server.py" -WindowStyle Hidden

# Check if running
curl http://localhost:3000
```

### Running Examples

```bash
# Laptop refresh with scenarios
python examples/laptop_refresh.py --scenarios

# K8s diagnostics with guide
python examples/k8s_diagnostics.py --guide

# Health check
python examples/k8s_diagnostics.py --health-check
```

## Customization

### Adding New Tools

1. Edit `mcp-server/server.py`
2. Add tool class with async methods
3. Register in `/tools` endpoint
4. Route in `/execute` endpoint

Example:

```python
class CustomTools:
    @staticmethod
    async def my_new_tool(param1: str) -> Dict[str, Any]:
        """Your tool implementation"""
        return {"result": "success"}
```

### Creating New Tasks

1. Edit `agent/orchestrator.py`
2. Add decomposition method:

```python
async def _decompose_my_task(self, context: Dict[str, Any]) -> TaskPlan:
    plan = TaskPlan("My Custom Task", "Description")
    plan.add_step(Step(
        step_id=1,
        description="Do something",
        tool_name="my_new_tool",
        arguments={"param1": "value"}
    ))
    return plan
```

3. Register in `decompose_task` method

### Modifying VS Code Settings

Edit `.vscode/settings.json` for demo-specific preferences:

```json
{
  "editor.fontSize": 20,
  "editor.cursorStyle": "block",
  "workbench.colorCustomizations": {
    "editorCursor.foreground": "#ff0000"
  }
}
```

## Troubleshooting

### Port Already in Use

```bash
# Windows: Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Container Build Fails

```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
# F1 > Dev Containers: Rebuild Container (Without Cache)
```

### MCP Server Not Responding

```bash
# Check if server is running
curl http://localhost:3000

# View server logs
# Check terminal where server was started

# Restart server
# Ctrl+C in server terminal, then restart
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or in dev container
pip install --user -r requirements.txt
```

## Next Steps

1. **Explore Examples**: Try all demo scenarios
2. **Add Custom Tools**: Implement tools for your environment
3. **Create Workflows**: Design new task orchestrations
4. **Enable Monitoring**: Set up full observability stack
5. **Connect OpenShift**: Integrate with real cluster

## Learning Resources

- [Architecture Guide](docs/ARCHITECTURE.md) - System design
- [MCP Guide](docs/MCP_GUIDE.md) - Protocol details
- [Security Guide](docs/SECURITY.md) - Best practices
- [OpenShift Integration](docs/OPENSHIFT.md) - Cluster setup

## Getting Help

- Check logs: `docker-compose logs -f`
- Review documentation in `/docs`
- Inspect example code in `/examples`
- Debug with VS Code debugger (launch.json provided)

## Performance Tips

1. **Use Preview Mode**: Test plans before execution
2. **Monitor Resource Usage**: Check Docker Desktop
3. **Limit Tool Calls**: For faster iteration
4. **Cache Results**: Store frequently accessed data
5. **Parallel Execution**: Enable for independent steps (advanced)

---

**Ready to build?** Start with `python examples/laptop_refresh.py` and explore from there!
