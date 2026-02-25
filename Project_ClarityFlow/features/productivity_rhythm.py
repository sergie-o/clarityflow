# features/productivity_rhythm.py

from __future__ import annotations
from typing import List, Dict
import pandas as pd
from core.models import Task


class PersonalProductivityRhythmTracker:
    """
    Learns personal productivity rhythm:
    - focus by hour of day
    - drift by hour of day
    - best time windows for deep work vs admin.
    """

    @staticmethod
    def build_history_dataframe(tasks: List[Task]) -> pd.DataFrame:
        rows = []
        for t in tasks:
            if not t.completed or t.actual_minutes is None:
                continue
            rows.append(
                {
                    "date": t.time_of_day.date(),
                    "task_type": t.task_type,
                    "estimated": t.estimated_minutes,
                    "actual": t.actual_minutes,
                    "drift": (t.actual_minutes - t.estimated_minutes)
                    / t.estimated_minutes
                    * 100,
                    "drift_ratio": t.actual_minutes / t.estimated_minutes,
                    "day_of_week": t.time_of_day.strftime("%A"),
                    "hour": t.time_of_day.hour,
                    "complexity": t.complexity_score,
                    "focus_level": t.focus_level,
                }
            )
        return pd.DataFrame(rows)

    @staticmethod
    def summarize_rhythm(tasks: List[Task]) -> Dict:
        """
        Returns:
            - hourly_focus: mean focus per hour
            - hourly_drift: mean drift per hour
            - best_hour: hour with highest focus
            - worst_hour: hour with worst drift
        """
        df = PersonalProductivityRhythmTracker.build_history_dataframe(tasks)
        if df.empty:
            return {}

        hourly = df.groupby("hour").agg(
            {"focus_level": "mean", "drift": "mean"}
        ).reset_index()

        best_focus_row = hourly.loc[hourly["focus_level"].idxmax()]
        worst_drift_row = hourly.loc[hourly["drift"].idxmax()]

        return {
            "hourly_focus": hourly[["hour", "focus_level"]],
            "hourly_drift": hourly[["hour", "drift"]],
            "best_focus_hour": int(best_focus_row["hour"]),
            "best_focus_value": float(best_focus_row["focus_level"]),
            "worst_drift_hour": int(worst_drift_row["hour"]),
            "worst_drift_value": float(worst_drift_row["drift"]),
        }
