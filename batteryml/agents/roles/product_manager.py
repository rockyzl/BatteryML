"""
Product Manager Agent - 产品经理智能体

Analyzes the BatteryML project from the perspective of product strategy,
roadmap planning, user needs prioritization, and feature development.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class ProductManagerAgent(BaseAgent):
    """Agent representing a product manager.

    Focus areas:
    - Product vision and roadmap
    - Feature prioritization (MoSCoW / RICE)
    - User story mapping
    - Go-to-market strategy
    - Metrics and KPIs
    - Cross-functional coordination
    """

    def __init__(self):
        super().__init__(
            name="PM Li - 产品经理",
            role=AgentRole.PRODUCT_MANAGER,
            description=(
                "Experienced product manager in developer tools and "
                "scientific software. Bridges the gap between technical "
                "capabilities and user needs, defines product roadmap, "
                "and prioritizes feature development."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "product_vision_clarity",
            "roadmap_definition",
            "feature_prioritization",
            "user_persona_coverage",
            "competitive_differentiation",
            "metrics_and_kpis",
            "release_management",
            "stakeholder_alignment",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "产品愿景清晰但窄——'电池降解预测的开源ML工具'是一个好的起点，"
            "但需要拓展为'电池全生命周期智能管理平台'以覆盖更大的市场",

            "缺少正式的产品路线图(Roadmap)——功能开发没有明确的优先级排序"
            "和时间节点规划",

            "版本号(0.0.1 Alpha)说明产品还处于非常早期的阶段——"
            "需要定义清晰的版本里程碑(0.1→0.5→1.0)和发布节奏",

            "用户画像定义不清——项目同时服务学术研究人员和工业工程师，"
            "但两者的需求差异很大，需要明确主次",

            "功能模块化程度高(Registry模式)——为按需组装不同版本"
            "(社区版/专业版/企业版)提供了良好的架构基础",

            "缺少用户反馈收集机制——没有in-app反馈、NPS调查、"
            "或用户行为分析(telemetry)来指导产品决策",

            "关键功能缺失清单(按用户频繁反馈排序)："
            "1) 自定义数据导入 2) 交互式可视化 3) 模型对比 "
            "4) 超参数调优 5) 结果导出",
        ]

        recommendations = [
            "【P0 - 本季度】定义清晰的产品路线图，划分三个版本阶段：\n"
            "  v0.5(3个月): 改善用户体验(错误提示、Colab Demo、CSV导入)\n"
            "  v1.0(6个月): 核心功能完善(HPO、多指标、可解释性、Web UI)\n"
            "  v2.0(12个月): 企业级功能(API服务、安全合规、Pack级分析)",

            "【P0 - 本季度】定义四个核心用户画像并排列优先级：\n"
            "  1) 学术研究人员(当前核心用户)\n"
            "  2) 电池公司ML工程师(最大增长潜力)\n"
            "  3) BMS开发工程师(最高付费意愿)\n"
            "  4) 管理层/投资人(决策支持需求)",

            "【P1 - 下季度】实施RICE评分法对所有功能需求排序——"
            "Reach(覆盖用户数) × Impact(影响程度) × Confidence(确定性) / Effort(工程量)",

            "【P1 - 下季度】建立用户反馈闭环——通过GitHub Discussions + "
            "季度用户调查 + 使用数据分析(opt-in telemetry)三位一体的反馈机制",

            "【P2 - 明年】制定Open Core版本策略：\n"
            "  Community Edition: 核心ML功能(永久免费开源)\n"
            "  Professional Edition: HPO + 可视化 + 报告($99/月)\n"
            "  Enterprise Edition: API + 安全 + SLA + 咨询(定制报价)",
        ]

        risks = [
            "功能范围蔓延(Feature Creep)——试图满足所有用户群的需求"
            "可能导致产品失焦和开发效率低下",

            "过度工程化——在用户群还不大的阶段就构建复杂的企业级功能，"
            "可能浪费宝贵的开发资源",

            "开源社区期望与商业化需求的潜在冲突——免费用户可能抵制"
            "将功能移至付费版本",
        ]

        opportunities = [
            "作为首个ICLR发表的电池ML开源工具，有机会成为事实上的行业标准",
            "模块化架构天然支持分层定价——可以精确控制每个版本的功能边界",
            "学术界用户可以成为最好的Product Ambassador——他们的论文引用"
            "就是最好的产品推广",
        ]

        action_items = [
            {
                'task': '制定2025-2026产品路线图',
                'assignee': 'product_manager',
                'priority': 'critical',
                'estimated_effort': '1-2周',
                'description': '明确v0.5/v1.0/v2.0的功能范围、时间节点和成功指标',
            },
            {
                'task': '用户画像和需求矩阵文档',
                'assignee': 'product_manager + market_researcher',
                'priority': 'high',
                'estimated_effort': '1周',
                'description': '定义4个核心画像，每个画像的Top 5需求和痛点',
            },
            {
                'task': 'RICE功能优先级评分表',
                'assignee': 'product_manager',
                'priority': 'high',
                'estimated_effort': '3天',
                'description': '对所有已知功能需求进行RICE评分并排序',
            },
            {
                'task': '定义v0.5版本发布计划',
                'assignee': 'product_manager + data_scientist',
                'priority': 'critical',
                'estimated_effort': '1周',
                'description': '确定v0.5包含的功能列表、验收标准和发布时间',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML缺少正式的产品路线图和版本规划，需要立即制定v0.5/v1.0/v2.0"
                "的阶段性目标。建议明确四个核心用户画像的优先级(学术研究员→ML工程师→"
                "BMS工程师→管理层)，使用RICE评分法排列功能需求。短期(3个月)聚焦于"
                "改善用户体验(CSV导入、错误提示、Colab Demo)；中期(6个月)完善核心功能"
                "(HPO、可解释性、Web UI)；长期(12个月)构建企业级能力(API、安全、Pack级)。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="critical",
            metadata={
                'version_roadmap': {
                    'v0.5': '3个月 - 用户体验改善',
                    'v1.0': '6个月 - 核心功能完善',
                    'v2.0': '12个月 - 企业级功能',
                },
                'user_personas': [
                    'Academic Researcher',
                    'ML Engineer',
                    'BMS Developer',
                    'Management/Investor',
                ],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'end_user':
                insights.append(
                    "【产品经理→终端用户】完全同意优先解决CSV导入和Colab Demo——"
                    "这是降低上手门槛的最快路径，纳入v0.5版本"
                )
            if report.agent_role == 'battery_company_ceo':
                insights.append(
                    "【产品经理→CEO】产品路线图将严格以客户价值优先——"
                    "企业版功能开发将与标杆客户的需求验证同步推进"
                )
            if report.agent_role == 'data_scientist':
                insights.append(
                    "【产品经理→数据科学家】HPO和多指标评估纳入v1.0计划，"
                    "SHAP可解释性也列为v1.0高优先级功能"
                )
        return insights
