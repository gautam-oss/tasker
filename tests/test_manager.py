"""
tests/test_manager.py
Unit tests for the TaskManager core logic.
Run with:  pytest
"""

import os
import json
import pytest
from tasker.manager import Task, TaskManager


@pytest.fixture
def tmp_manager(tmp_path):
    """Return a TaskManager that saves to a temporary file."""
    data_file = str(tmp_path / "tasks.json")
    return TaskManager(data_file=data_file)


# ------------------------------------------------------------------ #
#  add_task                                                            #
# ------------------------------------------------------------------ #

def test_add_task_creates_task(tmp_manager):
    task = tmp_manager.add_task("Buy milk")
    assert task.task_id == 1
    assert task.title == "Buy milk"
    assert task.completed is False


def test_add_task_increments_id(tmp_manager):
    t1 = tmp_manager.add_task("First")
    t2 = tmp_manager.add_task("Second")
    assert t2.task_id == t1.task_id + 1


def test_add_task_rejects_empty_title(tmp_manager):
    with pytest.raises(ValueError):
        tmp_manager.add_task("   ")


def test_add_task_persists_to_disk(tmp_manager):
    tmp_manager.add_task("Persisted task")
    # Load a fresh manager from the same file
    manager2 = TaskManager(data_file=tmp_manager.data_file)
    tasks = manager2.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Persisted task"


# ------------------------------------------------------------------ #
#  list_tasks                                                          #
# ------------------------------------------------------------------ #

def test_list_tasks_empty(tmp_manager):
    assert tmp_manager.list_tasks() == []


def test_list_tasks_returns_all(tmp_manager):
    tmp_manager.add_task("A")
    tmp_manager.add_task("B")
    assert len(tmp_manager.list_tasks()) == 2


def test_list_tasks_pending_only(tmp_manager):
    tmp_manager.add_task("Done task")
    tmp_manager.add_task("Pending task")
    tmp_manager.complete_task(1)
    pending = tmp_manager.list_tasks(show_completed=False)
    assert len(pending) == 1
    assert pending[0].title == "Pending task"


# ------------------------------------------------------------------ #
#  complete_task                                                        #
# ------------------------------------------------------------------ #

def test_complete_task_marks_done(tmp_manager):
    task = tmp_manager.add_task("Finish report")
    completed = tmp_manager.complete_task(task.task_id)
    assert completed.completed is True


def test_complete_task_raises_for_unknown_id(tmp_manager):
    with pytest.raises(ValueError):
        tmp_manager.complete_task(999)


def test_complete_task_raises_if_already_done(tmp_manager):
    task = tmp_manager.add_task("Already done")
    tmp_manager.complete_task(task.task_id)
    with pytest.raises(ValueError):
        tmp_manager.complete_task(task.task_id)


# ------------------------------------------------------------------ #
#  delete_task                                                         #
# ------------------------------------------------------------------ #

def test_delete_task_removes_task(tmp_manager):
    task = tmp_manager.add_task("Remove me")
    tmp_manager.delete_task(task.task_id)
    assert tmp_manager.list_tasks() == []


def test_delete_task_raises_for_unknown_id(tmp_manager):
    with pytest.raises(ValueError):
        tmp_manager.delete_task(42)