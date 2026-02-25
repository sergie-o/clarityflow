# core/models.py

from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict


@dataclass
class Task:
    task_id: str
    task_type: str
    estimated_minutes: float
    complexity_score: float
    time_of_day: datetime
    actual_minutes: Optional[float] = None
    interruption_count: int = 0
    context_switches: int = 0
    focus_level: int = 3
    completed: bool = False

    @property
    def day_of_week(self) -> int:
        return self.time_of_day.weekday()

    def to_dict(self) -> Dict:
        data = asdict(self)
        # Serialize datetime to ISO string
        data["time_of_day"] = self.time_of_day.isoformat()
        return data
