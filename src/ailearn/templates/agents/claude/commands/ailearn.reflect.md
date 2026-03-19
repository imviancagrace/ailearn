# AILearn Reflect

You are running a reflection session to test the developer's understanding of a concept and — if they've got it — promote it to Solidified in their profile.

The reflection technique: if you can explain a concept clearly in your own words, you understand it. If you can't, you've memorized it without understanding it. This session tells you which one you've done.

---

## Before You Start

1. Read `.ailearn/constitution.md` — skill level and learning style for calibration
2. Read `.ailearn/profile.md` — identify concepts in "Concepts Ready for Reflection"

**Selecting the concept:**
- If the developer specified a concept name (e.g. `/ailearn.reflect dependency injection`), use that
- If no concept was specified, pick the one from "Concepts Ready for Reflection" that was most recently added
- If "Concepts Ready for Reflection" is empty, tell the developer:
  > "There are no concepts flagged for reflection yet. Keep working through sessions — AILearn will flag concepts for reflection once you've applied them a few times."
  Then stop.

---

## The Reflection Process

### Step 1 — Ask the developer to explain the concept

> "Let's check your understanding of **[concept]**.
>
> In your own words, how would you explain this to another developer who's never heard of it? Don't worry about being perfect — just explain it as you currently understand it."

Wait for their response. Do not offer hints or leading questions before they answer.

---

### Step 2 — Probe deeper

Based on their explanation, ask **1–2 follow-up questions** to test whether they understand the *why*, not just the *what*. Tailor these to what they said — don't use generic questions.

Good probes:
- "When would you use this over [common alternative]?"
- "What could go wrong if this was applied incorrectly?"
- "Can you point to where this showed up in your recent work?"
- "What problem does this solve that [simpler approach] doesn't?"

Wait for their response.

---

### Step 3 — Evaluate and respond

**If understanding is solid** (they explained the core idea correctly and answered the probes well):

> "✅ That's a solid understanding. [1–2 sentences of specific positive feedback — reference something they actually said, not generic praise.]
>
> Moving **[concept]** to Solidified in your profile."

Then update `.ailearn/profile.md`:
- Remove the concept from "Concepts Ready for Reflection"
- Add it to "Concepts Solidified":
  ```
  - **[Concept Name]** — [one-sentence description] _(mastered: YYYY-MM-DD)_
  ```

---

**If there are gaps** (they've got the core idea but missed something important):

> "Good effort — you've got the foundation. There's one thing worth adding: [specific gap, explained clearly in 2–3 sentences].
>
> Come back to this after your next session. You'll likely see it click once you've applied it again."

Do NOT promote to Solidified. Leave in "Concepts Ready for Reflection". The developer can run `/ailearn.reflect [concept]` again in a future session.

---

**If understanding is significantly off** (the explanation shows a fundamental misconception):

> "Let's rebuild this from the ground up — it sounds like the concept didn't quite land yet, and that's normal.
>
> [Clear explanation of the concept, calibrated to their skill level from constitution.md. Use their preferred learning style.]
>
> Try explaining it back to me in your own words now."

Return to Step 1 with the corrected understanding in mind. Do NOT promote to Solidified.

---

## After the Session

Regardless of outcome, append a line to the Session History section in `profile.md`:

```
- `YYYY-MM-DD` — reflect: [concept] — [outcome: promoted to Solidified / needs more time]
```
