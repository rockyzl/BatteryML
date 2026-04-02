"""
BatteryML Multi-Role Agent Team

A comprehensive agent team for analyzing the BatteryML project from
multiple professional perspectives: material science, data science,
engineering, business, testing, and market analysis.
"""

from batteryml.agents.base import BaseAgent, AgentTeam
from batteryml.agents.roles import (
    MaterialScientistAgent,
    DataScientistAgent,
    DataAnalystFrontendEngineerAgent,
    MarketingEngineerAgent,
    BatteryApplicationEngineerAgent,
    BatteryCompanyCEOAgent,
    InvestorAgent,
    MarketResearcherAgent,
    EndUserAgent,
    ProductManagerAgent,
    SoftwareTestEngineerAgent,
    HardwareTestEngineerAgent,
    MaterialTestEngineerAgent,
    SalesDepartmentAgent,
    MarketSurveyAgent,
)
from batteryml.agents.team import BatteryMLAgentTeam

__all__ = [
    'BaseAgent',
    'AgentTeam',
    'BatteryMLAgentTeam',
    'MaterialScientistAgent',
    'DataScientistAgent',
    'DataAnalystFrontendEngineerAgent',
    'MarketingEngineerAgent',
    'BatteryApplicationEngineerAgent',
    'BatteryCompanyCEOAgent',
    'InvestorAgent',
    'MarketResearcherAgent',
    'EndUserAgent',
    'ProductManagerAgent',
    'SoftwareTestEngineerAgent',
    'HardwareTestEngineerAgent',
    'MaterialTestEngineerAgent',
    'SalesDepartmentAgent',
    'MarketSurveyAgent',
]
