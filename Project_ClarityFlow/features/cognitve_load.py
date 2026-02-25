# features/cognitive_load.py

from __future__ import annotations
from typing import List, Dict
from core.models import Task


class CognitiveLoadDetector:
    """Calculates and predicts cognitive load for a given schedule (list of tasks)."""

    @staticmethod
    def calculate_load(schedule: List[Task]) -> Dict:
        if not schedule:
            return {"score": 0, "components": {}, "level": "low"}

        total_time = sum(t.estimated_minutes for t in schedule) or 1
        available_hours = 8

        # Task density score (how packed the day is)
        task_density = len(schedule) / available_hours
        task_density_score = min(100, task_density * 20)

        # Complexity score (complexity weighted by time)
        weighted_complexity = sum(
            t.complexity_score * t.estimated_minutes for t in schedule
        )
        complexity_score = (weighted_complexity / total_time) * 20

        # Context switching score (number of type changes)
        switches = sum(
            1
            for i in range(len(schedule) - 1)
            if schedule[i].task_type != schedule[i + 1].task_type
        )
        context_switch_score = min(100, switches * 12)

        cognitive_load = (
            0.40 * task_density_score
            + 0.35 * complexity_score
            + 0.25 * context_switch_score
        )

        level = "high" if cognitive_load > 75 else "medium" if cognitive_load > 50 else "low"

        return {
            "score": round(cognitive_load, 1),
            "components": {
                "task_density": round(task_density_score, 1),
                "complexity": round(complexity_score, 1),
                "context_switching": round(context_switch_score, 1),
            },
            "level": level,
        }
