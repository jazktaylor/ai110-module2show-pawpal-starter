import streamlit as st
from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

# Owner creation and storage
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Owner's available minutes per day", min_value=1, max_value=1440, value=120)
if "owner" not in st.session_state or st.session_state.owner.name != owner_name:
    st.session_state.owner = Owner(name=owner_name, available_minutes_per_day=available_minutes)

# Pet creation and storage
st.markdown("### Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="Mixed")
age = st.number_input("Age", min_value=0, max_value=50, value=2)

if "pets" not in st.session_state:
    st.session_state.pets = []

if st.button("Add Pet"):
    # Check if pet already exists by name
    if not any(p.name == pet_name for p in st.session_state.pets):
        new_pet = Pet(name=pet_name, species=species, breed=breed, age=age)
        st.session_state.pets.append(new_pet)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet: {pet_name}")
    else:
        st.info(f"Pet '{pet_name}' already exists.")

if st.session_state.pets:
    st.write("Current pets:")
    st.table([{"Name": p.name, "Species": p.species, "Breed": p.breed, "Age": p.age} for p in st.session_state.pets])
else:
    st.info("No pets yet. Add one above.")

# Task scheduling UI
st.markdown("### Schedule a Task for a Pet")
if st.session_state.pets:
    pet_options = {f"{p.name} ({p.species})": p for p in st.session_state.pets}
    selected_pet_label = st.selectbox("Select pet", list(pet_options.keys()))
    selected_pet = pet_options[selected_pet_label]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
    with col3:
        priority = st.selectbox("Priority", ["low", "normal", "high"], index=1, key="priority")

    if st.button("Add Task"):
        from datetime import date
        new_task = Task(title=task_title, pet_id=selected_pet.pet_id, task_type="custom", due_date=date.today(), duration_minutes=int(duration), priority=priority)
        selected_pet.add_task(new_task)
        st.success(f"Added task '{task_title}' for {selected_pet.name}")

    # Show tasks for selected pet
    if selected_pet.get_tasks():
        st.write(f"Current tasks for {selected_pet.name}:")
        st.table([{"Title": t.title, "Duration": t.duration_minutes, "Priority": t.priority, "Completed": t.completed} for t in selected_pet.get_tasks()])
    else:
        st.info(f"No tasks for {selected_pet.name} yet.")
else:
    st.info("Add a pet before scheduling tasks.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()
...existing code...
