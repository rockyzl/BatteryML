"""
Data Analyst & Frontend Engineer Agent - 数据分析前端工程师智能体

Analyzes the BatteryML project from the perspective of data visualization,
user interface design, dashboard development, and data presentation.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class DataAnalystFrontendEngineerAgent(BaseAgent):
    """Agent representing a data analyst who is also a frontend engineer.

    Focus areas:
    - Data visualization quality and completeness
    - Interactive dashboard opportunities
    - User interface design for data exploration
    - Reporting and analytics capabilities
    - Web-based visualization platform potential
    """

    def __init__(self):
        super().__init__(
            name="Alex Analytics - 数据分析前端工程师",
            role=AgentRole.DATA_ANALYST_FRONTEND,
            description=(
                "Data visualization and frontend engineering expert. "
                "Evaluates the platform's visualization capabilities, "
                "proposes interactive dashboards, and designs user-friendly "
                "interfaces for battery data exploration and result presentation."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "visualization_quality",
            "interactive_dashboard_potential",
            "data_exploration_tools",
            "reporting_capabilities",
            "user_experience_design",
            "responsive_design",
            "real_time_monitoring_ui",
            "comparison_and_filtering_tools",
            "export_and_sharing_features",
            "accessibility_compliance",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "当前可视化模块(visualization/plot_helper.py)提供了基础的容量衰减曲线绘制"
            "和循环属性可视化功能，基于matplotlib实现，为静态图表",

            "项目提供了3个Jupyter Notebook(baseline.ipynb、result.ipynb、soh_example.ipynb)"
            "作为交互式数据探索工具，但缺少系统化的可视化框架",

            "缺少Web端可视化界面——当前只能通过CLI和Notebook使用，"
            "不利于非技术用户(如电池公司管理层)查看分析结果",

            "数据对比功能有限——难以在同一视图中对比不同电池、不同模型、"
            "不同数据集的分析结果",

            "没有实时数据监控仪表板——无法实时追踪正在进行的电池循环测试"
            "或模型训练进度",

            "缺少结果导出功能——分析结果无法方便地导出为PDF报告、"
            "Excel表格或可分享的HTML页面",

            "matplotlib的可视化在美观度和交互性上都有较大提升空间，"
            "缺少悬停提示(tooltip)、缩放、筛选等交互功能",
        ]

        recommendations = [
            "【高优先级】开发基于Streamlit或Gradio的Web可视化仪表板，"
            "提供直观的电池数据探索界面，包括数据集浏览、特征可视化、"
            "模型对比等核心功能模块",

            "【高优先级】引入Plotly或ECharts替代/补充matplotlib，"
            "实现交互式图表，支持缩放、悬停信息、数据点选择等操作",

            "【中优先级】开发模型对比仪表板——在同一页面展示不同模型在"
            "各数据集上的性能对比，包括雷达图、热力图、箱线图等",

            "【中优先级】实现自动化分析报告生成器——将分析结果自动整合为"
            "结构化的HTML/PDF报告，支持自定义模板",

            "【中优先级】开发电池健康状态实时监控界面——支持WebSocket实时数据推送，"
            "展示充放电曲线、容量趋势、预测结果的实时更新",

            "【低优先级】实现数据集探索界面——提供电池数据的多维度筛选、排序、"
            "统计摘要功能，帮助用户快速了解数据集特征",

            "【低优先级】增加暗色模式(Dark Mode)支持和响应式设计，"
            "适配不同设备和使用场景",
        ]

        risks = [
            "引入Web框架会增加项目依赖复杂度，可能影响纯研究用户的安装体验",
            "实时监控功能需要后端服务支持，增加了部署和运维复杂度",
            "过度投入前端开发可能分散核心ML功能的研发资源",
        ]

        opportunities = [
            "Web可视化界面将大幅降低非技术用户的使用门槛，"
            "扩大BatteryML的用户群体",

            "交互式仪表板可以作为SaaS产品的原型，探索商业化可能性",

            "可视化优秀的开源项目更容易获得star和社区贡献——"
            "好看的demo是最好的推广",

            "集成Jupyter Widget或Panel，可以在Notebook生态中"
            "提供增强的交互体验而不增加太多复杂度",
        ]

        action_items = [
            {
                'task': '开发Streamlit可视化原型',
                'assignee': 'data_analyst_frontend',
                'priority': 'high',
                'estimated_effort': '2-3周',
                'description': '创建包含数据集浏览、特征可视化、模型对比'
                               '三个核心模块的Streamlit应用',
            },
            {
                'task': '替换matplotlib为Plotly交互图表',
                'assignee': 'data_analyst_frontend',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '为核心可视化函数(容量衰减曲线、特征分布)'
                               '提供Plotly版本的交互实现',
            },
            {
                'task': '开发自动化报告生成模块',
                'assignee': 'data_analyst_frontend + data_scientist',
                'priority': 'medium',
                'estimated_effort': '2周',
                'description': '基于Jinja2模板引擎生成HTML/PDF分析报告',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML当前的可视化能力仅限于基础的matplotlib静态图表和Jupyter Notebook，"
                "缺少Web端交互界面、实时监控仪表板和自动化报告生成功能。建议优先开发基于"
                "Streamlit的Web可视化平台和基于Plotly的交互式图表组件，这将显著提升"
                "用户体验并扩大目标用户群体。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="medium",
            metadata={
                'current_visualization': ['matplotlib', 'Jupyter Notebook'],
                'proposed_stack': [
                    'Streamlit/Gradio', 'Plotly/ECharts',
                    'Jinja2', 'WebSocket',
                ],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'data_scientist':
                insights.append(
                    "【前端工程师→数据科学家】SHAP可解释性分析的结果可以用"
                    "交互式力图(Force Plot)和蜂群图(Beeswarm Plot)展示，"
                    "我可以协助设计最佳的可视化呈现方案"
                )
            if report.agent_role == 'end_user':
                insights.append(
                    "【前端工程师→终端用户】我会优先设计简洁直观的界面，"
                    "确保非技术用户也能轻松理解分析结果"
                )
        return insights
