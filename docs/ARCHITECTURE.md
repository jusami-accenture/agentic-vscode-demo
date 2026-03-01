# Architecture Deep Dive

Comprehensive technical architecture of the Agentic Development Environment.

## System Overview

The system implements a **specification-driven agentic architecture** with three main layers:

1. **Presentation Layer**: VS Code IDE with enhanced agent interface
2. **Orchestration Layer**: Agent task decomposition and execution engine
3. **Integration Layer**: Model Context Protocol (MCP) for tool access
4. **Infrastructure Layer**: OpenShift AI with vLLM inference (optional)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     VS Code IDE (Frontend)                       │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │  Editor    │  │   Terminal   │  │  Agent Chat Interface  │  │
│  │  Windows   │  │   Panels     │  │  (Copilot/Custom)      │  │
│  └────────────┘  └──────────────┘  └────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               Agent Orchestration Layer                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Task Decomposer                                         │   │
│  │  - Analyze user request                                  │   │
│  │  - Break into executable steps                           │   │
│  │  - Determine dependencies                                │   │
│  └────────────────────┬─────────────────────────────────────┘   │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐   │
│  │  Planner                                                  │   │
│  │  - Create execution plan                                 │   │
│  │  - Preview mode for human review                         │   │
│  │  - Manage step dependencies                              │   │
│  └────────────────────┬─────────────────────────────────────┘   │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐   │
│  │  Executor                                                 │   │
│  │  - Execute steps sequentially/parallel                   │   │
│  │  - Handle errors and retries                             │   │
│  │  - Maintain state across steps                           │   │
│  └────────────────────┬─────────────────────────────────────┘   │
└───────────────────────┼─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│           Model Context Protocol (MCP) Layer                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  MCP Client (in Agent)                                    │   │
│  │  - Tool discovery                                         │   │
│  │  - Tool invocation                                        │   │
│  │  - Result handling                                        │   │
│  └────────────────────┬─────────────────────────────────────┘   │
│                       │                                          │
│                       ▼                                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  MCP Server (HTTP/stdio)                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │   │
│  │  │  Kubernetes  │  │  ServiceNow  │  │  Knowledge   │   │   │
│  │  │  Tools       │  │  Tools       │  │  Base Tools  │   │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                  External Systems                                │
│  ┌───────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ OpenShift │  │ ServiceNow│ │ Databases │ │  API         │   │
│  │ Cluster   │  │ Instance  │ │           │ │  Services    │   │
│  └───────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              Observability Layer (Cross-Cutting)                 │
│  ┌─────────────┐  ┌──────────┐  ┌──────────────┐               │
│  │ Prometheus  │  │ Grafana  │  │ OpenTelemetry│               │
│  │ (Metrics)   │  │ (Viz)    │  │ (Traces)     │               │
│  └─────────────┘  └──────────┘  └──────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Agent Orchestrator

**Purpose**: Autonomous task execution engine

**Key Classes**:

```python
class AgentOrchestrator:
    - decompose_task()      # Break down high-level tasks
    - execute_plan()        # Run execution plan
    - _execute_step()       # Execute individual steps
```

**Responsibilities**:
- Parse user intent
- Generate execution plans
- Manage step dependencies
- Handle errors and retries
- Track execution state

**Design Patterns**:
- **Strategy Pattern**: Different decomposition strategies per task type
- **Chain of Responsibility**: Step execution pipeline
- **Observer Pattern**: Status updates to UI
- **State Pattern**: Task lifecycle management

### 2. Task Planner

**Purpose**: Create and manage execution plans

**Key Classes**:

```python
class TaskPlan:
    - add_step()           # Add step to plan
    - get_next_steps()     # Get ready-to-execute steps
    - is_complete()        # Check completion status

class Step:
    - step_id              # Unique identifier
    - tool_name            # MCP tool to invoke
    - depends_on           # Dependency list
    - status               # Execution status
```

**Features**:
- Dependency resolution (DAG-based)
- Preview mode (human-in-the-loop)
- Progress tracking
- Failure handling

**Step States**:
```
PENDING → IN_PROGRESS → COMPLETED
   ↓                        ↑
   └─────→ FAILED → RETRY ──┘
```

### 3. MCP Integration

**Purpose**: Standardized tool access protocol

**Architecture**:

```
┌────────────────────────────────────────┐
│         MCP Client (Agent)              │
│  - Tool discovery                       │
│  - Request formatting                   │
│  - Response parsing                     │
└──────────────┬─────────────────────────┘
               │ HTTP/JSON
               ▼
┌────────────────────────────────────────┐
│         MCP Server                      │
│  ┌────────────────────────────────┐    │
│  │  Tool Registry                  │    │
│  │  - list_pods                    │    │
│  │  - get_pod_logs                 │    │
│  │  - create_ticket                │    │
│  │  - query_policy                 │    │
│  └────────────────────────────────┘    │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  Tool Executor                  │    │
│  │  - Route to implementation      │    │
│  │  - Validate parameters          │    │
│  │  - Handle errors                │    │
│  └────────────────────────────────┘    │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  Tool Implementations           │    │
│  │  - KubernetesTools              │    │
│  │  - ServiceNowTools              │    │
│  │  - KnowledgeBaseTools           │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

**Tool Definition Format**:

```json
{
  "name": "list_pods",
  "description": "List Kubernetes pods in a namespace",
  "category": "kubernetes",
  "parameters": {
    "type": "object",
    "properties": {
      "namespace": {"type": "string", "default": "default"},
      "label_selector": {"type": "string", "optional": true}
    }
  }
}
```

**Benefits**:
- **Progressive Context Loading**: Only load needed tools (98.7% token reduction)
- **Standardization**: Uniform interface for all tools
- **Discoverability**: Dynamic tool discovery
- **Extensibility**: Easy to add new tools

### 4. Security Architecture

**Defense in Depth Strategy**:

```
┌─────────────────────────────────────────────────┐
│  Layer 1: Container Security                    │
│  - Non-root user execution                       │
│  - Dropped capabilities (cap_drop: ALL)         │
│  - No new privileges (security-opt)             │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│  Layer 2: Input Validation                      │
│  - LlamaGuard content moderation                │
│  - PromptGuard injection detection              │
│  - Parameter validation                         │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│  Layer 3: Authorization                         │
│  - RBAC for Kubernetes operations               │
│  - Service account tokens                       │
│  - Scoped permissions                           │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│  Layer 4: Audit Logging                         │
│  - All operations logged                        │
│  - Distributed tracing                          │
│  - Immutable audit trail                        │
└─────────────────────────────────────────────────┘
```

### 5. Data Flow

**Request Flow Example**: Laptop Refresh

```
1. User Request
   ↓
   "I need a new laptop"

2. Intent Recognition (Agent)
   ↓
   Task: "laptop-refresh"
   Context: {user: "jane.doe@example.com"}

3. Task Decomposition
   ↓
   Plan:
   - Step 1: Query policy [query_policy]
   - Step 2: Validate eligibility
   - Step 3: Search docs [search_documentation]
   - Step 4: Create ticket [create_ticket]

4. Human Review (Preview Mode)
   ↓
   User confirms: YES

5. Execution
   ↓
   Step 1: MCP call to query_policy
           ↓
           Response: Policy retrieved
   
   Step 2: Internal validation
           ↓
           Result: User eligible
   
   Step 3: MCP call to search_documentation
           ↓
           Response: Docs found
   
   Step 4: MCP call to create_ticket
           ↓
           Response: Ticket INC20260228101530

6. Result Summary
   ↓
   Display: "✅ Ticket created: INC20260228101530"
```

### 6. Observability Architecture

**Three Pillars**:

```
┌───────────────────────────────────────────────────┐
│  METRICS (Prometheus)                              │
│  - Task duration                                   │
│  - Step success/failure rates                      │
│  - Tool invocation counts                          │
│  - Resource utilization                            │
└───────────────────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────┐
│  LOGS (Structured Logging)                         │
│  - Timestamp                                       │
│  - Level (INFO, WARN, ERROR)                       │
│  - Component (orchestrator, mcp, tool)             │
│  - Message                                         │
│  - Context (task_id, step_id)                      │
└───────────────────────────────────────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────────┐
│  TRACES (OpenTelemetry)                            │
│  - Span: Task execution                            │
│    ├─ Span: Step 1 execution                       │
│    │  └─ Span: Tool call (query_policy)            │
│    ├─ Span: Step 2 execution                       │
│    └─ Span: Step 3 execution                       │
│       └─ Span: Tool call (create_ticket)           │
└───────────────────────────────────────────────────┘
```

**Correlation**:
- All three pillars linked by `task_id`
- Spans include metric attributes
- Logs attached to active spans
- End-to-end visibility

## Scalability Considerations

### Horizontal Scaling

**MCP Server**:
- Stateless design
- Load balancer in front
- Multiple replicas for HA

**Agent Orchestrator**:
- Queue-based task distribution
- Worker pool pattern
- Redis for shared state

### Performance Optimizations

1. **Tool Call Caching**: Cache frequent tool responses
2. **Parallel Execution**: Execute independent steps concurrently
3. **Connection Pooling**: Reuse HTTP connections
4. **Lazy Loading**: Load tools on-demand

## Extension Points

### Adding Custom Tool Categories

```python
# 1. Create tool class in mcp-server/tools/
class MyCustomTools:
    @staticmethod
    async def my_tool(param: str) -> Dict[str, Any]:
        return {"result": "success"}

# 2. Register in server.py
tools.append({
    "name": "my_tool",
    "category": "custom",
    "parameters": {...}
})

# 3. Route in execute endpoint
elif call.tool_name == "my_tool":
    result = await MyCustomTools.my_tool(**call.arguments)
```

### Adding Task Types

```python
# In agent/orchestrator.py
async def _decompose_my_task(self, context: Dict[str, Any]) -> TaskPlan:
    plan = TaskPlan("My Task", "Description")
    # Add steps...
    return plan

# Register in decompose_task()
elif task_name == "my-task":
    return await self._decompose_my_task(context)
```

## Production Deployment

### Infrastructure Requirements

```yaml
# Kubernetes resources
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: mcp-server
        image: mcp-server:latest
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
spec:
  type: LoadBalancer
  ports:
  - port: 3000
```

### High Availability

- **Multi-zone deployment**: Spread across availability zones
- **Database**: Postgres for persistent state
- **Cache**: Redis for performance
- **Monitoring**: 24/7 alerting

## References

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [OpenTelemetry](https://opentelemetry.io/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/)
- [vLLM Documentation](https://docs.vllm.ai/)
