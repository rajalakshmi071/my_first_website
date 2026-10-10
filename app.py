"""LifeOS: a friendly dashboard for student tasks, study, and habits."""

import random
from datetime import date
from uuid import uuid4

import streamlit as st

from storage import load_data, save_data


st.set_page_config(
    page_title="LifeOS | Student Dashboard",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #f3f1ff;
        --muted: #a5a3bd;
        --panel: #17182b;
        --panel-soft: #1d1d35;
        --line: rgba(195, 184, 255, 0.13);
        --lavender: #c7b7ff;
        --mint: #8de0c1;
        --rose: #ff9fbd;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: radial-gradient(ellipse at 82% 0%, #282044 0%, #111322 43%, #0d101b 100%); color: var(--ink); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #10111e; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }
    h1, h2, h3 { font-family: 'Manrope', sans-serif !important; letter-spacing: 0 !important; color: var(--ink); }
    h1 { font-size: 2.35rem !important; font-weight: 800 !important; }
    h2 { font-size: 1.45rem !important; }
    p, label, span { letter-spacing: 0 !important; }
    .brand-mark { font: 800 1.25rem 'Manrope', sans-serif; color: var(--ink); margin: .2rem 0 .2rem; }
    .brand-sub { color: var(--muted); font-size: .8rem; margin-bottom: 1.7rem; }
    .eyebrow { color: var(--lavender); font-weight: 700; text-transform: uppercase; font-size: .72rem; letter-spacing: .08em !important; }
    .muted { color: var(--muted); }
    .hero { background: linear-gradient(115deg, rgba(117, 97, 175, .24), rgba(29, 30, 52, .87) 55%, rgba(33, 64, 68, .30)); border: 1px solid var(--line); border-radius: 18px; padding: 1.65rem 1.8rem; margin: .4rem 0 1.2rem; }
    .hero p { color: #c3c0d6; margin: .25rem 0 0; }
    .metric { background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.1rem; min-height: 105px; }
    .metric-label { color: var(--muted); font-size: .8rem; }
    .metric-value { font: 700 1.8rem 'Manrope', sans-serif; color: var(--ink); margin-top: .3rem; }
    .quote { background: rgba(199, 183, 255, .09); border-left: 3px solid var(--lavender); border-radius: 0 12px 12px 0; padding: 1rem 1.2rem; color: #e3def5; font-size: 1rem; margin: .8rem 0 1.2rem; }
    .section-note { color: var(--muted); margin-top: -.6rem; margin-bottom: 1rem; }
    div[data-testid="stForm"] { background: rgba(23, 24, 43, .72); border: 1px solid var(--line); border-radius: 14px; padding: 1rem; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--line); border-radius: 14px; }
    .stButton button, .stFormSubmitButton button { border-radius: 9px; font-weight: 600; }
    .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background: var(--lavender); color: #211c35; border-color: var(--lavender); }
    [data-testid="stMetric"] { background: var(--panel); border: 1px solid var(--line); padding: .9rem; border-radius: 12px; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    [data-testid="stMetricValue"] { color: var(--ink); }
    [data-testid="stProgressBar"] > div > div { background: var(--lavender); }
    [data-testid="stRadio"] label { color: #d7d5e6; }
    @media (max-width: 700px) { h1 { font-size: 1.8rem !important; } .hero { padding: 1.2rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


QUOTES = [
    "Small steps every day add up to remarkable progress.",
    "You do not have to see the whole staircase. Just take the first step.",
    "The secret of getting ahead is getting started.",
    "Progress is progress, no matter how small.",
    "Your future is built by what you do today.",
]


def persist():
    """Save current session data and show a helpful message if it fails."""
    # Every page calls this after a change to write the shared data back to disk.
    error = save_data(st.session_state.lifeos_data)
    if error:
        st.error(error)
    else:
        st.toast("Saved to this project", icon="✅")


if "lifeos_data" not in st.session_state:
    # Load once per browser session so Streamlit reruns don't reset the user's edits.
    st.session_state.lifeos_data, load_error = load_data()
    if load_error:
        st.session_state.load_error = load_error

data = st.session_state.lifeos_data
today = date.today()
today_key = today.isoformat()

with st.sidebar:
    st.markdown('<div class="brand-mark">✦ LifeOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Your student life, in balance.</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Overview", "Tasks", "Study planner", "Habits", "Progress"],
        format_func=lambda item: {
            "Overview": "⌂   Overview",
            "Tasks": "☑   Tasks",
            "Study planner": "▤   Study planner",
            "Habits": "◉   Habits",
            "Progress": "↗   Progress",
        }[item],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption(f"📅  {today.strftime('%A, %B %d')}")
    st.caption("🔒  Your data stays on this device")

if "load_error" in st.session_state:
    st.warning(st.session_state.load_error)


def page_heading(title, subtitle):
    st.markdown(f'<div class="eyebrow">LIFEOS / {page.upper()}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p class="section-note">{subtitle}</p>', unsafe_allow_html=True)


def metric(label, value, icon):
    st.markdown(
        f'<div class="metric"><div class="metric-label">{icon} &nbsp; {label}</div><div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def add_task(title, priority, due_date):
    data["tasks"].append(
        {
            "id": str(uuid4()),
            "title": title.strip(),
            "priority": priority,
            "due_date": due_date.isoformat() if due_date else "",
            "completed": False,
        }
    )
    persist()


if page == "Overview":
    page_heading("A little more in control.", "Your day, your priorities, your pace.")
    st.markdown(
        f'<div class="hero"><div class="eyebrow">{today.strftime("%A, %B %d, %Y")}</div><h2 style="margin:.35rem 0 .2rem">Welcome back, student ✨</h2><p>Make space for what matters. One focused step at a time.</p></div>',
        unsafe_allow_html=True,
    )
    task_done = sum(task["completed"] for task in data["tasks"])
    habits_done = sum(data["habit_logs"].get(today_key, {}).values())
    metric_columns = st.columns(3)
    with metric_columns[0]:
        metric("Tasks complete", f"{task_done}/{len(data['tasks'])}", "☑")
    with metric_columns[1]:
        metric("Study topics", len(data["study_plans"]), "▤")
    with metric_columns[2]:
        metric("Habits today", f"{habits_done}/{len(data['habits'])}", "◉")

    st.markdown(f'<div class="quote">“{random.choice(QUOTES)}”</div>', unsafe_allow_html=True)
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Up next")
        open_tasks = [task for task in data["tasks"] if not task["completed"]]
        if open_tasks:
            for task in open_tasks[:4]:
                detail = f" · Due {task['due_date']}" if task["due_date"] else ""
                st.markdown(f"- **{task['title']}** · {task['priority']}{detail}")
        else:
            st.success("You're all caught up. Enjoy the breathing room!")
    with right:
        st.subheader("Study focus")
        if data["study_plans"]:
            for plan in data["study_plans"][:3]:
                st.caption(f"{plan['subject']} · {plan['topic']}")
                st.progress(int(plan["progress"]) / 100)
        else:
            st.info("Add your first topic in the study planner.")

elif page == "Tasks":
    page_heading("Tasks", "Keep the next small steps somewhere you can see them.")
    with st.form("add_task_form", clear_on_submit=True):
        st.subheader("Add a task")
        title = st.text_input("Task", placeholder="e.g. Finish the lab report")
        first, second = st.columns(2)
        with first:
            priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        with second:
            due_date = st.date_input("Due date (optional)", value=None, format="YYYY-MM-DD")
        submitted = st.form_submit_button("＋  Add task", type="primary")
    if submitted:
        if title.strip():
            add_task(title, priority, due_date)
            st.rerun()
        else:
            st.error("Give your task a short name before adding it.")

    st.subheader("Your list")
    if not data["tasks"]:
        st.info("No tasks yet. Add one above to get started.")
    for task in list(data["tasks"]):
        row = st.columns([0.08, 0.64, 0.16, 0.12])
        checked = row[0].checkbox("Done", value=task["completed"], key=f"task_done_{task['id']}", label_visibility="collapsed")
        if checked != task["completed"]:
            task["completed"] = checked
            persist()
        title_style = "text-decoration:line-through;color:#a5a3bd" if task["completed"] else "color:#f3f1ff"
        row[1].markdown(f"<span style='{title_style}'>{task['title']}</span>", unsafe_allow_html=True)
        row[2].caption(task["priority"] + (f" · {task['due_date']}" if task["due_date"] else ""))
        if row[3].button("🗑", key=f"task_delete_{task['id']}", help="Delete task"):
            data["tasks"] = [item for item in data["tasks"] if item["id"] != task["id"]]
            persist()
            st.rerun()

elif page == "Study planner":
    page_heading("Study planner", "Break big subjects into clear, trackable topics.")
    with st.form("add_study_form", clear_on_submit=True):
        st.subheader("Plan a study topic")
        subject = st.text_input("Subject", placeholder="e.g. Computer Science")
        topic = st.text_input("Topic", placeholder="e.g. Recursion")
        first, second = st.columns(2)
        with first:
            deadline = st.date_input("Deadline (optional)", value=None, format="YYYY-MM-DD")
        with second:
            progress = st.slider("Starting progress", 0, 100, 0, format="%d%%")
        submitted = st.form_submit_button("＋  Add to planner", type="primary")
    if submitted:
        if subject.strip() and topic.strip():
            data["study_plans"].append(
                {
                    "id": str(uuid4()),
                    "subject": subject.strip(),
                    "topic": topic.strip(),
                    "deadline": deadline.isoformat() if deadline else "",
                    "progress": progress,
                }
            )
            persist()
            st.rerun()
        else:
            st.error("Add both a subject and a topic so your plan is easy to find.")

    st.subheader("Topics in progress")
    if not data["study_plans"]:
        st.info("Your planner is ready when you are. Add a subject and topic above.")
    for plan in list(data["study_plans"]):
        with st.container(border=True):
            detail = f" · Deadline {plan['deadline']}" if plan["deadline"] else ""
            st.markdown(f"**{plan['subject']}**  ·  {plan['topic']}{detail}")
            control, remove = st.columns([0.85, 0.15])
            new_progress = control.slider(
                "Progress", 0, 100, int(plan["progress"]), format="%d%%", key=f"study_progress_{plan['id']}"
            )
            if new_progress != plan["progress"]:
                plan["progress"] = new_progress
                persist()
            if remove.button("Remove", key=f"study_delete_{plan['id']}"):
                data["study_plans"] = [item for item in data["study_plans"] if item["id"] != plan["id"]]
                persist()
                st.rerun()

elif page == "Habits":
    page_heading("Daily habits", "A gentle check-in for the routines you want to keep.")
    st.markdown(f"### Today · {today.strftime('%A, %B %d')}")
    today_log = data["habit_logs"].setdefault(today_key, {})
    if not data["habits"]:
        st.info("Add a habit below to create your daily check-in.")
    for habit in list(data["habits"]):
        habit_columns = st.columns([0.1, 0.72, 0.18])
        habit_columns[0].markdown(f"### {habit['icon']}")
        habit_columns[1].markdown(f"**{habit['name']}**")
        done = habit_columns[2].checkbox(
            "Done today", value=today_log.get(habit["id"], False), key=f"habit_{today_key}_{habit['id']}"
        )
        if done != today_log.get(habit["id"], False):
            today_log[habit["id"]] = done
            persist()

    checked_today = sum(today_log.get(habit["id"], False) for habit in data["habits"])
    if data["habits"]:
        st.progress(checked_today / len(data["habits"]), text=f"{checked_today} of {len(data['habits'])} habits checked in")

    with st.expander("＋  Add a habit"):
        with st.form("add_habit_form", clear_on_submit=True):
            habit_name = st.text_input("Habit name", placeholder="e.g. Take a short walk")
            habit_icon = st.selectbox("Icon", ["🌱", "📖", "🧠", "💻", "💧", "🏃", "✍️"])
            submitted = st.form_submit_button("Add habit")
        if submitted:
            if habit_name.strip():
                data["habits"].append({"id": str(uuid4()), "name": habit_name.strip(), "icon": habit_icon})
                persist()
                st.rerun()
            else:
                st.error("Enter a habit name first.")

    if data["habits"]:
        with st.expander("Manage habits"):
            for habit in list(data["habits"]):
                habit_row = st.columns([0.85, 0.15])
                habit_row[0].write(f"{habit['icon']}  {habit['name']}")
                if habit_row[1].button("🗑", key=f"habit_delete_{habit['id']}", help="Delete habit"):
                    data["habits"] = [item for item in data["habits"] if item["id"] != habit["id"]]
                    for log in data["habit_logs"].values():
                        log.pop(habit["id"], None)
                    persist()
                    st.rerun()

elif page == "Progress":
    page_heading("Your progress", "A snapshot of the effort you have already put in.")
    task_total = len(data["tasks"])
    task_done = sum(task["completed"] for task in data["tasks"])
    task_percent = round(task_done / task_total * 100) if task_total else 0
    study_total = len(data["study_plans"])
    study_average = round(sum(int(plan["progress"]) for plan in data["study_plans"]) / study_total) if study_total else 0
    first, second = st.columns(2)
    with first:
        st.subheader("Task completion")
        st.metric("Completed", f"{task_done} of {task_total}", f"{task_percent}%")
        st.bar_chart(
            [{"Status": "Completed", "Tasks": task_done}, {"Status": "To do", "Tasks": task_total - task_done}],
            x="Status",
            y="Tasks",
            color="#c7b7ff",
        )
    with second:
        st.subheader("Study progress")
        st.metric("Average topic progress", f"{study_average}%")
        if data["study_plans"]:
            chart_data = [
                {"Topic": f"{plan['subject']}: {plan['topic']}", "Progress": int(plan["progress"])}
                for plan in data["study_plans"]
            ]
            st.bar_chart(chart_data, x="Topic", y="Progress", color="#8de0c1")
        else:
            st.info("Add study topics to see your progress chart.")

    st.subheader("Habit history")
    if data["habit_logs"]:
        history = []
        for day, log in sorted(data["habit_logs"].items()):
            history.append({"Date": day, "Habits completed": sum(log.values())})
        st.bar_chart(history, x="Date", y="Habits completed", color="#ff9fbd")
    else:
        st.info("Check in with a habit to start building your history.")