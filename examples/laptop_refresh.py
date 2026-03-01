#!/usr/bin/env python3
"""
Example: Laptop Refresh Automation
Demonstrates autonomous IT self-service workflow

Scenario:
1. User requests laptop refresh via automated system
2. Agent recognizes intent and retrieves user profile
3. Validates eligibility against policy knowledge base
4. Creates ServiceNow ticket automatically
5. Validates compliance using policy framework

This example showcases:
- Human-in-the-loop agentic workflow
- MCP tool integration (ServiceNow, Knowledge Base)
- Policy validation and compliance checking
- Multi-step task orchestration
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from agent.orchestrator import AgentOrchestrator


async def run_laptop_refresh_demo(user_email: str = "john.doe@example.com"):
    """
    Run the laptop refresh automation demo
    
    This demonstrates how an agent can autonomously handle
    a structured IT process with policy validation and ticket creation.
    """
    
    print("="*70)
    print("🖥️  LAPTOP REFRESH AUTOMATION DEMO")
    print("="*70)
    print()
    print("Scenario: Employee requests new laptop")
    print(f"User: {user_email}")
    print()
    print("The agent will:")
    print("  1. Query organizational laptop refresh policy")
    print("  2. Validate user eligibility based on policy rules")
    print("  3. Search for relevant documentation")
    print("  4. Create ServiceNow ticket for hardware team")
    print("  5. Verify ticket creation and provide tracking info")
    print()
    print("="*70)
    print()
    
    input("Press Enter to start the demo...")
    print()
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(mcp_server_url="http://localhost:3000")
    
    # Prepare context
    context = {
        "user": user_email,
        "request_type": "laptop_refresh",
        "reason": "Current device is 3+ years old and experiencing performance issues"
    }
    
    try:
        # Decompose the task
        print("🤖 Agent analyzing request and creating execution plan...")
        print()
        plan = await orchestrator.decompose_task("laptop-refresh", context)
        
        # Execute the plan
        success = await orchestrator.execute_plan(plan, preview_only=False)
        
        if success:
            print("\n✅ SUCCESS: Laptop refresh request processed")
            print()
            print("Next Steps:")
            print("  - Manager approval will be requested")
            print("  - Hardware team will process within 2-3 business days")
            print("  - User will receive laptop selection options")
            print("  - Data migration will be scheduled")
            print()
        else:
            print("\n❌ FAILED: Could not complete laptop refresh request")
            print("Manual intervention required")
            print()
        
        return success
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


async def run_with_different_scenarios():
    """Run demo with different user scenarios"""
    
    scenarios = [
        {
            "user": "john.doe@example.com",
            "description": "Standard user - eligible for refresh"
        },
        {
            "user": "jane.smith@example.com",
            "description": "New employee - not yet eligible"
        },
        {
            "user": "manager@example.com",
            "description": "Manager - priority processing"
        }
    ]
    
    print("\n" + "="*70)
    print("🎯 MULTIPLE SCENARIO DEMO")
    print("="*70)
    print()
    print("Available scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario['description']}")
        print(f"   User: {scenario['user']}")
    print()
    
    choice = input("Select scenario (1-3) or press Enter for scenario 1: ").strip()
    
    if choice in ['2', '3']:
        idx = int(choice) - 1
        scenario = scenarios[idx]
    else:
        scenario = scenarios[0]
    
    print(f"\nRunning scenario: {scenario['description']}")
    print()
    
    return await run_laptop_refresh_demo(scenario['user'])


def print_policy_info():
    """Display policy information for context"""
    print("\n" + "="*70)
    print("📚 LAPTOP REFRESH POLICY (Reference)")
    print("="*70)
    print()
    print("Eligibility Requirements:")
    print("  • Minimum 12 months tenure with company")
    print("  • Current device is 3+ years old")
    print("  • Performance rating: Meets or Exceeds Expectations")
    print()
    print("Process:")
    print("  1. Submit request via IT portal or automated system")
    print("  2. Manager approval (automatic for eligible requests)")
    print("  3. IT verifies eligibility and device condition")
    print("  4. User selects device from approved catalog")
    print("  5. Data migration and setup scheduled")
    print()
    print("Timeline:")
    print("  • Approval: 2-3 business days")
    print("  • Delivery: 5-7 business days after approval")
    print()
    print("="*70)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Laptop Refresh Automation Demo")
    parser.add_argument(
        "--user",
        type=str,
        default="john.doe@example.com",
        help="User email address"
    )
    parser.add_argument(
        "--scenarios",
        action="store_true",
        help="Run multiple scenario demo"
    )
    parser.add_argument(
        "--show-policy",
        action="store_true",
        help="Show policy information"
    )
    
    args = parser.parse_args()
    
    if args.show_policy:
        print_policy_info()
    
    if args.scenarios:
        asyncio.run(run_with_different_scenarios())
    else:
        success = asyncio.run(run_laptop_refresh_demo(args.user))
        sys.exit(0 if success else 1)
