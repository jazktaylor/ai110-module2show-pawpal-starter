from dataclasses import dataclass, field
from typing import List
from datetime import datetime, date

@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    pet_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    
    def add(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

@dataclass
class Task:
    title: str
    pet_id: str
    task_type: str
    due_date: date
    task_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    completed: bool = False
    
    def add(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def mark_complete(self):
        self.completed = True

@dataclass
class GroomingSchedule:
    pet_id: str
    task_type: str
    frequency_days: int
    schedule_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    tasks: List[Task] = field(default_factory=list)
    
    def create_task(self) -> Task:
        task = Task(
            title=f"{self.task_type} for pet",
            pet_id=self.pet_id,
            task_type=self.task_type,
            due_date=date.today()
        )
        self.tasks.append(task)
        return task

@dataclass
class DailyTasks:
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def get_today_tasks(self) -> List[Task]:
        return [t for t in self.tasks if t.due_date == date.today()]
    
    def get_pending_tasks(self) -> List[Task]:
        return [t for t in self.tasks if not t.completed]

@dataclass
class User:
    name: str
    user_id: str = field(default_factory=lambda: str(datetime.now().timestamp()))
    pets: List[Pet] = field(default_factory=list)
    schedules: List[GroomingSchedule] = field(default_factory=list)
    daily_tasks: DailyTasks = field(default_factory=DailyTasks)
    
    def add_pet(self, pet: Pet):
        self.pets.append(pet)
    
    def add_schedule(self, schedule: GroomingSchedule):
        self.schedules.append(schedule)