from typing import Dict, Any, Tuple, List
from config import SCORING_WEIGHTS, READINESS_LEVELS

def calculate_field_score(field_name: str, value: str) -> int:
    val = (value or "").strip()
    if not val:
        return 0

    cfg = SCORING_WEIGHTS.get(field_name)
    if not cfg:
        return 0
    max_pts = cfg["max_points"]

    length = len(val)
    if max_pts == 20:
        if length >= 40:
            return 20
        elif length >= 15:
            return 10
        return 5
    elif max_pts == 15:
        if length >= 35:
            return 15
        elif length >= 15:
            return 8
        return 4
    elif max_pts == 10:
        if length >= 25:
            return 10
        elif length >= 10:
            return 5
        return 3
    return 0

def calculate_task_score(task_data: Dict[str, Any]) -> Tuple[int, Dict[str, int], List[str]]:
    breakdown: Dict[str, int] = {}
    missing_fields: List[str] = []
    total_score = 0

    for field_name, cfg in SCORING_WEIGHTS.items():
        val = task_data.get(field_name, "")
        pts = calculate_field_score(field_name, val)
        breakdown[field_name] = pts
        total_score += pts
        if pts < cfg["max_points"]:
            missing_fields.append(field_name)

    total_score = min(100, max(0, total_score))
    return total_score, breakdown, missing_fields

def get_readiness_level(score: int) -> Dict[str, str]:
    for level_info in READINESS_LEVELS:
        if level_info["min_score"] <= score <= level_info["max_score"]:
            return {
                "level": level_info["level"],
                "description": level_info["description"],
                "badge_class": level_info["badge_class"]
            }
    return {
        "level": "Черновик",
        "description": "Требует уточнения",
        "badge_class": "badge-draft"
    }

def get_improvement_suggestions(breakdown: Dict[str, int]) -> List[Dict[str, Any]]:
    suggestions = []
    for field_name, cfg in SCORING_WEIGHTS.items():
        current_pts = breakdown.get(field_name, 0)
        max_pts = cfg["max_points"]
        diff = max_pts - current_pts
        if diff > 0:
            suggestions.append({
                "field": field_name,
                "title": cfg["title"],
                "potential_points": diff,
                "hint": f"Заполните подробнее раздел '{cfg['title']}' (+{diff} баллов). {cfg['description']}."
            })
    suggestions.sort(key=lambda s: s["potential_points"], reverse=True)
    return suggestions
