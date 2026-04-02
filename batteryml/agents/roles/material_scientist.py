"""
Material Scientist Agent - 材料科学家智能体

Analyzes the BatteryML project from the perspective of battery materials,
electrochemistry, degradation mechanisms, and material characterization.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class MaterialScientistAgent(BaseAgent):
    """Agent representing a battery material scientist.

    Focus areas:
    - Battery chemistry coverage (LFP, NMC, NCA, LCO, etc.)
    - Degradation mechanism modeling accuracy
    - Material characterization data quality
    - Electrochemical feature relevance
    - Anode/cathode/electrolyte material diversity
    """

    def __init__(self):
        super().__init__(
            name="Dr. Materials - 材料科学家",
            role=AgentRole.MATERIAL_SCIENTIST,
            description=(
                "Battery materials expert specializing in electrochemistry, "
                "degradation mechanisms (SEI growth, lithium plating, active "
                "material loss), and material characterization. Evaluates the "
                "scientific rigor and material coverage of the platform."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "battery_chemistry_coverage",
            "degradation_mechanism_modeling",
            "material_characterization_quality",
            "electrochemical_feature_relevance",
            "cathode_material_diversity",
            "anode_material_diversity",
            "electrolyte_system_coverage",
            "cycling_protocol_representation",
            "temperature_effect_modeling",
            "capacity_fade_mechanism_accuracy",
            "impedance_data_utilization",
            "voltage_profile_analysis_depth",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "项目支持8个公开电池数据集，覆盖LFP/石墨、NMC_LCO/石墨、NCA/石墨、NMC/碳等"
            "多种主流电池化学体系，材料体系覆盖面较广",

            "BatteryData数据模型包含阳极材料(anode_material)、阴极材料(cathode_material)、"
            "电解质材料(electrolyte_material)等关键材料属性字段，数据结构设计合理",

            "CycleData记录了电压(V)、电流(A)、充放电容量(Ah)、温度(℃)、内阻(Ω)等"
            "完整的循环数据，能够捕获关键的电化学老化特征",

            "Severson特征提取器实现了方差模型(Variance)、放电模型(Discharge)和"
            "完整模型(Full)三种特征工程方案，基于领域专家知识设计",

            "RUL标签标注器使用EOL SOH阈值(默认0.8)来定义电池寿命终点(End-of-Life)，"
            "这与工业界80%容量保持率的通用标准一致",

            "电压-容量矩阵特征提取器(VoltageCapacityMatrix)通过插值和差分操作"
            "捕获容量衰减曲线的形状变化，具有良好的物理可解释性",

            "当前数据集以磷酸铁锂(LFP)和三元材料(NMC/NCA)为主，缺少对"
            "新兴材料体系如固态电池、钠离子电池、锂硫电池等的支持",

            "降解机制建模主要基于容量衰减曲线的统计特征，未显式建模SEI膜生长、"
            "锂枝晶析出、正极材料相变等具体物理化学机制",

            "缺少阻抗谱(EIS)数据分析模块，电化学阻抗谱是表征电池老化状态的"
            "重要工具，目前仅记录内阻而未进行频域分析",

            "温度效应建模不足，虽然CycleData记录了温度数据，但特征提取器"
            "未充分利用温度信息来建模Arrhenius温度依赖关系",
        ]

        recommendations = [
            "【高优先级】引入固态电池(Solid-State)、钠离子电池(Na-ion)材料体系数据集，"
            "扩展平台在新兴储能材料领域的覆盖范围",

            "【高优先级】增加基于物理机制的降解模型(Physics-informed models)，"
            "将SEI生长动力学、锂枝晶生长模型等嵌入特征工程和模型架构中",

            "【中优先级】开发阻抗谱(EIS)分析模块，支持Nyquist图、Bode图的自动化分析，"
            "提取等效电路模型参数(R_ct, R_SEI, C_dl, W等)作为老化特征",

            "【中优先级】增加温度加速老化模型，实现Arrhenius方程参数提取，"
            "支持不同温度条件下的寿命预测模型校准",

            "【中优先级】添加微分容量分析(dQ/dV)和微分电压分析(dV/dQ)模块，"
            "这些技术能直接反映电极材料的相变和活性物质损失",

            "【低优先级】增加对半电池数据的支持，允许分离正极和负极的独立老化贡献",

            "【低优先级】考虑集成密度泛函理论(DFT)计算结果作为材料描述符，"
            "提高模型的物理可解释性和迁移学习能力",
        ]

        risks = [
            "当前模型可能在不同材料体系间的迁移性较差——在LFP体系上训练的模型"
            "直接应用于NMC体系可能产生较大误差",

            "忽视温度效应可能导致模型在实际工况(高温/低温极端条件)下性能大幅下降",

            "缺少物理约束的纯数据驱动模型可能产生违反电化学基本定律的预测结果"
            "(如预测容量恢复超过理论值)",

            "数据集中电解质信息记录不完整，可能遗漏电解质老化(如LiPF6分解)"
            "对电池寿命的重要影响",
        ]

        opportunities = [
            "固态电池市场正在快速增长(预计2030年达到数百亿美元)，率先支持固态电池"
            "数据分析将获得巨大的先发优势",

            "结合机理模型与数据驱动模型(Hybrid Model)是当前学术界和工业界的热门方向，"
            "BatteryML可以成为这一领域的标杆平台",

            "与材料基因组(Materials Genome)数据库集成，实现从材料组成到电池寿命的"
            "端到端预测，具有重大科学价值",

            "开发针对电池回收(Recycling)场景的材料状态评估功能，契合循环经济趋势",
        ]

        action_items = [
            {
                'task': '新增固态电池数据预处理模块',
                'assignee': 'material_scientist',
                'priority': 'high',
                'estimated_effort': '2-3周',
                'description': '开发支持固态电池循环数据的预处理器，'
                               '包括界面阻抗、枝晶生长等特有指标',
            },
            {
                'task': '实现dQ/dV微分容量分析特征提取器',
                'assignee': 'material_scientist + data_scientist',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '基于微分容量曲线的峰位移、峰面积变化'
                               '提取材料老化特征',
            },
            {
                'task': '建立材料体系迁移学习基准测试',
                'assignee': 'material_scientist + data_scientist',
                'priority': 'medium',
                'estimated_effort': '2-3周',
                'description': '系统评估模型在不同化学体系间的迁移能力，'
                               '建立跨材料预测的基准指标',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML在电池材料数据建模方面具备良好基础，覆盖了主流锂离子电池化学体系，"
                "数据模型设计合理。但在新兴材料体系支持、物理机制建模深度、阻抗谱分析、"
                "温度效应建模等方面存在提升空间。建议优先引入物理信息增强的特征工程方法，"
                "并扩展对固态电池和钠离子电池等新兴材料体系的支持。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'chemistry_systems_covered': [
                    'LFP/Graphite', 'NMC_LCO/Graphite',
                    'NCA/Graphite', 'NMC/Carbon', 'LCO/Graphite',
                ],
                'datasets_analyzed': [
                    'CALCE', 'MATR', 'HUST', 'HNEI',
                    'RWTH', 'SNL', 'UL_PUR', 'OX',
                ],
                'missing_chemistry_systems': [
                    'Solid-State', 'Na-ion', 'Li-S',
                    'Li-Air', 'LTO/NMC',
                ],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'data_scientist':
                insights.append(
                    "【材料科学家→数据科学家】建议在模型训练中加入材料体系标签"
                    "作为条件变量，使模型能够学习不同化学体系的老化差异"
                )
            if report.agent_role == 'battery_application_engineer':
                insights.append(
                    "【材料科学家→应用工程师】不同应用场景(EV/储能/消费电子)"
                    "对材料性能的要求差异很大，建议按应用场景细分材料评估标准"
                )
            if report.agent_role == 'hardware_test_engineer':
                insights.append(
                    "【材料科学家→硬件测试工程师】建议增加原位表征测试数据的接入，"
                    "如原位XRD、原位Raman等，丰富材料老化信息"
                )
        return insights
