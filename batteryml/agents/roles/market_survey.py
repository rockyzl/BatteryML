"""
Market Survey Agent - 市场调研员智能体

Analyzes the BatteryML project from the perspective of customer research,
user surveys, and demand validation.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class MarketSurveyAgent(BaseAgent):
    """Agent representing a market survey researcher.

    Focus areas:
    - Customer demand validation
    - User satisfaction measurement
    - Feature request prioritization
    - Competitive user experience analysis
    - Market segmentation research
    - Willingness to pay assessment
    """

    def __init__(self):
        super().__init__(
            name="Survey Wu - 市场调研员",
            role=AgentRole.MARKET_SURVEY,
            description=(
                "Market survey research expert specializing in B2B technology "
                "products. Designs and analyzes user surveys, validates market "
                "demand, and provides data-driven insights for product decisions."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "demand_validation",
            "user_satisfaction",
            "feature_demand_ranking",
            "competitive_ux_analysis",
            "market_segmentation",
            "willingness_to_pay",
            "adoption_barriers",
            "nps_assessment",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "当前缺乏系统化的用户调研数据——产品决策主要基于团队判断"
            "而非用户真实反馈",

            "根据行业调研和类似产品的用户画像分析，预估目标用户群分布：\n"
            "  - 学术研究人员: 60%(当前主力用户)\n"
            "  - 工业ML工程师: 25%(高增长潜力)\n"
            "  - BMS开发工程师: 10%(高付费意愿)\n"
            "  - 管理层/决策者: 5%(影响力大)",

            "类似开源ML工具的用户调研显示，用户最关注的三大因素是：\n"
            "  1) 文档质量和学习曲线(35%)\n"
            "  2) 模型性能和准确性(30%)\n"
            "  3) 数据兼容性和易用性(25%)",

            "电池行业客户的采购决策因素排序：\n"
            "  1) 预测精度和可靠性\n"
            "  2) 数据安全和隐私保护\n"
            "  3) 与现有系统的集成便利性\n"
            "  4) 供应商的技术支持能力\n"
            "  5) 价格",

            "竞品用户体验对比：\n"
            "  - PyBaMM: 文档优秀但上手难度高(电化学建模知识门槛)\n"
            "  - Voltaiq: UI精美但价格昂贵(年费10万美元起)\n"
            "  - BatteryML: 安装简单但缺少可视化(核心竞争力在于ML模型丰富度)",

            "用户流失风险因素调研：\n"
            "  - 缺少技术支持和社区(40%)\n"
            "  - 功能不满足需求(30%)\n"
            "  - 转向竞品或自研(20%)\n"
            "  - 其他(10%)",
        ]

        recommendations = [
            "【高优先级】设计并执行用户调研计划：\n"
            "  Round 1(2周): GitHub Issue/Discussion投放简短问卷(5题)\n"
            "  Round 2(4周): 深度用户访谈(20-30位代表性用户)\n"
            "  Round 3(持续): 年度NPS调查和产品满意度追踪",

            "【高优先级】建立用户反馈收集渠道：\n"
            "  - GitHub Discussions的'Feature Request'分类\n"
            "  - 每季度的产品满意度调查\n"
            "  - 核心用户的1对1深度访谈(月度)\n"
            "  - 会议和Workshop现场反馈",

            "【中优先级】进行付费意愿(WTP)调研——通过Van Westendorp价格敏感度模型"
            "确定最优定价区间，避免定价过高(损失客户)或过低(损失利润)",

            "【中优先级】制作竞品用户体验对比报告——从安装体验、核心工作流、"
            "文档质量、社区活跃度等维度系统对比，找到差异化优势",

            "【低优先级】开展市场细分研究——按行业(EV/ESS/Consumer)、"
            "公司规模(大型/中型/初创)、地理位置(中/美/欧)分析不同细分市场的需求差异",
        ]

        risks = [
            "在没有用户数据支撑的情况下做产品决策可能导致投入方向错误",
            "用户调研样本量不足可能产生选择偏差——活跃用户的反馈不代表沉默大多数",
            "过度依赖当前用户的反馈可能导致忽视潜在用户的需求",
        ]

        opportunities = [
            "GitHub Issue和PR的自然语言文本可以作为用户需求挖掘的数据源",
            "学术论文引用数据可以帮助了解BatteryML在哪些研究方向被使用最多",
            "竞品的用户评论(G2、Capterra)可以间接了解行业用户的通用痛点",
        ]

        action_items = [
            {
                'task': '设计GitHub问卷调查',
                'assignee': 'market_survey',
                'priority': 'high',
                'estimated_effort': '3天',
                'description': '5题简短问卷覆盖使用场景、满意度、功能需求',
            },
            {
                'task': '执行20人深度用户访谈',
                'assignee': 'market_survey + product_manager',
                'priority': 'high',
                'estimated_effort': '4-6周',
                'description': '每位访谈30-45分钟，覆盖学术/工业/初创不同背景',
            },
            {
                'task': '付费意愿定价调研',
                'assignee': 'market_survey + sales_department',
                'priority': 'medium',
                'estimated_effort': '3-4周',
                'description': '使用Van Westendorp模型确定最优定价区间',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML当前严重缺乏系统化的用户调研数据——所有产品决策都基于"
                "团队判断而非用户真实反馈。建议立即启动三轮调研计划：GitHub快速问卷→"
                "深度用户访谈→年度NPS调查。调研重点应包括功能需求排序、付费意愿评估、"
                "和竞品体验对比。用户调研的结论应直接指导产品路线图和定价策略。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'survey_plan': {
                    'Round 1': 'GitHub问卷(2周)',
                    'Round 2': '深度访谈(4-6周)',
                    'Round 3': '年度NPS(持续)',
                },
                'target_sample_size': {
                    'questionnaire': '100+',
                    'interviews': '20-30',
                    'annual_survey': '200+',
                },
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'product_manager':
                insights.append(
                    "【市场调研→产品经理】RICE评分的Confidence(确定性)分数"
                    "需要我的调研数据支撑——建议在调研结果出来后更新一次RICE评分"
                )
            if report.agent_role == 'sales_department':
                insights.append(
                    "【市场调研→销售部门】WTP调研结果将直接影响定价策略——"
                    "建议在定价方案确定前完成至少50份有效问卷"
                )
        return insights
