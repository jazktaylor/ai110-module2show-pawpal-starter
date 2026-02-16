
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime, date, timedelta
import uuid

@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    pet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    schedules: List['GroomingSchedule'] = field(default_factory=list)
    tasks: List['Task'] = field(default_factory=list)

    def add(self, **kwargs):
        """Update pet attributes from kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def add_schedule(self, schedule: 'GroomingSchedule'):
        """Add a grooming schedule to the pet."""
        self.schedules.append(schedule)

    def add_task(self, task: 'Task'):
        """Add a task to the pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List['Task']:
        """Return all tasks for the pet."""
        return self.tasks

    def get_pending_tasks(self) -> List['Task']:
        """Return all incomplete tasks for the pet."""
        return [t for t in self.tasks if not t.completed]

    def get_overdue_tasks(self) -> List['Task']:
        """Return all overdue tasks for the pet."""
        return [t for t in self.tasks if t.is_overdue()]

@dataclass
class Task:
    """
    Represents a single activity for a pet.
    """
    title: str
    pet_id: str
    task_type: str
    due_date: date
    duration_minutes: int
    frequency_days: Optional[int] = None  # How often this task repeats
    priority: str = "normal"  # "low", "normal", "high"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    completed: bool = False

    def add(self, **kwargs):
        """Update task attributes from kwargs."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def mark_complete(self, pet: 'Pet' = None):
        """
        Mark the task as completed. If the task is daily or weekly, auto-create the next occurrence.
        If a Pet instance is provided, the new task is added to the pet.
        """
        self.completed = True
        # Auto-create next occurrence for daily/weekly tasks
        if self.frequency_days in (1, 7) and pet is not None:
            next_due = self.next_due_date()
            # Avoid duplicate next occurrence
            exists = any(
                t.title == self.title and t.due_date == next_due and t.pet_id == self.pet_id
                for t in pet.get_tasks()
            )
            if not exists:
                new_task = Task(
                    title=self.title,
                    pet_id=self.pet_id,
                    task_type=self.task_type,
                    due_date=next_due,
                    duration_minutes=self.duration_minutes,
                    frequency_days=self.frequency_days,
                    priority=self.priority
                )
                pet.add_task(new_task)

    def is_today(self) -> bool:
        """Return True if the task is due today."""
        return self.due_date == date.today()

    def is_overdue(self) -> bool:
        """Return True if the task is overdue and not completed."""
        return self.due_date < date.today() and not self.completed

    def next_due_date(self) -> Optional[date]:
        """Return the next due date if the task is recurring."""
        if self.frequency_days:
            return self.due_date + timedelta(days=self.frequency_days)
        return None

@dataclass
class GroomingSchedule:
    pet_id: str
    task_type: str
    frequency_days: int
    duration_minutes: int
    priority: str = "normal"
    schedule_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    last_completed: Optional[date] = None
    
    def create_task(self, pet_name: str) -> Task:
        """Create a new task for this schedule."""
        task = Task(
            title=f"{self.task_type} for {pet_name}",
            pet_id=self.pet_id,
            task_type=self.task_type,
            due_date=date.today(),
            duration_minutes=self.duration_minutes,
            priority=self.priority
        )
        return task

    def needs_task_today(self) -> bool:
        """Return True if a task is due today based on frequency."""
        if self.last_completed is None:
            return True
        days_since = (date.today() - self.last_completed).days
        return days_since >= self.frequency_days

@dataclass
class DailyTasks:
    """Container for managing tasks across the system"""
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task):
        """Add a task to the system."""
        self.tasks.append(task)

    def get_today_tasks(self) -> List[Task]:
        """Return all tasks due today."""
        return [t for t in self.tasks if t.due_date == date.today()]

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks."""
        return [t for t in self.tasks if not t.completed]

    def get_today_pending(self) -> List[Task]:
        """Return incomplete tasks due today."""
        return [t for t in self.tasks if t.is_today() and not t.completed]

    def get_overdue_tasks(self) -> List[Task]:
        """Return overdue incomplete tasks."""
        return [t for t in self.tasks if t.is_overdue()]

    def remove_task(self, task_id: str):
        """Remove a task by its ID."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

@dataclass
class Owner:
    """
    Manages multiple pets and provides access to all their tasks.
    """
    name: str
    available_minutes_per_day: int
    owner_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pets: List[Pet] = field(default_factory=list)

    def filter_tasks(self, status: str = None, pet_name: str = None) -> List[Task]:
        """
        Filter all tasks by completion status ('pending', 'completed', 'overdue') or pet name.
        Returns a list of matching Task objects.
        """
        tasks = self.get_all_tasks()
        if pet_name:
            pet_ids = [pet.pet_id for pet in self.pets if pet.name == pet_name]
            tasks = [t for t in tasks if t.pet_id in pet_ids]
        if status == 'pending':
            tasks = [t for t in tasks if not t.completed and not t.is_overdue()]
        elif status == 'completed':
            tasks = [t for t in tasks if t.completed]
        elif status == 'overdue':
            tasks = [t for t in tasks if t.is_overdue()]
        return tasks

    def add_pet(self, pet: Pet):
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_pet(self, pet_id: str) -> Optional[Pet]:
        """Return a pet by its ID."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for all pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for all pets."""
        return [task for pet in self.pets for task in pet.get_pending_tasks()]

    def get_all_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks for all pets."""
        return [task for pet in self.pets for task in pet.get_overdue_tasks()]

    def assign_task_to_pet(self, pet_id: str, task: Task):
        """Assign a task to a specific pet."""
        pet = self.get_pet(pet_id)
        if pet:
            pet.add_task(task)

    def get_tasks_for_pet(self, pet_id: str) -> List[Task]:
        """Return all tasks for a specific pet."""
        pet = self.get_pet(pet_id)
        if pet:
            return pet.get_tasks()
        return []

    def generate_grooming_tasks(self) -> List[Task]:
        """Generate and assign grooming tasks for all pets."""
        new_tasks = []
        for pet in self.pets:
            for schedule in pet.schedules:
                if schedule.needs_task_today():
                    task = schedule.create_task(pet.name)
                    pet.add_task(task)
                    new_tasks.append(task)
        return new_tasks

    def get_daily_plan(self) -> dict:
        """Return an optimized daily schedule for the owner."""
        today_tasks = [t for t in self.get_all_pending_tasks() if t.is_today()]
        overdue_tasks = self.get_all_overdue_tasks()
        priority_order = {"high": 0, "normal": 1, "low": 2}
        all_tasks = overdue_tasks + today_tasks
        sorted_tasks = sorted(all_tasks, key=lambda t: (priority_order.get(t.priority, 1), t.due_date))
        scheduled = []
        total_time = 0
        for task in sorted_tasks:
            if total_time + task.duration_minutes <= self.available_minutes_per_day:
                scheduled.append(task)
                total_time += task.duration_minutes
        return {
            "scheduled_tasks": scheduled,
            "total_minutes": total_time,
            "remaining_minutes": self.available_minutes_per_day - total_time,
            "unscheduled_tasks": [t for t in sorted_tasks if t not in scheduled]
        }


# Scheduler class: the "brain" that manages and organizes tasks across pets and owners
class Scheduler:
    """
    Central system to retrieve, organize, and manage tasks across all pets and owners.
    """

    def __init__(self):
        """Initialize the Scheduler system."""
        self.owners = {}

    def warn_on_task_conflicts(self) -> list:
        """
        Lightweight conflict detection: returns a list of warning messages for pets with conflicting tasks (same due_date).
        Does not raise exceptions or crash the program.
        """
        warnings = []
        conflicts = self.detect_task_conflicts()
        for pet_id, due_date, tlist in conflicts:
            task_titles = ', '.join(t.title for t in tlist)
            warnings.append(
                f"Warning: Pet {pet_id} has {len(tlist)} tasks scheduled on {due_date}: {task_titles}"
            )
        return warnings

    def detect_task_conflicts(self) -> list:
        """
        Detects and returns a list of conflicts: (pet_id, due_date, [conflicting_tasks])
        where two or more tasks for the same pet are scheduled at the same time (same due_date).
        """
        from collections import defaultdict
        conflicts = []
        for owner in self.owners.values():
            for pet in owner.pets:
                by_date = defaultdict(list)
                for t in pet.get_tasks():
                    by_date[t.due_date].append(t)
                for due_date, tlist in by_date.items():
                    if len(tlist) > 1:
                        conflicts.append((pet.pet_id, due_date, tlist))
        return conflicts

    def add_owner(self, owner: Owner):
        """Add an owner to the system."""
        self.owners[owner.owner_id] = owner

    def get_owner(self, owner_id: str) -> Optional[Owner]:
        """Return an owner by their ID."""
        return self.owners.get(owner_id)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for all owners."""
        return [task for owner in self.owners.values() for task in owner.get_all_tasks()]

    def get_all_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks for all owners."""
        return [task for owner in self.owners.values() for task in owner.get_all_pending_tasks()]

    def get_all_overdue_tasks(self) -> List[Task]:
        """Return all overdue tasks for all owners."""
        return [task for owner in self.owners.values() for task in owner.get_all_overdue_tasks()]

    def generate_all_grooming_tasks(self) -> List[Task]:
        """Generate and assign grooming tasks for all owners."""
        return [task for owner in self.owners.values() for task in owner.generate_grooming_tasks()]

    def get_daily_plan_for_owner(self, owner_id: str) -> Optional[dict]:
        """Return the daily plan for a specific owner."""
        owner = self.get_owner(owner_id)
        if owner:
            return owner.get_daily_plan()
        return None

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort Task objects by their due_date attribute.
        """
        return sorted(tasks, key=lambda t: t.due_date)