#!/usr/bin/env python3
"""
Agent Orchestrator
Autonomous task execution with multi-step decomposition and planning

Implements:
- Task Decomposition: Breaking complex requests into manageable steps
- Planning Mode: Preview actions before execution
- Tool Discovery: Dynamic MCP tool usage
- State Management: Track progress across workflows
- Error Recovery: Intelligent retry and fallback strategies

Based on agentic workflow patterns and functional specification
"""

import asyncio
import argparse
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import httpx


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Step:
    """Represents a single step in a task workflow"""
    
    def __init__(
        self,
        step_id: int,
        description: str,
        tool_name: Optional[str] = None,
        arguments: Optional[Dict[str, Any]] = None,
        depends_on: Optional[List[int]] = None
    ):
        self.step_id = step_id
        self.description = description
        self.tool_name = tool_name
        self.arguments = arguments or {}
        self.depends_on = depends_on or []
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.started_at = None
        self.completed_at = None
    
    def __repr__(self):
        return f"Step({self.step_id}: {self.description} - {self.status.value})"
    
    def to_dict(self):
        """Convert step to dictionary for display"""
        return {
            "id": self.step_id,
            "description": self.description,
            "status": self.status.value,
            "tool": self.tool_name,
            "result": self.result if self.status == TaskStatus.COMPLETED else None
        }


class TaskPlan:
    """Represents a complete task execution plan"""
    
    def __init__(self, task_name: str, description: str):
        self.task_name = task_name
        self.description = description
        self.steps: List[Step] = []
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
    
    def add_step(self, step: Step):
        """Add a step to the plan"""
        self.steps.append(step)
    
    def get_next_steps(self) -> List[Step]:
        """Get steps that are ready to execute (dependencies satisfied)"""
        ready_steps = []
        completed_ids = {s.step_id for s in self.steps if s.status == TaskStatus.COMPLETED}
        
        for step in self.steps:
            if step.status == TaskStatus.PENDING:
                if all(dep_id in completed_ids for dep_id in step.depends_on):
                    ready_steps.append(step)
        
        return ready_steps
    
    def is_complete(self) -> bool:
        """Check if all steps are completed"""
        return all(
            s.status in (TaskStatus.COMPLETED, TaskStatus.SKIPPED)
            for s in self.steps
        )
    
    def has_failures(self) -> bool:
        """Check if any steps failed"""
        return any(s.status == TaskStatus.FAILED for s in self.steps)
    
    def display_plan(self):
        """Display the execution plan"""
        print(f"\n{'='*70}")
        print(f"📋 Task Plan: {self.task_name}")
        print(f"{'='*70}")
        print(f"Description: {self.description}")
        print(f"\nSteps ({len(self.steps)} total):")
        print(f"{'-'*70}")
        
        for step in self.steps:
            status_emoji = {
                TaskStatus.PENDING: "⏳",
                TaskStatus.IN_PROGRESS: "▶️",
                TaskStatus.COMPLETED: "✅",
                TaskStatus.FAILED: "❌",
                TaskStatus.SKIPPED: "⏭️"
            }
            emoji = status_emoji.get(step.status, "❓")
            
            deps = f" (depends on: {step.depends_on})" if step.depends_on else ""
            tool = f" [{step.tool_name}]" if step.tool_name else ""
            
            print(f"{emoji} Step {step.step_id}: {step.description}{tool}{deps}")
        
        print(f"{'='*70}\n")


class MCPClient:
    """Client for communicating with MCP server"""
    
    def __init__(self, server_url: str = "http://localhost:3000"):
        self.server_url = server_url
        self.tools_cache = None
    
    async def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools from MCP server"""
        if self.tools_cache:
            return self.tools_cache
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.server_url}/tools", timeout=10.0)
                response.raise_for_status()
                self.tools_cache = response.json()
                logger.info(f"Discovered {len(self.tools_cache)} tools from MCP server")
                return self.tools_cache
        except Exception as e:
            logger.error(f"Failed to discover tools: {e}")
            return []
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool via MCP server"""
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "tool_name": tool_name,
                    "arguments": arguments
                }
                response = await client.post(
                    f"{self.server_url}/execute",
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                
                if not result.get("success"):
                    raise Exception(result.get("error", "Unknown error"))
                
                return result.get("data")
        
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            raise


class AgentOrchestrator:
    """Main agent orchestrator for autonomous task execution"""
    
    def __init__(self, mcp_server_url: str = "http://localhost:3000"):
        self.mcp_client = MCPClient(mcp_server_url)
        self.current_plan: Optional[TaskPlan] = None
    
    async def decompose_task(self, task_name: str, context: Dict[str, Any] = None) -> TaskPlan:
        """
        Decompose a high-level task into executable steps
        
        This is where the "intelligence" of the agent lives.
        In a production system, this would use an LLM to analyze the task
        and generate appropriate steps.
        """
        logger.info(f"Decomposing task: {task_name}")
        
        context = context or {}
        
        # Task-specific decomposition logic
        if task_name == "laptop-refresh":
            return await self._decompose_laptop_refresh(context)
        elif task_name == "k8s-diagnose":
            return await self._decompose_k8s_diagnostics(context)
        elif task_name == "simple-demo":
            return await self._decompose_simple_demo(context)
        else:
            raise ValueError(f"Unknown task type: {task_name}")
    
    async def _decompose_laptop_refresh(self, context: Dict[str, Any]) -> TaskPlan:
        """Decompose laptop refresh automation task"""
        user = context.get("user", "john.doe@example.com")
        
        plan = TaskPlan(
            task_name="Laptop Refresh Automation",
            description=f"Automate laptop refresh request for user: {user}"
        )
        
        # Step 1: Query policy
        plan.add_step(Step(
            step_id=1,
            description="Query laptop refresh policy",
            tool_name="query_policy",
            arguments={"policy_type": "laptop_refresh", "user_id": user}
        ))
        
        # Step 2: Validate eligibility (depends on step 1)
        plan.add_step(Step(
            step_id=2,
            description="Validate user eligibility against policy",
            tool_name=None,  # Internal logic, no tool needed
            depends_on=[1]
        ))
        
        # Step 3: Search for documentation
        plan.add_step(Step(
            step_id=3,
            description="Search for laptop refresh procedures",
            tool_name="search_documentation",
            arguments={"query": "laptop refresh process", "max_results": 3},
            depends_on=[1]
        ))
        
        # Step 4: Create ServiceNow ticket (depends on validation)
        plan.add_step(Step(
            step_id=4,
            description="Create ServiceNow ticket for laptop refresh",
            tool_name="create_ticket",
            arguments={
                "title": f"Laptop Refresh Request - {user}",
                "description": "Automated laptop refresh request based on eligibility verification",
                "category": "Hardware",
                "priority": "3",
                "requester": user
            },
            depends_on=[2]
        ))
        
        # Step 5: Verify ticket creation
        plan.add_step(Step(
            step_id=5,
            description="Verify ticket was created successfully",
            tool_name=None,
            depends_on=[4]
        ))
        
        return plan
    
    async def _decompose_k8s_diagnostics(self, context: Dict[str, Any]) -> TaskPlan:
        """Decompose Kubernetes diagnostics task"""
        namespace = context.get("namespace", "default")
        pod_name = context.get("pod_name")
        
        plan = TaskPlan(
            task_name="Kubernetes Diagnostics",
            description=f"Diagnose issues with pod: {pod_name or 'all pods'}"
        )
        
        # Step 1: List pods
        plan.add_step(Step(
            step_id=1,
            description=f"List all pods in namespace: {namespace}",
            tool_name="list_pods",
            arguments={"namespace": namespace}
        ))
        
        # Step 2: Identify problematic pod
        plan.add_step(Step(
            step_id=2,
            description="Identify pods with issues (not Running status)",
            tool_name=None,
            depends_on=[1]
        ))
        
        if pod_name:
            # Step 3: Get logs from specific pod
            plan.add_step(Step(
                step_id=3,
                description=f"Retrieve logs from pod: {pod_name}",
                tool_name="get_pod_logs",
                arguments={"pod_name": pod_name, "namespace": namespace, "lines": 50},
                depends_on=[2]
            ))
            
            # Step 4: Describe the resource
            plan.add_step(Step(
                step_id=4,
                description=f"Describe deployment/pod details: {pod_name}",
                tool_name="describe_resource",
                arguments={
                    "resource_type": "deployment",
                    "name": pod_name.rsplit('-', 2)[0],  # Extract deployment name
                    "namespace": namespace
                },
                depends_on=[3]
            ))
            
            # Step 5: Analyze and suggest fix
            plan.add_step(Step(
                step_id=5,
                description="Analyze logs and resource config to identify root cause",
                tool_name=None,
                depends_on=[3, 4]
            ))
            
            # Step 6: Create remediation ticket if needed
            plan.add_step(Step(
                step_id=6,
                description="Create ticket for manual remediation if required",
                tool_name="create_ticket",
                arguments={
                    "title": f"Pod Issue: {pod_name}",
                    "description": "Automated diagnostics found issues requiring attention",
                    "category": "Infrastructure",
                    "priority": "2"
                },
                depends_on=[5]
            ))
        
        return plan
    
    async def _decompose_simple_demo(self, context: Dict[str, Any]) -> TaskPlan:
        """Simple demo task for testing"""
        plan = TaskPlan(
            task_name="Simple Demo",
            description="Demonstrate basic agent capabilities"
        )
        
        plan.add_step(Step(
            step_id=1,
            description="List pods in default namespace",
            tool_name="list_pods",
            arguments={"namespace": "default"}
        ))
        
        plan.add_step(Step(
            step_id=2,
            description="Query laptop refresh policy",
            tool_name="query_policy",
            arguments={"policy_type": "laptop_refresh"}
        ))
        
        return plan
    
    async def execute_plan(self, plan: TaskPlan, preview_only: bool = False) -> bool:
        """
        Execute a task plan
        
        Args:
            plan: TaskPlan to execute
            preview_only: If True, only display the plan without executing
            
        Returns:
            True if execution was successful, False otherwise
        """
        self.current_plan = plan
        
        # Display the plan
        plan.display_plan()
        
        if preview_only:
            logger.info("Preview mode - plan not executed")
            return True
        
        # Ask for confirmation
        confirmation = input("\n🤔 Execute this plan? (yes/no): ").strip().lower()
        if confirmation not in ['yes', 'y']:
            logger.info("Execution cancelled by user")
            return False
        
        print(f"\n{'='*70}")
        print("🚀 Starting Execution")
        print(f"{'='*70}\n")
        
        plan.started_at = datetime.now()
        
        # Execute steps
        max_iterations = len(plan.steps) * 2  # Prevent infinite loops
        iteration = 0
        
        while not plan.is_complete() and not plan.has_failures() and iteration < max_iterations:
            iteration += 1
            next_steps = plan.get_next_steps()
            
            if not next_steps:
                logger.warning("No steps ready to execute but plan not complete")
                break
            
            # Execute ready steps (could be parallel, but keeping sequential for clarity)
            for step in next_steps:
                await self._execute_step(step)
                
                # Small delay for readability
                await asyncio.sleep(0.5)
        
        plan.completed_at = datetime.now()
        
        # Display results
        self._display_results(plan)
        
        return not plan.has_failures()
    
    async def _execute_step(self, step: Step):
        """Execute a single step"""
        step.status = TaskStatus.IN_PROGRESS
        step.started_at = datetime.now()
        
        print(f"\n▶️  Executing Step {step.step_id}: {step.description}")
        
        try:
            if step.tool_name:
                # Execute tool via MCP
                logger.info(f"Calling tool: {step.tool_name} with args: {step.arguments}")
                result = await self.mcp_client.execute_tool(step.tool_name, step.arguments)
                step.result = result
                
                # Display relevant result info
                if isinstance(result, dict):
                    self._display_step_result(step, result)
            else:
                # Internal logic step (simplified for demo)
                step.result = {"status": "completed", "note": "Internal processing"}
                print(f"   ✓ Internal processing completed")
            
            step.status = TaskStatus.COMPLETED
            step.completed_at = datetime.now()
            print(f"   ✅ Step {step.step_id} completed successfully\n")
        
        except Exception as e:
            step.status = TaskStatus.FAILED
            step.error = str(e)
            step.completed_at = datetime.now()
            logger.error(f"Step {step.step_id} failed: {e}")
            print(f"   ❌ Step {step.step_id} failed: {e}\n")
    
    def _display_step_result(self, step: Step, result: Dict[str, Any]):
        """Display relevant information from step result"""
        # Customize display based on tool
        if step.tool_name == "list_pods":
            count = result.get("count", 0)
            print(f"   📊 Found {count} pods")
            for pod in result.get("pods", [])[:3]:  # Show first 3
                status_emoji = "✅" if pod["status"] == "Running" else "❌"
                print(f"      {status_emoji} {pod['name']}: {pod['status']}")
        
        elif step.tool_name == "get_pod_logs":
            lines = result.get("lines", 0)
            print(f"   📝 Retrieved {lines} log lines")
            # Show last few lines
            logs = result.get("logs", "").split('\n')
            for line in logs[-3:]:
                if line.strip():
                    print(f"      {line}")
        
        elif step.tool_name == "create_ticket":
            ticket_num = result.get("ticket_number")
            print(f"   🎫 Created ticket: {ticket_num}")
            print(f"      Status: {result.get('status')}")
            print(f"      URL: {result.get('url')}")
        
        elif step.tool_name == "query_policy":
            title = result.get("title", "Policy")
            print(f"   📚 Retrieved: {title}")
            if "eligibility" in result:
                print(f"      Eligibility criteria found")
        
        else:
            # Generic display
            print(f"   ✓ Result: {json.dumps(result, indent=2)[:200]}...")
    
    def _display_results(self, plan: TaskPlan):
        """Display final execution results"""
        duration = (plan.completed_at - plan.started_at).total_seconds()
        
        print(f"\n{'='*70}")
        print("📊 Execution Summary")
        print(f"{'='*70}")
        print(f"Task: {plan.task_name}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"Steps: {len(plan.steps)} total")
        
        completed = sum(1 for s in plan.steps if s.status == TaskStatus.COMPLETED)
        failed = sum(1 for s in plan.steps if s.status == TaskStatus.FAILED)
        
        print(f"  ✅ Completed: {completed}")
        print(f"  ❌ Failed: {failed}")
        
        if plan.has_failures():
            print(f"\n❌ Execution FAILED")
            print("Failed steps:")
            for step in plan.steps:
                if step.status == TaskStatus.FAILED:
                    print(f"  - Step {step.step_id}: {step.description}")
                    print(f"    Error: {step.error}")
        else:
            print(f"\n✅ Execution SUCCESSFUL")
        
        print(f"{'='*70}\n")


# ============================================
# MAIN ENTRY POINT
# ============================================

async def main():
    """Main entry point for agent orchestrator"""
    parser = argparse.ArgumentParser(description="Agent Orchestrator for Agentic Workflows")
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        choices=["laptop-refresh", "k8s-diagnose", "simple-demo"],
        help="Task to execute"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview plan without executing"
    )
    parser.add_argument(
        "--user",
        type=str,
        default="john.doe@example.com",
        help="User email (for laptop-refresh task)"
    )
    parser.add_argument(
        "--pod",
        type=str,
        help="Pod name (for k8s-diagnose task)"
    )
    parser.add_argument(
        "--namespace",
        type=str,
        default="default",
        help="Kubernetes namespace"
    )
    parser.add_argument(
        "--mcp-server",
        type=str,
        default="http://localhost:3000",
        help="MCP server URL"
    )
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(mcp_server_url=args.mcp_server)
    
    # Prepare context
    context = {
        "user": args.user,
        "namespace": args.namespace
    }
    if args.pod:
        context["pod_name"] = args.pod
    
    try:
        # Decompose task into plan
        plan = await orchestrator.decompose_task(args.task, context)
        
        # Execute plan
        success = await orchestrator.execute_plan(plan, preview_only=args.preview)
        
        exit(0 if success else 1)
    
    except Exception as e:
        logger.error(f"Orchestration failed: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
