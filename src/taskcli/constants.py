from pathlib import Path
from typing import Any

from platformdirs import PlatformDirs
from rich.theme import Theme
from rich.console import Console

# some path variables
_dirs = PlatformDirs("TaskCLI", appauthor="nerrader")
MAIN_FILEPATH: Path = _dirs.user_data_path
APPLOG_FILEPATH: Path = _dirs.user_data_path / "app.log"
HISTORY_DIR_FILEPATH: Path = _dirs.user_data_path / "histories"
CONFIG_FILEPATH: Path = _dirs.user_config_path / "config.json"

# usually only for if a task file is empty
PLACEHOLDER_TASKS: dict[str, Any] = {"next_id": 1, "tasklist": []}

PLACEHOLDER_HISTORY: dict[str, list] = {"undo_stack": [], "redo_stack": []}

DEFAULT_CONFIG: dict[str, Any] = {
    "visible_columns": ["ID", "Name", "Status", "Priority", "Duedate"],
    "default_priority": "medium",
    "current_tasklist": "main",
    "tasklists_dir_filepath": str(MAIN_FILEPATH / "tasklists"),
    "behaviour_settings": {
        "auto_clear_done_tasks": False,
        "require_clear_confirmation": True,
        "require_delete_confirmation": False,
        "show_table_lines": True,
        "show_status_colors": True,
        "show_priority_colors": True,
        "show_duedate_colors": True,
        "verbose_mode": False,
    },
}


# tasks things
VALID_PRIORITIES: tuple[str, str, str, str] = ("low", "medium", "high", "urgent")
VALID_STATUSES: tuple[str, str, str, str] = ("on-hold", "todo", "doing", "done")

# rich styling things
CUSTOM_THEME = Theme(
    {"error": "red", "success": "green", "info": "blue", "warning": "yellow"}
)
CONSOLE = Console(theme=CUSTOM_THEME)
