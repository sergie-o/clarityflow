# features/emotion_planner.py

# features/emotion_planner.py

from __future__ import annotations
from typing import List, Dict, Optional
from core.models import Task
import os

try:
    # Optional OpenAI import – only used if API key is available
    from openai import OpenAI
    _OPENAI_CLIENT: Optional[OpenAI] = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    _OPENAI_CLIENT = None


class EmotionAwarePlanner:
    """
    Suggests which tasks to prioritize based on current mood/energy.
    mood: 1 (very low) to 5 (very high)

    Also integrates with an OpenAI LLM (if OPENAI_API_KEY is set) to:
    - Interpret free-text mood descriptions into a mood score (1–5)
    - Generate short coaching suggestions.
    """

    # ============ CORE NUMERIC LOGIC ============

    @staticmethod
    def score_task_for_mood(task: Task, mood: int) -> float:
        """
        Higher score = better fit for current mood.
        Simplified rule set:
          - High mood: favor deep_work / coding, higher complexity
          - Low mood: favor admin / communication, lower complexity
        """
        base = 0.0

        # Task type preferences
        high_focus_types = {"deep_work", "coding"}
        low_focus_types = {"admin", "communication"}

        if mood >= 4:
            if task.task_type in high_focus_types:
                base += 2.0
        elif mood <= 2:
            if task.task_type in low_focus_types:
                base += 2.0

        # Complexity alignment
        if mood >= 4:
            # reward higher complexity
            base += (task.complexity_score - 3) * 0.5
        elif mood <= 2:
            # reward lower complexity
            base += (3 - task.complexity_score) * 0.5

        # Neutral mood: slight preference for mid-complexity
        if mood == 3:
            base -= abs(task.complexity_score - 3) * 0.2

        return base

    @staticmethod
    def suggest_for_mood(tasks: List[Task], mood: int) -> Dict[str, List[Task]]:
        """
        Returns:
            - 'recommended_now': tasks that fit current mood
            - 'better_for_later': tasks that fit less well
        """
        if not tasks:
            return {"recommended_now": [], "better_for_later": []}

        scored: List[tuple[Task, float]] = []
        for t in tasks:
            if t.completed:
                continue
            score = EmotionAwarePlanner.score_task_for_mood(t, mood)
            scored.append((t, score))

        if not scored:
            return {"recommended_now": [], "better_for_later": []}

        scored.sort(key=lambda x: x[1], reverse=True)

        recommended = [t for t, s in scored if s >= 0]
        later = [t for t, s in scored if s < 0]

        return {
            "recommended_now": recommended,
            "better_for_later": later,
        }

    # ============ LLM-ASSISTED PARTS ============

    @staticmethod
    def interpret_mood_text(mood_text: str) -> Dict:
        """
        Use an OpenAI LLM to interpret free-text mood description into:
            - mood_score: int 1–5
            - energy: "low" | "medium" | "high"
            - explanation: short text summary

        If no OpenAI client is available (no API key / import error),
        it falls back to a simple heuristic and explanation.
        """
        mood_text = (mood_text or "").strip()
        if not mood_text:
            # No text → neutral
            return {
                "mood_score": 3,
                "energy": "medium",
                "explanation": "No mood text provided, defaulting to neutral energy.",
            }

        # Fallback if LLM isn't configured
        if _OPENAI_CLIENT is None:
            # Very simple keyword-based heuristic so the app still works
            text_lower = mood_text.lower()
            if any(w in text_lower for w in ["tired", "exhausted", "stressed", "drained", "burnt"]):
                mood_score = 2
                energy = "low"
            elif any(w in text_lower for w in ["excited", "motivated", "pumped", "focused"]):
                mood_score = 4
                energy = "high"
            else:
                mood_score = 3
                energy = "medium"

            return {
                "mood_score": mood_score,
                "energy": energy,
                "explanation": "Heuristic interpretation (LLM not configured).",
            }

        # Use OpenAI LLM if we have a client
        prompt = f"""
You are helping a manager describe their current state.

User's description:
\"\"\"{mood_text}\"\"\"

1. Infer a mood score from 1 (very low energy / overwhelmed) to 5 (very high energy / very focused).
2. Classify energy as one of: "low", "medium", "high".
3. Give a short 1–2 sentence explanation of how they are likely feeling.

Respond ONLY as compact JSON like:
{{
  "mood_score": 3,
  "energy": "medium",
  "explanation": "..."
}}
"""

        try:
            response = _OPENAI_CLIENT.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
            )
            # Depending on SDK, adjust parsing – here we assume text output:
            raw_text = response.output[0].content[0].text  # may differ in your SDK
            import json
            parsed = json.loads(raw_text)

            mood_score = int(parsed.get("mood_score", 3))
            mood_score = max(1, min(5, mood_score))  # clamp
            energy = str(parsed.get("energy", "medium"))
            explanation = str(parsed.get("explanation", "")).strip()

            if not explanation:
                explanation = "LLM mood interpretation."

            return {
                "mood_score": mood_score,
                "energy": energy,
                "explanation": explanation,
            }
        except Exception as e:
            # On any error, log minimal info and fall back gracefully
            print(f"[EmotionAwarePlanner] LLM mood interpretation failed: {e}")
            return {
                "mood_score": 3,
                "energy": "medium",
                "explanation": "LLM interpretation failed, defaulting to neutral.",
            }

    @staticmethod
    def generate_mood_coaching(
        mood_score: int,
        energy: str,
        num_tasks: int,
        top_task_types: List[str] | None = None,
    ) -> str:
        """
        Optional: ask the LLM to generate a short, friendly coaching message
        about how to approach the next block of work.

        If LLM is unavailable, returns a simple rule-based suggestion.
        """
        top_task_types = top_task_types or []

        # Simple fallback if no LLM
        if _OPENAI_CLIENT is None:
            if mood_score <= 2:
                return (
                    "Your energy seems low. Focus on simple, low-stakes tasks "
                    "like admin or light communication. Avoid heavy deep work blocks."
                )
            elif mood_score >= 4:
                return (
                    "You have good energy right now. This is a great time for deep, "
                    "high-impact tasks that require focus."
                )
            else:
                return (
                    "Your energy is moderate. Mix medium-complexity tasks with a few "
                    "lighter ones, and avoid overloading your schedule."
                )

        # Use LLM to craft a short suggestion
        prompt = f"""
You are coaching an operations manager about what to work on next.

Mood score (1–5): {mood_score}
Energy label: {energy}
Number of pending tasks: {num_tasks}
Top recommended task types: {top_task_types}

Write 2–3 short bullet points:
- What kind of work they should focus on in the next 1–2 hours
- What to avoid for now
- One small self-care or pacing suggestion

Keep it under 80 words.
"""

        try:
            response = _OPENAI_CLIENT.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
            )
            text = response.output[0].content[0].text  # adjust depending on SDK
            return text.strip()
        except Exception as e:
            print(f"[EmotionAwarePlanner] LLM coaching generation failed: {e}")
            # Fallback
            if mood_score >= 4:
                return (
                    "Use this high energy window for your most important deep work. "
                    "Reduce distractions and protect a solid focus block."
                )
            elif mood_score <= 2:
                return (
                    "Take it easy: handle light tasks and admin, and consider a short break "
                    "before attempting harder work."
                )
            else:
                return (
                    "Balance your workload: mix medium-effort tasks with lighter ones, "
                    "and avoid overcommitting your schedule."
                )