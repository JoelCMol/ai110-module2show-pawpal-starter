from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
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

    def get_upcoming_tasks(self, pet_id: str) -> list[Task]:
        """Return incomplete tasks for a pet, ordered by due date."""
        return sorted(
            [t for t in self.tasks.values() if t.pet_id == pet_id and not t.is_completed],
            key=lambda t: t.due_date,
        )

    def get_overdue_tasks(self) -> list[Task]:
        """Return all incomplete tasks whose due date has passed."""
        return [t for t in self.tasks.values() if t.is_overdue()]

    def send_reminder(self, task: Task) -> None:
        """Send a reminder notification for the given task."""
        print(f"REMINDER: '{task.title}' is due {task.due_date.strftime('%Y-%m-%d %H:%M')}")

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
