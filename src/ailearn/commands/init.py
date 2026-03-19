from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path
from typing import Optional

import questionary
import typer
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.panel import Panel

console = Console()

# Where the bundled templates live inside the installed package
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

_BANNER = """\
[#aa2233] █████╗ ██╗██╗     ███████╗ █████╗ ██████╗ ███╗   ██╗[/#aa2233]
[#aa2233]██╔══██╗██║██║     ██╔════╝██╔══██╗██╔══██╗████╗  ██║[/#aa2233]
[#aa2233]███████║██║██║     █████╗  ███████║██████╔╝██╔██╗ ██║[/#aa2233]
[#aa2233]██╔══██║██║██║     ██╔══╝  ██╔══██║██╔══██╗██║╚██╗██║[/#aa2233]
[#aa2233]██║  ██║██║███████╗███████╗██║  ██║██║  ██║██║ ╚████║[/#aa2233]
[#aa2233]╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝[/#aa2233]
[dim]          Building and Learning with AI[/dim]
"""


def init(
    project_name: Optional[str] = typer.Argument(
        None,
        help="Name of the project directory to create. Use '.' or --here to scaffold into the current directory.",
    ),
    agent: Optional[str] = typer.Option(
        None,
        "--agent",
        help="AI agent to configure: claude, cursor, or both.",
    ),
    here: bool = typer.Option(
        False,
        "--here",
        help="Scaffold into the current directory instead of creating a new one.",
    ),
    update: bool = typer.Option(
        False,
        "--update",
        help="Re-run prompts to update settings on an already-initialized project. Preserves sessions and profile.",
    ),
    sync: bool = typer.Option(
        False,
        "--sync",
        help="Redeploy agent command files from the installed tool. No prompts — constitution and profile are untouched.",
    ),
) -> None:
    """Scaffold a new AILearn project."""

    console.print(_BANNER)

    # --- Sync mode: just redeploy agent files, nothing else ---
    if sync:
        target_dir = Path.cwd()
        ailearn_dir = target_dir / ".ailearn"
        if not ailearn_dir.exists():
            console.print("[red]No AILearn installation found in this directory. Run `ailearn init` first.[/red]")
            raise typer.Abort()
        agent_to_sync = agent or questionary.select(
            "Which agent files would you like to sync?",
            choices=[
                questionary.Choice("Claude Code", value="claude"),
                questionary.Choice("Cursor", value="cursor"),
                questionary.Choice("Both", value="both"),
            ],
        ).ask()
        _install_agent_files(agent_to_sync, target_dir, ailearn_dir)
        console.print()
        console.print(Panel.fit(
            "[bold green]✓ Agent files synced![/bold green]\n\n"
            "[dim]constitution.md and profile.md were not modified.[/dim]",
            border_style="green",
        ))
        return

    # --- Resolve target directory ---
    if here or project_name in (".", None):
        target_dir = Path.cwd()
    else:
        target_dir = Path.cwd() / project_name
        if target_dir.exists() and any(target_dir.iterdir()):
            overwrite = questionary.confirm(
                f"Directory '{project_name}' already exists and is not empty. Continue anyway?",
                default=False,
            ).ask()
            if not overwrite:
                raise typer.Abort()
        target_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"\n[dim]Scaffolding into:[/dim] [bold]{target_dir}[/bold]\n")

    # --- Check for existing AILearn installation ---
    ailearn_dir = target_dir / ".ailearn"
    already_initialized = ailearn_dir.exists() and (ailearn_dir / "constitution.md").exists()

    if already_initialized and not update:
        action = questionary.select(
            "AILearn is already initialized in this project. What would you like to do?",
            choices=[
                questionary.Choice(
                    "Update settings (re-run prompts, preserve sessions and profile)",
                    value="update",
                ),
                questionary.Choice(
                    "Override everything (start completely fresh)",
                    value="override",
                ),
                questionary.Choice("Cancel", value="cancel"),
            ],
        ).ask()
        if action == "cancel":
            raise typer.Abort()
        update = action == "update"

    # --- Interactive prompts ---
    project_type: str = questionary.select(
        "Is this a new or existing project?",
        choices=[
            questionary.Choice("New project", value="new"),
            questionary.Choice("Existing project", value="existing"),
        ],
    ).ask()

    if project_type == "new":
        project_description: str = questionary.text(
            "Describe the project in 1–2 sentences.",
        ).ask()
    else:
        project_description = (
            questionary.text(
                "Any additional context for the agent?",
                instruction="(optional — press Enter to skip)",
            ).ask()
            or ""
        )

    preferred_language: str = (
        questionary.text(
            "When explaining language-agnostic concepts, which language should examples use?",
            instruction="(e.g. Python, TypeScript — or press Enter to let the agent decide)",
        ).ask()
        or "No preference"
    )

    _LEARNING_STYLE_DEFAULT = "Explain the concept and why before showing code"
    _CUSTOM_STYLE_SENTINEL = "__custom__"

    learning_style_choice: str = questionary.select(
        "How do you prefer the agent to explain things?",
        choices=[
            questionary.Choice("Explain the concept and why before showing code", value="Explain the concept and why before showing code"),
            questionary.Choice("Show working code examples first, then explain", value="Show working code examples first, then explain"),
            questionary.Choice("Use real-world analogies to explain technical ideas", value="Use real-world analogies to explain technical ideas"),
            questionary.Choice("Keep explanations brief — show the pattern, I'll figure it out", value="Keep explanations brief — show the pattern, I'll figure it out"),
            questionary.Choice("Describe my learning style…", value=_CUSTOM_STYLE_SENTINEL),
        ],
    ).ask()

    if learning_style_choice == _CUSTOM_STYLE_SENTINEL:
        custom = (
            questionary.text(
                "Describe how you'd like the agent to explain things.",
                instruction="(press Enter to use the default)",
            ).ask()
            or ""
        ).strip()
        learning_style = custom if custom else _LEARNING_STYLE_DEFAULT
    else:
        learning_style = learning_style_choice

    learning_goals_input: str = (
        questionary.text(
            "What do you want to get better at during this project?",
            instruction="Comma-separated (e.g. API design, testing, state management) — or press Enter to skip",
        ).ask()
        or ""
    )
    learning_goals = [g.strip() for g in learning_goals_input.split(",") if g.strip()]

    if agent is None:
        agent = questionary.select(
            "Which AI agent are you using?",
            choices=[
                questionary.Choice("Claude Code (primary)", value="claude"),
                questionary.Choice("Cursor", value="cursor"),
                questionary.Choice("Both", value="both"),
            ],
        ).ask()

    # --- Scaffold .ailearn/ folder tree ---
    dirs_to_create = [
        ailearn_dir / "sessions",
        ailearn_dir / "recaps",
        ailearn_dir / "agents" / "claude",
    ]
    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)

    # Keep sessions/ and recaps/ discoverable even when empty
    (ailearn_dir / "sessions" / ".gitkeep").touch()
    (ailearn_dir / "recaps" / ".gitkeep").touch()

    # --- Write .ailearn/.gitignore ---
    # Sessions and recaps are personal learning artifacts — gitignored by default.
    # Developers can delete this file if they want to track them in git.
    (ailearn_dir / ".gitignore").write_text(
        "# Sessions and recaps are personal learning artifacts.\n"
        "# Remove this file if you want to track them in git.\n"
        "sessions/\n"
        "recaps/\n"
    )

    # --- Render constitution.md from Jinja2 template ---
    jinja_env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )
    constitution_tmpl = jinja_env.get_template("constitution.md")
    constitution_content = constitution_tmpl.render(
        project_type="New" if project_type == "new" else "Existing",
        project_description=project_description,
        preferred_language=preferred_language,
        learning_style=learning_style,
        learning_goals=learning_goals,
        date=date.today().isoformat(),
    )
    (ailearn_dir / "constitution.md").write_text(constitution_content)

    # --- Copy profile.md scaffold (only on fresh init — preserve existing profile on update) ---
    if not update:
        shutil.copy(TEMPLATES_DIR / "profile.md", ailearn_dir / "profile.md")

    # --- Offer starter session (only on fresh init when a project description was given) ---
    if not update and project_description:
        want_starter = questionary.confirm(
            "Would you like a suggested first task to help you get started?",
            default=True,
        ).ask()
        if want_starter:
            _generate_starter_session(ailearn_dir, project_description, date.today())

    # --- Install agent files ---
    _install_agent_files(agent, target_dir, ailearn_dir)

    # --- Done ---
    if update:
        console.print()
        console.print(
            Panel.fit(
                f"[bold green]✓ AILearn updated![/bold green]\n\n"
                f"[dim]constitution.md:[/dim] re-rendered with your new answers\n"
                f"[dim]Agent files:[/dim] synced from installed tool\n"
                f"[dim]profile.md + sessions:[/dim] untouched",
                border_style="green",
            )
        )
    else:
        console.print()
        console.print(
            Panel.fit(
                f"[bold green]✓ AILearn initialized![/bold green]\n\n"
                f"[dim]Folder:[/dim] [cyan].ailearn/[/cyan]\n"
                f"[dim]Agent:[/dim] [cyan]{agent}[/cyan]\n\n"
                f"[bold]Next steps:[/bold]\n"
                f"  1. Review [cyan].ailearn/constitution.md[/cyan] — fill in what you know and what you're shaky on\n"
                f"  2. Open your project in your AI agent\n"
                f"  3. Type [bold cyan]/ailearn.plan[/bold cyan] to start your first learning-enhanced session",
                border_style="green",
            )
        )


def _generate_starter_session(ailearn_dir: Path, project_description: str, today: date) -> None:
    """Create a context file guiding the developer's first session."""
    session_dir = ailearn_dir / "sessions" / f"{today.isoformat()}-getting-started"
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "context.md").write_text(
        f"# Getting Started\n\n"
        f"**Created:** {today.isoformat()}\n\n"
        f"---\n\n"
        f"## Your Project\n\n"
        f"{project_description}\n\n"
        f"---\n\n"
        f"## Suggested First Task\n\n"
        f"A natural starting point is to set up your core project structure and implement your first feature.\n\n"
        f"**To begin your first AILearn session:**\n\n"
        f"1. Open this project in your AI agent\n"
        f"2. Run `/ailearn.plan` followed by a specific task description\n\n"
        f"**Example prompt:**\n"
        f"```\n"
        f"/ailearn.plan Set up the project structure and implement [your first core feature]\n"
        f"```\n\n"
        f"**Tip:** Be as specific as possible. Instead of \"build the app\", try "
        f"\"implement the user login endpoint with JWT tokens\". "
        f"The more focused the task, the better calibrated the learning notes will be.\n\n"
        f"---\n\n"
        f"*Generated by `ailearn init`. Delete this file once you've run your first plan.*\n"
    )


def _install_agent_files(agent: str, target_dir: Path, ailearn_dir: Path) -> None:
    """Copy agent-specific files to the correct locations."""

    claude_src = TEMPLATES_DIR / "agents" / "claude"
    cursor_src = TEMPLATES_DIR / "agents" / "cursor"

    if agent in ("claude", "both"):
        # Copy CLAUDE.md into .ailearn/agents/claude/ (source of truth)
        dest_claude_dir = ailearn_dir / "agents" / "claude"
        shutil.copy(claude_src / "CLAUDE.md", dest_claude_dir / "CLAUDE.md")

        # Also copy CLAUDE.md to .claude/ at project root so Claude Code picks it up
        dot_claude_dir = target_dir / ".claude"
        dot_claude_dir.mkdir(exist_ok=True)
        shutil.copy(claude_src / "CLAUDE.md", dot_claude_dir / "CLAUDE.md")

        # Copy slash commands to .claude/commands/ so /ailearn.plan etc. work
        commands_dest = target_dir / ".claude" / "commands"
        commands_dest.mkdir(exist_ok=True)
        commands_src = claude_src / "commands"
        for cmd_file in commands_src.iterdir():
            shutil.copy(cmd_file, commands_dest / cmd_file.name)

        console.print("[dim]  ✓ Claude Code: .claude/CLAUDE.md + .claude/commands/[/dim]")

    if agent in ("cursor", "both"):
        # Copy project rules to .cursor/rules/ (Cursor's modern rules system)
        cursor_rules_dest = target_dir / ".cursor" / "rules"
        cursor_rules_dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(cursor_src / "rules" / "ailearn.mdc", cursor_rules_dest / "ailearn.mdc")

        # Copy slash commands to .cursor/commands/
        cursor_commands_dest = target_dir / ".cursor" / "commands"
        cursor_commands_dest.mkdir(parents=True, exist_ok=True)
        for cmd_file in (cursor_src / "commands").iterdir():
            shutil.copy(cmd_file, cursor_commands_dest / cmd_file.name)

        console.print("[dim]  ✓ Cursor: .cursor/rules/ailearn.mdc + .cursor/commands/[/dim]")
