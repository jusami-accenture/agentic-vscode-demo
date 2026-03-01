"""
OpenTelemetry Tracing Setup
Distributed tracing for agentic workflows

Implements:
- Span instrumentation for agent operations
- Service overview and performance tracking
- Tool call tracing with input/output capture
- Error tracking and reporting

Based on observability requirements from functional specification
"""

import logging
from typing import Dict, Any, Optional
from contextlib import contextmanager
from datetime import datetime

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False
    logging.warning("OpenTelemetry not available - tracing disabled")


logger = logging.getLogger(__name__)


class TracingConfig:
    """Configuration for OpenTelemetry tracing"""
    
    # Service identification
    SERVICE_NAME = "agentic-orchestrator"
    SERVICE_VERSION = "1.0.0"
    ENVIRONMENT = "development"
    
    # OTLP endpoint (Jaeger, Tempo, etc.)
    OTLP_ENDPOINT = "http://localhost:4317"
    
    # Console export for demo purposes
    CONSOLE_EXPORT = True
    
    # Sampling rate (1.0 = 100%)
    SAMPLING_RATE = 1.0


def initialize_tracing(
    service_name: str = TracingConfig.SERVICE_NAME,
    console_export: bool = TracingConfig.CONSOLE_EXPORT
) -> Optional[trace.Tracer]:
    """
    Initialize OpenTelemetry tracing
    
    Args:
        service_name: Name of the service
        console_export: Whether to export to console for debugging
        
    Returns:
        Tracer instance or None if OpenTelemetry not available
    """
    if not OTEL_AVAILABLE:
        logger.warning("OpenTelemetry not installed - tracing disabled")
        return None
    
    # Create resource with service information
    resource = Resource.create({
        "service.name": service_name,
        "service.version": TracingConfig.SERVICE_VERSION,
        "deployment.environment": TracingConfig.ENVIRONMENT
    })
    
    # Create tracer provider
    provider = TracerProvider(resource=resource)
    
    # Add console exporter for demo
    if console_export:
        console_exporter = ConsoleSpanExporter()
        provider.add_span_processor(BatchSpanProcessor(console_exporter))
    
    # Add OTLP exporter (if endpoint available)
    try:
        otlp_exporter = OTLPSpanExporter(endpoint=TracingConfig.OTLP_ENDPOINT)
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        logger.info(f"OTLP tracing enabled: {TracingConfig.OTLP_ENDPOINT}")
    except Exception as e:
        logger.warning(f"OTLP exporter not available: {e}")
    
    # Set global tracer provider
    trace.set_tracer_provider(provider)
    
    # Get tracer
    tracer = trace.get_tracer(__name__)
    logger.info(f"Tracing initialized for service: {service_name}")
    
    return tracer


def instrument_fastapi(app):
    """
    Instrument FastAPI application with OpenTelemetry
    
    Args:
        app: FastAPI application instance
    """
    if not OTEL_AVAILABLE:
        return
    
    try:
        FastAPIInstrumentor.instrument_app(app)
        logger.info("FastAPI instrumented with OpenTelemetry")
    except Exception as e:
        logger.error(f"Failed to instrument FastAPI: {e}")


class AgentTracer:
    """
    Wrapper for tracing agent operations
    Provides convenient methods for common tracing patterns
    """
    
    def __init__(self, tracer: Optional[trace.Tracer] = None):
        self.tracer = tracer or (trace.get_tracer(__name__) if OTEL_AVAILABLE else None)
        self.enabled = self.tracer is not None
    
    @contextmanager
    def trace_operation(
        self,
        operation_name: str,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """
        Context manager for tracing an operation
        
        Usage:
            with tracer.trace_operation("decompose_task", {"task": "laptop-refresh"}):
                # ... operation code ...
        """
        if not self.enabled or not self.tracer:
            yield None
            return
        
        with self.tracer.start_as_current_span(operation_name) as span:
            # Add custom attributes
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, str(value))
            
            # Add timestamp
            span.set_attribute("timestamp", datetime.now().isoformat())
            
            try:
                yield span
            except Exception as e:
                # Record exception
                span.set_attribute("error", True)
                span.set_attribute("error.type", type(e).__name__)
                span.set_attribute("error.message", str(e))
                span.record_exception(e)
                raise
    
    def trace_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        parent_span=None
    ):
        """
        Trace a tool call
        
        Args:
            tool_name: Name of the tool being called
            arguments: Tool arguments
            parent_span: Optional parent span
            
        Returns:
            Context manager for the tool call span
        """
        attributes = {
            "tool.name": tool_name,
            "tool.arguments": str(arguments),
            "operation.type": "tool_call"
        }
        
        return self.trace_operation(f"tool:{tool_name}", attributes)
    
    def trace_step_execution(
        self,
        step_id: int,
        description: str,
        tool_name: Optional[str] = None
    ):
        """
        Trace a step execution
        
        Args:
            step_id: Step identifier
            description: Step description
            tool_name: Optional tool name
            
        Returns:
            Context manager for the step span
        """
        attributes = {
            "step.id": step_id,
            "step.description": description,
            "operation.type": "step_execution"
        }
        
        if tool_name:
            attributes["tool.name"] = tool_name
        
        return self.trace_operation(f"step:{step_id}", attributes)
    
    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """
        Add an event to the current span
        
        Args:
            name: Event name
            attributes: Event attributes
        """
        if not self.enabled:
            return
        
        current_span = trace.get_current_span()
        if current_span:
            current_span.add_event(name, attributes or {})


# Global tracer instance
_global_tracer: Optional[AgentTracer] = None


def get_tracer() -> AgentTracer:
    """
    Get the global agent tracer instance
    
    Returns:
        AgentTracer instance
    """
    global _global_tracer
    
    if _global_tracer is None:
        otel_tracer = initialize_tracing()
        _global_tracer = AgentTracer(otel_tracer)
    
    return _global_tracer


# Decorator for tracing functions
def traced(operation_name: Optional[str] = None):
    """
    Decorator for tracing functions
    
    Usage:
        @traced("my_operation")
        def my_function():
            pass
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            tracer = get_tracer()
            op_name = operation_name or func.__name__
            
            with tracer.trace_operation(op_name):
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Example usage
if __name__ == "__main__":
    # Initialize tracing
    tracer = get_tracer()
    
    # Example: Trace a multi-step operation
    with tracer.trace_operation("demo_workflow", {"task_id": "demo-123"}):
        # Step 1
        with tracer.trace_step_execution(1, "Query policy", "query_policy"):
            print("Querying policy...")
            tracer.add_event("policy_retrieved", {"policy_type": "laptop_refresh"})
        
        # Step 2
        with tracer.trace_tool_call("create_ticket", {"title": "Demo Ticket"}):
            print("Creating ticket...")
            tracer.add_event("ticket_created", {"ticket_number": "INC12345"})
    
    print("\n✅ Tracing demo complete - check console output for traces")
