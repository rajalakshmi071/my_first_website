"""Small JSON storage helpers for the LifeOS dashboard."""

import json
from pathlib import Path
from uuid import uuid4


DATA_FILE = Path(__file__).parent / "data" / "lifeos_data.json"


def starter_data():
    """Return example data used the first time the app is opened."""
    return {
        "tasks": [
            {
                "id": str(uuid4()),
                "title": "Review data structures notes",
                "priority": "High",
                "due_date": "",
                "completed": False,
            },
            {
                "id": str(uuid4()),
                "title": "Submit programming lab",
                "priority": "Medium",
                "due_date": "",
                "completed": True,
            },
        ],
        "study_plans": [
            {
                "id": str(uuid4()),
                "subject": "Computer Science",
                "topic": "Python loops and functions",
                "deadline": "",
                "progress": 35,
            },
            {
                "id": str(uuid4()),
                "subject": "Mathematics",
                "topic": "Introductory calculus",
                "deadline": "",
                "progress": 60,
            },
        ],
        "habits": [
            {"id": str(uuid4()), "name": "Read for 20 minutes", "icon": "📖"},
            {"id": str(uuid4()), "name": "Study session", "icon": "🧠"},
            {"id": str(uuid4()), "name": "Practise coding", "icon": "💻"},
        ],
        "habit_logs": {},
    }


def load_data():
    """Load saved data, or provide starter data when no save exists."""
    if not DATA_FILE.exists():
        return starter_data(), None

    try:
        with DATA_FILE.open("r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        # Keep older or partially edited save files usable as the app grows.
        defaults = starter_data()
        for key, value in defaults.items():
            data.setdefault(key, value)
        return data, None
    except (OSError, json.JSONDecodeError, AttributeError) as error:
        return starter_data(), f"Couldn't read your saved data ({error}). Starter data is shown for now. Check {DATA_FILE} before saving again."


def save_data(data):
    """Write the latest dashboard data to a local JSON file."""
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with DATA_FILE.open("w", encoding="utf-8") as data_file:
            json.dump(data, data_file, indent=2, ensure_ascii=False)
        return None
    except OSError as error:
        return f"Couldn't save your changes: {error}. Check that the project folder is writable."