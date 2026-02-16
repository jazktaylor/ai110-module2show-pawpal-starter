# --- Basic Conflict Detection ---
def detect_conflicts(tasks):
	"""
	Detects tasks for the same pet that are scheduled at the same time (same due_date).
	Returns a list of tuples: (pet_id, due_date, [conflicting_tasks])
	"""
	from collections import defaultdict
	conflicts = []
	by_pet_and_date = defaultdict(list)
	for t in tasks:
		by_pet_and_date[(t.pet_id, t.due_date)].append(t)
	for (pet_id, due_date), tlist in by_pet_and_date.items():
		if len(tlist) > 1:
			conflicts.append((pet_id, due_date, tlist))
	return conflicts

# Example: detect and print conflicts
conflicts = detect_conflicts(owner.get_all_tasks())
if conflicts:
	print("\nTask Conflicts Detected:")
	for pet_id, due_date, tlist in conflicts:
		pet = owner.get_pet(pet_id)
		pet_name = pet.name if pet else pet_id
		print(f"- {pet_name} has {len(tlist)} tasks on {due_date}:")
		for t in tlist:
			print(f"    * {t.title} ({t.duration_minutes} min, Priority: {t.priority})")
else:
	print("\nNo task conflicts detected.")
def handle_recurring_tasks(owner):
	"""
	For each completed recurring task, schedule the next occurrence if not already present.
	"""
	for pet in owner.pets:
		for task in list(pet.get_tasks()):
			if task.frequency_days and task.completed:
				# Check if next occurrence already exists
				next_due = task.next_due_date()
				exists = any(
					t.title == task.title and t.due_date == next_due and t.pet_id == task.pet_id
					for t in pet.get_tasks()
				)
				if not exists:
					new_task = Task(
						title=task.title,
						pet_id=task.pet_id,
						task_type=task.task_type,
						due_date=next_due,
						duration_minutes=task.duration_minutes,
						frequency_days=task.frequency_days,
						priority=task.priority
					)
					pet.add_task(new_task)

# Call recurring task handler after initial setup
handle_recurring_tasks(owner)
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


# Add tasks out of order
from datetime import date, timedelta
from pawpal_system import Task

tasks_pet1 = [
	Task(title="Playtime", pet_id=pet1.pet_id, task_type="play", due_date=date.today() + timedelta(days=2), duration_minutes=30, priority="low"),
	Task(title="Morning Walk", pet_id=pet1.pet_id, task_type="walk", due_date=date.today(), duration_minutes=20, priority="high"),
	Task(title="Feeding", pet_id=pet1.pet_id, task_type="feed", due_date=date.today() + timedelta(days=1), duration_minutes=10, priority="normal"),
]
tasks_pet2 = [
	Task(title="Cuddle Time", pet_id=pet2.pet_id, task_type="cuddle", due_date=date.today() + timedelta(days=2), duration_minutes=25, priority="low"),
	Task(title="Litter Cleaning", pet_id=pet2.pet_id, task_type="clean", due_date=date.today(), duration_minutes=15, priority="high"),
	Task(title="Feeding", pet_id=pet2.pet_id, task_type="feed", due_date=date.today() + timedelta(days=1), duration_minutes=10, priority="normal"),
]


# Add two tasks for the same pet at the same time to test conflict detection
from pawpal_system import Scheduler

for task in tasks_pet1:
	pet1.add_task(task)
for task in tasks_pet2:
	pet2.add_task(task)

# Add two tasks for pet1 at the same time (today)
conflict_task1 = Task(title="Vet Visit", pet_id=pet1.pet_id, task_type="vet", due_date=date.today(), duration_minutes=60, priority="high")
conflict_task2 = Task(title="Training", pet_id=pet1.pet_id, task_type="train", due_date=date.today(), duration_minutes=30, priority="normal")
pet1.add_task(conflict_task1)
pet1.add_task(conflict_task2)

# Create Scheduler and add owner
sched = Scheduler()
sched.add_owner(owner)

# Print conflict warnings
warnings = sched.warn_on_task_conflicts()
if warnings:
	print("\nConflict Warnings:")
	for w in warnings:
		print(w)
else:
	print("\nNo conflicts detected by Scheduler.")

# Print all tasks sorted by due_date and priority
def sort_tasks(tasks):
	priority_order = {"high": 0, "normal": 1, "low": 2}
	return sorted(tasks, key=lambda t: (t.due_date, priority_order.get(t.priority, 1)))

print("\nAll tasks sorted by date and priority:")
for task in sort_tasks(owner.get_all_tasks()):
	pet = owner.get_pet(task.pet_id)
	pet_name = pet.name if pet else task.pet_id
	print(f"- {task.title} for {pet_name} (Due: {task.due_date}, Priority: {task.priority})")

# Print filtered tasks using Owner's filter_tasks
print(f"\nPending tasks for {pet1.name} (sorted):")
for task in sort_tasks(owner.filter_tasks(status='pending', pet_name=pet1.name)):
	print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")

print(f"\nAll overdue tasks for {pet2.name} (sorted):")
for task in sort_tasks(owner.filter_tasks(status='overdue', pet_name=pet2.name)):
	print(f"- {task.title} (Due: {task.due_date}, Priority: {task.priority})")

# Print today's schedule

# --- Task Filtering Logic ---
def filter_tasks(tasks, pet_id=None, status=None):
	"""
	Filter tasks by pet_id and status ('all', 'pending', 'completed', 'overdue').
	"""
	filtered = tasks
	if pet_id:
		filtered = [t for t in filtered if t.pet_id == pet_id]
	if status == 'pending':
		filtered = [t for t in filtered if not t.completed and not t.is_overdue()]
	elif status == 'completed':
		filtered = [t for t in filtered if t.completed]
	elif status == 'overdue':
		filtered = [t for t in filtered if t.is_overdue()]
	return filtered

print("\nToday's Schedule (with filtering):")
all_tasks = owner.get_all_tasks()
# Example: filter by pet1 and pending tasks
filtered = filter_tasks(all_tasks, pet_id=pet1.pet_id, status='pending')
print(f"\nPending tasks for {pet1.name}:")
for task in filtered:
	if task.is_today():
		print(f"- {task.title} ({task.duration_minutes} min, Priority: {task.priority})")

# Example: show all overdue tasks for pet2
filtered_overdue = filter_tasks(all_tasks, pet_id=pet2.pet_id, status='overdue')
print(f"\nOverdue tasks for {pet2.name}:")
for task in filtered_overdue:
	print(f"- {task.title} (was due {task.due_date}, Priority: {task.priority})")
