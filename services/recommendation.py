from typing import Dict, Any, Tuple

def calculate_recommendation_score(team: Dict[str, Any], task: Dict[str, Any]) -> Tuple[int, str]:
    score = 0
    reasons = []

    # 1. Industry / Domain match (weight: 40 points)
    team_industries = [i.lower() for i in team.get("industry_interests", [])]
    task_industry = task.get("industry", "").lower()
    if any(ind in task_industry or task_industry in ind for ind in team_industries):
        score += 40
        reasons.append(f"доменное соответствие ({task.get('industry')})")
    else:
        score += 10

    # 2. Task archetype / Problem type match (weight: 40 points)
    team_task_types = [t.lower() for t in team.get("task_type_interests", [])]
    task_type = task.get("task_type", "").lower()
    if any(t_type in task_type or task_type in t_type for t_type in team_task_types):
        score += 40
        reasons.append(f"профиль компетенций ({task.get('task_type')})")
    else:
        score += 10

    # 3. Readiness level fit (weight: 20 points)
    task_rating = task.get("rating", 0)
    preferred_level = team.get("preferred_readiness", "Любая")
    task_level = task.get("readiness_level", "Черновик")

    if preferred_level == "Любая" or preferred_level == task_level:
        if task_rating >= 90:
            score += 20
            reasons.append("высокая готовность ТЗ к разработке")
        elif task_rating >= 70:
            score += 16
        elif task_rating >= 40:
            score += 12
        else:
            score += 6
    else:
        score += 8

    final_score = min(100, max(0, score))
    explanation = f"Совпадение {final_score}%: " + ", ".join(reasons) if reasons else f"Базовое соответствие {final_score}%"
    return final_score, explanation
