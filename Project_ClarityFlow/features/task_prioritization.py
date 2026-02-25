# features/task_prioritization.py

from __future__ import annotations
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from core.models import Task
import os

try:
    from openai import OpenAI
    _OPENAI_CLIENT: Optional[OpenAI] = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    _OPENAI_CLIENT = None


class TaskPrioritizer:
    """
    AI-Powered Task Prioritization Engine

    Uses multiple factors + OpenAI to help managers prioritize their daily tasks:
    - Urgency (deadline proximity)
    - Impact (complexity, estimated time)
    - Dependencies (what blocks other tasks)
    - Cognitive load (current mental capacity)
    - Energy alignment (task difficulty vs current energy)
    - Strategic importance (AI-assisted)
    """

    # Priority weights (can be customized per manager)
    DEFAULT_WEIGHTS = {
        'urgency': 0.30,           # How soon it's due
        'impact': 0.25,            # How important/complex
        'effort': 0.15,            # Time required
        'energy_alignment': 0.15,  # Matches current energy
        'strategic_value': 0.15,   # Long-term importance
    }

    @staticmethod
    def calculate_urgency_score(task: Task, current_time: datetime = None) -> float:
        """
        Calculate urgency based on scheduled time

        Returns:
            0-100 score (100 = extremely urgent, 0 = far away)
        """
        if current_time is None:
            current_time = datetime.now()

        time_until = (task.time_of_day -
                      current_time).total_seconds() / 3600  # hours

        # Scoring curve
        if time_until < 0:
            return 100  # Overdue - maximum urgency
        elif time_until < 0.5:
            return 95   # Less than 30 min
        elif time_until < 1:
            return 85   # Less than 1 hour
        elif time_until < 2:
            return 70   # Less than 2 hours
        elif time_until < 4:
            return 50   # Less than 4 hours
        elif time_until < 8:
            return 30   # Same day but later
        else:
            return max(0, 20 - (time_until - 8) * 2)  # Future days

    @staticmethod
    def calculate_impact_score(task: Task) -> float:
        """
        Calculate impact based on complexity and estimated time

        Higher complexity + longer time = higher impact

        Returns:
            0-100 score
        """
        # Normalize complexity (1-5 → 0-100)
        complexity_score = (task.complexity_score / 5.0) * 60

        # Normalize time (longer tasks = higher impact, cap at 120min)
        time_score = min(task.estimated_minutes / 120, 1.0) * 40

        return complexity_score + time_score

    @staticmethod
    def calculate_effort_score(task: Task) -> float:
        """
        Calculate effort score (inverse - lower effort = higher score)

        This helps prioritize quick wins when needed

        Returns:
            0-100 score (100 = low effort, 0 = high effort)
        """
        # Inverse scoring - shorter tasks score higher
        # Tasks under 15 min get highest score
        if task.estimated_minutes <= 15:
            return 100
        elif task.estimated_minutes <= 30:
            return 80
        elif task.estimated_minutes <= 60:
            return 60
        elif task.estimated_minutes <= 90:
            return 40
        else:
            return max(0, 40 - (task.estimated_minutes - 90) / 10)

    @staticmethod
    def calculate_energy_alignment_score(
        task: Task,
        current_energy: int = 3,
        current_hour: int = None
    ) -> float:
        """
        Calculate how well task matches current energy level

        Args:
            task: The task to evaluate
            current_energy: 1-5 scale (1=drained, 5=energized)
            current_hour: Hour of day (for time-based energy patterns)

        Returns:
            0-100 score (100 = perfect match)
        """
        if current_hour is None:
            current_hour = datetime.now().hour

        # Determine if it's a high-focus time (morning typically)
        is_peak_time = 8 <= current_hour <= 11
        is_low_time = current_hour >= 16

        # High energy + high complexity = good match
        # Low energy + low complexity = good match
        complexity = task.complexity_score

        if current_energy >= 4:
            # High energy - prefer complex tasks
            if complexity >= 4:
                base_score = 100
            elif complexity >= 3:
                base_score = 80
            else:
                base_score = 60  # Can do simple tasks but not optimal use
        elif current_energy >= 3:
            # Medium energy - prefer medium complexity
            if 2.5 <= complexity <= 3.5:
                base_score = 100
            elif complexity >= 4:
                base_score = 70
            else:
                base_score = 80
        else:
            # Low energy - prefer simple tasks
            if complexity <= 2:
                base_score = 100
            elif complexity <= 3:
                base_score = 70
            else:
                base_score = 40  # Poor match

        # Boost for time alignment
        if is_peak_time and complexity >= 3:
            base_score = min(100, base_score + 10)
        elif is_low_time and complexity <= 2:
            base_score = min(100, base_score + 10)

        # Task type considerations
        high_focus_types = {'deep_work', 'coding'}
        low_focus_types = {'admin', 'communication'}

        if current_energy >= 4 and task.task_type in high_focus_types:
            base_score = min(100, base_score + 10)
        elif current_energy <= 2 and task.task_type in low_focus_types:
            base_score = min(100, base_score + 10)

        return base_score

    @staticmethod
    def prioritize_tasks(
        tasks: List[Task],
        current_energy: int = 3,
        weights: Dict[str, float] = None,
        current_time: datetime = None
    ) -> List[Dict]:
        """
        Prioritize a list of tasks using multiple factors

        Args:
            tasks: List of incomplete tasks
            current_energy: Current energy level (1-5)
            weights: Custom priority weights (optional)
            current_time: Current datetime (defaults to now)

        Returns:
            List of tasks with priority scores, sorted by priority (highest first)
        """
        if weights is None:
            weights = TaskPrioritizer.DEFAULT_WEIGHTS

        if current_time is None:
            current_time = datetime.now()

        current_hour = current_time.hour

        # Calculate scores for each task
        scored_tasks = []

        for task in tasks:
            if task.completed:
                continue

            urgency = TaskPrioritizer.calculate_urgency_score(
                task, current_time)
            impact = TaskPrioritizer.calculate_impact_score(task)
            effort = TaskPrioritizer.calculate_effort_score(task)
            energy_alignment = TaskPrioritizer.calculate_energy_alignment_score(
                task, current_energy, current_hour
            )

            # Calculate weighted priority score
            priority_score = (
                weights['urgency'] * urgency +
                weights['impact'] * impact +
                weights['effort'] * effort +
                weights['energy_alignment'] * energy_alignment
            )

            # Note: strategic_value will be added by AI if available

            scored_tasks.append({
                'task': task,
                'priority_score': priority_score,
                'urgency_score': urgency,
                'impact_score': impact,
                'effort_score': effort,
                'energy_alignment_score': energy_alignment,
                'strategic_value_score': 50,  # Default neutral score
            })

        # Sort by priority (highest first)
        scored_tasks.sort(key=lambda x: x['priority_score'], reverse=True)

        return scored_tasks

    @staticmethod
    def get_prioritization_insights(prioritized_tasks: List[Dict]) -> Dict:
        """
        Generate insights from prioritized task list

        Returns:
            Dictionary with recommendations and insights
        """
        if not prioritized_tasks:
            return {
                'top_3_now': [],
                'quick_wins': [],
                'defer_later': [],
                'insights': []
            }

        # Top 3 priorities
        top_3 = prioritized_tasks[:3]

        # Quick wins (high priority + low effort)
        quick_wins = [
            t for t in prioritized_tasks
            if t['effort_score'] >= 80 and t['priority_score'] >= 60
        ][:3]

        # Can defer (low urgency + lower priority)
        defer_later = [
            t for t in prioritized_tasks
            if t['urgency_score'] < 30 and t['priority_score'] < 50
        ][-3:]

        # Generate insights
        insights = []

        # Check for urgency clustering
        urgent_count = sum(
            1 for t in prioritized_tasks if t['urgency_score'] > 80)
        if urgent_count > 3:
            insights.append({
                'type': 'warning',
                'message': f'⚠️ {urgent_count} urgent tasks detected - consider blocking distractions',
                'action': 'Focus mode recommended'
            })

        # Check for energy mismatch
        low_alignment_count = sum(
            1 for t in prioritized_tasks[:5]
            if t['energy_alignment_score'] < 50
        )
        if low_alignment_count >= 3:
            insights.append({
                'type': 'info',
                'message': '💡 Top tasks may not match your current energy - adjust schedule?',
                'action': 'Consider reordering based on energy'
            })

        # Check for quick wins opportunity
        if len(quick_wins) >= 2:
            insights.append({
                'type': 'success',
                'message': f'✨ {len(quick_wins)} quick wins available - great for momentum!',
                'action': 'Knock out quick wins first'
            })

        # Check for high-impact concentration
        high_impact_count = sum(1 for t in top_3 if t['impact_score'] > 70)
        if high_impact_count >= 2:
            insights.append({
                'type': 'info',
                'message': '🎯 Multiple high-impact tasks ahead - pace yourself',
                'action': 'Schedule breaks between major tasks'
            })

        return {
            'top_3_now': [t['task'] for t in top_3],
            'quick_wins': [t['task'] for t in quick_wins],
            'defer_later': [t['task'] for t in defer_later],
            'insights': insights,
            'total_tasks': len(prioritized_tasks),
            'avg_priority_score': sum(t['priority_score'] for t in prioritized_tasks) / len(prioritized_tasks)
        }

    # ============ AI-ENHANCED PRIORITIZATION ============

    @staticmethod
    def ai_enhance_prioritization(
        prioritized_tasks: List[Dict],
        context: str = "",
        manager_goals: str = "",
    ) -> List[Dict]:
        """
        Use OpenAI to add strategic value scoring to prioritized tasks

        This helps identify tasks that are strategically important even if
        they're not urgent (e.g., long-term planning, team development)

        Args:
            prioritized_tasks: Already scored tasks from prioritize_tasks()
            context: Additional context about current situation
            manager_goals: Manager's current goals/priorities

        Returns:
            Same task list with updated strategic_value_score and priority_score
        """
        if _OPENAI_CLIENT is None:
            # No OpenAI - return as-is
            return prioritized_tasks

        if not prioritized_tasks:
            return []

        # Prepare task descriptions for AI
        task_descriptions = []
        for i, t in enumerate(prioritized_tasks):
            task = t['task']
            task_descriptions.append({
                'index': i,
                'type': task.task_type,
                'estimated_minutes': task.estimated_minutes,
                'complexity': task.complexity_score,
                'scheduled': task.time_of_day.strftime('%I:%M %p'),
                'current_priority_score': round(t['priority_score'], 1)
            })

        # Create prompt for OpenAI
        prompt = f"""You are helping a manager prioritize their tasks for today.

Current Context:
{context if context else "Regular work day"}

Manager's Current Goals:
{manager_goals if manager_goals else "General productivity and task completion"}

Tasks to prioritize:
{task_descriptions}

For each task, assign a strategic_value_score (0-100) based on:
- Alignment with stated goals
- Long-term impact vs short-term urgency
- Whether it unlocks other work
- Strategic importance for career/team/company

Important: Don't just favor urgent tasks. Sometimes non-urgent strategic work 
(like planning, team development, process improvement) is more valuable long-term.

Respond ONLY with a JSON array like:
[
  {{"index": 0, "strategic_value_score": 75, "reasoning": "Aligns with goal X"}},
  {{"index": 1, "strategic_value_score": 60, "reasoning": "Important but not urgent"}},
  ...
]
"""

        try:
            response = _OPENAI_CLIENT.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert executive coach helping managers prioritize effectively. You understand the difference between urgent and important."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )

            # Parse response
            import json
            ai_scores = json.loads(response.choices[0].message.content)

            # Update tasks with strategic scores
            weights = TaskPrioritizer.DEFAULT_WEIGHTS

            for score_data in ai_scores:
                idx = score_data['index']
                strategic_score = score_data['strategic_value_score']
                reasoning = score_data.get('reasoning', '')

                if 0 <= idx < len(prioritized_tasks):
                    # Update strategic value
                    prioritized_tasks[idx]['strategic_value_score'] = strategic_score
                    prioritized_tasks[idx]['ai_reasoning'] = reasoning

                    # Recalculate priority score with strategic value
                    t = prioritized_tasks[idx]
                    new_priority = (
                        weights['urgency'] * t['urgency_score'] +
                        weights['impact'] * t['impact_score'] +
                        weights['effort'] * t['effort_score'] +
                        weights['energy_alignment'] * t['energy_alignment_score'] +
                        weights['strategic_value'] * strategic_score
                    )

                    prioritized_tasks[idx]['priority_score'] = new_priority

            # Re-sort with new scores
            prioritized_tasks.sort(
                key=lambda x: x['priority_score'], reverse=True)

        except Exception as e:
            print(f"[TaskPrioritizer] AI enhancement failed: {e}")
            # Return original prioritization if AI fails

        return prioritized_tasks

    @staticmethod
    def get_ai_prioritization_explanation(
        prioritized_tasks: List[Dict],
        top_n: int = 5
    ) -> str:
        """
        Generate a natural language explanation of prioritization using AI

        Args:
            prioritized_tasks: Prioritized task list (with scores)
            top_n: Number of top tasks to explain

        Returns:
            Human-readable explanation of why tasks are ordered this way
        """
        if _OPENAI_CLIENT is None:
            return "AI explanation unavailable (no OpenAI API key configured)"

        if not prioritized_tasks:
            return "No tasks to prioritize"

        # Take top N tasks
        top_tasks = prioritized_tasks[:top_n]

        # Format task info
        task_info = []
        for i, t in enumerate(top_tasks, 1):
            task = t['task']
            task_info.append({
                'rank': i,
                'type': task.task_type,
                'estimated_time': task.estimated_minutes,
                'complexity': task.complexity_score,
                'urgency_score': round(t['urgency_score'], 1),
                'impact_score': round(t['impact_score'], 1),
                'energy_alignment': round(t['energy_alignment_score'], 1),
                'strategic_value': round(t['strategic_value_score'], 1),
                'final_priority': round(t['priority_score'], 1),
                'ai_reasoning': t.get('ai_reasoning', 'N/A')
            })

        prompt = f"""Explain to a busy manager why these tasks are prioritized in this order.

Top {top_n} tasks:
{task_info}

Write 2-3 sentences explaining:
1. Why the #1 task should be done first
2. The overall logic of this prioritization
3. One actionable tip for executing this list

Keep it concise, practical, and motivating. Use a friendly, coaching tone.
"""

        try:
            response = _OPENAI_CLIENT.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an executive coach. Give brief, actionable advice."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"[TaskPrioritizer] AI explanation failed: {e}")
            return f"Prioritized by urgency ({top_tasks[0]['urgency_score']:.0f}%), impact, and energy alignment."

    @staticmethod
    def suggest_schedule_reordering(
        prioritized_tasks: List[Dict],
        available_hours: float = 8.0
    ) -> Dict:
        """
        Suggest optimal time slots for prioritized tasks

        Args:
            prioritized_tasks: Already prioritized tasks
            available_hours: Hours available today

        Returns:
            Suggested schedule with time blocks
        """
        if not prioritized_tasks:
            return {'schedule': [], 'overflow': []}

        current_time = datetime.now()
        schedule = []
        total_minutes = 0
        available_minutes = available_hours * 60

        for t_data in prioritized_tasks:
            task = t_data['task']

            if total_minutes + task.estimated_minutes <= available_minutes:
                # Fits in schedule
                start_time = current_time + timedelta(minutes=total_minutes)
                end_time = start_time + \
                    timedelta(minutes=task.estimated_minutes)

                schedule.append({
                    'task': task,
                    'suggested_start': start_time,
                    'suggested_end': end_time,
                    'priority_score': t_data['priority_score'],
                    'reason': TaskPrioritizer._get_scheduling_reason(t_data)
                })

                total_minutes += task.estimated_minutes
            else:
                # Overflow - doesn't fit today
                schedule.append({
                    'task': task,
                    'suggested_start': None,
                    'suggested_end': None,
                    'priority_score': t_data['priority_score'],
                    'reason': 'Overflow - consider tomorrow or delegate'
                })

        fits_count = sum(
            1 for s in schedule if s['suggested_start'] is not None)
        overflow_count = len(schedule) - fits_count

        return {
            'schedule': schedule,
            'fits_count': fits_count,
            'overflow_count': overflow_count,
            'total_time_needed': sum(t['task'].estimated_minutes for t in prioritized_tasks),
            'available_time': available_minutes,
            'utilization': min(100, (total_minutes / available_minutes) * 100)
        }

    @staticmethod
    def _get_scheduling_reason(task_data: Dict) -> str:
        """Generate reasoning for why task is scheduled at this time"""
        scores = {
            'urgency': task_data['urgency_score'],
            'impact': task_data['impact_score'],
            'energy': task_data['energy_alignment_score'],
            'strategic': task_data['strategic_value_score']
        }

        # Find highest scoring factor
        max_factor = max(scores.items(), key=lambda x: x[1])

        reasons = {
            'urgency': 'Time-sensitive',
            'impact': 'High-impact work',
            'energy': 'Matches your current energy',
            'strategic': 'Strategically important'
        }

        return reasons[max_factor[0]]
