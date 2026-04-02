#!/usr/bin/env python3
"""
BatteryML Multi-Role Agent Team Runner
电池ML多角色智能体团队运行脚本

Usage:
    python run_agent_team.py                    # Run full analysis and print summary
    python run_agent_team.py --export report.json  # Export to JSON
"""

import argparse
import logging
import sys

# Add project root to path
sys.path.insert(0, '.')

from batteryml.agents.team import BatteryMLAgentTeam


def main():
    parser = argparse.ArgumentParser(
        description='BatteryML Multi-Role Agent Team Analysis'
    )
    parser.add_argument(
        '--export', type=str, default=None,
        help='Export full report to JSON file'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Enable verbose logging'
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )

    # Initialize the team
    team = BatteryMLAgentTeam()

    print(f"Initialized team with {len(team.team.agents)} agents:")
    for role, agent in team.team.agents.items():
        print(f"  • {agent.name} ({role.value})")
    print()

    # Run full analysis
    result = team.run_full_analysis()

    # Print executive summary
    team.print_executive_summary()

    # Export if requested
    if args.export:
        team.export_report(args.export)
        print(f"\nFull report exported to: {args.export}")

    # Print statistics
    print(f"\n--- Statistics ---")
    print(f"Total agents: {result['agents_count']}")
    print(f"Total findings: {result['total_findings']}")
    print(f"Total recommendations: {result['total_recommendations']}")
    print(f"Total risks: {result['total_risks']}")
    print(f"Total opportunities: {result['total_opportunities']}")
    print(f"Total action items: {len(result['action_items'])}")

    critical = result.get('critical_reports', [])
    if critical:
        print(f"\n⚠️  {len(critical)} CRITICAL priority reports require immediate attention!")


if __name__ == '__main__':
    main()
