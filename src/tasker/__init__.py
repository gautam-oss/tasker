"""
tasker
~~~~~~
A simple task management framework with a CLI.

Public API:
    from tasker import TaskManager
    from tasker.manager import Task
"""

from tasker.manager import Task, TaskManager

__all__ = ["TaskManager", "Task"]
__version__ = "0.1.0"