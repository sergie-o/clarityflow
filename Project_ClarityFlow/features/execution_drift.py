# features/execution_drift.py

from __future__ import annotations
from typing import List, Dict
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_absolute_error
from core.models import Task


TASK_TYPES = ["coding", "meeting", "admin", "deep_work", "communication"]


class ExecutionDriftAnalyzer:
    """Analyzes and predicts task execution drift"""

    def __init__(self) -> None:
        self.model: xgb.XGBRegressor | None = None
        self.feature_columns = [
            "estimated_minutes",
            "task_type_encoded",
            "complexity_score",
            "hour_of_day",
            "day_of_week",
            "is_morning",
            "is_afternoon",
            "interruption_count",
            "context_switches",
        ]

    def engineer_features(self, tasks: List[Task]) -> pd.DataFrame:
        """Transform completed tasks into ML features."""
        rows = []

        for task in tasks:
            if not task.completed or task.actual_minutes is None:
                continue

            hour = task.time_of_day.hour
            try:
                task_type_encoded = TASK_TYPES.index(task.task_type)
            except ValueError:
                # Unknown type: bucket as last index
                task_type_encoded = len(TASK_TYPES)

            rows.append(
                {
                    "estimated_minutes": task.estimated_minutes,
                    "actual_minutes": task.actual_minutes,
                    "task_type": task.task_type,
                    "task_type_encoded": task_type_encoded,
                    "complexity_score": task.complexity_score,
                    "hour_of_day": hour,
                    "day_of_week": task.day_of_week,
                    "is_morning": 1 if hour < 12 else 0,
                    "is_afternoon": 1 if 12 <= hour < 17 else 0,
                    "interruption_count": task.interruption_count,
                    "context_switches": task.context_switches,
                    "drift_ratio": task.actual_minutes / task.estimated_minutes,
                }
            )

        return pd.DataFrame(rows)

    def train(self, tasks: List[Task]) -> Dict:
        """Train the drift prediction model on completed tasks."""
        df = self.engineer_features(tasks)

        if len(df) < 20:
            return {"status": "insufficient_data", "tasks_needed": 20 - len(df)}

        X = df[self.feature_columns]
        y = df["drift_ratio"]

        split = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]

        self.model = xgb.XGBRegressor(
            max_depth=3, n_estimators=50, learning_rate=0.1, random_state=42
        )
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        return {"status": "success", "mae": mae, "samples": len(df)}

    def predict(self, task: Task) -> Dict:
        """Predict actual duration for a task, returning both user + AI estimate."""
        if self.model is None:
            # Fall back to a simple heuristic
            return {
                "user_estimate": task.estimated_minutes,
                "ai_prediction": round(task.estimated_minutes * 1.2, 1),
                "method": "heuristic",
            }

        hour = task.time_of_day.hour
        try:
            task_type_encoded = TASK_TYPES.index(task.task_type)
        except ValueError:
            task_type_encoded = len(TASK_TYPES)

        features = pd.DataFrame(
            [
                {
                    "estimated_minutes": task.estimated_minutes,
                    "task_type_encoded": task_type_encoded,
                    "complexity_score": task.complexity_score,
                    "hour_of_day": hour,
                    "day_of_week": task.day_of_week,
                    "is_morning": 1 if hour < 12 else 0,
                    "is_afternoon": 1 if 12 <= hour < 17 else 0,
                    "interruption_count": task.interruption_count,
                    "context_switches": task.context_switches,
                }
            ]
        )[self.feature_columns]

        drift_ratio = float(self.model.predict(features)[0])
        corrected_duration = task.estimated_minutes * drift_ratio

        return {
            "user_estimate": task.estimated_minutes,
            "ai_prediction": round(corrected_duration, 1),
            "drift_ratio": drift_ratio,
            "method": "ml_model",
        }
