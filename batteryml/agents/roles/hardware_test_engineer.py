"""
Hardware Test Engineer Agent - 硬件测试工程师智能体

Analyzes the BatteryML project from the perspective of battery hardware
testing, test equipment, data acquisition, and test protocol validation.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class HardwareTestEngineerAgent(BaseAgent):
    """Agent representing a hardware test engineer.

    Focus areas:
    - Battery test equipment compatibility
    - Data acquisition quality and sampling rates
    - Test protocol coverage and standardization
    - Hardware-software integration
    - Test automation and throughput
    - Calibration and measurement accuracy
    """

    def __init__(self):
        super().__init__(
            name="HW Engineer Liu - 硬件测试工程师",
            role=AgentRole.HARDWARE_TEST_ENGINEER,
            description=(
                "Battery hardware testing expert with deep knowledge of "
                "cycling equipment (Arbin, Neware, Biologic), test chamber "
                "configuration, and data acquisition systems. Evaluates "
                "hardware compatibility and data quality aspects."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "equipment_compatibility",
            "data_acquisition_quality",
            "test_protocol_coverage",
            "hw_sw_integration",
            "test_automation",
            "calibration_accuracy",
            "sampling_rate_adequacy",
            "environmental_chamber_support",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "项目支持2种主流充放电设备格式：ARBIN和NEWARE，另有Biologic、LANDT、"
            "Indigo正在开发中——覆盖了市场上约60%的测试设备",

            "数据预处理模块能够处理不同设备的原始数据格式差异"
            "(CSV/Excel/MAT等)，标准化为统一的BatteryData格式",

            "缺少对Maccor充放电测试仪的支持——Maccor在北美和欧洲市场"
            "占有率约20%，是重要的数据源",

            "采样率信息未在数据模型中显式记录——不同设备的采样率差异"
            "(从0.1s到60s)可能影响特征提取的准确性",

            "温度数据的采集精度和位置(表面/环境/内部)未区分——"
            "不同位置的温度差异可达5-10°C，对模型预测有显著影响",

            "缺少多通道并行测试数据的处理能力——工业级测试设备通常"
            "同时运行数十到数百个通道，需要高效的批量处理",

            "内阻测量方法(AC/DC/EIS)未标准化——不同方法得到的内阻值"
            "可能差异较大，直接比较会引入系统误差",

            "没有数据采集质量检查——传感器漂移、通信中断、采样跳变等"
            "硬件级别的数据质量问题未被检测和处理",
        ]

        recommendations = [
            "【高优先级】增加Maccor数据格式支持——完成ARBIN/NEWARE/Biologic/Maccor"
            "四大设备的全覆盖，满足90%以上实验室的需求",

            "【高优先级】开发数据采集质量自动检查模块：\n"
            "  - 采样率异常检测(突然变化或中断)\n"
            "  - 电压/电流/温度传感器漂移检测\n"
            "  - 通道间一致性校验(多通道测试时)\n"
            "  - 容量跳变检测(设备重启或通信错误导致)",

            "【中优先级】在CycleData中增加元数据字段：\n"
            "  - sampling_rate_in_hz: 采样频率\n"
            "  - temperature_location: 温度传感器位置\n"
            "  - resistance_measurement_method: 内阻测量方法\n"
            "  - equipment_model: 测试设备型号",

            "【中优先级】支持大规模并行数据处理——优化I/O操作，"
            "支持流式处理(Streaming)和内存映射(Memory-mapped)文件，"
            "处理百通道级别的测试数据",

            "【低优先级】开发测试设备驱动层(HAL: Hardware Abstraction Layer)——"
            "实现与测试设备的实时通信，支持边测边分析",

            "【低优先级】增加标准测试工况模板——如IEC 62660-1(EV循环测试)、"
            "GB/T 31484(中国国标循环测试)等标准协议的预定义",
        ]

        risks = [
            "不同设备的数据精度差异可能导致跨数据集模型训练时引入系统性偏差",
            "传感器故障产生的错误数据如果不被过滤，会污染训练数据集",
            "采样率差异导致特征提取不一致——高采样率数据和低采样率数据"
            "提取的特征可能不具有可比性",
        ]

        opportunities = [
            "与ARBIN/NEWARE等设备厂商建立合作——设备软件预集成BatteryML，"
            "实现'开箱即用'的数据分析",
            "开发设备无关的通用数据采集标准(类似电池领域的ASAM标准)，"
            "引领行业数据规范化",
            "IoT传感器的价格下降使得更密集的数据采集成为可能——"
            "BatteryML应准备好利用这些高分辨率数据",
        ]

        action_items = [
            {
                'task': '增加Maccor数据格式预处理器',
                'assignee': 'hardware_test_engineer',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '解析Maccor原始数据格式(.txt/.csv)并转化为BatteryData',
            },
            {
                'task': '开发数据采集质量检测模块',
                'assignee': 'hardware_test_engineer + software_test_engineer',
                'priority': 'high',
                'estimated_effort': '2-3周',
                'description': '实现采样率异常、传感器漂移、通道不一致等自动检测',
            },
            {
                'task': '扩展CycleData元数据字段',
                'assignee': 'hardware_test_engineer + data_scientist',
                'priority': 'medium',
                'estimated_effort': '1周',
                'description': '增加采样率、温度传感器位置、内阻方法等元数据',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML在测试设备支持方面覆盖了ARBIN和NEWARE两大主流平台，"
                "但缺少Maccor支持。核心问题包括：(1)数据采集质量缺乏自动检查 "
                "(2)采样率和温度传感器位置等关键元数据未记录 (3)内阻测量方法未标准化 "
                "(4)大规模并行测试数据处理能力不足。建议优先增加设备覆盖率和"
                "数据质量自动检查功能。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="medium",
            metadata={
                'supported_equipment': ['ARBIN', 'NEWARE'],
                'in_development': ['Biologic', 'LANDT', 'Indigo'],
                'missing_equipment': ['Maccor', 'BTS', 'Gamry'],
                'data_formats': ['CSV', 'Excel', 'MAT', 'HDF5'],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'material_scientist':
                insights.append(
                    "【硬件测试→材料科学家】同意增加原位表征数据接入——"
                    "建议先从最常用的原位EIS(电化学阻抗谱)开始支持"
                )
            if report.agent_role == 'material_test_engineer':
                insights.append(
                    "【硬件测试→材料测试】建议统一不同测试设备的数据质量标准——"
                    "制定最低采样率要求、精度要求和校准频率规范"
                )
        return insights
