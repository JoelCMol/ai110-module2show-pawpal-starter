# PawPal+ Project Reflection

## 1. System Design

- Add a dog, track food/water intake, next pet visit
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
I designed four main classes for PawPal+:
- **Task** – Represents a single pet care activity. It stores things like due date, duration, priority, and recurrence. It can mark itself complete, be rescheduled, and check if it’s overdue.
- **Pet** – Stores basic pet info like name, species, breed, and birth date. It can calculate its age and get its tasks, but it doesn’t handle scheduling itself.
- **Owner** – Represents the user. It stores contact info and a list of pets, with simple methods to add, remove, and view pets.
- **Scheduler** – Handles all the scheduling work. It manages tasks, finds upcoming or overdue ones, sends reminders, and creates a daily plan for each pet.

Key idea: Pet and Owner mainly store data, while Scheduler handles the logic. I used IDs (like `pet_id` and `owner_id`) instead of direct links between objects to keep things flexible and less tightly connected.

**b. Design changes**

Three main changes were made after reviewing the design:

1. Scheduler is now the central hub
Originally, the Scheduler only had a simple list of tasks, so it couldn’t easily find pets or owners. Now it stores tasks, pets, and owners in dictionaries. This makes it easy to look things up and send reminders.

2. Pet now links directly to Owner
Before, Pet only stored an owner_id (a string), which was hard to use. Now it keeps a direct reference to the Owner object, making the connection clearer and easier to work with.

3. Priority uses an enum instead of text
Priority used to be strings like “high” or “low,” which caused sorting problems. Now it uses a numbered enum (LOW=1, MEDIUM=2, HIGH=3), so tasks can be sorted correctly and invalid values are avoided.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The scheduler keeps all tasks in a plain Python dictionary in memory — fast and simple, but everything disappears the moment the program stops. There's no file or database, so you can't pick up where you left off between runs.
- Why is that tradeoff reasonable for this scenario?
This is reasonable because we have not implemented a backend for our web app to use.

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
