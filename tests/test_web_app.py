import re
from pathlib import Path
import pytest
from starlette.testclient import TestClient

# Import will fail during initial red phase if server.py is not yet created
try:
    from server import app
except ImportError:
    app = None


@pytest.fixture
def client():
    assert app is not None, "server.app must be defined"
    return TestClient(app)


def test_index_page_status_and_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    content = response.text
    assert "AI Sana" in content
    assert "Конструктор" in content
    assert "Каталог" in content
    assert "Команда" in content or "Кабинет студента" in content
    assert "Бизнес" in content or "Кабинет бизнеса" in content
    assert "Демо жюри" in content
    assert "OpenAI API" in content or "Локальный движок" in content
    assert "/api/reset-data" in content or "Сброс данных" in content


def test_nav_routes(client):
    for route in ["/catalog", "/student", "/business", "/jury-demo"]:
        response = client.get(route)
        assert response.status_code == 200
        assert "AI Sana" in response.text


def test_reset_data_endpoint(client):
    response = client.post("/api/reset-data")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_constructor_page_renders_form_and_seed_data(client):
    for route in ["/", "/constructor"]:
        response = client.get(route)
        assert response.status_code == 200
        content = response.text
        assert "Конструктор задачи" in content
        assert "Заполнить эталонный черновик" in content
        assert "Ритейл и e-commerce" in content
        assert "Диалоговый AI и чат-боты" in content
        assert "Быстрый ответ для жюри" in content
        assert "Рейтинг готовности" in content


def test_qa_next_endpoint_flow(client):
    # Initial question
    payload = {
        "draft_text": "Нужен умный чат-бот для поддержки клиентов интернет-магазина электроники",
        "industry": "Ритейл и e-commerce",
        "task_type": "Диалоговый AI и чат-боты",
        "qa_history": []
    }
    response = client.post("/api/qa/next", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "question" in data and len(data["question"]) > 0
    assert "field_target" in data
    assert "quick_reply_for_jury" in data and len(data["quick_reply_for_jury"]) > 0
    first_target = data["field_target"]

    # Next question with history
    payload["qa_history"].append({
        "question": data["question"],
        "field_target": first_target,
        "answer": data["quick_reply_for_jury"]
    })
    response2 = client.post("/api/qa/next", json=payload)
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["field_target"] != first_target


def test_tasks_create_and_synthesize_endpoint(client):
    payload = {
        "draft_text": "Нужен умный чат-бот для поддержки клиентов интернет-магазина электроники",
        "industry": "Ритейл и e-commerce",
        "task_type": "Диалоговый AI и чат-боты",
        "qa_history": [
            {
                "question": "Какие исходные данные вы готовы предоставить?",
                "field_target": "data_materials",
                "answer": "Выгрузка 25 000 обезличенных диалогов в формате JSONL, база знаний FAQ из 450 статей, каталог товаров с характеристиками в формате CSV."
            },
            {
                "question": "Какой ожидаемый результат работы команды?",
                "field_target": "expected_result",
                "answer": "Работающий микросервис чат-бота с интеграцией в Telegram и веб-виджет, классификатором интентов и возможностью перевода сложного диалога на оператора."
            },
            {
                "question": "По каким критериям будете оценивать успех?",
                "field_target": "success_criteria",
                "answer": "Автоматическое разрешение не менее 65% типовых обращений без участия человека; точность классификации интентов не ниже 88%; среднее время ответа до 2 секунд."
            },
            {
                "question": "Каковы технические ограничения проекта?",
                "field_target": "constraints",
                "answer": "Срок разработки 4 недели; язык Python (FastAPI); упаковка в Docker-контейнер; соответствие 152-ФЗ по персональным данным."
            },
            {
                "question": "Кто конечные пользователи решения?",
                "field_target": "target_users",
                "answer": "Покупатели интернет-магазина и дежурные специалисты первой линии технической поддержки."
            },
            {
                "question": "Кто контактное лицо со стороны бизнеса?",
                "field_target": "business_contact",
                "answer": "CTO Алексей Смирнов (alexey@retail-tech.kz, Telegram: @alex_retail), еженедельные онлайн-синки по вторникам в 15:00."
            }
        ]
    }
    
    # Test /api/tasks/create
    resp = client.post("/api/tasks/create", json=payload)
    assert resp.status_code == 200
    res = resp.json()
    assert res.get("status") == "ok"
    task = res.get("task")
    assert task is not None
    assert task["id"]
    assert task["title"]
    assert task["rating"] >= 70
    assert task["readiness_level"] in ["Готовая", "Приоритетная"]
    assert "milestones" in res
    assert len(res["milestones"]) == 3
    assert sum(m["points"] for m in res["milestones"]) == 100
    assert "gauge_html" in res
    assert "<svg" in res["gauge_html"]

    # Verify task was saved in storage
    from server import storage
    stored_task = storage.get_task_by_id(task["id"])
    assert stored_task is not None
    assert stored_task["title"] == task["title"]

    # Verify milestones were saved
    stored_milestones = [m for m in storage.load_milestones() if m.get("task_id") == task["id"]]
    assert len(stored_milestones) == 3

    # Test alias /api/tasks/synthesize
    alias_resp = client.post("/api/tasks/synthesize", json=payload)
    assert alias_resp.status_code == 200
    assert alias_resp.json().get("status") == "ok"


def test_catalog_page_renders_tasks_and_filters(client):
    response = client.get("/catalog")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    content = response.text
    assert "Общий каталог задач" in content
    assert "Найдено:" in content or "Найдено" in content
    assert "Ритейл и e-commerce" in content
    assert "Финтех и банкинг" in content
    assert "Приоритетная" in content
    assert "Готовая" in content
    assert "Рабочая" in content
    assert "Черновик" in content
    assert "Интеллектуальный ассистент клиентской поддержки" in content
    assert "Предиктивная модель кредитного скоринга" in content
    assert "<svg" in content
    assert "Подробнее о задаче" in content or "Подробнее" in content


def test_catalog_tasks_sorted_by_rating_descending(client):
    response = client.get("/catalog")
    assert response.status_code == 200
    content = response.text

    idx_95 = content.find("Интеллектуальный ассистент клиентской поддержки")
    idx_85 = content.find("Предиктивная модель кредитного скоринга")
    idx_30 = content.find("Автоматическая маршрутизация пациентов поликлиники")

    assert idx_95 != -1, "Task with rating 95 must be present"
    assert idx_85 != -1, "Task with rating 85 must be present"
    assert idx_30 != -1, "Task with rating 30 must be present"
    assert idx_95 < idx_85 < idx_30, "Tasks must be sorted in descending order of rating"


def test_catalog_modal_contains_tz_blocks(client):
    response = client.get("/catalog")
    assert response.status_code == 200
    content = response.text
    for block_label in ["Контекст", "Данные", "Ожидаемый результат", "Критерии", "Ограничения"]:
        assert block_label in content


def test_catalog_tasks_json_data(client):
    response = client.get("/catalog")
    assert response.status_code == 200
    content = response.text
    assert "tasks: [" in content
    assert '"id": "task-001"' in content
    assert '"rating": 95' in content
    assert '"readiness_level": "Приоритетная"' in content



def test_business_page_renders_tasks_milestones_and_proposals(client):
    response = client.get("/business")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    content = response.text
    assert "Кабинет бизнеса" in content
    assert "Шкала прогресса" in content or "контрольных этапов" in content
    assert "Входящие отклики команд" in content or "Отклики команд" in content
    assert "Выбрать команду" in content
    assert "Отклонить" in content
    assert "Подтвердить этап" in content or "+XP" in content
    assert "Ожидает назначения команды" in content
    assert "Сначала выберите команду-исполнителя" in content
    # Ensure tasks and proposals from seed data are rendered
    assert "Интеллектуальный ассистент клиентской поддержки" in content or "task-001" in content
    assert "NeuralMinds" in content or "EdTech Innovators" in content


def test_milestone_complete_endpoint(client):
    from server import storage
    storage.reset_all_data()

    # Find an in_progress milestone for task-001
    milestones = storage.load_milestones()
    target_ms = next((m for m in milestones if m.get("task_id") == "task-001" and m.get("status") != "completed"), None)
    assert target_ms is not None, "Must have an in_progress milestone for task-001"
    ms_id = target_ms["id"]

    team_id = target_ms.get("team_id") or "team-001"
    team_before = storage.get_team_by_id(team_id)
    points_before = team_before.get("progress_points", 0)

    # Call complete endpoint
    resp = client.post(f"/api/milestones/task-001/{ms_id}/complete")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "ok"
    assert data.get("milestone") is not None
    assert data["milestone"]["status"] == "completed"
    assert data["milestone"]["completed_at"] is not None
    assert data.get("awarded_xp") == target_ms.get("points", 25)
    assert "progress" in data
    assert data["progress"]["completed_count"] >= 1
    assert data["progress"]["earned_xp"] >= target_ms.get("points", 25)

    # Verify team progress points updated in storage
    team_after = storage.get_team_by_id(team_id)
    assert team_after["progress_points"] == points_before + target_ms.get("points", 25)
    assert ms_id in team_after.get("completed_milestones", [])

    # Completing already completed milestone should return ok without double-awarding
    resp2 = client.post(f"/api/milestones/task-001/{ms_id}/complete")
    assert resp2.status_code == 200
    team_after_repeat = storage.get_team_by_id(team_id)
    assert team_after_repeat["progress_points"] == team_after["progress_points"]


def test_milestone_complete_guardrail_without_accepted_team(client):
    from server import storage
    storage.reset_all_data()

    # task-003 has prop-004 in pending status (no accepted proposal)
    task_id = "task-003"
    ms_id = "ms-guardrail-test"
    storage.add_milestone({
        "id": ms_id,
        "task_id": task_id,
        "team_id": "",
        "title": "Тестовый этап без выбранной команды",
        "points": 35,
        "status": "in_progress",
        "completed_at": None
    })

    team_id = "team-003"
    team_before = storage.get_team_by_id(team_id)
    points_before = team_before.get("progress_points", 0)

    # 1. Attempt to complete milestone without an accepted team -> 400 Bad Request
    resp = client.post(f"/api/milestones/{task_id}/{ms_id}/complete")
    assert resp.status_code == 400
    err_data = resp.json()
    assert err_data.get("status") == "error"
    assert "команд" in err_data.get("message", "").lower()

    # Verify milestone status did not change and no points awarded
    ms_in_storage = next((m for m in storage.load_milestones() if m["id"] == ms_id), None)
    assert ms_in_storage is not None
    assert ms_in_storage.get("status") == "in_progress"
    assert ms_in_storage.get("completed_at") is None

    team_after_fail = storage.get_team_by_id(team_id)
    assert team_after_fail["progress_points"] == points_before

    # 2. Accept proposal for task-003
    accept_resp = client.post(
        "/api/proposals/prop-004/status",
        json={"status": "accepted", "comment": "Команда утверждена"}
    )
    assert accept_resp.status_code == 200

    # 3. Now completing the milestone must succeed and award XP to the accepted team
    success_resp = client.post(f"/api/milestones/{task_id}/{ms_id}/complete")
    assert success_resp.status_code == 200
    success_data = success_resp.json()
    assert success_data.get("status") == "ok"
    assert success_data["milestone"]["status"] == "completed"
    assert success_data["milestone"]["team_id"] == team_id

    team_after_success = storage.get_team_by_id(team_id)
    assert team_after_success["progress_points"] == points_before + 35
    assert ms_id in team_after_success.get("completed_milestones", [])


def test_proposal_status_update_endpoint(client):
    from server import storage
    storage.reset_all_data()

    # prop-002 is originally pending
    proposals = storage.load_proposals()
    prop_002 = next((p for p in proposals if p["id"] == "prop-002"), None)
    assert prop_002 is not None
    assert prop_002.get("status") == "pending"

    # Accept proposal
    accept_resp = client.post(
        "/api/proposals/prop-002/status",
        json={"status": "accepted", "comment": "Отличная идея решения, берем в работу"}
    )
    assert accept_resp.status_code == 200
    accept_data = accept_resp.json()
    assert accept_data.get("status") == "ok"
    assert accept_data.get("proposal")["status"] == "accepted"
    assert accept_data.get("proposal")["review_comment"] == "Отличная идея решения, берем в работу"

    # Verify in storage
    updated_prop = next((p for p in storage.load_proposals() if p["id"] == "prop-002"), None)
    assert updated_prop["status"] == "accepted"
    assert updated_prop["review_comment"] == "Отличная идея решения, берем в работу"

    # Reject proposal prop-004
    reject_resp = client.post(
        "/api/proposals/prop-004/status",
        json={"status": "rejected", "comment": "Стек не соответствует требованиям"}
    )
    assert reject_resp.status_code == 200
    reject_data = reject_resp.json()
    assert reject_data.get("status") == "ok"
    assert reject_data.get("proposal")["status"] == "rejected"
    assert reject_data.get("proposal")["review_comment"] == "Стек не соответствует требованиям"


def test_student_page_renders_team_profile_and_xp_summary(client):
    from server import storage
    storage.reset_all_data()

    response = client.get("/student")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    content = response.text
    assert "Кабинет студенческой команды" in content
    # Default team
    assert "NeuralMinds" in content
    # XP Stats
    assert "125" in content  # Team 001 points
    assert "XP" in content
    # Milestones ledger
    assert "Архитектура микросервиса" in content
    assert "+25 XP" in content or "25 XP" in content
    # In-progress milestone
    assert "Финальный деплой веб-виджета" in content
    # Recommendations block
    assert "Персональные AI-рекомендации" in content or "AI-рекомендации" in content
    assert "Совпадение 100%" in content or "100%" in content
    assert "доменное соответствие" in content
    assert "Перейти к задаче" in content or "В каталог" in content or "/catalog" in content


def test_student_recommendation_calculation(client):
    from server import storage
    from services.recommendation import calculate_recommendation_score
    storage.reset_all_data()

    team_1 = storage.get_team_by_id("team-001")
    task_1 = storage.get_task_by_id("task-001")
    score_1, reason_1 = calculate_recommendation_score(team_1, task_1)
    assert score_1 == 100
    assert "доменное соответствие" in reason_1
    assert "профиль компетенций" in reason_1

    team_2 = storage.get_team_by_id("team-002")
    task_2 = storage.get_task_by_id("task-002")
    score_2, reason_2 = calculate_recommendation_score(team_2, task_2)
    assert score_2 >= 90
    assert "доменное соответствие" in reason_2


def test_student_team_switching(client):
    from server import storage
    storage.reset_all_data()

    # Switch to team-002 (DataCrafters)
    resp2 = client.get("/student?team_id=team-002")
    assert resp2.status_code == 200
    content2 = resp2.text
    assert "DataCrafters" in content2
    assert "95" in content2  # 95 XP
    assert "CatBoost" in content2 or "Финтех" in content2

    # Switch to team-003 (EdTech Innovators)
    resp3 = client.get("/student?team_id=team-003")
    assert resp3.status_code == 200
    content3 = resp3.text
    assert "EdTech Innovators" in content3
    assert "70" in content3  # 70 XP


def test_jury_demo_page_content_and_steps(client):
    response = client.get("/jury-demo")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    content = response.text

    assert "Экспресс-демонстрация" in content
    # 5 Key Steps
    assert "Шаг 1" in content
    assert "Первичная потребность" in content or "эталонный черновик" in content
    assert "Шаг 2" in content
    assert "диалог с AI" in content or "AI-интервью" in content
    assert "Шаг 3" in content
    assert "Синтез карточки" in content or "рейтинга готовности" in content or "спидометр" in content
    assert "Шаг 4" in content
    assert "Общий каталог" in content or "рекомендации студентам" in content
    assert "Шаг 5" in content
    assert "Кабинет бизнеса" in content or "ручной выбор" in content or "контрольных этапов" in content

    # Quick links to modules
    assert 'href="/constructor"' in content or 'href="/"' in content
    assert 'href="/catalog"' in content
    assert 'href="/student"' in content
    assert 'href="/business"' in content

    # Architectural Memo
    assert "Clean Tech White" in content or "чистая белая" in content.lower()
    assert "ADR-0003" in content or "запрет автоназначения" in content.lower()
    assert "двухрежим" in content.lower() or "локальный движок" in content.lower() or "openai" in content.lower()
    assert "XP" in content or "баллы прогресса" in content.lower()

    # Reset Data Action
    assert "/api/reset-data" in content or "Сброс данных" in content


def test_demo_redirect(client):
    response = client.get("/demo", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["location"] == "/jury-demo"


def test_run_web_script():
    import os
    script_path = Path(__file__).resolve().parent.parent / "run_web.sh"
    assert script_path.exists(), "run_web.sh must exist in repository root"
    assert os.access(script_path, os.X_OK), "run_web.sh must be executable"
    content = script_path.read_text(encoding="utf-8")
    assert "uvicorn" in content
    assert "8000" in content
    assert "server:app" in content
    assert "venv" in content
    assert "http://localhost:8000" in content


def test_no_emojis_in_web_code():
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U0001FA00-\U0001FA6F"  # symbols and pictographs extended-a
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
        "\U00002600-\U000026FF"  # misc symbols
        "]+",
        flags=re.UNICODE,
    )

    base_dir = Path(__file__).resolve().parent.parent
    files_to_check = [
        base_dir / "server.py",
        base_dir / "run_web.sh",
        Path(__file__)
    ]
    templates_dir = base_dir / "templates"
    if templates_dir.exists():
        files_to_check.extend(templates_dir.rglob("*.html"))

    for file_path in files_to_check:
        if file_path.exists():
            text = file_path.read_text(encoding="utf-8")
            matches = emoji_pattern.findall(text)
            assert not matches, f"Emoji found in {file_path}: {matches}"



