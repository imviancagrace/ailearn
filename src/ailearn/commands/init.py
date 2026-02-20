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
) -> None:
    """Scaffold a new AILearn project."""

    console.print(
        Panel.fit(
            "[bold cyan]AILearn[/bold cyan] — AI-assisted learning toolkit\n"
            "[dim]Wrapping your AI agent with structured learning[/dim]",
            border_style="cyan",
        )
    )

    # --- Resolve target directory ---
    if here or project_name in (".", None):
        target_dir = Path.cwd()
        if project_name is None:
            # No arg given — default to cwd, same as --here
            pass
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

    # --- Interactive prompts ---
    skill_level: str = questionary.select(
        "What's your current skill level?",
        choices=[
            questionary.Choice("Junior (0–2 years, learning fundamentals)", value="Junior"),
            questionary.Choice("Early-Mid (2–4 years, building confidence)", value="Early-Mid"),
        ],
    ).ask()

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
        project_description: str = (
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

    learning_style: str = questionary.select(
        "How do you prefer the agent to explain things?",
        choices=[
            "Explain the concept and why before showing code",
            "Show working code examples first, then explain",
            "Use real-world analogies to explain technical ideas",
            "Keep explanations brief — show the pattern, I'll figure it out",
        ],
    ).ask()

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
    ailearn_dir = target_dir / ".ailearn"
    dirs_to_create = [
        ailearn_dir / "sessions",
        ailearn_dir / "recaps",
        ailearn_dir / "agents" / "claude",
    ]
    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)

    # Keep sessions/ and recaps/ tracked by git even when empty
    (ailearn_dir / "sessions" / ".gitkeep").touch()
    (ailearn_dir / "recaps" / ".gitkeep").touch()

    # --- Render constitution.md from Jinja2 template ---
    jinja_env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
    )
    constitution_tmpl = jinja_env.get_template("constitution.md")
    constitution_content = constitution_tmpl.render(
        skill_level=skill_level,
        project_type="New" if project_type == "new" else "Existing",
        project_description=project_description,
        preferred_language=preferred_language,
        learning_style=learning_style,
        date=date.today().isoformat(),
    )
    (ailearn_dir / "constitution.md").write_text(constitution_content)

    # --- Copy profile.md scaffold ---
    shutil.copy(TEMPLATES_DIR / "profile.md", ailearn_dir / "profile.md")

    # --- Install agent files ---
    _install_agent_files(agent, target_dir, ailearn_dir)

    # --- Done ---
    console.print()
    console.print(
        Panel.fit(
            f"[bold green]✓ AILearn initialized![/bold green]\n\n"
            f"[dim]Folder:[/dim] [cyan].ailearn/[/cyan]\n"
            f"[dim]Agent:[/dim] [cyan]{agent}[/cyan]\n\n"
            f"[bold]Next steps:[/bold]\n"
            f"  1. Edit [cyan].ailearn/constitution.md[/cyan] to refine your learning goals\n"
            f"  2. Open your project in your AI agent\n"
            f"  3. Type [bold cyan]/ailearn.plan[/bold cyan] to start your first learning-enhanced plan",
            border_style="green",
        )
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

        # Copy slash commands to .cursor/commands/ so /ailearn.plan etc. work natively
        cursor_commands_dest = target_dir / ".cursor" / "commands"
        cursor_commands_dest.mkdir(parents=True, exist_ok=True)
        for cmd_file in (cursor_src / "commands").iterdir():
            shutil.copy(cmd_file, cursor_commands_dest / cmd_file.name)

        console.print("[dim]  ✓ Cursor: .cursor/rules/ailearn.mdc + .cursor/commands/[/dim]")
