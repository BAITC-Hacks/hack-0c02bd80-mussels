"""
UI Components for AI Sana platform.
Includes dynamic circular SVG speedometer for readiness score,
interactive milestone progress visualizer, and XP award cards.

STRICT REQUIREMENT: NO EMOJIS in any markup or text.
"""

from typing import Dict, Any, List
import math


def get_gauge_color_scheme(score: int) -> Dict[str, str]:
    """
    Returns color palette and metadata based on score:
    - 0-39: Red (Черновик)
    - 40-69: Amber/Yellow (Рабочая)
    - 70-89: Blue (Готовая)
    - 90-100: Emerald/Green (Приоритетная)
    """
    score = max(0, min(100, int(score)))

    if score >= 90:
        return {
            "level": "Приоритетная",
            "primary": "#10b981",       # emerald-500
            "secondary": "#059669",     # emerald-600
            "track": "#d1fae5",         # emerald-100
            "bg": "#ecfdf5",            # emerald-50
            "border": "#6ee7b7",        # emerald-300
            "text": "#065f46",          # emerald-800
            "badge_bg": "#dcfce7",
            "badge_text": "#15803d",
            "badge_border": "#86efac",
            "description": "Полная готовность к реализации"
        }
    elif score >= 70:
        return {
            "level": "Готовая",
            "primary": "#3b82f6",       # blue-500
            "secondary": "#2563eb",     # blue-600
            "track": "#dbeafe",         # blue-100
            "bg": "#eff6ff",            # blue-50
            "border": "#93c5fd",        # blue-300
            "text": "#1e40af",          # blue-800
            "badge_bg": "#dbeafe",
            "badge_text": "#1d4ed8",
            "badge_border": "#93c5fd",
            "description": "Высокая степень проработки"
        }
    elif score >= 40:
        return {
            "level": "Рабочая",
            "primary": "#f59e0b",       # amber-500
            "secondary": "#d97706",     # amber-600
            "track": "#fef3c7",         # amber-100
            "bg": "#fffbeb",            # amber-50
            "border": "#fde047",        # yellow-300
            "text": "#92400e",          # amber-800
            "badge_bg": "#fef9c3",
            "badge_text": "#a16207",
            "badge_border": "#fde047",
            "description": "Базовые требования указаны"
        }
    else:
        return {
            "level": "Черновик",
            "primary": "#ef4444",       # red-500
            "secondary": "#dc2626",     # red-600
            "track": "#fee2e2",         # red-100
            "bg": "#fef2f2",            # red-50
            "border": "#fca5a5",        # red-300
            "text": "#991b1b",          # red-800
            "badge_bg": "#fee2e2",
            "badge_text": "#b91c1c",
            "badge_border": "#fca5a5",
            "description": "Требует детализации"
        }


def render_circular_gauge(score: int, size: int = 140, compact: bool = False, title: str = "") -> str:
    """
    Renders an SVG circular speedometer (240-degree arc) for readiness score (0-100).
    Uses pure SVG/CSS without external dependencies.
    Strictly NO emojis.
    """
    score = max(0, min(100, int(score)))
    colors = get_gauge_color_scheme(score)

    if compact:
        # Compact version for catalog cards and recommendation list
        dim = size
        cx, cy = dim / 2, dim / 2
        r = (dim / 2) - 6
        circ = 2 * math.pi * r
        arc_angle = 240.0
        arc_len = circ * (arc_angle / 360.0)
        active_len = arc_len * (score / 100.0)

        grad_id = f"compact-grad-{score}-{size}"
        
        svg = f"""
        <div style="display:inline-flex; flex-direction:column; align-items:center; justify-content:center;">
            <svg width="{dim}" height="{dim}" viewBox="0 0 {dim} {dim}" style="overflow:visible;">
                <defs>
                    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="{colors['primary']}" />
                        <stop offset="100%" stop-color="{colors['secondary']}" />
                    </linearGradient>
                </defs>
                <!-- Background track -->
                <circle cx="{cx}" cy="{cy}" r="{r}"
                    fill="none"
                    stroke="#e2e8f0"
                    stroke-width="5"
                    stroke-dasharray="{arc_len:.2f} {circ:.2f}"
                    stroke-linecap="round"
                    transform="rotate(150 {cx} {cy})" />
                <!-- Active progress stroke -->
                <circle cx="{cx}" cy="{cy}" r="{r}"
                    fill="none"
                    stroke="url(#{grad_id})"
                    stroke-width="5"
                    stroke-dasharray="{max(0.1, active_len):.2f} {circ:.2f}"
                    stroke-linecap="round"
                    opacity="{1 if score > 0 else 0}"
                    transform="rotate(150 {cx} {cy})"
                    style="transition: stroke-dasharray 0.5s ease;" />
                <!-- Score text in center -->
                <text x="{cx}" y="{cy - 1}" text-anchor="middle" dominant-baseline="middle"
                    fill="{colors['text']}" font-family="system-ui, -apple-system, sans-serif"
                    font-size="{int(dim * 0.32)}px" font-weight="700">
                    {score}
                </text>
                <text x="{cx}" y="{cy + int(dim * 0.22)}" text-anchor="middle" dominant-baseline="middle"
                    fill="#64748b" font-family="system-ui, -apple-system, sans-serif"
                    font-size="{max(8, int(dim * 0.16))}px" font-weight="500">
                    /100
                </text>
            </svg>
        </div>
        """
        return svg.strip()

    # Large version for Constructor Step 3 and 4
    dim = size
    cx, cy = dim / 2, (dim / 2) - 4
    r = (dim / 2) - 16
    circ = 2 * math.pi * r
    arc_angle = 240.0
    arc_len = circ * (arc_angle / 360.0)
    active_len = arc_len * (score / 100.0)

    grad_id = f"large-grad-{score}-{size}"

    # Calculate tick coordinates for 0 and 100
    # Start angle: 150 deg (left), End angle: 390 / 30 deg (right)
    start_rad = math.radians(150)
    end_rad = math.radians(30)
    tick_r = r + 10
    x0 = cx + tick_r * math.cos(start_rad)
    y0 = cy + tick_r * math.sin(start_rad)
    x100 = cx + tick_r * math.cos(end_rad)
    y100 = cy + tick_r * math.sin(end_rad)

    svg = f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:18px; display:inline-flex; flex-direction:column; align-items:center; box-shadow:0 1px 3px rgba(0,0,0,0.05); min-width:180px;">
        {f'<div style="font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px;">{title}</div>' if title else ''}
        <svg width="{dim}" height="{int(dim * 0.88)}" viewBox="0 0 {dim} {int(dim * 0.88)}" style="overflow:visible;">
            <defs>
                <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{colors['primary']}" />
                    <stop offset="100%" stop-color="{colors['secondary']}" />
                </linearGradient>
                <filter id="glow-{score}" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="{colors['primary']}" flood-opacity="0.25"/>
                </filter>
            </defs>
            <!-- Background track -->
            <circle cx="{cx}" cy="{cy}" r="{r}"
                fill="none"
                stroke="#e2e8f0"
                stroke-width="11"
                stroke-dasharray="{arc_len:.2f} {circ:.2f}"
                stroke-linecap="round"
                transform="rotate(150 {cx} {cy})" />
            <!-- Active progress stroke -->
            <circle cx="{cx}" cy="{cy}" r="{r}"
                fill="none"
                stroke="url(#{grad_id})"
                stroke-width="11"
                stroke-dasharray="{max(0.1, active_len):.2f} {circ:.2f}"
                stroke-linecap="round"
                opacity="{1 if score > 0 else 0}"
                filter="url(#glow-{score})"
                transform="rotate(150 {cx} {cy})"
                style="transition: stroke-dasharray 0.6s cubic-bezier(0.4, 0, 0.2, 1);" />
            <!-- Min / Max scale markers -->
            <text x="{x0}" y="{y0 + 2}" text-anchor="middle" dominant-baseline="middle"
                fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif"
                font-size="11px" font-weight="600">0</text>
            <text x="{x100}" y="{y100 + 2}" text-anchor="middle" dominant-baseline="middle"
                fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif"
                font-size="11px" font-weight="600">100</text>
            <!-- Central score text -->
            <text x="{cx}" y="{cy - 5}" text-anchor="middle" dominant-baseline="middle"
                fill="{colors['text']}" font-family="system-ui, -apple-system, sans-serif"
                font-size="{int(dim * 0.26)}px" font-weight="800" letter-spacing="-0.5px">
                {score}
            </text>
            <text x="{cx}" y="{cy + int(dim * 0.14)}" text-anchor="middle" dominant-baseline="middle"
                fill="#64748b" font-family="system-ui, -apple-system, sans-serif"
                font-size="12px" font-weight="600">
                из 100 баллов
            </text>
        </svg>
        <div style="margin-top:2px; display:inline-block; padding:4px 12px; background:{colors['badge_bg']}; color:{colors['badge_text']}; border:1px solid {colors['badge_border']}; border-radius:6px; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
            {colors['level']}
        </div>
        <div style="font-size:0.75rem; color:#64748b; margin-top:4px; text-align:center;">
            {colors['description']}
        </div>
    </div>
    """
    return svg.strip()


def render_milestone_progress(milestones: List[Dict[str, Any]], team_name: str = "") -> str:
    """
    Renders an interactive milestone progress visualizer for the Business Cabinet.
    Calculates completed stages, total stages, percentage, earned XP.
    Strictly NO emojis.
    """
    total = len(milestones)
    if total == 0:
        return """
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:10px; padding:20px; color:#64748b; text-align:center;">
            Контрольные этапы еще не сформированы для данной задачи.
        </div>
        """.strip()

    completed = sum(1 for m in milestones if m.get("status") == "completed")
    pct = int(round((completed / total) * 100)) if total > 0 else 0
    earned_xp = sum(m.get("points", 0) for m in milestones if m.get("status") == "completed")
    total_xp = sum(m.get("points", 0) for m in milestones)

    # Color for progress bar based on percentage
    if pct == 100:
        bar_color = "linear-gradient(90deg, #10b981, #059669)"
        status_badge_bg = "#dcfce7"
        status_badge_text = "#15803d"
        status_label = "Все этапы завершены"
    elif pct >= 50:
        bar_color = "linear-gradient(90deg, #3b82f6, #2563eb)"
        status_badge_bg = "#dbeafe"
        status_badge_text = "#1d4ed8"
        status_label = "Активная реализация"
    else:
        bar_color = "linear-gradient(90deg, #f59e0b, #d97706)"
        status_badge_bg = "#fef9c3"
        status_badge_text = "#a16207"
        status_label = "Начальный этап"

    # Step indicators
    steps_html = []
    for i, m in enumerate(milestones, 1):
        is_done = m.get("status") == "completed"
        step_bg = "#10b981" if is_done else "#ffffff"
        step_border = "#059669" if is_done else "#cbd5e1"
        step_text_color = "#ffffff" if is_done else "#64748b"
        icon_or_num = "[V]" if is_done else str(i)
        stage_state = "Завершен" if is_done else "В работе"

        steps_html.append(f"""
        <div style="flex:1; display:flex; flex-direction:column; align-items:center; position:relative; min-width:80px; padding:0 4px;">
            <div style="width:28px; height:28px; border-radius:50%; background:{step_bg}; border:2px solid {step_border}; color:{step_text_color}; font-weight:700; font-size:0.75rem; display:flex; align-items:center; justify-content:center; margin-bottom:6px; box-shadow:0 1px 2px rgba(0,0,0,0.05);">
                {icon_or_num}
            </div>
            <div style="font-size:0.75rem; font-weight:600; color:{'#0f172a' if is_done else '#475569'}; text-align:center; line-height:1.2;">
                Этап {i}
            </div>
            <div style="font-size:0.7rem; color:{'#15803d' if is_done else '#94a3b8'}; text-align:center;">
                {stage_state} (+{m.get('points', 0)} XP)
            </div>
        </div>
        """)

    steps_row = "".join(steps_html)

    team_info = f"<span style='color:#0f172a; font-weight:600;'>{team_name}</span>" if team_name else "Выбранная команда"

    html = f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.04); margin-bottom:20px;">
        <!-- Header with summary stats -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
                <div style="font-size:0.8rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">
                    Шкала прогресса контрольных этапов
                </div>
                <div style="font-size:1.15rem; font-weight:700; color:#0f172a; margin-top:2px;">
                    {completed} из {total} этапов завершено ({pct}%)
                </div>
                <div style="font-size:0.85rem; color:#475569; margin-top:2px;">
                    Команда проекта: {team_info}
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="padding:6px 12px; background:{status_badge_bg}; color:{status_badge_text}; border-radius:6px; font-size:0.8rem; font-weight:600;">
                    {status_label}
                </div>
                <div style="padding:6px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; text-align:right;">
                    <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase;">Начислено XP</div>
                    <div style="font-size:1rem; font-weight:700; color:#0f172a;">{earned_xp} / {total_xp} XP</div>
                </div>
            </div>
        </div>

        <!-- Visual progress bar container -->
        <div style="background:#f1f5f9; border-radius:999px; height:12px; overflow:hidden; position:relative; margin-bottom:20px;">
            <div style="width:{pct}%; background:{bar_color}; height:100%; border-radius:999px; transition:width 0.6s ease;"></div>
        </div>

        <!-- Step-by-step nodes -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; border-top:1px solid #f1f5f9; padding-top:16px;">
            {steps_row}
        </div>
    </div>
    """
    return html.strip()


def render_xp_award_card(milestone: Dict[str, Any], task_title: str) -> str:
    """
    Renders an XP award card for a completed milestone in the Student Team Cabinet.
    Strictly NO emojis.
    """
    points = milestone.get("points", 25)
    title = milestone.get("title", "Контрольный этап")
    date_str = milestone.get("completed_at", "")
    if date_str and "T" in date_str:
        formatted_date = date_str.replace("T", " ")[:16]
    else:
        formatted_date = date_str or "Дата зафиксирована"

    return f"""
    <div style="background:#ffffff; border:1px solid #bbf7d0; border-left:4px solid #10b981; border-radius:8px; padding:14px 16px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
            <div style="flex:1;">
                <div style="font-size:0.75rem; font-weight:600; color:#15803d; text-transform:uppercase; letter-spacing:0.5px;">
                    Баллы прогресса подтверждены
                </div>
                <div style="font-size:0.95rem; font-weight:700; color:#0f172a; margin-top:2px;">
                    {title}
                </div>
                <div style="font-size:0.8rem; color:#475569; margin-top:4px;">
                    Задача: <b>{task_title}</b>
                </div>
            </div>
            <div style="display:flex; flex-direction:column; align-items:flex-end;">
                <span style="display:inline-block; padding:4px 10px; background:#dcfce7; color:#15803d; border:1px solid #86efac; border-radius:6px; font-size:0.9rem; font-weight:800;">
                    +{points} XP
                </span>
                <span style="font-size:0.7rem; color:#94a3b8; margin-top:6px;">
                    {formatted_date}
                </span>
            </div>
        </div>
    </div>
    """.strip()


def render_xp_pending_card(milestone: Dict[str, Any], task_title: str) -> str:
    """
    Renders an XP card for an in-progress milestone in the Student Team Cabinet.
    Strictly NO emojis.
    """
    points = milestone.get("points", 25)
    title = milestone.get("title", "Контрольный этап")

    return f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-left:4px solid #3b82f6; border-radius:8px; padding:14px 16px; margin-bottom:12px; box-shadow:0 1px 3px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
            <div style="flex:1;">
                <div style="font-size:0.75rem; font-weight:600; color:#2563eb; text-transform:uppercase; letter-spacing:0.5px;">
                    Этап в работе (Ожидает подтверждения)
                </div>
                <div style="font-size:0.95rem; font-weight:700; color:#0f172a; margin-top:2px;">
                    {title}
                </div>
                <div style="font-size:0.8rem; color:#475569; margin-top:4px;">
                    Задача: <b>{task_title}</b>
                </div>
            </div>
            <div style="display:flex; flex-direction:column; align-items:flex-end;">
                <span style="display:inline-block; padding:4px 10px; background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; border-radius:6px; font-size:0.85rem; font-weight:700;">
                    до +{points} XP
                </span>
                <span style="font-size:0.7rem; color:#64748b; margin-top:6px;">
                    В процессе
                </span>
            </div>
        </div>
    </div>
    """.strip()


def render_xp_summary(team: Dict[str, Any], milestones: List[Dict[str, Any]]) -> str:
    """
    Renders the overall XP summary panel for a student team.
    Strictly NO emojis.
    """
    total_xp = team.get("progress_points", 0)
    completed_milestones = sum(1 for m in milestones if m.get("status") == "completed")
    pending_milestones = sum(1 for m in milestones if m.get("status") != "completed")
    potential_xp = sum(m.get("points", 0) for m in milestones if m.get("status") != "completed")

    return f"""
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:12px; margin-bottom:18px;">
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size:0.75rem; color:#64748b; font-weight:600; text-transform:uppercase;">Баланс прогресса</div>
            <div style="font-size:1.6rem; font-weight:800; color:#0f172a; margin-top:4px;">{total_xp} XP</div>
            <div style="font-size:0.75rem; color:#15803d; margin-top:2px;">Подтвержденные очки команды</div>
        </div>
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size:0.75rem; color:#64748b; font-weight:600; text-transform:uppercase;">Завершено этапов</div>
            <div style="font-size:1.6rem; font-weight:800; color:#0f172a; margin-top:4px;">{completed_milestones}</div>
            <div style="font-size:0.75rem; color:#475569; margin-top:2px;">Контрольные точки приняты</div>
        </div>
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size:0.75rem; color:#64748b; font-weight:600; text-transform:uppercase;">Этапов в работе</div>
            <div style="font-size:1.6rem; font-weight:800; color:#0f172a; margin-top:4px;">{pending_milestones}</div>
            <div style="font-size:0.75rem; color:#2563eb; margin-top:2px;">Потенциал: +{potential_xp} XP</div>
        </div>
    </div>
    """.strip()
