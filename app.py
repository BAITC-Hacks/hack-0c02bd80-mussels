import streamlit as st
import pandas as pd
from typing import Dict, Any, List
from datetime import datetime

from config import (
    SCORING_WEIGHTS,
    READINESS_LEVELS,
    INDUSTRY_OPTIONS,
    TASK_TYPE_OPTIONS,
    OPENAI_API_KEY,
    OPENAI_MODEL
)
from services import (
    calculate_task_score,
    get_readiness_level,
    get_improvement_suggestions,
    calculate_recommendation_score,
    Storage,
    AIGenerator
)

# Page configuration
st.set_page_config(
    page_title="AI Sana: Платформа геймификации бизнес-задач",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional look (Strictly NO EMOJIS)
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-priority {
        background-color: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
    }
    .badge-ready {
        background-color: #dbeafe;
        color: #1d4ed8;
        border: 1px solid #93c5fd;
    }
    .badge-workable {
        background-color: #fef9c3;
        color: #a16207;
        border: 1px solid #fde047;
    }
    .badge-draft {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fca5a5;
    }
    .score-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .recommendation-banner {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 12px;
        margin-bottom: 12px;
        border-radius: 0 6px 6px 0;
    }
    .task-card-box {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize storage and AI engine
@st.cache_resource
def get_storage():
    return Storage()

@st.cache_resource
def get_ai_generator():
    return AIGenerator()

storage = get_storage()
ai_generator = get_ai_generator()

# Session state initialization
if "draft_text" not in st.session_state:
    st.session_state.draft_text = ""
if "draft_industry" not in st.session_state:
    st.session_state.draft_industry = INDUSTRY_OPTIONS[0]
if "draft_task_type" not in st.session_state:
    st.session_state.draft_task_type = TASK_TYPE_OPTIONS[0]
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "active_card" not in st.session_state:
    st.session_state.active_card = None

# Sidebar navigation
st.sidebar.title("Навигация платформы")
menu = st.sidebar.radio(
    "Разделы:",
    [
        "1. Конструктор задачи (Бизнес)",
        "2. Общий каталог задач",
        "3. Кабинет студенческой команды",
        "4. Отклики и решения бизнеса",
        "5. Экспресс-демонстрация (Жюри)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Статус системы")
api_status = "OpenAI API активен" if ai_generator.client else "Локальный детерминированный движок"
st.sidebar.info(f"Режим AI: {api_status}")

if st.sidebar.button("Сбросить все данные к исходным"):
    storage.reset_all_data()
    st.session_state.draft_text = ""
    st.session_state.qa_history = []
    st.session_state.current_question = None
    st.session_state.active_card = None
    st.sidebar.success("Данные успешно сброшены к начальным 5 черновикам, карточкам и командам.")
    st.rerun()


# ==========================================
# 1. КОНСТРУКТОР ЗАДАЧИ (БИЗНЕС)
# ==========================================
if menu == "1. Конструктор задачи (Бизнес)":
    st.markdown("<div class='main-title'>Конструктор бизнес-задачи</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Превращение сырого описания потребности в подтвержденную карточку с расчетом рейтинга готовности</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Шаг 1 и 2: Ввод и пошаговое уточнение", "Шаг 3 и 4: Карточка и рейтинг"])

    with tab1:
        st.subheader("Шаг 1: Первоначальный ввод черновика")
        col1, col2 = st.columns([2, 1])
        with col1:
            draft_input = st.text_area(
                "Краткое описание проблемы, идеи или потребности бизнеса:",
                value=st.session_state.draft_text,
                height=110,
                placeholder="Например: Нужен умный чат-бот для поддержки клиентов интернет-магазина, чтобы разгрузить операторов в пиковые часы."
            )
        with col2:
            industry_val = st.selectbox("Отрасль бизнеса:", INDUSTRY_OPTIONS, index=INDUSTRY_OPTIONS.index(st.session_state.draft_industry))
            task_type_val = st.selectbox("Направление задачи:", TASK_TYPE_OPTIONS, index=TASK_TYPE_OPTIONS.index(st.session_state.draft_task_type))

            if st.button("Заполнить эталонный черновик для демо"):
                st.session_state.draft_text = "Нужен умный чат-бот для поддержки клиентов интернет-магазина электроники, чтобы разгрузить операторов в пиковые часы."
                st.session_state.draft_industry = "Ритейл и e-commerce"
                st.session_state.draft_task_type = "Диалоговый AI и чат-боты"
                st.session_state.qa_history = []
                st.session_state.current_question = None
                st.session_state.active_card = None
                st.rerun()

        st.session_state.draft_text = draft_input
        st.session_state.draft_industry = industry_val
        st.session_state.draft_task_type = task_type_val

        st.markdown("---")
        st.subheader("Шаг 2: Пошаговый диалог уточнения задачи")

        if not st.session_state.draft_text.strip():
            st.info("Введите описание черновика выше, чтобы запустить процесс уточнения с помощью AI.")
        else:
            # Generate first question if not yet present
            if st.session_state.current_question is None:
                next_q = ai_generator.generate_next_question(
                    st.session_state.draft_text,
                    st.session_state.draft_industry,
                    st.session_state.draft_task_type,
                    st.session_state.qa_history
                )
                st.session_state.current_question = next_q

            # Display previous QA history
            if st.session_state.qa_history:
                st.markdown("**Ранее отвеченные вопросы:**")
                for idx, qa in enumerate(st.session_state.qa_history, 1):
                    with st.expander(f"Вопрос {idx}: {qa['question']}", expanded=False):
                        st.markdown(f"**Ответ бизнеса:** {qa['answer']}")
                        st.caption(f"Уточненный блок: {SCORING_WEIGHTS.get(qa.get('field_target', ''), {}).get('title', 'Общее')}")

            # Active question container
            curr = st.session_state.current_question
            target_title = SCORING_WEIGHTS.get(curr.get("field_target", ""), {}).get("title", "Уточнение")
            
            st.markdown(f"**Текущий вопрос системы (направление: {target_title}):**")
            st.info(curr["question"])

            ans_key = f"answer_input_{len(st.session_state.qa_history)}"
            user_ans = st.text_input("Ваш ответ представителя бизнеса:", key=ans_key)

            col_btn1, col_btn2 = st.columns([1, 1])
            with col_btn1:
                if st.button("Быстрый ответ для жюри"):
                    # Immediately record quick answer and move forward
                    st.session_state.qa_history.append({
                        "question": curr["question"],
                        "field_target": curr["field_target"],
                        "answer": curr["quick_reply_for_jury"]
                    })
                    st.session_state.current_question = ai_generator.generate_next_question(
                        st.session_state.draft_text,
                        st.session_state.draft_industry,
                        st.session_state.draft_task_type,
                        st.session_state.qa_history
                    )
                    st.rerun()

            with col_btn2:
                if st.button("Отправить свой ответ"):
                    if user_ans.strip():
                        st.session_state.qa_history.append({
                            "question": curr["question"],
                            "field_target": curr["field_target"],
                            "answer": user_ans.strip()
                        })
                        st.session_state.current_question = ai_generator.generate_next_question(
                            st.session_state.draft_text,
                            st.session_state.draft_industry,
                            st.session_state.draft_task_type,
                            st.session_state.qa_history
                        )
                        st.rerun()
                    else:
                        st.warning("Пожалуйста, введите ответ или нажмите кнопку быстрого ответа.")

            # Activation of card synthesis button
            st.markdown("---")
            questions_count = len(st.session_state.qa_history)
            
            if questions_count >= 3:
                st.success(f"Завершено {questions_count} уточнений (выполнено обязательное требование: не менее 3 вопросов). Кнопка синтеза карточки активна.")
                if st.button("Сформировать финальную карточку задачи", type="primary"):
                    with st.spinner("Синтез карточки и расчет рейтинга готовности..."):
                        card_data = ai_generator.synthesize_task_card(
                            st.session_state.draft_text,
                            st.session_state.draft_industry,
                            st.session_state.draft_task_type,
                            st.session_state.qa_history
                        )
                        # Score the synthesized card
                        score, breakdown, missing = calculate_task_score(card_data)
                        level_info = get_readiness_level(score)
                        card_data["id"] = f"task-{datetime.now().strftime('%M%S')}"
                        card_data["rating"] = score
                        card_data["readiness_level"] = level_info["level"]
                        card_data["rating_breakdown"] = breakdown
                        card_data["missing_fields"] = missing
                        card_data["published"] = False
                        st.session_state.active_card = card_data
                    st.success("Карточка успешно сформирована. Перейдите на вкладку 'Шаг 3 и 4: Карточка и рейтинг'.")
            else:
                st.caption(f"Отвечено вопросов: {questions_count}. Для генерации карточки необходимо ответить минимум на 3 вопроса.")

    with tab2:
        st.subheader("Шаг 3 и 4: Редактируемая карточка и рейтинг готовности")
        
        if st.session_state.active_card is None:
            st.info("Карточка еще не создана. Сначала завершите опрос на вкладке 'Шаг 1 и 2' или загрузите готовую задачу.")
            if st.button("Загрузить образец карточки для редактирования"):
                initial_tasks = storage.load_tasks()
                if initial_tasks:
                    st.session_state.active_card = initial_tasks[0].copy()
                    st.rerun()
        else:
            card = st.session_state.active_card

            # Recalculate score live based on current card inputs
            c_score, c_breakdown, c_missing = calculate_task_score(card)
            c_level_info = get_readiness_level(c_score)
            card["rating"] = c_score
            card["readiness_level"] = c_level_info["level"]
            card["rating_breakdown"] = c_breakdown
            card["missing_fields"] = c_missing

            # Top rating banner
            col_r1, col_r2 = st.columns([1, 2])
            with col_r1:
                st.metric("Текущий рейтинг готовности:", f"{c_score} / 100 баллов")
                st.markdown(f"Уровень: **{c_level_info['level']}** — {c_level_info['description']}")
            with col_r2:
                st.markdown("**Что дает баллы сейчас:**")
                breakdown_cols = st.columns(4)
                idx = 0
                for f_key, pts in c_breakdown.items():
                    col_idx = idx % 4
                    breakdown_cols[col_idx].caption(f"{SCORING_WEIGHTS[f_key]['title']}: **{pts} б.**")
                    idx += 1

            st.markdown("---")

            # Editable card fields
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                card["title"] = st.text_input("Название задачи:", value=card.get("title", ""))
                card["context_need"] = st.text_area(
                    "1. Контекст и потребность (до 20 баллов):",
                    value=card.get("context_need", ""),
                    height=100
                )
                card["data_materials"] = st.text_area(
                    "2. Данные и материалы (до 20 баллов):",
                    value=card.get("data_materials", ""),
                    height=100
                )
                card["expected_result"] = st.text_area(
                    "3. Ожидаемый результат (до 15 баллов):",
                    value=card.get("expected_result", ""),
                    height=90
                )
            with col_f2:
                card["success_criteria"] = st.text_area(
                    "4. Критерии успеха (до 15 баллов):",
                    value=card.get("success_criteria", ""),
                    height=90
                )
                card["constraints"] = st.text_area(
                    "5. Ограничения (до 10 баллов):",
                    value=card.get("constraints", ""),
                    height=80
                )
                card["target_users"] = st.text_area(
                    "6. Пользователи (до 10 баллов):",
                    value=card.get("target_users", ""),
                    height=80
                )
                card["business_contact"] = st.text_area(
                    "7. Связь с бизнесом (до 10 баллов):",
                    value=card.get("business_contact", ""),
                    height=80
                )

            # Improvement suggestions
            suggestions = get_improvement_suggestions(c_breakdown)
            if suggestions:
                st.markdown("**Рекомендации по повышению рейтинга задачи:**")
                for s in suggestions[:3]:
                    st.caption(f"- {s['hint']}")

            st.markdown("---")
            col_act1, col_act2 = st.columns([1, 1])
            with col_act1:
                if st.button("Сохранить изменения карточки"):
                    storage.upsert_task(card)
                    st.success("Изменения сохранены. Рейтинг пересчитан.")
            with col_act2:
                if st.button("Подтвердить и опубликовать в каталоге", type="primary"):
                    card["published"] = True
                    storage.upsert_task(card)
                    st.success(f"Задача '{card['title']}' успешно опубликована в общем каталоге на позиции рейтинга {card['rating']}!")


# ==========================================
# 2. ОБЩИЙ КАТАЛОГ ЗАДАЧ
# ==========================================
elif menu == "2. Общий каталог задач":
    st.markdown("<div class='main-title'>Общий каталог бизнес-задач</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Открытый пул подтвержденных задач с ранжированием по рейтингу готовности</div>", unsafe_allow_html=True)

    tasks = storage.load_tasks()

    # Filter section
    col_filter1, col_filter2, col_filter3 = st.columns([2, 1, 1])
    with col_filter1:
        search_query = st.text_input("Поиск по названию или тексту:", placeholder="Введите ключевое слово...")
    with col_filter2:
        filter_industry = st.selectbox("Отрасль:", ["Все отрасли"] + INDUSTRY_OPTIONS)
    with col_filter3:
        filter_level = st.selectbox("Уровень готовности:", ["Все уровни", "Приоритетная (90-100)", "Готовая (70-89)", "Рабочая (40-69)", "Черновик (0-39)"])

    filtered_tasks = []
    for t in tasks:
        if search_query:
            q = search_query.lower()
            in_title = q in t.get("title", "").lower()
            in_context = q in t.get("context_need", "").lower()
            if not (in_title or in_context):
                continue
        if filter_industry != "Все отрасли" and t.get("industry") != filter_industry:
            continue
        if filter_level != "Все уровни":
            level_name = filter_level.split(" ")[0]
            if t.get("readiness_level") != level_name:
                continue
        filtered_tasks.append(t)

    st.markdown(f"Всего задач в каталоге: **{len(filtered_tasks)}** (отсортированы по убыванию рейтинга)")

    for task in filtered_tasks:
        badge_cls = f"badge-{task.get('readiness_level', 'draft').lower()}"
        with st.container():
            st.markdown(f"""
            <div class='task-card-box'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                    <h3 style='margin:0; color:#1e293b;'>{task.get('title')}</h3>
                    <span class='badge {badge_cls}'>{task.get('readiness_level')} | {task.get('rating')} баллов</span>
                </div>
                <p style='color:#64748b; font-size:0.9rem; margin-bottom:12px;'>
                    Отрасль: <b>{task.get('industry')}</b> | Направление: <b>{task.get('task_type')}</b>
                </p>
                <p><b>Контекст и потребность:</b> {task.get('context_need')}</p>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("Подробная карточка задачи и критерии"):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown(f"**Данные и материалы:** {task.get('data_materials')}")
                    st.markdown(f"**Ожидаемый результат:** {task.get('expected_result')}")
                    st.markdown(f"**Критерии успеха:** {task.get('success_criteria')}")
                with col_d2:
                    st.markdown(f"**Ограничения:** {task.get('constraints')}")
                    st.markdown(f"**Пользователи:** {task.get('target_users')}")
                    st.markdown(f"**Связь с бизнесом:** {task.get('business_contact')}")

                props = storage.get_proposals_for_task(task.get("id"))
                st.caption(f"Подано предложений от студенческих команд: {len(props)}")


# ==========================================
# 3. КАБИНЕТ СТУДЕНЧЕСКОЙ КОМАНДЫ
# ==========================================
elif menu == "3. Кабинет студенческой команды":
    st.markdown("<div class='main-title'>Кабинет студенческой команды</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Персонализированные рекомендации, открытый выбор задач и подача предложений</div>", unsafe_allow_html=True)

    teams = storage.load_teams()
    team_names = [t["name"] for t in teams]
    selected_team_name = st.selectbox("Выберите активную команду:", team_names)
    team = next(t for t in teams if t["name"] == selected_team_name)

    # Team profile summary
    col_tp1, col_tp2, col_tp3 = st.columns([1, 2, 1])
    with col_tp1:
        st.metric("Баллы прогресса (XP):", f"{team.get('progress_points', 0)} XP")
    with col_tp2:
        st.markdown(f"**Интересы:** {', '.join(team.get('industry_interests', []))}")
        st.markdown(f"**Направления:** {', '.join(team.get('task_type_interests', []))}")
        st.markdown(f"**Навыки:** {', '.join(team.get('skills', []))}")
    with col_tp3:
        st.caption("Регламент: система может рекомендовать задачи по интересам, но не ограничивает каталог и не назначает команды автоматически.")

    st.markdown("---")
    st.subheader("Рекомендованные задачи для вашей команды")

    all_tasks = storage.load_tasks()
    ranked_tasks = []
    for t in all_tasks:
        rec_score, rec_explanation = calculate_recommendation_score(team, t)
        ranked_tasks.append({
            "task": t,
            "rec_score": rec_score,
            "rec_explanation": rec_explanation
        })
    ranked_tasks.sort(key=lambda x: (x["rec_score"], x["task"].get("rating", 0)), reverse=True)

    for item in ranked_tasks:
        t = item["task"]
        rec_score = item["rec_score"]
        rec_exp = item["rec_explanation"]

        badge_cls = f"badge-{t.get('readiness_level', 'draft').lower()}"
        with st.container():
            st.markdown(f"""
            <div class='recommendation-banner'>
                <b>{rec_exp}</b>
            </div>
            <div class='task-card-box'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                    <h4 style='margin:0;'>{t.get('title')}</h4>
                    <span class='badge {badge_cls}'>{t.get('readiness_level')} | {t.get('rating')} б.</span>
                </div>
                <p style='color:#475569; font-size:0.9rem;'>{t.get('context_need')}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Подача предложения (отклика) на задачу")

    task_choices = {t["id"]: f"{t['title']} (Рейтинг: {t['rating']} б.)" for t in all_tasks}
    selected_task_id = st.selectbox(
        "Выберите задачу для подачи предложения:",
        options=list(task_choices.keys()),
        format_func=lambda x: task_choices[x]
    )

    with st.form("proposal_form"):
        col_pr1, col_pr2 = st.columns(2)
        with col_pr1:
            idea_val = st.text_area(
                "Идея решения:",
                placeholder="Опишите архитектурную или алгоритмическую концепцию решения...",
                height=100
            )
            plan_val = st.text_area(
                "План реализации по этапам:",
                placeholder="Неделя 1: ..., Неделя 2: ..., Неделя 3: ...",
                height=100
            )
        with col_pr2:
            timeline_val = st.text_input("Ожидаемый срок реализации:", value="4 недели")
            proto_val = st.text_input("Ссылка на прототип / репозиторий:", placeholder="https://github.com/team/prototype")
            st.caption("Число предложений от одной команды не ограничивается.")

        submitted = st.form_submit_button("Отправить предложение бизнесу", type="primary")
        if submitted:
            if idea_val.strip() and plan_val.strip():
                new_prop = {
                    "id": f"prop-{datetime.now().strftime('%M%S')}",
                    "task_id": selected_task_id,
                    "team_id": team["id"],
                    "team_name": team["name"],
                    "solution_idea": idea_val.strip(),
                    "plan": plan_val.strip(),
                    "timeline": timeline_val.strip(),
                    "prototype_url": proto_val.strip(),
                    "status": "pending",
                    "submitted_at": datetime.now().isoformat(),
                    "review_comment": ""
                }
                storage.add_proposal(new_prop)
                st.success("Предложение успешно отправлено представителю бизнеса!")
            else:
                st.error("Пожалуйста, заполните идею решения и план реализации.")


# ==========================================
# 4. ОТКЛИКИ И РЕШЕНИЯ БИЗНЕСА
# ==========================================
elif menu == "4. Отклики и решения бизнеса":
    st.markdown("<div class='main-title'>Кабинет бизнеса: Отклики и Решения</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Сравнение поступивших предложений, ручной выбор команды и подтверждение этапов прогресса</div>", unsafe_allow_html=True)

    tasks = storage.load_tasks()
    proposals = storage.load_proposals()

    task_choices = {t["id"]: t["title"] for t in tasks}
    selected_task_id = st.selectbox(
        "Выберите задачу для просмотра откликов:",
        options=list(task_choices.keys()),
        format_func=lambda x: task_choices[x]
    )

    task_proposals = storage.get_proposals_for_task(selected_task_id)

    st.markdown(f"Всего поступивших предложений по выбранной задаче: **{len(task_proposals)}**")

    if not task_proposals:
        st.info("По данной задаче пока нет предложений от команд. Перейдите в кабинет студента для подачи отклика.")
    else:
        for p in task_proposals:
            status_text = "Ожидает решения" if p["status"] == "pending" else ("Команда выбрана" if p["status"] == "accepted" else "Отклонено")
            
            with st.container():
                st.markdown(f"""
                <div class='task-card-box'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <h4 style='margin:0;'>Команда: {p['team_name']}</h4>
                        <b>Статус: {status_text}</b>
                    </div>
                    <p><b>Идея решения:</b> {p['solution_idea']}</p>
                    <p><b>План:</b> {p['plan']}</p>
                    <p><b>Срок:</b> {p['timeline']} | <b>Прототип:</b> <a href='{p.get('prototype_url', '#')}' target='_blank'>{p.get('prototype_url', 'Не указан')}</a></p>
                </div>
                """, unsafe_allow_html=True)

                col_dec1, col_dec2, col_dec3 = st.columns([1, 1, 2])
                with col_dec1:
                    if st.button("Выбрать команду", key=f"accept_{p['id']}"):
                        storage.update_proposal_status(p["id"], "accepted", "Команда выбрана для реализации проекта.")
                        st.success(f"Команда '{p['team_name']}' выбрана для работы над задачей!")
                        st.rerun()
                with col_dec2:
                    if st.button("Отклонить", key=f"reject_{p['id']}"):
                        storage.update_proposal_status(p["id"], "rejected", "Спасибо за предложение. Выбрано альтернативное решение.")
                        st.warning(f"Предложение команды '{p['team_name']}' отклонено.")
                        st.rerun()
                with col_dec3:
                    if p.get("review_comment"):
                        st.caption(f"Комментарий бизнеса: {p['review_comment']}")

    st.markdown("---")
    st.subheader("Шаг 8: Контрольные этапы и начисление баллов прогресса")
    st.caption("После подтверждения этапа выбранная команда получает баллы за фактический прогресс (XP).")

    all_milestones = storage.get_milestones_for_task_team(selected_task_id, task_proposals[0]["team_id"]) if task_proposals else []
    if not all_milestones:
        # Load general milestones for task
        all_milestones = [m for m in storage.load_milestones() if m.get("task_id") == selected_task_id]

    if all_milestones:
        for m in all_milestones:
            col_m1, col_m2 = st.columns([3, 1])
            with col_m1:
                status_label = "Подтвержден" if m["status"] == "completed" else "В работе"
                st.markdown(f"- **{m['title']}** (+{m['points']} XP) — *{status_label}*")
            with col_m2:
                if m["status"] != "completed":
                    if st.button(f"Подтвердить этап (+{m['points']} XP)", key=f"m_btn_{m['id']}"):
                        storage.complete_milestone(m["id"])
                        st.success(f"Этап подтвержден! Команде начислено +{m['points']} XP.")
                        st.rerun()
    else:
        st.info("Контрольные этапы будут доступны после выбора команды.")


# ==========================================
# 5. ЭКСПРЕСС-ДЕМОНСТРАЦИЯ (ЖЮРИ)
# ==========================================
elif menu == "5. Экспресс-демонстрация (Жюри)":
    st.markdown("<div class='main-title'>Эталонный сквозной сценарий для защиты (до 5 минут)</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Пошаговое прохождение всех 8 этапов регламента хакатона на одном экране</div>", unsafe_allow_html=True)

    st.markdown("""
    В соответствии с пунктом 11 кейса:
    *«На защите участники вводят слабое описание бизнес-задачи, дополняют его и показывают рост рейтинга. Затем задача публикуется в общем каталоге, студенческая команда самостоятельно отправляет предложение, а бизнес вручную принимает или отклоняет отклик.»*
    """)

    st.markdown("---")
    st.markdown("### Сквозной маршрут демонстрации:")
    
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        st.markdown("**1. Исходный слабый черновик (Рейтинг: 20 баллов, Черновик):**")
        st.info("«Нужен умный чат-бот для поддержки клиентов интернет-магазина, чтобы разгрузить операторов»")

        st.markdown("**2. AI-интервьюер задает 3 уточняющих вопроса:**")
        st.markdown("- Данные: выгрузка 25 000 диалогов и FAQ.")
        st.markdown("- Критерии успеха: разрешение >65% обращений, точность >88%.")
        st.markdown("- Ограничения: 4 недели, FastAPI, Docker.")

    with col_demo2:
        st.markdown("**3. Рост рейтинга до 95 баллов (Приоритетная):**")
        st.success("Задача поднимается на 1-ю позицию в общем каталоге благодаря максимальной готовности ТЗ.")

        st.markdown("**4. Отклик и ручной выбор бизнеса:**")
        st.markdown("- Команда NeuralMinds отправляет предложение с RAG-архитектурой.")
        st.markdown("- Бизнес вручную нажимает 'Выбрать команду' и подтверждает этап (+35 XP).")

    if st.button("Запустить эталонную демонстрацию в конструкторе", type="primary"):
        st.session_state.draft_text = "Нужен умный чат-бот для поддержки клиентов интернет-магазина электроники, чтобы разгрузить операторов в пиковые часы."
        st.session_state.draft_industry = "Ритейл и e-commerce"
        st.session_state.draft_task_type = "Диалоговый AI и чат-боты"
        st.session_state.qa_history = [
            {
                "field_target": "data_materials",
                "question": "Какие конкретно исходные данные, примеры диалогов, документы или базы знаний вы готовы передать команде?",
                "answer": "Выгрузка 25 000 обезличенных диалогов в JSONL, база FAQ из 450 статей и каталог товаров в CSV."
            },
            {
                "field_target": "success_criteria",
                "question": "По каким измеримым метрикам и критериям вы будете оценивать успешность решения и принимать работу?",
                "answer": "Автоматическое разрешение не менее 65% типовых обращений, точность классификации от 88%, время ответа до 2 сек."
            },
            {
                "field_target": "constraints",
                "question": "Каковы жесткие ограничения по срокам, технологическому стеку, безопасности данных или интеграциям?",
                "answer": "Срок разработки 4 недели, стек Python/FastAPI, упаковка в Docker, соблюдение требований безопасности данных."
            }
        ]
        st.session_state.current_question = None
        st.session_state.active_card = None
        st.success("Данные для демонстрации загружены. Перейдите в раздел '1. Конструктор задачи (Бизнес)'.")
