from datetime import date, datetime
from pawpal_system import Owner, Pet, Priority, Scheduler, Task

# --- Setup ---
scheduler = Scheduler()

owner = Owner(id="o1", name="Alex Rivera", email="alex@example.com", phone="555-1234")
scheduler.register_owner(owner)

luna = Pet(id="p1", name="Luna", species="dog", breed="Labrador",
           birth_date=date(2020, 6, 15), owner=owner)
mochi = Pet(id="p2", name="Mochi", species="cat", breed="Siamese",
            birth_date=date(2018, 3, 22), owner=owner)

owner.add_pet(luna)
owner.add_pet(mochi)
scheduler.register_pet(luna)
scheduler.register_pet(mochi)

today = datetime.now().replace(second=0, microsecond=0)

tasks = [
    Task(id="t1", title="Morning walk",        description="30-min walk around the park",
         pet_id="p1", duration_minutes=30, priority=Priority.HIGH,
         due_date=today.replace(hour=7, minute=0)),
    Task(id="t2", title="Flea medication",     description="Monthly flea & tick treatment",
         pet_id="p1", duration_minutes=5,  priority=Priority.HIGH,
         due_date=today.replace(hour=9, minute=0)),
    Task(id="t3", title="Breakfast feeding",   description="Half cup dry food",
         pet_id="p2", duration_minutes=5,  priority=Priority.MEDIUM,
         due_date=today.replace(hour=8, minute=0)),
    Task(id="t4", title="Playtime",            description="Feather wand session",
         pet_id="p2", duration_minutes=15, priority=Priority.LOW,
         due_date=today.replace(hour=11, minute=0)),
    Task(id="t5", title="Evening walk",        description="Evening neighbourhood loop",
         pet_id="p1", duration_minutes=20, priority=Priority.MEDIUM,
         due_date=today.replace(hour=18, minute=0)),
]

for task in tasks:
    scheduler.schedule_task(task)

# --- Print Today's Schedule ---
print("=" * 44)
print("         PawPal+  —  Today's Schedule")
print("=" * 44)

for pet in owner.get_pets():
    plan = scheduler.generate_daily_plan(pet.id)
    print(f"\n{pet.name} ({pet.species}, age {pet.get_age()})")
    print("-" * 44)
    if not plan:
        print("  No tasks scheduled for today.")
    for task in plan:
        status = "✓" if task.is_completed else "•"
        time_str = task.due_date.strftime("%I:%M %p")
        print(f"  {status} [{task.priority.name:<6}] {time_str}  {task.title} ({task.duration_minutes} min)")

overdue = scheduler.get_overdue_tasks()
if overdue:
    print(f"\n⚠  Overdue tasks ({len(overdue)})")
    print("-" * 44)
    for task in overdue:
        print(f"  • {task.title} — was due {task.due_date.strftime('%I:%M %p')}")

print("\n" + "=" * 44)
