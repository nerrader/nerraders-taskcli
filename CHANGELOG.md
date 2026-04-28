# v2.0.0 - 28/4/2026
This version marks the release of the new feature: tasklists!
- Added the tasklists feature, which allows you to add, delete, rename, and switch between tasklists, with the use of one subcommand: `tasklist`.
- Added a real README.md to my project.
- Modified the pyproject.toml to move types-dateparser to dev-dependencies, and to remove rich from the main dependency section.

# v1.0.0 - 24/4/2026
This version marks the initial release of the TaskCLI.
- Added core features like adding, removing, updating, marking, listing tasks.
- Added other task attributes such as priority and duedate.
- Added customizable settings you can configure yourself using the `config` command.
- Added logging using loguru, saved in `AppData\Roaming\taskcli` in `app.log`.
- Added more destructive commands, like `clear` to clear your entire tasklist, or `reset` for a full factory reset of your taskcli and configs.
