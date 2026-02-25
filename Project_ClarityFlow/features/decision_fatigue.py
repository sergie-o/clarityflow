# features/decision_fatigue.py

from __future__ import annotations
from typing import List, Dict
from datetime import date
import pandas as pd
from core.models import Task


class DecisionFatigueMonitor:
    """
    Estimates decision fatigue per day (0–100).
    Higher = more mentally drained.
    """

    @staticmethod
    def build_daily_df(tasks: List[Task]) -> pd.DataFrame:
        """Aggregate tasks into per-day stats."""
        rows = []
        for t in tasks:
            if not t.completed:
                continue

            rows.append(
                {
                    "date": t.time_of_day.date(),
                    "hour": t.time_of_day.hour,
                    "complexity": t.complexity_score,
                    "interruptions": t.interruption_count,
                    "context_switches": t.context_switches,
                }
            )

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows)
        daily = df.groupby("date").agg(
            tasks=("date", "count"),
            avg_complexity=("complexity", "mean"),
            total_interruptions=("interruptions", "sum"),
            total_switches=("context_switches", "sum"),
            latest_hour=("hour", "max"),
        )
        daily = daily.reset_index()
        return daily

    @staticmethod
    def compute_daily_fatigue(tasks: List[Task]) -> pd.DataFrame:
        """
        Returns a DataFrame with columns:
        - date
        - fatigue_score (0–100)
        - components for debugging/visualization
        """
        daily = DecisionFatigueMonitor.build_daily_df(tasks)
        if daily.empty:
            return pd.DataFrame()

        # Normalize components into 0–100-ish scores
        # You can tweak these weights over time.
        max_tasks = max(5, daily["tasks"].max())
        max_interruptions = max(3, daily["total_interruptions"].max())
        max_switches = max(3, daily["total_switches"].max())

        daily["task_load_score"] = (daily["tasks"] / max_tasks) * 100
        daily["interrupt_score"] = (
            daily["total_interruptions"] / max_interruptions) * 100
        daily["switch_score"] = (daily["total_switches"] / max_switches) * 100
        daily["late_work_score"] = daily["latest_hour"].apply(
            lambda h: 0 if h <= 17 else min(100, (h - 17) * 20)
        )
        daily["complexity_score"] = daily["avg_complexity"] / 5 * 100

        # Weighted fatigue score
        daily["fatigue_score"] = (
            0.30 * daily["task_load_score"]
            + 0.25 * daily["interrupt_score"]
            + 0.20 * daily["switch_score"]
            + 0.15 * daily["late_work_score"]
            + 0.10 * daily["complexity_score"]
        )

        return daily[[
            "date",
            "fatigue_score",
            "task_load_score",
            "interrupt_score",
            "switch_score",
            "late_work_score",
            "complexity_score",
        ]]
