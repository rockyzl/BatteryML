"""
Battery Application Engineer Agent - 电池应用工程师智能体

Analyzes the BatteryML project from the perspective of real-world
battery applications, system integration, and deployment scenarios.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class BatteryApplicationEngineerAgent(BaseAgent):
    """Agent representing a battery application engineer.

    Focus areas:
    - Electric vehicle (EV) application scenarios
    - Energy storage systems (ESS)
    - Consumer electronics applications
    - Battery management system (BMS) integration
    - Real-world deployment constraints
    - Safety and compliance requirements
    """

    def __init__(self):
        super().__init__(
            name="Engineer Wang - 电池应用工程师",
            role=AgentRole.BATTERY_APPLICATION_ENGINEER,
            description=(
                "Experienced battery application engineer specializing in "
                "EV battery packs, energy storage systems, and BMS integration. "
                "Evaluates the platform's practical applicability in real-world "
                "battery deployment scenarios."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "ev_application_readiness",
            "ess_application_readiness",
            "bms_integration_potential",
            "safety_compliance",
            "real_world_deployment_constraints",
            "edge_computing_compatibility",
            "multi_cell_pack_level_analysis",
            "operational_condition_coverage",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "BatteryML当前专注于单体电芯(Cell)级别的寿命预测，"
            "不支持模组(Module)和电池包(Pack)级别的分析——而实际应用中"
            "电池包的健康管理才是终端需求",

            "支持的数据集主要来自实验室加速老化测试，与实际使用场景"
            "(动态负载、变温环境、不规则充放电)存在差距",

            "缺少BMS集成接口——实际部署中需要与电池管理系统通信，"
            "获取实时电压、电流、温度数据进行在线预测",

            "不支持实时在线推理(Online Inference)模式——当前只能批量离线预测，"
            "无法嵌入到BMS控制回路中进行实时SOH估计",

            "缺少边缘计算(Edge Computing)优化——BMS通常运行在资源受限的"
            "嵌入式处理器上，需要轻量化模型部署方案",

            "安全相关的指标建模不足——缺少对热失控风险预测、内短路检测、"
            "锂枝晶生长预警等安全关键场景的支持",

            "不支持动态工况(Dynamic Profile)数据——如UDDS、HWFET等标准驾驶工况"
            "下的电池性能预测",

            "缺少二次利用(Second-life)评估功能——退役EV电池在储能场景的"
            "剩余价值评估是新兴的重要需求",
        ]

        recommendations = [
            "【高优先级】开发Pack级别分析框架——支持从单体到模组到电池包的"
            "多层级健康管理，考虑一致性(Consistency)问题",

            "【高优先级】实现在线推理API——开发RESTful API或gRPC服务接口，"
            "支持实时数据流输入和SOH/RUL预测输出",

            "【高优先级】增加动态工况数据支持——集成UDDS、WLTP等标准驾驶工况"
            "数据集，开发工况自适应的寿命预测模型",

            "【中优先级】开发轻量化模型导出——支持ONNX、TensorFlow Lite格式导出，"
            "模型量化(INT8/FP16)和剪枝，适配边缘部署",

            "【中优先级】增加安全预警模型——基于电压/温度异常检测实现"
            "热失控早期预警和内短路概率评估",

            "【中优先级】开发电池二次利用评估模块——评估退役电池的剩余容量、"
            "内阻增长趋势和适用储能场景",

            "【低优先级】支持CAN总线协议数据格式——实现与主流BMS控制器的"
            "数据交互标准",

            "【低优先级】增加SOC(State of Charge)估计功能，与现有SOH/RUL"
            "预测形成完整的电池状态估计工具链",
        ]

        risks = [
            "纯实验室数据训练的模型直接用于实际工况可能产生严重偏差——"
            "实验室恒流恒压循环与实际动态负载差异巨大",

            "缺少安全相关功能可能阻碍在汽车行业(ISO 26262功能安全标准)"
            "的应用推广",

            "边缘部署性能不达标可能导致BMS实时性要求无法满足——"
            "关键控制回路的延迟要求通常在毫秒级",

            "Pack级别的一致性问题(最差电芯决定整包性能)如果不加以考虑，"
            "预测结果可能过于乐观",
        ]

        opportunities = [
            "全球EV市场年增长率超过30%，电池健康管理是核心技术需求——"
            "市场空间巨大",

            "储能行业的电池安全事故频发，智能预警系统需求迫切——"
            "BatteryML可以成为安全管理的核心工具",

            "V2G(Vehicle-to-Grid)双向充电技术兴起，需要更精确的"
            "电池SOH估计来优化充放电策略",

            "电池护照(Battery Passport)法规即将在欧盟实施，"
            "BatteryML可以提供寿命预测数据支撑",
        ]

        action_items = [
            {
                'task': '开发在线推理API服务',
                'assignee': 'battery_application_engineer + software_test_engineer',
                'priority': 'high',
                'estimated_effort': '2-3周',
                'description': '基于FastAPI开发RESTful推理服务，支持实时SOH/RUL预测',
            },
            {
                'task': '实现ONNX模型导出',
                'assignee': 'battery_application_engineer + data_scientist',
                'priority': 'medium',
                'estimated_effort': '1-2周',
                'description': '为PyTorch模型添加ONNX导出功能，支持边缘设备部署',
            },
            {
                'task': '开发Pack级分析原型',
                'assignee': 'battery_application_engineer',
                'priority': 'high',
                'estimated_effort': '3-4周',
                'description': '设计多层级数据模型(Cell→Module→Pack)和一致性分析框架',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML在实验室级别的电芯寿命预测方面表现出色，但在实际工程应用部署方面"
                "存在显著差距：不支持Pack级分析、缺少在线推理接口、未针对边缘部署优化、"
                "缺少安全预警功能。建议优先开发在线推理API和Pack级分析框架，"
                "同时增加动态工况数据支持和轻量化模型导出功能，以满足EV、储能等"
                "实际应用场景的需求。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'application_scenarios': ['EV', 'ESS', 'Consumer Electronics'],
                'deployment_targets': ['Cloud', 'Edge', 'BMS Embedded'],
                'standards': ['ISO 26262', 'IEC 62619', 'UN38.3', 'EU Battery Passport'],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'material_scientist':
                insights.append(
                    "【应用工程师→材料科学家】请特别关注低温环境(-20℃以下)"
                    "的材料老化行为建模——这是EV冬季续航焦虑的核心技术瓶颈"
                )
            if report.agent_role == 'investor':
                insights.append(
                    "【应用工程师→投资方】BMS集成和边缘部署能力是商业化的关键——"
                    "建议将此作为产品化路线图的第一优先级"
                )
        return insights
