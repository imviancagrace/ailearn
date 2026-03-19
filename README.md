# AILearn

> Ship code and build real understanding — session by session.

## The Problem

You've probably felt it: you ship code that works, but you're not sure you could explain it to anyone. The AI generated it, you accepted it, and now it's in production. You're moving fast, but the understanding isn't keeping up.

This is the gap that shows up in interviews, in code reviews, and in the moments when something breaks and you don't know where to start.

AILearn is built for developers navigating that gap. It wraps your AI agent — Claude Code or Cursor — with a structured learning layer that makes sure every session builds real understanding, not just output. You ship code *and* you grow. Both, every time.

---

## How It Works

```
Developer types /ailearn.plan
        ↓
Agent reads .ailearn/constitution.md  →  knows your skill level, stack, and learning goals
Agent reads .ailearn/profile.md       →  knows what you've learned and what's ready for review
        ↓
Identifies ambiguities a senior dev would resolve first (up to 5)
  → Notifies you: "I have N questions. Run /ailearn.clarify to go through them."
  → /ailearn.clarify asks one question at a time — each with the engineering principle behind it
  → Saves Q&A to .ailearn/sessions/YYYY-MM-DD-{task}/clarifications.md
        ↓
Generates plan with:
  · 🧠 AI Reasoning — alternatives considered, decision rationale
  · 📚 Prior Knowledge — what the plan assumes you already know
  · 📝 The Plan — step-by-step implementation
  · 🎓 Learning Notes — concepts, pitfalls, best practices, calibrated to your level
  · 📊 Success Criteria — how to know it worked
        ↓
Saves to .ailearn/sessions/YYYY-MM-DD-{task}/plan.md
Updates .ailearn/profile.md with new concepts + application tracking
        ↓
After 2+ applications of the same concept:
  → "Run /ailearn.reflect to test your understanding and earn the Solidified badge"
  → /ailearn.reflect asks you to explain it, probes deeper, promotes if solid
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

**From a local copy of this repo:**
```bash
uv tool install --editable /path/to/ailearn
ailearn init my-project
```

**Reinstall to pick up changes (local development):**
```bash
uv tool install --reinstall --editable /path/to/ailearn
```

---

## Quickstart

```bash
# 1. Scaffold AILearn into a new project
ailearn init my-project

# 2. Navigate into the project and open it in your AI agent
cd my-project

# 3. Start a plan — the agent will flag ambiguities and tell you if clarify is needed
/ailearn.plan Set up the project structure and implement the user auth endpoint

# 4. If the agent identified questions, run clarify to go through them
/ailearn.clarify

# 5. When a concept gets flagged after enough sessions, run reflect
/ailearn.reflect JWT authentication

# 6. At the end of the week
/ailearn.weekrecap
```

During `ailearn init`, you'll be asked:
- Your skill level
- Your project description
- What you want to get better at (your learning goals)
- Your preferred explanation style
- Which agent you're using (Claude Code, Cursor, or both)

---

## Folder Structure

After `ailearn init`, your project gets a `.ailearn/` folder:

```
.ailearn/
├── .gitignore               # Sessions and recaps are gitignored by default
├── constitution.md          # Your profile: skill level, learning goals, what you know
├── profile.md               # Auto-updated: concepts encountered, ready for reflection, mastered
├── sessions/
│   └── YYYY-MM-DD-{task}/
│       ├── clarifications.md  # Q&A from /ailearn.clarify (when run)
│       └── plan.md            # The implementation plan
├── recaps/
│   └── YYYY-MM-DD-recap.md  # Weekly learning recaps
└── agents/
    ├── claude/
    │   ├── CLAUDE.md         # System instructions for Claude Code
    │   └── commands/         # Source of truth for slash commands
    └── cursor/
        ├── rules/            # Source of truth for Cursor rules
        └── commands/         # Source of truth for Cursor slash commands
```

> **Note:** `sessions/` and `recaps/` are gitignored by default — they're personal learning artifacts. Delete `.ailearn/.gitignore` if you want to track them.

For **Claude Code**, the following are also installed at the project root:
- `.claude/CLAUDE.md` — picked up automatically by Claude Code
- `.claude/commands/ailearn.plan.md` — enables `/ailearn.plan`
- `.claude/commands/ailearn.clarify.md` — enables `/ailearn.clarify`
- `.claude/commands/ailearn.reflect.md` — enables `/ailearn.reflect`
- `.claude/commands/ailearn.weekrecap.md` — enables `/ailearn.weekrecap`

For **Cursor**, the following are installed at the project root:
- `.cursor/rules/ailearn.mdc` — project rules picked up automatically by Cursor
- `.cursor/commands/ailearn.plan.md` — enables `/ailearn.plan`
- `.cursor/commands/ailearn.clarify.md` — enables `/ailearn.clarify`
- `.cursor/commands/ailearn.reflect.md` — enables `/ailearn.reflect`
- `.cursor/commands/ailearn.weekrecap.md` — enables `/ailearn.weekrecap`

---

## Commands

### `ailearn init [PROJECT_NAME]`

Scaffolds a new AILearn project. On first run, creates `.ailearn/`, installs agent files, and generates your `constitution.md` from your answers.

```
Options:
  PROJECT_NAME        Directory to create. Omit to scaffold into the current directory.
  --here              Scaffold into the current directory.
  --agent TEXT        claude | cursor | both  (skips the interactive prompt)
  --update            Re-run prompts to update settings. Preserves your sessions and profile.
  --sync              Redeploy agent command files from the installed tool. No prompts, constitution and profile untouched.
```

Examples:
```bash
ailearn init my-app              # creates my-app/ and scaffolds inside
ailearn init --here              # scaffolds into current directory
ailearn init . --agent claude    # current directory, Claude Code only
ailearn init --update            # update settings without losing your history
ailearn init --sync              # redeploy command files after updating the tool
```

If AILearn is already initialized and you run `ailearn init` without `--update`, it will ask whether you want to update settings, override everything, or cancel.

---

### `/ailearn.clarify` (slash command in your AI agent)

You won't run this command on your own initiative — you run it when `/ailearn.plan` tells you to. If the agent detects ambiguities in your task that would meaningfully change the plan, it will say so before generating anything and ask you to run `/ailearn.clarify` first.

When you do, the agent walks you through the questions **one at a time**. Each question includes:
- The question itself
- **Why a senior engineer asks this** — the engineering principle or trade-off behind it

This is where a lot of the learning happens. You're not just answering questions to fill in gaps — you're being shown how experienced engineers think before they write a single line of code.

After the Q&A, the answers are saved to `.ailearn/sessions/YYYY-MM-DD-{task}/clarifications.md`. When you then run `/ailearn.plan`, it picks them up automatically.

---

### `/ailearn.plan` (slash command in your AI agent)

Generates a learning-enhanced plan for your current task.

**The plan includes:**
- **AI Reasoning** — alternatives considered, decision rationale
- **Prior Knowledge** — what concepts from your profile this plan assumes
- **The Plan** — step-by-step implementation
- **Learning Notes** — concepts, pitfalls, best practices, calibrated to your level
- **Success Criteria** — how to know it worked

> **Cursor users:** When the plan is presented and Cursor asks you to accept or reject, use **"Auto-accept edits"** — do NOT use "Clear context and auto-accept". The clear context option resets the conversation, which breaks the rest of the workflow (the plan won't be saved to `.ailearn/sessions/` and the profile won't be updated).

---

### `/ailearn.reflect [concept]` (slash command in your AI agent)

Run this when a concept has been flagged as "Ready for Reflection" — typically after it's appeared across multiple sessions.

The agent asks you to explain the concept in your own words, then probes deeper to test whether you understand the *why* behind it, not just the *what*. If you've got it, the concept is promoted to Solidified and the AI stops over-explaining it in future sessions. If there are gaps, you get targeted feedback and try again next session.

You can also run it proactively: `/ailearn.reflect dependency injection` will test any concept by name.

---

### `/ailearn.weekrecap` (slash command in your AI agent)

Reads all session plans from the past week and generates a personalized recap:

- What you built
- The most important concepts from the week (skipping what you've mastered)
- Patterns emerging across sessions
- What you're ready to explore next
- A note from your AI mentor

Saved to `.ailearn/recaps/`.

---

## Concept Progression

AILearn tracks concepts through four stages:

```
Encountered → Ready for Reflection → Solidified → Ready to Go Deeper
```

- **Encountered:** Introduced in a plan. Tracked with `applied in: [session-slug, ...]` — a record of every session where you actively used it, not just learned it.
- **Ready for Reflection:** Applied across 3+ sessions. Run `/ailearn.reflect` to validate your understanding.
- **Solidified:** Validated through reflection. The AI references it without re-explaining.
- **Ready to Go Deeper:** Solidified concepts the recap will push further on.

You can also edit `profile.md` manually to promote or adjust concepts — the AI respects whatever's there.

---

## Customising Your Experience

**`constitution.md`** is the most important file to fill in after init. The more honest you are about what you know and don't know, the better the AI calibrates to you. Update it with `ailearn init --update` whenever your skill level or goals change.

**`profile.md`** is updated automatically but you can edit it manually — promote a concept to Solidified if you feel confident, or move one to "Ready to Go Deeper" to get more advanced coverage in your next plan.

---

## Agent Support

| Agent | Plan | Clarify | Reflect | Recap |
|---|---|---|---|---|
| Claude Code | `/ailearn.plan` | `/ailearn.clarify` | `/ailearn.reflect` | `/ailearn.weekrecap` |
| Cursor | `/ailearn.plan` | `/ailearn.clarify` | `/ailearn.reflect` | `/ailearn.weekrecap` |

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

```bash
git clone https://github.com/imviancagrace/ailearn.git
cd ailearn

# Install dependencies into a local .venv
uv sync

# Install ailearn as a global CLI tool pointing to your local code.
# Any changes you make are reflected immediately — no reinstall needed.
uv tool install --editable .

# Verify it works
ailearn --help
```

To test changes end-to-end, run `ailearn init` inside any project directory. To pick up changes after a reinstall is needed (e.g. changes to `pyproject.toml`):

```bash
uv tool install --reinstall --editable .
```

---

## License

MIT — see [LICENSE](./LICENSE).
