from datetime import datetime as dt
from dataclasses import dataclass
from pathlib import Path
import sys  # we import sys for stderr for loguru specifically
from typing import Annotated

from loguru import logger  # for logging
import questionary  # for cli prompts (confirm/selection/checkbox)

# rich things, for themes colors and tables
from rich.table import Table

# typer things
import typer

# other taskcli files, local to project
from taskcli import tasks
from taskcli import storage
from taskcli import config
from taskcli import constants as const
from taskcli import __version__ as taskcli_version


print = const.CONSOLE.print
app = typer.Typer()

tasklist_command = typer.Typer()
app.add_typer(tasklist_command, name="tasklist")


@dataclass
class ContextObject:
    config: config.Config
    tasklist: list[tasks.Task]
    tasklist_next_id: int
    tasklist_filepath: Path


@app.command("add")
def add_task(
    context: typer.Context,
    name: Annotated[list[str], typer.Argument(help="The name of the task")],
    status: Annotated[
        str | None,
        typer.Option("--status", "-s", help="The status of the task"),
    ] = None,  # the __init__ in task class will automatically add a default value
    priority: Annotated[
        str | None,
        typer.Option("--priority", "-p", help="The priority of the created task"),
    ] = None,  # let the add_task() get the default priority later
    duedate: Annotated[
        str | None,
        typer.Option(
            "--duedate",
            "-d",
            help="The duedate of the task. Enter a shortcut (tomorrow, next week), or a date (MM-DD-YYYY)",
        ),
    ] = None,
    tags: Annotated[
        str | None,
        typer.Option(
            "--tags",
            "-t",
            help="The tags of a task. Seperate multiple values with commas. (e.g. education, work)",
        ),
    ] = None,
) -> None:
    """Adds a task to the tasklist based on its name, priority, status, and duedates are set to default if not given.

    args are pretty self explanatory wont add them here, except for one:
    context (typer.Context): The context required to read and write to the needed global variables
    config (config.Config): only required to make the thing fill in the default priority if priority is not given by user
    """
    logger.info(
        "User invoked add command",
    )

    # literally just for the autocomplete really
    state: ContextObject = context.obj

    # to override the old list[str] so mypys happy
    joined_name: str = (" ".join(name)).strip()
    parsed_duedate: dt | None = None
    if duedate:
        parsed_duedate = tasks.parse_duedate(duedate)

    # the add_task function will deal with the missing values themselves
    logger.debug(
        "task manager add task command_params",
        command_params={
            "name": joined_name,
            "priority": priority,
            "status": status,
            "duedate": parsed_duedate,
            "tags": tags,
        },
    )
    state.tasklist_next_id, state.tasklist, new_task = tasks.add_task(
        joined_name,
        state.tasklist_next_id,
        state.tasklist,
        state.config,
        priority,
        status,
        parsed_duedate,
        tags,
    )
    logger.success("Appended new task to the tasklist")
    print(
        f"Successfully added new task '{new_task.name}' with ID {new_task.id} to the tasklist.",
        style="success",
    )
    display_tasks_table(context)
    tasks.save_tasks(state.tasklist_filepath, state.tasklist, state.tasklist_next_id)


@app.command("delete")
@app.command("remove", hidden=True)
@app.command("del", hidden=True)
@app.command("rm", hidden=True)
def delete_task(
    context: typer.Context,
    task_id: int,
) -> None:
    """Deletes a task based on its ID. Aliases: remove | del | rm

    Args:
        context (typer.Context): The context required to read and write to the needed global variables
        task_id (int): The task ID of the given task that the user wants to delete.
    """
    logger.info("User invoked 'delete' command")
    logger.debug("delete command params", command_params={"task_id": task_id})
    # literally just for the autocomplete really
    state: ContextObject = context.obj

    confirm_delete = (
        questionary.confirm(f"Are you sure you want to delete task ID {task_id}")
        .skip_if(
            not state.config.behaviour_settings.require_delete_confirmation,
            default=True,
        )
        .ask()
    )
    if not confirm_delete:
        print("Task deletion cancelled", style="info")
        logger.info("Task deletion was cancelled")
        return

    state.tasklist = tasks.delete_task(state.tasklist, task_id)
    logger.success(f"Succesfully deleted task with ID {task_id}")
    print(f"Successfully deleted task with ID {task_id}", style="success")
    display_tasks_table(context)

    tasks.save_tasks(state.tasklist_filepath, state.tasklist, state.tasklist_next_id)


@app.command("update")
def update_task(
    context: typer.Context,
    task_id: int,
    updated_name: Annotated[
        list[str] | None, typer.Option("--name", "-n", help="The updated name.")
    ] = None,
    updated_priority: Annotated[
        str | None,
        typer.Option("--priority", "-p", help="The updated priority."),
    ] = None,
    updated_duedate: Annotated[
        str | None,
        typer.Option(
            "--duedate",
            "-d",
            help="The duedate of the task. Enter a shortcut (tomorrow, next week), or a date (MM-DD-YYYY)",
        ),
    ] = None,
    updated_tags: Annotated[
        str | None,
        typer.Option(
            "--tags",
            "-t",
            help="The new tag(s) of the updated task.",
        ),
    ] = None,
) -> None:
    """Updates a specific task given task ID. You can update the priority and duedate of the task. Does not allow updating statuses, use the mark command instead.

    Args:
        context (typer.Context): The context required to read and write to the needed global variables
        Other args are pretty self explanatory.
    """
    logger.info(
        "User invoked 'update' command",
    )

    # literally just for the autocomplete really
    state: ContextObject = context.obj

    raw_updated_contents = {
        "name": updated_name,
        "priority": updated_priority,
        "duedate": updated_duedate or None,
        "tags": updated_tags or None,
    }
    logger.debug(
        "update command params",
        command_params={
            "task_id": task_id,
            "updated_name": updated_name,
            "updated_priority": updated_priority,
            "updated_duedate": updated_duedate,
            "updated_tags": updated_tags,
        },
    )

    state.tasklist = tasks.update_task(state.tasklist, task_id, raw_updated_contents)

    # if it reaches here, that means no errors occured
    logger.success(f"Successfully updated task with ID {task_id}")
    print(f"Successfully updated task with ID {task_id}", style="success")
    display_tasks_table(context)

    tasks.save_tasks(state.tasklist_filepath, state.tasklist, state.tasklist_next_id)


@app.command("mark")
def mark_task(
    context: typer.Context,
    task_id: Annotated[
        int, typer.Argument(help="The task id being marked as the upadted status")
    ],
    updated_status: Annotated[
        str, typer.Argument(help="The updated status of the task ID given by the user")
    ],
) -> None:
    """Updates a task's status based on task ID.

    Args:
        context (typer.Context): The context required to read and write to the needed global variables
        task_id (int): The task ID given by the user
        updated_status (str): The updated status given by the user
    """
    logger.info("User invoked 'mark' command")
    logger.debug(
        "mark command params",
        command_params={
            "task_id": task_id,
            "updated_status": updated_status,
        },
    )
    # literally just for the autocomplete really
    state: ContextObject = context.obj

    # dw, the task class setter will deal with invalid statuses
    state.tasklist = tasks.mark_task(state.tasklist, task_id, updated_status)
    logger.success(
        f"Successfully updated task ID {task_id} with status {updated_status}"
    )
    print(
        f"Successfully updated task ID {task_id} with status {updated_status}",
        style="success",
    )
    display_tasks_table(context)

    tasks.save_tasks(state.tasklist_filepath, state.tasklist, state.tasklist_next_id)


def _get_styled_attribute(
    attribute: str, task: tasks.Task, config: config.Config
) -> str:
    """It gets the rich styled string (with colors) associated with the attribute,
    required for display_tasks_table()

    NOTE: This is meant to be used only in display_tasks_table(), using it elsewhere might causes unwanted results.

    Args:
        attribute (str): The attribute you want to change.
        task (tasks.Task): The task in which the attribute will be changed
        config (config.Config): The configs to comply with the user's behaviour settings.

    Raises:
        ValueError: If it is not a valid task attribute, raise this error.

    Returns:
        str: The rich stylized and colored string associated with that attribute.
    """
    attribute = attribute.lower().strip()  # for more leniency

    match attribute:
        case "id":
            return str(task.id)
        case "name":
            return task.name
        case "status":
            styled_status = f"[white]{task.status}[/]"
            if config.behaviour_settings.show_status_colors:
                status_colors: dict[str, str] = {
                    "on-hold": "dim",
                    "todo": "white",
                    "doing": "bold blue",
                    "done": "green4",
                }
                styled_status = f"[{status_colors[task.status]}]{task.status}[/]"
            return styled_status
        case "priority":
            styled_priority = f"[white]{task.priority}[/]"
            if config.behaviour_settings.show_priority_colors:
                priority_colors: dict[str, str] = {
                    "low": "green",
                    "medium": "yellow",
                    "high": "red",
                    "urgent": "bold red3",
                }
                styled_priority = (
                    f"[{priority_colors[task.priority]}]{task.priority}[/]"
                )
            return styled_priority
        case "duedate":
            formatted_duedate, task_duedate_color = task.get_formatted_duedate()
            return f"[{task_duedate_color if config.behaviour_settings.show_duedate_colors else 'white'}]{formatted_duedate}[/]"
        case "tags":
            if not task.tags:
                return "No Tags"
            return " ".join(f"#{tag.lstrip('#').strip()}" for tag in task.tags)
        case _:
            raise ValueError(f"Not a valid attribute: '{attribute}'")


def _validate_filters(filters: dict[str, str | None]) -> dict[str, str]:
    """NOTE: This function should only be used in display_tasks_table()

    Args:
        filters (dict[str, Any]): The filters passed in by the user in the app.command() options

    Raises:
        ValueError: If the status provided by the user is invalid, raise this error.
        ValueError: If the priority provided by the user is invalid, raise this error.

    Returns:
        dict[str, str]: The validated filter, removing none or empty values, and only returning valid ones.
    """
    validated_filters: dict[str, str] = {}
    for filter, value in filters.items():
        formatted_value = value.lower().strip().replace(" ", "") if value else None
        if not formatted_value:  # basically if its none or smth like that
            continue
        if filter == "status" and formatted_value not in const.VALID_STATUSES:
            raise ValueError(
                f"'{formatted_value}' is not a valid priority. Must be one of {const.VALID_STATUSES}"
            )
        if filter == "priority" and formatted_value not in const.VALID_PRIORITIES:
            raise ValueError(
                f"'{formatted_value}' is not a valid priority. Must be one of {const.VALID_PRIORITIES}"
            )
        # if it passes all these checks, then add it
        validated_filters[filter] = formatted_value

    return validated_filters


def display_tasks_table(
    context: typer.Context, filters: dict[str, str | None] | None = None
) -> None:
    """This is an internal CLI Command to display the rich table based off the tasklist."""
    # literally just for the autocomplete really
    state: ContextObject = context.obj

    # doing all filtering and removal of tasks before the len check

    # this auto clears all done tasks if the user enabled the auto_clear_done_tasks config
    if state.config.behaviour_settings.auto_clear_done_tasks:
        state.tasklist = tasks.clear_done_tasks(state.tasklist)

    # this filters the tasks if the user added options to the list command
    filtered_tasklist: list[tasks.Task] = [
        task for task in state.tasklist
    ]  # doing = state.tasklist will also modify the original tasklist

    # the filters thing
    if filters and (validated_filters := _validate_filters(filters)):
        filtered_tasklist = [
            task
            for task in state.tasklist
            if all(
                getattr(task, filter) == val
                for filter, val in validated_filters.items()
            )
        ]

    if len(filtered_tasklist) <= 0:
        print("There is nothing in the tasklist...", style="info")
        return

    # making the tables with the correct columns
    tasks_table = Table(
        title="The Tasklist",
        show_lines=state.config.behaviour_settings.show_table_lines,
    )
    for column_name in state.config.visible_columns:
        tasks_table.add_column(column_name)

    for task in filtered_tasklist:
        task_contents = [
            _get_styled_attribute(column_name, task, state.config)
            for column_name in state.config.visible_columns
        ]
        tasks_table.add_row(*task_contents)

    print("\n", tasks_table, "\n")
    # newlines to make it look better


@app.command("list")
@app.command("view", hidden=True)
@app.command("ls", hidden=True)
def list_tasks(
    context: typer.Context,
    status_filter: Annotated[
        str | None,
        typer.Option(
            "--status",
            "-s",
            help="This will only allow the listing of the task with this status.",
        ),
    ] = None,
    priority_filter: Annotated[
        str | None,
        typer.Option(
            "--priority",
            "-p",
            help="This will only allow the listing of the task with that priority.",
        ),
    ] = None,
) -> None:
    """To list the tasks from the tasklist. Additionally allows filtering for status and priority. Aliases: view | ls"""
    # The actual CLI Command to list the rich table tasklist
    filters = {"status": status_filter, "priority": priority_filter}
    logger.info("User invoked 'list' command")
    display_tasks_table(context, filters)


@app.command("clear")
def clear_tasks(
    context: typer.Context,
    confirm: Annotated[
        bool,
        typer.Option("--confirm", "-c", help="Skips the confirmation prompt"),
    ] = False,
) -> None:
    """Asks a confirmation prompt first, then if they confirm, clear the tasklist.

    Args:
        context (typer.Context): The context required to read and write to the needed global variables
        confirm (bool): Defaults to False, if value is false, then confirmation is still required, otherwise, skip the prompt
    """
    # literally just for the autocomplete really
    logger.info("User invoked 'clear' command")
    logger.debug("clear command params", command_params={"clear_confirm": confirm})
    state: ContextObject = context.obj

    confirm_clear: bool = (
        questionary.confirm("Are you sure you want to clear the entire tasklist?")
        .skip_if(
            not state.config.behaviour_settings.require_clear_confirmation or confirm,
            True,
        )
        .ask()
    )
    if not confirm_clear:
        print("Tasklist clear cancelled", style="info")
        logger.info("Cancelled clearing of tasklist")
        return
    tasks.save_tasks(state.tasklist_filepath, state.tasklist, state.tasklist_next_id)
    logger.success("Successfully cleared all tasks in tasklist!")


@app.command("config")
def config_cli(context: typer.Context) -> None:
    """To configure the TaskCLI settings.

    Args:
        context (typer.Context): The needed context to access and change the global variables.
    """
    logger.info("User invoked 'config' command")

    state: ContextObject = context.obj
    state.config.main_configuration_ui()


def get_tasklist_filepath(config: config.Config) -> Path:
    return (config.tasklists_dir_filepath / config.current_tasklist).with_suffix(
        ".json"
    )


@app.callback(invoke_without_command=True)
def initialize(
    context: typer.Context,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="This flag enables verbose mode"),
    ] = False,
    version: Annotated[
        bool, typer.Option("--version", "-V", help="Shows the version of the TaskCLI")
    ] = False,
) -> None:
    """TaskCLI: A tool to help organize and list your tasks"""
    # basically this is the first thing that runs when app() is called
    # we first check storage to generate the files and stuff if they dont exist, then
    # we create a context.obj to store the variables in
    # we also create a logger object thingy to actually log things

    # Args:
    #     context (typer.Context): Context object used by typer. You must use context.obj to store persistent values.
    #

    if version:
        print(f"v{taskcli_version}")
        raise typer.Exit()

    # for the app.log, always runs
    logger.remove()
    logger.add(
        const.MAIN_FILEPATH / "app.log",
        rotation="00:00",
        retention=0,
        level="DEBUG",
        format="{time:DD-MM-YYYY_HH:mm:ss} > {name}:{line} > {level}: {message}",
    )

    storage.check_config_file(
        const._dirs.user_config_path,
        const.CONFIG_FILEPATH,
        config.Config.DEFAULT_CONFIG,
    )

    loaded_config: config.Config = config.Config()
    final_verbose_mode: bool = loaded_config.behaviour_settings.verbose_mode or verbose

    logger.debug(f"Verbose mode is {final_verbose_mode}")

    # this makes the user be able to see things in the terminal
    if final_verbose_mode:
        logger.debug(
            f"Verbose mode enabled via {'config' if loaded_config.behaviour_settings.verbose_mode else 'CLI flag'}"
        )
        logger.add(
            sys.stderr,
            format="{time:DD-MM-YYYY_HH:mm:ss} > {name}:{line} > {level}: {message}",
            level="DEBUG",
        )

    tasklist_filepath = get_tasklist_filepath(loaded_config)

    storage.check_tasklists(
        loaded_config.tasklists_dir_filepath, const.PLACEHOLDER_TASKS
    )

    tasklist, next_id = tasks.initialize_tasks(tasklist_filepath)

    context.obj = ContextObject(loaded_config, tasklist, next_id, tasklist_filepath)
    logger.debug(
        "App initialization done. Put all the variables needed in context.obj",
    )


@tasklist_command.command("add")
def add_tasklist(
    context: typer.Context,
    name: Annotated[list[str], typer.Argument(help="The new tasklist name.")],
):
    """Adds a new tasklist which you can switch to using the switch command.

    Args:
        name (str): The new tasklist's name.
    """
    state: ContextObject = context.obj  # just for the autocomplete really
    logger.info("User invoked 'tasklist add' command.")

    joined_name: str = (" ".join(name)).strip()
    tasks.add_tasklist(joined_name, state.config.tasklists_dir_filepath)
    print(f"\nSuccessfully made a new tasklist: {joined_name}\n")
    logger.success(f"Successfully made a new tasklist: {joined_name}")


@tasklist_command.command("delete")
@tasklist_command.command("remove", hidden=True)
@tasklist_command.command("del", hidden=True)
@tasklist_command.command("rm", hidden=True)
def delete_tasklist(
    context: typer.Context,
    name: Annotated[
        list[str], typer.Argument(help="The name of the tasklist that will be deleted.")
    ],
):
    """Deletes a tasklist. Aliases: remove | del | rm"""
    state: ContextObject = context.obj  # just for the autocomplete really
    logger.info("User invoked 'tasklist delete' command.")

    joined_name: str = (" ".join(name)).strip()
    tasks.delete_tasklist(joined_name, state.config.tasklists_dir_filepath)
    print(f"\nSuccessfully deleted a tasklist: {joined_name}\n")
    logger.success(f"Successfully deleted a tasklist: {joined_name}")


@tasklist_command.command("rename")
def rename_tasklist(
    context: typer.Context,
    old_name: Annotated[
        str, typer.Argument(help="The name of the tasklist that you want to rename")
    ],
    new_name: Annotated[
        str, typer.Argument(help="The new renamed name of the tasklist")
    ],
):
    logger.info("User invoked 'tasklist rename' command.")

    state: ContextObject = context.obj  # just for the autocomplete really
    tasks.rename_tasklist(old_name, new_name, state.config.tasklists_dir_filepath)
    print(f"\nSuccessfully renamed tasklist into '{new_name}'\n")
    logger.success(f"Successfully renamed tasklist into '{new_name}'")


@tasklist_command.command("switch")
def switch_tasklists(
    context: typer.Context,
    name: Annotated[
        list[str],
        typer.Argument(help="The name of the tasklist you want to switch to."),
    ],
):
    state: ContextObject = context.obj  # just for the autocomplete really

    joined_name: str = (" ".join(name)).strip()
    if joined_name not in tasks.get_tasklists(state.config.tasklists_dir_filepath):
        raise ValueError(f"Invalid tasklist name, as it doesn't exist: {joined_name}")

    state.config.current_tasklist = joined_name
    state.config.save_config()

    print(f"\nSwitched to tasklist: {joined_name}.\n", style="info")
    logger.info(f"User switch to tasklist '{joined_name}'")


@tasklist_command.command("list")
@tasklist_command.command("view", hidden=True)
@tasklist_command.command("ls", hidden=True)
def list_tasklists(context: typer.Context):
    state: ContextObject = context.obj  # just for the autocomplete really

    for tasklist in tasks.get_tasklists(state.config.tasklists_dir_filepath):
        print(
            f"- {tasklist} {'(CURRENT)' if tasklist == state.config.current_tasklist else ''}"
        )


def main():
    try:
        app()
    except ValueError as error:
        # These are usually errors raised by Task class setters (invalid priority, etc.)
        print(f"[bold red]Input Error:[/] {error}")
        logger.error(error)
        sys.exit(0)
    except KeyboardInterrupt:
        # Handles Ctrl+C
        logger.debug("User did keyboard interrupt, operation cancelled")
        print("\n[yellow]Operation cancelled by user.[/]")
        sys.exit(0)
    except Exception as error:
        logger.opt(exception=True).critical("The app crashed unexpectedly.")
        print(f"[bold red]CRITICAL ERROR:[/] {error}")
        print("[dim]Please check the app.log for a full traceback.[/]")
        sys.exit(0)


if __name__ == "__main__":
    main()
