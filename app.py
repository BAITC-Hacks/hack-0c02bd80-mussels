# Prototype: Three variants of the AI Sana platform design, switchable via ?variant= on existing routes.
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
    AIGenerator,
    VARIANT_CONFIGS,
    get_gauge_color_scheme,
    render_circular_gauge,
    render_milestone_progress,
    render_xp_award_card,
    render_xp_pending_card,
    render_xp_summary,
    render_prototype_switcher
)

# Page configuration
st.set_page_config(
    page_title="AI Sana: Платформа геймификации бизнес-задач",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Read active UI design variant from URL (?variant=A, B, or C)
current_variant = st.query_params.get("variant", "A").upper()
if current_variant not in ["A", "B", "C"]:
    current_variant = "A"

variant_cfg = VARIANT_CONFIGS[current_variant]

# Custom CSS for the active design variant (Strictly NO EMOJIS)
if current_variant == "B":
    st.markdown("""
    <style>
        .stApp { background-color: #fafafa; color: #18181b; }
        header[data-testid="stHeader"] { background-color: #fafafa; }
        section[data-testid="stSidebar"] { background-color: #f4f4f5; border-right: 1px solid #e4e4e7; }
        .main-title { font-size: 2.0rem; font-weight: 700; color: #18181b; margin-bottom: 0.2rem; letter-spacing: -0.5px; }
        .subtitle { font-size: 1.0rem; color: #71717a; margin-bottom: 1.4rem; }
        .task-card-box { background-color: #ffffff; border: 1px solid #e4e4e7; border-left: 4px solid #71717a; border-radius: 4px; padding: 18px 20px; margin-bottom: 16px; box-shadow: none; transition: border-color 0.2s ease; }
        .task-card-box:hover { border-color: #a1a1aa; border-left-color: #18181b; }
        .recommendation-banner { background-color: #f4f4f5; border: 1px solid #e4e4e7; border-left: 4px solid #047857; padding: 10px 14px; margin-bottom: 10px; border-radius: 4px; color: #047857; font-size: 0.9rem; }
        .score-card { background-color: #ffffff; border: 1px solid #e4e4e7; border-radius: 4px; padding: 14px; margin-bottom: 14px; }
    </style>
    """, unsafe_allow_html=True)
elif current_variant == "C":
    st.markdown("""
    <style>
        .stApp { background-color: #ffffff; color: #09090b; }
        header[data-testid="stHeader"] { background-color: #ffffff; }
        section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 2px solid #0f172a; }
        .main-title { font-size: 2.2rem; font-weight: 900; color: #09090b; margin-bottom: 0.25rem; letter-spacing: -1px; }
        .subtitle { font-size: 1.05rem; color: #334155; margin-bottom: 1.5rem; }
        .task-card-box { background-color: #ffffff; border: 2px solid #0f172a; border-radius: 8px; padding: 22px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(15, 23, 42, 0.08); transition: transform 0.15s ease, box-shadow 0.15s ease; }
        .task-card-box:hover { box-shadow: 0 8px 16px -2px rgba(15, 23, 42, 0.14); }
        .recommendation-banner { background-color: #0f172a; border: 1px solid #1e293b; padding: 12px 16px; margin-bottom: 12px; border-radius: 6px; color: #f8fafc; font-size: 0.9rem; }
        .score-card { background-color: #ffffff; border: 2px solid #0f172a; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp { background-color: #ffffff; color: #0f172a; }
        header[data-testid="stHeader"] { background-color: #ffffff; }
        section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
        .main-title { font-size: 2.1rem; font-weight: 800; color: #0f172a; margin-bottom: 0.25rem; letter-spacing: -0.5px; }
        .subtitle { font-size: 1.05rem; color: #475569; margin-bottom: 1.5rem; line-height: 1.5; }
        .task-card-box { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 22px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); transition: border-color 0.2s ease, box-shadow 0.2s ease; }
        .task-card-box:hover { border-color: #cbd5e1; box-shadow: 0 4px 10px -2px rgba(0,0,0,0.06); }
        .recommendation-banner { background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 4px solid #10b981; padding: 12px 16px; margin-bottom: 12px; border-radius: 6px; color: #15803d; font-size: 0.9rem; }
        .score-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 16px; }
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
st.sidebar.subheader("Прототип дизайна (UI / Цвета)")
selected_variant = st.sidebar.radio(
    "Вариант стиля UI:",
    options=["A", "B", "C"],
    index=["A", "B", "C"].index(current_variant),
    format_func=lambda x: f"{x}: {VARIANT_CONFIGS[x]['name']}"
)
if selected_variant != current_variant:
    st.query_params["variant"] = selected_variant
    st.rerun()

st.sidebar.caption(f"**{variant_cfg['full_name']}**")
st.sidebar.caption(variant_cfg["tagline"])

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

            # Top rating banner with dynamic circular SVG speedometer
            col_r1, col_r2 = st.columns([1, 2])
            with col_r1:
                gauge_html = render_circular_gauge(c_score, size=150, title="Рейтинг готовности", variant=current_variant)
                st.markdown(gauge_html, unsafe_allow_html=True)
            with col_r2:
                if current_variant == "B":
                    st.markdown("<div style='font-size:0.9rem; font-weight:700; color:#18181b; margin-bottom:8px;'>Факторы готовности ТЗ:</div>", unsafe_allow_html=True)
                    f_col1, f_col2 = st.columns(2)
                    idx = 0
                    for f_key, pts in c_breakdown.items():
                        target_col = f_col1 if idx % 2 == 0 else f_col2
                        max_pts = SCORING_WEIGHTS[f_key]["max_points"]
                        pct = int((pts / max_pts) * 100)
                        bar_bg = "#047857" if pts == max_pts else ("#b45309" if pts > 0 else "#e4e4e7")
                        target_col.markdown(
                            f"<div style='border-bottom:1px solid #e4e4e7; padding:4px 0; margin-bottom:6px;'>"
                            f"<div style='display:flex; justify-content:space-between; font-size:0.8rem;'>"
                            f"<span style='color:#18181b; font-weight:600;'>{SCORING_WEIGHTS[f_key]['title']}</span>"
                            f"<span style='color:#71717a; font-weight:700;'>{pts}/{max_pts} б.</span>"
                            f"</div>"
                            f"<div style='background:#f4f4f5; height:5px; border-radius:999px; margin-top:3px; overflow:hidden;'>"
                            f"<div style='width:{pct}%; height:100%; background:{bar_bg}; border-radius:999px;'></div>"
                            f"</div>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        idx += 1
                elif current_variant == "C":
                    st.markdown("<div style='font-size:0.95rem; font-weight:800; color:#09090b; margin-bottom:8px;'>ТЕЛЕМЕТРИЯ СКОРИНГА (ШВЕЙЦАРСКИЙ HUD):</div>", unsafe_allow_html=True)
                    breakdown_cols = st.columns(4)
                    idx = 0
                    for f_key, pts in c_breakdown.items():
                        col_idx = idx % 4
                        max_pts = SCORING_WEIGHTS[f_key]["max_points"]
                        is_full = pts == max_pts
                        chip_bg = "#064e3b" if is_full else ("#78350f" if pts > 0 else "#f1f5f9")
                        chip_text = "#ecfdf5" if is_full else ("#fef3c7" if pts > 0 else "#475569")
                        breakdown_cols[col_idx].markdown(
                            f"<div style='background:#ffffff; border:2px solid #0f172a; border-radius:6px; padding:8px; margin-bottom:8px;'>"
                            f"<div style='font-size:0.75rem; color:#475569; font-weight:700;'>{SCORING_WEIGHTS[f_key]['title']}</div>"
                            f"<div style='margin-top:4px;'><span style='display:inline-block; padding:2px 6px; background:{chip_bg}; color:{chip_text}; border-radius:4px; font-size:0.85rem; font-weight:800;'>{pts} / {max_pts}</span></div>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        idx += 1
                else:  # Variant A
                    st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:10px;'>Факторы начисления баллов:</div>", unsafe_allow_html=True)
                    breakdown_cols = st.columns(4)
                    idx = 0
                    for f_key, pts in c_breakdown.items():
                        col_idx = idx % 4
                        max_pts = SCORING_WEIGHTS[f_key]["max_points"]
                        is_full = pts == max_pts
                        val_color = "#15803d" if is_full else ("#b45309" if pts > 0 else "#64748b")
                        breakdown_cols[col_idx].markdown(
                            f"<div style='background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:10px; margin-bottom:8px; box-shadow:0 1px 2px rgba(0,0,0,0.02);'>"
                            f"<div style='font-size:0.75rem; color:#64748b; font-weight:600;'>{SCORING_WEIGHTS[f_key]['title']}</div>"
                            f"<div style='font-size:1.1rem; font-weight:800; color:{val_color}; margin-top:2px;'>{pts} <span style='font-size:0.75rem; font-weight:500; color:#94a3b8;'>/ {max_pts}</span></div>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
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
        task_rating = task.get("rating", 0)
        gauge_svg = render_circular_gauge(task_rating, size=58, compact=True, variant=current_variant)
        colors = get_gauge_color_scheme(task_rating, variant=current_variant)
        level_name = task.get("readiness_level", colors["level"])

        with st.container():
            if current_variant == "B":
                st.markdown(f"""
                <div class='task-card-box' style='border-left:4px solid {colors["primary"]};'>
                    <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:12px;'>
                        <div style='flex:1;'>
                            <div style='display:flex; align-items:center; gap:8px; margin-bottom:4px;'>
                                <span style='font-size:0.75rem; font-weight:700; color:{colors["text"]}; text-transform:uppercase;'>
                                    {level_name}
                                </span>
                                <span style='color:#a1a1aa;'>•</span>
                                <span style='font-size:0.8rem; color:#71717a;'>{task.get('industry')}</span>
                            </div>
                            <h3 style='margin:0 0 6px 0; color:#18181b; font-size:1.15rem; font-weight:700;'>{task.get('title')}</h3>
                            <p style='color:#52525b; font-size:0.9rem; line-height:1.4; margin:0;'>{task.get('context_need')}</p>
                        </div>
                        <div style='display:flex; align-items:center;'>
                            {gauge_svg}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif current_variant == "C":
                st.markdown(f"""
                <div class='task-card-box'>
                    <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:12px; border-bottom:1px solid #e2e8f0; padding-bottom:10px;'>
                        <div style='flex:1;'>
                            <div style='margin-bottom:6px;'>
                                <span style='display:inline-block; padding:3px 8px; background:{colors["badge_bg"]}; color:{colors["badge_text"]}; border-radius:4px; font-size:0.75rem; font-weight:800; text-transform:uppercase;'>
                                    {level_name}
                                </span>
                                <span style='font-size:0.8rem; color:#64748b; margin-left:8px;'>{task.get('task_type')}</span>
                            </div>
                            <h3 style='margin:0; color:#09090b; font-size:1.25rem; font-weight:900;'>{task.get('title')}</h3>
                        </div>
                        <div style='display:flex; align-items:center; gap:10px;'>
                            <div style='text-align:right;'>
                                <div style='font-size:1.1rem; font-weight:900; color:#09090b;'>{task_rating} <span style='font-size:0.75rem; color:#64748b;'>/100</span></div>
                                <div style='font-size:0.7rem; color:#64748b; text-transform:uppercase;'>Рейтинг ТЗ</div>
                            </div>
                            {gauge_svg}
                        </div>
                    </div>
                    <p style='color:#1e293b; font-size:0.95rem; line-height:1.5; margin:0;'><b>Потребность:</b> {task.get('context_need')}</p>
                </div>
                """, unsafe_allow_html=True)
            else:  # Variant A
                st.markdown(f"""
                <div class='task-card-box'>
                    <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:16px; margin-bottom:10px;'>
                        <div style='flex:1;'>
                            <h3 style='margin:0 0 6px 0; color:#0f172a; font-size:1.25rem; font-weight:700;'>{task.get('title')}</h3>
                            <p style='color:#64748b; font-size:0.85rem; margin:0 0 10px 0;'>
                                Отрасль: <b style='color:#334155;'>{task.get('industry')}</b> | Направление: <b style='color:#334155;'>{task.get('task_type')}</b>
                            </p>
                        </div>
                        <div style='display:flex; align-items:center; gap:12px;'>
                            <div style='text-align:right;'>
                                <span style='display:inline-block; padding:4px 10px; background:{colors["badge_bg"]}; color:{colors["badge_text"]}; border:1px solid {colors["badge_border"]}; border-radius:6px; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;'>
                                    {level_name}
                                </span>
                                <div style='font-size:0.75rem; color:#64748b; margin-top:3px;'>Рейтинг готовности</div>
                            </div>
                            {gauge_svg}
                        </div>
                    </div>
                    <p style='color:#334155; font-size:0.95rem; line-height:1.5; margin:0;'><b>Контекст и потребность:</b> {task.get('context_need')}</p>
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

    # Load all milestones for this team and task titles
    all_stored_milestones = storage.load_milestones()
    all_tasks_dict = {task_item["id"]: task_item["title"] for task_item in storage.load_tasks()}
    team_milestones = [m for m in all_stored_milestones if m.get("team_id") == team["id"]]

    # XP summary statistics
    st.markdown(render_xp_summary(team, team_milestones, variant=current_variant), unsafe_allow_html=True)

    # XP Cards Accordion/List
    with st.expander("Карточки начисления баллов прогресса (XP)", expanded=True):
        completed_m = [m for m in team_milestones if m.get("status") == "completed"]
        in_progress_m = [m for m in team_milestones if m.get("status") != "completed"]

        if not team_milestones:
            st.markdown(
                """
                <div style='background:#f8fafc; border:1px dashed #cbd5e1; border-radius:8px; padding:16px; color:#64748b; font-size:0.9rem;'>
                    У выбранной команды пока нет зафиксированных контрольных этапов. 
                    После того как представитель бизнеса примет ваше предложение и подтвердит выполнение контрольного этапа, здесь появятся именные карточки начисления XP.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            if completed_m:
                st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#15803d; text-transform:uppercase; margin-bottom:8px;'>Подтвержденные начисления:</div>", unsafe_allow_html=True)
                for cm in completed_m:
                    task_name = all_tasks_dict.get(cm.get("task_id"), "Бизнес-задача")
                    st.markdown(render_xp_award_card(cm, task_name, variant=current_variant), unsafe_allow_html=True)
            
            if in_progress_m:
                st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#2563eb; text-transform:uppercase; margin-top:12px; margin-bottom:8px;'>Этапы в процессе выполнения:</div>", unsafe_allow_html=True)
                for ipm in in_progress_m:
                    task_name = all_tasks_dict.get(ipm.get("task_id"), "Бизнес-задача")
                    st.markdown(render_xp_pending_card(ipm, task_name, variant=current_variant), unsafe_allow_html=True)

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
        t_rating = t.get("rating", 0)
        gauge_svg = render_circular_gauge(t_rating, size=52, compact=True, variant=current_variant)
        colors = get_gauge_color_scheme(t_rating, variant=current_variant)
        level_name = t.get("readiness_level", colors["level"])

        with st.container():
            st.markdown(f"""
            <div class='recommendation-banner'>
                <b>{rec_exp}</b>
            </div>
            <div class='task-card-box'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:8px;'>
                    <div>
                        <h4 style='margin:0 0 4px 0; color:#0f172a;'>{t.get('title')}</h4>
                        <span style='display:inline-block; padding:3px 8px; background:{colors["badge_bg"]}; color:{colors["badge_text"]}; border:1px solid {colors["badge_border"]}; border-radius:4px; font-size:0.75rem; font-weight:700; text-transform:uppercase;'>
                            {level_name}
                        </span>
                    </div>
                    {gauge_svg}
                </div>
                <p style='color:#475569; font-size:0.9rem; margin:0;'>{t.get('context_need')}</p>
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

    # Find accepted proposal or fallback to first proposal
    accepted_prop = next((p for p in task_proposals if p.get("status") == "accepted"), None)
    active_team_name = ""
    active_team_id = ""
    if accepted_prop:
        active_team_id = accepted_prop["team_id"]
        active_team_name = accepted_prop["team_name"]
    elif task_proposals:
        active_team_id = task_proposals[0]["team_id"]
        active_team_name = task_proposals[0]["team_name"]

    all_milestones = storage.get_milestones_for_task_team(selected_task_id, active_team_id) if active_team_id else []
    if not all_milestones:
        # Load general milestones for task
        all_milestones = [m for m in storage.load_milestones() if m.get("task_id") == selected_task_id]

    if all_milestones:
        # Interactive Milestone Progress Visualizer (percentage, bar, steps)
        st.markdown(render_milestone_progress(all_milestones, team_name=active_team_name, variant=current_variant), unsafe_allow_html=True)

        st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#0f172a; margin-top:14px; margin-bottom:10px;'>Контрольные точки и подтверждение выполнения:</div>", unsafe_allow_html=True)
        for m in all_milestones:
            is_completed = m.get("status") == "completed"
            border_color = "#86efac" if is_completed else "#cbd5e1"
            status_text = "Подтвержден бизнесом" if is_completed else "В процессе выполнения"
            status_color = "#15803d" if is_completed else "#2563eb"
            status_bg = "#dcfce7" if is_completed else "#eff6ff"
            date_info = f" | {m.get('completed_at', '')[:16].replace('T', ' ')}" if is_completed and m.get("completed_at") else ""

            col_card, col_action = st.columns([3, 1])
            with col_card:
                st.markdown(f"""
                <div style="background:#ffffff; border:1px solid {border_color}; border-left:4px solid {status_color}; border-radius:8px; padding:12px 16px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:0.95rem; font-weight:700; color:#0f172a;">{m['title']}</div>
                        <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">
                            Статус: <b style="color:{status_color};">{status_text}</b>{date_info}
                        </div>
                    </div>
                    <div>
                        <span style="display:inline-block; padding:4px 10px; background:{status_bg}; color:{status_color}; border-radius:6px; font-size:0.85rem; font-weight:800;">
                            +{m['points']} XP
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_action:
                if not is_completed:
                    if st.button(f"Подтвердить этап (+{m['points']} XP)", key=f"m_btn_{m['id']}", type="primary"):
                        storage.complete_milestone(m["id"])
                        st.success(f"Этап подтвержден! Команде начислено +{m['points']} XP.")
                        st.rerun()
                else:
                    st.caption("Баллы начислены")
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

# Floating prototype switcher bar at bottom of screen
st.markdown(render_prototype_switcher(current_variant), unsafe_allow_html=True)

