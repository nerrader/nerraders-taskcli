# Nerrader's TaskCLI

Nerrader's TaskCLI was a tool that was born out of necessity. I always had my own problems organizing and trying to remember my tasks and responsibilities, which has led to me frequently forgetting deadlines and oftentimes doing things at the last minute. And over time, those problems have caused me significant mental stress amd fatigue over the years.

So, I built this tool to get rid of my mental clutter by providing a way to better organize and track my responsibilities, so I can focus my time and energy on actually doing the work, rather than spending time worrying about what I might have forgotten.

# Features

- ### Core Features of a TaskCLI

    Adding, deleting, updating, marking, listing tasks are all here.

- ### Customizable Settings

    This tool uses the `questionary` module to open up an **interactive menu to customize the settings** by typing out a command.

- ### Local Storage
    This tool does not require an internet connection to run. You can still manage and use all the features while being **offline** without drawbacks.
- ### Logging
    This tool uses the `loguru` module for **logging and troubleshooting** the app.
- ### Additional Commands

    This tool has some additional commands like `clear` to clear your entire tasklist, and `reset` to factory reset both your tasklist and configs.

- ### Additional Task Attributes

    This tool has additional task attributes like priority, and duedates.

- ### Tasklists
    This tool allows for the adding, removing, renaming and switching of different tasklists, so you can group your tasks more easily.

# How to Download & Use

With these instructions, I am assuming you are using the **latest version of the tool**.

1. **Download the .zip folder**, from the latest [release.](https://github.com/nerrader/nerrader-taskcli-python/releases)
2. **Extract** the .zip folder.
3. **Open your terminal**, and navigate to the **folder containing the .exe.**
4. Start running commands!

Here are some **quick commands** to get you to know how it works better:

- `taskcli add get groceries`: Adds a task called 'get groceries' with ID 1
- `taskcli list`: Lists the tasks table
- `taskcli delete 1`: Removes a task with the ID 1, in this case its task "get groceries"

Use `--help` after any command to find more about its arguments, options and aliases.

> [!tip]
> You can also change the .exe file name to make it shorter.
> So for example, you can change the file from `TaskCLI.exe` to `task.exe` which makes it so that you only have to type in `task list` instead.
>
> Also, make sure to check and configure your settings by using the `config` command, as defaults might be undesirable.

#### Main TaskCLI Commands:

| Command  | Required Arguments          | Description                                                                              |
| :------: | :-------------------------- | :--------------------------------------------------------------------------------------- |
|   add    | task_name                   | Adds a new task with that task name                                                      |
|  delete  | task_id                     | Removes a specific task from your list based on the task ID.                             |
|  update  | task_id, `updated-contents` | Updates with the updated_contents (e.g. name, priority) based on task ID                 |
|   mark   | task_id, updated_status     | Marks task with the new updated status based on task ID                                  |
|   list   | NONE                        | Lists all tasks in a table                                                               |
|  config  | NONE                        | Opens up the main configuration menu                                                     |
|  clear   | NONE                        | Asks the user for confirmation, then clears the tasklist                                 |
|  reset   | NONE                        | Asks the user for confirmation, then resets the tasklist and configs to factory defaults |
| tasklist | `sub-command`               | Manage multiple lists (add, remove, rename, switch)                                      |

> [!NOTE]
> All data and logs are stored locally in `AppData/Roaming/taskcli`.

# Upcoming/Planned Features

Here are some features that will be planned for future major/minor releases.

- Undo/Redo commands
- Adding task tags or groups.

# Contributing

This project welcomes all contributors, and whether you are fixing a bug, adding a new feature, or just improving the documentation of this project, you can get started by just following these steps:

1. Fork this repository
2. Clone this repository on your computer `https://github.com/[YOUR-USERNAME]/nerrader-taskcli-python.git`
3. It is recommended that you make a seperate branch than the main branch `git switch -c [NEW-BRANCH-NAME]`, using `feature/` for new features, and `fix/` to fix a known issue/bug, just to name a few.
4. Use `uv sync` to automatically set up the virtual environment and grab all the dependencies for you.
5. Commit your changes. Make sure your commit messages are clear and concise.
6. Push changes to your fork of the repository
7. Open a pull request. If you go back to the original repository, there should be a button called Compare & Pull Request. Click it, and one should be automaticallly made for you. Describe your changes and why they should be implemented in the main repository, then submit.

> [!IMPORTANT]
> Please make sure your code works properly before submitting. Follow PEP 8 guidelines, maintain consistent styling, and include type annotations and documentation for any new functions.

By contributing this project, you agree that your contribution will be licensed under the MIT License.

# Project Module Technical Stack

This project does use some python modules and packages to help with the development process. So I thought it would be helpful If I documented them here:

### Main Project Dependencies

- Typer: To handle the main CLI arguments and the --help menu.
- Rich: To handle the color styling, and listing tables, just to make it more aesthetically pleasing to look at.
- Questionary: For the confirmation prompts and the main settings configuration UI.
- Dateparser: To help with parsing and validating the duedates that the user passes in.
- Loguru: To enable logging in the app.log and verbose mode.

### Developer Dependencies

- Mypy: For type checking and error catching.
- Pip-audit: For checking security vulnerabilities in packages.
- Pyinstaller: To make the distributable .exe file you are seeing in the releases.
- Radon: To help with measuring CC and MI in my code.
- Ruff: For code linting and formatting.
- Types-dateparser: To enable mypy to scan dateparser types.
- Vulture: For catching dead code
