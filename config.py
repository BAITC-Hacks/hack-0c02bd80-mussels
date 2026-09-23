import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SCORING_WEIGHTS = {
    "context_need": {
        "max_points": 20,
        "title": "Контекст и потребность",
        "description": "Понятно, что происходит сейчас и что необходимо изменить"
    },
    "data_materials": {
        "max_points": 20,
        "title": "Данные и материалы",
        "description": "Указаны доступные данные, примеры или источники"
    },
    "expected_result": {
        "max_points": 15,
        "title": "Ожидаемый результат",
        "description": "Описан конкретный результат работы команды"
    },
    "success_criteria": {
        "max_points": 15,
        "title": "Критерии успеха",
        "description": "Есть измеримые признаки принятия решения"
    },
    "constraints": {
        "max_points": 10,
        "title": "Ограничения",
        "description": "Указаны сроки, технологии, доступы или иные границы"
    },
    "target_users": {
        "max_points": 10,
        "title": "Пользователи",
        "description": "Понятно, для кого создается решение"
    },
    "business_contact": {
        "max_points": 10,
        "title": "Связь с бизнесом",
        "description": "Есть контакт, формат консультаций и порядок обратной связи"
    }
}

READINESS_LEVELS = [
    {
        "min_score": 90,
        "max_score": 100,
        "level": "Приоритетная",
        "description": "Задача полностью готова к работе и выделяется в каталоге",
        "badge_class": "badge-priority"
    },
    {
        "min_score": 70,
        "max_score": 89,
        "level": "Готовая",
        "description": "Задача получает повышенную позицию в каталоге",
        "badge_class": "badge-ready"
    },
    {
        "min_score": 40,
        "max_score": 69,
        "level": "Рабочая",
        "description": "Студенты могут откликаться, системе разрешено рекомендовать задачу",
        "badge_class": "badge-workable"
    },
    {
        "min_score": 0,
        "max_score": 39,
        "level": "Черновик",
        "description": "Задача видна в каталоге, но отмечена как требующая уточнения",
        "badge_class": "badge-draft"
    }
]

INDUSTRY_OPTIONS = [
    "Ритейл и e-commerce",
    "Финтех и банкинг",
    "EdTech и образование",
    "Логистика и доставка",
    "Здравоохранение и медицина",
    "Промышленность и производство"
]

TASK_TYPE_OPTIONS = [
    "Диалоговый AI и чат-боты",
    "Data Science и предиктивная аналитика",
    "Веб-платформы и клиентские сервисы",
    "Автоматизация бизнес-процессов",
    "Компьютерное зрение и мультимедиа"
]
