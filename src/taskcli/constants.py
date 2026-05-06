from pathlib import Path
from typing import Any

from platformdirs import PlatformDirs
from rich.theme import Theme
from rich.console import Console


_dirs = PlatformDirs("TaskCLI", appauthor="nerrader", roaming=True)
MAIN_FILEPATH: Path = _dirs.user_data_path
CONFIG_FILEPATH: Path = _dirs.user_config_path / "config.json"

PLACEHOLDER_TASKS: dict[str, Any] = {"next_id": 1, "tasklist": []}

VALID_PRIORITIES: tuple[str, str, str, str] = ("low", "medium", "high", "urgent")
VALID_STATUSES: tuple[str, str, str, str] = ("on-hold", "todo", "doing", "done")

CUSTOM_THEME = Theme(
    {"error": "red", "success": "green", "info": "blue", "warning": "yellow"}
)
CONSOLE = Console(theme=CUSTOM_THEME)
