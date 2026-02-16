import pytest
from datetime import date
from pawpal_system import Task, Pet

def test_task_mark_complete():
    task = Task(title="Test Task", pet_id="pet1", task_type="test", due_date=date.today(), duration_minutes=10)
    assert not task.completed
    task.mark_complete()
    assert task.completed

def test_pet_add_task_increases_count():
    pet = Pet(name="Rex", species="Dog", breed="Lab", age=4)
    initial_count = len(pet.get_tasks())
    task = Task(title="Feed", pet_id=pet.pet_id, task_type="feed", due_date=date.today(), duration_minutes=5)
    pet.add_task(task)
    assert len(pet.get_tasks()) == initial_count + 1
