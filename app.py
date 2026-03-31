import uuid
from datetime import date, datetime, time

import streamlit as st

from pawpal_system import Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Session-state bootstrap — create real backend objects once per session
# ---------------------------------------------------------------------------
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "owner" not in st.session_state:
    st.session_state.owner = None

if "pet" not in st.session_state:
    st.session_state.pet = None

# ---------------------------------------------------------------------------
# Owner + Pet setup
# ---------------------------------------------------------------------------
st.subheader("Owner & Pet")

col_o, col_p, col_s = st.columns(3)
with col_o:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_p:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_s:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save owner & pet"):
    owner = Owner(id=str(uuid.uuid4()), name=owner_name, email="", phone="")
    pet = Pet(
        id=str(uuid.uuid4()),
        name=pet_name,
        species=species,
        breed="",
        birth_date=date.today(),
        owner=owner,
    )
    owner.add_pet(pet)
    st.session_state.scheduler.register_owner(owner)
    st.session_state.scheduler.register_pet(pet)
    st.session_state.owner = owner
    st.session_state.pet = pet
    st.success(f"Saved {owner_name} and {pet_name}!")

st.divider()

# ---------------------------------------------------------------------------
# Add a Task
# ---------------------------------------------------------------------------
st.subheader("Schedule a Task")

PRIORITY_MAP = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority_str = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    due_time = st.time_input("Due time", value=time(9, 0))

if st.button("Add task"):
    pet = st.session_state.pet
    if pet is None:
        st.error("Please save an owner & pet first.")
    else:
        due_dt = datetime.combine(date.today(), due_time)
        task = Task(
            id=str(uuid.uuid4()),
            title=task_title,
            description="",
            pet_id=pet.id,
            duration_minutes=int(duration),
            priority=PRIORITY_MAP[priority_str],
            due_date=due_dt,
        )
        st.session_state.scheduler.schedule_task(task)
        st.success(f"Added '{task_title}' ({priority_str}, {due_time.strftime('%I:%M %p')})")

# Show current tasks
pet = st.session_state.pet
scheduler = st.session_state.scheduler
if pet:
    tasks = pet.get_tasks(scheduler)
    if tasks:
        st.write("Current tasks:")
        st.table([
            {
                "Title": t.title,
                "Priority": t.priority.name,
                "Due": t.due_date.strftime("%I:%M %p"),
                "Duration (min)": t.duration_minutes,
            }
            for t in tasks
        ])
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Generate Daily Plan
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    pet = st.session_state.pet
    if pet is None:
        st.error("Please save an owner & pet first.")
    elif not pet.get_tasks(scheduler):
        st.warning("No tasks scheduled yet. Add some tasks above.")
    else:
        plan = scheduler.generate_daily_plan(pet.id)
        if not plan:
            st.info("No tasks due today.")
        else:
            st.success(f"Today's plan for **{pet.name}** ({len(plan)} tasks)")
            for i, task in enumerate(plan, 1):
                overdue = " ⚠️ overdue" if task.is_overdue() else ""
                st.markdown(
                    f"**{i}. {task.title}**{overdue}  \n"
                    f"Priority: `{task.priority.name}` · "
                    f"Due: `{task.due_date.strftime('%I:%M %p')}` · "
                    f"Duration: `{task.duration_minutes} min`"
                )

        overdue_tasks = scheduler.get_overdue_tasks()
        if overdue_tasks:
            st.warning(f"{len(overdue_tasks)} overdue task(s) — consider rescheduling.")
