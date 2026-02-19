# AILearn

> AI-assisted development with built-in learning for junior and early-career developers.

AILearn wraps your AI agent (Claude Code or Cursor) and augments its planning output with structured learning content — concept explanations, pitfalls, best practices, and personalized weekly recaps. You ship code *and* build real understanding, session by session.

Inspired by [GitHub's Spec Kit](https://github.com/github/spec-kit).

---

## Why AILearn?

Most AI coding tools optimise for output speed. AILearn optimises for output speed *and* developer growth.

When you run `/ailearn.plan`, your agent generates a plan that includes:
- The reasoning behind architectural decisions
- Concepts you need to understand to implement it well
- Pitfalls specific to this approach
- Resources calibrated to your current skill level

Your `profile.md` tracks every concept you've encountered. Each session builds on the last — the AI stops re-explaining things you know and starts pushing you toward deeper understanding.

---

## How It Works

```
Developer types /ailearn.plan
        ↓
Agent reads .ailearn/constitution.md  →  knows your skill level + stack
Agent reads .ailearn/profile.md       →  knows what you've already learned
        ↓
Generates plan with 🎓 Learning Notes tailored to you
        ↓
Saves to .ailearn/sessions/YYYY-MM-DD-{task}/plan.md
Updates .ailearn/profile.md with new concepts introduced
```

At the end of the week, `/ailearn.weekrecap` reads all your sessions and generates a personalized recap — surfacing what mattered, skipping what you've mastered, and pointing toward what you're ready for next.

---

## Installation

Requires [uv](https://docs.astral.sh/uv/).

**Run once in any project (no install required):**
```bash
uvx --from git+https://github.com/imviancagrace/ailearn.git ailearn init my-project
```

**Or install globally:**
```bash
uv tool install git+https://github.com/imviancagrace/ailearn.git
ailearn init my-project
```

---

## Quickstart

```bash
# 1. Scaffold AILearn into a new project
ailearn init my-project

# 2. Navigate into the project and open it in your AI agent
cd my-project

# 3. In Claude Code or Cursor, start planning
/ailearn.plan

# 4. At the end of the week
/ailearn.weekrecap
```

During `ailearn init`, you'll be asked:
- Your name and skill level
- Your primary tech stack
- A short project description
- Which agent you're using (Claude Code, Cursor, or both)

---

## Folder Structure

After `ailearn init`, your project gets a `.ailearn/` folder:

```
.ailearn/
├── constitution.md          # Your profile: skill level, stack, learning goals
├── profile.md               # Auto-updated: concepts encountered and mastered
├── sessions/
│   └── YYYY-MM-DD-{task}/
│       └── plan.md          # Every plan, saved automatically
├── recaps/
│   └── YYYY-MM-DD-recap.md  # Weekly learning recaps
└── agents/
    ├── claude/
    │   ├── CLAUDE.md         # System instructions for Claude Code
    │   └── commands/         # Source of truth for slash commands
    └── cursor/
        └── .cursorrules      # System instructions for Cursor
```

For **Claude Code**, the following are also installed at the project root:
- `.claude/CLAUDE.md` — picked up automatically by Claude Code
- `.claude/commands/ailearn.plan.md` — enables `/ailearn.plan`
- `.claude/commands/ailearn.weekrecap.md` — enables `/ailearn.weekrecap`

For **Cursor**, `.cursorrules` is installed at the project root. Use `@ailearn plan` and `@ailearn weekrecap` as trigger phrases.

---

## Commands

### `ailearn init [PROJECT_NAME]`

Scaffolds a new AILearn project.

```
Options:
  PROJECT_NAME        Directory to create. Omit to scaffold into the current directory.
  --here              Scaffold into the current directory.
  --agent TEXT        claude | cursor | both  (skips the interactive prompt)
```

Examples:
```bash
ailearn init my-app              # creates my-app/ and scaffolds inside
ailearn init --here              # scaffolds into current directory
ailearn init . --agent claude    # current directory, Claude Code only
```

### `/ailearn.plan` (slash command in your AI agent)

Generates a learning-enhanced plan for your current task. The plan includes:

- **AI Reasoning** — context, alternatives considered, decision rationale
- **The Plan** — step-by-step implementation
- **Learning Notes** — concepts, pitfalls, best practices, calibrated to your skill level
- **Success Criteria** — how to know it worked

The plan is saved to `.ailearn/sessions/` and your `profile.md` is updated with any new concepts introduced.

### `/ailearn.weekrecap` (slash command in your AI agent)

Reads all session plans from the past week and generates a personalized recap:

- What you built
- The most important concepts from the week (skipping what you've mastered)
- Patterns emerging across sessions
- What you're ready to explore next
- A note from your AI mentor

Saved to `.ailearn/recaps/`.

---

## Customising Your Experience

**`constitution.md`** is the most important file to fill in after init. The more honest you are about what you know and don't know, the better the AI calibrates to you.

**`profile.md`** is updated automatically but you can also edit it manually — promote a concept to "Mastered" if you feel confident in it, or move one to "Ready to Go Deeper" to get more advanced coverage in your next plan.

---

## Agent Support

| Agent | Plan command | Recap command | Notes |
|---|---|---|---|
| Claude Code | `/ailearn.plan` | `/ailearn.weekrecap` | Full native slash command support |
| Cursor | `@ailearn plan` | `@ailearn weekrecap` | Via `.cursorrules` trigger phrases |

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

```bash
git clone https://github.com/imviancagrace/ailearn.git
cd ailearn
uv sync
uv run ailearn --help
```

---

## License

MIT — see [LICENSE](./LICENSE).
