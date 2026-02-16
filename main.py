from pawpal_system import Owner, Pet

# Create an owner
owner = Owner(name="Alex", available_minutes_per_day=120)

# Create two pets
pet1 = Pet(name="Buddy", species="Dog", breed="Golden Retriever", age=3)
pet2 = Pet(name="Mittens", species="Cat", breed="Siamese", age=2)

# Add pets to the owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Print owner and pets info

# Add three tasks for each pet with different times
from datetime import date
from pawpal_system import Task

tasks_pet1 = [
	Task(title="Morning Walk", pet_id=pet1.pet_id, task_type="walk", due_date=date.today(), duration_minutes=20, priority="high"),
	Task(title="Feeding", pet_id=pet1.pet_id, task_type="feed", due_date=date.today(), duration_minutes=10, priority="normal"),
	Task(title="Playtime", pet_id=pet1.pet_id, task_type="play", due_date=date.today(), duration_minutes=30, priority="low"),
]
tasks_pet2 = [
	Task(title="Litter Cleaning", pet_id=pet2.pet_id, task_type="clean", due_date=date.today(), duration_minutes=15, priority="high"),
	Task(title="Feeding", pet_id=pet2.pet_id, task_type="feed", due_date=date.today(), duration_minutes=10, priority="normal"),
	Task(title="Cuddle Time", pet_id=pet2.pet_id, task_type="cuddle", due_date=date.today(), duration_minutes=25, priority="low"),
]

for task in tasks_pet1:
	pet1.add_task(task)
for task in tasks_pet2:
	pet2.add_task(task)

# Print today's schedule
print("\nToday's Schedule:")
for pet in owner.pets:
	print(f"\nTasks for {pet.name}:")
	for task in pet.get_tasks():
		if task.is_today():
			print(f"- {task.title} ({task.duration_minutes} min, Priority: {task.priority})")
