"""
Sales Department Agent - 销售部门智能体

Analyzes the BatteryML project from the perspective of sales strategy,
customer acquisition, pricing, and revenue generation.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class SalesDepartmentAgent(BaseAgent):
    """Agent representing the sales department.

    Focus areas:
    - Customer acquisition strategy
    - Sales funnel and pipeline
    - Pricing strategy
    - Partnership and channel sales
    - Customer success and retention
    - Revenue targets and forecasting
    """

    def __init__(self):
        super().__init__(
            name="Sales Director Zhao - 销售部门",
            role=AgentRole.SALES_DEPARTMENT,
            description=(
                "Sales leader experienced in B2B enterprise software sales "
                "in the energy/automotive industry. Designs sales strategies, "
                "pricing models, and customer acquisition plans."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "customer_acquisition_strategy",
            "pricing_model",
            "sales_cycle_analysis",
            "channel_strategy",
            "customer_success",
            "revenue_forecasting",
            "competitive_win_rate",
            "upsell_cross_sell",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "当前产品处于开源免费状态——没有销售团队、定价策略或收入来源",

            "目标客户画像：\n"
            "  Tier 1: 头部电池厂商(CATL、BYD、LG、Samsung SDI、Panasonic) — 年预算千万+\n"
            "  Tier 2: EV OEM(特斯拉、蔚来、比亚迪、宝马) — 年预算百万+\n"
            "  Tier 3: 储能运营商(阳光电源、华为数字能源) — 年预算百万+\n"
            "  Tier 4: 科研院所(清华、MIT、斯坦福) — 年预算十万+",

            "电池行业的B2B销售周期长(6-18个月)——需要技术验证(PoC)、"
            "安全合规审查、采购流程等多个环节",

            "竞品定价参考：Voltaiq年费约10-50万美元(取决于规模)，"
            "TWAICE按GWh监控容量收费，Accure按模组数量收费",

            "开源到付费的转化是核心挑战——需要提供足够差异化的企业级功能"
            "来说服用户从免费版升级",

            "中国市场的销售需要本地团队——语言、关系、本地化部署等"
            "都需要本地化运营能力",
        ]

        recommendations = [
            "【高优先级】设计三层定价体系：\n"
            "  Community: 免费(开源，基础ML功能)\n"
            "  Professional: $499-999/月(HPO + 可视化 + API + 基础支持)\n"
            "  Enterprise: 定制报价(安全合规 + SLA + 专家咨询 + 本地部署)",

            "【高优先级】制定'Land and Expand'销售策略——通过免费版获取用户，"
            "技术团队试用后向上推荐给管理层，逐步扩大使用范围和付费规模",

            "【高优先级】开发3个标杆客户——以极低价格(甚至免费)签约前3个客户，"
            "用Case Study和口碑驱动后续销售",

            "【中优先级】建立渠道合作体系——与系统集成商(SI)、咨询公司合作，"
            "通过合作伙伴覆盖中小型客户",

            "【中优先级】开发ROI计算器——帮助客户量化使用BatteryML带来的："
            "1) 减少电池测试时间 2) 降低保修成本 3) 延长电池使用寿命 "
            "的经济价值",

            "【低优先级】组建3-5人的销售团队——包括1名销售总监、2名大客户经理(AE)、"
            "1-2名售前技术支持(SE)",
        ]

        risks = [
            "开源用户可能认为所有功能都应该免费——付费转化率可能远低于预期",
            "B2B长销售周期意味着前12个月几乎没有收入——需要充足的资金储备",
            "头部电池厂商可能选择自建AI团队而非采购第三方工具",
            "中国市场的竞争对手(如宁德时代内部AI团队)具有天然的数据优势",
        ]

        opportunities = [
            "开源社区的活跃用户是最好的销售线索来源——GitHub Star用户邮件列表",
            "技术会议和论文发表带来的'入站销售'(Inbound)成本极低",
            "电池护照法规合规需求创造了刚性购买理由——不是'nice to have'而是'must have'",
            "按使用量(GWh/通道数/API调用次数)收费的模式可以与客户业务规模同步增长",
        ]

        action_items = [
            {
                'task': '制定详细定价方案',
                'assignee': 'sales_department + product_manager',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '完成三层定价的功能边界定义、价格确定和竞争力分析',
            },
            {
                'task': '开发ROI计算工具',
                'assignee': 'sales_department + marketing_engineer',
                'priority': 'high',
                'estimated_effort': '2周',
                'description': '帮助客户量化BatteryML带来的成本节约和效率提升',
            },
            {
                'task': '签约前3个标杆客户',
                'assignee': 'sales_department + ceo',
                'priority': 'critical',
                'estimated_effort': '3-6个月',
                'description': '在EV/储能/消费电子各签约1个标杆客户',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML的商业化销售需要从零开始构建——建议采用'Land and Expand'"
                "策略，通过开源社区获取用户，逐步转化为付费客户。定价建议采用三层模式"
                "(免费/Professional/Enterprise)，对标Voltaiq但定价低30-50%以快速获客。"
                "首年目标是签约3个标杆客户并产生首批收入。最大挑战是B2B长销售周期"
                "(6-18个月)和开源到付费的转化率。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'pricing_tiers': {
                    'Community': '免费',
                    'Professional': '$499-999/月',
                    'Enterprise': '定制报价',
                },
                'target_customers': [
                    'Battery OEMs', 'EV OEMs',
                    'ESS Operators', 'Research Institutes',
                ],
                'sales_cycle': '6-18个月',
                'year1_revenue_target': '$50万',
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'marketing_engineer':
                insights.append(
                    "【销售→市场推广】ROI计算器和Case Study是销售最需要的武器——"
                    "请优先制作，每个客户沟通都会用到"
                )
            if report.agent_role == 'battery_company_ceo':
                insights.append(
                    "【销售→CEO】建议前3个客户给予70-90%折扣——"
                    "标杆案例的战略价值远高于短期收入"
                )
        return insights
