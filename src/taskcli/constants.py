from pathlib import Path
from typing import Any

from platformdirs import PlatformDirs
from rich.theme import Theme
from rich.console import Console
from questionary import Style

_dirs = PlatformDirs("TaskCLI", appauthor="nerrader")
MAIN_FILEPATH: Path = _dirs.user_data_path
APPLOG_FILEPATH: Path = _dirs.user_data_path / "app.log"
HISTORY_DIR_FILEPATH: Path = _dirs.user_data_path / "histories"
CONFIG_FILEPATH: Path = _dirs.user_config_path / "config.json"

# if task file is empty, write it with this
PLACEHOLDER_TASKS: dict[str, Any] = {"next_id": 1, "tasklist": []}

# if history file is empty, write it with this
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

VALID_PRIORITIES: tuple[str, str, str, str] = ("low", "medium", "high", "urgent")
VALID_STATUSES: tuple[str, str, str, str] = ("on-hold", "todo", "doing", "done")

PRIORITY_COLORS: dict[str, str] = {
    "low": "green",
    "medium": "yellow",
    "high": "red",
    "urgent": "bold red3",
}
STATUS_COLORS: dict[str, str] = {
    "on-hold": "dim",
    "todo": "white",
    "doing": "bold blue",
    "done": "green4",
}

CUSTOM_THEME = Theme(
    {"error": "red", "success": "green", "info": "blue", "warning": "yellow"}
)
CONSOLE = Console(theme=CUSTOM_THEME)

QUESTIONARY_STYLE = Style(
    [
        ("disabled", "#858585"),
        ("selected", "fg:#00d7ff"),
        ("highlighted", "fg:yellow"),
        ("pointer", "fg:yellow bold"),
    ]
)
