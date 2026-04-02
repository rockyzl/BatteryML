"""
Software Test Engineer Agent - 软件测试工程师智能体

Analyzes the BatteryML project from the perspective of software quality,
testing coverage, CI/CD pipeline, and code reliability.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class SoftwareTestEngineerAgent(BaseAgent):
    """Agent representing a software test engineer.

    Focus areas:
    - Unit test coverage
    - Integration test completeness
    - CI/CD pipeline setup
    - Code quality and linting
    - Error handling robustness
    - Regression testing strategy
    - Performance testing
    """

    def __init__(self):
        super().__init__(
            name="Tester Zhang - 软件测试工程师",
            role=AgentRole.SOFTWARE_TEST_ENGINEER,
            description=(
                "Software quality assurance expert specializing in ML system "
                "testing, CI/CD pipelines, and code reliability. Evaluates "
                "test coverage, code quality, and overall software robustness."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "unit_test_coverage",
            "integration_test_coverage",
            "ci_cd_pipeline",
            "code_quality_linting",
            "error_handling",
            "regression_testing",
            "performance_testing",
            "documentation_testing",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "【严重问题】项目完全没有测试套件——没有任何pytest/unittest测试文件，"
            "test覆盖率为0%。这在任何产品级软件中都是不可接受的",

            "【严重问题】没有CI/CD管线——没有GitHub Actions、Azure Pipelines"
            "或任何自动化构建/测试流程，代码变更无法自动验证",

            "代码风格配置(.flake8)存在但未集成到CI中——代码风格检查未强制执行",

            "异常处理覆盖不全——数据预处理模块中大量I/O操作缺少try/except保护，"
            "文件不存在或格式错误时会产生不友好的错误栈",

            "类型注解(Type Hints)使用不一致——部分函数有类型注解，部分没有，"
            "增加了代码理解和维护的难度",

            "依赖版本约束宽松——requirements.txt中部分依赖没有版本上限约束，"
            "可能导致未来的兼容性问题",

            "数据预处理模块涉及大量文件I/O和数据格式转换——这些是最容易出bug的地方，"
            "迫切需要测试覆盖",

            "模型的数值稳定性未经系统验证——极端输入(全零、NaN、极大值)"
            "可能导致训练过程崩溃或产生错误结果",
        ]

        recommendations = [
            "【P0 - 紧急】建立pytest测试框架，分三个阶段逐步提升覆盖率：\n"
            "  Phase 1(2周): 数据模型单元测试(BatteryData/CycleData序列化/反序列化)\n"
            "  Phase 2(3周): 数据预处理集成测试(每种数据源一个端到端测试)\n"
            "  Phase 3(2周): 模型训练/预测冒烟测试(快速验证模型能正常运行)",

            "【P0 - 紧急】搭建GitHub Actions CI管线：\n"
            "  - 每次PR自动运行: flake8 + pytest + mypy\n"
            "  - 每日定时运行: 完整基准测试(可选)\n"
            "  - 发布时运行: 完整测试 + 打包 + 发布到PyPI",

            "【P1 - 重要】为数据预处理模块添加边界条件测试：\n"
            "  - 空文件 / 损坏文件 / 格式错误的文件\n"
            "  - 缺少必要列的数据 / 数据类型不匹配\n"
            "  - 超大文件(内存压力测试)",

            "【P1 - 重要】建立模型回归测试基准——记录每个模型在标准数据集上的"
            "预期指标范围，代码变更后自动验证是否在预期范围内",

            "【P2 - 建议】引入Property-based Testing(如Hypothesis库)——"
            "自动生成各种边界输入测试数据模型的鲁棒性",

            "【P2 - 建议】添加集成测试——验证从数据下载→预处理→特征提取→模型训练→"
            "评估的完整pipeline在真实数据上能正确运行",

            "【P2 - 建议】引入mypy或pyright进行静态类型检查，"
            "逐步为核心模块添加完整的类型注解",
        ]

        risks = [
            "零测试覆盖率意味着任何代码修改都可能引入回归bug而不被发现——"
            "这是项目当前最大的软件工程风险",

            "没有CI意味着代码审查缺少自动化质量门控——可能merge有问题的代码",

            "数据预处理模块与外部数据格式紧耦合——上游数据格式变化可能"
            "静默地破坏预处理逻辑",

            "模型的数值稳定性问题可能导致研究人员得到错误的实验结果——"
            "影响基于BatteryML发表的研究论文的可信度",
        ]

        opportunities = [
            "高测试覆盖率是企业级用户采用开源工具的重要考量因素——"
            "完善测试将直接提升商业化可行性",

            "CI/CD管线可以自动化生成测试报告和benchmark结果——"
            "增强项目的透明度和可信度",

            "良好的测试基础设施会吸引更多的开源贡献者——"
            "贡献者可以放心提交PR而不用担心破坏现有功能",
        ]

        action_items = [
            {
                'task': '搭建pytest框架和第一批测试',
                'assignee': 'software_test_engineer',
                'priority': 'critical',
                'estimated_effort': '2周',
                'description': '创建tests/目录结构，编写BatteryData/CycleData的'
                               '序列化/反序列化单元测试，目标覆盖率30%',
            },
            {
                'task': '配置GitHub Actions CI',
                'assignee': 'software_test_engineer',
                'priority': 'critical',
                'estimated_effort': '3天',
                'description': '设置PR触发的自动化测试(flake8 + pytest)管线',
            },
            {
                'task': '数据预处理边界测试',
                'assignee': 'software_test_engineer',
                'priority': 'high',
                'estimated_effort': '2周',
                'description': '为每种数据源编写正常路径和异常路径测试用例',
            },
            {
                'task': '模型回归测试基准',
                'assignee': 'software_test_engineer + data_scientist',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '记录各模型在MATR数据集上的baseline指标，'
                               '设置回归检测阈值',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML当前最严重的软件工程问题是零测试覆盖率和零CI/CD——"
                "这意味着任何代码修改都无法自动验证正确性。建议立即(P0)搭建pytest框架"
                "和GitHub Actions CI管线，分阶段提升测试覆盖率(30%→60%→80%)。"
                "数据预处理模块的边界条件测试和模型回归测试是最高优先级的测试项目。"
                "在产品化之前，必须达到至少60%的代码覆盖率。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="critical",
            metadata={
                'current_test_coverage': '0%',
                'target_coverage_v0_5': '30%',
                'target_coverage_v1_0': '60%',
                'target_coverage_v2_0': '80%',
                'ci_cd_status': 'None',
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'data_scientist':
                insights.append(
                    "【软件测试→数据科学家】模型回归测试需要你提供各模型的"
                    "预期指标范围——请协助定义'性能退化'的判定阈值"
                )
            if report.agent_role == 'product_manager':
                insights.append(
                    "【软件测试→产品经理】强烈建议将测试覆盖率作为v0.5发布的"
                    "强制门控条件——不达标不发布"
                )
        return insights
