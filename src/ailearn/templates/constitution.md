# AILearn Constitution

**Project Type:** {{ project_type }}
**Example Language:** {{ preferred_language }}
**Created:** {{ date }}

---

## Project Context

{% if project_description %}
{{ project_description }}
{% else %}
*(No additional context provided — the agent will read the project to determine context.)*
{% endif %}

---

## Learning Style

{{ learning_style }}

---

## Learning Goals

> What you want to get better at during this project. The AI will actively steer toward these — not just explain what comes up, but look for opportunities to teach toward them.

{% if learning_goals %}
{% for goal in learning_goals %}
- [ ] {{ goal }}
{% endfor %}
{% else %}
- [ ] *(Add your learning goals here — the more specific, the better)*
{% endif %}

---

## What I Already Know

> Be honest — this helps the AI skip re-explaining things you've got and focus on what actually moves the needle.

-
-
-

---

## What I'm Shaky On

> These are the areas where you want the AI to slow down and explain more carefully.

-
-
-
