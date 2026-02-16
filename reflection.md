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
    My scheduler considers several constraints:
        - **Time:** Each task has a due date and a duration in minutes. The scheduler checks the owner's available_minutes_per_day to avoid overbooking.
        - **Priority:** Tasks are sorted and scheduled based on their priority (high, normal, low). Overdue and high-priority tasks are scheduled first.
        - **Pet-specific preferences:** Tasks are linked to individual pets, so scheduling respects which pet needs which care.
        - **Recurring tasks:** The scheduler automatically handles recurring tasks, ensuring future occurrences are scheduled if needed.
        - **Conflict detection:** It checks for tasks scheduled at the same time for the same pet and warns about conflicts.
- How did you decide which constraints mattered most?
    I decided which constraints mattered most by focusing on what would make the scheduler practical for daily pet care. Time and priority were essential to prevent overbooking and ensure urgent tasks are handled first. Pet-specific preferences were important for personalized care. Recurring tasks and conflict detection were added to automate routine scheduling and avoid overlapping tasks, based on common real-life needs and feedback from testing.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    The Scheduler class methods get_all_tasks, get_all_pending_tasks, get_all_overdue_tasks, and generate_all_grooming_tasks have been refactored to use list comprehensions for improved readability and performance. This makes the code cleaner and more efficient.
- Why is that tradeoff reasonable for this scenario?
    List comprehensions are great for simplicity and speed, but explicit loops offer more control and flexibility, especially for complex or large-scale operations.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    For design brainstorming, I relied more on my own ideas, but AI was useful for reviewing class relationships and suggesting improvements. I used AI tools mainly for debugging and refactoring. When I encountered errors or needed to optimize code, I asked for suggestions and explanations. AI helped clarify logic, propose fixes, and generate unit tests. 
- What kinds of prompts or questions were most helpful?
    The more specfic my prompts were, the more helpful AI was. Using the prompts provided in the Project checklist helped me greatly and allowed me to use similar prompt structure when creating my own. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    One moment where I did not accept an AI suggestion as-is was when the AI recommended combining all task lists into a single global collection. I realized this would make it harder to track which tasks belonged to which pet and owner, so I kept tasks organized by pet and owner instead.
- How did you evaluate or verify what the AI suggested?
    I evaluated the suggestion by considering the impact on data structure clarity and maintainability.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    I tested behaviors such as adding pets and tasks, scheduling tasks based on priority and available time, detecting conflicts when tasks overlap, handling recurring tasks, filtering tasks by status (pending, completed, overdue), and sorting tasks by due date and priority. 
- Why were these tests important?
    These tests were important to ensure the scheduler works reliably for daily planning and handles edge cases like overlapping tasks or overdue items.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    Due to the combined usage with AI, I rated my confidence level a 4 out of 5 stars. 
- What edge cases would you test next if you had more time?
    If I had more time, I would test edge cases such as:
        - Tasks with overlapping durations for the same pet.
        - Recurring tasks with unusual frequencies (e.g., every 2 days, monthly).
        - Tasks with missing or invalid data (e.g., no due date, negative duration).
        - Handling task completion and rescheduling for recurring tasks.
        - Detecting conflicts across multiple owners or pets.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    I am most satisified with the structure of the project. The clear organization of classes and relationships made it easy to extend features, maintain code, and ensure data consistency. 

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    If I had another iteration, I would like to improve the Streamlit App Deployment and user interface for a smoother experience. I would also redesign parts of the scheduler to better handle edge cases. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    One important thing I learned bout working with Ai on this project is the importance of human input. Although AI is capable of completing the project, it is still essential to review, adapt, and sometimes reject its suggestions to ensure clarity or maintainability. However, the use of thoughtful, specific prompts does yield better responses. 