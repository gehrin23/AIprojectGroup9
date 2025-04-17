```javascript
// Select DOM elements
const taskTableBody = document.querySelector('#task-table-body'); // Tasks table
const addTaskForm = document.querySelector('#add-task-form'); // Add task form
const filterForm = document.querySelector('#task-filter-form'); // Filter form
const currentMonthLabel = document.querySelector('#current-month'); // Calendar month label
const calendarGrid = document.querySelector('.calendar-grid'); // Calendar grid

// Popup elements
let popup = null; // Task popup for calendar

// Sample tasks (replace with real data later)
const tasks = {
    '2024-12-02': ['Task 1: Finish project', 'Task 2: Submit report'],
    '2024-12-15': ['Task 1: Prepare presentation'],
    '2024-12-25': ['Task 1: Celebrate Christmas!']
};

// Month names
const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
];

// Date variables
let today = new Date();
let currentYear = today.getFullYear();
let currentMonth = today.getMonth();

/**
 * Renders tasks from the tasks object into the task table.
 */
function renderTasks() {
    if (!taskTableBody) return;

    taskTableBody.innerHTML = ''; // Clear the task table

    Object.keys(tasks).forEach(date => {
        tasks[date].forEach(task => {
            const row = `
                <tr>
                    <td>${task}</td>
                    <td>${date}</td>
                    <td>
                        <button onclick="deleteTask('${date}', '${task}')">Delete</button>
                    </td>
                </tr>
            `;
            taskTableBody.innerHTML += row;
        });
    });
}

/**
 * Adds a new task to the tasks object.
 * @param {Event} event - The form submission event.
 */
function addTask(event) {
    event.preventDefault();

    const form = event.target;
    const taskName = form['task-name'].value;
    const dueDate = form['due-date'].value;

    if (!tasks[dueDate]) tasks[dueDate] = [];
    tasks[dueDate].push(taskName);

    form.reset(); // Reset form fields
    updateTasksAndCalendar(); // Sync tasks with the calendar and task list
}

/**
 * Deletes a task from the tasks object.
 * @param {string} date - The date of the task to delete.
 * @param {string} taskName - The name of the task to delete.
 */
function deleteTask(date, taskName) {
    tasks[date] = tasks[date].filter(task => task !== taskName);
    if (tasks[date].length === 0) delete tasks[date]; // Remove the date if no tasks remain
    updateTasksAndCalendar();
}

/**
 * Filters tasks based on specified criteria.
 * @param {Event} event - The form submission event.
 */
function filterTasks(event) {
    event.preventDefault();

    const status = filterForm['status'].value;
    const dueDate = filterForm['due-date'].value;

    // Filter logic here (if needed)
    console.log(`Filter applied: Status - ${status}, Due Date - ${dueDate}`);
    renderTasks();
}

/**
 * Renders the calendar for a given month and year.
 * @param {number} year - The year to render.
 * @param {number} month - The month to render (0-11).
 */
function renderCalendar(year, month) {
    if (!calendarGrid) return;

    calendarGrid.innerHTML = ''; // Clear the calendar grid

    currentMonthLabel.textContent = `${monthNames[month]} ${year}`; // Update month label

    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPreviousMonth = new Date(year, month, 0).getDate();

    // Leading days from the previous month
    for (let i = firstDayOfMonth - 1; i >= 0; i--) {
        const daySlot = createDaySlot(daysInPreviousMonth - i, 'prev-month');
        calendarGrid.appendChild(daySlot);
    }

    // Current month days
    for (let day = 1; day <= daysInMonth; day++) {
        const fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const daySlot = createDaySlot(day, 'current-month', fullDate);

        if (tasks[fullDate]) {
            const dot = document.createElement('div');
            dot.classList.add('task-dot');
            daySlot.appendChild(dot);
        }

        calendarGrid.appendChild(daySlot);
    }

    // Trailing days from the next month
    const totalSlots = calendarGrid.children.length;
    const trailingDays = 42 - totalSlots; // Ensure 6 rows of 7 slots
    for (let day = 1; day <= trailingDays; day++) {
        const daySlot = createDaySlot(day, 'next-month');
        calendarGrid.appendChild(daySlot);
    }
}

/**
 * Creates a day slot element.
 * @param {number} day - The day number to display.
 * @param {string} type - The type of the day slot ('prev-month', 'current-month', 'next-month').
 * @param {string|null} fullDate - The full date string (YYYY-MM-DD), used for current month days.
 * @returns {HTMLElement} - The created day slot element.
 */
function createDaySlot(day, type, fullDate = null) {
    const daySlot = document.createElement('div');
    daySlot.classList.add('day-slot', type);
    daySlot.textContent = day;

    if (type === 'current-month' && fullDate) {
        // Add click event to show popup
        daySlot.addEventListener('click', () => {
            const taskList = tasks[fullDate] || [];
            showPopup(fullDate, taskList);
        });
    }

    return daySlot;
}

/**
 * Shows a popup with tasks for a specific date.
 * @param {string} date - The date string (YYYY-MM-DD).
 * @param {Array<string>} taskList - The list of tasks for the given date.
 */
function showPopup(date, taskList) {
    if (popup) popup.remove(); // Remove existing popup

    popup = document.createElement('div');
    popup.classList.add('task-popup');
    popup.innerHTML = `
        <h3>Tasks for ${date}</h3>
        <ul>
            ${taskList.map(task => `<li>${task}</li>`).join('') || '<li>No tasks</li>'}
        </ul>
        <button id="close-popup">Close</button>
    `;

    document.body.appendChild(popup);

    document.querySelector('#close-popup').addEventListener('click', () => {
        popup.remove();
        popup = null;
    });
}

/**
 * Updates both the tasks table and the calendar.
 */
function updateTasksAndCalendar() {
    renderTasks(); // Update tasks table
    renderCalendar(currentYear, currentMonth); // Update calendar
}

// Event listeners
if (addTaskForm) addTaskForm.addEventListener('submit', addTask);
if (filterForm) filterForm.addEventListener('submit', filterTasks);

// Initial rendering
renderTasks();
renderCalendar(currentYear, currentMonth);
```

### Onboarding PDF Summary

#### Overall File Purpose
This JavaScript file manages the functionality of a task management system integrated with a calendar. It handles adding, deleting, and filtering tasks, as well as displaying them in both a tabular format and a grid-based calendar view.

#### Key Functions/Methods and Their Responsibilities
1. **`renderTasks()`**: Renders tasks from the `tasks` object into the task table.
2. **`addTask(event)`**: Adds a new task to the `tasks` object based on form input.
3. **`deleteTask(date, taskName)`**: Deletes a specific task from the `tasks` object.
4. **`filterTasks(event)`**: Filters tasks based on specified criteria (currently logs to console).
5. **`renderCalendar(year, month)`**: Renders the calendar for a given month and year.
6. **`createDaySlot(day, type, fullDate = null)`**: Creates a day slot element with optional click event for current month days.
7. **`showPopup(date, taskList)`**: Shows a popup with tasks for a specific date.
8. **`updateTasksAndCalendar()`**: Updates both the tasks table and the calendar.

#### Inputs/Outputs/Side Effects
- **Inputs**:
  - User input from forms (add task, filter tasks).
  - Date values for rendering calendar and tasks.
- **Outputs**:
  - Updated HTML content in the task table and calendar grid.
  - Popup with tasks for a specific date.
- **Side Effects**:
  - Modifies the DOM to reflect changes in tasks and calendar.
  - Logs filter criteria to the console.

#### Design Patterns, Dependencies
- **Design Patterns**: The code follows a procedural design pattern, focusing on individual functions that perform specific tasks. It also uses event-driven programming for handling user interactions.
- **Dependencies**: The script relies on DOM manipulation methods provided by the browser environment (e.g., `document.querySelector`, `addEventListener`).

#### Cohesion and Coupling
- **Cohesion**: High cohesion is observed as each function has a clear and specific responsibility related to task management or calendar rendering.
- **Coupling**: Low coupling exists between functions. For example, `renderTasks()` and `renderCalendar()` are independent but both depend on the `tasks` object. The script avoids tight coupling by using global variables like `currentYear` and `currentMonth`.