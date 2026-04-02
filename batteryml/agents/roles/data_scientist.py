"""
Data Scientist Agent - 数据科学家智能体

Analyzes the BatteryML project from the perspective of machine learning,
statistical modeling, data quality, and model performance.
"""

from typing import Any, Dict, List

from batteryml.agents.base import AgentRole, AnalysisReport, BaseAgent


class DataScientistAgent(BaseAgent):
    """Agent representing a data scientist.

    Focus areas:
    - Model architecture diversity and appropriateness
    - Feature engineering quality and coverage
    - Training pipeline robustness
    - Evaluation metrics and benchmarking methodology
    - Data quality and preprocessing rigor
    - Hyperparameter tuning strategies
    - Model interpretability and explainability
    """

    def __init__(self):
        super().__init__(
            name="Dr. Data - 数据科学家",
            role=AgentRole.DATA_SCIENTIST,
            description=(
                "Machine learning expert specializing in time series analysis, "
                "predictive modeling, and deep learning. Evaluates model "
                "architectures, training pipelines, evaluation methodology, "
                "and data quality of the BatteryML platform."
            ),
        )

    def get_analysis_dimensions(self) -> List[str]:
        return [
            "model_architecture_diversity",
            "feature_engineering_quality",
            "training_pipeline_robustness",
            "evaluation_metrics_completeness",
            "data_quality_assurance",
            "hyperparameter_optimization",
            "model_interpretability",
            "cross_validation_methodology",
            "overfitting_prevention",
            "scalability_analysis",
            "reproducibility_assessment",
            "benchmark_methodology_rigor",
        ]

    def analyze(self, context: Dict[str, Any]) -> AnalysisReport:
        findings = [
            "模型库涵盖15+种RUL预测模型，从统计模型(线性回归、Ridge、ElasticNet)到"
            "树模型(随机森林、XGBoost)再到深度学习(MLP、LSTM、CNN、Transformer)，"
            "覆盖面全面，形成了完整的基准对比体系",

            "特征工程模块实现了3种基于领域知识的特征提取方案(Variance/Discharge/Full Model)"
            "和1种基于数据驱动的特征提取方案(VoltageCapacityMatrix)，平衡了可解释性和表达能力",

            "训练管线(Pipeline)设计合理，支持YAML配置驱动的实验管理，checkpoint保存与恢复，"
            "多种数据变换(ZScore/LogScale/Sequential)的组合应用",

            "Registry模式实现的组件注册系统使得模型、特征提取器、标签标注器等组件高度解耦，"
            "添加新组件只需注册即可，架构设计具有良好的可扩展性",

            "评估指标目前主要使用RMSE，缺少MAE、MAPE、R²、Spearman相关系数等"
            "多维度评估指标，评估体系不够完善",

            "DataBundle类中的数据变换(fit/transform/inverse_transform)遵循scikit-learn范式，"
            "确保训练集和测试集变换的一致性，避免数据泄露",

            "缺少系统化的超参数调优(HPO)模块，当前实验需要手动修改YAML配置文件，"
            "无法进行自动化的网格搜索、贝叶斯优化或随机搜索",

            "深度学习模型(NNModel)使用固定的Adam优化器和MSE损失函数，"
            "缺少学习率调度器(LR Scheduler)、早停(Early Stopping)等训练策略",

            "交叉验证支持不完善——当前仅支持固定的训练/测试划分，"
            "缺少K-Fold、留一法(LOO)、时序交叉验证等更鲁棒的评估方法",

            "模型可解释性工具缺失，无法了解哪些特征对预测结果贡献最大，"
            "难以建立研究人员对模型预测的信任",

            "数据预处理模块处理了8种不同来源的数据格式统一化，但缺少自动化的"
            "数据质量检查(异常值检测、缺失值处理、循环数据完整性验证)",

            "基准测试结果表明，在部分数据集上简单的线性模型(如PLSR)表现优于深度学习模型，"
            "表明当前深度学习模型可能未充分优化或特征表示不够好",
        ]

        recommendations = [
            "【高优先级】引入多维度评估指标体系——除RMSE外，增加MAE、MAPE、R²、"
            "中位绝对误差(MedAE)、以及校准曲线(Calibration Curve)等指标，"
            "全面评估模型性能",

            "【高优先级】集成超参数自动调优框架(如Optuna或Ray Tune)，"
            "支持贝叶斯优化、早期停止等高效搜索策略",

            "【高优先级】增加模型可解释性工具——集成SHAP值分析、特征重要性排序、"
            "偏依赖图(PDP)等，帮助研究人员理解模型决策过程",

            "【中优先级】实现完善的交叉验证框架，支持K-Fold、Stratified K-Fold、"
            "GroupKFold(按电池分组)和时序交叉验证，提供更可靠的性能估计",

            "【中优先级】为NNModel增加学习率调度器(CosineAnnealing/OneCycleLR)、"
            "早停机制(基于验证集损失)、梯度裁剪等训练稳定性优化",

            "【中优先级】开发自动化数据质量报告模块，包括缺失值统计、异常循环检测、"
            "容量跳变识别、传感器噪声估计等功能",

            "【中优先级】探索自监督预训练方法(如Masked Autoencoder)，利用大量未标注的"
            "循环数据学习通用的电池老化表示，提升小样本场景的预测能力",

            "【低优先级】引入不确定性量化方法(如MC Dropout、Deep Ensemble、"
            "Conformal Prediction)，为预测结果提供置信区间",

            "【低优先级】考虑集成Graph Neural Network(GNN)模型，"
            "利用电池间的相似性关系构建图结构进行协同预测",
        ]

        risks = [
            "当前缺少正式的测试套件(无pytest/unittest)，代码变更可能引入"
            "静默错误而不被发现，影响研究结果的可信度",

            "部分深度学习模型(如Transformer)在小数据集上可能严重过拟合，"
            "当前缺少有效的正则化和数据增强策略",

            "固定的训练/测试划分可能导致性能估计的偏差——某些划分可能恰好"
            "将容易预测的电池分入测试集，导致过于乐观的结果",

            "numpy版本限制(>=1.24, <2.0.0)可能与其他依赖产生冲突，"
            "影响在某些环境中的部署",
        ]

        opportunities = [
            "Foundation Model for Batteries——利用大规模电池循环数据训练通用的"
            "电池基础模型，类似于NLP领域的BERT/GPT，具有重大学术价值",

            "联邦学习(Federated Learning)集成——允许多个电池制造商在不共享原始数据"
            "的前提下协作训练模型，解决数据隐私问题",

            "AutoML集成——自动选择最佳的特征提取器+模型+超参数组合，"
            "降低使用门槛，让非ML专家也能快速获得好结果",

            "实时在线学习(Online Learning)——支持模型在电池使用过程中持续学习更新，"
            "适应个体电池的独特老化模式",
        ]

        action_items = [
            {
                'task': '引入Optuna超参数自动调优',
                'assignee': 'data_scientist',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '集成Optuna框架，为每个模型定义搜索空间，'
                               '实现自动化超参数优化',
            },
            {
                'task': '开发多指标评估模块',
                'assignee': 'data_scientist',
                'priority': 'high',
                'estimated_effort': '1周',
                'description': '扩展evaluate()方法，支持RMSE/MAE/MAPE/R²/'
                               'MedAE等多维度指标计算和报告',
            },
            {
                'task': '集成SHAP可解释性分析',
                'assignee': 'data_scientist',
                'priority': 'high',
                'estimated_effort': '1-2周',
                'description': '为所有模型类型添加SHAP值计算和可视化功能',
            },
            {
                'task': '实现K-Fold交叉验证框架',
                'assignee': 'data_scientist',
                'priority': 'medium',
                'estimated_effort': '1-2周',
                'description': '开发支持多种交叉验证策略的通用框架',
            },
            {
                'task': '建立自动化数据质量检查管线',
                'assignee': 'data_scientist + software_test_engineer',
                'priority': 'medium',
                'estimated_effort': '1-2周',
                'description': '开发数据质量报告生成器，自动检测异常值、'
                               '缺失值、数据不一致等问题',
            },
        ]

        return AnalysisReport(
            agent_role=self.role.value,
            agent_name=self.name,
            summary=(
                "BatteryML的机器学习管线设计精良，模型库覆盖全面，组件化架构可扩展性强。"
                "主要改进方向包括：完善评估指标体系(不仅仅是RMSE)、引入超参数自动调优、"
                "增加模型可解释性工具、实现更鲁棒的交叉验证方案、以及建立自动化数据质量检查。"
                "深度学习模型的训练策略需要优化(学习率调度、早停等)。长期来看，"
                "电池基础模型(Foundation Model)和联邦学习是极具潜力的研究方向。"
            ),
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            opportunities=opportunities,
            action_items=action_items,
            priority="high",
            metadata={
                'models_count': {
                    'statistical': 4,
                    'tree_based': 2,
                    'dimensionality_reduction': 2,
                    'kernel_methods': 2,
                    'deep_learning': 4,
                    'baseline': 1,
                },
                'feature_extractors': [
                    'VarianceModel', 'DischargeModel',
                    'FullModel', 'VoltageCapacityMatrix',
                ],
                'current_metrics': ['RMSE'],
                'missing_metrics': [
                    'MAE', 'MAPE', 'R²', 'MedAE',
                    'Calibration', 'Uncertainty',
                ],
            },
        )

    def collaborate(self, other_reports: List[AnalysisReport]) -> List[str]:
        insights = []
        for report in other_reports:
            if report.agent_role == 'material_scientist':
                insights.append(
                    "【数据科学家→材料科学家】同意引入dQ/dV特征，建议同时开发"
                    "自动化峰检测算法，将峰位置、峰宽、峰面积作为模型输入特征"
                )
            if report.agent_role == 'product_manager':
                insights.append(
                    "【数据科学家→产品经理】模型服务化部署(Model Serving)需要考虑"
                    "推理延迟和批量预测能力，建议评估ONNX导出和TensorRT加速"
                )
            if report.agent_role == 'software_test_engineer':
                insights.append(
                    "【数据科学家→软件测试工程师】建议建立模型回归测试——每次代码变更后"
                    "自动运行基准测试并与历史结果对比，防止性能退化"
                )
        return insights
