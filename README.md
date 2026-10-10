# LifeOS — My Student Life Dashboard

LifeOS is a local, beginner-friendly student dashboard built with Python and Streamlit. Keep track of assignments, plan study topics, check in with daily habits, and see your progress in one place. It uses no paid APIs, accounts, or secret keys.

## Features

- A dated overview with a rotating motivational quote and a quick look at your day.
- A task list where you can add tasks, set priority and optional due dates, mark tasks done, and delete them.
- A study planner for subjects, topics, optional deadlines, and adjustable progress.
- A daily habit tracker with editable habits and a record for each date.
- Progress charts for task completion, study topics, and habit history.
- Local JSON storage. Your data is saved in `data/lifeos_data.json` in this project and is still there after you close and reopen the app.
- Example tasks, study topics, and habits appear the first time you run the app.

## Run in GitHub Codespaces

1. Open this repository in a GitHub Codespace.
2. Open the terminal from **Terminal → New Terminal**.
3. (Recommended) Create and activate a virtual environment:

	```bash
	python -m venv .venv
	source .venv/bin/activate
	```

	If your terminal uses a different shell, activate the environment using that shell's equivalent command. You can skip this step in a disposable Codespace.

4. Install the app dependency:

	```bash
	python -m pip install -r requirements.txt
	```

5. Start the dashboard:

	```bash
	python -m streamlit run app.py
	```

6. When Codespaces offers to open the forwarded port (usually **8501**), choose **Open in Browser**.

To stop the app, focus the terminal and press `Ctrl+C`.

## Run on your computer

Install Python 3.9 or later, open a terminal in this project folder, then run the virtual-environment, dependency-install, and Streamlit commands above. Open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Project files

```text
app.py          Streamlit pages, forms, charts, and styling
storage.py      Starter data and local JSON load/save helpers
requirements.txt
data/           Created automatically when the first change is saved
```

## How the code works

- Streamlit reruns `app.py` after each interaction. `st.session_state` keeps the loaded dashboard data available between those reruns.
- `storage.py` reads and writes that data as ordinary JSON. The file is created the first time you add or change something. The app can be customized without a database or internet service.
- The sidebar switches between five pages. Each page reads and updates the same data, so changes appear across the dashboard.
- Habit check-ins are stored by date. The habit history chart shows the number of completed habits for each day that has a check-in.

## Your data and troubleshooting

- Your saved data is local to the project. Keep `data/lifeos_data.json` if you want to keep it, or make a copy before experimenting with the file.
- If a save fails, check that the project folder is writable and that you have disk space. The app shows a message with the error.
- If the JSON save file is invalid, the app displays a warning and loads starter data. Check or restore `data/lifeos_data.json` before making further changes, since saving new changes will replace the invalid file.
- If `streamlit` is not found, make sure the virtual environment is activated and run `python -m pip install -r requirements.txt` again.
- If port 8501 is already in use, start Streamlit on another port: `python -m streamlit run app.py --server.port 8502`.

## Ideas to customize

Try changing the example habits and quote list in `app.py` or the starter tasks and subjects in `storage.py`. Run the app again to see your changes. Python comments and small functions are included near the parts that save data and build pages.
