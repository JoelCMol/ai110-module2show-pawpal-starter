from datetime import date, datetime
from pawpal_system import Owner, Pet, Priority, Scheduler, Task


def make_task(pet_id="p1") -> Task:
    return Task(
        id="t1",
        title="Walk",
        description="Daily walk",
        pet_id=pet_id,
        duration_minutes=30,
        priority=Priority.MEDIUM,
        due_date=datetime(2026, 4, 1, 9, 0),
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
