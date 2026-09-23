import pytest
from services.scoring import calculate_task_score, get_readiness_level, get_improvement_suggestions
from services.recommendation import calculate_recommendation_score
from services.seed_data import (
    get_initial_drafts,
    get_initial_tasks,
    get_initial_teams,
    get_initial_proposals,
    get_initial_milestones
)

def test_empty_task_score():
    empty_task = {}
    score, breakdown, missing = calculate_task_score(empty_task)
    assert score == 0
    assert len(missing) == 7
    level_info = get_readiness_level(score)
    assert level_info["level"] == "Черновик"

def test_full_task_score():
    full_task = {
        "context_need": "Детальное описание бизнес-контекста и реальной потребности ритейлера с метриками.",
        "data_materials": "Обезличенные выгрузки диалогов в JSONL и каталог товаров с категориями в CSV.",
        "expected_result": "Готовый микросервис чат-бота с интеграцией в Telegram и веб-виджет.",
        "success_criteria": "Разрешение не менее 65% типовых обращений без участия человека; SLA до 2 сек.",
        "constraints": "Срок разработки 4 недели; стек Python FastAPI; упаковка в Docker.",
        "target_users": "Покупатели интернет-магазина и сотрудники первой линии поддержки.",
        "business_contact": "CTO Алексей Смирнов (alexey@retail.kz), еженедельные онлайн-синки по вторникам."
    }
    score, breakdown, missing = calculate_task_score(full_task)
    assert score >= 90
    assert len(missing) == 0
    level_info = get_readiness_level(score)
    assert level_info["level"] == "Приоритетная"

def test_seed_data_counts():
    drafts = get_initial_drafts()
    tasks = get_initial_tasks()
    teams = get_initial_teams()
    proposals = get_initial_proposals()
    milestones = get_initial_milestones()

    assert len(drafts) >= 5
    assert len(tasks) >= 5
    assert len(teams) >= 5
    assert len(proposals) >= 5
    assert len(milestones) >= 5

def test_recommendation_scoring():
    team = {
        "industry_interests": ["Ритейл и e-commerce"],
        "task_type_interests": ["Диалоговый AI и чат-боты"],
        "preferred_readiness": "Любая"
    }
    task = {
        "industry": "Ритейл и e-commerce",
        "task_type": "Диалоговый AI и чат-боты",
        "rating": 95,
        "readiness_level": "Приоритетная"
    }
    score, explanation = calculate_recommendation_score(team, task)
    assert score == 100
    assert "доменное соответствие" in explanation
    assert "профиль компетенций" in explanation

def test_improvement_suggestions():
    partial_task = {
        "context_need": "Краткое описание проблемы без деталей.",
        "expected_result": "Чат-бот для саппорта."
    }
    score, breakdown, missing = calculate_task_score(partial_task)
    suggestions = get_improvement_suggestions(breakdown)
    assert len(suggestions) > 0
    top_suggestion = suggestions[0]
    assert "potential_points" in top_suggestion
    assert top_suggestion["potential_points"] > 0
