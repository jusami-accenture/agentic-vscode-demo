# Agentic Development Environment Demo

A working demonstration of an integrated agentic architecture for Visual Studio Code, implementing concepts from specification-driven development, Model Context Protocol (MCP), and autonomous AI agents.

## 🎯 Overview

This demo showcases:

- **Specification-Driven Development (SDD)**: Living specification documents that guide agent behavior
- **Model Context Protocol (MCP)**: Standardized tool integration for AI agents
- **Autonomous Task Orchestration**: Multi-step task decomposition and execution
- **Dev Container Security**: Hardened containerized development environment
- **Observability**: Monitoring and tracing for agentic workflows
- **OpenShift Integration**: Cloud-native resource management concepts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VS Code IDE Interface                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐      ┌──────────────┐    ┌──────────────┐ │
│  │   Agent     │◄─────┤ MCP Client   │◄───┤   User       │ │
│  │ Orchestrator│      │   Layer      │    │  Interface   │ │
│  └──────┬──────┘      └──────────────┘    └──────────────┘ │
│         │                                                    │
│         │ Tools & Resources                                 │
│         ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           MCP Server (stdio/HTTP)                   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  • Kubernetes Tools    • File Operations            │   │
│  │  • ServiceNow API      • Policy Validation          │   │
│  │  • Logging & Metrics   • Knowledge Base             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │   OpenShift AI / vLLM       │
              │   (Inference Infrastructure) │
              └─────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Visual Studio Code (version 1.80+)
- Docker Desktop or Podman
- Python 3.12+
- Node.js 22+

### 1. Open in Dev Container

```bash
# Clone and open in VS Code
cd agentic-vscode-demo
code .

# In VS Code, press F1 and select:
# "Dev Containers: Reopen in Container"
```

### 2. Run the Demo

```bash
# Start the MCP server
python mcp-server/server.py

# In another terminal, run the agent demo
python agent/orchestrator.py --task laptop-refresh
```

### 3. Explore Use Cases

See `/examples` directory for:
- **Laptop Refresh Automation** - IT self-service workflow
- **Cloud-Native Diagnostics** - Kubernetes troubleshooting
- **Multi-Step Task Execution** - Complex workflow orchestration

## 📁 Project Structure

```
agentic-vscode-demo/
├── .devcontainer/           # Dev container configuration
│   ├── devcontainer.json    # Container metadata & settings
│   └── Dockerfile           # Hardened container image
├── .vscode/                 # VS Code settings for demos
│   └── settings.json        # Optimized presentation configuration
├── agent/                   # Agent orchestration system
│   ├── orchestrator.py      # Main agent logic
│   ├── task_decomposer.py   # Task breakdown engine
│   └── planner.py           # Planning mode implementation
├── mcp-server/              # MCP server implementation
│   ├── server.py            # MCP server (stdio)
│   ├── tools/               # Tool definitions
│   │   ├── kubernetes.py    # K8s resource management
│   │   ├── servicenow.py    # Ticket management
│   │   └── knowledge.py     # Policy & docs lookup
│   └── resources/           # MCP resources
│       └── cache_metrics.py # KV cache statistics
├── examples/                # Demo scenarios
│   ├── laptop_refresh.py    # Use case 1
│   ├── k8s_diagnostics.py   # Use case 2
│   └── spec_driven_dev.py   # SDD workflow
├── observability/           # Monitoring setup
│   ├── prometheus.yml       # Metrics collection
│   ├── grafana/             # Dashboard definitions
│   └── traces.py            # OpenTelemetry setup
├── specs/                   # Living specifications
│   ├── spec.md              # System specification
│   └── plan.md              # Implementation plan
└── README.md                # This file
```

## 🔧 Key Components

### Agent Orchestrator

The agent orchestrator implements autonomous task execution with:

- **Task Decomposition**: Breaks complex requests into manageable steps
- **Planning Mode**: Previews actions before execution
- **Tool Discovery**: Dynamically finds and uses MCP tools
- **State Management**: Tracks progress across multi-step workflows
- **Error Recovery**: Handles failures and retries intelligently

### MCP Server

Implements the Model Context Protocol providing:

- **Tools**: Executable functions (e.g., `list_pods`, `create_ticket`)
- **Resources**: Read-only data access (e.g., `cache_metrics`, `policy_docs`)
- **Prompts**: Reusable templates for common tasks
- **Progressive Context Loading**: 98.7% reduction in token overhead

### Dev Container

Security-hardened development environment:

- Non-root user execution
- Dropped kernel capabilities (`cap_drop: [ALL]`)
- Restricted privilege escalation
- Isolated network namespace
- Reproducible build environment

## 📊 Observability

The demo includes monitoring for:

- **Inference Metrics**: TTFT (Time To First Token), cache hit rates
- **Agent Performance**: Task completion time, tool call accuracy
- **Distributed Tracing**: Full request traces with OpenTelemetry
- **Resource Utilization**: GPU memory, CPU, network

Access dashboards:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)

## 🎮 Demo Scenarios

### Scenario 1: Autonomous Laptop Refresh

```bash
python agent/orchestrator.py --task laptop-refresh --user "john.doe@example.com"
```

Flow:
1. User requests laptop refresh via Slack/email
2. Agent recognizes intent and retrieves user profile
3. Validates eligibility against policy knowledge base
4. Creates ServiceNow ticket automatically
5. Validates compliance using DeepEval framework

### Scenario 2: Kubernetes Diagnostics

```bash
python agent/orchestrator.py --task k8s-diagnose --pod "frontend-service-xyz"
```

Flow:
1. Agent detects failing pod
2. Fetches logs using MCP Kubernetes tool
3. Identifies missing environment variable
4. Proposes fix to Deployment manifest
5. Applies fix and verifies pod recovery
6. Checks Grafana for performance stability

## 🔒 Security

Following enterprise security best practices:

- **Content Moderation**: LlamaGuard integration for input/output filtering
- **Injection Prevention**: PromptGuard detects malicious prompts
- **Minimal Privileges**: Agents run with least-required permissions
- **Audit Logging**: All agent actions are logged with timestamps
- **Multi-Tenant Isolation**: Workload separation on shared infrastructure

## 📖 Documentation

- [Architecture Deep Dive](docs/ARCHITECTURE.md)
- [MCP Integration Guide](docs/MCP_GUIDE.md)
- [Security Best Practices](docs/SECURITY.md)
- [OpenShift Deployment](docs/OPENSHIFT.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🎓 Learning Path

1. **Start Simple**: Run the laptop refresh example
2. **Explore MCP**: Add custom tools to the MCP server
3. **Build Agents**: Create new task orchestration workflows
4. **Add Observability**: Integrate custom metrics and traces
5. **Deploy to OpenShift**: Scale the demo to production

## 🤝 Contributing

This demo is designed for exploration and extension. Key areas to explore:

- Add new MCP tools for your environment
- Implement additional use cases
- Enhance observability with custom metrics
- Integrate with your OpenShift cluster
- Experiment with different LLM backends

## 📚 References

Based on the comprehensive functional specification incorporating:

- VS Code Agent Mode with MCP support
- Red Hat OpenShift AI with vLLM inference
- llm-d distributed inference framework
- Specification-Driven Development methodology
- Enterprise security and observability patterns

## 📝 License

MIT License - See LICENSE file for details

---

**Note**: This is a demonstration environment designed for learning and exploration. For production deployments, refer to the security hardening guidelines and consult with your platform team.
