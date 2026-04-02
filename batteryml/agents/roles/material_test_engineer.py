"""
Material Test Engineer Agent - 材料测试工程师智能体

Analyzes the BatteryML project from the perspective of battery material
characterization, testing methodologies, and material quality assurance.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class MaterialTestEngineerAgent(BaseAgent):
    """Agent representing a material test engineer.

    Focus areas:
    - Material characterization test coverage
    - Battery cell aging test protocols
    - Material degradation testing methodology
    - Quality control for battery materials
    - Test data standardization
    """

    def __init__(self):
        super().__init__(
            name="MT Engineer Sun - 材料测试工程师",
            role=AgentRole.MATERIAL_TEST_ENGINEER,
            description=(
                "Material characterization and testing expert specializing in "
                "battery material degradation analysis, aging test protocol "
                "design, and quality control methodologies."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "characterization_test_coverage",
            "aging_test_protocol_diversity",
            "degradation_testing_methodology",
            "quality_control_integration",
            "test_data_standardization",
            "post_mortem_analysis_support",
            "accelerated_aging_validation",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "数据集涵盖了多种循环老化测试协议——包括不同C-rate(0.5C-8C)、"
            "不同温度(25-45°C)、不同截止电压的加速老化方案",

            "CyclingProtocol数据模型记录了充放电速率(C-rate)、电流(A)、电压(V)、"
            "功率(W)、起止SOC等关键协议参数，协议描述较为完整",

            "缺少日历老化(Calendar Aging)测试数据——现有数据集全部为循环老化，"
            "而实际电池寿命中日历老化可能贡献30-50%的容量衰减",

            "缺少后验分析(Post-mortem)数据支持——拆解分析后的极片SEM图像、"
            "XRD谱图等结构化数据无法接入平台",

            "加速老化测试与实际使用条件之间的等效性未被建模——"
            "无法验证高C-rate加速测试结果是否能准确外推至正常使用条件",

            "材料批次一致性信息缺失——同一化学体系不同批次电芯的性能差异"
            "可能影响模型泛化能力，但当前数据模型未记录批次信息",

            "湿度、振动等环境应力因素未纳入——实际应用中(特别是车载环境)"
            "这些因素对电池老化有显著影响",
        ]

        recommendations = [
            "【高优先级】增加日历老化数据集支持——开发Calendar Aging数据预处理器，"
            "支持基于时间的SOH衰减建模(而不仅仅是循环次数)",

            "【高优先级】开发加速因子(Acceleration Factor)计算工具——"
            "基于Arrhenius方程和经验公式，将加速测试结果映射到实际使用条件",

            "【中优先级】在BatteryData中增加材料测试元数据：\n"
            "  - batch_number: 生产批次号\n"
            "  - manufacturing_date: 生产日期\n"
            "  - initial_characterization: 初始性能测试结果\n"
            "  - storage_conditions: 存储条件(温度、SOC)",

            "【中优先级】开发多应力老化模型框架——支持温度×C-rate×DOD"
            "多因子交叉的老化加速模型",

            "【低优先级】探索后验分析数据集成——定义标准化的Post-mortem数据格式，"
            "支持SEM/XRD/EDX等表征数据的结构化存储",

            "【低优先级】增加电芯间一致性分析工具——统计同批次电芯的"
            "容量分布、内阻分布，评估材料工艺质量",
        ]

        risks = [
            "仅基于循环老化数据训练的模型可能低估实际电池老化速度——"
            "因为忽略了日历老化的贡献",

            "加速测试条件可能激活在正常使用条件下不会发生的降解机制——"
            "导致模型学习到错误的老化模式",

            "材料批次差异如果不加以控制，可能在数据集中引入系统性噪声",
        ]

        opportunities = [
            "结合循环老化和日历老化的综合寿命预测模型是行业急需但尚未解决的问题",
            "材料批次追溯和质量控制与欧盟电池护照要求高度吻合",
            "后验分析数据的机器学习(如SEM图像的自动化分析)是新兴的研究方向",
        ]

        action_items = [
            {
                'task': '开发日历老化数据处理模块',
                'assignee': 'material_test_engineer',
                'priority': 'high',
                'estimated_effort': '2周',
                'description': '支持基于时间的存储老化数据导入和SOH建模',
            },
            {
                'task': '实现加速因子计算工具',
                'assignee': 'material_test_engineer + material_scientist',
                'priority': 'high',
                'estimated_effort': '2周',
                'description': '基于Arrhenius方程实现温度加速因子和'
                               'C-rate加速因子的计算',
            },
            {
                'task': '扩展BatteryData批次信息字段',
                'assignee': 'material_test_engineer',
                'priority': 'medium',
                'estimated_effort': '3天',
                'description': '增加batch_number、manufacturing_date等字段',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML在循环老化测试数据处理方面表现良好，支持多种充放电协议。"
                "但存在三个关键缺失：(1)不支持日历老化数据——可能低估30-50%的实际老化 "
                "(2)缺少加速因子计算——无法将加速测试结果映射到实际使用条件 "
                "(3)材料批次信息未记录——影响质量控制和可追溯性。"
                "建议优先开发日历老化支持和加速因子计算工具。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'test_types_supported': ['Cycle Aging'],
                'test_types_missing': [
                    'Calendar Aging', 'Dynamic Profile',
                    'Abuse Testing', 'Post-mortem',
                ],
                'protocols_in_datasets': [
                    'Constant Current', 'CC-CV',
                    'Multi-step Charging', 'Fast Charging',
                ],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'material_scientist':
                insights.append(
                    "【材料测试→材料科学家】加速老化实验设计需要你的指导——"
                    "特别是确保加速条件不会改变主导降解机制"
                )
            if report.agent_role == 'hardware_test_engineer':
                insights.append(
                    "【材料测试→硬件测试】同意统一数据质量标准——"
                    "建议将我们的测试协议规范和你的设备规范整合为一份完整的测试指南"
                )
        return insights
