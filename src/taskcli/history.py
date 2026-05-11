from typing import Any, TYPE_CHECKING

from taskcli import constants as const
from taskcli import storage
from taskcli import tasks

if TYPE_CHECKING:
    from pathlib import Path


def add_undo_stack(
    history: dict[str, list], original_tasklist: dict[str, Any]
) -> dict[str, list]:
    history["undo_stack"].append(original_tasklist)
    history["redo_stack"] = []

    return history


def add_redo_stack(
    history: dict[str, list], tasklist: dict[str, Any]
) -> dict[str, list]:
    history["redo_stack"].append(tasklist)

    return history


def load_history(tasklist_name: str) -> dict[str, list]:
    raw_loaded_history = storage.load_json(resolve_history_filepath(tasklist_name))

    return {
        "undo_stack": [
            {
                "next_id": state["next_id"],
                "tasklist": tasks.rehydrate_loaded_tasks(state["tasklist"]),
            }
            for state in raw_loaded_history["undo_stack"]
        ],
        "redo_stack": [
            {
                "next_id": state["next_id"],
                "tasklist": tasks.rehydrate_loaded_tasks(state["tasklist"]),
            }
            for state in raw_loaded_history["redo_stack"]
        ],
    }


def save_history(tasklist_name: str, history: dict[str, list]) -> None:
    serialized_history = {
        "undo_stack": [
            {
                "next_id": tasklist["next_id"],
                "tasklist": [task.to_dict() for task in tasklist["tasklist"]],
            }
            for tasklist in history["undo_stack"]
        ],
        "redo_stack": [
            {
                "next_id": tasklist["next_id"],
                "tasklist": [task.to_dict() for task in tasklist["tasklist"]],
            }
            for tasklist in history["redo_stack"]
        ],
    }

    storage.write_json(resolve_history_filepath(tasklist_name), serialized_history)


def resolve_history_filepath(tasklist_name: str) -> Path:
    return const.HISTORY_DIR_FILEPATH / f"{tasklist_name}-history.json"
