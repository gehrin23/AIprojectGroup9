AcceptanceTestLogin.py
=======================

File purpose: This file contains test cases for the login functionality of the Django application. The tests are designed to ensure that the login page behaves as expected and that the correct redirection URL is returned after successful authentication.

Key functions/methods and their responsibilities:

* setUp(): Initializes the client object and creates three users with different roles (TA, Instructor, Admin).
* test_ta_login_success(): Tests that a TA user can successfully log in and redirect to the dashboard page.
* test_instructor_login_success(): Tests that an instructor user can successfully log in and redirect to the dashboard page.
* test_admin_login_success(): Tests that an admin user can successfully log in and redirect to the dashboard page.
* test_login_invalid_credentials(): Tests that an invalid username or password will result in a 200 response containing "Invalid Username Or Password" message.
* test_login_missing_fields(): Tests that missing username or password fields will result in a 200 response containing "Invalid Username Or Password" message.
* test_redirect_url_for_undefined_role(): Tests that an undefined role user will redirect to the dashboard page after logging in.
* tearDown(): Deletes all users created during testing.

Inputs/outputs/side effects:

* Inputs: Username, password, and role name.
* Outputs: Redirection URL after successful authentication or "Invalid Username Or Password" message if the credentials are invalid or missing fields.
* Side effects: Creates three users with different roles, logs in with each user, and redirects to the dashboard page.

Design patterns, dependencies:

* The test cases use the Django test client object to simulate HTTP requests and check the response status code and redirection URL.
* The test cases also use the User model from django_app.models to create users with different roles.

Cohesion and coupling:

* Cohesion: The class has a clear responsibility (testing login functionality) and its methods are well-structured and focused on that responsibility.
* Coupling: The class depends on the Django test client object and User model to perform testing and create users, respectively. However, these dependencies are necessary for the class to function properly.