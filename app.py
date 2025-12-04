import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path
import calendar

# Configuration de la page
st.set_page_config(
    page_title="My Planning Pro",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé ultra-moderne
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* Fond principal */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    /* Header principal */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #00d4ff, #7c3aed, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        letter-spacing: -1px;
    }

    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Cards modernes */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin: 10px 0;
    }

    /* Créneaux horaires */
    .time-block {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.2), rgba(0, 212, 255, 0.1));
        border-radius: 12px;
        padding: 12px;
        margin: 4px 0;
        border-left: 4px solid #7c3aed;
        transition: all 0.3s ease;
    }

    .time-block:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }

    .time-block-rest {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 197, 253, 0.1));
        border-left: 4px solid #3b82f6;
    }

    .time-block-work {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(134, 239, 172, 0.1));
        border-left: 4px solid #22c55e;
    }

    .time-block-urgent {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.3), rgba(252, 165, 165, 0.1));
        border-left: 4px solid #ef4444;
        animation: pulse-urgent 2s infinite;
    }

    @keyframes pulse-urgent {
        0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 0 20px 5px rgba(239, 68, 68, 0.2); }
    }

    /* Time slot libre */
    .time-slot-free {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 2px 0;
        border: 1px dashed rgba(255, 255, 255, 0.1);
        color: #64748b;
        font-size: 0.9rem;
    }

    /* Stats cards */
    .stat-card {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        color: white;
    }

    .stat-card-blue {
        background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%);
    }

    .stat-card-green {
        background: linear-gradient(135deg, #22c55e 0%, #4ade80 100%);
    }

    .stat-card-orange {
        background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 8px;
        border-radius: 16px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 12px;
        padding: 12px 24px;
        color: #94a3b8;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
        color: white !important;
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4);
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
    }

    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #7c3aed, #00d4ff);
        border-radius: 10px;
    }

    /* Calendar day */
    .calendar-day {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        min-height: 80px;
        transition: all 0.3s ease;
    }

    .calendar-day:hover {
        background: rgba(124, 58, 237, 0.2);
        transform: scale(1.02);
    }

    .calendar-day-today {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.3), rgba(0, 212, 255, 0.2));
        border: 2px solid #7c3aed;
    }

    .calendar-day-has-events {
        position: relative;
    }

    .calendar-day-has-events::after {
        content: '';
        position: absolute;
        bottom: 8px;
        left: 50%;
        transform: translateX(-50%);
        width: 6px;
        height: 6px;
        background: #7c3aed;
        border-radius: 50%;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #7c3aed;
    }

    /* Dividers */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(124, 58, 237, 0.5), transparent);
        margin: 20px 0;
    }

    /* Checkbox custom */
    .stCheckbox > label > span {
        color: white !important;
    }

    /* Activity block in calendar */
    .activity-block {
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        margin: 4px 0;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Week view */
    .week-header {
        background: rgba(124, 58, 237, 0.2);
        padding: 15px;
        border-radius: 12px 12px 0 0;
        text-align: center;
        font-weight: 600;
        color: #7c3aed;
    }

    .week-body {
        background: rgba(255, 255, 255, 0.03);
        padding: 15px;
        border-radius: 0 0 12px 12px;
        min-height: 200px;
    }
</style>
""", unsafe_allow_html=True)

# Fichier de sauvegarde
DATA_FILE = Path(__file__).parent / "planning_data.json"

# Tous les créneaux horaires (de 00:00 à 23:00)
ALL_TIME_SLOTS = [f"{h:02d}:00" for h in range(24)]

# Catégories d'activités avec couleurs
CATEGORIES = {
    "Repos/Sommeil": {"icon": "😴", "color": "#3b82f6", "class": "rest"},
    "Travail": {"icon": "💼", "color": "#22c55e", "class": "work"},
    "Trading": {"icon": "📈", "color": "#eab308", "class": "work"},
    "Sport": {"icon": "🏋️", "color": "#f97316", "class": "work"},
    "Études": {"icon": "📚", "color": "#8b5cf6", "class": "work"},
    "Réunion": {"icon": "👥", "color": "#ec4899", "class": "work"},
    "Repas": {"icon": "🍽️", "color": "#14b8a6", "class": "rest"},
    "Pause": {"icon": "☕", "color": "#6366f1", "class": "rest"},
    "Personnel": {"icon": "🏠", "color": "#a855f7", "class": "work"},
    "Projet": {"icon": "🎯", "color": "#f43f5e", "class": "work"},
    "Loisirs": {"icon": "🎮", "color": "#06b6d4", "class": "rest"},
    "Autre": {"icon": "📌", "color": "#64748b", "class": "work"}
}

PRIORITIES = {
    "Urgent": {"icon": "🔴", "color": "#ef4444"},
    "Haute": {"icon": "🟠", "color": "#f97316"},
    "Moyenne": {"icon": "🟡", "color": "#eab308"},
    "Basse": {"icon": "🟢", "color": "#22c55e"}
}

# Fonctions de données
def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "planning": {},
        "tasks": {},
        "weekly_goals": {},
        "monthly_goals": {},
        "quarterly_vision": {},
        "notes": {}
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "data" not in st.session_state:
    st.session_state.data = load_data()

# Header
st.markdown('<p class="main-header">✨ MY PLANNING PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Organisez votre vie, atteignez vos objectifs</p>', unsafe_allow_html=True)

# Onglets
tab_daily, tab_weekly, tab_monthly, tab_quarterly = st.tabs([
    "📆 JOURNÉE",
    "📅 SEMAINE",
    "🗓️ MOIS",
    "📊 TRIMESTRE"
])

# ==================== ONGLET JOURNALIER ====================
with tab_daily:
    # Sélection de date
    col_nav1, col_date, col_nav2 = st.columns([1, 3, 1])

    with col_nav1:
        if st.button("◀️ Hier", key="prev_day"):
            if "selected_date" not in st.session_state:
                st.session_state.selected_date = datetime.today().date()
            st.session_state.selected_date = st.session_state.selected_date - timedelta(days=1)
            st.rerun()

    with col_date:
        if "selected_date" not in st.session_state:
            st.session_state.selected_date = datetime.today().date()

        selected_date = st.date_input(
            "",
            st.session_state.selected_date,
            key="date_picker",
            label_visibility="collapsed"
        )
        st.session_state.selected_date = selected_date
        date_key = selected_date.strftime("%Y-%m-%d")

        days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        months_fr = ["janvier", "février", "mars", "avril", "mai", "juin",
                     "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

        day_name = days_fr[selected_date.weekday()]
        month_name = months_fr[selected_date.month - 1]

        is_today = selected_date == datetime.today().date()
        today_badge = "📍 AUJOURD'HUI" if is_today else ""

        st.markdown(f"### {today_badge} {day_name} {selected_date.day} {month_name} {selected_date.year}")

    with col_nav2:
        if st.button("Demain ▶️", key="next_day"):
            st.session_state.selected_date = st.session_state.selected_date + timedelta(days=1)
            st.rerun()

    st.markdown("---")

    # Layout principal
    col_planning, col_tasks = st.columns([3, 1])

    with col_planning:
        st.markdown("### ⏰ Planning de la Journée")

        # Initialiser le planning
        if date_key not in st.session_state.data["planning"]:
            st.session_state.data["planning"][date_key] = {}

        # Formulaire d'ajout de bloc horaire
        with st.expander("➕ **AJOUTER UN BLOC HORAIRE**", expanded=False):
            st.markdown("*Sélectionnez une plage horaire pour planifier une activité*")

            col1, col2 = st.columns(2)
            with col1:
                start_hour = st.selectbox(
                    "⏰ Heure de début",
                    options=list(range(24)),
                    format_func=lambda x: f"{x:02d}:00",
                    index=8
                )
            with col2:
                end_hour = st.selectbox(
                    "⏰ Heure de fin",
                    options=list(range(24)),
                    format_func=lambda x: f"{x:02d}:00",
                    index=9
                )

            if end_hour <= start_hour:
                st.warning("⚠️ L'heure de fin doit être après l'heure de début")

            col3, col4 = st.columns(2)
            with col3:
                category = st.selectbox(
                    "📁 Catégorie",
                    options=list(CATEGORIES.keys()),
                    format_func=lambda x: f"{CATEGORIES[x]['icon']} {x}"
                )
            with col4:
                priority = st.selectbox(
                    "🎯 Priorité",
                    options=list(PRIORITIES.keys()),
                    format_func=lambda x: f"{PRIORITIES[x]['icon']} {x}"
                )

            description = st.text_input("📝 Description de l'activité")

            if st.button("✅ Ajouter au Planning", use_container_width=True, type="primary"):
                if description and end_hour > start_hour:
                    block_key = f"{start_hour:02d}:00-{end_hour:02d}:00"
                    st.session_state.data["planning"][date_key][block_key] = {
                        "start": start_hour,
                        "end": end_hour,
                        "category": category,
                        "priority": priority,
                        "description": description,
                        "completed": False
                    }
                    save_data(st.session_state.data)
                    st.success(f"✅ Bloc {block_key} ajouté!")
                    st.rerun()

        # Affichage du planning
        st.markdown("---")

        planning = st.session_state.data["planning"].get(date_key, {})

        # Créer une grille horaire
        for hour in range(6, 24):  # De 6h à 23h
            hour_str = f"{hour:02d}:00"
            next_hour_str = f"{hour+1:02d}:00"

            # Chercher si un bloc couvre cette heure
            block_found = None
            for block_key, block in planning.items():
                if block["start"] <= hour < block["end"]:
                    block_found = (block_key, block)
                    break

            if block_found:
                block_key, block = block_found
                # N'afficher que la première heure du bloc
                if block["start"] == hour:
                    cat = CATEGORIES[block["category"]]
                    prio = PRIORITIES[block["priority"]]
                    duration = block["end"] - block["start"]

                    col_time, col_block, col_actions = st.columns([1, 4, 1])

                    with col_time:
                        st.markdown(f"**{hour_str}**")
                        st.caption(f"↓ {block['end']:02d}:00")

                    with col_block:
                        status_icon = "✅" if block["completed"] else ""
                        text_style = "~~" if block["completed"] else ""

                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, {cat['color']}33, {cat['color']}11);
                            border-left: 4px solid {cat['color']};
                            border-radius: 12px;
                            padding: 15px;
                            margin: 5px 0;
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 1.2rem;">{cat['icon']} {prio['icon']} <strong>{text_style}{block['description']}{text_style}</strong> {status_icon}</span>
                                <span style="color: {cat['color']}; font-weight: 600;">{duration}h</span>
                            </div>
                            <div style="color: #94a3b8; font-size: 0.9rem; margin-top: 5px;">
                                {block['category']} • {hour_str} - {block['end']:02d}:00
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_actions:
                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("✓" if not block["completed"] else "↩️", key=f"toggle_{date_key}_{block_key}"):
                                st.session_state.data["planning"][date_key][block_key]["completed"] = not block["completed"]
                                save_data(st.session_state.data)
                                st.rerun()
                        with col_b:
                            if st.button("🗑️", key=f"del_{date_key}_{block_key}"):
                                del st.session_state.data["planning"][date_key][block_key]
                                save_data(st.session_state.data)
                                st.rerun()
            else:
                # Créneau libre
                col_time, col_free = st.columns([1, 5])
                with col_time:
                    st.markdown(f"**{hour_str}**")
                with col_free:
                    st.markdown(f"""
                    <div style="
                        background: rgba(255, 255, 255, 0.02);
                        border: 1px dashed rgba(255, 255, 255, 0.1);
                        border-radius: 8px;
                        padding: 10px;
                        color: #475569;
                        font-size: 0.9rem;
                    ">
                        — Créneau libre —
                    </div>
                    """, unsafe_allow_html=True)

    with col_tasks:
        st.markdown("### ✅ Tâches")

        if date_key not in st.session_state.data["tasks"]:
            st.session_state.data["tasks"][date_key] = []

        # Ajouter une tâche
        with st.form("quick_task", clear_on_submit=True):
            task_input = st.text_input("Nouvelle tâche", placeholder="Ex: Appeler le client...")
            task_prio = st.selectbox("Priorité", list(PRIORITIES.keys()), key="qp")

            if st.form_submit_button("➕ Ajouter", use_container_width=True):
                if task_input:
                    st.session_state.data["tasks"][date_key].append({
                        "task": task_input,
                        "priority": task_prio,
                        "completed": False
                    })
                    save_data(st.session_state.data)
                    st.rerun()

        # Liste des tâches
        tasks = st.session_state.data["tasks"].get(date_key, [])

        if tasks:
            priority_order = {"Urgent": 0, "Haute": 1, "Moyenne": 2, "Basse": 3}
            sorted_tasks = sorted(enumerate(tasks), key=lambda x: (x[1]["completed"], priority_order[x[1]["priority"]]))

            for idx, task in sorted_tasks:
                prio = PRIORITIES[task["priority"]]

                col_c, col_t = st.columns([0.3, 0.7])

                with col_c:
                    new_state = st.checkbox("", value=task["completed"], key=f"task_{date_key}_{idx}", label_visibility="collapsed")
                    if new_state != task["completed"]:
                        st.session_state.data["tasks"][date_key][idx]["completed"] = new_state
                        save_data(st.session_state.data)
                        st.rerun()

                with col_t:
                    text_style = "~~" if task["completed"] else ""
                    opacity = "0.5" if task["completed"] else "1"
                    st.markdown(f"<span style='opacity: {opacity};'>{prio['icon']} {text_style}{task['task']}{text_style}</span>", unsafe_allow_html=True)

        else:
            st.info("Aucune tâche")

        # Stats
        st.markdown("---")
        st.markdown("### 📊 Stats")

        all_items = list(planning.values()) + tasks
        total = len(all_items)
        completed = sum(1 for item in all_items if item.get("completed", False))

        if total > 0:
            pct = completed / total
            st.progress(pct)
            st.markdown(f"**{completed}/{total}** complétés ({pct*100:.0f}%)")
        else:
            st.caption("Aucune activité")

# ==================== ONGLET HEBDOMADAIRE ====================
with tab_weekly:
    st.markdown("### 📅 Vue Hebdomadaire")

    # Navigation
    if "week_start" not in st.session_state:
        today = datetime.today()
        st.session_state.week_start = today - timedelta(days=today.weekday())

    col_p, col_w, col_n = st.columns([1, 4, 1])

    with col_p:
        if st.button("◀️ Semaine", key="prev_week"):
            st.session_state.week_start = st.session_state.week_start - timedelta(weeks=1)
            st.rerun()

    with col_w:
        week_start = st.session_state.week_start
        week_end = week_start + timedelta(days=6)
        week_key = week_start.strftime("%Y-W%W")

        st.markdown(f"### Semaine du {week_start.strftime('%d/%m')} au {week_end.strftime('%d/%m/%Y')}")

    with col_n:
        if st.button("Semaine ▶️", key="next_week"):
            st.session_state.week_start = st.session_state.week_start + timedelta(weeks=1)
            st.rerun()

    st.markdown("---")

    # Grille de la semaine
    days_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    cols = st.columns(7)

    for i, col in enumerate(cols):
        with col:
            day_date = week_start + timedelta(days=i)
            day_key = day_date.strftime("%Y-%m-%d")
            is_today = day_date.date() == datetime.today().date()

            # Header du jour
            badge = "📍" if is_today else ""
            header_style = "background: linear-gradient(135deg, #7c3aed, #a855f7);" if is_today else "background: rgba(124, 58, 237, 0.2);"

            st.markdown(f"""
            <div style="{header_style} padding: 12px; border-radius: 12px 12px 0 0; text-align: center;">
                <strong style="color: white;">{badge} {days_fr[i]}</strong><br>
                <span style="color: rgba(255,255,255,0.7);">{day_date.strftime('%d/%m')}</span>
            </div>
            """, unsafe_allow_html=True)

            # Contenu du jour
            planning = st.session_state.data["planning"].get(day_key, {})
            tasks = st.session_state.data["tasks"].get(day_key, [])

            with st.container():
                if planning:
                    for block_key, block in sorted(planning.items(), key=lambda x: x[1]["start"]):
                        cat = CATEGORIES[block["category"]]
                        status = "✅" if block["completed"] else ""
                        st.markdown(f"""
                        <div style="
                            background: {cat['color']}22;
                            border-left: 3px solid {cat['color']};
                            padding: 6px 8px;
                            border-radius: 6px;
                            margin: 4px 0;
                            font-size: 0.75rem;
                        ">
                            {cat['icon']} {block['description'][:15]}... {status}
                        </div>
                        """, unsafe_allow_html=True)

                if tasks:
                    for task in tasks[:3]:
                        status = "✅" if task["completed"] else "⬜"
                        st.markdown(f"<span style='font-size: 0.75rem;'>{status} {task['task'][:12]}...</span>", unsafe_allow_html=True)

                if not planning and not tasks:
                    st.caption("Libre")

    st.markdown("---")

    # Objectifs hebdomadaires
    st.markdown("### 🎯 Objectifs de la Semaine")

    if week_key not in st.session_state.data["weekly_goals"]:
        st.session_state.data["weekly_goals"][week_key] = []

    col_form, col_list = st.columns([1, 2])

    with col_form:
        with st.form("weekly_form", clear_on_submit=True):
            goal = st.text_area("Nouvel objectif")
            gprio = st.selectbox("Priorité", list(PRIORITIES.keys()), key="wgp")

            if st.form_submit_button("➕ Ajouter", use_container_width=True):
                if goal:
                    st.session_state.data["weekly_goals"][week_key].append({
                        "goal": goal,
                        "priority": gprio,
                        "completed": False
                    })
                    save_data(st.session_state.data)
                    st.rerun()

    with col_list:
        goals = st.session_state.data["weekly_goals"].get(week_key, [])

        if goals:
            for idx, goal in enumerate(goals):
                prio = PRIORITIES[goal["priority"]]

                col_c, col_g, col_d = st.columns([0.5, 4, 0.5])

                with col_c:
                    new_state = st.checkbox("", value=goal["completed"], key=f"wg_{week_key}_{idx}")
                    if new_state != goal["completed"]:
                        st.session_state.data["weekly_goals"][week_key][idx]["completed"] = new_state
                        save_data(st.session_state.data)
                        st.rerun()

                with col_g:
                    style = "~~" if goal["completed"] else ""
                    st.markdown(f"{prio['icon']} {style}{goal['goal']}{style}")

                with col_d:
                    if st.button("🗑️", key=f"del_wg_{week_key}_{idx}"):
                        st.session_state.data["weekly_goals"][week_key].pop(idx)
                        save_data(st.session_state.data)
                        st.rerun()
        else:
            st.info("Définissez vos objectifs de la semaine")

# ==================== ONGLET MENSUEL ====================
with tab_monthly:
    st.markdown("### 🗓️ Vue Mensuelle")

    months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox("Mois", months_fr, index=datetime.today().month - 1)
    with col2:
        selected_year = st.number_input("Année", 2020, 2030, datetime.today().year)

    month_num = months_fr.index(selected_month) + 1
    month_key = f"{selected_year}-{month_num:02d}"

    st.markdown(f"### {selected_month} {selected_year}")
    st.markdown("---")

    # Calendrier
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(selected_year, month_num)

    days_header = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    cols = st.columns(7)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**{days_header[i]}**")

    for week in month_days:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    day_key = f"{selected_year}-{month_num:02d}-{day:02d}"

                    is_today = (day == datetime.today().day and
                               month_num == datetime.today().month and
                               selected_year == datetime.today().year)

                    planning = st.session_state.data["planning"].get(day_key, {})
                    tasks = st.session_state.data["tasks"].get(day_key, [])
                    total = len(planning) + len(tasks)

                    if is_today:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #7c3aed33, #a855f722);
                                    border: 2px solid #7c3aed;
                                    border-radius: 10px; padding: 10px; text-align: center; min-height: 60px;">
                            <strong style="color: #7c3aed;">📍 {day}</strong>
                            {"<br><span style='font-size: 0.8rem;'>"+str(total)+" items</span>" if total > 0 else ""}
                        </div>
                        """, unsafe_allow_html=True)
                    elif total > 0:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.05);
                                    border-radius: 10px; padding: 10px; text-align: center; min-height: 60px;">
                            <strong>{day}</strong><br>
                            <span style="font-size: 0.8rem; color: #7c3aed;">{total} items</span>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.02);
                                    border-radius: 10px; padding: 10px; text-align: center; min-height: 60px;">
                            {day}
                        </div>
                        """, unsafe_allow_html=True)

    st.markdown("---")

    # Objectifs mensuels
    st.markdown("### 🎯 Objectifs du Mois")

    if month_key not in st.session_state.data["monthly_goals"]:
        st.session_state.data["monthly_goals"][month_key] = []

    col_f, col_l = st.columns([1, 2])

    with col_f:
        with st.form("monthly_form", clear_on_submit=True):
            obj = st.text_area("Nouvel objectif")
            oprio = st.selectbox("Priorité", list(PRIORITIES.keys()), key="mgp")

            if st.form_submit_button("➕ Ajouter", use_container_width=True):
                if obj:
                    st.session_state.data["monthly_goals"][month_key].append({
                        "objective": obj,
                        "priority": oprio,
                        "completed": False,
                        "progress": 0
                    })
                    save_data(st.session_state.data)
                    st.rerun()

    with col_l:
        objectives = st.session_state.data["monthly_goals"].get(month_key, [])

        if objectives:
            for idx, obj in enumerate(objectives):
                prio = PRIORITIES[obj["priority"]]

                col_c, col_o, col_p, col_d = st.columns([0.5, 3, 1.5, 0.5])

                with col_c:
                    new_state = st.checkbox("", value=obj["completed"], key=f"mo_{month_key}_{idx}")
                    if new_state != obj["completed"]:
                        st.session_state.data["monthly_goals"][month_key][idx]["completed"] = new_state
                        save_data(st.session_state.data)
                        st.rerun()

                with col_o:
                    style = "~~" if obj["completed"] else ""
                    st.markdown(f"{prio['icon']} {style}{obj['objective']}{style}")

                with col_p:
                    prog = st.slider("", 0, 100, obj.get("progress", 0), key=f"prog_{month_key}_{idx}", label_visibility="collapsed")
                    if prog != obj.get("progress", 0):
                        st.session_state.data["monthly_goals"][month_key][idx]["progress"] = prog
                        if prog == 100:
                            st.session_state.data["monthly_goals"][month_key][idx]["completed"] = True
                        save_data(st.session_state.data)

                with col_d:
                    if st.button("🗑️", key=f"del_mo_{month_key}_{idx}"):
                        st.session_state.data["monthly_goals"][month_key].pop(idx)
                        save_data(st.session_state.data)
                        st.rerun()
        else:
            st.info("Définissez vos objectifs du mois")

# ==================== ONGLET TRIMESTRIEL ====================
with tab_quarterly:
    st.markdown("### 📊 Vision Trimestrielle")

    quarters_info = {
        "T1": {"name": "1er Trimestre (Jan-Mar)", "months": [1, 2, 3]},
        "T2": {"name": "2ème Trimestre (Avr-Juin)", "months": [4, 5, 6]},
        "T3": {"name": "3ème Trimestre (Juil-Sep)", "months": [7, 8, 9]},
        "T4": {"name": "4ème Trimestre (Oct-Déc)", "months": [10, 11, 12]}
    }

    col1, col2 = st.columns(2)
    with col1:
        q_select = st.selectbox("Trimestre", list(quarters_info.keys()),
                                index=(datetime.today().month - 1) // 3,
                                format_func=lambda x: quarters_info[x]["name"])
    with col2:
        q_year = st.number_input("Année", 2020, 2030, datetime.today().year, key="qy")

    quarter_key = f"{q_year}-{q_select}"

    st.markdown(f"### {quarters_info[q_select]['name']} {q_year}")
    st.markdown("---")

    # Vue des 3 mois
    cols = st.columns(3)
    months_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    for i, (col, m_num) in enumerate(zip(cols, quarters_info[q_select]["months"])):
        with col:
            m_key = f"{q_year}-{m_num:02d}"
            objectives = st.session_state.data["monthly_goals"].get(m_key, [])

            total = len(objectives)
            completed = sum(1 for o in objectives if o["completed"])

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #7c3aed22, #a855f711);
                        border-radius: 16px; padding: 20px; text-align: center;">
                <h4 style="color: #7c3aed;">{months_fr[m_num-1]}</h4>
                <h2>{completed}/{total}</h2>
                <span style="color: #94a3b8;">objectifs</span>
            </div>
            """, unsafe_allow_html=True)

            if total > 0:
                st.progress(completed / total)

    st.markdown("---")

    # Vision trimestrielle
    st.markdown("### 🌟 Ma Vision du Trimestre")

    if quarter_key not in st.session_state.data["quarterly_vision"]:
        st.session_state.data["quarterly_vision"][quarter_key] = {"vision": "", "goals": []}

    vision = st.text_area(
        "Quelle est votre vision pour ce trimestre?",
        value=st.session_state.data["quarterly_vision"][quarter_key].get("vision", ""),
        height=100,
        placeholder="Décrivez vos aspirations, ce que vous voulez accomplir..."
    )

    if vision != st.session_state.data["quarterly_vision"][quarter_key].get("vision", ""):
        st.session_state.data["quarterly_vision"][quarter_key]["vision"] = vision
        save_data(st.session_state.data)

    st.markdown("---")

    # Grands objectifs
    st.markdown("### 🎯 Grands Objectifs")

    col_f, col_l = st.columns([1, 2])

    with col_f:
        with st.form("quarterly_form", clear_on_submit=True):
            qgoal = st.text_area("Objectif majeur")
            qprio = st.selectbox("Priorité", list(PRIORITIES.keys()), key="qgp")
            qcat = st.selectbox("Domaine", list(CATEGORIES.keys()), key="qgc", format_func=lambda x: f"{CATEGORIES[x]['icon']} {x}")

            if st.form_submit_button("➕ Ajouter", use_container_width=True):
                if qgoal:
                    st.session_state.data["quarterly_vision"][quarter_key]["goals"].append({
                        "goal": qgoal,
                        "priority": qprio,
                        "category": qcat,
                        "completed": False
                    })
                    save_data(st.session_state.data)
                    st.rerun()

    with col_l:
        goals = st.session_state.data["quarterly_vision"][quarter_key].get("goals", [])

        if goals:
            for idx, goal in enumerate(goals):
                prio = PRIORITIES[goal["priority"]]
                cat = CATEGORIES[goal["category"]]

                col_c, col_g, col_d = st.columns([0.5, 4.5, 0.5])

                with col_c:
                    new_state = st.checkbox("", value=goal["completed"], key=f"qg_{quarter_key}_{idx}")
                    if new_state != goal["completed"]:
                        st.session_state.data["quarterly_vision"][quarter_key]["goals"][idx]["completed"] = new_state
                        save_data(st.session_state.data)
                        st.rerun()

                with col_g:
                    style = "~~" if goal["completed"] else ""
                    status = "✅" if goal["completed"] else ""
                    st.markdown(f"{cat['icon']} {prio['icon']} {style}**{goal['goal']}**{style} {status}")

                with col_d:
                    if st.button("🗑️", key=f"del_qg_{quarter_key}_{idx}"):
                        st.session_state.data["quarterly_vision"][quarter_key]["goals"].pop(idx)
                        save_data(st.session_state.data)
                        st.rerun()
        else:
            st.info("Définissez vos grands objectifs du trimestre")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="background: linear-gradient(120deg, #00d4ff, #7c3aed, #f472b6);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 1.8rem;">✨ PLANNING PRO</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats globales
    st.markdown("### 📊 Tableau de Bord")

    all_planning = st.session_state.data["planning"]
    all_tasks = st.session_state.data["tasks"]

    total_items = 0
    completed_items = 0
    urgent_pending = 0

    for items in all_planning.values():
        for item in items.values():
            total_items += 1
            if item.get("completed"):
                completed_items += 1
            elif item.get("priority") == "Urgent":
                urgent_pending += 1

    for items in all_tasks.values():
        for item in items:
            total_items += 1
            if item.get("completed"):
                completed_items += 1
            elif item.get("priority") == "Urgent":
                urgent_pending += 1

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", total_items)
    with col2:
        st.metric("Fait", completed_items)

    if total_items > 0:
        pct = completed_items / total_items
        st.progress(pct)
        st.caption(f"Progression: {pct*100:.0f}%")

    if urgent_pending > 0:
        st.error(f"🔴 {urgent_pending} tâche(s) urgente(s)!")

    st.markdown("---")

    # Légende
    with st.expander("📋 Légende Priorités"):
        for p, info in PRIORITIES.items():
            st.markdown(f"{info['icon']} {p}")

    with st.expander("📁 Catégories"):
        for c, info in CATEGORIES.items():
            st.markdown(f"{info['icon']} {c}")

    st.markdown("---")

    # Actions
    if st.button("🔄 Actualiser", use_container_width=True):
        st.rerun()

    st.download_button(
        "📤 Exporter",
        data=json.dumps(st.session_state.data, ensure_ascii=False, indent=2),
        file_name="planning_backup.json",
        mime="application/json",
        use_container_width=True
    )

    st.markdown("---")

    with st.expander("⚠️ Danger"):
        if st.button("🗑️ Tout effacer", use_container_width=True, type="primary"):
            st.session_state.data = {
                "planning": {},
                "tasks": {},
                "weekly_goals": {},
                "monthly_goals": {},
                "quarterly_vision": {},
                "notes": {}
            }
            save_data(st.session_state.data)
            st.rerun()

    st.markdown("---")
    st.caption("Planning Pro v2.0")
    st.caption("Made with Streamlit")
