# Getting Started with Agentic Development Environment

Welcome! This guide will help you get up and running with the Agentic Development Environment demo.

## What You'll Build

This demo showcases a production-ready agentic architecture featuring:

- ✅ **Autonomous AI Agents** that decompose and execute multi-step tasks
- ✅ **Model Context Protocol (MCP)** for standardized tool integration
- ✅ **Specification-Driven Development** with living documentation
- ✅ **Security-Hardened Dev Containers** for safe agent execution
- ✅ **Full Observability** with metrics, logs, and distributed tracing
- ✅ **Real-World Use Cases** (IT automation, Kubernetes diagnostics)

## 🚀 5-Minute Quick Start

### Option 1: Windows PowerShell (Recommended)

```powershell
# 1. Navigate to the project
cd C:\Users\julio.sanchez\agentic-vscode-demo

# 2. Show available commands
.\start-demo.ps1 help

# 3. Start everything
.\start-demo.ps1 all

# 4. Run a demo (in new terminal)
.\start-demo.ps1 laptop
```

### Option 2: Manual Steps

```powershell
# Terminal 1: Start MCP Server
python mcp-server/server.py

# Terminal 2: Run a demo
python examples/laptop_refresh.py
```

## 📁 Project Structure

```
agentic-vscode-demo/
├── agent/                    # Agent orchestration engine
│   └── orchestrator.py       # Main agent logic
├── mcp-server/               # MCP server implementation
│   └── server.py             # Tool registry and execution
├── examples/                 # Demo scenarios
│   ├── laptop_refresh.py     # IT automation demo
│   └── k8s_diagnostics.py    # Kubernetes troubleshooting
├── observability/            # Monitoring stack
│   ├── prometheus.yml        # Metrics config
│   ├── traces.py             # OpenTelemetry setup
│   └── docker-compose.yml    # Observability services
├── .devcontainer/            # Dev container configuration
├── .vscode/                  # VS Code settings (optimized for demos)
└── docs/                     # Documentation
```

## 🎯 Demo Scenarios

### 1. Laptop Refresh Automation

**What it demonstrates:**
- Human-in-the-loop agentic workflow
- Policy validation and compliance checking
- ServiceNow ticket automation
- Knowledge base integration

**How to run:**

```powershell
python examples/laptop_refresh.py

# With different scenarios
python examples/laptop_refresh.py --scenarios

# For specific user
python examples/laptop_refresh.py --user jane.smith@example.com
```

**What you'll see:**

```
======================================================================
📋 Task Plan: Laptop Refresh Automation
======================================================================
Steps (5 total):
⏳ Step 1: Query laptop refresh policy [query_policy]
⏳ Step 2: Validate user eligibility against policy
⏳ Step 3: Search for laptop refresh procedures [search_documentation]
⏳ Step 4: Create ServiceNow ticket [create_ticket]
⏳ Step 5: Verify ticket was created successfully
======================================================================

🤔 Execute this plan? (yes/no): 
```

### 2. Kubernetes Diagnostics

**What it demonstrates:**
- Cloud-native resource management
- Autonomous root cause analysis
- Log analysis and error detection
- Automated remediation suggestions

**How to run:**

```powershell
python examples/k8s_diagnostics.py --interactive

# Or directly diagnose a pod
python examples/k8s_diagnostics.py --pod backend-service-abc

# Health check mode
python examples/k8s_diagnostics.py --health-check
```

**What you'll see:**

The agent will:
1. List all pods in the namespace
2. Identify failing pods (CrashLoopBackOff)
3. Fetch logs showing the error
4. Describe the deployment configuration
5. Identify root cause (missing DATABASE_URL)
6. Suggest remediation steps
7. Create tracking ticket

## 🔧 Configuration

### MCP Server Configuration

The MCP server provides tools to the agent. Available tools:

**Kubernetes Tools:**
- `list_pods` - List pods in a namespace
- `get_pod_logs` - Retrieve pod logs
- `describe_resource` - Get resource details

**ServiceNow Tools:**
- `create_ticket` - Create IT ticket
- `get_ticket_status` - Check ticket status

**Knowledge Base Tools:**
- `query_policy` - Query organizational policies
- `search_documentation` - Search internal docs

### Adding Custom Tools

Edit `mcp-server/server.py`:

```python
class MyCustomTools:
    @staticmethod
    async def my_tool(param: str) -> Dict[str, Any]:
        """Your tool implementation"""
        return {"result": "success", "data": param}

# Register in /tools endpoint
tools.append({
    "name": "my_tool",
    "description": "My custom tool",
    "category": "custom",
    "parameters": {...}
})

# Route in /execute endpoint
elif call.tool_name == "my_tool":
    result = await MyCustomTools.my_tool(**call.arguments)
```

## 📊 Observability

### Starting the Monitoring Stack

```powershell
cd observability
docker-compose up -d
```

### Accessing Dashboards

- **Prometheus**: http://localhost:9090
  - Query metrics: `http_requests_total`, `agent_task_duration_seconds`
  
- **Grafana**: http://localhost:3001
  - Username: `admin`
  - Password: `admin`
  
- **Jaeger**: http://localhost:16686
  - View distributed traces
  - Search by service: `agentic-orchestrator`

### Key Metrics to Watch

```promql
# Task success rate
sum(rate(agent_task_completed_total[5m])) / sum(rate(agent_task_total[5m]))

# Average task duration
rate(agent_task_duration_seconds_sum[5m]) / rate(agent_task_duration_seconds_count[5m])

# Tool call latency (P95)
histogram_quantile(0.95, rate(tool_execution_duration_seconds_bucket[5m]))
```

## 🔐 Security Features

This demo implements enterprise security best practices:

### Dev Container Hardening

```json
{
  "runArgs": [
    "--cap-drop=ALL",              // Drop all Linux capabilities
    "--security-opt=no-new-privileges"  // Prevent privilege escalation
  ],
  "remoteUser": "vscode",          // Run as non-root user
}
```

### Input Validation

- All agent inputs pass through validation
- Tool parameters are type-checked
- SQL injection prevention
- Command injection prevention

### Audit Logging

Every action is logged with:
- Timestamp
- User/agent identifier
- Operation performed
- Result status
- Error details (if any)

## 🎓 Learning Path

### Beginner

1. ✅ Run the simple demo
2. ✅ Explore the laptop refresh example
3. ✅ Understand task decomposition
4. ✅ Review MCP tool definitions

### Intermediate

1. ✅ Add a custom MCP tool
2. ✅ Create a new task type
3. ✅ Modify the orchestrator logic
4. ✅ Set up observability stack

### Advanced

1. ✅ Integrate with real OpenShift cluster
2. ✅ Implement custom authentication
3. ✅ Add LLM-based planning
4. ✅ Deploy to production

## 📚 Documentation

- **[Quick Start](docs/QUICKSTART.md)** - Get running in 5 minutes
- **[Architecture](docs/ARCHITECTURE.md)** - Deep dive into system design
- **[MCP Guide](docs/MCP_GUIDE.md)** - Protocol details (coming soon)
- **[Security](docs/SECURITY.md)** - Best practices (coming soon)
- **[Observability README](observability/README.md)** - Monitoring guide

## 🐛 Troubleshooting

### MCP Server Won't Start

**Error**: Port 3000 already in use

```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process
taskkill /PID <PID> /F
```

### Examples Fail with Connection Error

**Error**: `Failed to connect to MCP server`

**Solution**: Make sure MCP server is running:

```powershell
# Check if server is running
curl http://localhost:3000

# Start server if not running
python mcp-server/server.py
```

### Container Build Fails

**Error**: Docker build error

```powershell
# Clear Docker cache
docker system prune -a

# Rebuild container
# In VS Code: F1 → "Dev Containers: Rebuild Container"
```

### Import Errors

**Error**: `ModuleNotFoundError`

```powershell
# Reinstall dependencies
pip install -r requirements.txt
```

## 💡 Tips & Best Practices

### Demo Presentation

1. **Use Preview Mode**: Review plans before execution
   ```powershell
   python agent/orchestrator.py --task laptop-refresh --preview
   ```

2. **Zen Mode**: For focused demos
   - Press `Ctrl+K Z` in VS Code
   - Hides all sidebars
   - Return with `Esc Esc`

3. **Font Size**: Already configured to 18px for readability
   - See `.vscode/settings.json`

### Development Workflow

1. **Test Tools Independently**:
   ```powershell
   curl -X POST http://localhost:3000/execute -H "Content-Type: application/json" -d '{
     "tool_name": "list_pods",
     "arguments": {"namespace": "default"}
   }'
   ```

2. **Use Tracing**: Enable for debugging
   ```python
   from observability.traces import get_tracer
   tracer = get_tracer()
   
   with tracer.trace_operation("my_operation"):
       # Your code here
   ```

3. **Check Metrics**: Monitor performance
   ```promql
   # In Prometheus
   rate(agent_task_duration_seconds_sum[5m])
   ```

## 🤝 Next Steps

1. **Explore the Code**:
   - Read through `agent/orchestrator.py`
   - Understand `mcp-server/server.py`
   - Review example implementations

2. **Customize**:
   - Add your own tools
   - Create custom workflows
   - Integrate with your systems

3. **Deploy**:
   - Connect to OpenShift cluster
   - Set up production monitoring
   - Enable authentication

4. **Learn More**:
   - Read the architecture guide
   - Watch demo videos (coming soon)
   - Join the community (coming soon)

## 🌟 What Makes This Special

Unlike simple chatbot demos, this showcases:

- **Production-Ready Architecture** - Not just a prototype
- **Real Tool Integration** - Actual Kubernetes and ServiceNow APIs
- **Security First** - Hardened containers and validation
- **Observable** - Full metrics, logs, and traces
- **Extensible** - Easy to add new capabilities
- **Specification-Driven** - Plans before execution

## 📞 Getting Help

- **Documentation**: Check `/docs` folder
- **Logs**: Review agent and MCP server logs
- **Metrics**: Use Prometheus for debugging
- **Traces**: Jaeger for request flow visualization

---

**Ready to start?** Run `.\start-demo.ps1 all` and explore! 🚀
