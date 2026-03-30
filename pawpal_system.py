from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime


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
    priority: str  # "low", "medium", "high"
    due_date: datetime
    is_completed: bool = False
    recurrence: str | None = None  # e.g. "daily", "weekly", or None

    def complete(self) -> None:
        """Mark this task as completed."""
        pass

    def reschedule(self, new_date: datetime) -> None:
        """Move the task's due date to new_date."""
        pass

    def is_overdue(self) -> bool:
        """Return True if the task is past due and not yet completed."""
        pass


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
    owner_id: str

    def get_age(self) -> int:
        """Return the pet's age in whole years."""
        pass

    def get_tasks(self, scheduler: Scheduler) -> list[Task]:
        """Return all tasks associated with this pet from the scheduler."""
        pass


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
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's roster."""
        pass

    def remove_pet(self, pet_id: str) -> None:
        """Remove the pet with the given id from this owner's roster."""
        pass

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        pass


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    def __init__(self) -> None:
        self.task_queue: list[Task] = []

    def schedule_task(self, task: Task) -> None:
        """Add a task to the queue."""
        pass

    def cancel_task(self, task_id: str) -> None:
        """Remove the task with the given id from the queue."""
        pass

    def get_upcoming_tasks(self, pet_id: str) -> list[Task]:
        """Return incomplete tasks for a pet, ordered by due date."""
        pass

    def get_overdue_tasks(self) -> list[Task]:
        """Return all incomplete tasks whose due date has passed."""
        pass

    def send_reminder(self, task: Task) -> None:
        """Send a reminder notification for the given task."""
        pass

    def generate_daily_plan(self, pet_id: str) -> list[Task]:
        """
        Build and return an ordered list of tasks for today for the given pet.
        Tasks should be selected and sorted by priority and due time.
        """
        pass
