"""
Agent role implementations for the BatteryML multi-role analysis team.

Each agent represents a distinct professional perspective for analyzing
the BatteryML project comprehensively.
"""

from batteryml.agents.roles.material_scientist import MaterialScientistAgent
from batteryml.agents.roles.data_scientist import DataScientistAgent
from batteryml.agents.roles.data_analyst_frontend import DataAnalystFrontendEngineerAgent
from batteryml.agents.roles.marketing_engineer import MarketingEngineerAgent
from batteryml.agents.roles.battery_application_engineer import BatteryApplicationEngineerAgent
from batteryml.agents.roles.battery_company_ceo import BatteryCompanyCEOAgent
from batteryml.agents.roles.investor import InvestorAgent
from batteryml.agents.roles.market_researcher import MarketResearcherAgent
from batteryml.agents.roles.end_user import EndUserAgent
from batteryml.agents.roles.product_manager import ProductManagerAgent
from batteryml.agents.roles.software_test_engineer import SoftwareTestEngineerAgent
from batteryml.agents.roles.hardware_test_engineer import HardwareTestEngineerAgent
from batteryml.agents.roles.material_test_engineer import MaterialTestEngineerAgent
from batteryml.agents.roles.sales_department import SalesDepartmentAgent
from batteryml.agents.roles.market_survey import MarketSurveyAgent

__all__ = [
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
