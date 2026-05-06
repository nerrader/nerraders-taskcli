import json
from pathlib import Path
from typing import Any

from loguru import logger

# This file is for anything related to reading and writing to files in the main filepath


def load_json(filepath: Path) -> Any:
    try:
        logger.debug(f"Attemping to read JSON from {filepath}")
        with open(filepath, "r", encoding="utf-8") as file:
            file_contents = json.load(file)
    except FileNotFoundError:
        file_contents = None
        logger.error("File was not found in the designated filepath, returning None")
    return file_contents


def write_json(filepath: Path, data: Any) -> None:
    logger.debug(f"Writing data to {filepath}", write_data=data)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def check_storage(
    tasks_dir_filepath: Path,
    config_filepath: Path,
    placeholder_tasks: dict,
    default_config: dict,
) -> None:
    """checks if the files exist, if not it creates them and fills them with default data

    i think args are pretty self explanatory"""
    logger.debug("Checking storage")
    # make both the main directory and tasks directory in the appdata if it doesn't exist
    tasks_dir_filepath.mkdir(parents=True, exist_ok=True)

    # check if the files exist, if not create them and fill them with default data
    if not config_filepath.exists():
        logger.debug("Config file wasn't found, set configs to default")
        write_json(config_filepath, default_config)

    tasklists = list(tasks_dir_filepath.glob("*.json"))
    if not tasklists:  # if empty
        # then create a main default tasklists with the placeholder tasks
        write_json(tasks_dir_filepath / "main.json", placeholder_tasks)
        return

    for tasklist in tasklists:
        tasklist_path = Path(tasklist)
        if not tasklist_path.exists():
            logger.debug(
                "Tasklist file wasn't found, set tasks to the starting tasklist."
            )
            write_json(tasklist_path, placeholder_tasks)


def reset_files(tasks_dir_filepath: Path, config_filepath: Path) -> None:
    """Removes all files according to the filepaths list. This list should only contain the tasklists

    Args:
        tasks_dir_filepath (Path): The tasklists directory, where all the tasklist.json(s) are stored
        config_filepath (Path): The config.json filepath
    """
    files_to_remove = list(tasks_dir_filepath.glob("*.json")) + [config_filepath]
    for file in files_to_remove:
        file.unlink(missing_ok=True)
        logger.debug(f"Deleted {file}")
    logger.success(
        "Successfully resetted tasklist and settings. Files will be initialized on next launch."
    )
