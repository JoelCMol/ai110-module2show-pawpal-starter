from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum


# ---------------------------------------------------------------------------
# Priority
# ---------------------------------------------------------------------------

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

@dataclass
class Task:
    id: str
    title: str
    description: str
    pet_id: str
    duration_minutes: int
    priority: Priority
    due_date: datetime
    is_completed: bool = False
    recurrence: str | None = None  # e.g. "daily", "weekly", or None

    def complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def reschedule(self, new_date: datetime) -> None:
        """Move the task's due date to new_date."""
        self.due_date = new_date

    def is_overdue(self) -> bool:
        """Return True if the task is past due and not yet completed."""
        return not self.is_completed and self.due_date < datetime.now()

    def spawn_next(self) -> Task | None:
        """Return a new Task for the next recurrence, or None if not recurring."""
        delta = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}.get(self.recurrence or "")
        if delta is None:
            return None
        return Task(
            id=str(uuid.uuid4()),
            title=self.title,
            description=self.description,
            pet_id=self.pet_id,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            due_date=self.due_date + delta,
            recurrence=self.recurrence,
        )


# ---------------------------------------------------------------------------
# Pet
# ---------------------------------------------------------------------------

@dataclass
class Pet:
    id: str
    name: str
    species: str   # "dog", "cat", "other"
    breed: str
    birth_date: date
    owner: Owner   # direct reference instead of owner_id string

    def get_age(self) -> int:
        """Return the pet's age in whole years."""
        today = date.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def get_tasks(self, scheduler: Scheduler) -> list[Task]:
        """Return all tasks associated with this pet from the scheduler."""
        return [t for t in scheduler.tasks.values() if t.pet_id == self.id]


# ---------------------------------------------------------------------------
# Owner
# ---------------------------------------------------------------------------

class Owner:
    def __init__(
        self,
        id: str,
        name: str,
        email: str,
        phone: str,
    ) -> None:
        """Initialize an Owner with contact details and an empty pet roster."""
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's roster."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove the pet with the given id from this owner's roster."""
        self.pets = [p for p in self.pets if p.id != pet_id]

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self) -> None:
        """Initialize a Scheduler with empty registries for tasks, owners, and pets."""
        self.tasks: dict[str, Task] = {}
        self.owners: dict[str, Owner] = {}
        self.pets: dict[str, Pet] = {}

    def register_owner(self, owner: Owner) -> None:
        """Add an owner to the registry."""
        self.owners[owner.id] = owner

    def register_pet(self, pet: Pet) -> None:
        """Add a pet to the registry."""
        self.pets[pet.id] = pet

    def schedule_task(self, task: Task) -> None:
        """Add a task to the queue."""
        self.tasks[task.id] = task

    def cancel_task(self, task_id: str) -> None:
        """Remove the task with the given id from the queue."""
        self.tasks.pop(task_id, None)

    def complete_task(self, task_id: str) -> Task | None:
        """Mark a task complete and auto-schedule its next occurrence if recurring.

        Returns the newly created Task if one was spawned, otherwise None.
        """
        task = self.tasks.get(task_id)
        if task is None:
            return None
        task.complete()
        next_task = task.spawn_next()
        if next_task:
            self.schedule_task(next_task)
        return next_task

    def get_conflicts(self, *, same_pet_only: bool = False) -> list[str]:
        """Return warning messages for any pending tasks whose time windows overlap.

        By default checks across all pets. Pass same_pet_only=True to restrict
        to conflicts between tasks belonging to the same pet.
        """
        pending = sorted(
            [t for t in self.tasks.values() if not t.is_completed],
            key=lambda t: t.due_date,
        )
        warnings = []
        for i, a in enumerate(pending):
            a_end = a.due_date + timedelta(minutes=a.duration_minutes)
            for b in pending[i + 1:]:
                if b.due_date >= a_end:
                    break  # sorted by start time — no further overlaps possible
                if same_pet_only and a.pet_id != b.pet_id:
                    continue
                pet_a = self.pets.get(a.pet_id)
                pet_b = self.pets.get(b.pet_id)
                name_a = pet_a.name if pet_a else a.pet_id
                name_b = pet_b.name if pet_b else b.pet_id
                scope = "same pet" if a.pet_id == b.pet_id else "different pets"
                warnings.append(
                    f"⚠ CONFLICT ({scope}): '{a.title}' ({name_a}, "
                    f"{a.due_date.strftime('%I:%M %p')}–{a_end.strftime('%I:%M %p')}) "
                    f"overlaps '{b.title}' ({name_b}, starts {b.due_date.strftime('%I:%M %p')})"
                )
        return warnings

    def get_upcoming_tasks(self, pet_id: str) -> list[Task]:
        """Return incomplete tasks for a pet, ordered by due date."""
        return sorted(
            [t for t in self.tasks.values() if t.pet_id == pet_id and not t.is_completed],
            key=lambda t: t.due_date,
        )

    def get_overdue_tasks(self) -> list[Task]:
        """Return all incomplete tasks whose due date has passed."""
        return [t for t in self.tasks.values() if t.is_overdue()]

def filter_tasks(
    self,
    *,
    pet_name: str | None = None,
    status: str = "all",
) -> list[Task]:
    """Return tasks optionally filtered by pet name and/or completion status."""

    target_ids = None
    if pet_name:
        name = pet_name.lower()
        target_ids = {
            p.id for p in self.pets.values()
            if p.name.lower() == name
        }

    def matches(task: Task) -> bool:
        if target_ids is not None and task.pet_id not in target_ids:
            return False
        if status == "pending":
            return not task.is_completed
        if status == "completed":
            return task.is_completed
        return True

    return [task for task in self.tasks.values() if matches(task)]

    def send_reminder(self, task: Task) -> None:
        """Send a reminder notification for the given task."""
        print(f"REMINDER: '{task.title}' is due {task.due_date.strftime('%Y-%m-%d %H:%M')}")

    def sort_by_time(self, tasks: list[Task], *, reverse: bool = False) -> list[Task]:
        """Return a new list of tasks sorted by due_date ascending (or descending if reverse=True)."""
        return sorted(tasks, key=lambda t: t.due_date, reverse=reverse)

    def generate_daily_plan(self, pet_id: str) -> list[Task]:
        """Return today's incomplete tasks for a pet, sorted by priority then due time."""
        today = date.today()
        tasks = [
            t for t in self.tasks.values()
            if t.pet_id == pet_id
            and not t.is_completed
            and (t.due_date.date() == today or t.is_overdue())
        ]
        return sorted(tasks, key=lambda t: (-t.priority.value, t.due_date))
