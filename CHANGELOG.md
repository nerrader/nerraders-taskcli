# v2.1.0 - 5/5/2026
- Added compatibility for other OSes such as Linux and macOS.
- Added platformdirs module to help with developing the multi OS compatibility feature.
- Added a `--version` `-V` flag that shows the version of TaskCLI you're using.
- Added an icon to the main .exe in the .zip file, which you can see in `assets/`
- Added the vermin package to check the minimum python version, and changed `pyproject.toml` to match that.
- Added an `__init__.py` to make it a regular package.
- Deleted TaskCLI.spec from the repository.

# v2.0.0 - 28/4/2026
This version marks the release of the new feature: tasklists!
- Added the tasklists feature, which allows you to add, delete, rename, and switch between tasklists, with the use of one subcommand: `tasklist`.
- Added a real README.md to my project.
- Removed the visibility of aliases of commands in help menu. It's now in the individual commands help menu context.
- Modified the pyproject.toml to move types-dateparser to dev-dependencies, and to remove rich from the main dependency section.

# v1.0.0 - 24/4/2026
This version marks the initial release of the TaskCLI.
- Added core features like adding, removing, updating, marking, listing tasks.
- Added other task attributes such as priority and duedate.
- Added customizable settings you can configure yourself using the `config` command.
- Added logging using loguru, saved in `AppData\Roaming\taskcli` in `app.log`.
- Added more destructive commands, like `clear` to clear your entire tasklist, or `reset` for a full factory reset of your taskcli and configs.
