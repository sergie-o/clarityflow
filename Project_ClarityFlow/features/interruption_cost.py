# features/interruption_cost.py

from __future__ import annotations
from typing import List, Dict
import pandas as pd
from core.models import Task


class InterruptionCostEstimator:
    """
    Estimates the time cost of interruptions based on
    (actual - estimated) vs interruption_count.
    """

    @staticmethod
    def build_df(tasks: List[Task]) -> pd.DataFrame:
        rows = []
        for t in tasks:
            if not t.completed or t.actual_minutes is None:
                continue
            if t.estimated_minutes <= 0:
                continue

            extra = t.actual_minutes - t.estimated_minutes
            rows.append(
                {
                    "task_id": t.task_id,
                    "task_type": t.task_type,
                    "estimated": t.estimated_minutes,
                    "actual": t.actual_minutes,
                    "extra_time": extra,
                    "interruptions": t.interruption_count,
                }
            )

        if not rows:
            return pd.DataFrame()

        return pd.DataFrame(rows)

    @staticmethod
    def estimate_cost(tasks: List[Task]) -> Dict:
        """
        Returns:
            - overall_avg_cost_per_interrupt (minutes)
            - by_task_type: dict of avg cost per interrupt by type
        """
        df = InterruptionCostEstimator.build_df(tasks)
        if df.empty:
            return {}

        # Only consider tasks where there was at least 1 interruption
        df_int = df[df["interruptions"] > 0].copy()
        if df_int.empty:
            return {}

        # Cost per interrupt = extra_time / interruptions
        df_int["cost_per_interrupt"] = df_int["extra_time"] / \
            df_int["interruptions"]

        overall = df_int["cost_per_interrupt"].mean()

        by_type = (
            df_int.groupby("task_type")["cost_per_interrupt"]
            .mean()
            .to_dict()
        )

        return {
            "overall_avg_cost_per_interrupt": float(overall),
            "by_task_type": {k: float(v) for k, v in by_type.items()},
        }
