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
I used AI to help create the UML classes and methods, implementing those methods, and writing test cases.
- What kinds of prompts or questions were most helpful?
Prompt to generate, and implement while giving it some context to work from.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When I was building the Pet class, the AI suggested just storing an owner_id string to represent the owner. That didn’t sit right with me—it felt like overkill for what I actually needed.

If I went that route, I’d have to keep looking up the owner every time I wanted basic info, which just adds unnecessary complexity.
- How did you evaluate or verify what the AI suggested?
I basically thought through how I’d use it in real code. For example, if I want something simple like pet.owner.name, using just an ID would turn that into a multi-step lookup.

So I kind of “tested it in my head” and realized it would be annoying to work with. That’s when I decided to just store the actual Owner object instead—it’s much more straightforward.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I focused on the main things the app is supposed to do:
	•	Adding tasks and making sure they show up sorted by time
	•	Scheduling overlapping tasks and checking if conflicts are detected
	•	Marking a task as complete and confirming it disappears from the active list
	•	Filtering tasks by priority
- Why were these tests important?
These are basically the core features of the app. If something like sorting or conflict detection is off, the whole scheduling system breaks down.

At that point, users could be getting incorrect information without even realizing it, which is a big problem.
**b. Confidence**

- How confident are you that your scheduler works correctly?
5
- What edge cases would you test next if you had more time?
A few things I’d want to dig into next:
	•	Two tasks at the exact same time and same priority—what happens there?
	•	Adding a task when no pet has been registered yet
	•	Tasks with zero or negative duration
	•	What happens when there are a lot of tasks (like 50+)—does the UI still work smoothly?
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Definitely the Scheduler class. It ended up being the central hub where everything connects—sorting, filtering, conflict detection, all in one place.

Once that was solid, the rest of the project became a lot easier to build. That decision to keep the logic centralized really paid off.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had more time I would improve the UI, add better styles, images, toast messages, icons, etc.
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
1. Which Copilot features were most effective?

The chat and inline suggestions were the most helpful once I had my design figured out. After defining things in the UML, like get_conflicts() and sort_by_time() in the Scheduler, Copilot could fill in the code pretty quickly because the structure was already clear.

It was also useful for smaller stuff, like setting up the Streamlit layout or writing simple dictionaries like PRIORITY_MAP in app.py. It saved time on repetitive code.

⸻

2. One AI suggestion you rejected or modified

One suggestion I pushed back on was using just an owner_id string in the Pet class. That’s something AI tends to default to since it’s more flexible, but for this project it didn’t really make sense.

I chose to store a direct Owner object inside Pet instead. It made the relationship clearer and easier to work with—like being able to access pet.owner.name directly without extra lookups. It just felt cleaner for the scale of this app.

⸻

3. How did separate chat sessions per phase help?

Keeping separate chat sessions actually helped a lot with staying organized. Each phase had its own focus, so things didn’t get mixed together.

For example, when I was working on the UML, I didn’t have to deal with UI suggestions. And when I moved on to features like conflict detection or sorting, I wasn’t dragging along half-finished ideas from earlier.

It felt like working on different whiteboards for each part of the project, which made everything clearer.

⸻

4. What did you learn about being the “lead architect”?

The biggest thing I learned is that AI can write code really fast, but it doesn’t really understand the bigger picture of your project.

It’ll suggest more complex solutions—like adding databases or APIs—when you don’t actually need them. So my role was to step in and keep things simple and focused.

I had to make the final calls on design choices, like keeping the Scheduler as the main control point or using direct object references instead of IDs.

In a way, it felt like the AI was a fast junior developer, and I was the one responsible for making sure everything stayed on track.
