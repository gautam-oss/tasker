# 📋 Tasker

A beginner-friendly Python package for managing tasks from the command line.  
Built with **Python + Click**. Tasks are stored in `~/.tasker_data.json` so they survive between terminal sessions.

---

## 📁 Project Structure
```
tasker/
├── pyproject.toml          ← package config & dependencies
├── requirements.txt        ← dependencies list
├── README.md
├── LICENSE
├── src/
│   └── tasker/
│       ├── __init__.py     ← public API
│       ├── manager.py      ← core logic (TaskManager class)
│       └── cli.py          ← Click CLI commands
└── tests/
    └── test_manager.py     ← unit tests
```

---

## ⚙️ Installation

### Option A — Install as a package (recommended)
```bash
git clone https://github.com/gautam-oss/tasker.git
cd tasker
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -e .
```

### Option B — Install dependencies only
```bash
pip install -r requirements.txt
```

---

## 🚀 CLI Usage

After installation the `tasker` command is available anywhere in your terminal.

### ➕ Add a task
```bash
tasker add-task "Buy groceries"
tasker add-task "Write unit tests"
```

### 📋 List all tasks
```bash
tasker list-tasks
```

### 🔍 List only pending tasks
```bash
tasker list-tasks --pending
```

### ✅ Mark a task as complete
```bash
tasker complete-task 1
```

### 🗑️ Delete a task
```bash
tasker delete-task 2
```

### ❓ Built-in help
```bash
tasker --help
tasker add-task --help
```

---

## 🐍 Use as a Python Library
```python
from tasker import TaskManager

manager = TaskManager()

task = manager.add_task("Learn Python packaging")
print(task.task_id, task.title)   # 1  Learn Python packaging

manager.complete_task(task.task_id)

for t in manager.list_tasks():
    status = "✔" if t.completed else "○"
    print(f"[{status}] {t.task_id}. {t.title}")
```

---

## 💾 Data Storage

Tasks are saved to `~/.tasker_data.json` automatically. You can inspect it anytime:
```bash
cat ~/.tasker_data.json
```
```json
[
  {
    "task_id": 1,
    "title": "Buy groceries",
    "completed": true,
    "created_at": "2024-01-15 10:30:00"
  }
]
```

---

## 🧪 Running Tests
```bash
pip install pytest
pytest tests/ -v
```

Expected: **12 tests passing** ✅

---

## 🏗️ How It Works

| File | Role |
|------|------|
| `manager.py` | `Task` class + `TaskManager` — all logic for add/list/complete/delete, reads & writes JSON |
| `cli.py` | Click commands that wrap `TaskManager` with coloured terminal output |
| `__init__.py` | Makes `tasker` importable as a Python library |
| `pyproject.toml` | Declares `click` dependency, registers `tasker` console script entry point |
| `requirements.txt` | Flat list of dependencies for manual installs |

---

## 📜 License

MIT © 2026 Gautam Kumar