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

### Testing PawPal+

## Test Coverage Overview

### Existing Tests
- **`test_complete_changes_status`** — completing a task flips `is_completed` to `True`
- **`test_schedule_task_increases_pet_task_count`** — adding a task to the scheduler is reflected in `pet.get_tasks()`

### Sorting Correctness
- **`test_sort_by_time_ascending`** — three out-of-order tasks come back earliest-first
- **`test_sort_by_time_descending`** — `reverse=True` returns latest-first
- **`test_sort_by_time_empty_list`** — empty input returns `[]` without error
- **`test_get_upcoming_tasks_no_tasks`** — a pet with no tasks returns an empty list
- **`test_get_upcoming_tasks_excludes_completed`** — completed tasks don't appear in upcoming

### Recurrence Logic
- **`test_spawn_next_daily`** — daily task spawns a copy exactly 24 hours later with a new ID
- **`test_spawn_next_weekly`** — weekly task spawns a copy exactly 7 days later
- **`test_spawn_next_non_recurring_returns_none`** — `recurrence=None` returns `None`
- **`test_spawn_next_unknown_recurrence_returns_none`** — unrecognised strings like `"monthly"` return `None`
- **`test_complete_task_spawns_next_in_scheduler`** — completing a recurring task auto-adds the next occurrence to the scheduler
- **`test_complete_task_nonexistent_id`** — completing a fake ID returns `None` without raising

### Conflict Detection
- **`test_no_conflicts_back_to_back`** — tasks that share an exact boundary (end = next start) are not flagged
- **`test_conflict_partial_overlap`** — overlapping windows produce exactly one warning
- **`test_conflict_same_pet_only_ignores_different_pets`** — `same_pet_only=True` skips cross-pet overlaps; the default catches them
- **`test_conflict_completed_tasks_excluded`** — completed tasks are invisible to conflict checks
- **`test_no_conflicts_single_task`** — a single task can never conflict with itself

### Confidence Level
- 5
