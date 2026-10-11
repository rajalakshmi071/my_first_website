"""LifeOS — My Student Life Dashboard

Save this as app.py, then run: streamlit run app.py
Dashboard data is stored in lifeos_data.json in the same folder.
"""

import json
import random
from datetime import date, timedelta
from pathlib import Path

import streamlit as st


DATA_FILE = Path(__file__).with_name("lifeos_data.json")
QUOTES = [
    "Small steps every day add up to big results.",
    "You do not have to be perfect. You just have to begin.",
    "The secret of getting ahead is getting started.",
    "Progress is progress, no matter how small.",
    "Your future is created by what you do today.",
]


def save_data(data):
    """Save dashboard information as readable JSON on this computer."""
    try:
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except OSError as error:
        st.error(f"Couldn't save your data: {error}")


def load_data():
    """Load saved information, or prepare examples on the first visit."""
    examples = {
        "tasks": [
            {"id": 1, "title": "Review today's lecture notes", "done": False},
            {"id": 2, "title": "Plan the week ahead", "done": True},
        ],
        "plans": [{
            "id": 3, "subject": "Computer Science", "topic": "Practice Python functions",
            "deadline": (date.today() + timedelta(days=2)).isoformat(), "done": False,
        }],
        "habits": [
            {"id": 4, "name": "Read for 20 minutes", "completed_dates": []},
            {"id": 5, "name": "Study without distractions", "completed_dates": []},
            {"id": 6, "name": "Practise coding", "completed_dates": []},
        ],
        "next_id": 7,
    }
    if not DATA_FILE.exists():
        save_data(examples)
        return examples
    try:
        saved = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        # Fill in any missing sections so a hand-edited file is less likely to break.
        for key, value in examples.items():
            saved.setdefault(key, value)
        return saved
    except (OSError, json.JSONDecodeError) as error:
        st.error(f"Couldn't read {DATA_FILE.name}: {error}. Starting with sample data.")
        return examples


st.set_page_config(page_title="LifeOS — My Student Life Dashboard", page_icon="🌙", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
.stApp {background:linear-gradient(145deg,#0b1020,#11172a 58%,#17152c);color:#f4f2ff}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
h1,h2,h3{font-family:'Manrope',sans-serif!important;letter-spacing:-.03em}
[data-testid="stSidebar"]{background:#101629;border-right:1px solid #252b43}
[data-testid="stMetric"]{background:#171e33;border:1px solid #292f49;padding:18px;border-radius:18px}
div[data-testid="stForm"]{background:#171e33;padding:18px;border:1px solid #292f49;border-radius:18px}
.hero{padding:26px 30px;border:1px solid #343050;border-radius:22px;background:linear-gradient(120deg,#211f3c,#171e33 75%);margin:8px 0 22px}
.hero p{color:#b8b5ce;margin:6px 0 0}.quote{padding:16px 20px;border-left:3px solid #b8a5ff;background:#191c32;border-radius:0 14px 14px 0;color:#d8d2f3;font-style:italic}
.stButton button[kind="primary"]{background:#9b87f5;border-color:#9b87f5;color:#17142a;font-weight:700}.stButton button{border-radius:10px}
</style>
""", unsafe_allow_html=True)

if "lifeos" not in st.session_state:
    st.session_state.lifeos = load_data()
data = st.session_state.lifeos
today = date.today()
today_key = today.isoformat()

with st.sidebar:
    st.markdown("# 🌙 LifeOS")
    st.caption("Your space to plan, focus, and grow.")
    page = st.radio("Navigate", ["🏠 Dashboard", "✅ Tasks", "📚 Study planner", "🌱 Habits", "📈 Progress"], label_visibility="collapsed")
    st.divider()
    st.caption("✨ Your data is stored locally on this device.")

task_done = sum(task["done"] for task in data["tasks"])
plan_done = sum(plan["done"] for plan in data["plans"])
habits_done = sum(today_key in habit["completed_dates"] for habit in data["habits"])

if page == "🏠 Dashboard":
    st.markdown(f'<div class="hero"><h1>Good to see you 👋</h1><p>{today.strftime("%A, %B %d, %Y")} · Make today count, one step at a time.</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="quote">“{random.choice(QUOTES)}”</div>', unsafe_allow_html=True)
    st.write("")
    first, second, third = st.columns(3)
    first.metric("✅ Tasks completed", f"{task_done} / {len(data['tasks'])}")
    second.metric("📚 Topics completed", f"{plan_done} / {len(data['plans'])}")
    third.metric("🌱 Habits today", f"{habits_done} / {len(data['habits'])}")
    left, right = st.columns(2)
    with left:
        st.subheader("🎯 Up next")
        pending = [task for task in data["tasks"] if not task["done"]]
        if pending:
            for task in pending[:5]:
                st.write(f"○  {task['title']}")
        else:
            st.info("You're all caught up. Add something new when you're ready!")
    with right:
        st.subheader("📅 Study deadlines")
        upcoming = sorted((item for item in data["plans"] if not item["done"]), key=lambda item: item["deadline"])
        if upcoming:
            for item in upcoming[:5]:
                st.write(f"**{item['subject']}** · {item['topic']} — {item['deadline']}")
        else:
            st.info("No study topics planned yet.")

elif page == "✅ Tasks":
    st.title("✅ Task manager")
    st.caption("Capture the small things so you can focus on doing them.")
    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("What needs to get done?", placeholder="e.g. Submit my lab report")
        submitted = st.form_submit_button("＋ Add task", type="primary")
    if submitted:
        if title.strip():
            data["tasks"].append({"id": data["next_id"], "title": title.strip(), "done": False})
            data["next_id"] += 1
            save_data(data)
            st.rerun()
        else:
            st.warning("Please enter a task before adding it.")
    st.subheader("Your tasks")
    if not data["tasks"]:
        st.info("Your list is clear. Add your first task above.")
    for task in list(data["tasks"]):
        task_col, delete_col = st.columns([8, 1])
        checked = task_col.checkbox(task["title"], value=task["done"], key=f"task_{task['id']}")
        if checked != task["done"]:
            task["done"] = checked
            save_data(data)
        if delete_col.button("🗑️", key=f"delete_task_{task['id']}", help="Delete task"):
            data["tasks"] = [item for item in data["tasks"] if item["id"] != task["id"]]
            save_data(data)
            st.rerun()

elif page == "📚 Study planner":
    st.title("📚 Study planner")
    st.caption("Turn big subjects into clear topics with a deadline.")
    with st.form("plan_form", clear_on_submit=True):
        subject = st.text_input("Subject", placeholder="e.g. Biology")
        topic = st.text_input("Topic to study", placeholder="e.g. Cell structure")
        deadline = st.date_input("Deadline", value=today + timedelta(days=7))
        submitted = st.form_submit_button("＋ Add to planner", type="primary")
    if submitted:
        if subject.strip() and topic.strip():
            data["plans"].append({"id": data["next_id"], "subject": subject.strip(), "topic": topic.strip(), "deadline": deadline.isoformat(), "done": False})
            data["next_id"] += 1
            save_data(data)
            st.rerun()
        else:
            st.warning("Please fill in both the subject and study topic.")
    st.subheader("Study topics")
    if not data["plans"]:
        st.info("No topics planned yet. Add one above to get started.")
    for plan in list(data["plans"]):
        plan_col, delete_col = st.columns([8, 1])
        plan_col.markdown(f"**{plan['subject']}** — {plan['topic']} · Due {plan['deadline']}")
        checked = plan_col.checkbox("Mark topic complete", value=plan["done"], key=f"plan_{plan['id']}")
        if checked != plan["done"]:
            plan["done"] = checked
            save_data(data)
        if delete_col.button("🗑️", key=f"delete_plan_{plan['id']}", help="Delete topic"):
            data["plans"] = [item for item in data["plans"] if item["id"] != plan["id"]]
            save_data(data)
            st.rerun()

elif page == "🌱 Habits":
    st.title("🌱 Daily habit tracker")
    st.caption(f"A check-in for {today.strftime('%A, %B %d')} — consistency beats intensity.")
    with st.form("habit_form", clear_on_submit=True):
        name = st.text_input("A habit you want to build", placeholder="e.g. Take a short walk")
        submitted = st.form_submit_button("＋ Add habit", type="primary")
    if submitted:
        if name.strip():
            data["habits"].append({"id": data["next_id"], "name": name.strip(), "completed_dates": []})
            data["next_id"] += 1
            save_data(data)
            st.rerun()
        else:
            st.warning("Please enter a habit name first.")
    st.subheader("Today's habits")
    if not data["habits"]:
        st.info("Add a habit above to start your daily check-in.")
    for habit in list(data["habits"]):
        habit_col, delete_col = st.columns([8, 1])
        was_done = today_key in habit["completed_dates"]
        checked = habit_col.checkbox(habit["name"], value=was_done, key=f"habit_{habit['id']}_{today_key}")
        if checked != was_done:
            if checked:
                habit["completed_dates"].append(today_key)
            else:
                habit["completed_dates"].remove(today_key)
            save_data(data)
        if delete_col.button("🗑️", key=f"delete_habit_{habit['id']}", help="Delete habit"):
            data["habits"] = [item for item in data["habits"] if item["id"] != habit["id"]]
            save_data(data)
            st.rerun()
    if data["habits"]:
        st.progress(habits_done / len(data["habits"]))
        st.caption(f"{habits_done} of {len(data['habits'])} habits complete today")

else:
    st.title("📈 Your progress")
    st.caption("Celebrate what you've done and plan your next step.")
    left, right = st.columns(2)
    with left:
        st.subheader("Task progress")
        st.bar_chart({"Tasks": {"Completed": task_done, "To do": len(data["tasks"]) - task_done}})
        if data["tasks"]:
            st.progress(task_done / len(data["tasks"]))
            st.caption(f"{round(100 * task_done / len(data['tasks']))}% of tasks complete")
        else:
            st.info("Add tasks to see your progress chart.")
    with right:
        st.subheader("Study progress")
        st.bar_chart({"Study topics": {"Completed": plan_done, "To study": len(data["plans"]) - plan_done}})
        if data["plans"]:
            st.progress(plan_done / len(data["plans"]))
            st.caption(f"{round(100 * plan_done / len(data['plans']))}% of topics complete")
        else:
            st.info("Add study topics to see your progress chart.")
    st.subheader("🌱 Habit check-ins — last 7 days")
    if data["habits"]:
        recent_days = [today - timedelta(days=offset) for offset in reversed(range(7))]
        chart = {"Completed habits": {day.strftime("%a"): sum(day.isoformat() in habit["completed_dates"] for habit in data["habits"]) for day in recent_days}}
        st.bar_chart(chart)
    else:
        st.info("Add habits and check them off to see weekly activity.")

st.markdown("<p style='text-align:center;color:#aaa9c2'>Made for your next small step. Keep going ✨</p>", unsafe_allow_html=True)