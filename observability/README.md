# Observability Stack

Monitoring and tracing infrastructure for the agentic development environment.

## Components

### Prometheus (Port 9090)
- Metrics collection and storage
- Scrapes metrics from MCP server, agent, and inference services
- Query language (PromQL) for analysis

### Grafana (Port 3001)
- Dashboard visualization
- Alert management
- Default credentials: admin/admin

### Jaeger (Port 16686)
- Distributed tracing
- OTLP collector
- Trace visualization and analysis

### Node Exporter (Port 9100)
- System metrics (CPU, memory, disk, network)
- Host-level monitoring

## Quick Start

### 1. Start Observability Stack

```bash
cd observability
docker-compose up -d
```

### 2. Access Dashboards

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)
- **Jaeger**: http://localhost:16686

### 3. Verify Services

```bash
# Check all services are running
docker-compose ps

# View logs
docker-compose logs -f
```

## Key Metrics

### Agent Performance

- `agent_task_duration_seconds` - Task execution time
- `agent_step_total` - Total steps executed
- `agent_step_failures_total` - Failed steps
- `agent_tool_calls_total` - Tool invocations

### MCP Server

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `tool_execution_duration_seconds` - Tool execution time
- `tool_errors_total` - Tool execution errors

### Inference (vLLM)

- `ttft_seconds` - Time To First Token
- `tpot_seconds` - Time Per Output Token
- `kv_cache_hit_rate` - Cache hit percentage
- `gpu_memory_utilization` - GPU memory usage

## Sample Queries

### Prometheus QL Examples

```promql
# Average task duration
rate(agent_task_duration_seconds_sum[5m]) / rate(agent_task_duration_seconds_count[5m])

# Tool call success rate
sum(rate(tool_execution_total{status="success"}[5m])) / sum(rate(tool_execution_total[5m]))

# P95 MCP server latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# KV cache hit rate (if available)
rate(kv_cache_hits_total[1m]) / rate(kv_cache_requests_total[1m])
```

## Distributed Tracing

### View Traces

1. Open Jaeger UI: http://localhost:16686
2. Select service: `agentic-orchestrator`
3. Click "Find Traces"

### Trace Attributes

- `service.name` - Service identifier
- `operation.type` - Operation category (tool_call, step_execution, etc.)
- `tool.name` - Tool that was invoked
- `step.id` - Step number in workflow
- `error` - Boolean indicating failure
- `prompt_tokens` - Token count (if available)

### Example Trace Flow

```
Workflow: laptop-refresh
├── Step 1: Query policy [query_policy]
│   └── Duration: 45ms
├── Step 2: Validate eligibility
│   └── Duration: 12ms
├── Step 3: Search documentation [search_documentation]
│   └── Duration: 78ms
└── Step 4: Create ticket [create_ticket]
    └── Duration: 156ms
Total: 291ms
```

## Alerting

### Configure Alerts

Create alert rules in `prometheus/alerts/`:

```yaml
groups:
  - name: agent_alerts
    rules:
      - alert: HighAgentFailureRate
        expr: |
          rate(agent_step_failures_total[5m]) / rate(agent_step_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High agent failure rate detected"
```

### Alert Destinations

Configure in Grafana:
- Notification Channels → Add Channel
- Supports: Email, Slack, PagerDuty, Webhook

## Dashboard Import

Pre-built dashboards in `grafana/dashboards/`:

1. Agent Performance
2. MCP Server Metrics
3. Inference Performance (vLLM)
4. System Resources

Import via Grafana UI or auto-provision through configuration.

## Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs prometheus
docker-compose logs grafana

# Restart services
docker-compose restart
```

### No Metrics Appearing

1. Verify Prometheus targets: http://localhost:9090/targets
2. Check firewall rules
3. Ensure services expose metrics endpoints

### Grafana Connection Issues

- Default URL: http://localhost:3001
- Check datasource configuration in Grafana
- Verify Prometheus is accessible from Grafana container

## Production Considerations

For production deployments:

1. **Persistent Storage**: Configure volume mounts for data retention
2. **Security**: Change default passwords, enable HTTPS
3. **High Availability**: Run multiple Prometheus instances
4. **Long-term Storage**: Configure remote write to Thanos/Cortex
5. **Resource Limits**: Set memory/CPU limits in docker-compose
6. **Retention Policies**: Configure data retention periods

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [OpenTelemetry](https://opentelemetry.io/)
