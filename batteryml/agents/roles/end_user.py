"""
End User Agent - 终端用户智能体

Analyzes the BatteryML project from the perspective of researchers,
engineers, and other end users who interact with the tool daily.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class EndUserAgent(BaseAgent):
    """Agent representing an end user (researcher / ML engineer).

    Focus areas:
    - Installation and setup experience
    - Learning curve and documentation quality
    - Daily workflow efficiency
    - Pain points and friction
    - Feature completeness for common tasks
    - Error messages and debugging experience
    """

    def __init__(self):
        super().__init__(
            name="Dr. User - 终端用户",
            role=AgentRole.END_USER,
            description=(
                "A battery researcher and ML practitioner who uses BatteryML "
                "in daily work. Provides ground-truth feedback on usability, "
                "documentation quality, common pain points, and feature requests."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "installation_experience",
            "learning_curve",
            "documentation_completeness",
            "workflow_efficiency",
            "error_handling_quality",
            "customization_flexibility",
            "result_reproducibility",
            "community_support",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "安装流程相对简单(pip install)，但依赖项较多(torch、scipy、h5py、"
            "xgboost等)，首次安装可能遇到版本冲突，特别是PyTorch的CUDA版本匹配",

            "CLI工具(batteryml命令)提供了download/preprocess/run三个核心命令，"
            "workflow清晰明了，但缺少交互式提示和帮助信息",

            "YAML配置文件驱动的实验管理方式灵活但有学习门槛——新用户需要理解"
            "模型、特征提取器、标签标注器、数据变换等概念才能正确配置",

            "数据下载(batteryml download)一键获取公开数据集非常方便，"
            "大大降低了数据准备的门槛",

            "Jupyter Notebook示例(baseline.ipynb、soh_example.ipynb)提供了"
            "很好的入门参考，但缺少中文版本和逐步讲解",

            "错误信息不够友好——当配置错误或数据格式不匹配时，"
            "用户看到的是Python原始异常栈而非有指导意义的错误提示",

            "缺少模型训练进度的可视化——除了tqdm进度条外，没有"
            "TensorBoard或WandB集成来追踪训练曲线",

            "自定义数据集接入流程不够顺畅——需要编写自己的Preprocessor类，"
            "缺少通用的CSV/Excel数据导入工具",

            "可复现性设计较好——支持seed设置和checkpoint保存，"
            "但缺少完整的实验管理(如MLflow集成)来追踪所有实验",
        ]

        recommendations = [
            "【高优先级】提供'一键上手'的Colab Notebook——让新用户无需本地安装"
            "即可在5分钟内运行第一个示例",

            "【高优先级】开发通用数据导入工具——支持从CSV/Excel文件直接导入"
            "自定义电池数据，自动匹配BatteryData字段映射",

            "【高优先级】改善错误信息——对常见错误场景(配置文件格式错误、"
            "数据路径不存在、模型-特征维度不匹配等)提供清晰的错误描述和修复建议",

            "【中优先级】集成TensorBoard或WandB——自动记录训练/验证损失曲线、"
            "学习率变化、模型性能指标，方便实验追踪",

            "【中优先级】增加CLI的交互模式——通过问答式引导帮助新用户创建"
            "配置文件，而不是要求手动编辑YAML",

            "【中优先级】编写中英文双语教程系列——从数据准备到模型训练再到结果分析，"
            "完整覆盖典型使用流程",

            "【低优先级】开发VS Code插件——提供YAML配置文件的语法高亮和自动补全，"
            "减少配置错误",
        ]

        risks = [
            "过高的学习曲线可能使非ML背景的电池研究人员望而却步",
            "缺少社区支持渠道可能导致遇到问题的用户直接放弃使用",
            "Python依赖冲突可能导致部分用户无法成功安装",
        ]

        opportunities = [
            "Google Colab免费GPU资源可以大幅降低深度学习模型的使用门槛",
            "中文电池研究社区庞大——中文文档和教程将大幅扩大用户群",
            "与JupyterHub集成可以提供团队协作功能",
        ]

        action_items = [
            {
                'task': '创建Google Colab一键体验Notebook',
                'assignee': 'end_user + data_scientist',
                'priority': 'high',
                'estimated_effort': '3天',
                'description': '制作可直接在Colab中运行的Demo Notebook，'
                               '包含数据下载、模型训练、结果可视化全流程',
            },
            {
                'task': '开发CSV/Excel通用数据导入器',
                'assignee': 'end_user + software_test_engineer',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '基于列名自动映射的通用数据导入工具',
            },
            {
                'task': '改善错误提示和诊断信息',
                'assignee': 'software_test_engineer',
                'priority': 'medium',
                'estimated_effort': '1周',
                'description': '为10个最常见的错误场景添加友好提示和解决建议',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "作为终端用户，BatteryML的核心功能(数据下载→预处理→模型训练→评估)"
                "流程完整，CLI设计合理。主要痛点集中在：(1)学习门槛较高——需要理解多个"
                "概念和YAML配置 (2)自定义数据接入不够便捷 (3)错误信息不友好 "
                "(4)缺少训练可视化和实验管理工具。建议优先提供Colab一键体验、"
                "通用数据导入工具和改善错误提示。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'user_personas': [
                    'Battery Researcher',
                    'ML Engineer',
                    'Graduate Student',
                    'Industry Engineer',
                ],
                'key_pain_points': [
                    'YAML Configuration Complexity',
                    'Custom Data Import',
                    'Error Messages',
                    'Training Visualization',
                ],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'data_analyst_frontend_engineer':
                insights.append(
                    "【终端用户→前端工程师】Web界面的配置文件编辑器是我最期待的功能——"
                    "可视化选择模型、特征提取器比手写YAML方便太多了"
                )
            if report.agent_role == 'marketing_engineer':
                insights.append(
                    "【终端用户→市场推广】我是通过ICLR论文发现这个项目的——"
                    "建议在各大ML社区(Reddit r/MachineLearning、知乎)也做推广"
                )
        return insights
