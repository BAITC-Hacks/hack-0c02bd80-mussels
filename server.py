import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import INDUSTRY_OPTIONS, TASK_TYPE_OPTIONS, READINESS_LEVELS
from services.storage import Storage
from services.ai_generator import AIGenerator
from services.seed_data import get_initial_drafts
from services.scoring import (
    calculate_task_score,
    get_readiness_level,
    get_improvement_suggestions,
)
from services.ui_components import render_circular_gauge

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="AI Sana Web App",
    description="Standalone web application for AI Sana hackathon platform",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

storage = Storage()
ai_generator = AIGenerator()


def get_ai_status() -> str:
    return "OpenAI API" if ai_generator.client else "Локальный движок"


def generate_milestones_for_task(task_id: str, title: str, task_type: str) -> List[Dict[str, Any]]:
    low_title = (title or "").lower()
    low_type = (task_type or "").lower()

    if "бот" in low_title or "диалог" in low_type:
        m1 = "Этап 1: Архитектура микросервиса и схема интеграции с базой FAQ"
        m2 = "Этап 2: Прототип чат-бота с классификацией интентов и диалоговым сценарием"
        m3 = "Этап 3: Финальный деплой веб-виджета, нагрузочное тестирование и передача оператору"
    elif "data" in low_type or "предиктив" in low_type or "кредит" in low_title:
        m1 = "Этап 1: Исследовательский анализ данных (EDA) и подготовка признаков"
        m2 = "Этап 2: Разработка и валидация прогнозной ML-модели"
        m3 = "Этап 3: Развертывание инференс-микросервиса и дашборд метрик качества"
    elif "веб" in low_type:
        m1 = "Этап 1: Проектирование UI/UX прототипов и спецификация OpenAPI"
        m2 = "Этап 2: Разработка клиентского веб-приложения и ключевых сценариев"
        m3 = "Этап 3: Комплексное тестирование, оптимизация LCP и релиз в продакшн"
    else:
        m1 = f"Этап 1: Проектирование архитектуры и подготовка требований: {title[:40]}"
        m2 = "Этап 2: Разработка базового функционального прототипа"
        m3 = "Этап 3: Финальное тестирование, документирование и сдача проекта"

    return [
        {
            "id": f"ms-{uuid.uuid4().hex[:6]}",
            "task_id": task_id,
            "team_id": "",
            "title": m1,
            "points": 25,
            "status": "in_progress",
            "completed_at": None
        },
        {
            "id": f"ms-{uuid.uuid4().hex[:6]}",
            "task_id": task_id,
            "team_id": "",
            "title": m2,
            "points": 35,
            "status": "in_progress",
            "completed_at": None
        },
        {
            "id": f"ms-{uuid.uuid4().hex[:6]}",
            "task_id": task_id,
            "team_id": "",
            "title": m3,
            "points": 40,
            "status": "in_progress",
            "completed_at": None
        }
    ]


class QANextRequest(BaseModel):
    draft_text: str = ""
    industry: str = "Ритейл и e-commerce"
    task_type: str = "Диалоговый AI и чат-боты"
    qa_history: List[Dict[str, str]] = Field(default_factory=list)


class TaskCreateRequest(BaseModel):
    draft_text: Optional[str] = ""
    industry: Optional[str] = "Ритейл и e-commerce"
    task_type: Optional[str] = "Диалоговый AI и чат-боты"
    qa_history: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    title: Optional[str] = None
    context_need: Optional[str] = None
    data_materials: Optional[str] = None
    expected_result: Optional[str] = None
    success_criteria: Optional[str] = None
    constraints: Optional[str] = None
    target_users: Optional[str] = None
    business_contact: Optional[str] = None


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
@app.api_route("/constructor", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def index_page(request: Request):
    initial_drafts = get_initial_drafts()
    sample_draft = initial_drafts[0] if initial_drafts else {}
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "current_route": request.url.path if request.url.path == "/constructor" else "/",
            "ai_status": get_ai_status(),
            "industry_options": INDUSTRY_OPTIONS,
            "task_type_options": TASK_TYPE_OPTIONS,
            "sample_draft": sample_draft,
            "initial_drafts": initial_drafts,
        }
    )



@app.api_route("/catalog", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def catalog_page(request: Request):
    tasks = storage.load_tasks()
    tasks.sort(key=lambda t: t.get("rating", 0), reverse=True)
    all_milestones = storage.load_milestones()

    for task in tasks:
        task["compact_gauge_html"] = render_circular_gauge(
            task.get("rating", 0), size=68, compact=True
        )
        task_milestones = [m for m in all_milestones if m.get("task_id") == task.get("id")]
        task["milestones"] = task_milestones if task_milestones else task.get("milestones", [])

    tasks_json = json.dumps(tasks, ensure_ascii=False)

    return templates.TemplateResponse(
        request=request,
        name="catalog.html",
        context={
            "current_route": "/catalog",
            "ai_status": get_ai_status(),
            "tasks": tasks,
            "tasks_json": tasks_json,
            "industry_options": INDUSTRY_OPTIONS,
            "task_type_options": TASK_TYPE_OPTIONS,
            "readiness_levels": READINESS_LEVELS,
        }
    )


class ProposalStatusRequest(BaseModel):
    status: str
    comment: Optional[str] = ""


def get_business_cabinet_data() -> List[Dict[str, Any]]:
    tasks = storage.load_tasks()
    all_milestones = storage.load_milestones()
    all_proposals = storage.load_proposals()
    teams = {t["id"]: t for t in storage.load_teams()}

    enriched_tasks = []
    for t in tasks:
        task_id = t.get("id")
        task_ms = [m for m in all_milestones if m.get("task_id") == task_id]
        if not task_ms and t.get("milestones"):
            task_ms = t.get("milestones")

        completed_count = sum(1 for m in task_ms if m.get("status") == "completed")
        total_count = len(task_ms)
        percentage = int(round((completed_count / total_count) * 100)) if total_count > 0 else 0
        earned_xp = sum(m.get("points", 0) for m in task_ms if m.get("status") == "completed")
        total_xp = sum(m.get("points", 0) for m in task_ms)
        potential_xp = total_xp - earned_xp

        task_props = [p for p in all_proposals if p.get("task_id") == task_id]
        for p in task_props:
            team = teams.get(p.get("team_id"), {})
            p["team_skills"] = team.get("skills", [])
            p["team_progress_points"] = team.get("progress_points", 0)

        accepted_prop = next((p for p in task_props if p.get("status") == "accepted"), None)
        accepted_team = teams.get(accepted_prop.get("team_id")) if accepted_prop else None

        enriched_tasks.append({
            **t,
            "milestones": task_ms,
            "proposals": task_props,
            "progress": {
                "completed_count": completed_count,
                "total_count": total_count,
                "percentage": percentage,
                "earned_xp": earned_xp,
                "total_xp": total_xp,
                "potential_xp": potential_xp
            },
            "accepted_proposal": accepted_prop,
            "accepted_team": accepted_team
        })

    return enriched_tasks


@app.api_route("/student", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def student_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={
            "current_route": "/student",
            "ai_status": get_ai_status(),
        }
    )


@app.api_route("/business", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def business_page(request: Request):
    tasks = get_business_cabinet_data()
    tasks_json = json.dumps(tasks, ensure_ascii=False)
    return templates.TemplateResponse(
        request=request,
        name="business.html",
        context={
            "current_route": "/business",
            "ai_status": get_ai_status(),
            "tasks": tasks,
            "tasks_json": tasks_json,
        }
    )


@app.post("/api/milestones/{task_id}/{milestone_id}/complete")
async def complete_milestone_endpoint(task_id: str, milestone_id: str):
    all_milestones = storage.load_milestones()
    target = next((m for m in all_milestones if m.get("id") == milestone_id), None)
    if not target:
        return JSONResponse({"status": "error", "message": "Этап не найден"}, status_code=404)

    if not target.get("team_id"):
        proposals = storage.get_proposals_for_task(task_id)
        accepted_prop = next((p for p in proposals if p.get("status") == "accepted"), None)
        if accepted_prop and accepted_prop.get("team_id"):
            target["team_id"] = accepted_prop.get("team_id")
            storage.save_milestones(all_milestones)

    completed = storage.complete_milestone(milestone_id)
    if completed is None:
        updated_milestone = target
    else:
        updated_milestone = completed

    task_milestones = [m for m in storage.load_milestones() if m.get("task_id") == task_id]
    completed_count = sum(1 for m in task_milestones if m.get("status") == "completed")
    total_count = len(task_milestones)
    percentage = int(round((completed_count / total_count) * 100)) if total_count > 0 else 0
    earned_xp = sum(m.get("points", 0) for m in task_milestones if m.get("status") == "completed")
    total_xp = sum(m.get("points", 0) for m in task_milestones)
    potential_xp = total_xp - earned_xp

    return JSONResponse({
        "status": "ok",
        "task_id": task_id,
        "milestone": updated_milestone,
        "awarded_xp": updated_milestone.get("points", 0),
        "progress": {
            "completed_count": completed_count,
            "total_count": total_count,
            "percentage": percentage,
            "earned_xp": earned_xp,
            "total_xp": total_xp,
            "potential_xp": potential_xp
        }
    })


@app.post("/api/proposals/{proposal_id}/status")
async def proposal_status_endpoint(proposal_id: str, payload: ProposalStatusRequest):
    updated = storage.update_proposal_status(proposal_id, payload.status, payload.comment or "")
    if not updated:
        return JSONResponse({"status": "error", "message": "Отклик не найден"}, status_code=404)

    if payload.status == "accepted":
        task_id = updated.get("task_id")
        team_id = updated.get("team_id")
        if task_id and team_id:
            milestones = storage.load_milestones()
            changed = False
            for m in milestones:
                if m.get("task_id") == task_id and not m.get("team_id"):
                    m["team_id"] = team_id
                    changed = True
            if changed:
                storage.save_milestones(milestones)

    return JSONResponse({
        "status": "ok",
        "proposal": updated
    })


@app.api_route("/jury-demo", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def jury_demo_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="jury_demo.html",
        context={
            "current_route": "/jury-demo",
            "ai_status": get_ai_status(),
        }
    )


@app.get("/demo")
async def demo_redirect():
    return RedirectResponse(url="/jury-demo", status_code=302)


@app.post("/api/reset-data")
async def reset_data_endpoint():
    storage.reset_all_data()
    return JSONResponse(
        {
            "status": "ok",
            "message": "База данных успешно сброшена к начальному эталонному состоянию"
        }
    )


@app.post("/api/qa/next")
async def qa_next_endpoint(payload: QANextRequest):
    result = ai_generator.generate_next_question(
        draft_text=payload.draft_text,
        industry=payload.industry,
        task_type=payload.task_type,
        qa_history=payload.qa_history
    )
    return JSONResponse(result)


@app.post("/api/tasks/create")
@app.post("/api/tasks/synthesize")
async def tasks_create_endpoint(payload: TaskCreateRequest):
    has_full_fields = bool(payload.title and payload.context_need and payload.expected_result)
    if has_full_fields:
        card = {
            "title": payload.title,
            "industry": payload.industry or "Ритейл и e-commerce",
            "task_type": payload.task_type or "Диалоговый AI и чат-боты",
            "context_need": payload.context_need or "",
            "data_materials": payload.data_materials or "",
            "expected_result": payload.expected_result or "",
            "success_criteria": payload.success_criteria or "",
            "constraints": payload.constraints or "",
            "target_users": payload.target_users or "",
            "business_contact": payload.business_contact or ""
        }
    else:
        card = ai_generator.synthesize_task_card(
            draft_text=payload.draft_text or "",
            industry=payload.industry or "Ритейл и e-commerce",
            task_type=payload.task_type or "Диалоговый AI и чат-боты",
            qa_history=payload.qa_history or []
        )
        if payload.title:
            card["title"] = payload.title
        if payload.context_need:
            card["context_need"] = payload.context_need
        if payload.data_materials:
            card["data_materials"] = payload.data_materials
        if payload.expected_result:
            card["expected_result"] = payload.expected_result
        if payload.success_criteria:
            card["success_criteria"] = payload.success_criteria
        if payload.constraints:
            card["constraints"] = payload.constraints
        if payload.target_users:
            card["target_users"] = payload.target_users
        if payload.business_contact:
            card["business_contact"] = payload.business_contact

    score, breakdown, missing_fields = calculate_task_score(card)
    level_info = get_readiness_level(score)
    suggestions = get_improvement_suggestions(breakdown)

    task_id = f"task-{uuid.uuid4().hex[:6]}"
    now_iso = datetime.now().isoformat()
    card["id"] = task_id
    card["rating"] = score
    card["readiness_level"] = level_info["level"]
    card["rating_breakdown"] = breakdown
    card["missing_fields"] = missing_fields
    card["published"] = True
    card["created_at"] = now_iso
    card["updated_at"] = now_iso

    milestones = generate_milestones_for_task(task_id, card.get("title", ""), card.get("task_type", ""))
    for m in milestones:
        storage.add_milestone(m)
    card["milestones"] = milestones

    storage.upsert_task(card)

    gauge_html = render_circular_gauge(score, size=150, title="Рейтинг готовности")

    return JSONResponse({
        "status": "ok",
        "task": card,
        "score": score,
        "readiness_level": level_info["level"],
        "readiness_description": level_info["description"],
        "rating_breakdown": breakdown,
        "missing_fields": missing_fields,
        "suggestions": suggestions,
        "milestones": milestones,
        "gauge_html": gauge_html
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
