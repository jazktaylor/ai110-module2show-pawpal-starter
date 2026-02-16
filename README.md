
# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

The Scheduler class now includes several advanced features:

- Efficient task retrieval using list comprehensions for all, pending, and overdue tasks across owners and pets.
- Automatic detection of scheduling conflicts for pets, with lightweight warnings instead of program crashes.
- Recurring task support: daily and weekly tasks are automatically rescheduled when completed.
- Flexible sorting and filtering of tasks by time, status, and pet.

These improvements make scheduling more robust, efficient, and user-friendly for pet owners.

## Testing PawPal+

To run the tests for PawPal+, use the following command:

```bash
python -m pytest
```

The test suite covers core scheduling behaviors, including task addition and editing, conflict detection, recurring task handling, and plan generation logic. This ensures the app remains reliable as you add features or refactor code.
## Confidence Level: ⭐⭐⭐⭐

# Features

- **Centralized Scheduling:**  
	The `Scheduler` class manages all owners, pets, and tasks, providing system-wide sorting, conflict detection, and daily planning.

- **Task Sorting:**  
	Tasks are sorted chronologically using the `sort_by_time()` method, ensuring schedules are always presented in order.

- **Conflict Detection:**  
	The scheduler automatically flags duplicate or overlapping tasks for the same pet on the same day, using `warn_on_task_conflicts()` and `detect_task_conflicts()`.

- **Recurring Tasks:**  
	Tasks can be set to repeat daily or weekly. When a recurring task is marked complete, the system auto-generates the next occurrence.

- **Priority-Based Planning:**  
	Daily plans are optimized based on task priority and available time, ensuring high-priority tasks are scheduled first.

- **Owner and Pet Management:**  
	Owners can add multiple pets, each with their own tasks and grooming schedules.

- **Grooming Schedule Automation:**  
	Grooming schedules automatically generate tasks for pets based on frequency and completion history.

- **Task Filtering:**  
	Tasks can be filtered by status (pending, completed, overdue) and by pet.

- **Overdue and Pending Tracking:**  
	The system tracks overdue and pending tasks for each pet and owner.

- **Streamlined UI Integration:**  
	All sorting, conflict detection, and planning algorithms are integrated with the Streamlit UI for real-time feedback and professional display.