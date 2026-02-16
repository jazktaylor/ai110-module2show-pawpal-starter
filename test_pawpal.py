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
    def test_task_initialization():
        task = Task(title="Walk", pet_id="pet2", task_type="walk", due_date=date.today(), duration_minutes=30)
        assert task.title == "Walk"
        assert task.pet_id == "pet2"
        assert task.task_type == "walk"
        assert task.due_date == date.today()
        assert task.duration_minutes == 30
        assert not task.completed

    def test_pet_initialization():
        pet = Pet(name="Milo", species="Cat", breed="Siamese", age=2)
        assert pet.name == "Milo"
        assert pet.species == "Cat"
        assert pet.breed == "Siamese"
        assert pet.age == 2
        assert isinstance(pet.pet_id, str)
        assert pet.get_tasks() == []

    def test_pet_add_multiple_tasks():
        pet = Pet(name="Bella", species="Dog", breed="Beagle", age=3)
        task1 = Task(title="Feed", pet_id=pet.pet_id, task_type="feed", due_date=date.today(), duration_minutes=5)
        task2 = Task(title="Walk", pet_id=pet.pet_id, task_type="walk", due_date=date.today(), duration_minutes=20)
        pet.add_task(task1)
        pet.add_task(task2)
        tasks = pet.get_tasks()
        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks

    def test_pet_get_tasks_returns_copy():
        pet = Pet(name="Luna", species="Cat", breed="Maine Coon", age=5)
        task = Task(title="Groom", pet_id=pet.pet_id, task_type="groom", due_date=date.today(), duration_minutes=15)
        pet.add_task(task)
        tasks = pet.get_tasks()
        tasks.append(Task(title="Fake", pet_id=pet.pet_id, task_type="fake", due_date=date.today(), duration_minutes=1))
        # The pet's internal task list should not be affected
        assert len(pet.get_tasks()) == 1

    def test_task_mark_complete_idempotent():
        task = Task(title="Play", pet_id="pet3", task_type="play", due_date=date.today(), duration_minutes=10)
        task.mark_complete()
        assert task.completed
        # Marking complete again should not change the state
        task.mark_complete()
        assert task.completed
