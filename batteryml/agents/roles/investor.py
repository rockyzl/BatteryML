"""
Investor Agent - 电池公司投资方智能体

Analyzes the BatteryML project from the perspective of venture capital,
ROI potential, market timing, and investment risk assessment.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class InvestorAgent(BaseAgent):
    """Agent representing a battery company investor / VC partner.

    Focus areas:
    - Market size and growth trajectory (TAM/SAM/SOM)
    - Technology defensibility and moat
    - Team and execution capability
    - Financial projections and unit economics
    - Exit scenarios (IPO, M&A)
    - Risk-adjusted return potential
    """

    def __init__(self):
        super().__init__(
            name="Victor Capital - 电池公司投资方",
            role=AgentRole.INVESTOR,
            description=(
                "Climate Tech / Deep Tech venture capital partner with "
                "extensive experience in battery and clean energy investments. "
                "Evaluates the project's investment attractiveness, market "
                "potential, and risk-return profile."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "market_size_tam_sam_som",
            "technology_defensibility",
            "team_capability",
            "financial_projections",
            "competitive_landscape",
            "exit_scenarios",
            "risk_return_profile",
            "esg_alignment",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "【市场规模】全球电池管理系统(BMS)软件市场预计2030年达到150亿美元，"
            "其中AI驱动的预测性维护占比约20-30%，可服务市场(SAM)约30-45亿美元",

            "【技术壁垒】BatteryML具备以下技术护城河：(1)统一的多数据集适配框架 "
            "(2)经学术验证的基准测试体系 (3)Microsoft组织背书 "
            "(4)跨材料体系的模型库",

            "【竞争格局】直接竞品较少——PyBaMM偏重电化学仿真而非ML预测，"
            "BEEP专注数据格式转换，battery-data-toolkit功能有限。"
            "BatteryML在ML预测领域处于领先地位",

            "【团队维度】作为Microsoft内部项目，依托大公司研发资源，"
            "但如果独立商业化需要评估核心团队的创业意愿和能力",

            "【产品成熟度】当前处于研究工具阶段(TRL 3-4)，要达到"
            "可商业化的产品级(TRL 7-9)还需要12-18个月的产品化投入",

            "【收入模型】目前无营收，建议的Open Core模式在DevTools领域"
            "已有多个成功案例(GitLab、Elastic、MongoDB等)",

            "【ESG合规】项目直接服务于电池寿命延长和循环经济——"
            "完美契合ESG投资主题，有利于吸引影响力投资基金",

            "【监管红利】欧盟电池法规(2027年生效)要求电池全生命周期追踪，"
            "这是一个确定性极高的政策驱动增长因子",
        ]

        recommendations = [
            "【投资建议】建议关注并考虑Pre-Seed/Seed阶段投资——"
            "当前项目估值较低但潜力巨大，是进入的最佳时机",

            "【投资条款】建议投资500-1000万美元(Seed轮)，用于："
            "(1)组建5-8人产品化团队 (2)开发企业版MVP "
            "(3)签约2-3个标杆客户 (4)12个月运营资金",

            "【里程碑设定】关键里程碑应包括："
            "M1(3个月): 企业版MVP上线 "
            "M2(6个月): 签约第一个付费客户 "
            "M3(12个月): ARR达到50万美元 "
            "M4(18个月): ARR达到200万美元",

            "【退出路径】两条主要退出通道："
            "(1)战略收购——Siemens/ABB/Honeywell等工业软件巨头 "
            "(2)IPO——Climate Tech SPV/独立上市(5-7年时间线)",

            "【风控要求】投资条件应包括："
            "(1)IP从Microsoft独立转移 (2)核心技术团队锁定期 "
            "(3)董事会席位 (4)信息权和反稀释保护",

            "【后续轮次】A轮预计在18个月后，融资2000-5000万美元，"
            "用于国际市场扩展和销售团队建设",
        ]

        risks = [
            "【高风险】Microsoft可能决定内部商业化或关停项目，"
            "外部投资者的权益需要在投资协议中严格保护",

            "【中风险】电池AI市场可能出现价格竞争——如果大量开源替代品涌现，"
            "企业版的溢价空间可能被压缩",

            "【中风险】客户获取成本(CAC)可能较高——电池行业决策周期长、"
            "安全要求严格，企业销售效率可能低于预期",

            "【低风险】技术路线变革风险——固态电池、钠离子电池等新技术"
            "可能需要全新的预测模型，但团队具备快速适应能力",
        ]

        opportunities = [
            "Climate Tech投资正在加速——2024年全球Climate Tech VC投资"
            "超过500亿美元，电池技术是最热门的赛道之一",

            "收并购标的吸引力高——工业软件巨头正在积极通过收购进入"
            "电池智能化领域",

            "政策确定性强——欧盟电池护照法规提供了明确的需求时间线，"
            "降低了市场不确定性",

            "网络效应潜力——随着更多用户贡献模型和数据，平台价值指数级增长",
        ]

        action_items = [
            {
                'task': '完成详细尽职调查(Due Diligence)',
                'assignee': 'investor',
                'priority': 'high',
                'estimated_effort': '4-6周',
                'description': '技术DD、市场DD、法律DD全面评估',
            },
            {
                'task': '制定Term Sheet',
                'assignee': 'investor + ceo',
                'priority': 'high',
                'estimated_effort': '2周',
                'description': '包含估值、投资金额、董事会席位、'
                               'IP转移条款等核心条款',
            },
            {
                'task': '组织Industry Advisory Board',
                'assignee': 'investor',
                'priority': 'medium',
                'estimated_effort': '1个月',
                'description': '邀请电池行业资深人士组成顾问委员会，'
                               '帮助公司建立行业网络',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML作为Climate Tech / Battery AI赛道的潜在投资标的，"
                "具备良好的基础：Microsoft背书、ICLR学术验证、清晰的市场定位、"
                "较弱的竞争对手。建议在Seed阶段投资500-1000万美元，"
                "重点支持产品化团队建设和标杆客户获取。关键风险在于IP从Microsoft"
                "独立转移的可行性和核心团队的稳定性。预期退出路径包括战略收购"
                "(3-5年)和IPO(5-7年)，目标回报倍数10-30x。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'proposed_investment': '500-1000万美元(Seed轮)',
                'target_return': '10-30x',
                'exit_timeline': '3-7年',
                'tam': '150亿美元(BMS软件市场2030)',
                'sam': '30-45亿美元(AI预测性维护)',
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'battery_company_ceo':
                insights.append(
                    "【投资方→CEO】商业化路径必须在6个月内验证——"
                    "建议先跑一个小型PoC项目证明客户付费意愿，再大规模投入产品化"
                )
            if report.agent_role == 'market_researcher':
                insights.append(
                    "【投资方→市场研究员】需要更深入的竞争情报——"
                    "包括潜在竞品的融资情况、客户名单和技术路线分析"
                )
        return insights
