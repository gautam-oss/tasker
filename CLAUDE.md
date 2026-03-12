# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🔧 Common Development Commands

### Installation
```bash
# Option A - Development install (recommended)
git clone https://github.com/gautam-oss/tasker.git
cd tasker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# Option B - Dependencies only
pip install -r requirements.txt
```

### CLI Usage (after installation)
```bash
# Add a task
tasker add-task "Buy groceries"
tasker add-task "Write unit tests"

# List all tasks
tasker list-tasks

# List pending tasks only
tasker list-tasks --pending

# Mark task as complete
tasker complete-task 1

# Delete a task
tasker delete-task 2

# Get help
tasker --help
tasker add-task --help
```

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/test_manager.py::test_add_task -v

# Run tests with coverage (if configured)
# pytest --cov=tasker tests/
```

### Using as a Python Library
```python
from tasker import TaskManager

manager = TaskManager()
task = manager.add_task("Learn Python packaging")
print(task.task_id, task.title)

manager.complete_task(task.task_id)

for t in manager.list_tasks():
    status = "✔" if t.completed else "○"
    print(f"[{status}] {t.task_id}. {t.title}")
```

## 🏗️ Code Architecture

### Project Structure
```
tasker/
├── pyproject.toml          ← Package config & dependencies (entry point defined here)
├── requirements.txt        ← Flat dependencies list
├── src/
│   └── tasker/
│       ├── __init__.py     ← Exposes TaskManager for library use
│       ├── manager.py      ← Core logic: Task class + TaskManager (JSON persistence)
│       └── cli.py          ← Click CLI wrapper with colored output
└── tests/
    └── test_manager.py     ← Unit tests for TaskManager
```

### Key Components
- **manager.py**: Contains `Task` dataclass and `TaskManager` class handling:
  - Task CRUD operations (add, list, complete, delete)
  - Automatic JSON serialization to `~/.tasker_data.json`
  - Task ID generation and persistence

- **cli.py**: Click-based command-line interface that:
  - Maps CLI commands to TaskManager methods
  - Provides colored terminal output and user feedback
  - Handles argument parsing and validation

- **pyproject.toml**: Defines:
  - Package metadata and dependencies (`click`)
  - Console script entry point: `tasker = tasker.cli:main`

- **Data Storage**: Tasks persisted in `~/.tasker_data.json` as JSON array of task objects

### Data Flow
1. User runs CLI command → `cli.py` parses arguments
2. `cli.py` invokes corresponding `TaskManager` method
3. `TaskManager` performs operation on in-memory task list
4. Changes automatically saved to `~/.tasker_data.json`
5. Results formatted and displayed via `cli.py`

## 📝 Notes
- The package is designed for simplicity: single JSON file storage, no external database
- All state is stored in the user's home directory (`~/.tasker_data.json`)
- Tests cover core functionality of TaskManager class
- Development uses standard Python tooling: venv, pytest, pip