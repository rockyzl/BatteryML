"""
BatteryML Agent Team - 电池ML智能体团队

Orchestrates the complete multi-role agent team for comprehensive
project analysis, planning, and strategic recommendations.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from batteryml.agents.base import AgentRole, AgentTeam, AnalysisReport
from batteryml.agents.roles import (
    BatteryApplicationEngineerAgent,
    BatteryCompanyCEOAgent,
    DataAnalystFrontendEngineerAgent,
    DataScientistAgent,
    EndUserAgent,
    HardwareTestEngineerAgent,
    InvestorAgent,
    MarketingEngineerAgent,
    MarketResearcherAgent,
    MarketSurveyAgent,
    MaterialScientistAgent,
    MaterialTestEngineerAgent,
    ProductManagerAgent,
    SalesDepartmentAgent,
    SoftwareTestEngineerAgent,
)

logger = logging.getLogger(__name__)


# Execution order: technical analysis first, then business, then testing, then strategy
DEFAULT_EXECUTION_ORDER = [
    # Phase 1: Technical Foundation (技术基础分析)
    AgentRole.MATERIAL_SCIENTIST,
    AgentRole.DATA_SCIENTIST,
    AgentRole.DATA_ANALYST_FRONTEND,
    AgentRole.BATTERY_APPLICATION_ENGINEER,

    # Phase 2: Testing & Quality (测试与质量)
    AgentRole.SOFTWARE_TEST_ENGINEER,
    AgentRole.HARDWARE_TEST_ENGINEER,
    AgentRole.MATERIAL_TEST_ENGINEER,

    # Phase 3: User & Market (用户与市场)
    AgentRole.END_USER,
    AgentRole.MARKET_RESEARCHER,
    AgentRole.MARKET_SURVEY,

    # Phase 4: Business & Strategy (商业与战略)
    AgentRole.PRODUCT_MANAGER,
    AgentRole.MARKETING_ENGINEER,
    AgentRole.SALES_DEPARTMENT,
    AgentRole.BATTERY_COMPANY_CEO,
    AgentRole.INVESTOR,
]


class BatteryMLAgentTeam:
    """Complete multi-role agent team for BatteryML project analysis.

    Manages 15 specialized agents across 4 analysis phases:
    1. Technical Foundation - Material science, ML, frontend, application engineering
    2. Testing & Quality - Software, hardware, and material testing
    3. User & Market - End user experience, market research, surveys
    4. Business & Strategy - Product management, marketing, sales, CEO, investor
    """

    def __init__(self):
        self.team = AgentTeam(name="BatteryML 多角色智能体分析团队")
        self._initialize_agents()
        self.team.set_execution_order(DEFAULT_EXECUTION_ORDER)
        self._analysis_results: Optional[Dict[AgentRole, AnalysisReport]] = None
        self._collaboration_results: Optional[Dict[AgentRole, List[str]]] = None

    def _initialize_agents(self):
        """Initialize all 15 agents and add them to the team."""
        agents = [
            MaterialScientistAgent(),
            DataScientistAgent(),
            DataAnalystFrontendEngineerAgent(),
            MarketingEngineerAgent(),
            BatteryApplicationEngineerAgent(),
            BatteryCompanyCEOAgent(),
            InvestorAgent(),
            MarketResearcherAgent(),
            EndUserAgent(),
            ProductManagerAgent(),
            SoftwareTestEngineerAgent(),
            HardwareTestEngineerAgent(),
            MaterialTestEngineerAgent(),
            SalesDepartmentAgent(),
            MarketSurveyAgent(),
        ]
        for agent in agents:
            self.team.add_agent(agent)

    def get_project_context(self) -> Dict[str, Any]:
        """Build the project context for analysis."""
        return {
            'project_name': 'BatteryML',
            'version': '0.0.1 (Alpha)',
            'organization': 'Microsoft Corporation',
            'license': 'MIT',
            'publication': 'ICLR 2024 (arXiv:2310.14714)',
            'description': (
                'An open-source platform for machine learning on '
                'battery degradation prediction'
            ),
            'core_capabilities': {
                'datasets': [
                    'CALCE', 'MATR', 'HUST', 'HNEI',
                    'RWTH', 'SNL', 'UL_PUR', 'OX',
                ],
                'models': {
                    'statistical': [
                        'LinearRegression', 'Ridge', 'ElasticNet',
                    ],
                    'tree_based': ['RandomForest', 'XGBoost'],
                    'dimensionality_reduction': ['PCR', 'PLSR'],
                    'kernel': ['GaussianProcess', 'SVM'],
                    'deep_learning': [
                        'MLP', 'LSTM', 'CNN', 'Transformer',
                    ],
                    'baseline': ['Dummy'],
                },
                'feature_extractors': [
                    'VarianceModel', 'DischargeModel',
                    'FullModel', 'VoltageCapacityMatrix',
                ],
                'prediction_tasks': ['RUL', 'SOH'],
                'equipment_support': ['ARBIN', 'NEWARE'],
            },
            'architecture': {
                'pattern': 'Registry + Pipeline + Configuration-driven',
                'language': 'Python',
                'ml_framework': 'PyTorch + scikit-learn',
                'cli_framework': 'fire',
                'visualization': 'matplotlib',
            },
            'gaps': {
                'no_test_suite': True,
                'no_ci_cd': True,
                'no_web_ui': True,
                'no_api_service': True,
                'no_enterprise_features': True,
                'limited_documentation': True,
            },
        }

    def run_full_analysis(self) -> Dict[str, Any]:
        """Execute complete multi-role analysis.

        Returns:
            Comprehensive analysis result with all reports and synthesis.
        """
        context = self.get_project_context()

        # Phase 1: Individual Analysis
        logger.info("=" * 60)
        logger.info("Phase 1: Running Individual Agent Analysis")
        logger.info("=" * 60)
        self._analysis_results = self.team.run_analysis(context)

        # Phase 2: Cross-functional Collaboration
        logger.info("=" * 60)
        logger.info("Phase 2: Running Cross-functional Collaboration")
        logger.info("=" * 60)
        self._collaboration_results = self.team.run_collaboration(
            self._analysis_results
        )

        # Phase 3: Generate Consolidated Summary
        logger.info("=" * 60)
        logger.info("Phase 3: Generating Consolidated Summary")
        logger.info("=" * 60)
        summary = self.team.generate_summary(
            self._analysis_results, self._collaboration_results
        )

        # Phase 4: Synthesize Strategic Plan
        strategic_plan = self._synthesize_strategic_plan()
        summary['strategic_plan'] = strategic_plan

        return summary

    def _synthesize_strategic_plan(self) -> Dict[str, Any]:
        """Synthesize a strategic plan from all agents' analysis."""
        return {
            'vision': (
                '将BatteryML打造为全球领先的电池全生命周期智能管理平台，'
                '覆盖从材料研发到退役回收的完整价值链'
            ),
            'phases': [
                {
                    'name': 'Phase 1: 基础夯实 (0-3个月)',
                    'theme': '提升软件质量和用户体验',
                    'key_deliverables': [
                        '搭建pytest测试框架，覆盖率达到30%',
                        '配置GitHub Actions CI/CD管线',
                        '创建Google Colab一键体验Demo',
                        '开发通用CSV/Excel数据导入工具',
                        '改善错误提示和诊断信息',
                        '发布v0.5版本',
                    ],
                    'responsible_agents': [
                        '软件测试工程师', '数据科学家',
                        '终端用户', '前端工程师',
                    ],
                    'success_metrics': [
                        '测试覆盖率≥30%',
                        'CI管线运行成功率≥95%',
                        'Colab Demo完成率≥80%',
                        'GitHub Star增长50%',
                    ],
                },
                {
                    'name': 'Phase 2: 功能完善 (3-6个月)',
                    'theme': '完善核心ML功能和可视化',
                    'key_deliverables': [
                        '引入Optuna超参数自动调优',
                        '实现多维度评估指标(MAE/MAPE/R²)',
                        '集成SHAP可解释性分析',
                        '开发Streamlit Web可视化仪表板',
                        '增加K-Fold交叉验证框架',
                        '搭建MkDocs官方文档站',
                        '创建在线Benchmark Leaderboard',
                        '发布v1.0版本',
                    ],
                    'responsible_agents': [
                        '数据科学家', '前端工程师',
                        '市场推广工程师', '产品经理',
                    ],
                    'success_metrics': [
                        '测试覆盖率≥60%',
                        'Web仪表板上线',
                        '文档站完成',
                        '活跃贡献者≥10人',
                    ],
                },
                {
                    'name': 'Phase 3: 产品化 (6-12个月)',
                    'theme': '构建企业级能力，启动商业化',
                    'key_deliverables': [
                        '开发RESTful在线推理API服务',
                        '实现Pack级分析框架',
                        '增加日历老化数据支持',
                        '实现ONNX轻量化模型导出',
                        '开发安全预警模型原型',
                        '增加Maccor设备数据支持',
                        '制定Open Core定价方案',
                        '签约3个标杆客户',
                        '发布v2.0版本',
                    ],
                    'responsible_agents': [
                        '应用工程师', '材料科学家',
                        '硬件测试工程师', 'CEO', '销售部门',
                    ],
                    'success_metrics': [
                        '测试覆盖率≥80%',
                        'API服务上线',
                        '3个付费客户',
                        'ARR达到$50万',
                    ],
                },
                {
                    'name': 'Phase 4: 规模增长 (12-24个月)',
                    'theme': '市场扩展和生态建设',
                    'key_deliverables': [
                        '固态电池/钠离子电池材料支持',
                        '电池数字孪生平台原型',
                        '联邦学习框架集成',
                        '电池护照(Battery Passport)合规模块',
                        '国际市场扩展(欧洲、北美)',
                        'A轮融资完成',
                    ],
                    'responsible_agents': [
                        '材料科学家', '投资方',
                        '市场研究员', 'CEO',
                    ],
                    'success_metrics': [
                        'ARR达到$200万',
                        '20+付费客户',
                        '全球5000+ GitHub Star',
                        'A轮融资完成',
                    ],
                },
            ],
            'critical_success_factors': [
                '1. 测试和CI/CD是一切的基础——没有质量保证的产品不可能商业化',
                '2. 用户体验决定采用率——降低学习曲线比增加新功能更重要',
                '3. 标杆客户证明价值——3个成功案例胜过100个功能列表',
                '4. 开源社区是增长引擎——社区活跃度直接影响商业化成功率',
                '5. 材料科学深度是护城河——跨学科能力是最难复制的竞争优势',
            ],
            'budget_estimate': {
                'Phase 1': '50-80万元(主要为现有团队时间投入)',
                'Phase 2': '100-150万元(需要增加1-2名工程师)',
                'Phase 3': '200-300万元(需要产品化团队+销售团队)',
                'Phase 4': '500-1000万元(国际扩展+大规模研发)',
            },
            'team_composition': {
                'Phase 1': '3-4人(ML工程师×2 + 前端×1 + 测试×1)',
                'Phase 2': '5-7人(+产品经理×1 + 文档工程师×1)',
                'Phase 3': '8-12人(+应用工程师×2 + 销售×2 + DevOps×1)',
                'Phase 4': '15-20人(+国际市场×3 + 研究员×2)',
            },
        }

    def get_action_items_by_priority(self) -> Dict[str, List[Dict]]:
        """Get all action items organized by priority level."""
        if not self._analysis_results:
            return {}

        items_by_priority: Dict[str, List[Dict]] = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': [],
        }

        for role, report in self._analysis_results.items():
            for item in report.action_items:
                priority = item.get('priority', 'medium')
                enriched_item = {
                    **item,
                    'source_agent': report.agent_name,
                }
                if priority in items_by_priority:
                    items_by_priority[priority].append(enriched_item)

        return items_by_priority

    def get_risk_matrix(self) -> List[Dict[str, str]]:
        """Get consolidated risk matrix from all agents."""
        if not self._analysis_results:
            return []

        risks = []
        for role, report in self._analysis_results.items():
            for risk in report.risks:
                risks.append({
                    'source': report.agent_name,
                    'risk': risk,
                    'report_priority': report.priority,
                })
        return risks

    def print_executive_summary(self):
        """Print a human-readable executive summary."""
        if not self._analysis_results:
            print("No analysis results available. Run run_full_analysis() first.")
            return

        print("=" * 80)
        print("BatteryML 多角色智能体团队分析报告 — 执行摘要")
        print("=" * 80)

        # Agent summaries
        print("\n" + "─" * 80)
        print("各角色分析摘要")
        print("─" * 80)
        for role, report in self._analysis_results.items():
            priority_marker = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢',
            }.get(report.priority, '⚪')
            print(f"\n{priority_marker} [{report.priority.upper()}] {report.agent_name}")
            print(f"   {report.summary}")

        # Critical action items
        items = self.get_action_items_by_priority()
        if items.get('critical'):
            print("\n" + "─" * 80)
            print("关键行动项 (CRITICAL)")
            print("─" * 80)
            for i, item in enumerate(items['critical'], 1):
                print(f"\n  {i}. {item['task']}")
                print(f"     负责人: {item['assignee']}")
                print(f"     预计工期: {item['estimated_effort']}")
                print(f"     来源: {item['source_agent']}")

        if items.get('high'):
            print("\n" + "─" * 80)
            print("高优先级行动项 (HIGH)")
            print("─" * 80)
            for i, item in enumerate(items['high'], 1):
                print(f"\n  {i}. {item['task']}")
                print(f"     负责人: {item['assignee']}")
                print(f"     预计工期: {item['estimated_effort']}")

        # Cross-functional insights
        if self._collaboration_results:
            print("\n" + "─" * 80)
            print("跨职能协作洞察")
            print("─" * 80)
            for role, insights in self._collaboration_results.items():
                for insight in insights:
                    print(f"  • {insight}")

        # Strategic plan summary
        plan = self._synthesize_strategic_plan()
        print("\n" + "─" * 80)
        print("战略路线图")
        print("─" * 80)
        print(f"\n愿景: {plan['vision']}")
        for phase in plan['phases']:
            print(f"\n  📋 {phase['name']}")
            print(f"     主题: {phase['theme']}")
            for d in phase['key_deliverables'][:3]:
                print(f"     • {d}")
            if len(phase['key_deliverables']) > 3:
                print(f"     ... 及其他{len(phase['key_deliverables'])-3}项")

        print("\n" + "=" * 80)
        print("报告生成完毕 — BatteryML 多角色智能体团队")
        print("=" * 80)

    def export_report(self, filepath: str):
        """Export full analysis to JSON file."""
        if not self._analysis_results:
            raise RuntimeError("No analysis results. Run run_full_analysis() first.")

        result = self.run_full_analysis()

        # Convert AgentRole keys to strings for JSON serialization
        serializable = {
            **result,
            'individual_reports': {
                role.value: report.to_dict()
                for role, report in self._analysis_results.items()
            },
        }

        if self._collaboration_results:
            serializable['collaboration'] = {
                role.value: insights
                for role, insights in self._collaboration_results.items()
            }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(serializable, f, indent=2, ensure_ascii=False)

        logger.info(f"Report exported to {filepath}")
