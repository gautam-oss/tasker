# 📋 Tasker

A beginner-friendly Python package for managing tasks from the command line.  
Tasks are stored in `~/.tasker_data.json` so they survive between terminal sessions.

---

## Project Structure

```
tasker/
├── pyproject.toml          ← package config & dependencies
├── README.md
├── src/
│   └── tasker/
│       ├── __init__.py     ← public API
│       ├── manager.py      ← core logic (TaskManager class)
│       └── cli.py          ← Click CLI commands
└── tests/
    └── test_manager.py     ← unit tests
```

---

## Installation

From the project root, install the package in **editable mode** (changes to the
source code take effect immediately without re-installing):

```bash
pip install -e .
```

---

## CLI Usage

After installation the `tasker` command is available in your terminal.

### Add a task
```bash
tasker add-task "Buy groceries"
tasker add-task "Write unit tests"
```

### List all tasks
```bash
tasker list-tasks
```

### List only pending (not completed) tasks
```bash
tasker list-tasks --pending
```

### Mark a task as complete
```bash
tasker complete-task 1
```

### Delete a task
```bash
tasker delete-task 2
```

### Built-in help
```bash
tasker --help
tasker add-task --help
```

---

## Using Tasker as a Python Library

You can also use `TaskManager` directly in your own Python code:

```python
from tasker import TaskManager

manager = TaskManager()              # loads from ~/.tasker_data.json

task = manager.add_task("Learn Python packaging")
print(task.task_id, task.title)     # 1  Learn Python packaging

manager.complete_task(task.task_id)

for t in manager.list_tasks():
    status = "✔" if t.completed else "○"
    print(f"[{status}] {t.task_id}. {t.title}")
```

---

## Running Tests

```bash
pip install pytest
pytest tests/
```

---

## How It Works

| File | Role |
|------|------|
| `manager.py` | `Task` dataclass + `TaskManager` (add / list / complete / delete). Reads and writes `~/.tasker_data.json`. |
| `cli.py` | Click commands that wrap `TaskManager` methods and display coloured output. |
| `pyproject.toml` | Declares `click` as a dependency and registers the `tasker` console script. |