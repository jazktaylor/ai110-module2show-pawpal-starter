# PawPal+ Project Reflection

## 1. System Design
- Add a pet with detailed descriptions
- Add pet care schedule (grooming, feeding, going for walks...)
- See tasks for the day

**a. Initial design**

- Briefly describe your initial UML design.
    Overall, the design follows a clear ownership hierarchy (User → Pet → Task/Schedule) with separation of concerns between data storage (Pet, Task), automation (GroomingSchedule), and presentation/aggregation (DailyTasks).

- What classes did you include, and what responsibilities did you assign to each?
    - Pet - Stores pet info with add() method and CRUD operations
    - Task - Manages grooming and care tasks with add() method and completion tracking
    - GroomingSchedule - Handles recurring schedules that create tasks
    - DailyTasks - Displays and filters tasks for today
    - User - Root entity that owns pets and accesses all features

**b. Design changes**

- Did your design change during implementation?
    Yes
- If yes, describe at least one change and why you made it.
    I fixed the missing relationships and the logic bottlenecks by implementing: 
    - Duration & Priority - Tasks now have duration_minutes and priority fields for realistic scheduling
    - Pet-Schedule Link - Moved schedules from User to Pet (schedules belong to specific pets)
    - Owner Constraints - Added available_minutes_per_day to User for time-based planning
    - UUID IDs - Replaced timestamp IDs with UUIDs to eliminate collision risk
    
    - Task-by-Pet Filtering - New get_tasks_for_pet() method to query tasks by specific pet
    - Daily Planning - New get_daily_plan() method that:
        Prioritizes high-priority and overdue tasks
        Fits tasks into available time budget
        Returns scheduled + unscheduled tasks
    - Grooming Auto-Generation - generate_grooming_tasks() creates tasks from schedules based on frequency
    - Task Utilities - Added is_today(), is_overdue(), get_today_pending(), get_overdue_tasks()
    - Data Consistency - Single task collection in DailyTasks (no more duplication)

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    The Scheduler class methods get_all_tasks, get_all_pending_tasks, get_all_overdue_tasks, and generate_all_grooming_tasks have been refactored to use list comprehensions for improved readability and performance. This makes the code cleaner and more efficient.
- Why is that tradeoff reasonable for this scenario?
    List comprehensions are great for simplicity and speed, but explicit loops offer more control and flexibility, especially for complex or large-scale operations.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
