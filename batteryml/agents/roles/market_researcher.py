"""
Market Researcher Agent - 市场研究员智能体

Analyzes the BatteryML project from the perspective of market trends,
competitive landscape, and industry dynamics.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class MarketResearcherAgent(BaseAgent):
    """Agent representing a market researcher.

    Focus areas:
    - Battery industry market trends
    - Competitive landscape analysis
    - Technology adoption curves
    - Regulatory environment
    - Geographic market analysis
    - Industry value chain positioning
    """

    def __init__(self):
        super().__init__(
            name="Rachel Research - 市场研究员",
            role=AgentRole.MARKET_RESEARCHER,
            description=(
                "Senior market research analyst specializing in the battery "
                "and clean energy technology sector. Provides deep analysis "
                "of market trends, competitive dynamics, and growth forecasts."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "market_size_forecasts",
            "competitive_landscape",
            "technology_adoption_curve",
            "regulatory_environment",
            "geographic_analysis",
            "value_chain_positioning",
            "customer_segmentation",
            "pricing_benchmarks",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "【市场趋势】全球锂电池市场2025年规模约1500亿美元，预计2030年达到4000亿美元，"
            "CAGR约21%。电池健康管理(BHM)软件作为配套需求同步增长",

            "【细分市场】电池AI软件的三大应用场景："
            "1) EV电池健康云服务(最大市场) "
            "2) 储能电站预测性维护(增长最快) "
            "3) 消费电子电池优化(利润率最高)",

            "【竞争对手分析】"
            "- PyBaMM: 牛津大学开源项目，偏重电化学仿真，2000+ GitHub Star\n"
            "- BEEP: 丰田研究院，专注电池数据格式，功能单一\n"
            "- Voltaiq: 商业SaaS平台，融资超5000万美元，企业级解决方案\n"
            "- TWAICE: 德国创业公司，电池数字孪生，融资超3000万欧元\n"
            "- Accure: 电池安全监控，融资超2000万欧元",

            "【技术采用曲线】电池AI技术目前处于'早期多数(Early Majority)'采用阶段——"
            "头部车企(特斯拉、宝马)已开始部署，中型企业正在评估方案",

            "【地理市场】中国占全球电池产能的75%以上——中国市场的渗透率将直接决定"
            "BatteryML的全球市场份额。欧洲市场受监管驱动增长迅速",

            "【客户付费意愿】根据行业调研，电池厂商愿意为预测性维护软件支付"
            "每GWh产能1-5万美元/年的订阅费用",

            "【开源vs商业】开源电池AI工具与商业解决方案的市场定位存在互补关系——"
            "开源工具吸引研究者和早期采用者，商业产品服务大型企业",
        ]

        recommendations = [
            "【高优先级】优先进入中国和欧洲市场——中国是产能中心，"
            "欧洲是监管驱动的增长市场",

            "【高优先级】明确与Voltaiq/TWAICE的差异化定位——"
            "BatteryML的优势在于开源透明、算法可审计、学术界认可度高",

            "【中优先级】针对三大细分市场分别制定Go-to-Market策略——"
            "EV市场走大客户战略，储能市场走渠道合作，消费电子走SaaS自助",

            "【中优先级】建立行业白皮书和报告发布机制——通过权威内容建立"
            "思想领导力(Thought Leadership)地位",

            "【低优先级】考虑与中国电池行业协会(CBBA)和欧洲电池联盟(EBA)"
            "建立合作关系，获取行业洞察和潜在客户资源",
        ]

        risks = [
            "Voltaiq、TWAICE等已获得大额融资的竞品可能通过价格战或"
            "捆绑销售挤压BatteryML的市场空间",

            "中国市场的本地化要求(数据合规、中文文档、本地部署)可能"
            "增加显著的运营成本",

            "电池技术代际更替(如固态电池)可能使当前的市场研究结论失效",
        ]

        opportunities = [
            "电池护照法规创造了全新的合规需求市场——仅欧盟市场就价值数十亿欧元",
            "电池回收市场(预计2030年达到350亿美元)需要准确的电池状态评估工具",
            "V2G技术商业化将创造对实时SOH估计的巨大需求",
            "与保险公司合作开发基于电池健康的EV保险产品是蓝海市场",
        ]

        action_items = [
            {
                'task': '完成详细竞争对手分析报告',
                'assignee': 'market_researcher',
                'priority': 'high',
                'estimated_effort': '2周',
                'description': '深入分析Voltaiq/TWAICE/Accure的产品功能、'
                               '定价、客户群和技术路线',
            },
            {
                'task': '客户需求调研(50+访谈)',
                'assignee': 'market_researcher + sales_department',
                'priority': 'high',
                'estimated_effort': '4-6周',
                'description': '对电池厂商、EV OEM、储能运营商进行深度访谈，'
                               '验证产品需求假设',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "电池AI软件市场正处于快速增长期，BatteryML在开源ML预测领域具有先发优势。"
                "主要商业竞品(Voltaiq/TWAICE/Accure)已获大额融资但定位不同。"
                "建议优先进入中国(产能中心)和欧洲(监管驱动)市场，"
                "利用开源透明和学术公信力的差异化优势。欧盟电池护照法规将是"
                "最大的需求催化剂。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'tam': '4000亿美元(全球电池市场2030)',
                'sam': '30-45亿美元(电池AI软件)',
                'key_competitors': [
                    'Voltaiq', 'TWAICE', 'Accure', 'PyBaMM', 'BEEP',
                ],
                'key_markets': ['China', 'Europe', 'North America'],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'battery_company_ceo':
                insights.append(
                    "【市场研究员→CEO】根据竞品分析，建议定价采用'渗透定价'策略——"
                    "初期低于Voltaiq 30-50%快速获客，后续通过增值服务提升客单价"
                )
            if report.agent_role == 'investor':
                insights.append(
                    "【市场研究员→投资方】建议密切关注TWAICE的B轮融资动态——"
                    "其估值将成为BatteryML商业化后的重要估值参考锚点"
                )
        return insights
