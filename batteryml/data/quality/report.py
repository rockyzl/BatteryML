# Licensed under the MIT License.

"""Data quality report module for battery cycling data.

This module provides the QualityReport class that encapsulates
quality check results for a single battery cell.

数据质量报告模块，用于封装单个电池单元的质量检查结果。
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class QualityReport:
    """Data quality report for a single battery cell.

    Stores results from all quality checks and provides methods to
    query issues, compute an overall quality score, and generate
    human-readable summaries.

    单个电池单元的数据质量报告。存储所有质量检查的结果，
    提供查询问题、计算总体质量分数和生成摘要的方法。

    Attributes:
        cell_id: Identifier of the battery cell.
        checks_results: Dictionary mapping check names to their results.
    """

    # Severity levels ordered by priority (higher index = more severe)
    SEVERITY_LEVELS = ('info', 'warning', 'error')

    # Weight of each check category for the overall quality score
    _SCORE_WEIGHTS = {
        'basic_stats': 0.10,
        'missing_data': 0.25,
        'anomaly_detection': 0.25,
        'consistency': 0.25,
        'noise_estimation': 0.15,
    }

    def __init__(self, cell_id: str, checks_results: Dict):
        """Initialize a QualityReport.

        Args:
            cell_id: Identifier of the battery cell.
                     电池单元标识符。
            checks_results: Dictionary mapping check category names
                to result dicts. Each result dict should contain at
                least an ``issues`` key (list of issue dicts) and
                optionally a ``score`` key (float 0-100).
                检查类别名称到结果字典的映射。
        """
        self.cell_id = cell_id
        self.checks_results = checks_results

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def score(self) -> float:
        """Overall quality score from 0 to 100.

        The score is a weighted average of individual check scores.
        If a check did not produce a score, it is assumed to be 100
        (no problems detected).

        总体质量评分（0-100）。各检查项分数的加权平均。
        """
        total_weight = 0.0
        weighted_sum = 0.0
        for category, weight in self._SCORE_WEIGHTS.items():
            result = self.checks_results.get(category)
            if result is not None:
                cat_score = result.get('score', 100.0)
                weighted_sum += cat_score * weight
                total_weight += weight
        if total_weight == 0:
            return 100.0
        return round(weighted_sum / total_weight, 2)

    def get_issues(self, severity: Optional[str] = None) -> List[Dict]:
        """Get list of issues found during quality checks.

        Args:
            severity: If provided, filter issues by severity level.
                Accepted values: ``'info'``, ``'warning'``, ``'error'``.
                If ``None``, return all issues.
                按严重程度过滤问题。

        Returns:
            A list of issue dictionaries, each containing at least
            ``category``, ``severity``, and ``message`` keys.
            问题字典列表。
        """
        if severity is not None and severity not in self.SEVERITY_LEVELS:
            raise ValueError(
                f"Invalid severity '{severity}'. "
                f"Must be one of {self.SEVERITY_LEVELS}"
            )

        issues: List[Dict] = []
        for category, result in self.checks_results.items():
            for issue in result.get('issues', []):
                if severity is None or issue.get('severity') == severity:
                    enriched = dict(issue)
                    enriched.setdefault('category', category)
                    issues.append(enriched)
        return issues

    def summary(self) -> str:
        """Generate a human-readable quality summary.

        生成可读的质量摘要。

        Returns:
            Multi-line string summarizing the quality report.
        """
        lines = [
            f"=== Data Quality Report for cell '{self.cell_id}' ===",
            f"Overall quality score: {self.score} / 100",
            "",
        ]

        # Per-category summary
        for category, result in self.checks_results.items():
            cat_score = result.get('score', 100.0)
            cat_issues = result.get('issues', [])
            n_errors = sum(
                1 for i in cat_issues if i.get('severity') == 'error')
            n_warnings = sum(
                1 for i in cat_issues if i.get('severity') == 'warning')
            n_info = sum(
                1 for i in cat_issues if i.get('severity') == 'info')
            lines.append(
                f"  [{category}] score={cat_score:.1f}  "
                f"errors={n_errors} warnings={n_warnings} info={n_info}"
            )

        # List all issues grouped by severity
        all_issues = self.get_issues()
        if all_issues:
            lines.append("")
            lines.append("Issues found:")
            for sev in reversed(self.SEVERITY_LEVELS):
                sev_issues = [
                    i for i in all_issues if i.get('severity') == sev]
                for issue in sev_issues:
                    lines.append(
                        f"  [{sev.upper()}] ({issue.get('category', '?')}) "
                        f"{issue.get('message', '')}"
                    )
        else:
            lines.append("")
            lines.append("No issues found. Data quality looks good!")

        lines.append("")
        lines.append("=== End of Report ===")
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        """Export the report as a plain dictionary.

        将报告导出为普通字典，便于序列化。

        Returns:
            Dictionary containing cell_id, score, checks_results,
            and a flat list of all issues.
        """
        return {
            'cell_id': self.cell_id,
            'score': self.score,
            'checks_results': self.checks_results,
            'issues': self.get_issues(),
        }

    def __repr__(self) -> str:
        return (
            f"QualityReport(cell_id={self.cell_id!r}, "
            f"score={self.score}, "
            f"n_issues={len(self.get_issues())})"
        )
