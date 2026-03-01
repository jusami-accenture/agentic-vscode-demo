#!/usr/bin/env python3
"""
Example: Kubernetes Diagnostics and Remediation
Demonstrates cloud-native diagnostic workflow

Scenario:
1. Developer identifies a failing pod in OpenShift
2. Agent investigates the failure autonomously
3. Agent fetches pod logs and resource descriptions
4. Identifies root cause (missing environment variable)
5. Proposes fix to deployment manifest
6. Creates remediation ticket if needed

This example showcases:
- Kubernetes/OpenShift integration via MCP
- Autonomous investigation and root cause analysis
- Multi-tool orchestration (logs, describe, create ticket)
- Intelligent error diagnosis
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from agent.orchestrator import AgentOrchestrator


async def run_k8s_diagnostics_demo(
    pod_name: str = "backend-service-abc",
    namespace: str = "default"
):
    """
    Run the Kubernetes diagnostics demo
    
    This demonstrates how an agent can autonomously diagnose
    and provide remediation guidance for failing Kubernetes pods.
    """
    
    print("="*70)
    print("🔍 KUBERNETES DIAGNOSTICS DEMO")
    print("="*70)
    print()
    print("Scenario: Production pod is failing")
    print(f"Pod: {pod_name}")
    print(f"Namespace: {namespace}")
    print()
    print("The agent will:")
    print("  1. List all pods in the namespace")
    print("  2. Identify pods with issues (not Running)")
    print("  3. Retrieve logs from the failing pod")
    print("  4. Describe the deployment configuration")
    print("  5. Analyze logs and config to find root cause")
    print("  6. Create remediation ticket with findings")
    print()
    print("="*70)
    print()
    
    input("Press Enter to start diagnostics...")
    print()
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(mcp_server_url="http://localhost:3000")
    
    # Prepare context
    context = {
        "pod_name": pod_name,
        "namespace": namespace,
        "alert_time": "2026-02-28 10:15:38",
        "alert_reason": "CrashLoopBackOff detected"
    }
    
    try:
        # Decompose the task
        print("🤖 Agent analyzing cluster state and creating diagnostic plan...")
        print()
        plan = await orchestrator.decompose_task("k8s-diagnose", context)
        
        # Execute the plan
        success = await orchestrator.execute_plan(plan, preview_only=False)
        
        if success:
            print("\n✅ DIAGNOSTICS COMPLETE")
            print()
            print("🔍 Root Cause Analysis:")
            print("  Issue: Missing environment variable 'DATABASE_URL'")
            print("  Impact: Application cannot start, resulting in CrashLoopBackOff")
            print()
            print("💡 Recommended Remediation:")
            print("  1. Add DATABASE_URL to deployment environment variables")
            print("  2. Verify database service is accessible")
            print("  3. Update deployment manifest:")
            print()
            print("     env:")
            print("       - name: DATABASE_URL")
            print("         value: postgresql://db-service:5432/appdb")
            print()
            print("  4. Apply changes: kubectl apply -f deployment.yaml")
            print()
            print("📋 Ticket created for tracking and manual review")
            print()
        else:
            print("\n⚠️  DIAGNOSTICS INCOMPLETE")
            print("Some steps failed - manual investigation required")
            print()
        
        return success
    
    except Exception as e:
        print(f"\n❌ Error during diagnostics: {e}")
        return False


async def run_cluster_health_check(namespace: str = "default"):
    """
    Run a general cluster health check
    
    Lists all pods and identifies any with issues
    """
    
    print("\n" + "="*70)
    print("🏥 CLUSTER HEALTH CHECK")
    print("="*70)
    print(f"Namespace: {namespace}")
    print()
    
    orchestrator = AgentOrchestrator(mcp_server_url="http://localhost:3000")
    
    try:
        # Create simple health check plan
        context = {"namespace": namespace}
        plan = await orchestrator.decompose_task("simple-demo", context)
        
        success = await orchestrator.execute_plan(plan, preview_only=False)
        
        if success:
            print("\n✅ Health check complete")
            print()
            print("Summary:")
            print("  • Frontend pods: Running ✅")
            print("  • Backend pods: Failing ❌ (requires attention)")
            print("  • Database pods: Running ✅")
            print()
            print("Recommendation: Investigate backend-service-abc")
            print()
        
        return success
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def print_troubleshooting_guide():
    """Display common Kubernetes troubleshooting patterns"""
    print("\n" + "="*70)
    print("📚 KUBERNETES TROUBLESHOOTING GUIDE")
    print("="*70)
    print()
    print("Common Pod Issues:")
    print()
    print("1. CrashLoopBackOff")
    print("   • Check logs: kubectl logs <pod-name>")
    print("   • Verify environment variables are set")
    print("   • Check resource limits (CPU/memory)")
    print("   • Verify image exists and is accessible")
    print()
    print("2. ImagePullBackOff")
    print("   • Verify image name and tag")
    print("   • Check registry credentials (imagePullSecrets)")
    print("   • Ensure network connectivity to registry")
    print()
    print("3. Pending Status")
    print("   • Check node resources (CPU/memory)")
    print("   • Verify persistent volume claims")
    print("   • Check node selectors and taints")
    print()
    print("4. Not Ready")
    print("   • Review readiness probe configuration")
    print("   • Check application startup time")
    print("   • Verify service dependencies")
    print()
    print("Agent Capabilities:")
    print("  • Automatically fetch logs and describe resources")
    print("  • Identify missing configuration")
    print("  • Cross-reference with documentation")
    print("  • Create tracking tickets")
    print("  • Suggest remediation steps")
    print()
    print("="*70)


async def interactive_mode():
    """Interactive mode for pod selection"""
    
    print("\n" + "="*70)
    print("🎮 INTERACTIVE DIAGNOSTICS MODE")
    print("="*70)
    print()
    
    # Simulated pod list
    pods = [
        {"name": "frontend-service-xyz", "status": "Running", "issue": False},
        {"name": "backend-service-abc", "status": "CrashLoopBackOff", "issue": True},
        {"name": "database-pod-def", "status": "Running", "issue": False}
    ]
    
    print("Available pods in 'default' namespace:")
    print()
    for i, pod in enumerate(pods, 1):
        status_emoji = "❌" if pod["issue"] else "✅"
        print(f"  {i}. {pod['name']}")
        print(f"     Status: {pod['status']} {status_emoji}")
    print()
    
    choice = input("Select pod to diagnose (1-3) or press Enter for pod 2: ").strip()
    
    if choice in ['1', '2', '3']:
        idx = int(choice) - 1
        selected_pod = pods[idx]
    else:
        selected_pod = pods[1]  # Default to failing pod
    
    print(f"\n🔍 Diagnosing: {selected_pod['name']}")
    print()
    
    return await run_k8s_diagnostics_demo(
        pod_name=selected_pod['name'],
        namespace="default"
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Kubernetes Diagnostics Demo")
    parser.add_argument(
        "--pod",
        type=str,
        help="Pod name to diagnose"
    )
    parser.add_argument(
        "--namespace",
        type=str,
        default="default",
        help="Kubernetes namespace"
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Run cluster health check"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive pod selection"
    )
    parser.add_argument(
        "--guide",
        action="store_true",
        help="Show troubleshooting guide"
    )
    
    args = parser.parse_args()
    
    if args.guide:
        print_troubleshooting_guide()
    
    if args.interactive:
        success = asyncio.run(interactive_mode())
    elif args.health_check:
        success = asyncio.run(run_cluster_health_check(args.namespace))
    else:
        pod = args.pod or "backend-service-abc"
        success = asyncio.run(run_k8s_diagnostics_demo(pod, args.namespace))
    
    sys.exit(0 if success else 1)
