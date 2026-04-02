"""
Base classes for the multi-role agent system.
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """All agent roles in the BatteryML analysis team."""
    MATERIAL_SCIENTIST = "material_scientist"
    DATA_SCIENTIST = "data_scientist"
    DATA_ANALYST_FRONTEND = "data_analyst_frontend_engineer"
    MARKETING_ENGINEER = "marketing_engineer"
    BATTERY_APPLICATION_ENGINEER = "battery_application_engineer"
    BATTERY_COMPANY_CEO = "battery_company_ceo"
    INVESTOR = "investor"
    MARKET_RESEARCHER = "market_researcher"
    END_USER = "end_user"
    PRODUCT_MANAGER = "product_manager"
    SOFTWARE_TEST_ENGINEER = "software_test_engineer"
    HARDWARE_TEST_ENGINEER = "hardware_test_engineer"
    MATERIAL_TEST_ENGINEER = "material_test_engineer"
    SALES_DEPARTMENT = "sales_department"
    MARKET_SURVEY = "market_survey"


@dataclass
class AnalysisReport:
    """A structured report produced by an agent."""
    agent_role: str
    agent_name: str
    summary: str
    findings: List[str]
    recommendations: List[str]
    risks: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    action_items: List[Dict[str, str]] = field(default_factory=list)
    priority: str = "medium"  # low, medium, high, critical
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_role': self.agent_role,
            'agent_name': self.agent_name,
            'summary': self.summary,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'risks': self.risks,
            'opportunities': self.opportunities,
            'action_items': self.action_items,
            'priority': self.priority,
            'metadata': self.metadata,
        }

    def to_json(self, indent=2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class BaseAgent(ABC):
    """Base class for all analysis agents."""

    def __init__(self, name: str, role: AgentRole, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.reports: List[AnalysisReport] = []

    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        """Perform analysis from this agent's perspective.

        Args:
            context: Project context including code structure, data,
                     configurations, and any prior analysis results.

        Returns:
            An AnalysisReport with findings and recommendations.
        """
        pass

    @abstractmethod
    def get_analysis_dimensions(self) -> List[str]:
        """Return the dimensions/aspects this agent analyzes."""
        pass

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        """Review other agents' reports and provide cross-functional feedback.

        Args:
            other_reports: Reports from other team agents.

        Returns:
            List of cross-functional insights or concerns.
        """
        return []

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', role={self.role.value})"


class AgentTeam:
    """Manages a team of agents for collaborative analysis."""

    def __init__(self, name: str):
        self.name = name
        self.agents: Dict[AgentRole, BaseAgent] = {}
        self._execution_order: List[AgentRole] = []

    def add_agent(self, agent: BaseAgent):
        """Add an agent to the team."""
        self.agents[agent.role] = agent
        if agent.role not in self._execution_order:
            self._execution_order.append(agent.role)

    def remove_agent(self, role: AgentRole):
        """Remove an agent from the team."""
        self.agents.pop(role, None)
        if role in self._execution_order:
            self._execution_order.remove(role)

    def set_execution_order(self, order: List[AgentRole]):
        """Set the order in which agents execute their analysis."""
        self._execution_order = order

    def run_analysis(self, context: Dict[str, Any]) -> Dict[AgentRole, AnalysisReport]:
        """Run analysis across all agents in order.

        Args:
            context: Project context shared among all agents.

        Returns:
            Dictionary mapping agent roles to their reports.
        """
        reports: Dict[AgentRole, AnalysisReport] = {}

        for role in self._execution_order:
            if role not in self.agents:
                continue
            agent = self.agents[role]
            logger.info(f"Running analysis: {agent.name} ({role.value})")

            # Provide accumulated reports as part of context
            enriched_context = {**context, 'prior_reports': reports}
            report = agent.analyze(enriched_context)
            reports[role] = report
            agent.reports.append(report)

        return reports

    def run_collaboration(
        self, reports: Dict[AgentRole, AnalysisReport]
    ) -> Dict[AgentRole, List[str]]:
        """Run cross-functional collaboration phase.

        Each agent reviews others' reports and provides feedback.

        Returns:
            Dictionary mapping agent roles to their cross-functional insights.
        """
        collaboration_insights: Dict[AgentRole, List[str]] = {}
        report_list = list(reports.values())

        for role, agent in self.agents.items():
            other_reports = [r for r in report_list if r.agent_role != role.value]
            insights = agent.collaborate(other_reports)
            if insights:
                collaboration_insights[role] = insights

        return collaboration_insights

    def generate_summary(
        self,
        reports: Dict[AgentRole, AnalysisReport],
        collaboration: Optional[Dict[AgentRole, List[str]]] = None,
    ) -> Dict[str, Any]:
        """Generate a consolidated team summary."""
        all_findings = []
        all_recommendations = []
        all_risks = []
        all_opportunities = []
        all_action_items = []

        for role, report in reports.items():
            all_findings.extend(
                [{'source': report.agent_name, 'finding': f} for f in report.findings]
            )
            all_recommendations.extend(
                [{'source': report.agent_name, 'recommendation': r}
                 for r in report.recommendations]
            )
            all_risks.extend(
                [{'source': report.agent_name, 'risk': r} for r in report.risks]
            )
            all_opportunities.extend(
                [{'source': report.agent_name, 'opportunity': o}
                 for o in report.opportunities]
            )
            all_action_items.extend(report.action_items)

        critical_items = [
            r for r in reports.values() if r.priority == 'critical'
        ]
        high_items = [
            r for r in reports.values() if r.priority == 'high'
        ]

        summary = {
            'team_name': self.name,
            'agents_count': len(self.agents),
            'agents': [
                {'name': a.name, 'role': a.role.value}
                for a in self.agents.values()
            ],
            'critical_reports': [r.to_dict() for r in critical_items],
            'high_priority_reports': [r.to_dict() for r in high_items],
            'total_findings': len(all_findings),
            'total_recommendations': len(all_recommendations),
            'total_risks': len(all_risks),
            'total_opportunities': len(all_opportunities),
            'findings': all_findings,
            'recommendations': all_recommendations,
            'risks': all_risks,
            'opportunities': all_opportunities,
            'action_items': all_action_items,
        }

        if collaboration:
            summary['collaboration_insights'] = {
                role.value: insights
                for role, insights in collaboration.items()
            }

        return summary
