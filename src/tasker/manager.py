"""
tasker/manager.py
Core task management logic — read/write tasks to a JSON file.
"""

import json
import os
from datetime import datetime
from typing import List, Optional


# Default path for storing tasks (in the user's home directory)
DEFAULT_DATA_FILE = os.path.join(os.path.expanduser("~"), ".tasker_data.json")


class Task:
    """Represents a single task."""

    def __init__(self, task_id: int, title: str, completed: bool = False, created_at: str = ""):
        self.task_id = task_id
        self.title = title
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """Convert task to a dictionary (for saving to JSON)."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Create a Task from a dictionary (for loading from JSON)."""
        return Task(
            task_id=data["task_id"],
            title=data["title"],
            completed=data.get("completed", False),
            created_at=data.get("created_at", ""),
        )


class TaskManager:
    """
    Manages a list of tasks stored in a JSON file.

    Usage:
        manager = TaskManager()
        manager.add_task("Buy groceries")
        manager.list_tasks()
        manager.complete_task(1)
    """

    def __init__(self, data_file: str = DEFAULT_DATA_FILE):
        self.data_file = data_file
        self._tasks: List[Task] = []
        self._load()

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _load(self):
        """Load tasks from the JSON file. Creates an empty file if missing."""
        if not os.path.exists(self.data_file):
            self._tasks = []
            return

        with open(self.data_file, "r", encoding="utf-8") as f:
            try:
                raw = json.load(f)
                self._tasks = [Task.from_dict(item) for item in raw]
            except (json.JSONDecodeError, KeyError):
                # Corrupted file — start fresh
                self._tasks = []

    def _save(self):
        """Persist tasks to the JSON file."""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self._tasks], f, indent=2)

    def _next_id(self) -> int:
        """Return the next available task ID."""
        if not self._tasks:
            return 1
        return max(t.task_id for t in self._tasks) + 1

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def add_task(self, title: str) -> Task:
        """
        Add a new task.

        Args:
            title: A short description of the task.

        Returns:
            The newly created Task object.
        """
        if not title.strip():
            raise ValueError("Task title cannot be empty.")

        task = Task(task_id=self._next_id(), title=title.strip())
        self._tasks.append(task)
        self._save()
        return task

    def list_tasks(self, show_completed: bool = True) -> List[Task]:
        """
        Return all tasks, optionally filtering out completed ones.

        Args:
            show_completed: If False, only pending tasks are returned.

        Returns:
            A list of Task objects.
        """
        if show_completed:
            return list(self._tasks)
        return [t for t in self._tasks if not t.completed]

    def complete_task(self, task_id: int) -> Task:
        """
        Mark a task as completed.

        Args:
            task_id: The ID of the task to complete.

        Returns:
            The updated Task object.

        Raises:
            ValueError: If no task with the given ID exists or it is already done.
        """
        for task in self._tasks:
            if task.task_id == task_id:
                if task.completed:
                    raise ValueError(f"Task {task_id} is already completed.")
                task.completed = True
                self._save()
                return task

        raise ValueError(f"No task found with ID {task_id}.")

    def delete_task(self, task_id: int) -> Task:
        """
        Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            The deleted Task object.

        Raises:
            ValueError: If no task with the given ID exists.
        """
        for i, task in enumerate(self._tasks):
            if task.task_id == task_id:
                removed = self._tasks.pop(i)
                self._save()
                return removed

        raise ValueError(f"No task found with ID {task_id}.")