# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

A few extra features were added to make the scheduler more useful in practice:

**Sorting by time** — `scheduler.sort_by_time(tasks)` takes any list of tasks and returns them in chronological order. Pass `reverse=True` to flip it. This works on any filtered subset, not just all tasks.

**Filtering** — `scheduler.filter_tasks()` lets you narrow down tasks by pet name, completion status, or both at once. For example, `filter_tasks(pet_name="Luna", status="pending")` returns only Luna's unfinished tasks. Name matching is case-insensitive.

**Recurring tasks** — Tasks can have a `recurrence` of `"daily"` or `"weekly"`. When you complete one using `scheduler.complete_task(id)`, the next occurrence is automatically added to the schedule with the due date shifted forward by one day or one week.

**Conflict detection** — `scheduler.get_conflicts()` checks whether any two pending tasks have overlapping time windows (based on start time + duration). It returns plain warning messages instead of crashing. By default it checks across all pets; pass `same_pet_only=True` to restrict it to one pet at a time.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
