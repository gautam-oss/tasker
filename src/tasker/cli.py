"""
tasker/cli.py
Command-line interface built with Click.

Available commands:
    tasker add-task   "Buy groceries"
    tasker list-tasks
    tasker list-tasks --pending
    tasker complete-task 1
    tasker delete-task 1
"""

import click
from tasker.manager import TaskManager


# Shared manager instance (re-used across all commands in one invocation)
pass_manager = click.make_pass_decorator(TaskManager, ensure=True)


@click.group()
@click.pass_context
def main(ctx: click.Context):
    """
    Tasker — a simple task management CLI.

    Tasks are saved in ~/.tasker_data.json so they persist between sessions.
    """
    # Store the TaskManager in Click's context so every sub-command can use it
    ctx.obj = TaskManager()


# ------------------------------------------------------------------ #
#  add-task                                                            #
# ------------------------------------------------------------------ #

@main.command("add-task")
@click.argument("title")
@pass_manager
def add_task(manager: TaskManager, title: str):
    """Add a new task.

    TITLE is the description of the task (wrap in quotes if it contains spaces).

    Example:

        tasker add-task "Write unit tests"
    """
    try:
        task = manager.add_task(title)
        click.echo(
            click.style(f"✅ Task added!", fg="green", bold=True)
            + f"  [ID: {task.task_id}]  {task.title}"
        )
    except ValueError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))
        raise SystemExit(1)


# ------------------------------------------------------------------ #
#  list-tasks                                                          #
# ------------------------------------------------------------------ #

@main.command("list-tasks")
@click.option(
    "--pending",
    is_flag=True,
    default=False,
    help="Show only tasks that are NOT yet completed.",
)
@pass_manager
def list_tasks(manager: TaskManager, pending: bool):
    """List all tasks (or only pending ones with --pending).

    Examples:

        tasker list-tasks

        tasker list-tasks --pending
    """
    tasks = manager.list_tasks(show_completed=not pending)

    if not tasks:
        click.echo(click.style("No tasks found.", fg="yellow"))
        return

    click.echo(click.style(f"\n{'ID':>4}  {'Status':<12}  {'Created':<20}  Title", bold=True))
    click.echo("─" * 70)

    for task in tasks:
        status = click.style("✔ Done", fg="green") if task.completed else click.style("○ Pending", fg="cyan")
        click.echo(f"{task.task_id:>4}  {status:<12}  {task.created_at:<20}  {task.title}")

    click.echo()  # blank line at the end


# ------------------------------------------------------------------ #
#  complete-task                                                       #
# ------------------------------------------------------------------ #

@main.command("complete-task")
@click.argument("task_id", type=int)
@pass_manager
def complete_task(manager: TaskManager, task_id: int):
    """Mark a task as completed.

    TASK_ID is the numeric ID shown in 'list-tasks'.

    Example:

        tasker complete-task 3
    """
    try:
        task = manager.complete_task(task_id)
        click.echo(
            click.style(f"🎉 Task completed!", fg="green", bold=True)
            + f"  [ID: {task.task_id}]  {task.title}"
        )
    except ValueError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))
        raise SystemExit(1)


# ------------------------------------------------------------------ #
#  delete-task                                                         #
# ------------------------------------------------------------------ #

@main.command("delete-task")
@click.argument("task_id", type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this task?")
@pass_manager
def delete_task(manager: TaskManager, task_id: int):
    """Delete a task permanently.

    TASK_ID is the numeric ID shown in 'list-tasks'.

    Example:

        tasker delete-task 3
    """
    try:
        task = manager.delete_task(task_id)
        click.echo(
            click.style(f"🗑️  Task deleted.", fg="yellow")
            + f"  [ID: {task.task_id}]  {task.title}"
        )
    except ValueError as e:
        click.echo(click.style(f"❌ Error: {e}", fg="red"))
        raise SystemExit(1)