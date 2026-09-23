"""
UI Components and Design Prototypes for AI Sana platform.
Supports 3 radically different UI and coloring variants:
- Variant A: Executive Clean (Deep Slate & Sapphire)
- Variant B: Nordic Minimal (Graphite & Forest Sage)
- Variant C: Swiss Enterprise HUD (High-Contrast Cobalt & Dark Chips)

STRICT REQUIREMENT: NO EMOJIS in any markup or text.
"""

from typing import Dict, Any, List
import math

VARIANT_CONFIGS: Dict[str, Dict[str, Any]] = {
    "A": {
        "code": "A",
        "name": "Modern Fintech SaaS",
        "full_name": "Modern Fintech (Slate & Electric Indigo)",
        "tagline": "Высокотехнологичный enterprise-стиль: плавные тени, округлые формы 12px, акцентный индиго и чистый белый холст",
        "app_bg": "#f8fafc",
        "sidebar_bg": "#ffffff",
        "card_bg": "#ffffff",
        "card_border": "#e2e8f0",
        "card_radius": "12px",
        "card_shadow": "0 4px 20px -2px rgba(15, 23, 42, 0.05)",
        "accent": "#4f46e5",
        "text_primary": "#0f172a",
        "text_secondary": "#475569",
        "colors": {
            "priority": {
                "level": "Приоритетная",
                "primary": "#10b981",
                "secondary": "#059669",
                "track": "#d1fae5",
                "bg": "#ecfdf5",
                "border": "#86efac",
                "text": "#065f46",
                "badge_bg": "#dcfce7",
                "badge_text": "#15803d",
                "badge_border": "#86efac",
                "description": "Полная готовность к реализации"
            },
            "ready": {
                "level": "Готовая",
                "primary": "#3b82f6",
                "secondary": "#2563eb",
                "track": "#dbeafe",
                "bg": "#eff6ff",
                "border": "#93c5fd",
                "text": "#1e40af",
                "badge_bg": "#dbeafe",
                "badge_text": "#1d4ed8",
                "badge_border": "#93c5fd",
                "description": "Высокая степень проработки"
            },
            "workable": {
                "level": "Рабочая",
                "primary": "#f59e0b",
                "secondary": "#d97706",
                "track": "#fef3c7",
                "bg": "#fffbeb",
                "border": "#fde047",
                "text": "#92400e",
                "badge_bg": "#fef9c3",
                "badge_text": "#a16207",
                "badge_border": "#fde047",
                "description": "Базовые требования указаны"
            },
            "draft": {
                "level": "Черновик",
                "primary": "#ef4444",
                "secondary": "#dc2626",
                "track": "#fee2e2",
                "bg": "#fef2f2",
                "border": "#fca5a5",
                "text": "#991b1b",
                "badge_bg": "#fee2e2",
                "badge_text": "#b91c1c",
                "badge_border": "#fca5a5",
                "description": "Требует детализации"
            }
        }
    },
    "B": {
        "code": "B",
        "name": "Скандинавская Бумага",
        "full_name": "Скандинавская Бумага (Warm Editorial & Forest Pine)",
        "tagline": "Теплый редакционный стиль: благородная бумага слоновой кости, антиквенные заголовки с засечками и хвойный акцент",
        "app_bg": "#f5f2eb",
        "sidebar_bg": "#ebe6dc",
        "card_bg": "#ffffff",
        "card_border": "#ddd6c8",
        "card_radius": "6px",
        "card_shadow": "0 2px 10px rgba(30, 58, 43, 0.05)",
        "accent": "#1e3a2b",
        "text_primary": "#262624",
        "text_secondary": "#57534e",
        "colors": {
            "priority": {
                "level": "Приоритетная",
                "primary": "#047857",
                "secondary": "#065f46",
                "track": "#ecfdf5",
                "bg": "#f0fdf4",
                "border": "#bbf7d0",
                "text": "#064e3b",
                "badge_bg": "#f0fdf4",
                "badge_text": "#064e3b",
                "badge_border": "#bbf7d0",
                "description": "Полная готовность к реализации"
            },
            "ready": {
                "level": "Готовая",
                "primary": "#0284c7",
                "secondary": "#0369a1",
                "track": "#f0f9ff",
                "bg": "#f0f9ff",
                "border": "#bae6fd",
                "text": "#0c4a6e",
                "badge_bg": "#f0f9ff",
                "badge_text": "#0c4a6e",
                "badge_border": "#bae6fd",
                "description": "Высокая степень проработки"
            },
            "workable": {
                "level": "Рабочая",
                "primary": "#b45309",
                "secondary": "#92400e",
                "track": "#fffbeb",
                "bg": "#fffbeb",
                "border": "#fde68a",
                "text": "#78350f",
                "badge_bg": "#fffbeb",
                "badge_text": "#78350f",
                "badge_border": "#fde68a",
                "description": "Базовые требования указаны"
            },
            "draft": {
                "level": "Черновик",
                "primary": "#9f1239",
                "secondary": "#881337",
                "track": "#fff1f2",
                "bg": "#fff1f2",
                "border": "#fecdd3",
                "text": "#881337",
                "badge_bg": "#fff1f2",
                "badge_text": "#881337",
                "badge_border": "#fecdd3",
                "description": "Требует детализации"
            }
        }
    },
    "C": {
        "code": "C",
        "name": "Швейцарский Neo-Brutalist HUD",
        "full_name": "Швейцарский HUD (High-Contrast & Jet Black)",
        "tagline": "Бескомпромиссная геометрия: четкие черные рамки 2.5px, жесткие тени 6px, плотный монохром и неоновые индикаторы",
        "app_bg": "#ffffff",
        "sidebar_bg": "#ffffff",
        "card_bg": "#ffffff",
        "card_border": "#000000",
        "card_radius": "2px",
        "card_shadow": "6px 6px 0px #000000",
        "accent": "#000000",
        "text_primary": "#000000",
        "text_secondary": "#18181b",
        "colors": {
            "priority": {
                "level": "Приоритетная",
                "primary": "#10b981",
                "secondary": "#059669",
                "track": "#000000",
                "bg": "#ffffff",
                "border": "#000000",
                "text": "#000000",
                "badge_bg": "#000000",
                "badge_text": "#34d399",
                "badge_border": "#000000",
                "description": "Полная готовность к реализации"
            },
            "ready": {
                "level": "Готовая",
                "primary": "#2563eb",
                "secondary": "#1d4ed8",
                "track": "#000000",
                "bg": "#ffffff",
                "border": "#000000",
                "text": "#000000",
                "badge_bg": "#000000",
                "badge_text": "#60a5fa",
                "badge_border": "#000000",
                "description": "Высокая степень проработки"
            },
            "workable": {
                "level": "Рабочая",
                "primary": "#f59e0b",
                "secondary": "#d97706",
                "track": "#000000",
                "bg": "#ffffff",
                "border": "#000000",
                "text": "#000000",
                "badge_bg": "#000000",
                "badge_text": "#fbbf24",
                "badge_border": "#000000",
                "description": "Базовые требования указаны"
            },
            "draft": {
                "level": "Черновик",
                "primary": "#ef4444",
                "secondary": "#b91c1c",
                "track": "#000000",
                "bg": "#ffffff",
                "border": "#000000",
                "text": "#000000",
                "badge_bg": "#000000",
                "badge_text": "#f87171",
                "badge_border": "#000000",
                "description": "Требует детализации"
            }
        }
    }
}


def get_gauge_color_scheme(score: int, variant: str = "A") -> Dict[str, str]:
    """
    Returns color palette and metadata based on score and active design variant:
    - 0-39: Черновик
    - 40-69: Рабочая
    - 70-89: Готовая
    - 90-100: Приоритетная
    """
    score = max(0, min(100, int(score)))
    v_key = variant.upper() if variant.upper() in VARIANT_CONFIGS else "A"
    cfg = VARIANT_CONFIGS[v_key]["colors"]

    if score >= 90:
        return cfg["priority"]
    elif score >= 70:
        return cfg["ready"]
    elif score >= 40:
        return cfg["workable"]
    else:
        return cfg["draft"]


def render_circular_gauge(score: int, size: int = 140, compact: bool = False, title: str = "", variant: str = "A") -> str:
    """
    Renders an SVG circular speedometer for readiness score (0-100).
    Uses pure SVG/CSS without external dependencies.
    Strictly NO emojis.
    """
    score = max(0, min(100, int(score)))
    v_key = variant.upper() if variant.upper() in VARIANT_CONFIGS else "A"
    colors = get_gauge_color_scheme(score, variant=v_key)

    if compact:
        dim = size
        cx, cy = dim / 2, dim / 2
        r = (dim / 2) - 6
        circ = 2 * math.pi * r
        arc_angle = 240.0
        arc_len = circ * (arc_angle / 360.0)
        active_len = arc_len * (score / 100.0)
        grad_id = f"compact-grad-{v_key}-{score}-{size}"

        track_stroke = "#e2e8f0" if v_key != "C" else "#334155"
        stroke_w = 5 if v_key != "C" else 6

        svg = f"""
        <div style="display:inline-flex; flex-direction:column; align-items:center; justify-content:center;">
            <svg width="{dim}" height="{dim}" viewBox="0 0 {dim} {dim}" style="overflow:visible;">
                <defs>
                    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="{colors['primary']}" />
                        <stop offset="100%" stop-color="{colors['secondary']}" />
                    </linearGradient>
                </defs>
                <circle cx="{cx}" cy="{cy}" r="{r}"
                    fill="none"
                    stroke="{track_stroke}"
                    stroke-width="{stroke_w}"
                    stroke-dasharray="{arc_len:.2f} {circ:.2f}"
                    stroke-linecap="round"
                    transform="rotate(150 {cx} {cy})" />
                <circle cx="{cx}" cy="{cy}" r="{r}"
                    fill="none"
                    stroke="url(#{grad_id})"
                    stroke-width="{stroke_w}"
                    stroke-dasharray="{max(0.1, active_len):.2f} {circ:.2f}"
                    stroke-linecap="round"
                    opacity="{1 if score > 0 else 0}"
                    transform="rotate(150 {cx} {cy})"
                    style="transition: stroke-dasharray 0.5s ease;" />
                <text x="{cx}" y="{cy - 1}" text-anchor="middle" dominant-baseline="middle"
                    fill="{colors['text']}" font-family="system-ui, -apple-system, sans-serif"
                    font-size="{int(dim * 0.32)}px" font-weight="800">
                    {score}
                </text>
                <text x="{cx}" y="{cy + int(dim * 0.22)}" text-anchor="middle" dominant-baseline="middle"
                    fill="#64748b" font-family="system-ui, -apple-system, sans-serif"
                    font-size="{max(8, int(dim * 0.16))}px" font-weight="600">
                    /100
                </text>
            </svg>
        </div>
        """
        return svg.strip()

    # Large version
    dim = size
    cx, cy = dim / 2, (dim / 2) - 4
    r = (dim / 2) - 16
    circ = 2 * math.pi * r
    arc_angle = 240.0
    arc_len = circ * (arc_angle / 360.0)
    active_len = arc_len * (score / 100.0)
    grad_id = f"large-grad-{v_key}-{score}-{size}"

    start_rad = math.radians(150)
    end_rad = math.radians(30)
    tick_r = r + 10
    x0 = cx + tick_r * math.cos(start_rad)
    y0 = cy + tick_r * math.sin(start_rad)
    x100 = cx + tick_r * math.cos(end_rad)
    y100 = cy + tick_r * math.sin(end_rad)

    # Box styles per variant
    if v_key == "B":
        box_style = "background:#ffffff; border:1px solid #e4e4e7; border-radius:6px; padding:16px; display:inline-flex; flex-direction:column; align-items:center; min-width:180px;"
    elif v_key == "C":
        box_style = "background:#ffffff; border:2px solid #0f172a; border-radius:8px; padding:18px; display:inline-flex; flex-direction:column; align-items:center; box-shadow:0 4px 6px -1px rgba(15, 23, 42, 0.08); min-width:180px;"
    else:
        box_style = "background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:18px; display:inline-flex; flex-direction:column; align-items:center; box-shadow:0 1px 3px rgba(0,0,0,0.05); min-width:180px;"

    track_stroke = "#e2e8f0" if v_key != "C" else "#cbd5e1"
    stroke_w = 11 if v_key != "C" else 13

    svg = f"""
    <div style="{box_style}">
        {f'<div style="font-size:0.85rem; font-weight:700; color:#334155; margin-bottom:6px; text-transform:uppercase; letter-spacing:0.5px;">{title}</div>' if title else ''}
        <svg width="{dim}" height="{int(dim * 0.88)}" viewBox="0 0 {dim} {int(dim * 0.88)}" style="overflow:visible;">
            <defs>
                <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{colors['primary']}" />
                    <stop offset="100%" stop-color="{colors['secondary']}" />
                </linearGradient>
                <filter id="glow-{v_key}-{score}" x="-20%" y="-20%" width="140%" height="140%">
                    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="{colors['primary']}" flood-opacity="0.25"/>
                </filter>
            </defs>
            <circle cx="{cx}" cy="{cy}" r="{r}"
                fill="none"
                stroke="{track_stroke}"
                stroke-width="{stroke_w}"
                stroke-dasharray="{arc_len:.2f} {circ:.2f}"
                stroke-linecap="round"
                transform="rotate(150 {cx} {cy})" />
            <circle cx="{cx}" cy="{cy}" r="{r}"
                fill="none"
                stroke="url(#{grad_id})"
                stroke-width="{stroke_w}"
                stroke-dasharray="{max(0.1, active_len):.2f} {circ:.2f}"
                stroke-linecap="round"
                opacity="{1 if score > 0 else 0}"
                filter="url(#glow-{v_key}-{score})"
                transform="rotate(150 {cx} {cy})"
                style="transition: stroke-dasharray 0.6s cubic-bezier(0.4, 0, 0.2, 1);" />
            <text x="{x0}" y="{y0 + 2}" text-anchor="middle" dominant-baseline="middle"
                fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif"
                font-size="11px" font-weight="700">0</text>
            <text x="{x100}" y="{y100 + 2}" text-anchor="middle" dominant-baseline="middle"
                fill="#94a3b8" font-family="system-ui, -apple-system, sans-serif"
                font-size="11px" font-weight="700">100</text>
            <text x="{cx}" y="{cy - 5}" text-anchor="middle" dominant-baseline="middle"
                fill="{colors['text']}" font-family="system-ui, -apple-system, sans-serif"
                font-size="{int(dim * 0.27)}px" font-weight="800" letter-spacing="-0.5px">
                {score}
            </text>
            <text x="{cx}" y="{cy + int(dim * 0.14)}" text-anchor="middle" dominant-baseline="middle"
                fill="#64748b" font-family="system-ui, -apple-system, sans-serif"
                font-size="12px" font-weight="600">
                из 100 баллов
            </text>
        </svg>
        <div style="margin-top:4px; display:inline-block; padding:4px 12px; background:{colors['badge_bg']}; color:{colors['badge_text']}; border:1px solid {colors['badge_border']}; border-radius:6px; font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">
            {colors['level']}
        </div>
        <div style="font-size:0.75rem; color:#64748b; margin-top:4px; text-align:center;">
            {colors['description']}
        </div>
    </div>
    """
    return svg.strip()


def render_milestone_progress(milestones: List[Dict[str, Any]], team_name: str = "", variant: str = "A") -> str:
    """
    Renders an interactive milestone progress visualizer for the Business Cabinet.
    Strictly NO emojis.
    """
    v_key = variant.upper() if variant.upper() in VARIANT_CONFIGS else "A"
    total = len(milestones)
    if total == 0:
        return """
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:18px; color:#64748b; text-align:center;">
            Контрольные этапы еще не сформированы для данной задачи.
        </div>
        """.strip()

    completed = sum(1 for m in milestones if m.get("status") == "completed")
    pct = int(round((completed / total) * 100)) if total > 0 else 0
    earned_xp = sum(m.get("points", 0) for m in milestones if m.get("status") == "completed")
    total_xp = sum(m.get("points", 0) for m in milestones)

    if pct == 100:
        bar_color = "linear-gradient(90deg, #10b981, #059669)"
        status_badge_bg = "#dcfce7" if v_key != "C" else "#064e3b"
        status_badge_text = "#15803d" if v_key != "C" else "#ecfdf5"
        status_label = "Все этапы завершены"
    elif pct >= 50:
        bar_color = "linear-gradient(90deg, #3b82f6, #2563eb)"
        status_badge_bg = "#dbeafe" if v_key != "C" else "#1e3a8a"
        status_badge_text = "#1d4ed8" if v_key != "C" else "#eff6ff"
        status_label = "Активная реализация"
    else:
        bar_color = "linear-gradient(90deg, #f59e0b, #d97706)"
        status_badge_bg = "#fef9c3" if v_key != "C" else "#78350f"
        status_badge_text = "#a16207" if v_key != "C" else "#fef3c7"
        status_label = "Начальный этап"

    steps_html = []
    for i, m in enumerate(milestones, 1):
        is_done = m.get("status") == "completed"
        if v_key == "B":
            step_bg = "#047857" if is_done else "#ffffff"
            step_border = "#047857" if is_done else "#d4d4d8"
            step_text = "#ffffff" if is_done else "#71717a"
        elif v_key == "C":
            step_bg = "#0f172a" if is_done else "#ffffff"
            step_border = "#0f172a" if is_done else "#cbd5e1"
            step_text = "#38bdf8" if is_done else "#0f172a"
        else:
            step_bg = "#10b981" if is_done else "#ffffff"
            step_border = "#059669" if is_done else "#cbd5e1"
            step_text = "#ffffff" if is_done else "#64748b"

        icon_or_num = "[V]" if is_done else str(i)
        stage_state = "Завершен" if is_done else "В работе"

        steps_html.append(f"""
        <div style="flex:1; display:flex; flex-direction:column; align-items:center; position:relative; min-width:80px; padding:0 4px;">
            <div style="width:28px; height:28px; border-radius:50%; background:{step_bg}; border:2px solid {step_border}; color:{step_text}; font-weight:800; font-size:0.75rem; display:flex; align-items:center; justify-content:center; margin-bottom:6px;">
                {icon_or_num}
            </div>
            <div style="font-size:0.75rem; font-weight:700; color:#0f172a; text-align:center; line-height:1.2;">
                Этап {i}
            </div>
            <div style="font-size:0.7rem; color:{'#15803d' if is_done else '#94a3b8'}; text-align:center; margin-top:2px;">
                {stage_state} (+{m.get('points', 0)} XP)
            </div>
        </div>
        """)

    steps_row = "".join(steps_html)
    team_info = f"<span style='color:#0f172a; font-weight:700;'>{team_name}</span>" if team_name else "Выбранная команда"

    if v_key == "B":
        container_style = "background:#ffffff; border:1px solid #e4e4e7; border-radius:4px; padding:18px; margin-bottom:18px;"
    elif v_key == "C":
        container_style = "background:#ffffff; border:2px solid #0f172a; border-radius:8px; padding:20px; box-shadow:0 4px 6px -1px rgba(15, 23, 42, 0.08); margin-bottom:20px;"
    else:
        container_style = "background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:20px; box-shadow:0 1px 4px rgba(0,0,0,0.04); margin-bottom:20px;"

    return f"""
    <div style="{container_style}">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
            <div>
                <div style="font-size:0.8rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">
                    Шкала прогресса контрольных этапов
                </div>
                <div style="font-size:1.2rem; font-weight:800; color:#0f172a; margin-top:2px;">
                    {completed} из {total} этапов завершено ({pct}%)
                </div>
                <div style="font-size:0.85rem; color:#475569; margin-top:2px;">
                    Команда проекта: {team_info}
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="padding:6px 12px; background:{status_badge_bg}; color:{status_badge_text}; border-radius:6px; font-size:0.8rem; font-weight:700;">
                    {status_label}
                </div>
                <div style="padding:6px 14px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; text-align:right;">
                    <div style="font-size:0.7rem; color:#64748b; text-transform:uppercase; font-weight:600;">Начислено XP</div>
                    <div style="font-size:1rem; font-weight:800; color:#0f172a;">{earned_xp} / {total_xp} XP</div>
                </div>
            </div>
        </div>

        <div style="background:#f1f5f9; border-radius:999px; height:12px; overflow:hidden; position:relative; margin-bottom:20px;">
            <div style="width:{pct}%; background:{bar_color}; height:100%; border-radius:999px; transition:width 0.6s ease;"></div>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:flex-start; border-top:1px solid #f1f5f9; padding-top:16px;">
            {steps_row}
        </div>
    </div>
    """.strip()


def render_xp_award_card(milestone: Dict[str, Any], task_title: str, variant: str = "A") -> str:
    """
    Renders an XP award card for a completed milestone in the Student Team Cabinet.
    Strictly NO emojis.
    """
    v_key = variant.upper() if variant.upper() in VARIANT_CONFIGS else "A"
    points = milestone.get("points", 25)
    title = milestone.get("title", "Контрольный этап")
    date_str = milestone.get("completed_at", "")
    formatted_date = date_str.replace("T", " ")[:16] if date_str and "T" in date_str else (date_str or "Дата зафиксирована")

    if v_key == "B":
        return f"""
        <div style="background:#ffffff; border:1px solid #e4e4e7; border-left:4px solid #047857; border-radius:4px; padding:12px 16px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
                <div>
                    <div style="font-size:0.75rem; font-weight:700; color:#047857; text-transform:uppercase;">Баллы подтверждены</div>
                    <div style="font-size:0.95rem; font-weight:700; color:#18181b; margin-top:2px;">{title}</div>
                    <div style="font-size:0.8rem; color:#71717a; margin-top:3px;">Задача: {task_title}</div>
                </div>
                <div style="text-align:right;">
                    <span style="display:inline-block; padding:3px 8px; background:#f0fdf4; color:#064e3b; border:1px solid #bbf7d0; border-radius:4px; font-size:0.85rem; font-weight:700;">
                        +{points} XP
                    </span>
                    <div style="font-size:0.7rem; color:#a1a1aa; margin-top:4px;">{formatted_date}</div>
                </div>
            </div>
        </div>
        """.strip()
    elif v_key == "C":
        return f"""
        <div style="background:#ffffff; border:2px solid #0f172a; border-radius:6px; padding:14px 18px; margin-bottom:12px; box-shadow:0 2px 4px rgba(15, 23, 42, 0.05);">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
                <div>
                    <span style="display:inline-block; padding:2px 8px; background:#064e3b; color:#ecfdf5; border-radius:4px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">
                        Подтверждено
                    </span>
                    <div style="font-size:1rem; font-weight:800; color:#09090b; margin-top:4px;">{title}</div>
                    <div style="font-size:0.85rem; color:#475569; margin-top:2px;">Задача: <b>{task_title}</b></div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.2rem; font-weight:900; color:#059669;">+{points} XP</div>
                    <div style="font-size:0.7rem; color:#64748b; margin-top:2px;">{formatted_date}</div>
                </div>
            </div>
        </div>
        """.strip()
    else:
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


def render_xp_pending_card(milestone: Dict[str, Any], task_title: str, variant: str = "A") -> str:
    """
    Renders an XP card for an in-progress milestone.
    Strictly NO emojis.
    """
    v_key = variant.upper() if variant.upper() in VARIANT_CONFIGS else "A"
    points = milestone.get("points", 25)
    title = milestone.get("title", "Контрольный этап")

    if v_key == "B":
        return f"""
        <div style="background:#ffffff; border:1px solid #e4e4e7; border-left:4px solid #0284c7; border-radius:4px; padding:12px 16px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
                <div>
                    <div style="font-size:0.75rem; font-weight:700; color:#0284c7; text-transform:uppercase;">В процессе</div>
                    <div style="font-size:0.95rem; font-weight:700; color:#18181b; margin-top:2px;">{title}</div>
                    <div style="font-size:0.8rem; color:#71717a; margin-top:3px;">Задача: {task_title}</div>
                </div>
                <div style="text-align:right;">
                    <span style="display:inline-block; padding:3px 8px; background:#f0f9ff; color:#0c4a6e; border:1px solid #bae6fd; border-radius:4px; font-size:0.85rem; font-weight:700;">
                        до +{points} XP
                    </span>
                </div>
            </div>
        </div>
        """.strip()
    elif v_key == "C":
        return f"""
        <div style="background:#ffffff; border:2px solid #334155; border-radius:6px; padding:14px 18px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
                <div>
                    <span style="display:inline-block; padding:2px 8px; background:#1e3a8a; color:#eff6ff; border-radius:4px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">
                        В работе
                    </span>
                    <div style="font-size:1rem; font-weight:800; color:#09090b; margin-top:4px;">{title}</div>
                    <div style="font-size:0.85rem; color:#475569; margin-top:2px;">Задача: <b>{task_title}</b></div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:1.1rem; font-weight:800; color:#2563eb;">+{points} XP</div>
                    <div style="font-size:0.7rem; color:#64748b; margin-top:2px;">Ожидает подтверждения</div>
                </div>
            </div>
        </div>
        """.strip()
    else:
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


def render_xp_summary(team: Dict[str, Any], milestones: List[Dict[str, Any]], variant: str = "A") -> str:
    """
    Renders the overall XP summary panel for a student team.
    Strictly NO emojis.
    """
    v_key = variant.upper() if variant.upper() in VARIANT_CONFIGS else "A"
    total_xp = team.get("progress_points", 0)
    completed_milestones = sum(1 for m in milestones if m.get("status") == "completed")
    pending_milestones = sum(1 for m in milestones if m.get("status") != "completed")
    potential_xp = sum(m.get("points", 0) for m in milestones if m.get("status") != "completed")

    card_border = "#e2e8f0" if v_key == "A" else ("#e4e4e7" if v_key == "B" else "#0f172a")
    card_border_w = "1px" if v_key != "C" else "2px"
    radius = "8px" if v_key != "B" else "4px"

    return f"""
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:12px; margin-bottom:18px;">
        <div style="background:#ffffff; border:{card_border_w} solid {card_border}; border-radius:{radius}; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">Баланс прогресса</div>
            <div style="font-size:1.6rem; font-weight:900; color:#0f172a; margin-top:4px;">{total_xp} XP</div>
            <div style="font-size:0.75rem; color:#15803d; margin-top:2px;">Подтвержденные очки команды</div>
        </div>
        <div style="background:#ffffff; border:{card_border_w} solid {card_border}; border-radius:{radius}; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">Завершено этапов</div>
            <div style="font-size:1.6rem; font-weight:900; color:#0f172a; margin-top:4px;">{completed_milestones}</div>
            <div style="font-size:0.75rem; color:#475569; margin-top:2px;">Контрольные точки приняты</div>
        </div>
        <div style="background:#ffffff; border:{card_border_w} solid {card_border}; border-radius:{radius}; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">Этапов в работе</div>
            <div style="font-size:1.6rem; font-weight:900; color:#0f172a; margin-top:4px;">{pending_milestones}</div>
            <div style="font-size:0.75rem; color:#2563eb; margin-top:2px;">Потенциал: +{potential_xp} XP</div>
        </div>
    </div>
    """.strip()


def get_variant_css(variant: str = "A") -> str:
    """
    Returns high-specificity CSS for the active design variant.
    Injects custom styles for the entire Streamlit canvas, typography, buttons, tabs, and cards.
    Strictly NO emojis.
    """
    v = variant.upper() if variant.upper() in ["A", "B", "C"] else "A"

    if v == "B":
        # Warm Scandinavian Editorial Paper (Ivory / Forest Pine / Serif)
        return """
        <style>
            /* Canvas & App Shell */
            [data-testid="stAppViewContainer"], .stApp {
                background-color: #f5f2eb !important;
                color: #262624 !important;
            }
            header[data-testid="stHeader"] {
                background-color: #f5f2eb !important;
                border-bottom: 1px solid #ddd6c8 !important;
            }
            section[data-testid="stSidebar"] {
                background-color: #ece7de !important;
                border-right: 1px solid #ddd6c8 !important;
            }

            /* Typography */
            h1, h2, h3, .main-title {
                font-family: Georgia, "Newsreader", "Playfair Display", "Times New Roman", serif !important;
                font-weight: 700 !important;
                color: #1e3a2b !important;
                letter-spacing: -0.2px !important;
            }
            .subtitle {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
                font-size: 1.05rem !important;
                color: #57534e !important;
                margin-bottom: 1.2rem !important;
            }

            /* Cards */
            .task-card-box {
                background-color: #ffffff !important;
                border: 1px solid #ddd6c8 !important;
                border-left: 5px solid #1e3a2b !important;
                border-radius: 6px !important;
                padding: 22px !important;
                margin-bottom: 18px !important;
                box-shadow: 0 2px 10px rgba(30, 58, 43, 0.05) !important;
            }
            .task-card-box:hover {
                border-color: #b5ac9d !important;
                border-left-color: #14281e !important;
            }
            .score-card {
                background-color: #ffffff !important;
                border: 1px solid #ddd6c8 !important;
                border-radius: 6px !important;
                padding: 16px !important;
                box-shadow: 0 1px 4px rgba(30, 58, 43, 0.04) !important;
            }
            .recommendation-banner {
                background-color: #f0fdf4 !important;
                border: 1px solid #bbf7d0 !important;
                border-left: 5px solid #047857 !important;
                padding: 12px 16px !important;
                margin-bottom: 14px !important;
                border-radius: 6px !important;
                color: #064e3b !important;
                font-size: 0.92rem !important;
            }

            /* Streamlit Native Buttons */
            .stButton > button {
                background-color: #1e3a2b !important;
                color: #fdfcf7 !important;
                border-radius: 6px !important;
                border: 1px solid #14281e !important;
                font-family: Georgia, serif !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 4px rgba(30, 58, 43, 0.15) !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button:hover {
                background-color: #284e3a !important;
                color: #ffffff !important;
                box-shadow: 0 4px 8px rgba(30, 58, 43, 0.25) !important;
                transform: translateY(-1px) !important;
            }

            /* Streamlit Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: transparent !important;
                border-bottom: 2px solid #ddd6c8 !important;
            }
            .stTabs [data-baseweb="tab"] {
                font-family: Georgia, serif !important;
                font-size: 0.95rem !important;
                color: #78716c !important;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                color: #1e3a2b !important;
                border-bottom: 3px solid #1e3a2b !important;
                font-weight: 700 !important;
            }
        </style>
        """
    elif v == "C":
        # Swiss Neo-Brutalist HUD (High-Contrast & Jet Black)
        return """
        <style>
            /* Canvas & App Shell */
            [data-testid="stAppViewContainer"], .stApp {
                background-color: #ffffff !important;
                color: #000000 !important;
                font-family: "Space Grotesk", -apple-system, "SF Pro Display", sans-serif !important;
            }
            header[data-testid="stHeader"] {
                background-color: #ffffff !important;
                border-bottom: 3px solid #000000 !important;
            }
            section[data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 3px solid #000000 !important;
            }

            /* Typography */
            h1, h2, h3, .main-title {
                font-weight: 900 !important;
                color: #000000 !important;
                text-transform: uppercase !important;
                letter-spacing: -0.5px !important;
            }
            .subtitle {
                font-size: 1.05rem !important;
                color: #000000 !important;
                font-weight: 600 !important;
                margin-bottom: 1.4rem !important;
            }

            /* Cards */
            .task-card-box {
                background-color: #ffffff !important;
                border: 2.5px solid #000000 !important;
                border-radius: 2px !important;
                padding: 22px !important;
                margin-bottom: 22px !important;
                box-shadow: 6px 6px 0px #000000 !important;
                transition: transform 0.1s ease, box-shadow 0.1s ease !important;
            }
            .task-card-box:hover {
                transform: translate(-2px, -2px) !important;
                box-shadow: 8px 8px 0px #000000 !important;
            }
            .score-card {
                background-color: #ffffff !important;
                border: 2px solid #000000 !important;
                border-radius: 2px !important;
                padding: 16px !important;
                box-shadow: 4px 4px 0px #000000 !important;
            }
            .recommendation-banner {
                background-color: #000000 !important;
                border: 2px solid #000000 !important;
                padding: 12px 18px !important;
                margin-bottom: 14px !important;
                border-radius: 2px !important;
                color: #ffffff !important;
                font-size: 0.92rem !important;
                box-shadow: 4px 4px 0px #10b981 !important;
            }

            /* Streamlit Native Buttons */
            .stButton > button {
                background-color: #000000 !important;
                color: #ffffff !important;
                border: 2.5px solid #000000 !important;
                border-radius: 2px !important;
                box-shadow: 4px 4px 0px #000000 !important;
                font-weight: 900 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                transition: all 0.1s ease !important;
            }
            .stButton > button:hover {
                background-color: #ffffff !important;
                color: #000000 !important;
                box-shadow: 2px 2px 0px #000000 !important;
                transform: translate(2px, 2px) !important;
            }

            /* Streamlit Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: transparent !important;
                border-bottom: 3px solid #000000 !important;
            }
            .stTabs [data-baseweb="tab"] {
                font-weight: 800 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
                color: #52525b !important;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #000000 !important;
                color: #ffffff !important;
                font-weight: 900 !important;
                border-radius: 2px 2px 0 0 !important;
            }
        </style>
        """
    else:
        # Variant A: Modern Fintech SaaS (Slate & Electric Indigo)
        return """
        <style>
            /* Canvas & App Shell */
            [data-testid="stAppViewContainer"], .stApp {
                background-color: #f8fafc !important;
                color: #0f172a !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            }
            header[data-testid="stHeader"] {
                background-color: #f8fafc !important;
                border-bottom: 1px solid #e2e8f0 !important;
            }
            section[data-testid="stSidebar"] {
                background-color: #ffffff !important;
                border-right: 1px solid #e2e8f0 !important;
            }

            /* Typography */
            h1, h2, h3, .main-title {
                font-size: 2.2rem !important;
                font-weight: 800 !important;
                color: #0f172a !important;
                letter-spacing: -0.5px !important;
            }
            .subtitle {
                font-size: 1.05rem !important;
                color: #475569 !important;
                margin-bottom: 1.3rem !important;
                line-height: 1.5 !important;
            }

            /* Cards */
            .task-card-box {
                background-color: #ffffff !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 12px !important;
                padding: 22px !important;
                margin-bottom: 20px !important;
                box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05) !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease !important;
            }
            .task-card-box:hover {
                border-color: #cbd5e1 !important;
                box-shadow: 0 10px 25px -4px rgba(15, 23, 42, 0.08) !important;
                transform: translateY(-2px) !important;
            }
            .score-card {
                background-color: #ffffff !important;
                border: 1px solid #e2e8f0 !important;
                border-radius: 10px !important;
                padding: 16px !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
            }
            .recommendation-banner {
                background-color: #f0fdf4 !important;
                border: 1px solid #bbf7d0 !important;
                border-left: 4px solid #10b981 !important;
                padding: 12px 16px !important;
                margin-bottom: 12px !important;
                border-radius: 8px !important;
                color: #15803d !important;
                font-size: 0.92rem !important;
            }

            /* Streamlit Native Buttons */
            .stButton > button {
                background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
                color: #ffffff !important;
                border-radius: 8px !important;
                border: none !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 6px rgba(79, 70, 229, 0.25) !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button:hover {
                background: linear-gradient(135deg, #4338ca, #3730a3) !important;
                box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
                transform: translateY(-1px) !important;
            }

            /* Streamlit Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: transparent !important;
                border-bottom: 2px solid #e2e8f0 !important;
            }
            .stTabs [data-baseweb="tab"] {
                font-size: 0.95rem !important;
                color: #64748b !important;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                color: #4f46e5 !important;
                border-bottom: 3px solid #4f46e5 !important;
                font-weight: 700 !important;
            }
        </style>
        """


def render_variant_showcase(variant: str = "A") -> str:
    """
    Renders an interactive side-by-side design showcase directly on the page,
    demonstrating the live typography, speedometer, sample card, and styling DNA.
    Strictly NO emojis.
    """
    v = variant.upper() if variant.upper() in ["A", "B", "C"] else "A"
    cfg = VARIANT_CONFIGS[v]

    if v == "B":
        container_style = "background:#ffffff; border:1px solid #ddd6c8; border-left:6px solid #1e3a2b; border-radius:6px; padding:20px; margin-bottom:24px; box-shadow:0 3px 12px rgba(30,58,43,0.06);"
        badge_style = "background:#ece7de; color:#1e3a2b; border:1px solid #ddd6c8; border-radius:4px; padding:3px 10px; font-family:Georgia, serif; font-weight:700; font-size:0.8rem; text-transform:uppercase;"
        title_font = "font-family:Georgia, serif; font-size:1.35rem; font-weight:700; color:#1e3a2b;"
        btn_sample = "background:#1e3a2b; color:#fdfcf7; border-radius:6px; padding:8px 16px; font-family:Georgia, serif; font-size:0.82rem; font-weight:700; display:inline-block;"
    elif v == "C":
        container_style = "background:#ffffff; border:3px solid #000000; border-radius:2px; padding:20px; margin-bottom:24px; box-shadow:6px 6px 0px #000000;"
        badge_style = "background:#000000; color:#ffffff; border-radius:2px; padding:3px 10px; font-weight:900; font-size:0.8rem; text-transform:uppercase; letter-spacing:0.5px;"
        title_font = "font-family:'Space Grotesk', sans-serif; font-size:1.4rem; font-weight:900; color:#000000; text-transform:uppercase;"
        btn_sample = "background:#000000; color:#ffffff; border:2px solid #000000; border-radius:2px; box-shadow:3px 3px 0px #000000; padding:8px 16px; font-size:0.82rem; font-weight:900; text-transform:uppercase; display:inline-block;"
    else:
        container_style = "background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:20px; margin-bottom:24px; box-shadow:0 4px 20px -2px rgba(15,23,42,0.06);"
        badge_style = "background:#eef2ff; color:#4f46e5; border:1px solid #c7d2fe; border-radius:999px; padding:3px 12px; font-weight:700; font-size:0.8rem;"
        title_font = "font-family:system-ui, sans-serif; font-size:1.35rem; font-weight:800; color:#0f172a;"
        btn_sample = "background:linear-gradient(135deg, #4f46e5, #4338ca); color:#ffffff; border-radius:8px; padding:8px 16px; font-size:0.82rem; font-weight:700; display:inline-block; box-shadow:0 2px 6px rgba(79,70,229,0.3);"

    sample_gauge = render_circular_gauge(85, size=90, compact=True, variant=v)

    return f"""
    <div style="{container_style}">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:14px; border-bottom:1px solid #f1f5f9; padding-bottom:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="{badge_style}">Вариант {v}</span>
                <span style="{title_font}">{cfg['full_name']}</span>
            </div>
            <div style="font-size:0.85rem; color:#64748b;">
                {cfg['tagline']}
            </div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:16px; align-items:center;">
            <div style="display:flex; align-items:center; gap:14px; background:#f8fafc; padding:12px 16px; border-radius:8px; border:1px solid #e2e8f0;">
                <div>{sample_gauge}</div>
                <div>
                    <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase;">Спидометр рейтинга</div>
                    <div style="font-size:1.1rem; font-weight:800; color:#0f172a; margin-top:2px;">85 / 100 Баллов</div>
                    <div style="font-size:0.75rem; color:#2563eb; font-weight:600;">Уровень: Готовая к разработке</div>
                </div>
            </div>
            <div style="background:#f8fafc; padding:12px 16px; border-radius:8px; border:1px solid #e2e8f0;">
                <div style="font-size:0.75rem; font-weight:700; color:#64748b; text-transform:uppercase; margin-bottom:6px;">Стиль кнопок платформы</div>
                <div style="{btn_sample}">Взять задачу в работу (+100 XP)</div>
            </div>
            <div style="background:#f8fafc; padding:12px 16px; border-radius:8px; border:1px solid #e2e8f0; font-size:0.8rem; line-height:1.45;">
                <div style="font-weight:700; color:#0f172a; margin-bottom:4px;">Характеристики дизайн-системы:</div>
                <div><b>Холст:</b> {cfg['app_bg']}</div>
                <div><b>Геометрия:</b> Радиус {cfg['card_radius']}, граница {cfg['card_border']}</div>
                <div><b>Тени:</b> {cfg['card_shadow']}</div>
            </div>
        </div>
    </div>
    """.strip()


def render_prototype_switcher(current_variant: str = "A") -> str:
    """
    Renders a floating bottom prototype switcher bar to flip between design variants.
    Strictly NO emojis.
    """
    curr = current_variant.upper() if current_variant.upper() in ["A", "B", "C"] else "A"
    variants_list = ["A", "B", "C"]
    curr_idx = variants_list.index(curr)
    prev_v = variants_list[(curr_idx - 1) % len(variants_list)]
    next_v = variants_list[(curr_idx + 1) % len(variants_list)]

    curr_cfg = VARIANT_CONFIGS[curr]

    # Render pill links for each variant
    pills_html = []
    for v_code in variants_list:
        v_info = VARIANT_CONFIGS[v_code]
        is_active = v_code == curr
        active_bg = "#3b82f6" if is_active else "rgba(255,255,255,0.12)"
        active_text = "#ffffff" if is_active else "#cbd5e1"
        pills_html.append(
            f'<a href="?variant={v_code}" target="_self" style="padding:4px 10px; background:{active_bg}; color:{active_text}; text-decoration:none; border-radius:6px; font-weight:700; font-size:0.78rem; transition:all 0.2s ease;">{v_code}: {v_info["name"].split()[0]}</a>'
        )

    pills_row = "".join(pills_html)

    return f"""
    <div style="position:fixed; bottom:20px; left:50%; transform:translateX(-50%); z-index:999999; background:rgba(15, 23, 42, 0.96); backdrop-filter:blur(10px); color:#ffffff; padding:10px 18px; border-radius:999px; box-shadow:0 12px 30px -4px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.12); display:flex; align-items:center; gap:12px; font-family:system-ui, -apple-system, sans-serif; font-size:0.85rem;">
        <span style="font-weight:800; color:#93c5fd; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.5px;">Прототип UI:</span>
        <a href="?variant={prev_v}" target="_self" style="color:#ffffff; text-decoration:none; font-weight:800; padding:2px 8px; background:rgba(255,255,255,0.15); border-radius:4px; font-size:0.8rem;">[ &lt; {prev_v} ]</a>
        <span style="color:#f8fafc; font-weight:700;">{curr_cfg['name']}</span>
        <a href="?variant={next_v}" target="_self" style="color:#ffffff; text-decoration:none; font-weight:800; padding:2px 8px; background:rgba(255,255,255,0.15); border-radius:4px; font-size:0.8rem;">[ {next_v} &gt; ]</a>
        <div style="height:16px; width:1px; background:rgba(255,255,255,0.25); margin:0 4px;"></div>
        <div style="display:flex; gap:6px;">
            {pills_row}
        </div>
    </div>
    """.strip()
