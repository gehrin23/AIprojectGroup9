**onboarding.pdf**

**File Purpose:**
This file contains the CreateCourse class, responsible for creating a new course in the Django App. The class takes post data as input and checks if it's well-formed before creating the course.

**Key Functions/Methods and Their Responsibilities:**

* `__init__(self, post_data)`: Initializes the class with post data and sets up instance variables.
* `wellFormed(self)`: Verifies if the provided data is well-formed. Checks for missing information, invalid date ranges, and incorrect credit values.
* `create_course(self)`: Creates a new course in the Django App if the data is well-formed.
* `date_check(self)`: Validates the start and end dates of the course to ensure they are not earlier than the current date or after each other.
* `credit_check(self)`: Verifies that the credit values are valid, i.e., whole numbers greater than zero, with a maximum of two digits.
* `course_id_check(self)`: Checks if the provided course ID and name do not already exist in the database.

**Inputs/Outputs/Side Effects:**

* Input: Post data containing courseId, courseName, credits, startDate, and endDate.
* Output: A new course object or an error message indicating why the creation failed.
* Side effects:
	+ Creates a new course in the Django App if the data is well-formed.
	+ Sets the `message` attribute to indicate any errors or successes.

**Design Patterns/Dependencies:**

* The class uses the Course model from the Django App (django_app.models.Course) to create and validate courses.

**Cohesion/Coupling:**
The CreateCourse class has a high level of cohesion, as it focuses on creating a new course based on provided data. It has minimal coupling with other classes or external dependencies, making it a self-contained unit.

Note: The code is well-structured, but some inline comments could be added to explain specific logic and edge cases.