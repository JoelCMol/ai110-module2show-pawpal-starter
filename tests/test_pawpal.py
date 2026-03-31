from datetime import date, datetime, timedelta
import uuid
from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def make_task(
    pet_id="p1",
    task_id=None,
    title="Walk",
    due_date=None,
    duration_minutes=30,
    priority=Priority.MEDIUM,
    recurrence=None,
) -> Task:
    return Task(
        id=task_id or str(uuid.uuid4()),
        title=title,
        description="Daily walk",
        pet_id=pet_id,
        duration_minutes=duration_minutes,
        priority=priority,
        due_date=due_date or datetime(2026, 4, 1, 9, 0),
        recurrence=recurrence,
    )


def make_pet(owner: Owner) -> Pet:
    return Pet(
        id="p1",
        name="Luna",
        species="dog",
        breed="Labrador",
        birth_date=date(2020, 6, 15),
        owner=owner,
    )


def make_owner() -> Owner:
    return Owner(id="o1", name="Alex", email="alex@example.com", phone="555-0000")


# --- Test 1: Task Completion ---

def test_complete_changes_status():
    task = make_task()
    assert task.is_completed is False
    task.complete()
    assert task.is_completed is True


# --- Test 2: Task Addition Increases Pet's Task Count ---

def test_schedule_task_increases_pet_task_count():
    owner = make_owner()
    pet = make_pet(owner)
    scheduler = Scheduler()
    scheduler.register_pet(pet)

    assert len(pet.get_tasks(scheduler)) == 0

    scheduler.schedule_task(make_task(pet_id=pet.id))
    assert len(pet.get_tasks(scheduler)) == 1


# ---------------------------------------------------------------------------
# Sorting correctness
# ---------------------------------------------------------------------------

def test_sort_by_time_ascending():
    """Tasks are returned in earliest-first order."""
    scheduler = Scheduler()
    base = datetime(2026, 4, 1, 9, 0)
    t1 = make_task(due_date=base + timedelta(hours=2))
    t2 = make_task(due_date=base)
    t3 = make_task(due_date=base + timedelta(hours=1))

    result = scheduler.sort_by_time([t1, t2, t3])
    assert [t.due_date for t in result] == [
        base,
        base + timedelta(hours=1),
        base + timedelta(hours=2),
    ]


def test_sort_by_time_descending():
    """reverse=True returns latest-first order."""
    scheduler = Scheduler()
    base = datetime(2026, 4, 1, 9, 0)
    t1 = make_task(due_date=base)
    t2 = make_task(due_date=base + timedelta(hours=1))

    result = scheduler.sort_by_time([t1, t2], reverse=True)
    assert result[0].due_date > result[1].due_date


def test_sort_by_time_empty_list():
    """sort_by_time on an empty list returns []."""
    scheduler = Scheduler()
    assert scheduler.sort_by_time([]) == []


def test_get_upcoming_tasks_no_tasks():
    """A pet with no tasks returns an empty upcoming list."""
    scheduler = Scheduler()
    assert scheduler.get_upcoming_tasks("p_no_tasks") == []


def test_get_upcoming_tasks_excludes_completed():
    """Completed tasks do not appear in upcoming."""
    scheduler = Scheduler()
    t = make_task(due_date=datetime(2026, 4, 1, 10, 0))
    t.complete()
    scheduler.schedule_task(t)

    assert scheduler.get_upcoming_tasks("p1") == []


# ---------------------------------------------------------------------------
# Recurrence logic
# ---------------------------------------------------------------------------

def test_spawn_next_daily():
    """A daily task spawns a new task exactly one day later."""
    base = datetime(2026, 4, 1, 9, 0)
    t = make_task(due_date=base, recurrence="daily")
    nxt = t.spawn_next()

    assert nxt is not None
    assert nxt.due_date == base + timedelta(days=1)
    assert nxt.recurrence == "daily"
    assert nxt.id != t.id  # must be a fresh task


def test_spawn_next_weekly():
    """A weekly task spawns a new task exactly seven days later."""
    base = datetime(2026, 4, 1, 9, 0)
    t = make_task(due_date=base, recurrence="weekly")
    nxt = t.spawn_next()

    assert nxt is not None
    assert nxt.due_date == base + timedelta(weeks=1)


def test_spawn_next_non_recurring_returns_none():
    """A task with no recurrence returns None from spawn_next."""
    t = make_task(recurrence=None)
    assert t.spawn_next() is None


def test_spawn_next_unknown_recurrence_returns_none():
    """An unrecognised recurrence string (e.g. 'monthly') returns None."""
    t = make_task(recurrence="monthly")
    assert t.spawn_next() is None


def test_complete_task_spawns_next_in_scheduler():
    """Completing a recurring task adds the next occurrence to the scheduler."""
    scheduler = Scheduler()
    t = make_task(due_date=datetime(2026, 4, 1, 9, 0), recurrence="daily")
    scheduler.schedule_task(t)

    next_task = scheduler.complete_task(t.id)

    assert next_task is not None
    assert next_task.id in scheduler.tasks
    assert next_task.due_date == t.due_date + timedelta(days=1)


def test_complete_task_nonexistent_id():
    """Completing a task with an unknown id returns None without raising."""
    scheduler = Scheduler()
    assert scheduler.complete_task("does-not-exist") is None


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_no_conflicts_back_to_back():
    """Tasks that end exactly when the next begins are NOT a conflict."""
    scheduler = Scheduler()
    base = datetime(2026, 4, 1, 9, 0)
    # t1: 9:00–9:30, t2 starts at 9:30 — zero gap, should not conflict
    t1 = make_task(task_id="a", due_date=base, duration_minutes=30)
    t2 = make_task(task_id="b", due_date=base + timedelta(minutes=30), duration_minutes=30)
    scheduler.schedule_task(t1)
    scheduler.schedule_task(t2)

    assert scheduler.get_conflicts() == []


def test_conflict_partial_overlap():
    """Two tasks whose windows overlap produce exactly one conflict warning."""
    scheduler = Scheduler()
    base = datetime(2026, 4, 1, 9, 0)
    # t1: 9:00–10:00, t2: 9:30–10:30 → overlap
    t1 = make_task(task_id="a", due_date=base, duration_minutes=60)
    t2 = make_task(task_id="b", due_date=base + timedelta(minutes=30), duration_minutes=60)
    scheduler.schedule_task(t1)
    scheduler.schedule_task(t2)

    conflicts = scheduler.get_conflicts()
    assert len(conflicts) == 1


def test_conflict_same_pet_only_ignores_different_pets():
    """same_pet_only=True skips overlapping tasks belonging to different pets."""
    scheduler = Scheduler()
    base = datetime(2026, 4, 1, 9, 0)
    t1 = make_task(task_id="a", pet_id="p1", due_date=base, duration_minutes=60)
    t2 = make_task(task_id="b", pet_id="p2", due_date=base + timedelta(minutes=30), duration_minutes=60)
    scheduler.schedule_task(t1)
    scheduler.schedule_task(t2)

    assert scheduler.get_conflicts(same_pet_only=True) == []
    assert len(scheduler.get_conflicts()) == 1  # default catches it


def test_conflict_completed_tasks_excluded():
    """Completed tasks are not included in conflict checks."""
    scheduler = Scheduler()
    base = datetime(2026, 4, 1, 9, 0)
    t1 = make_task(task_id="a", due_date=base, duration_minutes=60)
    t2 = make_task(task_id="b", due_date=base + timedelta(minutes=30), duration_minutes=60)
    t1.complete()
    scheduler.schedule_task(t1)
    scheduler.schedule_task(t2)

    assert scheduler.get_conflicts() == []


def test_no_conflicts_single_task():
    """A scheduler with only one task has nothing to conflict with."""
    scheduler = Scheduler()
    scheduler.schedule_task(make_task())
    assert scheduler.get_conflicts() == []
