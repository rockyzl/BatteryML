"""
Marketing Engineer Agent - 市场推广工程师智能体

Analyzes the BatteryML project from the perspective of product marketing,
developer community building, and technology evangelism.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class MarketingEngineerAgent(BaseAgent):
    """Agent representing a marketing engineer / developer advocate.

    Focus areas:
    - Open source community growth strategies
    - Developer documentation and onboarding
    - Technical content marketing
    - Conference and publication presence
    - Competitive positioning
    - Brand awareness in the battery ML ecosystem
    """

    def __init__(self):
        super().__init__(
            name="Mark Growth - 市场推广工程师",
            role=AgentRole.MARKETING_ENGINEER,
            description=(
                "Technology marketing expert focused on open-source community "
                "building, developer relations, technical content creation, "
                "and competitive positioning in the battery AI ecosystem."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "community_growth_potential",
            "documentation_quality",
            "onboarding_experience",
            "competitive_positioning",
            "content_marketing_strategy",
            "conference_presence",
            "partnership_opportunities",
            "brand_awareness",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "项目由Microsoft发布，已在ICLR 2024发表论文(https://arxiv.org/abs/2310.14714)，"
            "具有强大的学术背书和品牌信誉",

            "README文档提供了基本的Quick Start指南，但缺少详细的API文档、"
            "教程(Tutorial)系列、最佳实践(Best Practices)等深度内容",

            "MIT开源许可证对商业友好，降低了企业采用的法律门槛",

            "项目定位为'电池降解预测的开源机器学习工具'——在垂直领域AI工具中"
            "具有明确且独特的价值主张",

            "缺少活跃的社区运营——没有Discord/Slack社区、没有定期的Newsletter、"
            "没有Contributors指南，社区参与度可能较低",

            "没有官方网站或Landing Page——首次接触的用户只能通过GitHub仓库"
            "了解项目，第一印象不够专业",

            "Benchmark结果展示形式单一(论文中的表格)——缺少类似Papers with Code"
            "的在线Leaderboard来吸引研究者提交新结果",

            "缺少用户案例(Case Study)和成功故事(Success Story)来证明"
            "平台的实际应用价值",
        ]

        recommendations = [
            "【高优先级】建立项目官方文档站(基于MkDocs或Sphinx)，包含API Reference、"
            "Tutorial系列、FAQ、Changelog等，提升专业度和可发现性",

            "【高优先级】创建'Awesome BatteryML'生态列表和在线Benchmark Leaderboard，"
            "激励研究社区提交新模型和新结果，形成正向飞轮效应",

            "【高优先级】建立Discord/微信群等社区频道，定期举办Office Hours、"
            "AMA(Ask Me Anything)活动，拉近与用户的距离",

            "【中优先级】开发系列教程博客——如'5分钟入门BatteryML'、"
            "'从零到一构建你的电池寿命预测模型'、'BatteryML与你的数据集集成指南'等",

            "【中优先级】在电池行业会议(如ECS Meeting、International Battery Seminar)"
            "和AI会议(NeurIPS、ICML Workshop)上做演讲和Demo展示",

            "【中优先级】收集并发布3-5个用户案例(Case Study)，展示BatteryML"
            "在EV、储能、消费电子等领域的实际应用效果",

            "【低优先级】制作1-2分钟的项目介绍视频(YouTube/B站)，"
            "直观展示平台功能和使用流程",

            "【低优先级】建立GitHub Discussions板块，分类讨论(Q&A、Ideas、Show & Tell)，"
            "将一次性的Issue讨论转化为可搜索的知识库",
        ]

        risks = [
            "如果不主动运营社区，项目可能逐渐失去关注度和活跃贡献者",
            "竞品(如PyBaMM、BEEP等)如果在市场推广上更积极，"
            "可能抢占BatteryML的目标用户群",
            "仅依赖一篇论文的影响力是不可持续的，需要持续产出高质量内容",
        ]

        opportunities = [
            "电池AI是一个快速增长的蓝海领域，竞争对手少，先发优势明显",
            "Microsoft品牌背书有助于吸引企业级用户，可以尝试与Azure云服务整合推广",
            "可以与高校电池实验室合作，将BatteryML纳入教学课程，"
            "培养下一代用户群",
            "举办BatteryML Hackathon/竞赛活动，快速提升社区活跃度和知名度",
        ]

        action_items = [
            {
                'task': '搭建MkDocs官方文档站',
                'assignee': 'marketing_engineer + data_scientist',
                'priority': 'high',
                'estimated_effort': '2-3周',
                'description': '创建完整的API文档、教程系列和贡献者指南',
            },
            {
                'task': '创建在线Benchmark Leaderboard',
                'assignee': 'marketing_engineer + data_analyst_frontend',
                'priority': 'high',
                'estimated_effort': '2周',
                'description': '开发交互式排行榜页面，展示各模型在各数据集上的性能排名',
            },
            {
                'task': '建立社区Discord频道',
                'assignee': 'marketing_engineer',
                'priority': 'high',
                'estimated_effort': '1天',
                'description': '创建Discord服务器，设置FAQ、Showcase、Help等频道',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML具有强大的学术背书(ICLR 2024)和品牌支撑(Microsoft)，"
                "但在社区运营、文档完善度、内容营销等方面存在明显短板。建议优先建立"
                "专业的文档站和社区频道，通过Benchmark Leaderboard和教程系列"
                "吸引研究社区参与，同时收集用户案例证明实际应用价值。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="medium",
            metadata={
                'academic_backing': 'ICLR 2024',
                'license': 'MIT',
                'organization': 'Microsoft',
                'competitors': ['PyBaMM', 'BEEP', 'battery-data-toolkit'],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'data_analyst_frontend_engineer':
                insights.append(
                    "【市场推广→前端工程师】Web可视化仪表板是最好的'活广告'——"
                    "建议优先开发在线Demo页面，让用户无需安装即可体验核心功能"
                )
            if report.agent_role == 'sales_department':
                insights.append(
                    "【市场推广→销售部门】建议联合制作'ROI计算器'——帮助潜在客户"
                    "量化使用BatteryML带来的成本节省和效率提升"
                )
        return insights
