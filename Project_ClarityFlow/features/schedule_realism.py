# features/schedule_realism.py

from __future__ import annotations
from typing import List, Dict
from core.models import Task
from features.execution_drift import ExecutionDriftAnalyzer


class ScheduleRealismScorer:
    """Evaluates how realistic a day's schedule is."""

    @staticmethod
    def calculate_score(
        schedule: List[Task], drift_analyzer: ExecutionDriftAnalyzer
    ) -> Dict:
        if not schedule:
            return {"score": 100.0, "components": {}, "level": "high"}

        available_time = 8 * 60  # 8 hours in minutes
        total_estimated = sum(t.estimated_minutes for t in schedule)

        # 1. Time budget score (how close to capacity your plan is)
        utilization = total_estimated / available_time
        if utilization <= 0.75:
            time_budget_score = 100
        elif utilization <= 0.9:
            time_budget_score = 80
        elif utilization <= 1.0:
            time_budget_score = 50
        else:
            time_budget_score = max(0, 30 - (utilization - 1.0) * 50)

        # 2. Historical accuracy score (uses ML prediction if model available)
        if drift_analyzer and drift_analyzer.model is not None:
            predicted_total = sum(
                drift_analyzer.predict(t)["ai_prediction"] for t in schedule
            )
            actual_utilization = predicted_total / available_time
            historical_score = max(0, 100 - (actual_utilization - 0.9) * 200)
        else:
            historical_score = 70  # neutral default when no model

        # 3. Buffer score (slack time left)
        buffer = available_time - total_estimated
        buffer_pct = buffer / available_time
        if buffer_pct >= 0.25:
            buffer_score = 100
        elif buffer_pct >= 0.15:
            buffer_score = 80
        elif buffer_pct >= 0.05:
            buffer_score = 50
        else:
            buffer_score = 20

        overall_score = (
            0.40 * time_budget_score + 0.35 * historical_score + 0.25 * buffer_score
        )

        level = "high" if overall_score > 75 else "medium" if overall_score > 50 else "low"

        return {
            "score": round(overall_score, 1),
            "components": {
                "time_budget": round(time_budget_score, 1),
                "historical_fit": round(historical_score, 1),
                "buffer": round(buffer_score, 1),
            },
            "level": level,
        }
