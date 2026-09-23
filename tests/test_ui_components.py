import re
import pytest
from services.ui_components import (
    get_gauge_color_scheme,
    render_circular_gauge,
    render_milestone_progress,
    render_xp_award_card,
    render_xp_pending_card,
    render_xp_summary
)

EMOJI_REGEX = re.compile(r"[\U00010000-\U0010ffff]", flags=re.UNICODE)


def test_gauge_color_scheme_ranges():
    # 0-39: Черновик (Red)
    c0 = get_gauge_color_scheme(0)
    c39 = get_gauge_color_scheme(39)
    assert c0["level"] == "Черновик"
    assert c39["level"] == "Черновик"
    assert "#ef4444" in c0["primary"]

    # 40-69: Рабочая (Amber)
    c40 = get_gauge_color_scheme(40)
    c69 = get_gauge_color_scheme(69)
    assert c40["level"] == "Рабочая"
    assert c69["level"] == "Рабочая"
    assert "#f59e0b" in c40["primary"]

    # 70-89: Готовая (Blue)
    c70 = get_gauge_color_scheme(70)
    c89 = get_gauge_color_scheme(89)
    assert c70["level"] == "Готовая"
    assert c89["level"] == "Готовая"
    assert "#3b82f6" in c70["primary"]

    # 90-100: Приоритетная (Emerald/Green)
    c90 = get_gauge_color_scheme(90)
    c100 = get_gauge_color_scheme(100)
    assert c90["level"] == "Приоритетная"
    assert c100["level"] == "Приоритетная"
    assert "#10b981" in c90["primary"]


def test_circular_gauge_rendering():
    # Test large gauge
    large_html = render_circular_gauge(95, size=150, title="Рейтинг готовности")
    assert "<svg" in large_html
    assert "95" in large_html
    assert "Приоритетная" in large_html
    assert "из 100 баллов" in large_html
    assert not EMOJI_REGEX.search(large_html)

    # Test compact gauge
    compact_html = render_circular_gauge(55, size=58, compact=True)
    assert "<svg" in compact_html
    assert "55" in compact_html
    assert "/100" in compact_html
    assert not EMOJI_REGEX.search(compact_html)


def test_milestone_progress_calculation():
    # 2 of 3 completed -> 66% (round(2/3*100) = 67%, or int(round(66.6)) = 67% or 66%)
    milestones = [
        {"id": "m1", "title": "Этап 1", "points": 25, "status": "completed", "completed_at": "2026-09-21T18:00:00"},
        {"id": "m2", "title": "Этап 2", "points": 35, "status": "completed", "completed_at": "2026-09-22T15:00:00"},
        {"id": "m3", "title": "Этап 3", "points": 40, "status": "in_progress", "completed_at": None}
    ]

    html = render_milestone_progress(milestones, team_name="NeuralMinds")
    assert "2 из 3 этапов завершено" in html
    assert "NeuralMinds" in html
    assert "60 / 100 XP" in html
    assert not EMOJI_REGEX.search(html)

    # Empty list
    empty_html = render_milestone_progress([])
    assert "еще не сформированы" in empty_html
    assert not EMOJI_REGEX.search(empty_html)


def test_xp_award_cards():
    completed_m = {
        "id": "m1",
        "title": "Архитектура микросервиса",
        "points": 35,
        "status": "completed",
        "completed_at": "2026-09-22T15:00:00"
    }
    card_html = render_xp_award_card(completed_m, "Умный чат-бот")
    assert "+35 XP" in card_html
    assert "Архитектура микросервиса" in card_html
    assert "Умный чат-бот" in card_html
    assert "2026-09-22 15:00" in card_html
    assert not EMOJI_REGEX.search(card_html)

    pending_m = {
        "id": "m2",
        "title": "Финальный деплой",
        "points": 40,
        "status": "in_progress",
        "completed_at": None
    }
    pending_html = render_xp_pending_card(pending_m, "Умный чат-бот")
    assert "+40 XP" in pending_html
    assert "Финальный деплой" in pending_html
    assert not EMOJI_REGEX.search(pending_html)


def test_xp_summary():
    team = {"progress_points": 120}
    milestones = [
        {"status": "completed", "points": 25},
        {"status": "completed", "points": 35},
        {"status": "in_progress", "points": 40}
    ]
    summary_html = render_xp_summary(team, milestones)
    assert "120 XP" in summary_html
    assert "2" in summary_html
    assert "+40 XP" in summary_html
    assert not EMOJI_REGEX.search(summary_html)


def test_prototype_variants_and_switcher():
    from services.ui_components import VARIANT_CONFIGS, render_prototype_switcher

    assert "A" in VARIANT_CONFIGS
    assert "B" in VARIANT_CONFIGS
    assert "C" in VARIANT_CONFIGS

    for v_code in ["A", "B", "C"]:
        switcher_html = render_prototype_switcher(v_code)
        assert f"?variant=" in switcher_html
        assert not EMOJI_REGEX.search(switcher_html)

        gauge_b = render_circular_gauge(85, size=140, variant=v_code)
        assert "<svg" in gauge_b
        assert not EMOJI_REGEX.search(gauge_b)

        m_progress = render_milestone_progress([
            {"id": "m1", "title": "Этап 1", "points": 25, "status": "completed"}
        ], variant=v_code)
        assert not EMOJI_REGEX.search(m_progress)

