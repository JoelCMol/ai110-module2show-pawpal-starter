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

# --- Schedule tasks intentionally out of chronological order ---
tasks = [
    Task(id="t5", title="Evening walk",        description="Evening neighbourhood loop",
         pet_id="p1", duration_minutes=20, priority=Priority.MEDIUM,
         due_date=today.replace(hour=18, minute=0)),
    Task(id="t3", title="Breakfast feeding",   description="Half cup dry food",
         pet_id="p2", duration_minutes=5,  priority=Priority.MEDIUM,
         due_date=today.replace(hour=8, minute=0)),
    Task(id="t1", title="Morning walk",        description="30-min walk around the park",
         pet_id="p1", duration_minutes=30, priority=Priority.HIGH,
         due_date=today.replace(hour=7, minute=0)),
    Task(id="t4", title="Playtime",            description="Feather wand session",
         pet_id="p2", duration_minutes=15, priority=Priority.LOW,
         due_date=today.replace(hour=11, minute=0)),
    Task(id="t2", title="Flea medication",     description="Monthly flea & tick treatment",
         pet_id="p1", duration_minutes=5,  priority=Priority.HIGH,
         due_date=today.replace(hour=9, minute=0)),
    # Recurring tasks
    Task(id="t6", title="Morning walk",        description="Daily walk around the block",
         pet_id="p1", duration_minutes=20, priority=Priority.HIGH,
         due_date=today.replace(hour=7, minute=30), recurrence="daily"),
    Task(id="t7", title="Nail trim",           description="Weekly grooming",
         pet_id="p2", duration_minutes=10, priority=Priority.MEDIUM,
         due_date=today.replace(hour=10, minute=0), recurrence="weekly"),
    # Conflict #1 — same pet: overlaps Luna's flea medication (9:00, 5 min)
    Task(id="c1", title="Vet check-in call",   description="Quick call with vet re: results",
         pet_id="p1", duration_minutes=10, priority=Priority.HIGH,
         due_date=today.replace(hour=9, minute=3)),
    # Conflict #2 — different pets: overlaps Mochi's nail trim (10:00, 10 min)
    Task(id="c2", title="Luna bath time",      description="Post-walk rinse",
         pet_id="p1", duration_minutes=15, priority=Priority.MEDIUM,
         due_date=today.replace(hour=10, minute=5)),
]

for task in tasks:
    scheduler.schedule_task(task)

# Mark one task complete to make status filtering interesting
scheduler.tasks["t3"].complete()

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

# --- Demonstrate sort_by_time ---
print("\n" + "=" * 44)
print("   sort_by_time  —  All tasks, earliest first")
print("=" * 44)
all_tasks = list(scheduler.tasks.values())
for task in scheduler.sort_by_time(all_tasks):
    time_str = task.due_date.strftime("%I:%M %p")
    print(f"  {time_str}  {task.title}")

print()
print("   sort_by_time  —  All tasks, latest first")
print("-" * 44)
for task in scheduler.sort_by_time(all_tasks, reverse=True):
    time_str = task.due_date.strftime("%I:%M %p")
    print(f"  {time_str}  {task.title}")

# --- Demonstrate filter_tasks ---
print("\n" + "=" * 44)
print("   filter_tasks  —  Luna's tasks only")
print("=" * 44)
for task in scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Luna")):
    status = "✓" if task.is_completed else "•"
    print(f"  {status} {task.due_date.strftime('%I:%M %p')}  {task.title}")

print()
print("   filter_tasks  —  Pending tasks, all pets")
print("-" * 44)
for task in scheduler.sort_by_time(scheduler.filter_tasks(status="pending")):
    print(f"  • {task.due_date.strftime('%I:%M %p')}  {task.title}")

print()
print("   filter_tasks  —  Completed tasks, all pets")
print("-" * 44)
completed = scheduler.filter_tasks(status="completed")
if completed:
    for task in scheduler.sort_by_time(completed):
        print(f"  ✓ {task.due_date.strftime('%I:%M %p')}  {task.title}")
else:
    print("  No completed tasks.")

print("\n" + "=" * 44)

# --- Demonstrate conflict detection ---
print("   get_conflicts  —  All pets")
print("=" * 44)
conflicts = scheduler.get_conflicts()
if conflicts:
    for msg in conflicts:
        print(f"  {msg}")
else:
    print("  No conflicts detected.")

print()
print("   get_conflicts  —  Same pet only")
print("-" * 44)
same_pet_conflicts = scheduler.get_conflicts(same_pet_only=True)
if same_pet_conflicts:
    for msg in same_pet_conflicts:
        print(f"  {msg}")
else:
    print("  No same-pet conflicts detected.")

print("\n" + "=" * 44)

# --- Demonstrate recurring task auto-spawn ---
print("   complete_task  —  Recurring task demo")
print("=" * 44)

for task_id, label in [("t6", "daily"), ("t7", "weekly")]:
    task = scheduler.tasks[task_id]
    print(f"\n  Completing '{task.title}' ({label}, due {task.due_date.strftime('%Y-%m-%d %I:%M %p')})")
    next_task = scheduler.complete_task(task_id)
    if next_task:
        print(f"  → Next occurrence auto-scheduled: '{next_task.title}' on {next_task.due_date.strftime('%Y-%m-%d %I:%M %p')}")

print()
print("  All Luna tasks after completing recurring walk:")
print("-" * 44)
for task in scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Luna")):
    status = "✓" if task.is_completed else "•"
    recur = f" [{task.recurrence}]" if task.recurrence else ""
    print(f"  {status} {task.due_date.strftime('%Y-%m-%d %I:%M %p')}  {task.title}{recur}")

print("\n" + "=" * 44)
